"""pathfind SKILL.md body contracts — plan-don't-do, types, modes.

PFIND-1.2 PFIND-1.3 PFIND-4.* PFIND-5.* (skeleton); Chart/Work extended in later tasks.
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "discovery" / "pathfind" / "SKILL.md"


def _frontmatter(text: str) -> str:
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    self_assert = m is not None
    if not self_assert:
        return ""
    return m.group(1)


class PathfindSkeletonContract(unittest.TestCase):
    def setUp(self):
        self.assertTrue(SKILL.exists(), "skills/discovery/pathfind/SKILL.md missing")
        self.text = SKILL.read_text()
        self.fm = _frontmatter(self.text)
        # Body after second ---
        parts = self.text.split("---", 2)
        self.body = parts[2] if len(parts) > 2 else self.text

    def test_PFIND_1_3_description_plain_no_workflow_steps(self):
        """PFIND-1.3 — human description; no Chart/Work step summary in frontmatter."""
        self.assertIn("description:", self.fm)
        # Must not walk Chart then Work as a procedure in description
        desc = re.search(r"description:\s*(.+?)(?=\n\w|\n---|\Z)", self.fm, re.DOTALL)
        self.assertIsNotNone(desc)
        d = desc.group(1).lower()
        self.assertNotIn("chart mode", d)
        self.assertNotIn("work mode", d)
        self.assertNotRegex(d, r"1\.\s*chart|step 1")

    def test_PFIND_1_2_modes_chart_and_work(self):
        """PFIND-1.2 — body names Chart and Work modes."""
        self.assertRegex(self.body, r"(?i)\bchart\b")
        self.assertRegex(self.body, r"(?i)\bwork\b")

    def test_PFIND_4_2_exact_ticket_types(self):
        """PFIND-4.2 — types clarify, research, prototype, task."""
        for t in ("clarify", "research", "prototype", "task"):
            self.assertIn(t, self.body)

    def test_PFIND_4_7_pathfind_labels_no_grilling_wayfinder_types(self):
        """PFIND-4.7 — pathfind:map and pathfind:clarify; no grilling/wayfinder type names."""
        self.assertIn("pathfind:map", self.body)
        self.assertIn("pathfind:clarify", self.body)
        # Forbid as type/label identifiers (allow historical mention in vocabulary note)
        # Must not assign Type: grilling or label wayfinder:
        self.assertNotRegex(self.body, r"(?m)^\s*[-*]\s*`?grilling`?\s*[|:]")
        self.assertNotIn("wayfinder:map", self.body)
        self.assertNotIn("wayfinder:grilling", self.body)
        self.assertNotIn("pathfind:grilling", self.body)

    def test_PFIND_5_1_5_2_plan_dont_do(self):
        """PFIND-5.1 PFIND-5.2 — plan-don't-do; no production code / no minting CODE-N.M."""
        self.assertRegex(self.body, r"(?i)plan.?don.?t.?do|PLAN.?DON.?T.?DO|decisions, not deliverables")
        self.assertRegex(self.body, r"(?i)(no|not|never|SHALL NOT).{0,40}production")
        self.assertRegex(self.body, r"CODE-N\.M|requirement IDs")

    def test_PFIND_5_4_no_publish_issues_cross_graph(self):
        """PFIND-5.4 — no blocking edges between pathfind and implement issues."""
        self.assertRegex(
            self.body,
            r"(?is)(publish-issues|implement).{0,80}(block|edge|graph)|"
            r"(strict separation|URL.?title only|no cross)",
        )

    def test_PFIND_4_1_decision_tickets(self):
        """PFIND-4.1 — decision ticket vocabulary."""
        self.assertRegex(self.body, r"(?i)decision ticket")

    def test_PFIND_5_5_delivery_spine_continues(self):
        """PFIND-5.5 — delivery still requires frame-change / test-first spine."""
        self.assertRegex(self.body, r"(?i)frame-change|delivery spine|test-first")


if __name__ == "__main__":
    unittest.main()
