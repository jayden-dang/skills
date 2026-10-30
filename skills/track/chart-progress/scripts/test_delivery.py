"""Behavior tests for Focus lanes, delivery proof and the migration slot (unittest, stdlib only).

The fixture is a consuming repo whose PRs squash-merge onto `dev`: the integration ref is
`origin/dev`, a squash commit ends its subject with `(#N)`, and a feature branch head is
never an ancestor of it.
"""

from __future__ import annotations

import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

from extract import extract
from test_extract import INDEX, Repo, catalog

ROADMAP = """# Roadmap: Demo

Status: Approved
Date: 2026-10-01

## Focus

**Now:** MILE-2, ROAD-9
**Next:** MILE-3

| ID | Milestone | Outcome | Depends-on | Commitment |
|---|---|---|---|---|
| MILE-1 | Media | A teacher adds an image. | none | Planned |
| MILE-2 | Authoring | A person builds a course. | none | Planned |
| MILE-3 | Desktop | A person opens a course desktop. | none | Planned |
| MILE-4 | Ops | An operator restores a backup. | none | Planned |

## MILE-1 — Media

**Outcome:** A teacher adds an image.
**Goals:** None
**Members:**
- **ROAD-1** media-blocks — After: ROAD-8 — Surfaces: `web/markdown/`, `migrations/`
- **ROAD-8** asset-store — After: none — Surfaces: `api/assets/`
**Depends-on:** none
**Commitment:** Planned
**Closed:** None
**Deferred:** None
**Blockers:** None

## MILE-2 — Authoring

**Outcome:** A person builds a course.
**Goals:** None
**Members:**
- **ROAD-2** brief-and-plan — After: none — Surfaces: `api/authoring/`
- **ROAD-3** build-run — After: ROAD-2 — Surfaces: `api/authoring/build/`, `migrations/`
- **ROAD-4** image-jobs — After: ROAD-1 — Surfaces: `api/media_jobs/`
- **ROAD-5** brief-outside-default — After: none — Surfaces: `api/authoring/brief/`
**Depends-on:** none
**Commitment:** Planned
**Closed:** None
**Deferred:** None
**Blockers:** None

## MILE-3 — Desktop

**Outcome:** A person opens a course desktop.
**Goals:** None
**Members:**
- **ROAD-6** desktop-foundation — After: ROAD-3 — Surfaces: `web/course/`, `migrations/`
**Depends-on:** none
**Commitment:** Planned
**Closed:** None
**Deferred:** None
**Blockers:** None

## MILE-4 — Ops

**Outcome:** An operator restores a backup.
**Goals:** None
**Members:**
- **ROAD-9** secrets-rotation — After: none — Surfaces: `ops/secrets/`
- **ROAD-10** backups — After: ROAD-9 — Surfaces: `ops/backup/`
**Depends-on:** none
**Commitment:** Planned
**Closed:** None
**Deferred:** None
**Blockers:** None
"""

PROJECT = """# Project

## Project posture

- **Default PR base:** `dev`
- **Delivery proof:** required
- **Serialized surfaces:** `migrations/`
"""


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True).stdout.strip()


def build(root: Path, project: str = PROJECT) -> dict:
    """Returns the SHAs the tests assert against."""
    r = Repo(root)
    r.write("docs/roadmap/INDEX.md", ROADMAP)
    r.write("docs/specs/INDEX.md", INDEX)
    r.write("docs/agents/project.md", project)
    r.write("docs/specs/catalog/core.md", catalog([
        ("PLAN", "Implemented", "ROAD-2 amends ROAD-5"),
        ("BUILD", "Implemented", "ROAD-3"),
        ("ASSET", "Implemented", "ROAD-8"),
    ]))
    # PLAN: delivered by PR #12, squash-merged; its ROAD-5 amendment is fully ticked, PR #14
    r.write("docs/specs/2026-09-01-plan/tasks.md",
            "# Tasks\n\nDelivered-by: PR #12\n\n### Task 1: plan\n\n- [x] Step 1\n\n"
            "## ROAD-5 amendment: a brief never starts in the default project\n\n"
            "Delivered-by: PR #14\n\n### Task 9: refuse\n\n- [x] Step 1\n- [x] Step 2\n")
    # BUILD: Implemented at execute close, PR #13 still open — no integration commit
    r.write("docs/specs/2026-09-01-build/tasks.md", "# Tasks\n\nDelivered-by: PR #13\n\n### Task 1: run\n\n- [x] Step 1\n")
    # ASSET: landed by a local merge; Delivered-by names the merge SHA, filled in below
    r.commit("docs: seed", "2026-09-01")
    r.write("api/plan.txt", "plan\n")
    r.commit("feat(plan): brief and plan (#12)", "2026-09-05")
    r.write("api/amend.txt", "amend\n")
    r.commit("feat(plan): refuse default project (#14)", "2026-09-06")
    git(root, "checkout", "-q", "-b", "feat/asset")
    r.write("api/asset.txt", "asset\n")
    r.commit("feat(asset): store", "2026-09-07")
    git(root, "checkout", "-q", "dev")
    git(root, "merge", "-q", "--no-ff", "-m", "merge(ASSET): land the asset store", "feat/asset")
    merge_sha = git(root, "rev-parse", "HEAD")
    r.write("docs/specs/2026-09-01-asset/tasks.md", f"# Tasks\n\nDelivered-by: {merge_sha[:9]}\n\n### Task 1: store\n\n- [x] Step 1\n")
    r.commit("docs(asset): record delivery", "2026-09-08")
    git(root, "update-ref", "refs/remotes/origin/dev", "HEAD")
    # a BUILD branch head that is not on the integration ref
    git(root, "checkout", "-q", "-b", "feat/build")
    r.write("api/build.txt", "build\n")
    r.commit("feat(build): run", "2026-09-09")
    branch_sha = git(root, "rev-parse", "HEAD")
    git(root, "checkout", "-q", "dev")
    # ROAD-6 holds the migration slot
    git(root, "checkout", "-q", "-b", "locks/migrations")
    r._git("commit", "-q", "--allow-empty", "-m", "slot: ROAD-6 #301")
    git(root, "update-ref", "refs/remotes/origin/locks/migrations", "HEAD")
    git(root, "checkout", "-q", "dev")
    return {"merge": merge_sha, "branch": branch_sha, "integration": git(root, "rev-parse", "refs/remotes/origin/dev")}


