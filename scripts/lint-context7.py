#!/usr/bin/env python3
"""Fail if a library-reasoning skill drops its Context7 reference.

The skills that reason about third-party libraries prefer the Context7 MCP for
current, version-accurate facts over a model's training-cutoff memory. That
preference lives only in prose, so an ordinary edit could silently delete it and
nothing would notice until an agent shipped a stale version number months later.
This guard pins the reference in place: each skill in `REQUIRE` must still name
Context7, and each must still exist under that name — a `REQUIRE` entry pointing
at no skill is itself drift (a rename that outran this list), so it fails too,
the same way a lint pattern that never fires looks exactly like one that isn't
there.
"""
import re
import sys
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parent.parent

# Skills whose behavior depends on preferring Context7 over recollection.
# `research` owns the mechanics; the others reference it for their own step.
# Keep this in sync with the prose — that synchronization is the whole point.
REQUIRE = {"research", "brainstorm", "write-design", "setup-repo"}

# The MCP's proper name. Matched case-insensitively so `context7` in a code
# fence or a lowercased sentence still counts as a live reference.
TOKEN = "context7"


class Failure(NamedTuple):
    skill: str
    reason: str  # "no-mention" | "missing-skill"


def scan(root: Path) -> list[Failure]:
    """Return every required skill that has lost — or never had — its Context7 mention."""
    bodies = {}
    for f in sorted(root.glob("skills/*/*/SKILL.md")):
        text = f.read_text()
        name = re.search(r"^name:\s*(\S+)", text, re.M)
        if name:
            bodies[name.group(1)] = text

    failures = []
    for name in sorted(REQUIRE):
        if name not in bodies:
            failures.append(Failure(name, "missing-skill"))
        elif TOKEN not in bodies[name].lower():
            failures.append(Failure(name, "no-mention"))
    return failures


def main() -> int:
    failures = scan(ROOT)
    if failures:
        print("CONTEXT7 DRIFT — a library-reasoning skill lost its Context7 reference:\n")
        for f in failures:
            if f.reason == "missing-skill":
                print(f"  {f.skill}: no SKILL.md by this name — REQUIRE is out of date")
                print("    (was it renamed? update REQUIRE in scripts/lint-context7.py)\n")
            else:
                print(f"  skills/*/{f.skill}/SKILL.md: no mention of Context7")
                print("    this skill must prefer the Context7 MCP for library facts\n")
        print(f"{len(failures)} drift(s). Restore the Context7 reference (or fix REQUIRE).")
        return 1

    print(f"OK — {len(REQUIRE)} library-reasoning skills, all reference Context7.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
