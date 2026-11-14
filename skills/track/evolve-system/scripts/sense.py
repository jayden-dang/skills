#!/usr/bin/env python3
"""Delivery-loop sensor: read what the skill set already writes, print fixed signals.

Read-only on the repo except .skills/evolve/ (with --write). Standard library only, so any
runner (a person, a bot, a scheduler) can call it without an LLM or an MCP server.

Inputs
  .skills/<CODE>/progress.md, close-receipt.md   (deduplicated by realpath)
  git history of the repo
  docs/agents/project.md (or --ci-cmd / --jobs-cmd):
    **Integration CI:** `<command>`        JSON runs: [{databaseId, conclusion, headSha, createdAt}]
    **Integration CI jobs:** `<command>`   optional; `{run_id}` replaced; {"jobs":[{conclusion, steps}]}
  .skills/evolve/cycles.json               optional; cycles opened by earlier runs

Signals cover the window [--since, --now] (default: the 45 days before now). A flagged signal
whose key an open or awaiting cycle already tracks is reported but does not count as new.

Exit 0 = nothing new flagged, 10 = a new signal is flagged, 20 = a cycle settled as reverted,
2 = the sensor itself could not run.

Usage: python3 -I sense.py --repo PATH [--out FILE] [--write] [--now ISO] [--since ISO]
                           [--ci-cmd CMD] [--jobs-cmd CMD]
"""
import argparse, glob, json, os, re, subprocess, sys
from datetime import datetime, timedelta, timezone

LANES = {"reader-left-behind": re.compile(r"reader left behind\W+\**\s*hit", re.I),
         "silent-degradation": re.compile(r"silent degradation\W+\**\s*hit", re.I)}
# signal key -> (observations that settle a prediction, days before it is inconclusive)
SETTLE = {"ci:change_fail": (3, 30), "ci:landed_on_red": (3, 30), "ci:runs_real": (1, 7),
          "evidence:receipt_coverage": (3, 30), "evidence:close_vs_ci_command": (1, 30),
          "review:lane_repeat:reader-left-behind": (3, 45), "review:lane_repeat:silent-degradation": (3, 45)}
RANGE = re.compile(r"commits?\s+`?([0-9a-f]{7,40})`?\s*\.\.\s*`?([0-9a-f]{7,40})`?")


def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, shell=isinstance(cmd, str), capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def git(repo, *args):
    code, out, _ = run(["git", "-C", repo, *args], repo)
    return out.strip() if code == 0 else ""


def ts(s):
    d = datetime.fromisoformat(s.strip().replace("Z", "+00:00"))
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def config(repo, a):
    p = os.path.join(repo, "docs/agents/project.md")
    text = open(p, errors="replace").read() if os.path.exists(p) else ""
    def key(name):
        m = re.search(r"\*\*" + re.escape(name) + r":\*\*\s*`([^`]+)`", text)
        return m.group(1) if m else None
    base = re.search(r"\*\*Default PR base:\*\*\s*`?([\w./-]+)", text)
    return {"ci": a.ci_cmd or key("Integration CI"), "jobs": a.jobs_cmd or key("Integration CI jobs"),
            "branch": base.group(1) if base else "HEAD"}


def features(repo):
    seen, out = set(), []
    for prog in sorted(glob.glob(os.path.join(repo, ".skills/*/progress.md"))):
        d = os.path.dirname(prog)
        real = os.path.realpath(d)
        if real in seen or os.path.basename(d).startswith(("evolve", "_")):
            continue
        seen.add(real)
        out.append(d)
    return out


def landing_head(repo, d):
    """Receipt Head-SHA, else the last commit range in the ledger. (head, verification)."""
    p = os.path.join(d, "close-receipt.md")
    if os.path.exists(p):
        t = open(p, errors="replace").read()
        h = re.search(r"^Head-SHA:\s*([0-9a-f]{7,40})", t, re.M)
        v = re.search(r"^Verification:\s*(.*)$", t, re.M)
        if h:
            return h.group(1), (v.group(1).strip() if v else "")
    ranges = RANGE.findall(open(os.path.join(d, "progress.md"), errors="replace").read())
    head = git(repo, "rev-parse", "--verify", "--quiet", ranges[-1][1] + "^{commit}") if ranges else ""
    return (head or None), ""


