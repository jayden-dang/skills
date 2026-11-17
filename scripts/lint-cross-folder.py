#!/usr/bin/env python3
"""Allow a skill to reach across a folder boundary only into `build`.

`npx skills add` copies one skill folder at a time, so a `../other-skill/file.md`
pointer is a promise that breaks for anyone installing that skill alone. AGENTS.md
forbids the shape.

One exception is real and is written down rather than tolerated silently. `build`
holds the controller recipe every build mode shares: the task lifecycle, the ledger
check, the close receipt, the runtime binding and the tracker sync. `go` and
`land-branch` read two of those files instead of carrying copies, so `build` is the
only folder any skill may reference across a boundary. Every other `../` still
fails, which is what keeps the exception from widening into "cross-folder is fine".

Usage: python3 scripts/lint-cross-folder.py
"""

import glob
import os
import re
import sys

POINTER = re.compile(r"(\.\./(?:\.\./)*)([A-Za-z0-9_-]+(?:/[A-Za-z0-9_-]+)*\.md)")
ALLOWED_DIR = "build"


def skill_nav_files():
    """A skill's own navigation surface: SKILL.md and the siblings beside it.

    Not `templates/` — those are content copied into a consumer repo, and their
    pointer back to the repo-root canonical copy is the convention
    lint-skill-templates.py enforces. Not pack-level READMEs either; they are
    documentation about the set, not a skill routing to a file.
    """
    for skill in sorted(glob.glob("skills/*/*/SKILL.md")):
        d = os.path.dirname(skill)
        for f in sorted(glob.glob(os.path.join(d, "*.md"))):
            if os.path.basename(f) != "TESTS.md":
                yield f


def main():
    errs = []
    checked = 0
    for path in skill_nav_files():
        checked += 1
        with open(path, encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                for up, target in POINTER.findall(line):
                    parts = target.split("/")
                    if ALLOWED_DIR in parts:
                        # An install copies each skill folder flat into one directory
                        # (`~/.agents/skills/<name>/`), so the only pointer into build
                        # that resolves there is `../build/<file>`. A repo-layout path
                        # such as `../../execution/build/x.md` breaks after install.
                        if up != "../" or parts[0] != ALLOWED_DIR:
                            errs.append(
                                f"{path}:{n}: `{up}{target}` only resolves in this repo's "
                                f"layout. Installed skills sit side by side, so write it "
                                f"as `../{ALLOWED_DIR}/{'/'.join(parts[parts.index(ALLOWED_DIR) + 1:])}`."
                            )
                        elif not glob.glob(os.path.join("skills", "*", ALLOWED_DIR, *parts[1:])):
                            errs.append(f"{path}:{n}: `{up}{target}` names a file {ALLOWED_DIR}/ does not have.")
                        continue
                    # Only another skill's folder is forbidden. Reaching docs/ or
                    # the repo-root templates/ is navigation, not a broken install.
                    resolved = os.path.normpath(os.path.join(os.path.dirname(path), up + target))
                    if not resolved.startswith("skills" + os.sep):
                        continue
                    errs.append(
                        f"{path}:{n}: `{up}{target}` reaches into another skill's "
                        f"folder. Only {ALLOWED_DIR}/ may be referenced across a "
                        f"boundary — move the file to the skill that uses it, or to "
                        f"{ALLOWED_DIR}/ when several do."
                    )

    if errs:
        print("cross-folder pointers:")
        for e in errs:
            print(f"  {e}")
        return 1
    print(f"OK — {checked} skill files, every cross-folder pointer targets {ALLOWED_DIR}/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
