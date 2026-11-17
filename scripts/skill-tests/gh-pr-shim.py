#!/usr/bin/env python3
"""A stand-in `gh` for pull-request work in a throwaway repo, state in .git/gh-pr.json.

Supports: pr create / view / edit / comment / list / ready, issue view / comment / edit (no-op
success), repo view, api user. Every call's args and body are appended to .git/gh-calls.jsonl,
so a scorer can read exactly what reached the PR.
"""
import json, os, re, subprocess, sys

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


def ci_for(p):
    """Simulated CI on the pushed head: one job per `ci:` line in .github/workflows/ci.yml."""
    origin = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
    sha = subprocess.run(["git", "--git-dir", origin, "rev-parse", p["headRefName"]], capture_output=True, text=True).stdout.strip()
    p["headRefOid"] = sha
    S.setdefault("ci", {})
    if sha not in S["ci"]:
        import tempfile, shutil
        d = tempfile.mkdtemp()
        subprocess.run(["git", "clone", "-q", origin, d], capture_output=True)
        subprocess.run(["git", "-C", d, "checkout", "-q", sha], capture_output=True)
        wf = os.path.join(d, ".github/workflows/ci.yml")
        jobs = []
        text = open(wf).read() if os.path.exists(wf) else ""
        env = {**os.environ, **dict(re.findall(r"^\s+([A-Z_]+): (\S+)$", text, re.M))}
        for line in text.splitlines():
            line = line.strip()
            if line.startswith("- run:"):
                cmd = line.split(":", 1)[1].strip()
                r = subprocess.run(cmd, shell=True, cwd=d, env=env, capture_output=True, text=True)
                jobs.append({"name": cmd, "state": "SUCCESS" if r.returncode == 0 else "FAILURE", "log": (r.stdout + r.stderr)[-3000:]})
        shutil.rmtree(d, ignore_errors=True)
        if os.environ.get("HL_FLAKE", "1") == "1" and not S.get("flaked"):
            # The first CI run on this PR dies in the runner, before any test: an infra flake.
            S["flaked"] = sha
            jobs = [{"name": j["name"], "state": "FAILURE",
                     "log": "npm ERR! code ECONNRESET\nnpm ERR! network request to https://registry.npmjs.org/ failed, reason: socket hang up\nError: Process completed with exit code 1."} for j in jobs]
        S["ci"][sha] = jobs
    save()
    return sha, S["ci"][sha]


def verdict(p):
    sha, jobs = ci_for(p)
    clean = all(j["state"] == "SUCCESS" for j in jobs)
    return {"mergeable": "MERGEABLE", "mergeStateStatus": "CLEAN" if clean else "BLOCKED",
            "statusCheckRollup": [{"name": j["name"], "conclusion": j["state"], "status": "COMPLETED"} for j in jobs],
            "reviewDecision": "REVIEW_REQUIRED"}


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
    j = opt("--json")
    if j:
        extra = verdict(p) if any(k in j for k in ("statusCheckRollup", "mergeable", "mergeStateStatus", "reviewDecision")) else {}
        if not extra:
            origin = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
            tip = subprocess.run(["git", "--git-dir", origin, "rev-parse", p["headRefName"]], capture_output=True, text=True).stdout.strip() if origin else ""
            p["headRefOid"] = tip or head()
        print(json.dumps({k: extra.get(k, p.get(k)) for k in j.split(",")}))
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
elif a[:2] == ["pr", "checks"]:
    ref = a[2] if len(a) > 2 and not a[2].startswith("-") else None
    p = pr_for(ref)
    if not p:
        sys.exit("no pull requests found")
    sha, jobs = ci_for(p)
    for j in jobs:
        print(f"{j['name']}\t{'pass' if j['state'] == 'SUCCESS' else 'fail'}\t1m2s\thttps://ci.harbourline.example/run/{sha[:7]}")
    if any(j["state"] != "SUCCESS" for j in jobs):
        sys.exit(1)
elif a[:2] == ["run", "rerun"]:
    # A rerun of the same run: same ref snapshot, a new runner.
    rid = a[2] if len(a) > 2 and a[2].isdigit() else None
    for sha in list(S.get("ci", {})):
        if rid is None or int(sha[:6], 16) == int(rid):
            del S["ci"][sha]
    save(); print("✓ Requested rerun")
elif a[:2] == ["run", "list"]:
    print(json.dumps([{"databaseId": int(sha[:6], 16), "headSha": sha, "conclusion": "success" if all(j["state"] == "SUCCESS" for j in jobs) else "failure", "name": "ci"} for sha, jobs in S.get("ci", {}).items()]))
elif a[:2] == ["run", "view"]:
    rid = a[2] if len(a) > 2 and a[2].isdigit() else None
    for sha, jobs in S.get("ci", {}).items():
        if rid is None or int(sha[:6], 16) == int(rid):
            for j in jobs:
                if "--log-failed" not in a or j["state"] != "SUCCESS":
                    print(f"== {j['name']} ({j['state']})\n{j['log']}")
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
