#!/usr/bin/env python3
"""board.py [--issues FILE] [--prs FILE] [--drafts FILE] [--me LOGIN] — the board, by state.

Run from the repo root. Read-only. With no files on a github tracker it asks `gh` itself:
  gh issue list --state open --json number,title,labels,assignees,comments,body --limit 300
  gh pr list --state open --json number,title,body,headRefName --limit 100
Any other tracker: write the same JSON shapes from its own ops and pass the files.
--drafts is a JSON list of {"title", "status", "comment"} rows awaiting sign-off.

Every section always prints, `none` when empty, so a missing source shows as missing.
"""
import argparse, json, re, subprocess, sys
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument("--issues"); ap.add_argument("--prs"); ap.add_argument("--drafts"); ap.add_argument("--me")
o = ap.parse_args()


def gh(*args):
    r = subprocess.run(["gh", *args], capture_output=True, text=True)
    if r.returncode:
        print(f"# source failed: gh {' '.join(args[:2])}: {r.stderr.strip()[:200]}")
        return None
    return r.stdout


def load(path, *cmd):
    if path:
        return json.loads(Path(path).read_text())
    out = gh(*cmd)
    return json.loads(out) if out else []


issues = load(o.issues, "issue", "list", "--state", "open", "--json", "number,title,labels,assignees,comments,body", "--limit", "300")
prs = [p for p in load(o.prs, "pr", "list", "--state", "open", "--json", "number,title,body,headRefName,state", "--limit", "100")
       if str(p.get("state", "OPEN")).upper() == "OPEN"]
drafts = json.loads(Path(o.drafts).read_text()) if o.drafts else None
me = o.me or (json.loads(gh("api", "user") or "{}").get("login") if not o.issues else None)

# Role ← label, from docs/agents/triage-labels.md.
roles = {}
tl = Path("docs/agents/triage-labels.md")
if tl.exists():
    for role, label in re.findall(r"^\|\s*([a-z-]+)\s*\|\s*`?([^|`]+?)`?\s*\|", tl.read_text(), re.M):
        if role != "canonical" and not label.startswith("<"):
            roles[label.strip()] = role
STATES = ["needs-triage", "shaping", "ready-for-agent", "building", "in-review", "needs-info", "ready-for-human", "wontfix", "shipped"]

# Feature status ← "Requirements covered: CODE-…" → catalog row → requirements.md Status.
spec = {}
for shard in sorted(Path("docs/specs/catalog").glob("*.md")) if Path("docs/specs/catalog").is_dir() else []:
    for line in shard.read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) > 3 and re.fullmatch(r"[A-Z][A-Z0-9-]*", cells[0]):
            d = (shard.parent / cells[2].strip("`")).resolve()
            st = {}
            for f in ("requirements", "design", "tasks"):
                p = d / f"{f}.md"
                m = re.search(r"^Status:\s*(\w[\w-]*)", p.read_text(), re.M) if p.exists() else None
                st[f] = m.group(1) if m else "missing"
            spec[cells[0]] = st


def names(xs, key):
    return [x[key] if isinstance(x, dict) else x for x in xs or []]


def code_of(i):
    m = re.search(r"Requirements covered:\s*([A-Z][A-Z0-9-]*?)-\d", i.get("body") or "")
    return m.group(1) if m else None


def state_of(i):
    rs = [roles.get(l, l if l in STATES else None) for l in names(i.get("labels"), "name")]
    rs = [r for r in rs if r in STATES]
    return rs


def last_comment(i):
    cs = i.get("comments") or []
    if not cs:
        return "no comment"
    c = cs[-1]
    who = c.get("author", {}).get("login") if isinstance(c.get("author"), dict) else c.get("author")
    return f'{who}: "{" ".join((c.get("body") or "").split())[:220]}"'


pr_closes = {}
for p in prs:
    for c in re.findall(r"(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)", p.get("body") or ""):
        pr_closes[int(c)] = p["number"]
