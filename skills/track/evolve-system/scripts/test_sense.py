import json, os, subprocess, sys, tempfile, unittest
HERE = os.path.dirname(os.path.abspath(__file__))
NOW = "2026-11-14T08:00:00Z"
ALL = "2026-09-01T00:00:00Z"


def fixture(name):
    p = tempfile.mkdtemp(prefix="wk.")
    return subprocess.run([sys.executable, "-I", os.path.join(HERE, "build_fixture.py"), name, p],
                          capture_output=True, text=True, check=True).stdout.strip()


def sense(repo, *extra):
    r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "sense.py"), "--repo", repo, *extra],
                       capture_output=True, text=True)
    return r.returncode, (json.loads(r.stdout) if r.stdout.strip() else None)


def sig(rep, key):
    return next(s for s in rep["signals"] if s["key"] == key)


def cycles(repo, items):
    os.makedirs(os.path.join(repo, ".skills/evolve"), exist_ok=True)
    with open(os.path.join(repo, ".skills/evolve/cycles.json"), "w") as f:
        json.dump({"schema_version": 1, "cycles": items}, f)


def commit(repo, msg, date):
    with open(os.path.join(repo, "NOTES.md"), "a") as f:
        f.write(msg + "\n")
    env = dict(os.environ, GIT_AUTHOR_DATE=date, GIT_COMMITTER_DATE=date, GIT_AUTHOR_NAME="d",
               GIT_AUTHOR_EMAIL="d@x", GIT_COMMITTER_NAME="d", GIT_COMMITTER_EMAIL="d@x")
    subprocess.run(["git", "-C", repo, "add", "-A"], check=True)
    subprocess.run(["git", "-C", repo, "commit", "-qm", msg], check=True, env=env)


def land(repo, code, files, date, review=None):
    """A landed feature: one commit touching `files`, a ledger range, an optional review file."""
    base = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    for f in files:
        os.makedirs(os.path.join(repo, os.path.dirname(f)), exist_ok=True)
        open(os.path.join(repo, f), "a").write("x = 1\n")
    commit(repo, f"feat({code.lower()}): wide change", date)
    head = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    d = os.path.join(repo, ".skills", code)
    os.makedirs(d)
    open(os.path.join(d, "progress.md"), "w").write(f"Task 1: complete (commits {base[:9]}..{head[:9]}, review clean)\n")
    if review:
        open(os.path.join(d, "whole-branch-review.md"), "w").write(review)
    return head


