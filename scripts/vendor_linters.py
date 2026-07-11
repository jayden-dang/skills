#!/usr/bin/env python3
"""vendor-linters — install this skill set's linters into a consuming repo, and
detect drift between the two copies.

`setup-repo` calls this so a repo gets `check_trace.py` and `check_graph.py`
without a human remembering to copy them. Each linter carries a
`# @skills-linter: <name> sha256:<12hex>` stamp of its own body; comparing
stamps tells us whether a repo's copy is current, superseded, or locally
hacked.

The skill set's own `scripts/` is the single canonical copy — nothing is
mirrored elsewhere, so there is exactly one axis of drift to police.

Modes: --install | --check | --stamp   Flags: --from <skillSetRoot> --to <repoRoot>
Zero dependencies, no network, exits 1 from --check when any linter has drifted.

This module has no top-level side effects: importing it runs no CLI.
"""
import hashlib
import os
import re
import sys

# The linters this tool vendors and drift-checks, keyed by their skill-linter
# name and mapped to the filename it installs.
LINTERS = {
    "check-graph": "check_graph.py",
    "check-trace": "check_trace.py",
}

STAMP_LINE_RE = re.compile(r"^# @skills-linter: (\S+) sha256:([0-9a-f]{12})$", re.MULTILINE)
_STAMP_PREFIX = "# @skills-linter:"


def _is_stamp(line):
    return line.startswith(_STAMP_PREFIX)


def compute_stamp(src):
    """The stamp digest of a source body. The stamp line itself is excluded, so
    stamping is idempotent — re-stamping a stamped file is a no-op."""
    body = "\n".join(line for line in src.split("\n") if not _is_stamp(line))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]


def read_stamp(src):
    """Read a source's declared stamp, or None when it carries none."""
    m = STAMP_LINE_RE.search(src)
    return {"name": m.group(1), "digest": m.group(2)} if m else None


def restamp(src, name):
    """Return `src` carrying a stamp that matches its own body (idempotent)."""
    lines = [line for line in src.split("\n") if not _is_stamp(line)]
    at = 1 if lines and lines[0].startswith("#!") else 0  # the shebang must stay first
    lines.insert(at, f"# @skills-linter: {name} sha256:{compute_stamp(src)}")
    return "\n".join(lines)


def _linter_path(root, filename, scripts_dir):
    return os.path.join(root, scripts_dir, filename)


def install(src_root, dest_root, scripts_dir="scripts"):
    """Copy each linter from the skill set into the consumer repo, byte for byte
    (the stamp travels with the body). Returns one record per linter describing
    what changed, so a caller can report `created` vs `updated` vs `unchanged`.
    """
    os.makedirs(os.path.join(dest_root, scripts_dir), exist_ok=True)
    results = []
    for name, filename in LINTERS.items():
        src_path = _linter_path(src_root, filename, scripts_dir)
        with open(src_path, "r", encoding="utf-8") as fh:
            src = fh.read()
        dest_path = _linter_path(dest_root, filename, scripts_dir)
        prev = None
        if os.path.exists(dest_path):
            with open(dest_path, "r", encoding="utf-8") as fh:
                prev = fh.read()
        if prev != src:
            with open(dest_path, "w", encoding="utf-8") as fh:
                fh.write(src)
        action = "created" if prev is None else ("unchanged" if prev == src else "updated")
        results.append({"name": name, "dest": dest_path, "digest": compute_stamp(src), "action": action})
    return results


def check_drift(src_root, dest_root, scripts_dir="scripts"):
    """Compare each vendored linter against the skill set's copy. Read-only.

      missing   — never installed
      modified  — the repo's copy was hand-edited (its body no longer hashes to
                  its own stamp). Checked FIRST: a local edit that leaves the
                  stamp line alone would otherwise masquerade as `ok`.
      outdated  — untouched locally, but the skill set has moved on
      ok        — identical
    """
    results = []
    for name, filename in LINTERS.items():
        src_path = _linter_path(src_root, filename, scripts_dir)
        with open(src_path, "r", encoding="utf-8") as fh:
            source = fh.read()
        expected = compute_stamp(source)
        dest_path = _linter_path(dest_root, filename, scripts_dir)
        if not os.path.exists(dest_path):
            results.append({"name": name, "status": "missing", "expected": expected, "found": None})
            continue

        with open(dest_path, "r", encoding="utf-8") as fh:
            vendored = fh.read()
        stamp = read_stamp(vendored)
        declared = stamp["digest"] if stamp else None
        actual = compute_stamp(vendored)
        if declared != actual:
            results.append({"name": name, "status": "modified", "expected": expected, "found": actual, "declared": declared})
        elif declared != expected:
            results.append({"name": name, "status": "outdated", "expected": expected, "found": declared})
        else:
            results.append({"name": name, "status": "ok", "expected": expected, "found": declared})
    return results


REMEDY = {
    "missing": "not installed — run `vendor-linters --install`",
    "outdated": "superseded by the skill set — re-run `vendor-linters --install`",
    "modified": "edited locally — re-install to discard, or upstream the change",
}


# This script's own directory, and the skill set root one level above it — the
# default `--from` when a caller doesn't say otherwise.
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_FROM = os.path.dirname(_SCRIPTS_DIR)


def _flag(argv, name, default=None):
    """Read a flag's value: `default` when the flag is entirely absent, `None`
    when present but trailing with nothing after it, else the following token."""
    if name not in argv:
        return default
    i = argv.index(name)
    return argv[i + 1] if i + 1 < len(argv) else None


def main(argv):
    """CLI entry point. Never calls sys.exit — returns the exit code.

    Flags: --from <skillSetRoot>, --to <repoRoot>, --scripts-dir <dir>.
    Modes: --stamp | --check | --install. Unknown flags are ignored silently;
    exit 2 is reserved for an absent mode, not an unknown flag.
    """
    from_root = os.path.abspath(_flag(argv, "--from", _DEFAULT_FROM))
    to_root = os.path.abspath(_flag(argv, "--to", os.getcwd()))
    scripts_dir = _flag(argv, "--scripts-dir", "scripts")

    if "--stamp" in argv:
        for name, filename in LINTERS.items():
            p = _linter_path(from_root, filename, scripts_dir)
            with open(p, "r", encoding="utf-8") as fh:
                src = fh.read()
            stamped = restamp(src, name)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(stamped)
            print(f"stamped {name} -> {read_stamp(stamped)['digest']}")
        return 0

    if "--check" in argv:
        drift = [d for d in check_drift(from_root, to_root, scripts_dir) if d["status"] != "ok"]
        if not drift:
            print("vendor-linters: OK — every linter is current.")
            return 0
        for d in drift:
            print(f"  {d['name']}: {d['status']} — {REMEDY[d['status']]}")
        return 1

    if "--install" in argv:
        for r in install(from_root, to_root, scripts_dir):
            print(f"  {r['action'].ljust(9)} {r['dest']}")
        return 0

    print("usage: vendor-linters (--install|--check|--stamp) [--from <skillSetRoot>] [--to <repoRoot>]", file=sys.stderr)
    return 2


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
