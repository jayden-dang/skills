"""Behavior tests for lanes.py — the generated docs/roadmap/lanes.md (unittest, stdlib only)."""

from __future__ import annotations

import copy
import tempfile
import unittest
from pathlib import Path

import test_delivery
from extract import extract
from lanes import claims_from_issues, render_lanes, write_lanes

ISSUES = [
    {"number": 301, "title": "ROAD-6 desktop foundation", "assignees": [{"login": "alice"}],
     "labels": [{"name": "building"}], "updatedAt": "2026-10-13T09:00:00Z", "state": "OPEN"},
    {"number": 302, "title": "ROAD-1 media blocks", "assignees": [{"login": "bob"}],
     "labels": [{"name": "shaping"}], "updatedAt": "2026-10-01T09:00:00Z", "state": "OPEN"},
    {"number": 303, "title": "Idea: a notebook beside the course (mentions ROAD-9 in passing)", "assignees": [],
     "labels": [{"name": "needs-triage"}], "updatedAt": "2026-10-13T09:00:00Z", "state": "OPEN"},
]


class TestLanes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name) / "demo"
        root.mkdir()
        cls.shas = test_delivery.build(root)
        cls.snap = extract(root, today="2026-10-14")
        cls.claims = claims_from_issues(ISSUES)
        cls.md = render_lanes(cls.snap, cls.claims, tracker_read="2026-10-14T08:00:00Z")

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def section(self, title: str) -> str:
        return self.md.split(f"## {title}", 1)[1].split("\n## ", 1)[0]

    def test_header_names_the_generated_source_and_tracker_time(self):
        head = self.md.split("\n## ", 1)[0]
        self.assertIn("generated", head.lower())
        self.assertIn(f"origin/dev@{self.shas['integration'][:9]}", head)
        self.assertIn("2026-10-14T08:00:00Z", head)

    def test_now_lanes_appear_in_focus_order(self):
        now = self.section("Now")
        self.assertLess(now.index("MILE-2"), now.index("ROAD-9"))
        self.assertNotIn("MILE-3", now)
        self.assertIn("MILE-3", self.section("Next"))

    def test_an_unmerged_road_reads_in_review(self):
        row = next(l for l in self.section("Now").splitlines() if l.startswith("| ROAD-3 "))
        self.assertIn("In review", row)

    def test_only_an_assigned_issue_titled_with_the_road_is_a_claim(self):
        self.assertEqual(self.claims["ROAD-6"][0]["who"], ["alice"])
        self.assertNotIn("ROAD-9", self.claims)  # mentioned in passing, unassigned
        row = next(l for l in self.section("Next").splitlines() if l.startswith("| ROAD-6 "))
        self.assertIn("@alice #301", row)

    def test_a_claim_quiet_for_seven_days_is_marked_stale(self):
        row = next(l for l in self.section("Now").splitlines() if l.startswith("| ROAD-1 "))
        self.assertIn("@bob #302", row)
        self.assertIn("stale", row)

    def test_the_slot_section_names_the_holder_and_who_waits(self):
        slots = self.section("Slots")
        self.assertIn("`migrations/`", slots)
        self.assertIn("ROAD-6", slots)
        self.assertIn("ROAD-1", slots)

    def test_without_tracker_access_claims_say_so(self):
        md = render_lanes(self.snap, None, tracker_read=None)
        self.assertIn("not read", md.split("\n## ", 1)[0])


    def test_a_ready_item_with_a_spec_says_so(self):
        snap = copy.deepcopy(self.snap)
        next(i for i in snap["items"] if i["id"] == "ROAD-9")["state"] = "specced"
        md = render_lanes(snap, self.claims, tracker_read="2026-10-14T08:00:00Z")
        row = next(l for l in md.split("## Now", 1)[1].splitlines() if l.startswith("| ROAD-9 "))
        self.assertIn("Ready · spec written", row)
        plain = next(l for l in self.section("Now").splitlines() if l.startswith("| ROAD-9 "))
        self.assertNotIn("spec written", plain)

    def test_the_header_names_the_skill_that_regenerates_it(self):
        self.assertIn("`refresh-lanes`", self.md.split("\n## ", 1)[0])

    def test_a_local_integration_ref_is_shown_as_the_branch(self):
        snap = copy.deepcopy(self.snap)
        snap["integration"]["ref"] = "HEAD"
        head = render_lanes(snap, self.claims, tracker_read="2026-10-14T08:00:00Z").split("\n## ", 1)[0]
        self.assertIn(f"`{snap['branch']}@", head)


class TestWriteLanes(unittest.TestCase):
    """When the file is written: only on the base branch, only with a Focus, only when a lane changed."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        root = Path(cls.tmp.name) / "demo"
        root.mkdir()
        test_delivery.build(root)
        cls.snap = extract(root, today="2026-10-14")
        cls.claims = claims_from_issues(ISSUES)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def setUp(self):
        self.out = Path(tempfile.mkdtemp(dir=self.tmp.name)) / "docs/roadmap/lanes.md"

    def test_the_fixture_sits_on_its_base_branch(self):
        self.assertEqual(self.snap["branch"], self.snap["integration"]["base"])

    def test_on_the_base_branch_the_file_is_written(self):
        self.assertEqual(write_lanes(self.snap, self.claims, "2026-10-14T08:00:00Z", self.out), "written")
        self.assertIn("## Now", self.out.read_text())

    def test_a_new_tracker_reading_alone_leaves_the_file_as_it_was(self):
        write_lanes(self.snap, self.claims, "2026-10-14T08:00:00Z", self.out)
        before = self.out.read_text()
        self.assertEqual(write_lanes(self.snap, self.claims, "2026-10-14T09:30:00Z", self.out), "unchanged")
        self.assertEqual(self.out.read_text(), before)

    def test_a_changed_lane_rewrites_the_file(self):
        write_lanes(self.snap, self.claims, "2026-10-14T08:00:00Z", self.out)
        snap = copy.deepcopy(self.snap)
        next(i for i in snap["items"] if i["id"] == "ROAD-3")["state"] = "done"
        self.assertEqual(write_lanes(snap, self.claims, "2026-10-14T09:30:00Z", self.out), "written")
        self.assertIn("09:30", self.out.read_text())

    def test_off_the_base_branch_nothing_is_written(self):
        snap = copy.deepcopy(self.snap)
        snap["branch"] = "feat/asset"
        self.assertEqual(write_lanes(snap, self.claims, None, self.out), f"not on {snap['integration']['base']}")
        self.assertFalse(self.out.exists())

    def test_without_a_focus_nothing_is_written(self):
        snap = copy.deepcopy(self.snap)
        snap["focus"] = {"present": False, "now": [], "next": [], "lanes": []}
        self.assertEqual(write_lanes(snap, self.claims, None, self.out), "no Focus")
        self.assertFalse(self.out.exists())


    def test_without_a_configured_base_the_remote_default_branch_is_the_base(self):
        root = Path(tempfile.mkdtemp(dir=self.tmp.name)) / "bare-config"
        root.mkdir()
        test_delivery.build(root)
        cfg = root / "docs/agents/project.md"
        cfg.write_text("\n".join(l for l in cfg.read_text().splitlines() if "Default PR base" not in l) + "\n")
        test_delivery.git(root, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/dev")
        self.assertEqual(extract(root, today="2026-10-14")["integration"]["base"], "dev")


if __name__ == "__main__":
    unittest.main()
