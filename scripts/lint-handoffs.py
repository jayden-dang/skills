#!/usr/bin/env python3
"""Fail if a skill body directs the agent to *invoke* a user-invoked skill.

A skill carrying `disable-model-invocation: true` cannot be auto-invoked. A body
that tells the agent to invoke one is a dead-end hand-off. Such a skill may only
be *named for the user to run* (`/triage`), never invoked.
"""
import re
import sys
from pathlib import Path
from typing import NamedTuple

ROOT = Path(__file__).resolve().parent.parent

# Phrasings that direct the agent to invoke the named skill itself.
#
# `{name}` is substituted with the escaped target name (never `.format()` — a
# pattern is a regex, and `\s{1,3}` must stay a quantifier). Whitespace is `\s+`
# rather than a literal space so a phrasing still matches when prose wraps it
# across a line. The `hand ... to` middle is bounded so it cannot run across
# paragraphs. The trailing lookahead on `use` is the escape hatch: a body may
# write ``use `triage` — user-invoked`` when describing rather than invoking.
INVOKE = [
    r"REQUIRED SUB-SKILL:\s*(?:use|load)\s*`/?{name}`",
    r"hand(?:\s+\w+){0,4}\s+to\s+`/?{name}`",
    # Conjugations are spelled out rather than `delegat\w*`: a bare stem would
    # also swallow the noun ("delegation is the user's call"), and a bare
    # `delegate\s+to` would miss the conjugated form that already exists in
    # correct-course — a pattern that never fires looks exactly like a pattern
    # that isn't there.
    r"\bdelegat(?:e|es|ed|ing)(?:\s+\w+){0,4}\s+to\s+`/?{name}`",
    r"\binvoke\s+`/?{name}`",
    r"\buse\s+`/?{name}`(?!\s*[-—]*\s*user-invoked)",
]


class Failure(NamedTuple):
    path: Path
    line: int
    caller: str
    target: str
    snippet: str


def scan(root: Path) -> list[Failure]:
    """Return every dead hand-off in the skill tree rooted at `root`."""
    user_invoked, bodies = set(), {}
    for f in sorted(root.glob("skills/*/*/SKILL.md")):
        text = f.read_text()
        fm = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S)
        if not fm:
            print(f"ERROR {f.relative_to(root)}: no frontmatter")
            sys.exit(1)
        name = re.search(r"^name:\s*(\S+)", fm.group(1), re.M).group(1)
        if "disable-model-invocation: true" in fm.group(1):
            user_invoked.add(name)
        # The body starts after the frontmatter, so its first line is not file
        # line 1. Derive the offset from the match rather than guessing it.
        body_start = text[: fm.start(2)].count("\n") + 1
        bodies[name] = (f, fm.group(2), body_start)

    failures, seen = [], set()
    for target in sorted(user_invoked):
        for pat in INVOKE:
            # Substitute rather than .format(): a pattern is a regex, so a
            # quantifier like `\s{1,3}` must not be read as a format field.
            rx = re.compile(pat.replace("{name}", re.escape(target)), re.I)
            for caller, (path, body, body_start) in bodies.items():
                if caller == target:
                    continue
                # Search the body whole, not line by line: a phrasing that wraps
                # across a newline is still a dead hand-off. The line number is
                # derived from where the match starts.
                for m in rx.finditer(body):
                    i = body_start + body.count("\n", 0, m.start())
                    # Patterns overlap; one bad line is still one defect.
                    key = (caller, i, target)
                    if key in seen:
                        continue
                    seen.add(key)
                    failures.append(
                        Failure(
                            path.relative_to(root), i, caller, target,
                            " ".join(m.group(0).split())[:90],
                        )
                    )
    return sorted(failures, key=lambda f: (str(f.path), f.line))


def main() -> int:
    failures = scan(ROOT)
    if failures:
        print("DEAD HAND-OFF — a skill directs the agent to invoke a user-invoked skill:\n")
        for f in failures:
            print(f"  {f.path}:{f.line}")
            print(f"    {f.caller} -> {f.target} (user-invoked)")
            print(f"    {f.snippet}\n")
        print(f"{len(failures)} dead hand-off(s). Name the skill for the user to run instead.")
        return 1

    total = len(sorted(ROOT.glob("skills/*/*/SKILL.md")))
    user_invoked = sum(
        1
        for f in ROOT.glob("skills/*/*/SKILL.md")
        if "disable-model-invocation: true" in f.read_text()
    )
    print(f"OK — {total} skills, {user_invoked} user-invoked, 0 dead hand-offs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
