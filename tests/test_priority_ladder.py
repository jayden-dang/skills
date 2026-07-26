"""Priority ladder: identical artifact state must yield an identical recommendation."""

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LADDER = REPO / "skills" / "track" / "check-roadmap" / "SKILL.md"

# (state substring, expected recommendation substring) — one row per rung, in order.
# Every left-hand string is a verbatim substring of the ladder table in design.md.
ROWS = [
    ("withholding finding", "none"),
    ("is `Draft`", "write-roadmap"),
    ("member with no binding", "brainstorm"),
    ("feature `Status:` is `Draft`", "write-requirements"),
    ("no `design.md`", "write-design"),
    ("`design.md` exists, no `tasks.md`", "write-plan"),
    ("`tasks.md` exists", "execute-plan"),
    ("`Implemented`", "/release"),
    ("all bound and `Shipped`", "/assess-milestone"),
    ("a `Planned` one exists", "write-roadmap"),
    ("every milestone `Closed`", "complete"),
]


class PriorityLadder(unittest.TestCase):
    def setUp(self):
        self.text = LADDER.read_text()
        # Prose wraps, so a phrase can straddle a newline. Collapse whitespace for prose
        # checks; a test that fails on a reflow is coupled to formatting, not behaviour.
        self.flat = re.sub(r"\s+", " ", self.text)

    def test_ladder_is_documented_in_order(self):
        """RMAP-3.10 — the ladder is a fixed, ordered, first-match-wins table."""
        positions = []
        for label, _ in ROWS:
            self.assertIn(label, self.text, f"ladder row missing: {label}")
            positions.append(self.text.index(label))
        self.assertEqual(sorted(positions), positions, "ladder rows are out of order")

    def test_every_row_names_its_recommendation(self):
        """RMAP-3.10 — each state maps to exactly one named action."""
        for label, expected in ROWS:
            with self.subTest(state=label):
                row = next(ln for ln in self.text.splitlines() if label in ln)
                self.assertIn(expected, row)

    def test_first_match_wins_and_ties_are_broken(self):
        """RMAP-3.10 — ordering plus tie-breaks are what make the ladder deterministic."""
        self.assertIn("First match wins", self.text)
        self.assertRegex(self.text, r"(?i)table order")
        self.assertRegex(self.text, r"(?i)lowest\s+`?ROAD-N")

    def test_withholding_replaces_the_recommendation(self):
        """RMAP-3.16 — a withholding finding yields a reason in place of an action."""
        self.assertRegex(self.text, r"withholding reason")

    def test_standup_mode_names_its_three_parts(self):
        """RMAP-3.11 — the card names milestone in flight, member statuses, next action."""
        for part in ("in flight", "members", "next action"):
            with self.subTest(part=part):
                self.assertIn(part, self.flat)

    def test_standup_mode_writes_nothing_either(self):
        """RMAP-3.11 — the second rendering does not acquire write behaviour."""
        standup = self.flat[self.flat.index("Standup mode"):]
        self.assertRegex(standup, r"(?i)read-only")

    def test_release_is_named_not_invoked(self):
        """RMAP-3.10 — row 7 targets a user-invoked skill, so it may only be named (ARCH-5)."""
        row = next(ln for ln in self.text.splitlines() if "/release" in ln)
        self.assertRegex(row, r"(?i)name")

    def test_assessment_rung_names_the_skill_rather_than_invoking_it(self):
        """ASSESS-5.2 — the ladder names /assess-milestone for the user to run."""
        row = next(ln for ln in self.text.splitlines() if "all bound and `Shipped`" in ln)
        self.assertIn("name `/assess-milestone`", row)
        self.assertNotIn("use `assess-milestone`", self.flat)


if __name__ == "__main__":
    unittest.main()