class TestDeliveryProof(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name) / "demo"
        cls.root.mkdir()
        cls.shas = build(cls.root)
        cls.snap = extract(cls.root, today="2026-10-14")
        cls.items = {i["id"]: i for i in cls.snap["items"]}
        cls.feats = {f["code"]: f for f in cls.snap["features"]}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def rules(self, rule: str) -> list[dict]:
        return [f for f in self.snap["findings"] if f["rule"] == rule]

    def test_snapshot_records_the_integration_ref_and_its_sha(self):
        self.assertEqual(self.snap["integration"]["ref"], "origin/dev")
        self.assertEqual(self.snap["integration"]["sha"], self.shas["integration"])
        self.assertTrue(self.snap["integration"]["proof_required"])

    def test_binding_cell_separates_the_primary_road_from_amended_roads(self):
        self.assertEqual(self.feats["PLAN"]["roads"], ["ROAD-2"])
        self.assertEqual(self.feats["PLAN"]["amends"], ["ROAD-5"])

    def test_a_squash_merged_pr_resolves_to_its_integration_commit(self):
        self.assertEqual(self.items["ROAD-2"]["state"], "done")
        self.assertEqual(self.items["ROAD-2"]["delivery"]["ref"], "PR #12")
        self.assertTrue(self.items["ROAD-2"]["delivery"]["resolved"])

    def test_a_local_merge_sha_resolves_by_ancestry(self):
        self.assertEqual(self.items["ROAD-8"]["state"], "done")

    def test_implemented_with_an_unmerged_pr_is_in_review_and_unlocks_nothing(self):
        self.assertEqual(self.items["ROAD-3"]["state"], "in-review")
        self.assertIn("ROAD-6", self.snap["graph"]["blocked"])
        self.assertEqual(self.snap["graph"]["blocked"]["ROAD-6"], ["ROAD-3"])
        self.assertNotIn("ROAD-3", self.snap["graph"]["ready"])

    def test_an_amend_road_is_done_when_its_task_group_is_ticked_and_delivered(self):
        self.assertEqual(self.items["ROAD-5"]["state"], "done")
        self.assertEqual(self.items["ROAD-5"]["feature"], "PLAN")

    def test_ambiguous_or_unresolvable_delivery_is_a_finding_and_never_done(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / "demo"
            root.mkdir()
            build(root)
            r = Repo.__new__(Repo)
            r.root = root
            r.write("api/again.txt", "x\n")
            r.commit("revert: plan again (#12)", "2026-09-10")
            git(root, "update-ref", "refs/remotes/origin/dev", "HEAD")
            snap = extract(root, today="2026-10-14")
        items = {i["id"]: i for i in snap["items"]}
        self.assertEqual(items["ROAD-2"]["state"], "in-review")
        self.assertTrue(any(f["rule"] == "DELIVERY" and f["item"] == "ROAD-2" for f in snap["findings"]))

    def test_a_missing_delivered_by_is_in_review_with_a_proposed_candidate(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / "demo"
            root.mkdir()
            shas = build(root)
            tasks = root / "docs/specs/2026-09-01-asset/tasks.md"
            tasks.write_text(re.sub(r"Delivered-by: \w+\n\n", "", tasks.read_text()))
            snap = extract(root, today="2026-10-14")
        items = {i["id"]: i for i in snap["items"]}
        self.assertEqual(items["ROAD-8"]["state"], "in-review")
        self.assertTrue(any(f["rule"] == "DELIVERY" and f["item"] == "ROAD-8" and "no Delivered-by" in f["detail"]
                            for f in snap["findings"]))
        # the merge commit whose subject names ASSET is proposed, never written
        self.assertEqual(snap["delivery_candidates"]["ASSET"], [shas["merge"]])

    def test_without_proof_required_status_alone_still_decides_done(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / "demo"
            root.mkdir()
            build(root, project=PROJECT.replace("- **Delivery proof:** required\n", ""))
            snap = extract(root, today="2026-10-14")
        items = {i["id"]: i for i in snap["items"]}
        self.assertEqual(items["ROAD-3"]["state"], "done")
        self.assertFalse(snap["integration"]["proof_required"])


class TestFocusLanes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.tmp.name) / "demo"
        cls.root.mkdir()
        build(cls.root)
        cls.snap = extract(cls.root, today="2026-10-14")
        cls.lanes = {l["entry"]: l for l in cls.snap["focus"]["lanes"]}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_focus_lines_parse_in_priority_order(self):
        self.assertEqual(self.snap["focus"]["now"], ["MILE-2", "ROAD-9"])
        self.assertEqual(self.snap["focus"]["next"], ["MILE-3"])

    def test_a_milestone_entry_pulls_its_members_and_their_direct_predecessors(self):
        lane = self.lanes["MILE-2"]
        # ROAD-4 waits on ROAD-1 (MILE-1): pulled in one step. ROAD-8, which ROAD-1 waits on, is not.
        self.assertEqual(lane["items"], ["ROAD-1", "ROAD-2", "ROAD-3", "ROAD-4", "ROAD-5"])
        self.assertEqual(lane["horizon"], "now")

    def test_a_road_entry_is_that_item_alone(self):
        self.assertEqual(self.lanes["ROAD-9"]["items"], ["ROAD-9"])

    def test_a_predecessor_two_steps_out_of_focus_is_reported_not_pulled(self):
        # ROAD-8 is done here, so nothing is reported for it; ROAD-6 (MILE-3, Next) waits on ROAD-3, inside Focus.
        out = [f for f in self.snap["findings"] if f["rule"] == "F-OUT"]
        self.assertEqual(out, [])

    def test_structural_focus_defects_are_rule_s9(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / "demo"
            root.mkdir()
            build(root)
            r = Repo.__new__(Repo)
            r.root = root
            r.write("docs/roadmap/INDEX.md", ROADMAP.replace(
                "**Now:** MILE-2, ROAD-9", "**Now:** MILE-2, ROAD-9, ROAD-77, MILE-1, ROAD-8, ROAD-10\n**Next:** ROAD-9"
            ).replace("**Next:** MILE-3\n", ""))
            r.commit("docs: focus", "2026-09-11")
            snap = extract(root, today="2026-10-14")
        details = [f["detail"] for f in snap["findings"] if f["rule"] == "S9"]
        self.assertTrue(any("ROAD-77" in d for d in details))
        self.assertTrue(any("ROAD-9" in d and "twice" in d for d in details))
        self.assertTrue(any("more than 5" in d for d in details))

    def test_a_deeper_predecessor_outside_focus_is_reported(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / "demo"
            root.mkdir()
            build(root)
            r = Repo.__new__(Repo)
            r.root = root
            r.write("docs/specs/catalog/core.md", catalog([
                ("PLAN", "Implemented", "ROAD-2 amends ROAD-5"), ("BUILD", "Implemented", "ROAD-3"),
            ]))
            r.commit("docs: asset unbound", "2026-09-11")
            snap = extract(root, today="2026-10-14")
        out = [f for f in snap["findings"] if f["rule"] == "F-OUT"]
        self.assertEqual([(f["item"], f["detail"]) for f in out],
                         [("ROAD-1", "waits on ROAD-8, outside Focus")])


class TestMigrationSlot(unittest.TestCase):
    def test_the_slot_holder_is_read_from_the_lock_branch(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / "demo"
            root.mkdir()
            build(root)
            snap = extract(root, today="2026-10-14")
        slot = snap["slots"]["migrations/"]
        self.assertEqual(slot["holder"], "ROAD-6")
        waits = {w["item"] for w in slot["waiting"]}
        # ROAD-1 is ready and touches migrations/ while ROAD-6 holds the slot
        self.assertIn("ROAD-1", waits)
        self.assertNotIn("ROAD-6", waits)

    def test_a_lock_held_by_a_done_road_is_a_finding(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t) / "demo"
            root.mkdir()
            build(root)
            git(root, "checkout", "-q", "locks/migrations")
            subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", "slot: ROAD-2 #300"], cwd=root, check=True)
            git(root, "update-ref", "refs/remotes/origin/locks/migrations", "HEAD")
            git(root, "checkout", "-q", "dev")
            snap = extract(root, today="2026-10-14")
        self.assertTrue(any(f["rule"] == "SLOT" and f["item"] == "ROAD-2" for f in snap["findings"]))


if __name__ == "__main__":
    unittest.main()
