#!/usr/bin/env python3
"""List the rule atoms in a SKILL.md, and diff them across a trim.

A length pass fails silently: a WHEN branch, a Done-when clause, a rationalization
row, or a red-flag bullet disappears in the edit and nothing notices until an agent
reaches that branch weeks later. Reading the diff by hand is what everyone plans to
do and what nobody does the same way twice on file 17 of 22.

An atom is a line that carries a rule rather than describing one: a heading, a
conditional, an imperative, a hand-off, a completion criterion, a table row, a
bullet under Red Flags, or anything inside a gate block. Prose is not an atom, so
tightening a paragraph is invisible here and losing a branch is not.

Usage:
    python3 scripts/skill-rule-inventory.py <SKILL.md>              # list atoms
    python3 scripts/skill-rule-inventory.py --diff <old> <new>...   # what vanished

--diff reads the OLD file from git (default HEAD) and checks every atom still
appears in the union of the NEW paths given, so an atom moved into a sibling
reference file counts as kept. Exit 1 if any atom has no home.
"""

import os
import re
import subprocess
import sys

ATOM = re.compile(
    r"^\s*(#{1,6}\s|\||[-*]\s|\d+\.\s)"      # heading, table row, bullet, numbered step
    r"|\b(WHEN|IF|MUST|NEVER|REQUIRED|ALWAYS|DO NOT|Done when)\b"
    r"|</?(NON-NEGOTIABLE|HARD-GATE|SUBAGENT-EXEMPT)>",
)
NOISE = re.compile(r"^\s*\|[\s|:-]*\|?\s*$")   # table separator rows


def normalise(line):
    line = re.sub(r"[`*_]", "", line)
    line = re.sub(r"\s+", " ", line).strip().lower()
    return line.rstrip(".")


def atoms(text):
    out = []
    fenced = False
    for raw in text.splitlines():
        if raw.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced or not raw.strip() or NOISE.match(raw):
            continue
        if ATOM.search(raw):
            n = normalise(raw)
            if len(n) > 3:
                out.append((n, raw.strip()))
    return out


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def from_git(path, ref="HEAD"):
    r = subprocess.run(["git", "show", f"{ref}:{path}"], capture_output=True, text=True)
    if r.returncode:
        sys.exit(f"cannot read {path} at {ref}: {r.stderr.strip()}")
    return r.stdout


def cmd_list(path):
    found = atoms(read(path))
    for _, raw in found:
        print(raw)
    print(f"\n{len(found)} atoms", file=sys.stderr)
    return 0


def cmd_diff(old_path, new_paths, ref="HEAD"):
    before = atoms(from_git(old_path, ref))
    after = set()
    for p in new_paths:
        after |= {n for n, _ in atoms(read(p))}

    # A sibling nothing names is a rule deleted with extra steps: the atoms are
    # present, so the atom check passes, and no run will ever reach them.
    skill = read(old_path)
    orphans = [p for p in new_paths
               if p != old_path and os.path.basename(p) not in skill]

    # An atom reworded in place is not an atom lost, but an exact match cannot
    # tell the two apart and leaves a human reading every flag. Score each miss
    # against its closest surviving line so a rewrite reads differently from a
    # deletion.
    after_tokens = [(set(n.split()), n) for n in after]
    # Coverage is measured against the whole surviving text, not line by line: a
    # four-item list folded into one paragraph keeps every rule while no single
    # line holds most of any original item.
    corpus_words = set()
    for p in new_paths:
        corpus_words |= set(normalise(read(p)).split())

    def closest(atom):
        """Fraction of the atom's distinctive words that survive anywhere, plus
        the nearest single line as a hint for whoever reads the flag."""
        want = set(atom.split())
        distinctive = {w for w in want if len(w) > 4} or want
        coverage = len(distinctive & corpus_words) / len(distinctive)
        best, best_line = 0.0, ""
        for have, line in after_tokens:
            score = len(want & have) / len(want) if want else 0.0
            if score > best:
                best, best_line = score, line
        return coverage, best_line

    missing = [raw for n, raw in before if n not in after]
    print(f"{old_path}: {len(before)} atoms at {ref}, {len(after)} across "
          f"{len(new_paths)} file(s) now")
    if orphans:
        print(f"\n{len(orphans)} sibling file(s) no pointer in {os.path.basename(old_path)} names:")
        for p in orphans:
            print(f"  - {p}")
        print("\nAtoms inside an unreachable file still count as present, so the "
              "atom check above cannot see this. Name the file, or fold it back.")

    reworded, lost = [], []
    for n, raw in ((normalise(r), r) for r in missing):
        score, near = closest(n)
        (reworded if score >= 0.7 else lost).append((score, raw, near))

    if reworded:
        print(f"\n{len(reworded)} reworded rather than removed (>=70% of their "
              f"distinctive words survive somewhere); read these only to check the "
              f"rule did not shift:")
        for score, raw, _ in reworded:
            print(f"  {score:.0%}  {raw[:88]}")

    if lost:
        print(f"\n{len(lost)} with no home in the new file set:")
        for score, raw, near in lost:
            print(f"  - {raw}")
            print(f"      {score:.0%} of its distinctive words survive anywhere")
            if near:
                print(f"      closest line: {near[:76]}")
        print("\nEach must be a deliberate no-op deletion or a duplicate whose one "
              "home survives. Anything else is a rule lost to the trim.")
    if lost or orphans:
        return 1
    print("every atom still has a home, and every sibling is named")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        sys.exit(__doc__)
    if args[0] == "--diff":
        if len(args) < 3:
            sys.exit("usage: --diff <old-path> <new-path>...")
        sys.exit(cmd_diff(args[1], args[2:]))
    sys.exit(cmd_list(args[0]))
