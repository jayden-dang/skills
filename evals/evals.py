#!/usr/bin/env python3
"""Skill evals — Tier 1 (structural) and Tier 2 (lexical routing).

Runs against the skill set in ../skills. No third-party dependency — Python 3.9+
stdlib only, matching the linters in scripts/. Two tiers, both free to run in CI:

  Tier 1  structural   frontmatter, naming, category, key allow-list, line budget.
                       Hard failures — a violation exits non-zero.
  Tier 2  routing      a lexical approximation of skill selection. For each seeded
                       prompt, the intended skill's description must rank in the
                       top-K by keyword overlap (positive) or NOT rank first
                       (negative). Catches the two failure modes that dominate real
                       trigger bugs: a description missing the words users say
                       (false negative) and an over-broad description that outranks
                       the right skill (false positive).

Usage:
    python3 evals/evals.py                # both tiers
    python3 evals/evals.py --tier 1       # structural only
    python3 evals/evals.py --tier 2       # routing only
    python3 evals/evals.py --json         # machine-readable summary
    python3 evals/evals.py --strict       # Tier-2 misses also fail the exit code

Exit code is non-zero when any Tier-1 check fails (always) or any Tier-2 check
fails (only under --strict). This is the foundation the writing-skills TDD loop
and CI both build on.
"""
import argparse
import json
import os
import re
import sys

_EVALS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_EVALS_DIR)
_SKILLS_DIR = os.path.join(_REPO_ROOT, "skills")

CATEGORIES = {
    "meta", "setup", "discovery", "spec", "execution",
    "review", "acceptance", "ship", "track",
}
ALLOWED_KEYS = {"name", "description", "disable-model-invocation"}
KEBAB = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
LINE_BUDGET = 500


# --------------------------------------------------------------------------- #
# loading
# --------------------------------------------------------------------------- #
def discover_skills():
    """Yield (category, name, path) for every skills/<category>/<name>/SKILL.md."""
    for category in sorted(os.listdir(_SKILLS_DIR)):
        cat_dir = os.path.join(_SKILLS_DIR, category)
        if not os.path.isdir(cat_dir):
            continue
        for name in sorted(os.listdir(cat_dir)):
            skill_dir = os.path.join(cat_dir, name)
            if not os.path.isdir(skill_dir):
                continue
            yield category, name, os.path.join(skill_dir, "SKILL.md")


def parse_frontmatter(text):
    """Return (frontmatter_dict, body_str) or (None, text) when absent/malformed.

    Deliberately tiny — the frontmatter here is flat `key: value` scalars only,
    so a YAML dependency would be dead weight. Values may wrap across lines
    (indented continuations), matching how the skills fold long descriptions.
    """
    if not text.startswith("---\n"):
        return None, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return None, text
    block = text[4:end]
    body = text[end + 5:]
    fm, key = {}, None
    for line in block.split("\n"):
        m = re.match(r"^([A-Za-z0-9_-]+):\s?(.*)$", line)
        if m and not line.startswith((" ", "\t")):
            key = m.group(1)
            fm[key] = m.group(2).strip()
        elif key is not None and (line.startswith((" ", "\t"))):
            fm[key] = (fm[key] + " " + line.strip()).strip()
    return fm, body


# --------------------------------------------------------------------------- #
# Tier 1 — structural
# --------------------------------------------------------------------------- #
def tier1(skills):
    """Return list of failure strings; empty means the tier passed."""
    fails = []

    def bad(path, msg):
        rel = os.path.relpath(path, _REPO_ROOT)
        fails.append(f"{rel}: {msg}")

    seen_user_invoked = 0
    seen_categories = set()

    for category, name, path in skills:
        seen_categories.add(category)
        if not os.path.isfile(path):
            bad(path, "no SKILL.md in skill directory")
            continue
        if category not in CATEGORIES:
            bad(path, f"unknown category '{category}' (not one of the 9 buckets)")
        if not KEBAB.match(name):
            bad(path, f"skill name '{name}' is not kebab-case")

        with open(path, "r", encoding="utf-8") as fh:
            text = fh.read()
        fm, body = parse_frontmatter(text)
        if fm is None:
            bad(path, "missing or malformed YAML frontmatter (--- ... ---)")
            continue

        unknown = set(fm) - ALLOWED_KEYS
        if unknown:
            bad(path, f"unexpected frontmatter key(s): {', '.join(sorted(unknown))}")
        if "name" not in fm:
            bad(path, "frontmatter missing 'name'")
        elif fm["name"] != name:
            bad(path, f"frontmatter name '{fm['name']}' != directory '{name}'")
        if not fm.get("description"):
            bad(path, "frontmatter missing 'description'")
        elif not fm["description"].startswith("Use"):
            bad(path, "description must state a triggering condition, starting with 'Use'")
        if "disable-model-invocation" in fm:
            if fm["disable-model-invocation"] != "true":
                bad(path, "disable-model-invocation, when present, must be 'true'")
            else:
                seen_user_invoked += 1

        n_lines = body.count("\n") + 1
        if n_lines > LINE_BUDGET:
            bad(path, f"body is {n_lines} lines, over the {LINE_BUDGET}-line budget")

    missing_cats = CATEGORIES - seen_categories
    if missing_cats:
        fails.append(f"<repo>: categories with no skills: {', '.join(sorted(missing_cats))}")

    return fails, {"user_invoked": seen_user_invoked, "categories": len(seen_categories)}


