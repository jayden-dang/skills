#!/usr/bin/env python3
"""Fail if a skill body directs the agent to *invoke* a user-invoked skill.

A skill carrying `disable-model-invocation: true` cannot be auto-invoked. A body
that tells the agent to invoke one is a dead-end hand-off. Such a skill may only
be *named for the user to run* (`/triage`), never invoked.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = sorted(ROOT.glob("skills/*/*/SKILL.md"))

# Phrasings that direct the agent to invoke the named skill itself.
INVOKE = [
    r"REQUIRED SUB-SKILL:\s*(?:use|load)\s*`{name}`",
    r"hand(?:\s+\w+)*\s+to\s+`{name}`",
    r"hand off to `{name}`",
    r"\binvoke `{name}`",
    r"\buse `{name}`(?! *[-—]* *user-invoked)",
]

user_invoked, bodies = set(), {}
for f in SKILLS:
    text = f.read_text()
    fm = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
    if not fm:
        print(f"ERROR {f.relative_to(ROOT)}: no frontmatter")
        sys.exit(1)
    name = re.search(r"^name:\s*(\S+)", fm.group(1), re.M).group(1)
    if "disable-model-invocation: true" in fm.group(1):
        user_invoked.add(name)
    bodies[name] = (f, fm.group(2))

failures = []
for target in sorted(user_invoked):
    for pat in INVOKE:
        rx = re.compile(pat.format(name=re.escape(target)), re.I)
        for caller, (path, body) in bodies.items():
            if caller == target:
                continue
            for i, line in enumerate(body.split("\n"), start=2):
                if rx.search(line):
                    failures.append(
                        (path.relative_to(ROOT), i, caller, target, line.strip()[:90])
                    )

if failures:
    print("DEAD HAND-OFF — a skill directs the agent to invoke a user-invoked skill:\n")
    for path, line, caller, target, snippet in failures:
        print(f"  {path}:{line}")
        print(f"    {caller} -> {target} (user-invoked)")
        print(f"    {snippet}\n")
    print(f"{len(failures)} dead hand-off(s). Name the skill for the user to run instead.")
    sys.exit(1)

print(f"OK — {len(SKILLS)} skills, {len(user_invoked)} user-invoked, 0 dead hand-offs.")