class Sense(unittest.TestCase):
    def test_red_repo_flags_change_fail_and_skips_infra_runs(self):
        code, rep = sense(fixture("harborline"), "--now", NOW, "--since", ALL)
        self.assertEqual(code, 10)
        # 8 landings (receipt, else the ledger's last range); TRAY has no earlier run so its
        # base is unknown, SPLIT landed on AUDIT's red -> 6 on a green base, 3 red.
        self.assertEqual(sig(rep, "ci:change_fail")["value"], "3/6")
        self.assertEqual([e["code"] for e in sig(rep, "ci:change_fail")["events"]], ["LEDGER", "REFUND", "AUDIT"])
        self.assertEqual(sig(rep, "ci:landed_on_red")["events"], ["SPLIT"])
        self.assertIn("5 of", sig(rep, "ci:runs_real")["value"])
        self.assertFalse(sig(rep, "ci:runs_real")["flag"])  # the outage is over
        self.assertTrue(sig(rep, "evidence:close_vs_ci_command")["flag"])
        self.assertEqual(sig(rep, "evidence:receipt_coverage")["missing"], ["FEES", "SPLIT"])
        self.assertEqual(sig(rep, "evidence:receipt_coverage")["value"], "6/8 with a receipt")
        self.assertTrue(sig(rep, "review:lane_repeat:reader-left-behind")["flag"])

    def test_green_repo_is_a_no_op(self):
        code, rep = sense(fixture("quillmark"), "--now", NOW, "--since", ALL)
        self.assertEqual(rep["flagged"], [])
        self.assertEqual(code, 0)

    def test_old_reds_outside_the_window_do_not_flag(self):
        _, rep = sense(fixture("harborline"), "--now", NOW, "--since", "2026-11-08T00:00:00Z")
        self.assertFalse(sig(rep, "ci:change_fail")["flag"])
        self.assertFalse(sig(rep, "ci:landed_on_red")["flag"])

    def test_a_tracked_key_is_reported_but_not_new(self):
        repo = fixture("harborline")
        cycles(repo, [{"key": "ci:change_fail", "state": "open", "opened_at": "2026-11-13T00:00:00Z", "ticket": "#41"}])
        _, rep = sense(repo, "--now", NOW, "--since", ALL)
        self.assertNotIn("ci:change_fail", rep["flagged"])
        self.assertIn("ci:change_fail", rep["tracked"])

    def test_open_cycle_advances_when_a_commit_names_its_ticket(self):
        repo = fixture("quillmark")
        cycles(repo, [{"key": "evidence:receipt_coverage", "state": "open", "opened_at": "2026-11-14T09:00:00Z", "ticket": "#41"}])
        commit(repo, "docs(agents): close writes a receipt (Closes #41)", "2026-11-15T10:00:00")
        _, rep = sense(repo, "--now", "2026-11-16T00:00:00Z", "--since", ALL, "--write")
        c = rep["cycles"][0]
        self.assertEqual(c["state"], "awaiting")
        saved = json.load(open(os.path.join(repo, ".skills/evolve/cycles.json")))["cycles"][0]
        self.assertEqual(saved["state"], "awaiting")

    def test_a_bare_list_is_read_and_saved_back_in_shape(self):
        repo = fixture("harborline")
        os.makedirs(os.path.join(repo, ".skills/evolve"))
        json.dump([{"key": "ci:change_fail", "state": "open", "opened_at": "2026-11-14T09:00:00Z", "ticket": "#9"}],
                  open(os.path.join(repo, ".skills/evolve/cycles.json"), "w"))
        code, rep = sense(repo, "--now", NOW, "--since", ALL, "--write")
        self.assertIn("ci:change_fail", rep["tracked"])
        saved = json.load(open(os.path.join(repo, ".skills/evolve/cycles.json")))
        self.assertEqual(saved["schema_version"], 1)
        self.assertEqual(len(saved["cycles"]), 1)

    def test_write_creates_the_file_shape_when_none_exists(self):
        repo = fixture("harborline")
        sense(repo, "--now", NOW, "--since", ALL, "--write")
        saved = json.load(open(os.path.join(repo, ".skills/evolve/cycles.json")))
        self.assertEqual(saved, {"schema_version": 1, "cycles": []})

    def test_local_ticket_advances_on_a_commit_that_edits_it(self):
        repo = fixture("quillmark")
        tk = ".scratch/evolve/issues/01-x.md"
        os.makedirs(os.path.join(repo, os.path.dirname(tk)))
        open(os.path.join(repo, tk), "w").write("Status: needs-triage\n")
        cycles(repo, [{"key": "evidence:receipt_coverage", "state": "open", "opened_at": "2026-11-14T09:00:00Z", "ticket": tk}])
        open(os.path.join(repo, tk), "w").write("Status: closed\n")
        commit(repo, "docs(agents): close always writes a receipt", "2026-11-15T10:00:00")
        _, rep = sense(repo, "--now", "2026-11-16T00:00:00Z", "--since", ALL)
        self.assertEqual(rep["cycles"][0]["state"], "awaiting")

    def test_a_draft_ticket_never_advances(self):
        repo = fixture("quillmark")
        cycles(repo, [{"key": "evidence:receipt_coverage", "state": "open", "opened_at": "2026-11-14T09:00:00Z",
                       "ticket": "draft:.skills/evolve/drafts/x.md"}])
        commit(repo, "chore: mention draft:.skills/evolve/drafts/x.md", "2026-11-15T10:00:00")
        _, rep = sense(repo, "--now", "2026-11-16T00:00:00Z", "--since", ALL)
        self.assertEqual(rep["cycles"][0]["state"], "open")

    def test_ticket_match_respects_boundaries(self):
        repo = fixture("quillmark")
        cycles(repo, [{"key": "evidence:receipt_coverage", "state": "open", "opened_at": "2026-11-14T09:00:00Z", "ticket": "#4"}])
        commit(repo, "fix: something else (Closes #41)", "2026-11-15T10:00:00")
        _, rep = sense(repo, "--now", "2026-11-16T00:00:00Z", "--since", ALL)
        self.assertEqual(rep["cycles"][0]["state"], "open")
        commit(repo, "docs: close writes a receipt (Closes #4)", "2026-11-15T11:00:00")
        _, rep = sense(repo, "--now", "2026-11-16T00:00:00Z", "--since", ALL)
        self.assertEqual(rep["cycles"][0]["state"], "awaiting")

    def test_an_undelivered_open_cycle_expires_and_frees_the_slot(self):
        repo = fixture("harborline")
        cycles(repo, [{"key": "ci:change_fail", "state": "open", "opened_at": "2026-10-01T00:00:00Z",
                       "ticket": "draft:.skills/evolve/drafts/x.md"}])
        _, rep = sense(repo, "--now", NOW, "--since", ALL)
        self.assertEqual(rep["cycles"][0]["state"], "expired")
        self.assertIn("ci:change_fail", rep["flagged"])

    def test_pick_order_puts_what_breaks_ci_before_review_repeats(self):
        _, rep = sense(fixture("harborline"), "--now", NOW, "--since", ALL)
        self.assertEqual(rep["pick_order"][0], "ci:change_fail")
        self.assertEqual(rep["pick_order"][-1], "review:lane_repeat:reader-left-behind")
        self.assertEqual(set(rep["pick_order"]), set(rep["flagged"]))

    def test_an_old_verdict_is_not_reported_again_and_does_not_hold_the_pick(self):
        repo = fixture("quillmark")
        cycles(repo, [{"key": "ci:change_fail", "state": "reverted", "settled_at": "2026-10-01T00:00:00Z",
                       "why": "old"},
                      {"key": "ci:change_fail", "state": "kept", "settled_at": "2026-11-01T00:00:00Z", "why": "later"}])
        code, rep = sense(repo, "--now", NOW, "--since", ALL)
        self.assertEqual(code, 0)
        self.assertEqual(rep["pick_order"], [])
        self.assertEqual(rep["settled_now"], [])

    def test_a_cycle_settled_this_run_is_listed_once(self):
        repo = fixture("tidewater")
        cycles(repo, [{"key": "ci:change_fail", "state": "awaiting", "changed_at": "2026-10-21T10:00:00Z"}])
        code, rep = sense(repo, "--now", NOW, "--since", ALL, "--write")
        self.assertEqual(code, 20)
        self.assertEqual([c["key"] for c in rep["settled_now"]], ["ci:change_fail"])
        code2, rep2 = sense(repo, "--now", NOW, "--since", ALL)
        self.assertEqual(rep2["settled_now"], [])
        self.assertNotEqual(code2, 20)

    def test_a_lane_cycle_settles_on_landings_after_the_change(self):
        repo = fixture("harborline")  # lane hits on LEDGER, REFUND, AUDIT, TAX
        cycles(repo, [{"key": "review:lane_repeat:reader-left-behind", "state": "awaiting",
                       "changed_at": "2026-11-05T00:00:00Z"}])
        _, rep = sense(repo, "--now", NOW, "--since", ALL)
        c = rep["cycles"][0]
        self.assertEqual(c["state"], "reverted")  # TAX (11-12) still had the hit after the change
        self.assertIn("TAX", c["why"])

    def test_a_rate_better_than_the_repo_baseline_does_not_flag(self):
        # tidewater: before 10-21 one of two green-base landings went red, after it one of four
        _, rep = sense(fixture("tidewater"), "--now", NOW, "--since", "2026-10-21T00:00:00Z", "--min-baseline", "2")
        s = sig(rep, "ci:change_fail")
        self.assertEqual(s["trend"], "better")
        self.assertFalse(s["flag"])
        self.assertIn("previous", s)

    def test_a_rate_no_better_than_baseline_flags(self):
        _, rep = sense(fixture("harborline"), "--now", NOW, "--since", "2026-10-15T00:00:00Z", "--min-baseline", "2")
        s = sig(rep, "ci:change_fail")
        self.assertIn(s["trend"], ("same", "worse"))
        self.assertTrue(s["flag"])

    def test_no_history_before_the_window_means_no_baseline_and_events_flag(self):
        _, rep = sense(fixture("harborline"), "--now", NOW, "--since", ALL)
        self.assertEqual(sig(rep, "ci:change_fail")["trend"], "no-baseline")
        self.assertTrue(sig(rep, "ci:change_fail")["flag"])

    def test_latest_red_flags_while_the_integration_branch_is_red(self):
        _, rep = sense(fixture("harborline"), "--now", "2026-10-31T00:00:00Z", "--since", ALL)
        self.assertTrue(sig(rep, "ci:latest_red")["flag"])
        _, rep = sense(fixture("harborline"), "--now", NOW, "--since", ALL)
        self.assertFalse(sig(rep, "ci:latest_red")["flag"])

    def test_blast_radius_flags_when_multi_module_landings_rise(self):
        repo = fixture("quillmark")  # every quillmark landing touches one module (src)
        land(repo, "WIDE", ["billing/core/a.py", "notify/core/b.py", "ledger/core/c.py"], "2026-11-13T10:00:00")
        _, rep = sense(repo, "--now", NOW, "--since", "2026-10-25T00:00:00Z")  # previous window: 3 commits
        s = sig(rep, "arch:blast_radius")
        self.assertEqual(s["events"], ["WIDE"])
        self.assertEqual(s["value"], "1/" + s["value"].split("/")[1])  # one commit crossed modules
        self.assertTrue(s["flag"])
        self.assertEqual(s["trend"], "worse")

    def test_a_violates_verdict_is_an_architecture_signal(self):
        repo = fixture("quillmark")
        land(repo, "PORTX", ["src/ports.py"], "2026-11-13T10:00:00",
             review="inspect-invariants (1 citation)\n  violates ARCH-2  calls persistence directly\n")
        _, rep = sense(repo, "--now", NOW, "--since", ALL)
        s = sig(rep, "arch:invariant_violations")
        self.assertEqual(s["events"], [{"code": "PORTX", "invariant": "ARCH-2"}])
        self.assertTrue(s["flag"])

    def test_posture_is_read_when_present_and_never_flags(self):
        repo = fixture("quillmark")
        os.makedirs(os.path.join(repo, ".skills/scan-architecture"))
        json.dump({"rules_total": 12, "rules_mechanised": 1, "multi_module_commit_pct": 18.7},
                  open(os.path.join(repo, ".skills/scan-architecture/posture.json"), "w"))
        _, rep = sense(repo, "--now", NOW, "--since", ALL)
        s = sig(rep, "arch:posture")
        self.assertEqual(s["value"], "1/12 rules mechanised; 18.7% multi-module commits")
        self.assertFalse(s["flag"])

    def test_blast_radius_cycle_settles_from_the_baseline_slot_when_no_rate_was_recorded(self):
        repo = fixture("quillmark")
        for i, day in enumerate(("15", "16", "17", "18", "19")):
            land(repo, f"NARROW{i}", [f"billing/core/n{i}.py"], f"2026-11-{day}T10:00:00")
        cycles(repo, [{"key": "arch:blast_radius", "state": "awaiting", "baseline": "1/7 (INVOICE)",
                       "changed_at": "2026-11-14T12:00:00Z"}])
        _, rep = sense(repo, "--now", "2026-11-20T00:00:00Z", "--since", ALL)
        self.assertEqual(rep["cycles"][0]["state"], "kept")

    def test_a_previous_window_below_the_minimum_sample_is_no_baseline(self):
        # tidewater before 10-21 has two green-base landings: too few to judge a trend by default
        _, rep = sense(fixture("tidewater"), "--now", NOW, "--since", "2026-10-21T00:00:00Z")
        self.assertEqual(sig(rep, "ci:change_fail")["trend"], "no-baseline")

    def test_an_open_cycle_on_a_red_branch_is_kept_once_the_branch_is_green(self):
        repo = fixture("harborline")
        cycles(repo, [{"key": "ci:latest_red", "state": "open", "opened_at": "2026-10-31T00:00:00Z",
                       "ticket": "draft:.skills/evolve/drafts/ci-latest_red.md"}])
        _, rep = sense(repo, "--now", NOW, "--since", ALL)
        self.assertEqual(rep["cycles"][0]["state"], "kept")
        self.assertNotIn("ci:latest_red", rep["tracked"])

    def test_an_unreadable_blast_baseline_is_inconclusive(self):
        repo = fixture("quillmark")
        for i, day in enumerate(("15", "16", "17", "18", "19")):
            land(repo, f"NARROW{i}", [f"billing/core/n{i}.py"], f"2026-11-{day}T10:00:00")
        cycles(repo, [{"key": "arch:blast_radius", "state": "awaiting", "baseline": "about a third",
                       "changed_at": "2026-11-14T12:00:00Z"}])
        _, rep = sense(repo, "--now", "2026-11-20T00:00:00Z", "--since", ALL)
        self.assertEqual(rep["cycles"][0]["state"], "inconclusive")

    def test_awaiting_cycle_settles_reverted_when_a_green_base_landing_turns_red(self):
        repo = fixture("tidewater")
        cycles(repo, [{"key": "ci:change_fail", "state": "awaiting", "changed_at": "2026-10-21T10:00:00Z"}])
        code, rep = sense(repo, "--now", NOW, "--since", ALL)
        self.assertEqual(code, 20)
        self.assertEqual(rep["cycles"][0]["state"], "reverted")
        self.assertIn("NOTIFY", rep["cycles"][0]["why"])

    def test_awaiting_cycle_goes_inconclusive_after_its_window(self):
        repo = fixture("quillmark")
        cycles(repo, [{"key": "ci:change_fail", "state": "awaiting", "changed_at": "2026-11-13T00:00:00Z"}])
        _, rep = sense(repo, "--now", "2026-12-20T00:00:00Z", "--since", ALL)
        self.assertEqual(rep["cycles"][0]["state"], "inconclusive")

    def test_now_cuts_off_later_history(self):
        _, rep = sense(fixture("harborline"), "--now", "2026-10-12T00:00:00Z", "--since", ALL)
        self.assertEqual([r["code"] for r in rep["landings"]], ["TRAY", "LEDGER", "FEES"])
        self.assertTrue(sig(rep, "ci:runs_real")["flag"])  # mid-outage: the latest run had no runner

    def test_a_shared_non_test_ci_line_is_not_a_match(self):
        repo = fixture("harborline")
        wf = os.path.join(repo, ".github/workflows/ci.yml")
        open(wf, "a").write("      - run: make lint\n")
        _, rep = sense(repo, "--now", NOW, "--since", ALL)
        self.assertEqual(sig(rep, "evidence:close_vs_ci_command")["ci_test_commands"], ["make test-coverage"])
        self.assertTrue(sig(rep, "evidence:close_vs_ci_command")["flag"])

    def test_missing_ci_command_is_a_flag_not_silence(self):
        repo = fixture("quillmark")
        p = os.path.join(repo, "docs/agents/project.md")
        open(p, "w").write(open(p).read().replace("**Integration CI:**", "**Old CI:**"))
        code, rep = sense(repo, "--now", NOW, "--since", ALL)
        self.assertEqual(code, 10)
        self.assertIn("ci:configured", rep["flagged"])


if __name__ == "__main__":
    unittest.main()