def ci_runs(repo, cfg, now):
    if not cfg["ci"]:
        return None, "no `**Integration CI:**` command in docs/agents/project.md and no --ci-cmd"
    code, out, err = run(cfg["ci"], repo)
    if code != 0:
        return None, f"Integration CI command failed: {err.strip()[:160]}"
    runs = [r for r in json.loads(out or "[]")
            if r.get("conclusion") in ("success", "failure") and ts(r["createdAt"]) <= now]
    runs.sort(key=lambda r: r["createdAt"])
    for r in runs:
        r["_repo"], r["_jobs"] = repo, cfg["jobs"]
    return runs, None


def real(r):
    """success | failure | infra (every failed job ran 0 steps). Asked lazily, cached on the run."""
    if "real" not in r:
        r["real"] = r["conclusion"]
        if r["conclusion"] == "failure" and r.get("_jobs"):
            c2, o2, _ = run(r["_jobs"].replace("{run_id}", str(r["databaseId"])), r["_repo"])
            if c2 == 0 and o2.strip():
                failed = [j for j in json.loads(o2).get("jobs", []) if j.get("conclusion") == "failure"]
                if failed and all(not j.get("steps") for j in failed):
                    r["real"] = "infra"
    return r["real"]


def contains(repo, sha, head):
    return run(["git", "-C", repo, "merge-base", "--is-ancestor", sha, head], repo)[0] == 0


def landings(repo, feats, runs, now):
    shas = "\n".join(r["headSha"] for r in (runs or []))
    present = set()
    if shas:
        p = subprocess.run(["git", "-C", repo, "cat-file", "--batch-check"], input=shas + "\n",
                           capture_output=True, text=True)
        present = {l.split()[0] for l in p.stdout.splitlines() if l.endswith(tuple("0123456789")) and " commit " in l}
    known = [r for r in (runs or []) if r["headSha"] in present]
    rows = []
    for d in feats:
        head, ver = landing_head(repo, d)
        if not head:
            continue
        landed = git(repo, "show", "-s", "--format=%cI", head)
        if not landed or ts(landed) > now:
            continue
        row = {"code": os.path.basename(d), "head_sha": head, "landed_at": landed, "receipt": bool(ver),
               "verification": ver, "base_before": "unknown", "first_real_ci": "no-real-run"}
        at = ts(landed) - timedelta(hours=1)  # a run created before the landing cannot contain it
        for i, r in enumerate(known):
            if ts(r["createdAt"]) < at or not contains(repo, head, r["headSha"]) or real(r) == "infra":
                continue
            row["first_real_ci"], row["ci_run"] = real(r), r["databaseId"]
            for prev in reversed(known[:i]):
                if not contains(repo, head, prev["headSha"]) and real(prev) != "infra":
                    row["base_before"] = real(prev)
                    break
            break
        rows.append(row)
    rows.sort(key=lambda r: r["landed_at"])
    return rows


def ci_test_commands(repo):
    cmds = []
    for wf in glob.glob(os.path.join(repo, ".github/workflows/*.y*ml")):
        for m in re.findall(r"^\s*-?\s*run:\s*(.+)$", open(wf, errors="replace").read(), re.M):
            if re.search(r"\btest", m):
                cmds.append(m.strip())
    return cmds


def signals(repo, feats, rows, runs, err, since):
    win = [r for r in rows if ts(r["landed_at"]) >= since]
    out = []
    if runs is None:
        out.append({"key": "ci:configured", "rung": "ci", "value": "no", "flag": True, "detail": err})
    else:
        green = [r for r in win if r["base_before"] == "success"]
        red = [r for r in green if r["first_real_ci"] == "failure"]
        on_red = [r for r in win if r["base_before"] == "failure"]
        out.append({"key": "ci:change_fail", "rung": "ci", "value": f"{len(red)}/{len(green)}", "flag": bool(red),
                    "events": [{k: r.get(k) for k in ("code", "head_sha", "landed_at", "ci_run")} for r in red]})
        out.append({"key": "ci:landed_on_red", "rung": "ci", "value": f"{len(on_red)}/{len(win)}",
                    "flag": bool(on_red), "events": [r["code"] for r in on_red]})
        recent = [r for r in runs if ts(r["createdAt"]) >= since]
        infra = [r for r in recent if real(r) == "infra"]
        out.append({"key": "ci:runs_real", "rung": "ci", "value": f"{len(infra)} of {len(recent)} runs ran 0 steps",
                    "flag": bool(runs) and real(runs[-1]) == "infra",
                    "infra_window": [infra[0]["createdAt"], infra[-1]["createdAt"]] if infra else None,
                    "latest": real(runs[-1]) if runs else None})
    if win:
        missing = [r["code"] for r in win if not r["receipt"]]
        out.append({"key": "evidence:receipt_coverage", "rung": "local",
                    "value": f"{len(win) - len(missing)}/{len(win)}", "flag": bool(missing), "missing": missing})
    ci_cmds = ci_test_commands(repo)
    with_v = [r for r in win if r["verification"]]
    if ci_cmds and with_v:
        latest = with_v[-1]
        lacking = [c for c in ci_cmds if c not in latest["verification"]]
        out.append({"key": "evidence:close_vs_ci_command", "rung": "local", "flag": bool(lacking),
                    "value": "match" if not lacking else "differs", "ci_test_commands": ci_cmds,
                    "latest_receipt": {"code": latest["code"], "verification": latest["verification"]}})
    codes = {r["code"] for r in win}
    for lane, rx in LANES.items():
        hit = [os.path.basename(d) for d in feats if os.path.basename(d) in codes and
               rx.search("".join(open(f, errors="replace").read() for f in glob.glob(os.path.join(d, "*.md"))))]
        out.append({"key": f"review:lane_repeat:{lane}", "rung": "local", "value": f"{len(hit)}/{len(codes)}",
                    "flag": len(hit) >= 2, "features": hit})
    return out


