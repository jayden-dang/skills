#!/usr/bin/env python3
# @skills-linter: check-trace sha256:b3245a8b8de8
"""check-trace — requirements traceability linter.

Sources of truth:
  <specsDir>/<feature>/requirements.md   defines requirement IDs (**CODE-N.M**)
  <specsDir>/fixes.md                    optional shared home for tier-1 fix/guard requirements

References:
  <specsDir>/<feature>/tasks.md          task footers: _Requirements: CODE-N.M, CODE-N.M_
  test files (globs)                     IDs in tags/annotations/names/comments, e.g. @CODE-N.M,
                                          annotate('CODE-N.M', ...), /// REQ: CODE-N.M

Checks:
  E1  a task or test cites an ID that is not defined in any requirements file
  E2  a requirements file with Status Implemented/Shipped has a requirement with zero test references
  E3  the same ID is defined more than once
  W1  a requirements file with Status Approved has a requirement not cited by any task
  W2  a requirements file is missing a Status line or feature code

Exit code 1 on any error (and on warnings with --strict), 0 otherwise.

Usage: python3 check_trace.py [--strict] [--json] [--root <repo-root>]
Config (optional): docs/agents/trace.json
  { "specsDir": "docs/specs", "testGlobs": ["tests/", "e2e/", "src/"], "testFilePattern": "\\.(test|spec)\\.|/tests?/|/e2e/|_test\\.",
    "ignore": ["fixtures/", "some.test.ts"] }
  ignore: repo-relative path substrings additionally excluded from the test-file
  scan (e.g. fixture-bearing files that legitimately cite unknown/example IDs).
  Off by default; applied on top of testGlobs/testFilePattern, never in place of them.

This module has no top-level side effects: importing it runs no CLI.
"""
import json
import os
import re
import sys

DEFAULTS = {
    "specsDir": "docs/specs",
    # Directories scanned for test files (relative to root).
    "testGlobs": ["tests", "test", "e2e", "src", "src-tauri", "crates", "app", "lib", "packages"],
    # A file is a test file if its repo-relative path matches this regex.
    "testFilePattern": r"(\.(test|spec)\.[cm]?[jt]sx?$)|([/\\]tests?[/\\])|([/\\]e2e[/\\])|(_test\.(rs|go|py)$)|(\.rs$)",
    # Repo-relative path substrings to additionally exclude from the test-file scan
    # (e.g. fixture-bearing files that legitimately mention unknown/example IDs).
    "ignore": [],
}

# No trailing \b: markdown italics footers end `..._`, and `_` is a word char,
# which would silently drop the last ID on the line. Guard against partial
# number matches with a lookahead instead.
ID_RE = re.compile(r"\b([A-Z][A-Z0-9]{1,11})-(\d+)\.(\d+)(?![.\d])", re.ASCII)
SKIP_DIRS = {"node_modules", ".git", "dist", "build", "target", "coverage", ".next", ".skills", "vendor"}

_STATUS_RE = re.compile(r"^Status:\s*(Draft|Approved|Implemented|Shipped)", re.MULTILINE)
_CODE_RE = re.compile(r"^Feature code:\s*([A-Z][A-Z0-9]{1,11})", re.MULTILINE)
_STRIKETHROUGH_RE = re.compile(r"~~.*?~~")
_BOLD_ID_RE = re.compile(r"\*\*([A-Z][A-Z0-9]{1,11}-\d+\.\d+)\*\*", re.ASCII)


def _walk(dir_, predicate, root):
    """Recursively collect files under dir_ for which predicate(repo-relative path) is true.

    Entries are visited in name-sorted order at each directory level (files and
    subdirectories interleaved, recursing into a subdirectory as soon as it's
    reached). os.scandir() yields entries in raw filesystem/inode order, which
    is not stable across machines, so this sorts explicitly: the sort is what
    makes "first" deterministic whenever a directory holds more than one
    matching candidate (e.g. which file an E1's example citation names, or the
    order of the errors/warnings arrays)."""
    out = []

    def _recurse(d):
        try:
            entries = sorted(os.scandir(d), key=lambda e: e.name)
        except OSError:
            return
        for e in entries:
            if e.name.startswith(".") and e.name != ".":
                continue
            full = os.path.join(d, e.name)
            if e.is_dir(follow_symlinks=False):
                if e.name not in SKIP_DIRS:
                    _recurse(full)
            elif predicate(os.path.relpath(full, root)):
                out.append(full)

    _recurse(dir_)
    return out


