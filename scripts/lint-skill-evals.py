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
# behavior / trigger assert against an OBSERVED failure and must cite TESTS.md.
# contract asserts only that the skill does what its own text already promises,
# and must cite a heading that really exists in SKILL.md. The split exists so a
# conformance checklist can never be mistaken for a regression test backed by a
# recorded baseline.
EVIDENCE_KINDS = ("behavior", "trigger")
KINDS = EVIDENCE_KINDS + ("contract",)
REQUIRED = ("eval_id", "eval_name", "kind", "derived_from", "prompt", "assertions")


def _skill_text(d):
    try:
        with open(os.path.join(d, "SKILL.md"), encoding="utf-8") as f:
            return f.read()
    except OSError:
        return ""


def check(path):
    errs = []
    d = os.path.dirname(path)
    if not os.path.exists(os.path.join(d, "SKILL.md")):
        errs.append("no SKILL.md beside this eval.json")
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

        src = ev.get("derived_from")
        if isinstance(src, str) and src.strip():
            if kind in EVIDENCE_KINDS:
                if not src.startswith("TESTS.md"):
                    errs.append(f"{where}: a {kind} eval asserts against an observed failure, "
                                "so 'derived_from' must cite TESTS.md")
                elif not os.path.exists(os.path.join(d, "TESTS.md")):
                    errs.append(f"{where}: cites TESTS.md but none exists beside this "
                                "eval.json — record the RED/GREEN run first")
            elif kind == "contract":
                if not src.startswith("SKILL.md § "):
                    errs.append(f"{where}: a contract eval must cite its source as "
                                "'SKILL.md § <heading or rule text>'")
                else:
                    quoted = src[len("SKILL.md § "):].split(" — ")[0].strip()
                    if quoted and quoted not in _skill_text(d):
                        errs.append(f"{where}: SKILL.md contains no {quoted!r} — a contract "
                                    "eval may only assert what the skill's own text states")

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
        evaled, backed = set(), set()
        for p in files:
            d = os.path.dirname(p)
            evaled.add(d)
            try:
                with open(p, encoding="utf-8") as f:
                    if any(e.get("kind") in EVIDENCE_KINDS for e in json.load(f)):
                        backed.add(d)
            except (OSError, json.JSONDecodeError, AttributeError, TypeError):
                pass
        n = len(skills)
        print(f"\ncoverage: {len(evaled)}/{n} skills have eval.json")
        print(f"  evidence-backed (behavior/trigger, from a recorded baseline): {len(backed)}/{n}")
        print(f"  contract-only   (asserts what SKILL.md already promises):     "
              f"{len(evaled - backed)}/{n}")
        gap = sorted(d for d in tested if d not in evaled)
        if gap:
            print(f"evidence recorded but no eval.json yet ({len(gap)}):")
            for d in gap:
                print(f"  - {d.replace('skills/', '')}")
        unproven = sorted(d for d in evaled - backed if d in tested)
        if unproven:
            print(f"has TESTS.md but only contract evals ({len(unproven)}) — "
                  "recorded evidence not yet converted:")
            for d in unproven:
                print(f"  - {d.replace('skills/', '')}")

    if failed:
        print(f"\nlint-skill-evals: {failed} of {len(files)} eval.json failed")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
