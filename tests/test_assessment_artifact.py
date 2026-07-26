"""Milestone assessment artifact: slot contract and disposition value set."""

import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TEMPLATE = REPO / "templates" / "milestone-assessment.md"

SLOTS = [
    "## Assessment",
    "**Supersedes:**",
    "**Committed baseline:**",
    "**Candidate closing revision:**",
    "**Roadmap revision assessed:**",
    "**Assessed:**",
    "### Agent assessment",
    "### Human disposition",
    "**Current:**",
    "**Close decision:**",
    "**History:**",
]
DISPOSITIONS = ["Pending", "Deferred", "Accepted", "Overridden"]
TERMINAL = ["Accepted", "Overridden"]
NON_TERMINAL = ["Pending", "Deferred"]
CLOSE_DECISIONS = ["Close", "Hold"]


class AssessmentTemplate(unittest.TestCase):
    def setUp(self):
        self.text = TEMPLATE.read_text()

    def test_every_required_slot_is_present(self):
        """ASSESS-2.2 — each assessment block carries its full evidence header."""
        for slot in SLOTS:
            with self.subTest(slot=slot):
                self.assertIn(slot, self.text)

    def test_block_heading_grammar_is_ordinal(self):
        """ASSESS-2.1 — one file per milestone, blocks identified by ascending ordinal."""
        self.assertRegex(self.text, r"(?m)^## Assessment \d+")
        self.assertIn("docs/roadmap/assessments/", self.text)

    def test_append_only_rule_is_stated(self):
        """ASSESS-2.3 — earlier blocks are never rewritten."""
        self.assertIn("byte-identical", self.text)

    def test_supersedes_is_required_after_the_first_block(self):
        """ASSESS-2.4 — a further assessment names what it supersedes and why."""
        self.assertRegex(self.text, r"Supersedes:.*Assessment")

    def test_disposition_value_set_is_closed(self):
        """ASSESS-2.14 — exactly four disposition values are allowed."""
        for value in DISPOSITIONS:
            with self.subTest(value=value):
                self.assertIn(value, self.text)

    def test_terminal_values_are_named(self):
        """ASSESS-2.15 — only Accepted and Overridden are terminal."""
        for value in TERMINAL:
            with self.subTest(value=value):
                self.assertRegex(self.text, rf"(?m)^\| `{value}` \| yes \|")
        for value in NON_TERMINAL:
            with self.subTest(value=value):
                self.assertRegex(self.text, rf"(?m)^\| `{value}` \| no \|")

    def test_history_is_dated_and_append_only(self):
        """ASSESS-2.16 — each transition appends a dated entry; latest is current."""
        self.assertIn("latest entry", self.text)

    def test_close_decision_accompanies_every_terminal_disposition(self):
        """ASSESS-4.18 — a terminal disposition records Close or Hold."""
        for value in CLOSE_DECISIONS:
            with self.subTest(value=value):
                self.assertIn(f"`{value}`", self.text)


if __name__ == "__main__":
    unittest.main()