def extract_ids(text):
    """Return every CODE-N.M requirement ID found in text, in order of appearance."""
    return [m.group(0) for m in ID_RE.finditer(text)]


class ConfigError(Exception):
    """Raised by load_config on an unparseable trace.json.

    load_config itself never calls sys.exit — the CLI is responsible for catching this
    and translating it into an exit code + stderr message.
    """


def load_config(root):
    """Load docs/agents/trace.json (optional), shallow-merged over DEFAULTS.

    Raises ConfigError, never exits, on unparseable JSON.
    """
    p = os.path.join(root, "docs/agents/trace.json")
    if not os.path.exists(p):
        return DEFAULTS
    try:
        with open(p, "r", encoding="utf-8") as fh:
            user = json.load(fh)
    except (OSError, ValueError) as exc:
        raise ConfigError(f"could not parse {p}: invalid JSON") from exc
    return {**DEFAULTS, **user}


def _collect_requirement_files(specs_dir, root):
    """Walk specsDir for requirements.md/fixes.md files.

    Returns (defined, req_files, warnings, errors):
      defined    id -> {"file": rel, "status": status}
      req_files  [{"rel", "status", "ids"}, ...]
      warnings   W2 (missing Status/Feature code)
      errors     E3 (duplicate definition)

    Only bold-defined IDs (**CODE-N.M**) count as definitions; struck-through
    (~~**CODE-N.M**~~) are retired and deliberately excluded from coverage.
    """
    defined = {}
    definition_sites = {}  # id -> [rel, ...], for E3 duplicate detection
    req_files = []
    warnings = []
    errors = []

    requirement_files = _walk(
        specs_dir, lambda rel: rel.endswith("requirements.md") or rel.endswith("fixes.md"), root
    )
    for file in requirement_files:
        rel = os.path.relpath(file, root)
        with open(file, "r", encoding="utf-8") as fh:
            text = fh.read()
        status_match = _STATUS_RE.search(text)
        code_match = _CODE_RE.search(text)
        status = status_match.group(1) if status_match else None
        if not status_match and not rel.endswith("fixes.md"):
            warnings.append(f'W2 {rel}: missing "Status:" line')
        if not code_match and not rel.endswith("fixes.md"):
            warnings.append(f'W2 {rel}: missing "Feature code:" line')

        ids = []
        scannable = _STRIKETHROUGH_RE.sub("", text)
        for m in _BOLD_ID_RE.finditer(scannable):
            id_ = m.group(1)
            ids.append(id_)
            definition_sites.setdefault(id_, []).append(rel)
            defined[id_] = {"file": rel, "status": status}
        req_files.append({"rel": rel, "status": status, "ids": ids})

    for id_, sites in definition_sites.items():
        if len(sites) > 1:
            uniq = list(dict.fromkeys(sites))
            errors.append(f"E3 duplicate definition of {id_} in: {', '.join(uniq)}")

    return defined, req_files, warnings, errors


def _collect_task_refs(specs_dir, root):
    """Walk specsDir for tasks.md files; collect id -> [rel, ...] from `_Requirements:` footers."""
    task_refs = {}
    task_files = _walk(specs_dir, lambda rel: rel.endswith("tasks.md"), root)
    for file in task_files:
        rel = os.path.relpath(file, root)
        with open(file, "r", encoding="utf-8") as fh:
            text = fh.read()
        for line in text.split("\n"):
            if "_Requirements:" not in line:
                continue
            for id_ in extract_ids(line):
                task_refs.setdefault(id_, []).append(rel)
    return task_refs


def _collect_test_refs(root, cfg):
    """Walk cfg's testGlobs for files matching testFilePattern (minus ignore substrings);
    collect id -> [rel, ...] from every defined-looking ID appearing in a test file.

    Returns (test_refs, test_files) where test_files may contain duplicates across roots
    (deduped by the caller via dict.fromkeys, preserving first-seen order).
    """
    test_refs = {}
    file_re = re.compile(cfg["testFilePattern"])
    # Blank/empty entries must be no-ops: `s in rel` is always true for s == "", so a
    # stray "" in `ignore` would otherwise silently exclude every test file.
    ignore_list = [s for s in (cfg.get("ignore") or []) if isinstance(s, str) and len(s) > 0]
    roots = [p for p in (os.path.join(root, g) for g in cfg["testGlobs"]) if os.path.exists(p)]
    test_files = []
    for r in roots:
        test_files.extend(
            _walk(r, lambda rel: bool(file_re.search(rel)) and not any(s in rel for s in ignore_list), root)
        )
    for file in list(dict.fromkeys(test_files)):
        rel = os.path.relpath(file, root)
        try:
            with open(file, "r", encoding="utf-8") as fh:
                text = fh.read()
        except OSError:
            continue
        for id_ in dict.fromkeys(extract_ids(text)):
            test_refs.setdefault(id_, []).append(rel)
    return test_refs, test_files