# --------------------------------------------------------------------------- #
# Tier 2 — lexical routing
# --------------------------------------------------------------------------- #
_STOP = set(
    "a an the to of for and or in on is are be as it its this that with when "
    "before after any you your they them their via not no than then so at by "
    "from into over per each other some every all one two both new use used "
    "using need needs about which what who whom whose only just also more most "
    "should must may can could would will do does done have has had".split()
)


def _tokens(s):
    """Lowercase word stems: drop stopwords, strip a couple of common suffixes."""
    out = []
    for w in re.findall(r"[a-z]+", s.lower()):
        if w in _STOP or len(w) < 3:
            continue
        for suf in ("ing", "ed", "es", "s"):
            if w.endswith(suf) and len(w) - len(suf) >= 3:
                w = w[: -len(suf)]
                break
        out.append(w)
    return out


def _build_index(skills):
    """description tokens per skill + inverse-document-frequency weights."""
    import math

    docs, df = {}, {}
    for _category, name, path in skills:
        with open(path, "r", encoding="utf-8") as fh:
            fm, _ = parse_frontmatter(fh.read())
        toks = _tokens((fm or {}).get("description", ""))
        docs[name] = toks
        for t in set(toks):
            df[t] = df.get(t, 0) + 1
    n = max(1, len(docs))
    idf = {t: math.log(1 + n / c) for t, c in df.items()}
    return docs, idf


def _rank(prompt, docs, idf):
    """Skills ranked by idf-weighted overlap between prompt and each description."""
    q = set(_tokens(prompt))
    scored = []
    for name, toks in docs.items():
        tset = set(toks)
        score = sum(idf.get(t, 0.0) for t in (q & tset))
        scored.append((score, name))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return [name for score, name in scored if score > 0]


def tier2(skills, top_k=3):
    """Return list of failure strings from the seeded trigger cases."""
    cases_path = os.path.join(_EVALS_DIR, "triggers.json")
    if not os.path.isfile(cases_path):
        return [f"{os.path.relpath(cases_path, _REPO_ROOT)}: trigger cases file missing"], {}
    with open(cases_path, "r", encoding="utf-8") as fh:
        cases = json.load(fh)

    docs, idf = _build_index(skills)
    known = set(docs)
    fails, n_pos, n_neg = [], 0, 0

    for skill, spec in cases.items():
        if skill.startswith("_"):
            continue  # metadata keys like _comment
        if skill not in known:
            fails.append(f"triggers.json: '{skill}' is not a real skill")
            continue
        for prompt in spec.get("positive", []):
            n_pos += 1
            ranked = _rank(prompt, docs, idf)
            if skill not in ranked[:top_k]:
                pos = ranked.index(skill) + 1 if skill in ranked else "unranked"
                fails.append(
                    f"[route +] '{skill}' should rank <= {top_k} for "
                    f"\"{prompt}\" but ranked {pos} (top: {', '.join(ranked[:top_k]) or 'none'})"
                )
        for prompt in spec.get("negative", []):
            n_neg += 1
            ranked = _rank(prompt, docs, idf)
            if ranked and ranked[0] == skill:
                fails.append(
                    f"[route -] '{skill}' must NOT rank first for \"{prompt}\" "
                    f"but it did (over-broad description)"
                )
    return fails, {"positive": n_pos, "negative": n_neg}


# --------------------------------------------------------------------------- #
# main
# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser(description="Skill evals — structural + routing.")
    ap.add_argument("--tier", choices=["1", "2", "all"], default="all")
    ap.add_argument("--json", action="store_true", help="machine-readable summary")
    ap.add_argument("--strict", action="store_true", help="Tier-2 misses fail the exit code")
    args = ap.parse_args()

    skills = list(discover_skills())
    report = {"skills": len(skills), "tier1": None, "tier2": None}
    hard_fail = False

    if args.tier in ("1", "all"):
        fails, stats = tier1(skills)
        report["tier1"] = {"failures": fails, **stats}
        if fails:
            hard_fail = True

    if args.tier in ("2", "all"):
        fails, stats = tier2(skills)
        report["tier2"] = {"failures": fails, **stats}
        if fails and args.strict:
            hard_fail = True

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print(f"Skills discovered: {report['skills']}")
        if report["tier1"] is not None:
            t = report["tier1"]
            head = "PASS" if not t["failures"] else f"FAIL ({len(t['failures'])})"
            print(f"\nTier 1 structural: {head}"
                  f"  [{t['user_invoked']} user-invoked, {t['categories']} categories]")
            for f in t["failures"]:
                print(f"  ✗ {f}")
        if report["tier2"] is not None:
            t = report["tier2"]
            head = "PASS" if not t["failures"] else f"{len(t['failures'])} miss(es)"
            note = "" if args.strict else "  (advisory — use --strict to enforce)"
            print(f"\nTier 2 routing: {head}"
                  f"  [{t['positive']} positive, {t['negative']} negative]{note}")
            for f in t["failures"]:
                print(f"  ✗ {f}")
        print("\n" + ("FAILED" if hard_fail else "OK"))

    return 1 if hard_fail else 0


if __name__ == "__main__":
    sys.exit(main())
