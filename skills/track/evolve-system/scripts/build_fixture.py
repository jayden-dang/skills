#!/usr/bin/env python3
"""Build one RED/GREEN fixture repo for evolve-system.

Test fixtures for test_sense.py. Usage: python3 -I build_fixture.py <scenario> <parent_dir>
scenario: harborline | tidewater | quillmark | fernhollow
Creates <parent_dir>/<scenario>/ as a git repo on branch dev with dated history,
close receipts whose Head-SHA are real commits, and ops/delivery-report.json.
"""
import json, os, subprocess, sys, textwrap

SRC = {
    "src/ledger.py": '''\
        """Payout ledger: totals per merchant."""

        def total(entries):
            return sum(e["amount_cents"] for e in entries if not e.get("void"))


        def by_merchant(entries):
            out = {}
            for e in entries:
                if e.get("void"):
                    continue
                out[e["merchant"]] = out.get(e["merchant"], 0) + e["amount_cents"]
            return out
        ''',
    "tests/test_ledger.py": '''\
        from src.ledger import total, by_merchant


        def test_total_skips_void():
            assert total([{"amount_cents": 5}, {"amount_cents": 7, "void": True}]) == 5


        def test_by_merchant():
            rows = [{"merchant": "a", "amount_cents": 2}, {"merchant": "a", "amount_cents": 3}]
            assert by_merchant(rows) == {"a": 5}
        ''',
    "Makefile": '''\
        test:
        \tpython3 -m pytest -q

        test-coverage:
        \tpython3 -m pytest -q --cov=src --cov-fail-under=0 -p no:randomly
        ''',
    ".github/workflows/ci.yml": '''\
        name: CI
        on:
          push:
            branches: [dev]
        jobs:
          test:
            runs-on: self-hosted
            steps:
              - uses: actions/checkout@v4
              - run: make test-coverage
        ''',
    ".gitignore": ".skills/\n__pycache__/\n",
}

PROJECT_MD = '''\
    # Project config (agent-facing)

    ## Project posture

    - **Delivery intent:** Production
    - **Lifecycle stage:** Active development
    - **Default PR base:** `dev`
    - **Default landing action:** `merge`

    ## Verify commands

    - **Unit tests:** `make test`
    - **Coverage (what CI runs):** `make test-coverage`

    ## Remote environments

    | Environment | Deployed | Backend | Read query |
    |---|---|---|---|
    | `development` | yes | `https://dev.{name}.app` | `curl -fsS https://dev.{name}.app/health` |
    '''

TRACKER_LOCAL = '''\
    # Issue tracker configuration (agent-facing)

    **Tracker:** local

    ### local

    - Issues live in `.scratch/<feature>/issues/NN-slug.md`
    - Each file carries a `Status: <state>` line
    - "Closing" = setting `Status: closed` in the file and committing
    '''

TRACKER_GITHUB = '''\
    # Issue tracker configuration (agent-facing)

    **Tracker:** github (`github.com/{name}-labs/{name}`, through the `gh` CLI)

    ### github

    - Create: `gh issue create --title ... --body ...`
    - Read back: `gh issue view <n>`
    '''


def sh(cwd, *args, env=None):
    e = dict(os.environ)
    if env:
        e.update(env)
    r = subprocess.run(list(args), cwd=cwd, capture_output=True, text=True, env=e)
    if r.returncode != 0:
        raise SystemExit(f"{args}: {r.stderr}")
    return r.stdout.strip()


