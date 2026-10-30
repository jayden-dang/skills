"""Behavior tests for lanes.py — the generated docs/roadmap/lanes.md (unittest, stdlib only)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import test_delivery
from extract import extract
from lanes import claims_from_issues, render_lanes

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


if __name__ == "__main__":
    unittest.main()
