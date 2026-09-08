#!/usr/bin/env python3
"""Hold SKILL.md bodies to a line budget that can only decrease.

A trim that nothing enforces regrows. `skills/discovery/clarify-decisions/SKILL.md`
was cut by 225 lines in 8579a54 (2026-09-01) and stood at 300 again within weeks,
because the only thing holding it down was the intention of whoever cut it. This
check is that intention made mechanical.

The rule:

  * A SKILL.md at or under LIMIT lines passes, and must not appear in the budget.
  * A SKILL.md over LIMIT must have a budget entry, and must not exceed its
    recorded line count or its recorded word count. Words are tracked because a
    line ceiling is gameable: merging hard-wrapped paragraphs cuts a third off the
    line count while every turn still pays for the same text.
  * A budget entry for a file now under LIMIT fails: the entry has to be deleted,
    so the budget shrinks as files are fixed and can never be re-spent.

That last rule is what makes this a ratchet rather than a permanent exemption
list. Nothing here judges what a line contains; `author-skills` owns the question
of which lines earn their place, and this only answers how many there are.

Usage:
    python3 scripts/lint-skill-length.py [files...]   # check (default: all)
    python3 scripts/lint-skill-length.py --write      # rewrite the budget downward
"""

import glob
import json
import os
import sys

LIMIT = 200
BUDGET = os.path.join(os.path.dirname(os.path.abspath(__file__)), "skill-length-budget.json")


def measure(path):
    """Lines and words. Lines are the stated ceiling; words are what a reflow
    cannot fake, and reflow is the first thing a trim under deadline reaches for."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    return len(text.splitlines()), len(text.split())


def load_budget():
    """Read the budget, tolerating the pre-word format where an entry was a bare
    line count. Such an entry gets no word ceiling rather than a wrong one."""
    if not os.path.exists(BUDGET):
        return {}
    with open(BUDGET, encoding="utf-8") as fh:
        raw = json.load(fh).get("over_limit", {})
    out = {}
    for path, value in raw.items():
        if isinstance(value, int):
            out[path] = {"lines": value, "words": float("inf")}
        else:
            out[path] = value
    return out


def all_skills():
    return sorted(glob.glob("skills/**/SKILL.md", recursive=True))


def write_budget():
    """Regenerate the budget from the working tree. Entries only ever go down."""
    previous = load_budget()
    entries = {}
    for path in all_skills():
        lines, words = measure(path)
        if lines <= LIMIT:
            continue
        was = previous.get(path)
        if was:
            for key, now in (("lines", lines), ("words", words)):
                if now > was[key]:
                    print(f"refusing to raise the {key} budget for {path}: "
                          f"{was[key]} -> {now}")
                    return 1
        entries[path] = {"lines": lines, "words": words}

    payload = {
        "limit": LIMIT,
        "comment": (
            "Files still over the limit, with the count they may not exceed. "
            "Entries come out as files are trimmed; none may be added by hand "
            "or raised. See scripts/lint-skill-length.py."
        ),
        "over_limit": entries,
    }
    with open(BUDGET, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")
    freed = sorted(set(previous) - set(entries))
    print(f"budget written: {len(entries)} files over {LIMIT} lines")
    for path in freed:
        print(f"  cleared: {path}")
    return 0


def check(paths):
    budget = load_budget()
    errs = []
    for path in paths:
        if not os.path.exists(path):
            continue
        lines, words = measure(path)
        allowed = budget.get(path)
        if lines <= LIMIT:
            if allowed is not None:
                errs.append(
                    f"{path}: now {lines} lines, at or under the {LIMIT}-line limit. "
                    f"Delete its entry from {os.path.relpath(BUDGET)} so the budget "
                    f"cannot be re-spent (run --write)."
                )
            continue
        if allowed is None:
            errs.append(
                f"{path}: {lines} lines, over the {LIMIT}-line limit. Split detail "
                f"behind a pointer to a sibling file, or delete what fails the no-op "
                f"test. See author-skills."
            )
            continue
        if lines > allowed["lines"]:
            errs.append(f"{path}: grew from {allowed['lines']} to {lines} lines; "
                        f"the budget only decreases.")
        if words > allowed["words"]:
            errs.append(f"{path}: grew from {allowed['words']} to {words} words; "
                        f"rewrapping lines is not a trim, and words are what every "
                        f"turn pays for.")

    if errs:
        print("skill length:")
        for err in errs:
            print(f"  {err}")
        return 1

    remaining = sum(1 for p in budget if os.path.exists(p))
    over = f", {remaining} still over it" if remaining else ""
    print(f"OK — {len(paths)} skills checked against a {LIMIT}-line limit{over}.")
    return 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if a != "--write"]
    if "--write" in sys.argv[1:]:
        sys.exit(write_budget())
    sys.exit(check(args or all_skills()))