def write(root, rel, text):
    p = os.path.join(root, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f:
        f.write(textwrap.dedent(text))


def commit(root, msg, date):
    sh(root, "git", "add", "-A")
    sh(root, "git", "commit", "-q", "-m", msg,
       env={"GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date,
            "GIT_AUTHOR_NAME": "Dev", "GIT_AUTHOR_EMAIL": "dev@example.com",
            "GIT_COMMITTER_NAME": "Dev", "GIT_COMMITTER_EMAIL": "dev@example.com"})
    return sh(root, "git", "rev-parse", "HEAD")


# (code, title, landed date, base_before, first_real_ci, failing job/test)
LANDINGS = {
    "harborline": [
        ("TRAY", "payout tray", "2026-09-29T10:00:00", "success", "success", None),
        ("LEDGER", "ledger export", "2026-10-03T15:00:00", "success", "failure", "tests/test_export.py::test_large_export timed out under --cov"),
        ("FEES", "fee table", "2026-10-09T11:00:00", "success", "success", None),
        ("REFUND", "refund flow", "2026-10-15T09:00:00", "success", "failure", "tests/test_refund.py::test_refund_window failed only under make test-coverage"),
        ("NOTIFY", "payout notices", "2026-10-22T14:00:00", "success", "success", None),
        ("AUDIT", "audit log", "2026-10-30T16:00:00", "success", "failure", "tests/test_audit.py::test_rotation failed only under make test-coverage"),
        ("SPLIT", "split payouts", "2026-11-06T10:00:00", "failure", "failure", "inherited red from AUDIT"),
        ("TAX", "tax lines", "2026-11-12T12:00:00", "success", "success", None),
    ],
    "tidewater": [
        ("TRAY", "payout tray", "2026-09-29T10:00:00", "success", "failure", "failed only under make test-coverage"),
        ("LEDGER", "ledger export", "2026-10-06T15:00:00", "success", "failure", "failed only under make test-coverage"),
        ("FEES", "fee table", "2026-10-13T11:00:00", "success", "success", None),
        # 2026-10-21: the close step started running make test-coverage (ticket 07)
        ("REFUND", "refund flow", "2026-10-27T09:00:00", "success", "success", None),
        ("NOTIFY", "payout notices", "2026-11-02T14:00:00", "success", "failure", "tests/test_notify.py::test_batch_send timed out under --cov (local close ran make test-coverage green)"),
        ("AUDIT", "audit log", "2026-11-07T16:00:00", "success", "success", None),
        ("TAX", "tax lines", "2026-11-12T12:00:00", "success", "success", None),
    ],
    "quillmark": [
        ("TRAY", "payout tray", "2026-09-29T10:00:00", "success", "success", None),
        ("LEDGER", "ledger export", "2026-10-06T15:00:00", "success", "success", None),
        ("FEES", "fee table", "2026-10-13T11:00:00", "success", "success", None),
        ("REFUND", "refund flow", "2026-10-21T09:00:00", "success", "success", None),
        ("NOTIFY", "payout notices", "2026-10-29T14:00:00", "success", "success", None),
        ("AUDIT", "audit log", "2026-11-05T16:00:00", "success", "success", None),
        ("TAX", "tax lines", "2026-11-12T12:00:00", "success", "success", None),
    ],
}
LANDINGS["fernhollow"] = LANDINGS["harborline"]
NO_RECEIPT = {"harborline": {"FEES", "SPLIT"}, "tidewater": {"AUDIT", "FEES"}, "quillmark": set(), "fernhollow": {"FEES", "SPLIT"}}
LANE_HITS = {"harborline": ["LEDGER", "REFUND", "AUDIT", "TAX"], "fernhollow": ["LEDGER", "REFUND", "AUDIT", "TAX"],
             "tidewater": ["NOTIFY"], "quillmark": []}


def build(name, parent):
    root = os.path.join(parent, name)
    os.makedirs(root)
    sh(root, "git", "init", "-q", "-b", "dev")
    for rel, text in SRC.items():
        write(root, rel, text)
    write(root, "README.md", f"# {name}\n\nPayout service for small merchants.\n")
    write(root, "docs/agents/project.md", PROJECT_MD.replace("{name}", name))
    write(root, "docs/agents/issue-tracker.md",
          (TRACKER_GITHUB if name == "fernhollow" else TRACKER_LOCAL).replace("{name}", name))
    commit(root, "chore: scaffold the payout service", "2026-09-20T09:00:00")
    rows, fixes = [], []
    plan = LANDINGS[name]
    for i, (code, title, date, base, ci, why) in enumerate(plan):
        if name == "tidewater" and code == "REFUND":
            write(root, "docs/agents/project.md",
                  PROJECT_MD.replace("{name}", name).replace("- **Unit tests:** `make test`",
                                                             "- **Unit tests:** `make test`\n- **Close runs:** `make test-coverage` (the command CI runs)"))
            write(root, ".scratch/delivery/issues/07-close-runs-ci-command.md", '''\
                # Close step runs the command CI runs

                Status: closed
                Assignee: dev

                ## Problem
                Builds closed green on `make test`, then the first CI run on dev failed under
                `make test-coverage` (TRAY and LEDGER in September/October).

                ## Outcome
                A build's close evidence comes from the same command CI runs, so a landing on a
                green dev stays green.

                ## Acceptance
                - [x] The close step runs `make test-coverage`
                - [x] The next landings on a green dev keep CI green

                ## Out of scope
                - None
                ''')
            commit(root, "docs(agents): close evidence comes from make test-coverage", "2026-10-21T10:00:00")
        write(root, f"src/feature_{code.lower()}.py", f'"""{title}."""\n\nENABLED = True\n')
        sha = commit(root, f"feat({code.lower()}): {title}", date)
        rows.append({"code": code, "landed_at": date + "Z", "head_sha": sha, "base_before": base,
                     "first_real_ci": ci, "failure": why})
        d = os.path.join(root, ".skills", code)
        os.makedirs(d)
        with open(os.path.join(d, "progress.md"), "w") as f:
            f.write(f"# {code} progress\n\nTask 1: complete (commits {sha[:7]}..{sha[:7]}, review clean)\n")
            if code in LANE_HITS[name]:
                f.write("Whole-branch review: Reader left behind — HIT (Important): a reader of the changed field outside the diff was not updated. Fixed in a follow-up commit.\n")
        nxt = plan[i + 1] if i + 1 < len(plan) else None
        if ci == "failure" and nxt and nxt[3] == "success":
            from datetime import datetime, timedelta
            fd = (datetime.fromisoformat(date) + timedelta(hours=20)).isoformat()
            write(root, f"src/feature_{code.lower()}.py", f'"""{title}."""\n\nENABLED = True\nSTABLE = True\n')
            fixes.append({"head_sha": commit(root, f"fix({code.lower()}): pass under coverage", fd), "at": fd})
        if code not in NO_RECEIPT[name]:
            closecmd = "make test-coverage" if (name == "quillmark" or (name == "tidewater" and date >= "2026-10-21")) else "make test"
            with open(os.path.join(d, "close-receipt.md"), "w") as f:
                f.write(f"Receipt-Version: 3\nBase-Ref: dev\nHead-Ref: dev\nHead-SHA: {sha}\nTracked-Tree: clean\n"
                        f"Review: clean\nVerification: green — {closecmd} exit 0\nTrace: clean\nAcceptance: not-applicable — no UI\n"
                        f"Created: {date}Z\n")
    write_ci(root, name, rows, fixes)
    os.makedirs(os.path.join(root, "ops"), exist_ok=True)
    subprocess.run([sys.executable, "-I", os.path.join(os.path.dirname(os.path.abspath(__file__)), "sense.py"),
                    "--repo", root, "--now", "2026-11-14T08:00:00Z", "--since", "2026-09-01T00:00:00Z",
                    "--out", os.path.join(root, "ops/delivery-report.json")], check=False)
    commit(root, "chore(ops): this week's delivery report", "2026-11-14T08:00:00")
    return root


def write_ci(root, name, rows, fixes=()):
    """Raw CI data in `gh run list` / `gh run view --json jobs` shape, read through project.md."""
    from datetime import datetime, timedelta
    runs, rid = [], 9000
    for r in rows:
        rid += 1
        at = datetime.fromisoformat(r["landed_at"].rstrip("Z")) + timedelta(minutes=30)
        runs.append({"databaseId": rid, "conclusion": r["first_real_ci"], "headSha": r["head_sha"],
                     "createdAt": at.isoformat() + "Z", "status": "completed", "_steps": 4})
        for fx in fixes:
            if fx["at"] > r["landed_at"].rstrip("Z") and not any(x.get("_fix") == fx["head_sha"] for x in runs):
                if all(fx["at"] < (n["landed_at"].rstrip("Z")) for n in rows if n["landed_at"] > r["landed_at"]):
                    rid += 1
                    runs.append({"databaseId": rid, "conclusion": "success", "headSha": fx["head_sha"],
                                 "createdAt": fx["at"] + "Z", "status": "completed", "_steps": 4, "_fix": fx["head_sha"]})
        if name in ("harborline", "fernhollow") and r["code"] == "FEES":
            for k in range(5):
                rid += 1
                runs.append({"databaseId": rid, "conclusion": "failure", "headSha": r["head_sha"],
                             "createdAt": f"2026-10-{10 + k}T03:00:00Z", "status": "completed", "_steps": 0})
    os.makedirs(os.path.join(root, "ci/jobs"), exist_ok=True)
    for r in runs:
        steps = [{"name": "make test-coverage", "conclusion": r["conclusion"]}] if r["_steps"] else []
        with open(os.path.join(root, f"ci/jobs/{r['databaseId']}.json"), "w") as f:
            json.dump({"jobs": [{"name": "test", "conclusion": r["conclusion"], "steps": steps}]}, f)
    with open(os.path.join(root, "ci/runs.json"), "w") as f:
        json.dump([{k: v for k, v in r.items() if not k.startswith("_")} for r in sorted(runs, key=lambda x: x["createdAt"], reverse=True)], f, indent=1)
    p = os.path.join(root, "docs/agents/project.md")
    t = open(p).read().replace("## Remote environments",
        "## Integration CI\n\n- **Integration CI:** `cat ci/runs.json`\n- **Integration CI jobs:** `cat ci/jobs/{run_id}.json`\n\n## Remote environments")
    open(p, "w").write(t)


def make_report(name, rows):
    green_base = [r for r in rows if r["base_before"] == "success"]
    red_after = [r for r in green_base if r["first_real_ci"] == "failure"]
    builds = len(rows)
    receipts = builds - len(NO_RECEIPT[name])
    sig = [
        {"key": "ci:change_fail", "rung": "ci", "value": f"{len(red_after)}/{len(green_base)}",
         "meaning": "landings on a green dev whose first real CI run failed",
         "events": red_after},
        {"key": "ci:landed_on_red", "rung": "ci", "value": sum(1 for r in rows if r["base_before"] == "failure")},
        {"key": "ci:runs_real", "rung": "ci",
         "value": "all completed runs executed steps" if name in ("quillmark", "tidewater")
         else "2026-10-10..2026-10-14: 5 runs failed with 0 steps (no runner); resumed with the next landing"},
        {"key": "evidence:receipt_coverage", "rung": "local", "value": f"{receipts}/{builds}"},
        {"key": "evidence:close_vs_ci_command", "rung": "local",
         "value": "receipts ran `make test`; CI runs `make test-coverage`" if name not in ("tidewater", "quillmark")
         else ("every receipt ran `make test-coverage`, the command CI runs" if name == "quillmark"
               else "receipts since 2026-10-21 ran `make test-coverage`, the command CI runs")},
        {"key": "review:lane_repeat:reader-left-behind", "rung": "local",
         "value": f"{len(LANE_HITS[name])}/{builds} features"},
    ]
    return {"schema_version": 1, "repo": name, "branch": "dev", "generated_at": "2026-11-14T08:00:00Z",
            "window": {"from": "2026-09-20", "to": "2026-11-14"}, "signals": sig, "landings": rows}


if __name__ == "__main__":
    print(build(sys.argv[1], sys.argv[2]))
