#!/usr/bin/env python3
"""unflag.py <spec.json> — make user-invoked skills model-invocable, one cluster at a time.

spec.json: {"<skill>": "<new description>", …}. For each skill: drops `disable-model-invocation`,
sets the description, bumps the minor version, takes its name out of AGENTS.md §3's list and
count, and rewrites its guide page's Invocation / Called by rows and its README row.
Run from the repo root. Mechanical only: bodies, TESTS.md and eval.json are edited by hand.
"""
import glob, json, re, sys

spec = json.load(open(sys.argv[1]))
agents = open("AGENTS.md").read()
readme_p = "docs/guide/skills/README.md"
readme = open(readme_p).read()

for name, desc in spec.items():
    (path,) = glob.glob(f"skills/*/{name}/SKILL.md")
    s = open(path).read()
    _, fm, body = s.split("---", 2)
    if "disable-model-invocation: true" not in fm:
        print(f"{name}: already unflagged, skill file left alone")
        fm = None
    v = re.search(r"^version: (\d+)\.(\d+)\.(\d+)$", fm or s.split("---", 2)[1], re.M)
    new_v = f"{v.group(1)}.{int(v.group(2)) + 1}.0"
    lines, out, skip = (fm or "").strip("\n").split("\n"), [], False
    for l in lines:
        if l.startswith("description:"):
            out.append("description: " + json.dumps(desc, ensure_ascii=False) if (":" in desc or desc[0] in "'\"`[{>|*&!%@") else "description: " + desc)
            skip = True
            continue
        if skip and l.startswith((" ", "\t")):
            continue  # continuation of the old description
        skip = False
        if l.startswith("disable-model-invocation"):
            continue
        out.append(f"version: {new_v}" if l.startswith("version:") else l)
    if fm is not None:
        open(path, "w").write("---\n" + "\n".join(out) + "\n---" + body)

    # AGENTS.md §3 list: drop the name, keep separators tidy
    start = agents.index("All ")
    end = agents.index("**A runner the user configured")
    block = agents[start:end]
    nb = re.sub(rf"`{re.escape(name)}`,? ?", "", block, count=1)
    if nb == block: print(f"  !! {name} not in AGENTS list")
    agents = agents[:start] + nb + agents[end:]

    g = f"docs/guide/skills/{name}.md"
    import os
    if not os.path.exists(g):
        print(f"  !! {name}: no guide page"); t = None
    else:
        t = open(g).read()
    t = t or ""
    t2 = re.sub(r"\| \*\*Invocation\*\* \|[^\n]*\|", f"| **Invocation** | model-invoked when its description matches, or `/{name}` |", t, count=1)
    t2 = re.sub(r"\| \*\*Called by\*\* \| nobody[^\n]*\|", "| **Called by** | nobody yet — it fires on what the user asks, or on `/" + name + "` |", t2, count=1)
    if t2 != t and t:
        open(g, "w").write(t2)
    elif "model-invoked when its description matches" not in t:
        print(f"  !! {name}: guide rows not found")

    r2 = re.sub(rf"(\| \[`{re.escape(name)}`\]\({re.escape(name)}\.md\) \| )(?:`/{re.escape(name)}[^|]*`|user)( \|)", rf"\1model, or `/{name}`\2", readme, count=1)
    if r2 == readme:
        print(f"  !! {name}: README row not found")
    readme = r2
    print(f"{name}: {v.group(0)[9:]} -> {new_v}")

n = len(glob.glob("skills/*/*/SKILL.md"))
left = sum("disable-model-invocation: true" in open(p).read().split("---", 2)[1] for p in glob.glob("skills/*/*/SKILL.md"))
agents = re.sub(r"All \d+ of them", f"All {left} of them", agents)
agents = re.sub(r" ·\s*·", " ·", agents)
open("AGENTS.md", "w").write(agents)
open(readme_p, "w").write(readme)
print(f"user-invoked left: {left} of {n}")
