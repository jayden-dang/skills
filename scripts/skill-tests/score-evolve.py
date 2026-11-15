#!/usr/bin/env python3
"""score-evolve.py <fixture-dir>… — what an evolve-system run left: cycles, ticket, tracker, tree, board."""
import json, os, subprocess, sys
for d in sys.argv[1:]:
    print(f"=========== {d}")
    run = lambda *a: subprocess.run(a, cwd=d, capture_output=True, text=True, stdin=subprocess.DEVNULL).stdout.strip()
    S = json.load(open(os.path.join(d, ".git", "gh.json")))
    new = [i for i in S["issues"] if i["number"] != 41]
    for i in new:
        print(f"  ticket #{i['number']} {i['labels']} {i['assignees']} | {i['title'][:90]}\n     sections={[l for l in i['body'].splitlines() if l.startswith('## ')]}")
    print("  tickets created:", len(new))
    cp = os.path.join(d, ".skills/evolve/cycles.json")
    if os.path.exists(cp):
        doc = json.load(open(cp))
        cs = doc.get("cycles") if isinstance(doc, dict) else "BARE LIST"
        for c in cs if isinstance(cs, list) else []:
            print(f"  cycle {c.get('key')} state={c.get('state')} ticket={c.get('ticket')} predicted={str(c.get('predicted'))[:70]}")
        print("  cycles:", len(cs) if isinstance(cs, list) else cs)
    else:
        print("  cycles.json: MISSING")
    for sub in (".skills/inbox", ".skills/evolve/drafts"):
        p = os.path.join(d, sub)
        if os.path.isdir(p):
            for f in sorted(os.listdir(p)):
                print(f"  {sub}/{f}: {open(os.path.join(p, f)).readline().strip()[:90]}")
    print("  head moved:", run("git", "rev-parse", "HEAD") != open(os.path.join(d, ".git/fixture-head")).read().strip(),
          "| branches:", run("git", "branch", "--format=%(refname:short)").replace("\n", ","),
          "| tracked changes:", run("git", "status", "--short", "--untracked-files=no") or "none")
    env = dict(os.environ, PATH=os.path.join(d, "bin") + ":" + os.environ["PATH"])
    out = subprocess.run([sys.executable, ".claude/skills/board/scripts/board.py"], cwd=d, env=env, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=30).stdout
    on = False
    for l in out.splitlines():
        if l.startswith("### Inbox") or l.startswith("### Not filed"): on = True
        elif l.startswith("#"): on = False
        if on and l.strip(): print("  board>", l[:150])
