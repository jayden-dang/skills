#!/usr/bin/env python3
"""vendor-linters — install this skill set's linters into a consuming repo, and
detect drift between the two copies. (Python port of vendor-linters.mjs.)

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
from typing import Optional

# name -> (oracle_filename, port_filename). install/check_drift install and
# drift-check the `.py` port only, using port_filename. oracle_filename is
# also used by the `legacy` verdict below, which detects a vendored `.mjs`
# left behind from before the Python port existed.
LINTERS = {
    "check-graph": ("check-graph.mjs", "check_graph.py"),
    "check-trace": ("check-trace.mjs", "check_trace.py"),
}

STAMP_LINE_RE = re.compile(r"^# @skills-linter: (\S+) sha256:([0-9a-f]{12})$", re.MULTILINE)
_STAMP_PREFIX = "# @skills-linter:"

# The `.mjs` oracle's own stamp convention (`// ...` — a JS comment — rather
# than `# ...`). Used only by the `legacy` verdict to tell an untouched
# vendored `.mjs` apart from one hand-edited after vendoring; the primary
# `.py`-facing compute_stamp/read_stamp above are untouched by this.
_ORACLE_STAMP_LINE_RE = re.compile(r"^// @skills-linter: (\S+) sha256:([0-9a-f]{12})$", re.MULTILINE)
_ORACLE_STAMP_PREFIX = "// @skills-linter:"


def _is_stamp(line):
    return line.startswith(_STAMP_PREFIX)


def _oracle_compute_stamp(src):
    """compute_stamp's counterpart for a `.mjs` body: same recipe, excluding
    lines that start with the `//`-flavored stamp prefix instead of `#`."""
    body = "\n".join(line for line in src.split("\n") if not line.startswith(_ORACLE_STAMP_PREFIX))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]


def _oracle_read_stamp(src):
    """read_stamp's counterpart for a `.mjs` body, or None when it carries no
    `// @skills-linter:` line (e.g. a legacy file that predates stamping)."""
    m = _ORACLE_STAMP_LINE_RE.search(src)
    return {"name": m.group(1), "digest": m.group(2)} if m else None


def compute_stamp(src):
    """The stamp digest of a source body. The stamp line itself is excluded, so
    stamping is idempotent — re-stamping a stamped file is a no-op."""
    body = "\n".join(line for line in src.split("\n") if not _is_stamp(line))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]


def read_stamp(src: str) -> Optional[dict]:
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


def install(src_root, dest_root, scripts_dir="scripts", remove_legacy=False):
    """Copy each linter from the skill set into the consumer repo, byte for byte
    (the stamp travels with the body). Returns one record per linter describing
    what changed, so a caller can report `created` vs `updated` vs `unchanged`.

    `remove_legacy` defaults to False: a vendored `.mjs` left behind from
    before the Python port existed is never deleted unless the caller
    explicitly opts in. "Opts in" means the literal `True` — the removal is
    gated on `remove_legacy is True`, an identity check rather than a
    truthiness check, so a naively-forwarded value like the string "false"
    (truthy in Python) or `1` cannot slip past the guard and delete a file
    the caller never actually consented to remove. Even a real `True` is not
    enough on its own: a legacy file that has been hand-edited since
    vendoring (its body no longer hashes to its own stamp — see
    check_drift's `legacy` verdict) is NOT removed: it may hold work the
    caller has not saved elsewhere. Its record instead carries a
    `legacy_warning` and no `legacy_removed`.
    """
    os.makedirs(os.path.join(dest_root, scripts_dir), exist_ok=True)
    results = []
    for name, (oracle_filename, port_filename) in LINTERS.items():
        src_path = _linter_path(src_root, port_filename, scripts_dir)
        with open(src_path, "r", encoding="utf-8") as fh:
            src = fh.read()
        dest_path = _linter_path(dest_root, port_filename, scripts_dir)
        prev = None
        if os.path.exists(dest_path):
            with open(dest_path, "r", encoding="utf-8") as fh:
                prev = fh.read()
        if prev != src:
            with open(dest_path, "w", encoding="utf-8") as fh:
                fh.write(src)
        action = "created" if prev is None else ("unchanged" if prev == src else "updated")
        record = {"name": name, "dest": dest_path, "digest": compute_stamp(src), "action": action}

        legacy_path = _linter_path(dest_root, oracle_filename, scripts_dir)
        if os.path.exists(legacy_path):
            with open(legacy_path, "r", encoding="utf-8") as fh:
                legacy_src = fh.read()
            legacy_stamp = _oracle_read_stamp(legacy_src)
            legacy_modified = legacy_stamp is not None and legacy_stamp["digest"] != _oracle_compute_stamp(legacy_src)
            if legacy_modified:
                record["legacy_warning"] = (
                    f"{legacy_path} was hand-edited after vendoring and was NOT removed — "
                    "it may hold work you have not saved elsewhere. Review it, then remove it manually."
                )
            elif remove_legacy is True:
                # Identity check, not truthiness: `remove_legacy` guards a
                # real `os.remove`, and `install()` is a public function a
                # future caller could invoke with a naively-parsed CLI value
                # (e.g. the string "false", or 1). Only the literal `True`
                # this module's own CLI passes (see main()'s `answer in
                # ("y", "yes")`) may reach the delete — every other value,
                # truthy or not, fails closed and leaves the file in place.
                os.remove(legacy_path)
                record["legacy_removed"] = legacy_path

        results.append(record)
    return results


def check_drift(src_root, dest_root, scripts_dir="scripts"):
    """Compare each vendored linter against the skill set's copy. Read-only.

      missing   — never installed (neither the .py port nor a legacy .mjs)
      modified  — the repo's copy was hand-edited (its body no longer hashes to
                  its own stamp). Checked FIRST: a local edit that leaves the
                  stamp line alone would otherwise masquerade as `ok`.
      legacy    — the .py port is absent, but a vendored .mjs (the pre-port
                  oracle) is present. Also carries "legacy": True. If that
                  .mjs had a `// @skills-linter:` stamp but was ALSO
                  hand-edited since it was vendored (its body no longer
                  hashes to its own stamp), the status is `modified` (not
                  `legacy`) with "legacy": True set alongside it, so both
                  facts survive together. A .mjs with no stamp at all is
                  always `legacy`, never `modified`.
      outdated  — untouched locally, but the skill set has moved on
      ok        — identical
    """
    results = []
    for name, (oracle_filename, port_filename) in LINTERS.items():
        src_path = _linter_path(src_root, port_filename, scripts_dir)
        with open(src_path, "r", encoding="utf-8") as fh:
            source = fh.read()
        expected = compute_stamp(source)
        dest_path = _linter_path(dest_root, port_filename, scripts_dir)
        if not os.path.exists(dest_path):
            legacy_path = _linter_path(dest_root, oracle_filename, scripts_dir)
            if os.path.exists(legacy_path):
                with open(legacy_path, "r", encoding="utf-8") as fh:
                    legacy_src = fh.read()
                legacy_stamp = _oracle_read_stamp(legacy_src)
                legacy_actual = _oracle_compute_stamp(legacy_src)
                legacy_declared = legacy_stamp["digest"] if legacy_stamp else None
                if legacy_stamp is not None and legacy_declared != legacy_actual:
                    results.append({
                        "name": name, "status": "modified", "legacy": True, "file": legacy_path,
                        "expected": expected, "found": legacy_actual, "declared": legacy_declared,
                    })
                else:
                    results.append({
                        "name": name, "status": "legacy", "legacy": True, "file": legacy_path,
                        "expected": expected, "found": legacy_declared,
                    })
                continue
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
    "legacy": "vendored as the legacy .mjs, ahead of the Python port — run `vendor-linters --install` "
              "to add the .py port; the .mjs stays until you consent to remove it",
    "legacy-modified": "hand-edited legacy .mjs with no .py port installed yet — run `vendor-linters --install` "
                        "first, then remove the .mjs by hand once you've confirmed no local work is lost",
}


def _remedy_for(d):
    """REMEDY[status], except a legacy file that is ALSO hand-edited gets its
    own combined message rather than the plain `modified` one."""
    if d.get("legacy") and d["status"] == "modified":
        return REMEDY["legacy-modified"]
    return REMEDY[d["status"]]


# This script's own directory, and the skill set root one level above it — the
# default `--from` when a caller doesn't say otherwise.
_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_FROM = os.path.dirname(_SCRIPTS_DIR)


def _flag(argv, name, default=None):
    """Read a flag's value: `d` when the flag is entirely absent, `None` when
    present but trailing with nothing after it (mirrors argv[i + 1] being
    undefined in the oracle), else the following token."""
    if name not in argv:
        return default
    i = argv.index(name)
    return argv[i + 1] if i + 1 < len(argv) else None


def main(argv):
    """CLI entry point. Never calls sys.exit — returns the exit code.

    Flags: --from <skillSetRoot>, --to <repoRoot>, --scripts-dir <dir>.
    Modes: --stamp | --check | --install. No argparse — that exits 2 on an
    unknown flag; unknown flags here are ignored silently. Exit 2 is reserved
    for an absent mode, not an unknown flag.
    """
    from_root = os.path.abspath(_flag(argv, "--from", _DEFAULT_FROM))
    to_root = os.path.abspath(_flag(argv, "--to", os.getcwd()))
    scripts_dir = _flag(argv, "--scripts-dir", "scripts")

    if "--stamp" in argv:
        for name, (_, port_filename) in LINTERS.items():
            p = _linter_path(from_root, port_filename, scripts_dir)
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
            # A legacy verdict is labeled by the .mjs filename it found, not
            # the linter's short name — "check-trace.mjs: legacy" reads
            # unambiguously, where "check-trace: legacy" would not say which
            # extension was found. The four pre-existing statuses print the
            # bare short name (`d["name"]`); that exact format is pinned
            # byte-for-byte against the .mjs oracle by parity_test.py and
            # must not change. `legacy`/`legacy-modified` have no oracle, so
            # their label is relative to `to_root` rather than an absolute
            # filesystem path — informative without leaking the caller's
            # home directory into the output.
            label = os.path.relpath(d["file"], to_root) if d.get("legacy") else d["name"]
            print(f"  {label}: {d['status']} — {_remedy_for(d)}")
        return 1

    if "--install" in argv:
        # Consented migration: a legacy .mjs is never removed without an
        # explicit yes, and that consent is only ever solicited when there is
        # something to remove and a human is actually there to answer (an
        # unattended/piped invocation — e.g. every test in this suite — must
        # never block on stdin, and must default to leaving the file alone).
        remove_legacy = False
        legacy_names = [d["name"] for d in check_drift(from_root, to_root, scripts_dir) if d.get("legacy")]
        if legacy_names and sys.stdin.isatty():
            names = ", ".join(legacy_names)
            answer = input(f"Remove legacy .mjs for {names}? [y/N]: ").strip().lower()
            remove_legacy = answer in ("y", "yes")

        for r in install(from_root, to_root, scripts_dir, remove_legacy=remove_legacy):
            print(f"  {r['action'].ljust(9)} {r['dest']}")
            if r.get("legacy_removed"):
                print(f"  removed   {r['legacy_removed']}")
            if r.get("legacy_warning"):
                print(f"  ! {r['legacy_warning']}")
        return 0

    print("usage: vendor-linters (--install|--check|--stamp) [--from <skillSetRoot>] [--to <repoRoot>]", file=sys.stderr)
    return 2


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
