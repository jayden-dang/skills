#!/usr/bin/env python3
"""retire.py <child> [--into <parent> --as <file.md>] [--no-deleted-list]

Retire a skill. With --into, its body becomes a sibling file of the parent and every pointer to it
is rewritten to the parent; without, the skill is deleted and the pointers left behind are listed.
Mechanical only: the parent's own text (the pointer to the new file, its description) is edited by
hand afterwards, and every rewritten line is printed for review. Run from the repo root.
"""
import argparse, glob, json, os, re, shutil, subprocess, sys

ap = argparse.ArgumentParser()
ap.add_argument("child"); ap.add_argument("--into"); ap.add_argument("--as", dest="file")
ap.add_argument("--no-deleted-list", action="store_true", help="name too generic to grep for (e.g. reflect)")
a = ap.parse_args()
child, parent = a.child, a.into
(cdir,) = glob.glob(f"skills/*/{child}")
pdir = glob.glob(f"skills/*/{parent}")[0] if parent else None


def read(p): return open(p).read()
def write(p, s): open(p, "w").write(s)


# 1. files
if parent:
    body = read(f"{cdir}/SKILL.md").split("---", 2)[2].lstrip("\n")
    assert not os.path.exists(f"{pdir}/{a.file}"), f"{a.file} exists in {pdir}"
    write(f"{pdir}/{a.file}", body)
    for f in sorted(glob.glob(f"{cdir}/**", recursive=True)):
        if os.path.isdir(f): continue
        rel = os.path.relpath(f, cdir)
        if rel == "SKILL.md": continue
        dst = f"{pdir}/{rel}"
        if rel == "TESTS.md":
            t = read(f).split("\n", 1)
            old = read(dst) if os.path.exists(dst) else f"# TESTS.md — {parent}\n"
            write(dst, old.rstrip("\n") + f"\n\n---\n\n# Merged from `{child}` — now `{a.file}` beside this skill\n" + (t[1] if len(t) > 1 else "") )
        elif rel == "eval.json":
            mine = json.load(open(dst)) if os.path.exists(dst) else []
            nid = max([e["eval_id"] for e in mine] or [0])
            dropped = 0
            for e in json.load(open(f)):
                if e.get("kind") == "contract":  # cites the child's SKILL.md headings, which moved to a sibling
                    dropped += 1; continue
                nid += 1; e["eval_id"] = nid; mine.append(e)
            json.dump(mine, open(dst, "w"), indent=2); open(dst, "a").write("\n")
            print(f"  eval.json: merged, {dropped} contract eval(s) dropped")
        else:
            if os.path.exists(dst) and open(dst, "rb").read() == open(f, "rb").read(): continue
            assert not os.path.exists(dst), f"collision: {dst}"
            os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copy2(f, dst)
shutil.rmtree(cdir)

# 2. pointers
SKIP = ("/TESTS.md", "CHANGELOG.md", "/docs/releases/", "/docs/design/", "/.skills/", "/node_modules/", "/.git/")
files = [f for pat in ("skills/**/*.md", "skills/**/*.json", "docs/**/*.md", "templates/**/*.md", "*.md")
         for f in glob.glob(pat, recursive=True) if not any(s in "/" + f for s in SKIP)]
c = re.escape(child)
changed = []
left = []
for f in sorted(set(files)):
    s = read(f); o = s
    if parent:
        s = re.sub(rf"\[`/?{c}`\]\((\.\./skills/|skills/)?{c}\.md\)", lambda m: f"[`{parent}`]({m.group(1) or ''}{parent}.md)", s)
        s = re.sub(rf"`/{c}`", f"`/{parent}`", s)
        s = re.sub(rf"`{c}`", f"`{parent}`", s)
        s = re.sub(rf"(?<![\w/.-]){c}(?![\w.-])", parent, s)
        s = re.sub(rf"`{re.escape(parent)}`(,| and| or|/) `{re.escape(parent)}`", f"`{parent}`", s)
    if s != o:
        write(f, s)
        for x, y in zip(o.splitlines(), s.splitlines()):
            if x != y: changed.append(f"{f}: {y.strip()[:170]}")
    if re.search(rf"(?<![\w-]){c}(?![\w-])", s): left.append(f)

# 3. guide page, README row, manifests, counts, DELETED
g = f"docs/guide/skills/{child}.md"
if os.path.exists(g): os.remove(g)
r = "docs/guide/skills/README.md"; s = read(r)
s2 = re.sub(rf"(?m)^\| \[`{c}`\][^\n]*\n", "", s)
write(r, s2)
for m in (".claude-plugin/plugin.json", ".claude-plugin/marketplace.json", ".kimi-plugin/plugin.json"):
    s = read(m); s2 = re.sub(rf'\s*"\./{re.escape(cdir)}",?', "", s)
    s2 = re.sub(r",(\s*\])", r"\1", s2)
    assert s2 != s, m; write(m, s2); json.load(open(m))
n = len(glob.glob("skills/*/*/SKILL.md"))
for p, pat, fmt in (("AGENTS.md", r"\*\*\d+ skills across", "**{} skills across"),
                    ("docs/guide/skills/README.md", r"(?m)^\d+ skills in eleven buckets", "{} skills in eleven buckets"),
                    ("docs/guide/START-HERE.md", r"\(\d+ engineering skills\)", "({} engineering skills)"),
                    ("docs/guide/methodology/overview.md", r"\*\*~\d+ skills\*\*", "**~{} skills**")):
    s = read(p); s2 = re.sub(pat, fmt.format(n), s, count=1); assert s2 != s or str(n) in s, p; write(p, s2)
if not a.no_deleted_list:
    q = "scripts/qa-set.py"; s = read(q)
    s2 = s.replace('"pathfind", "work-the-problem"]', f'"pathfind", "work-the-problem", "{child}"]') if '"pathfind", "work-the-problem"]' in s \
        else re.sub(r'(DELETED = \[.*?)\]', lambda m: m.group(1) + f', "{child}"]', s, count=1, flags=re.S)
    assert s2 != s; write(q, s2)

print(f"{child}: {'merged into ' + parent + ' as ' + a.file if parent else 'deleted'}; {n} skills; {len(changed)} line(s) rewritten")
for l in changed: print("   ~", l)
if left: print("  !! still names it:", ", ".join(left))
