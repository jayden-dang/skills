#!/usr/bin/env python3
"""Lint eval.json files so a skill's runnable assertions stay grounded in real evidence.

A skill's test material lives in two files with two different jobs, and this
check exists to keep them from becoming two sources of truth:

  TESTS.md   the recorded evidence — RED transcripts verbatim, the rationalizations
             the text had to counter, what changed between iterations. The *why*.
  eval.json  the runnable assertions derived from that evidence. The *what must hold*.

The load-bearing rule is `derived_from`: every eval must cite the TESTS.md section
it came from, and that TESTS.md must exist beside it. This is what stops anyone
(agent or human) filling the repo with plausible-sounding assertions for failures
nobody ever observed — the exact thing author-skills' Iron Law forbids. An eval
with no evidence behind it is a guess wearing a test's clothing.

Checks per eval.json:
  - parses as JSON and is a non-empty array of objects
  - each entry has eval_id (unique positive int), eval_name (kebab-case),
    kind ("behavior" or "trigger"), derived_from, prompt, assertions
  - assertions is a non-empty array of non-empty strings
  - the file sits beside a SKILL.md, and a TESTS.md exists in the same directory

Usage:
  lint-skill-evals.py                 # scan every skills/**/eval.json, report coverage
  lint-skill-evals.py FILE [FILE ...] # lint the given files (non-eval.json paths ignored)
"""
import glob
import json
import os
import re
import sys

KEBAB = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*")
KINDS = ("behavior", "trigger")
REQUIRED = ("eval_id", "eval_name", "kind", "derived_from", "prompt", "assertions")


def check(path):
    errs = []
    d = os.path.dirname(path)
    if not os.path.exists(os.path.join(d, "SKILL.md")):
        errs.append("no SKILL.md beside this eval.json")
    if not os.path.exists(os.path.join(d, "TESTS.md")):
        errs.append("no TESTS.md beside this eval.json — an eval must derive from "
                    "recorded evidence, so record the RED/GREEN run first")
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return errs + [f"not valid JSON — {e}"]

    if not isinstance(data, list) or not data:
        return errs + ["eval.json must be a non-empty JSON array"]

    seen = set()
    for i, ev in enumerate(data):
        where = f"entry {i}"
        if not isinstance(ev, dict):
            errs.append(f"{where}: not an object")
            continue
        name = ev.get("eval_name")
        if isinstance(name, str) and name:
            where = f"'{name}'"
        for key in REQUIRED:
            if key not in ev:
                errs.append(f"{where}: missing '{key}'")

        eid = ev.get("eval_id")
        if not isinstance(eid, int) or isinstance(eid, bool) or eid < 1:
            errs.append(f"{where}: 'eval_id' must be a positive integer, got {eid!r}")
        elif eid in seen:
            errs.append(f"{where}: duplicate eval_id {eid}")
        else:
            seen.add(eid)

        if not (isinstance(name, str) and KEBAB.fullmatch(name or "")):
            errs.append(f"{where}: 'eval_name' must be kebab-case, got {name!r}")

        kind = ev.get("kind")
        if kind not in KINDS:
            errs.append(f"{where}: 'kind' must be one of {KINDS}, got {kind!r}")

        for key in ("derived_from", "prompt"):
            val = ev.get(key)
            if not (isinstance(val, str) and val.strip()):
                errs.append(f"{where}: '{key}' must be a non-empty string")

        asserts = ev.get("assertions")
        if not isinstance(asserts, list) or not asserts:
            errs.append(f"{where}: 'assertions' must be a non-empty array")
        elif not all(isinstance(a, str) and a.strip() for a in asserts):
            errs.append(f"{where}: every assertion must be a non-empty string")
    return errs


def main(argv):
    args = [a for a in argv if os.path.basename(a) == "eval.json"]
    scan_all = not args
    files = args if args else sorted(glob.glob("skills/**/eval.json", recursive=True))

    failed = 0
    for path in files:
        errs = check(path)
        if errs:
            failed += 1
            for e in errs:
                print(f"  ✗ {path}: {e}")

    if scan_all:
        skills = sorted(glob.glob("skills/**/SKILL.md", recursive=True))
        tested = {os.path.dirname(p) for p in glob.glob("skills/**/TESTS.md", recursive=True)}
        evaled = {os.path.dirname(p) for p in files}
        n = len(skills)
        print(f"\ncoverage: {len(evaled)}/{n} skills have eval.json; "
              f"{len(tested)}/{n} have TESTS.md")
        gap = sorted(d for d in tested if d not in evaled)
        if gap:
            print(f"evidence recorded but no eval.json yet ({len(gap)}):")
            for d in gap:
                print(f"  - {d.replace('skills/', '')}")

    if failed:
        print(f"\nlint-skill-evals: {failed} of {len(files)} eval.json failed")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