def analyze(root, cfg):
    """Run the full trace analysis over root and return the summary dict:
    {requirements, requirementFiles, taskCitations, testedRequirements, testFilesScanned,
     errors, warnings}.

    Caller (main) is responsible for checking that <root>/<cfg.specsDir> exists first —
    analyze assumes it does.
    """
    specs_dir = os.path.join(root, cfg["specsDir"])
    defined, req_files, warnings, errors = _collect_requirement_files(specs_dir, root)
    task_refs = _collect_task_refs(specs_dir, root)
    test_refs, test_files = _collect_test_refs(root, cfg)

    for id_, files in task_refs.items():
        if id_ not in defined:
            uniq = list(dict.fromkeys(files))
            errors.append(f"E1 task cites unknown requirement {id_} ({', '.join(uniq)})")
    for id_, files in test_refs.items():
        if id_ not in defined:
            uniq = list(dict.fromkeys(files))
            extra = f", +{len(files) - 1} more" if len(files) > 1 else ""
            errors.append(f"E1 test cites unknown requirement {id_} ({uniq[0]}{extra})")
    for rf in req_files:
        rel, status, ids = rf["rel"], rf["status"], rf["ids"]
        for id_ in ids:
            tested = id_ in test_refs
            tasked = id_ in task_refs
            if status in ("Implemented", "Shipped") and not tested:
                errors.append(f"E2 {id_} ({rel}, {status}) has no covering test")
            if status == "Approved" and not tasked:
                warnings.append(f"W1 {id_} ({rel}, Approved) is not cited by any task")

    return {
        "requirements": len(defined),
        "requirementFiles": len(req_files),
        "taskCitations": len(task_refs),
        "testedRequirements": len([id_ for id_ in defined if id_ in test_refs]),
        "testFilesScanned": len(set(test_files)),
        "errors": errors,
        "warnings": warnings,
    }


def main(argv):
    """CLI entry point. Never calls sys.exit — returns the exit code.

    Flags: --strict, --json, --root R. Unknown flags are ignored silently (no argparse —
    that exits 2 on an unknown flag).
    """
    strict = "--strict" in argv
    as_json = "--json" in argv
    root_idx = argv.index("--root") if "--root" in argv else -1
    root = os.path.abspath(argv[root_idx + 1]) if root_idx != -1 else os.getcwd()

    try:
        cfg = load_config(root)
    except ConfigError as exc:
        print(f"check-trace: {exc}", file=sys.stderr)
        return 1

    specs_dir = os.path.join(root, cfg["specsDir"])
    if not os.path.exists(specs_dir):
        print(f"check-trace: no specs directory at {cfg['specsDir']} — nothing to check.", file=sys.stderr)
        return 0

    summary = analyze(root, cfg)

    if as_json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(
            f"check-trace: {summary['requirements']} requirements in {summary['requirementFiles']} files; "
            f"{summary['testedRequirements']} covered by tests; {summary['taskCitations']} cited by tasks; "
            f"{summary['testFilesScanned']} test files scanned."
        )
        for w in summary["warnings"]:
            print(f"  warn  {w}")
        for e in summary["errors"]:
            print(f"  ERROR {e}")

    if summary["errors"] or (strict and summary["warnings"]):
        return 1
    return 0


# Deliberately duplicated across the vendored linters (not shared) — this file ships standalone with zero cross-imports.
# Run main() only when this file IS the entry point. Comparing realpath on
# both sides is what makes a copy under /tmp (a symlink to /private/tmp on
# macOS) actually run its CLI instead of silently no-op'ing.
def _invoked_as_script():
    argv0 = sys.argv[0] if sys.argv else None
    if not argv0:
        return False
    try:
        return os.path.realpath(argv0) == os.path.realpath(__file__)
    except OSError:
        return False


if _invoked_as_script():
    sys.exit(main(sys.argv[1:]))