open_nums = {i["number"] for i in issues}

by = {s: [] for s in STATES}
drift = []
for i in issues:
    rs = state_of(i)
    if i["number"] in pr_closes and "in-review" not in rs:
        drift.append(f"#{i['number']} has open PR #{pr_closes[i['number']]} but no in-review role")
        if not rs:
            continue
    if len(rs) > 1:
        drift.append(f"#{i['number']} carries {len(rs)} state roles: {', '.join(rs)}")
    by[rs[0] if rs else "needs-triage"].append(i)
    code = code_of(i)
    st = spec.get(code) if code else None
    if st and st["requirements"] in ("Implemented", "Shipped"):
        drift.append(f"#{i['number']} is open, but {code} reads {st['requirements']}")

print(f"board: {len(issues)} open tickets · {len(prs)} open PRs · me={me or 'unknown'}")
print("\n## Waiting on you")
print("### In review (open PRs)")
for p in prs:
    body = p.get("body") or ""
    closes = re.findall(r"(?i)\b(?:close[sd]?|fix(?:e[sd])?|resolve[sd]?)\s+#(\d+)", body)
    m = re.search(r"(?ims)^#+\s*needs a decision[^\n]*\n(.*?)(?=^#+\s|\Z)", body)
    dec = " ".join(m.group(1).split())[:260] if m else "none"
    print(f"- PR #{p['number']} {p.get('title')} — closes {', '.join('#' + c for c in closes) or 'nothing'} — decision: {dec}")
if not prs:
    print("none")
for title, s in (("Needs input (the open question)", "needs-info"), ("Shaping (spec to write or approve)", "shaping"),
                 ("Inbox (not triaged)", "needs-triage")):
    print(f"\n### {title}")
    for i in by[s]:
        extra = last_comment(i) if s == "needs-info" else ""
        if s == "shaping":
            st = spec.get(code_of(i) or "")
            extra = "no spec yet" if not st else ", ".join(f"{k} {v}" for k, v in st.items())
        print(f"- #{i['number']} {i['title']}" + (f" — {extra}" if extra else ""))
    if not by[s]:
        print("none")
print("\n### Human-only")
for i in by["ready-for-human"]:
    who = ", ".join(names(i.get("assignees"), "login")) or "unassigned"
    print(f"- #{i['number']} {i['title']} — {who}{' (you)' if me and me in who else ''} — {last_comment(i)}")
if not by["ready-for-human"]:
    print("none")
print("\n### Drafts awaiting sign-off")
if drafts is None:
    print("not read (no Notion draft surface, or not passed)")
for d in drafts or []:
    print(f"- {d.get('title')} — {d.get('status')} — {d.get('comment') or 'no comment'}")
if drafts == []:
    print("none")

print("\n## With agents")
print("### Building")
for i in by["building"]:
    print(f"- #{i['number']} {i['title']} — {', '.join(names(i.get('assignees'), 'login')) or 'unassigned'}")
if not by["building"]:
    print("none")
print("### Ready")
for i in by["ready-for-agent"]:
    st = spec.get(code_of(i) or "")
    ok = st and all(v == "Approved" for v in st.values())
    if not ok:
        drift.append(f"#{i['number']} is ready, but its spec is " + ("missing" if not st else ", ".join(f"{k} {v}" for k, v in st.items())))
    blk = [int(b) for b in re.findall(r"Blocked by:\s*((?:#\d+[ ,]*)+)", i.get("body") or "") for b in re.findall(r"\d+", b)]
    blk = [b for b in blk if b in open_nums]
    print(f"- #{i['number']} {i['title']} — {'eligible' if ok else 'NOT eligible'}" + (f", blocked by {', '.join('#%d' % b for b in blk)}" if blk else ""))
if not by["ready-for-agent"]:
    print("none")

print("\n## Board and repo disagree")
print("\n".join(f"- {d}" for d in drift) or "none")
