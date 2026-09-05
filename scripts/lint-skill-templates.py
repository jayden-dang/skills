#!/usr/bin/env python3
"""Fail if a skill cites a pack seed that is missing or drifted from SSOT.

Repo-root templates/ is the authoring original. `npx skills add` copies only
each skill folder, so every cited seed must also live at
<skill-dir>/templates/<relpath> and match the SSOT bytes.

Push before relying on an edit here. The marketplace is registered against a
remote (~/.claude/plugins/known_marketplaces.json records this repo as
source github: jayden-dang/skills), so a plugin update refreshes the checkout
from origin and re-derives every install under
~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/. An SSOT-plus-mirror
edit that is committed locally but unpushed is therefore reverted in every
derived copy at the next update — including the one a running session reads.
Committing is not enough; the fix is durable only once it is on origin. Use
--write to mirror rather than copying by hand.

A cite is a greppable templates/<relpath> in that skill's SKILL.md whose
relpath names a file or directory under repo-root templates/. A skill's
private tree (for example define-system-doc/templates/) is ignored because
those paths are not files under the pack SSOT.

Usage:
  lint-skill-templates.py              # scan every skills/**/SKILL.md
  lint-skill-templates.py FILE ...     # lint the given SKILL.md files
  lint-skill-templates.py --write      # copy SSOT files into consumers
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SSOT = ROOT / "templates"

# Capture a relative path after templates/. Stop before markdown/prose closers.
CITE = re.compile(
    r"(?:\$\{CLAUDE_PLUGIN_ROOT\}/|\.\./\.\./\.\./)?templates/"
    r"([A-Za-z0-9][A-Za-z0-9_./-]*)"
)


def ssot_files() -> dict[str, Path]:
    files = {}
    for p in SSOT.rglob("*"):
        if p.is_file():
            files[p.relative_to(SSOT).as_posix()] = p
    return files


def cites_in(text: str, ssot: dict[str, Path]) -> set[str]:
    """Return SSOT-relative paths this SKILL.md cites."""
    found: set[str] = set()
    for raw in CITE.findall(text):
        rel = raw.rstrip("./")
        if rel in ssot:
            found.add(rel)
            continue
        prefix = rel + "/"
        children = [k for k in ssot if k.startswith(prefix)]
        found.update(children)
    return found


def skill_mds(paths: list[str] | None) -> list[Path]:
    if paths:
        return [Path(p).resolve() for p in paths if Path(p).name == "SKILL.md"]
    return sorted(ROOT.glob("skills/*/*/SKILL.md"))


def check_skill(skill_md: Path, ssot: dict[str, Path], write: bool) -> list[str]:
    text = skill_md.read_text(encoding="utf-8")
    needed = cites_in(text, ssot)
    if not needed:
        return []
    dest_root = skill_md.parent / "templates"
    errs = []
    # SEED-1.3: sibling templates/ is first in the resolve order.
    # Require the exact token so "team-inference.md beside this file" does not pass.
    if "`templates/` beside this SKILL.md" not in text:
        errs.append(
            "resolve order must name sibling `templates/` beside this SKILL.md "
            "before CLAUDE_PLUGIN_ROOT and ../../../templates"
        )
    for rel in sorted(needed):
        src = ssot[rel]
        dest = dest_root / rel
        if write:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(src.read_bytes())
            if src.stat().st_mode & 0o111:
                dest.chmod(dest.stat().st_mode | 0o111)
        if not dest.is_file():
            errs.append(f"missing copy templates/{rel} → {dest.relative_to(ROOT)}")
            continue
        if dest.read_bytes() != src.read_bytes():
            errs.append(f"drift templates/{rel} ≠ {dest.relative_to(ROOT)}")
    return errs


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", help="SKILL.md paths (default: all)")
    parser.add_argument(
        "--write",
        action="store_true",
        help="copy SSOT seeds into each consumer, then re-check",
    )
    args = parser.parse_args(argv)

    if not SSOT.is_dir():
        print(f"lint-skill-templates: SSOT missing: {SSOT}", file=sys.stderr)
        return 2

    ssot = ssot_files()
    if not ssot:
        print("lint-skill-templates: SSOT is empty", file=sys.stderr)
        return 2

    failed = 0
    for skill_md in skill_mds(args.files):
        rel_skill = skill_md.relative_to(ROOT) if skill_md.is_relative_to(ROOT) else skill_md
        for err in check_skill(skill_md, ssot, write=args.write):
            print(f"{rel_skill}: {err}")
            failed += 1
    if failed:
        print(f"lint-skill-templates: {failed} error(s)")
        return 1
    return 0


if __name__ == "__main__":
    # Python 3.8 compat: Path.is_relative_to is 3.9+
    if not hasattr(Path, "is_relative_to"):
        def _is_relative_to(self, other):  # type: ignore[no-redef]
            try:
                self.relative_to(other)
                return True
            except ValueError:
                return False

        Path.is_relative_to = _is_relative_to  # type: ignore[method-assign]
    sys.exit(main(sys.argv[1:]))
