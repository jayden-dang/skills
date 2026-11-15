#!/usr/bin/env python3
import json, sys, os, subprocess, datetime
root = subprocess.run(["git", "rev-parse", "--git-dir"], capture_output=True, text=True).stdout.strip()
P = os.path.join(root, "gh.json")
S = json.load(open(P))
a = sys.argv[1:]
def save(): json.dump(S, open(P, "w"), indent=1)
def opt(name, many=False):
    out = []
    for i, x in enumerate(a):
        if x == name and i + 1 < len(a): out.append(a[i + 1])
        elif x.startswith(name + "="): out.append(x.split("=", 1)[1])
    if many: return [y for x in out for y in x.split(",") if y]
    return out[-1] if out else None
def body():
    f = opt("--body-file") or opt("-F")
    if f: return sys.stdin.read() if f == "-" else open(f).read()
    return opt("--body") or opt("-b") or ""
def shape(i, fields):
    full = {"number": i["number"], "title": i["title"], "body": i["body"], "state": i["state"].upper(),
            "labels": [{"name": l} for l in i["labels"]], "assignees": [{"login": l} for l in i["assignees"]],
            "comments": i["comments"], "url": f"https://github.com/quayside/billing/issues/{i['number']}",
            "createdAt": i.get("createdAt", "")}
    return {k: full[k] for k in fields if k in full} if fields else full
def find(n):
    for i in S["issues"]:
        if str(i["number"]) == str(n).lstrip("#"): return i
    sys.exit(f"GraphQL: Could not resolve to an Issue with the number of {n}. (repository.issue)")
if a[:2] == ["api", "user"]:
    print(json.dumps({"login": "lan"}))
elif a[:2] == ["issue", "list"]:
    st = opt("--state") or opt("-s") or "open"
    lab = opt("--label", True) + opt("-l", True)
    xs = [i for i in S["issues"] if st == "all" or i["state"] == st]
    xs = [i for i in xs if all(l in i["labels"] for l in lab)]
    j = opt("--json")
    if j is not None: print(json.dumps([shape(i, [f for f in j.split(",") if f != "blockedBy"]) for i in xs]))
    else:
        for i in xs: print(f"{i['number']}\t{i['state'].upper()}\t{i['title']}\t{', '.join(i['labels'])}")
elif a[:2] == ["issue", "create"]:
    t = opt("--title") or opt("-t")
    if not t: sys.exit("must provide `--title` and `--body` (or `--fill` or `fill-first` or `--fill-verbose`) when not running interactively")
    n = max(i["number"] for i in S["issues"] + S["prs"]) + 1
    S["issues"].append({"number": n, "title": t, "body": body(), "state": "open",
                        "labels": opt("--label", True) + opt("-l", True),
                        "assignees": ["lan" if x == "@me" else x for x in opt("--assignee", True) + opt("-a", True)],
                        "comments": [], "createdAt": datetime.datetime.utcnow().isoformat() + "Z"})
    save(); print(f"https://github.com/quayside/billing/issues/{n}")
elif a[:2] == ["issue", "view"]:
    i = find(a[2]); j = opt("--json")
    if j is not None: print(json.dumps(shape(i, j.split(","))))
    else:
        print(f"title:\t{i['title']}\nstate:\t{i['state'].upper()}\nlabels:\t{', '.join(i['labels'])}\nassignees:\t{', '.join(i['assignees'])}\nnumber:\t{i['number']}\n--\n{i['body']}")
        for c in i["comments"]: print(f"--\n{c['author']['login']}:\n{c['body']}")
elif a[:2] == ["issue", "edit"]:
    i = find(a[2])
    for l in opt("--add-label", True):
        if l not in i["labels"]: i["labels"].append(l)
    i["labels"] = [l for l in i["labels"] if l not in opt("--remove-label", True)]
    for l in opt("--add-assignee", True):
        l = "lan" if l == "@me" else l
        if l not in i["assignees"]: i["assignees"].append(l)
    if opt("--title"): i["title"] = opt("--title")
    if opt("--body") or opt("--body-file"): i["body"] = body()
    save(); print(f"https://github.com/quayside/billing/issues/{i['number']}")
elif a[:2] == ["issue", "comment"]:
    i = find(a[2]); i["comments"].append({"author": {"login": "lan"}, "body": body()}); save()
    print(f"https://github.com/quayside/billing/issues/{i['number']}#issuecomment-{len(i['comments'])}")
elif a[:2] == ["issue", "close"]:
    i = find(a[2]); i["state"] = "closed"; save(); print(f"✓ Closed issue #{i['number']}")
elif a[:2] == ["pr", "list"]:
    st = opt("--state") or "open"
    xs = [p for p in S["prs"] if st == "all" or p["state"] == st]
    j = opt("--json")
    if j is not None: print(json.dumps([{k: ({**p, "state": p["state"].upper()}).get(k) for k in j.split(",")} for p in xs]))
    else:
        for p in xs: print(f"{p['number']}\t{p['title']}\t{p['headRefName']}\t{p['state'].upper()}")
elif a[:2] == ["label", "list"]:
    for l in S["labels"]: print(l)
elif a[:2] == ["repo", "view"]:
    print("quayside/billing")
else:
    sys.exit(f"unknown command \"{' '.join(a[:2])}\" for \"gh\"")
