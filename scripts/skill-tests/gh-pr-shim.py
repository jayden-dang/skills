#!/usr/bin/env python3
"""A stand-in `gh` for pull-request work in a throwaway repo, state in .git/gh-pr.json.

Supports: pr create / view / edit / comment / list / ready, issue view / comment / edit (no-op
success), repo view, api user. Every call's args and body are appended to .git/gh-calls.jsonl,
so a scorer can read exactly what reached the PR.
"""
import json, os, subprocess, sys

git_dir = subprocess.run(["git", "rev-parse", "--git-common-dir"], capture_output=True, text=True).stdout.strip()
P = os.path.join(git_dir, "gh-pr.json")
S = json.load(open(P)) if os.path.exists(P) else {"prs": [], "issues": [{"number": 41, "title": "Seat booking", "state": "open", "comments": [], "body": "Book seats on a sailing."}]}
a = sys.argv[1:]


def opt(name):
    for i, x in enumerate(a):
        if x == name and i + 1 < len(a):
            return a[i + 1]
        if x.startswith(name + "="):
            return x.split("=", 1)[1]
    return None


def body():
    f = opt("--body-file") or opt("-F")
    if f:
        return sys.stdin.read() if f == "-" else open(f).read()
    return opt("--body") or opt("-b") or ""


def save():
    json.dump(S, open(P, "w"), indent=1)


def head():
    return subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()


def branch():
    return subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()


def pr_for(ref):
    if ref and ref.lstrip("#").isdigit():
        return next((p for p in S["prs"] if p["number"] == int(ref.lstrip("#"))), None)
    b = ref or branch()
    return next((p for p in S["prs"] if p["headRefName"] == b), None)


b = body() if any(x in a for x in ("--body", "-b", "--body-file", "-F")) else None
with open(os.path.join(git_dir, "gh-calls.jsonl"), "a") as log:
    log.write(json.dumps({"args": a, "body": b}) + "\n")

URL = "https://github.com/harbourline/app/pull/{}"
if a[:2] == ["api", "user"]:
    print(json.dumps({"login": "thao"}))
elif a[:2] == ["repo", "view"]:
    print(json.dumps({"nameWithOwner": "harbourline/app", "defaultBranchRef": {"name": "main"}}) if "--json" in a else "harbourline/app")
elif a[:2] == ["pr", "create"]:
    n = 100 + len(S["prs"]) + 1
    S["prs"].append({"number": n, "title": opt("--title") or opt("-t") or "", "body": b or "", "state": "OPEN",
                     "isDraft": "--draft" in a or "-d" in a, "headRefName": opt("--head") or branch(),
                     "baseRefName": opt("--base") or opt("-B") or "main", "comments": [], "headRefOid": head(),
                     "url": URL.format(n)})
    save(); print(URL.format(n))
elif a[:2] == ["pr", "view"]:
    ref = a[2] if len(a) > 2 and not a[2].startswith("-") else None
    p = pr_for(ref)
    if not p:
        sys.exit("no pull requests found for branch \"%s\"" % (ref or branch()))
    p["headRefOid"] = head()
    j = opt("--json")
    if j:
        print(json.dumps({k: p.get(k) for k in j.split(",")}))
    else:
        print(f"title:\t{p['title']}\nstate:\t{p['state']}\nurl:\t{p['url']}\n--\n{p['body']}")
elif a[:2] == ["pr", "edit"]:
    ref = a[2] if len(a) > 2 and not a[2].startswith("-") else None
    p = pr_for(ref)
    if not p:
        sys.exit("no pull requests found")
    if b is not None:
        p["body"] = b
    if opt("--title"):
        p["title"] = opt("--title")
    save(); print(p["url"])
elif a[:2] == ["pr", "ready"]:
    p = pr_for(a[2] if len(a) > 2 else None); p["isDraft"] = False; save(); print(f"✓ Pull request #{p['number']} is marked as ready for review")
elif a[:2] == ["pr", "comment"]:
    ref = a[2] if len(a) > 2 and not a[2].startswith("-") else None
    p = pr_for(ref)
    if not p:
        sys.exit("no pull requests found")
    p["comments"].append({"author": {"login": "thao"}, "body": b or ""}); save()
    print(p["url"] + f"#issuecomment-{len(p['comments'])}")
elif a[:2] == ["pr", "list"]:
    print(json.dumps([{k: p.get(k) for k in (opt("--json") or "number,url,headRefName").split(",")} for p in S["prs"]]) if "--json" in a else "\n".join(f"{p['number']}\t{p['title']}\t{p['headRefName']}" for p in S["prs"]))
elif a[:1] == ["issue"]:
    n = next((x for x in a[2:] if x.lstrip("#").isdigit()), "41")
    i = next((i for i in S["issues"] if str(i["number"]) == n.lstrip("#")), S["issues"][0])
    if a[1] == "comment":
        i["comments"].append({"author": {"login": "thao"}, "body": b or ""}); save()
    if a[1] == "view":
        j = opt("--json")
        print(json.dumps({k: i.get(k) for k in j.split(",")}) if j else f"title:\t{i['title']}\nstate:\t{i['state']}\n--\n{i['body']}")
    else:
        print(f"https://github.com/harbourline/app/issues/{i['number']}")
else:
    sys.exit(f"unknown command \"{' '.join(a[:2])}\" for \"gh\"")
