#!/usr/bin/env python3
"""score-inbox.py <fixture-dir>… — new tickets per fixture, and what board.py shows in Inbox."""
import json, os, subprocess, sys

for d in sys.argv[1:]:
    print(f"=========== {d}")
    S = json.load(open(os.path.join(d, ".git", "gh.json")))
    for i in S["issues"]:
        if i["number"] > 13:
            heads = [l for l in i["body"].splitlines() if l.startswith("## ")]
            leak = [x for x in ("src/", ".js:", "PAY-1", "REFUND-1", "LATEFEE-1") if x in i["body"]]
            print(f"  #{i['number']} {i['state']} {i['labels']} {i['assignees']} | {i['title'][:80]}\n     sections={heads} internal={leak}")
    dirty = subprocess.run(["git", "status", "--short"], cwd=d, capture_output=True, text=True).stdout.strip()
    print("  tree:", dirty or "clean")
    drafts = [os.path.join(r, f) for r, _, fs in os.walk(d) if ".git" not in r and "node_modules" not in r
              for f in fs if "draft" in r.lower() or "inbox" in r.lower()]
    print("  draft files:", drafts or "none")
    env = dict(os.environ, PATH=os.path.join(d, "bin") + ":" + os.environ["PATH"])
    out = subprocess.run([sys.executable, ".claude/skills/board/scripts/board.py"], cwd=d, env=env,
                         capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=30).stdout
    on = False
    for l in out.splitlines():
        if l.startswith("### Inbox") or l.startswith("### Not filed"): on = True
        elif l.startswith("#"): on = False
        if on and l.strip(): print("  board>", l)