def advance(repo, cfg, cycles, now):
    """open -> awaiting once a commit on the integration branch names the cycle's ticket."""
    for c in cycles:
        if c.get("state") != "open" or not c.get("ticket"):
            continue
        if c["ticket"].startswith("draft:"):
            continue  # not filed yet: nothing can name it
        log = git(repo, "log", cfg["branch"], f"--since={c['opened_at']}", "--format=%H%x09%cI%x09%s%x09%b%x00")
        hits = []
        for entry in log.split("\x00"):
            parts = entry.strip().split("\t")
            if len(parts) >= 3 and re.search(r"(?<![\w#/-])" + re.escape(c["ticket"]) + r"(?![\w-])", "\t".join(parts[2:])):
                hits.append((parts[1], parts[0]))
        if os.path.exists(os.path.join(repo, c["ticket"])):  # local tracker: a commit that edits the ticket
            for line in git(repo, "log", cfg["branch"], f"--since={c['opened_at']}", "--format=%H%x09%cI",
                            "--", c["ticket"]).splitlines():
                h, d = line.split("\t")
                hits.append((d, h))
        hits = sorted(x for x in hits if ts(x[0]) <= now)
        if hits:
            c.update(state="awaiting", changed_at=hits[0][0], change_commit=hits[0][1])
    return cycles


OPEN_DAYS = 30  # an improvement nobody delivered within this many days frees the slot


def settle(cycles, rows, sigs, now):
    before = [c.get("state") for c in cycles]
    _settle(cycles, rows, sigs, now)
    for c, b in zip(cycles, before):
        if c.get("state") != b and c.get("state") in ("kept", "reverted", "inconclusive", "expired"):
            c["settled_at"] = now.isoformat()
            c["_now"] = True
    return cycles


