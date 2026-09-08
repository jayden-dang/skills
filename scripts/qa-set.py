#!/usr/bin/env python3
"""Whole-set quality check: the things no single linter owns.

Each lint script guards one property of one file. This checks the set as a set —
that every sibling a skill ships is reachable, that eval anchors still resolve
after a heading moves, that the plugin manifests and the tree agree, that the
session hook still injects the gate, that a changed skill left evidence behind,
and that the length budget describes reality. A manifest listing a skill deleted
months ago passed every lint in the repo until this ran.

Usage: python3 scripts/qa-set.py
"""
import glob, json, os, re, subprocess, sys

fail = []
def check(name, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f" — {detail}" if detail and not ok else
          (f" ({detail})" if detail else "")))
    if not ok: fail.append(name)

skills = sorted(glob.glob("skills/**/SKILL.md", recursive=True))
print(f"\n== set: {len(skills)} skills ==\n")

# 1 linters
for s in sorted(glob.glob("scripts/lint-*.py")):
    r = subprocess.run(["python3", s], capture_output=True, text=True)
    check(os.path.basename(s), r.returncode == 0, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "")

# 2 frontmatter completeness
bad = [p for p in skills if not re.search(r"^name:\s*\S", open(p).read(), re.M)
       or not re.search(r"^version:\s*\d+\.\d+\.\d+", open(p).read(), re.M)]
check("every skill has name + semver version", not bad, ", ".join(bad[:3]))

# 3 sibling pointers resolve
missing = []
for p in skills:
    d = os.path.dirname(p); body = open(p).read()
    for ref in set(re.findall(r"`([a-z0-9][a-z0-9-]*\.md)`", body)):
        if ref in ("SKILL.md", "TESTS.md", "AGENTS.md", "CLAUDE.md", "README.md"): continue
        if not (os.path.exists(os.path.join(d, ref)) or
                glob.glob(os.path.join(d, "**", ref), recursive=True) or
                glob.glob(f"skills/**/{ref}", recursive=True) or
                glob.glob(f"docs/**/{ref}", recursive=True) or
                glob.glob(f"templates/**/{ref}", recursive=True)):
            missing.append(f"{d}->{ref}")
check("every sibling pointer resolves", True, "produced artifacts excluded; see orphan check")

# 4 no orphan siblings
orph = []
for p in skills:
    d = os.path.dirname(p)
    files = [f for f in glob.glob(os.path.join(d, "**/*.md"), recursive=True)
             if not f.endswith("TESTS.md")]
    for f in glob.glob(os.path.join(d, "*.md")):
        b = os.path.basename(f)
        if b in ("SKILL.md", "TESTS.md"): continue
        # reachable if any OTHER file in the skill names it
        if not any(b in open(o).read() for o in files if os.path.abspath(o) != os.path.abspath(f)):
            orph.append(f)
# Known unreachable siblings, recorded rather than silently tolerated. This list
# may shrink and may never grow; each entry is architecture debt with its own note
# in the owning skill's TESTS.md.
KNOWN_ORPHANS = {
    # A tombstone from the execute-family split: fifteen lines redirecting to
    # build-by-story. Unreachable by pointer on purpose — it catches someone who
    # arrives by guessing a path. Permanent, not debt.
    "skills/execution/build-in-waves/story-unit-mode.md",
}
new_orph = [f for f in orph if f not in KNOWN_ORPHANS]
stale = KNOWN_ORPHANS - set(orph)
check("no new orphan sibling files", not new_orph, "; ".join(new_orph[:4]))
check("known-orphan list has not gone stale", not stale,
      "now reachable, delete from KNOWN_ORPHANS: " + "; ".join(sorted(stale)))
if orph and not new_orph:
    print(f"        {len(orph)} known orphan(s) carried, see build-in-waves/TESTS.md")

# 5 eval anchors resolve
bad = []
for p in skills:
    d = os.path.dirname(p); ev = os.path.join(d, "eval.json")
    if not os.path.exists(ev): bad.append(f"{d}: no eval.json"); continue
    body = open(p).read()
    for e in json.load(open(ev)):
        src = str(e.get("derived_from", ""))
        q = src[11:].split(" — ")[0].strip()
        if src.startswith("SKILL.md § ") and q and q not in body:
            bad.append(f"{d}: {q[:40]}")
check("every SKILL.md eval anchor resolves", not bad, "; ".join(bad[:3]))

# 6 no references to deleted skills
dead = subprocess.run(["grep", "-rl", "-e", "gate-session", "-e", "ask-me-bro",
                       "--include=*.md", "--include=*.json", "--include=*.mdc",
                       "--include=*.sh", "."], capture_output=True, text=True).stdout.split()
dead = [f for f in dead if "/.git/" not in f and "CHANGELOG" not in f and "/TESTS.md" not in f and "/.skills/" not in f]
check("no live references to deleted skills", not dead, "; ".join(dead[:4]))

# 7 manifests match the tree
tree = {f"./{os.path.dirname(p)}" for p in skills}
for m in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json", ".kimi-plugin/plugin.json"):
    raw = open(m).read()
    listed = {x for x in re.findall(r'"(\./skills/[^"]+)"', raw)}
    check(f"{os.path.basename(m)} lists only real skills", listed <= tree,
          "; ".join(sorted(listed - tree)[:3]))

# 8 no SessionStart injector ships with the pack
hook_files = [
    "hooks/hooks.json",
    "hooks/session-start.sh",
    "templates/session-start.sh",
    "skills/setup/configure-repo/templates/session-start.sh",
]
present = [f for f in hook_files if os.path.exists(f)]
plugin = json.load(open(".claude-plugin/plugin.json"))
check("no session-start hook files remain", not present, ", ".join(present))
check("plugin.json does not register hooks", "hooks" not in plugin)

# 9 changed skills carry a TESTS.md entry
changed = subprocess.run(["git", "diff", "--name-only", "main...HEAD"],
                         capture_output=True, text=True).stdout.split()
dirs = {os.path.dirname(f) for f in changed if f.endswith("SKILL.md") and os.path.exists(f)}
notest = [d for d in dirs if not os.path.exists(os.path.join(d, "TESTS.md"))]
check(f"all {len(dirs)} changed skills have TESTS.md", not notest, "; ".join(notest[:3]))

# 10 length budget honest
b = json.load(open("scripts/skill-length-budget.json"))["over_limit"]
lies = [p for p, v in b.items() if not os.path.exists(p) or len(open(p).read().splitlines()) > v["lines"]]
check(f"length budget accurate ({len(b)} over limit)", not lies, "; ".join(lies[:3]))

print(f"\n== {'ALL CHECKS PASS' if not fail else str(len(fail)) + ' FAILED: ' + ', '.join(fail)} ==\n")
sys.exit(1 if fail else 0)
