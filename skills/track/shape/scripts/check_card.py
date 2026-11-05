#!/usr/bin/env python3
"""Check one road card before an unattended run builds it.

usage: check_card.py <card.md> [--root <repo root>]

A card is the operator's intent for one road: what changes for a person, the examples that
prove it, and which decisions are theirs and which are the agents'. Prints one line per
problem, then `card: ready` or `card: not ready`. Exits 0 ready, 1 not ready, 2 no card.
"""
import argparse
import re
import sys
from pathlib import Path

SLOTS = ["Outcome", "Examples", "Must keep", "Off limits", "Decided", "Delegated", "Ask me"]
UI_LEVELS = ["none", "reuse", "reference", "new"]
MAX_LINES = 30


def field(text, name):
    """The text after **Name:** up to the next **Field:** line, or None when the label is absent."""
    m = re.search(r"^\*\*" + re.escape(name) + r":\*\*[ \t]*(.*?)(?=^\*\*[A-Za-z][^*\n]*:\*\*|\Z)",
                  text, re.M | re.S)
    return None if m is None else m.group(1).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("card")
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    path = Path(args.card)
    if not path.is_file():
        print(f"no card at {path}")
        return 2
    text = path.read_text()
    problems = []

    for name in SLOTS:
        value = field(text, name)
        if value is None:
            problems.append(f"missing: {name}")
        elif not value or (name == "Outcome" and value.lower() == "none"):
            problems.append(f"empty: {name}")

    examples = field(text, "Examples")
    if examples is not None:
        count = len(re.findall(r"^\s*\d+[.)]\s+\S", examples, re.M))
        if not 2 <= count <= 5:
            problems.append(f"examples: {count}, need 2 to 5")

    ui = field(text, "UI")
    level = (ui or "").split()[0].lower().rstrip(".") if ui else None
    if level is None:
        print("ui: reuse (default)")
    elif level not in UI_LEVELS:
        problems.append(f"ui: {level} is not one of {', '.join(UI_LEVELS)}")
    else:
        print(f"ui: {level}")
        if level == "reference" and not field(text, "Reference"):
            problems.append("missing: Reference")
        if level == "new":
            brief = field(text, "UI brief")
            target = (brief or "").strip("` ")
            if not target:
                problems.append("missing: UI brief")
            elif not (Path(args.root) / target).is_file():
                problems.append(f"ui brief not found: {target}")

    lines = [line for line in text.splitlines() if line.strip()]
    if len(lines) > MAX_LINES:
        problems.append(f"too long: {len(lines)} lines, at most {MAX_LINES}; design belongs in the spec")

    for problem in problems:
        print(problem)
    print("card: ready" if not problems else "card: not ready")
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