def _settle(cycles, rows, sigs, now):
    by_key = {s["key"]: s for s in sigs}
    for c in cycles:
        if c.get("state") == "open" and c.get("opened_at"):
            age = (now - ts(c["opened_at"])).days
            c["age_days"] = age
            if age > OPEN_DAYS:
                c["state"], c["why"] = "expired", f"no commit delivered its ticket within {OPEN_DAYS} days"
            continue
        if c.get("state") != "awaiting":
            continue
        need, days = SETTLE.get(c["key"], (1, 30))
        since = ts(c["changed_at"])
        if c["key"] in ("ci:change_fail", "ci:landed_on_red"):
            want = "success" if c["key"] == "ci:change_fail" else None
            obs = [r for r in rows if ts(r["landed_at"]) > since and (want is None or r["base_before"] == want)]
            bad = [r["code"] for r in obs if (r["first_real_ci"] == "failure" if want else r["base_before"] == "failure")]
            c["observed"] = f"{len(obs)}/{need}"
            if bad:
                c["state"], c["why"] = "reverted", f"after the change, {', '.join(bad)} still showed {c['key']}"
            elif len(obs) >= need:
                c["state"], c["why"] = "kept", f"{len(obs)} landings since the change, none showed {c['key']}"
        elif c["key"].startswith("review:lane_repeat:"):
            hits = set(by_key.get(c["key"], {}).get("features", []))
            obs = [r for r in rows if ts(r["landed_at"]) > since]
            bad = [r["code"] for r in obs if r["code"] in hits]
            c["observed"] = f"{len(obs)}/{need}"
            if bad:
                c["state"], c["why"] = "reverted", f"after the change, {', '.join(bad)} still had the {c['key'].split(':')[-1]} finding"
            elif len(obs) >= need:
                c["state"], c["why"] = "kept", f"{len(obs)} landings since the change, none with the finding"
        elif c["key"] == "evidence:receipt_coverage":
            obs = [r for r in rows if ts(r["landed_at"]) > since]
            bad = [r["code"] for r in obs if not r["receipt"]]
            c["observed"] = f"{len(obs)}/{need}"
            if bad:
                c["state"], c["why"] = "reverted", f"after the change, {', '.join(bad)} landed with no receipt"
            elif len(obs) >= need:
                c["state"], c["why"] = "kept", f"{len(obs)} landings since the change, all with a receipt"
        else:
            s = by_key.get(c["key"])
            if s is not None and s.get("flag") is False:
                c["state"], c["why"] = "kept", f"{c['key']} no longer flagged ({s['value']})"
        if c["state"] == "awaiting" and now - since > timedelta(days=days):
            c["state"], c["why"] = "inconclusive", f"not enough observations within {days} days"
    return cycles


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--out")
    ap.add_argument("--write", action="store_true", help="save advanced/settled cycles to cycles.json")
    ap.add_argument("--now")
    ap.add_argument("--since")
    ap.add_argument("--ci-cmd")
    ap.add_argument("--jobs-cmd")
    a = ap.parse_args()
    repo = os.path.abspath(a.repo)
    if not git(repo, "rev-parse", "--git-dir"):
        print(f"not a git repo: {repo}", file=sys.stderr)
        return 2
    now = ts(a.now) if a.now else datetime.now(timezone.utc)
    since = ts(a.since) if a.since else now - timedelta(days=45)
    cfg = config(repo, a)
    feats = features(repo)
    runs, err = ci_runs(repo, cfg, now)
    rows = landings(repo, feats, runs, now)
    sigs = signals(repo, feats, rows, runs, err, since)
    cpath = os.path.join(repo, ".skills/evolve/cycles.json")
    doc = json.load(open(cpath)) if os.path.exists(cpath) else {"schema_version": 1, "cycles": []}
    if isinstance(doc, list):  # a hand-written bare list: keep its cycles, restore the shape
        doc = {"schema_version": 1, "cycles": doc}
    cycles = settle(advance(repo, cfg, doc["cycles"], now), rows, sigs, now)
    for s in sigs:
        need, days = SETTLE.get(s["key"], (1, 30))
        s["settle"] = {"observations": need, "days": days}
    tracked = {c["key"] for c in cycles if c.get("state") in ("open", "awaiting")}
    for s in sigs:
        if s.get("flag") and s["key"] in tracked:
            s["tracked"] = True
    report = {"schema_version": 1, "repo": os.path.basename(repo), "generated_at": now.isoformat(),
              "window": [since.isoformat(), now.isoformat()], "signals": sigs, "landings": rows, "cycles": cycles,
              "flagged": [s["key"] for s in sigs if s.get("flag") and not s.get("tracked")],
              "tracked": sorted(tracked)}
    settled_now = [c for c in cycles if c.pop("_now", False)]
    report["settled_now"] = [{k: c.get(k) for k in ("key", "state", "why", "ticket")} for c in settled_now]
    reverted = [c["key"] for c in settled_now if c["state"] == "reverted" and c["key"] in report["flagged"]]
    # what makes CI meaningless first, then what CI caught after landing, then evidence, then review
    rank = ["ci:configured", "ci:runs_real", "ci:change_fail", "ci:landed_on_red",
            "evidence:close_vs_ci_command", "evidence:receipt_coverage"]
    weight = lambda s: len(s.get("events") or s.get("features") or s.get("missing") or [])
    order = [s["key"] for s in sorted((s for s in sigs if s["key"] in report["flagged"]),
                                      key=lambda s: (rank.index(s["key"]) if s["key"] in rank else len(rank), -weight(s)))]
    report["pick_order"] = list(dict.fromkeys(reverted + order))
    text = json.dumps(report, indent=2) + "\n"
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        open(a.out, "w").write(text)
    else:
        sys.stdout.write(text)
    if a.write:
        doc["cycles"] = cycles
        os.makedirs(os.path.dirname(cpath), exist_ok=True)
        open(cpath, "w").write(json.dumps(doc, indent=2) + "\n")
    if any(c["state"] == "reverted" for c in report["settled_now"]):
        return 20
    return 10 if report["flagged"] else 0


if __name__ == "__main__":
    sys.exit(main())
