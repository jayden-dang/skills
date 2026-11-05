#!/usr/bin/env python3
"""Run: python3 skills/track/shape/scripts/test_check_card.py"""
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).with_name("check_card.py")

GOOD = """# ROAD-4 calendar-export

**Outcome:** A dock crew member imports one berth's arrivals for a month into their phone calendar.

**Examples:**
1. Ada is booked on B2 from 2026-11-06. The B2 export for 2026-11 holds one all-day event "Ada".
2. B3 has no bookings in 2026-12. The export still writes a valid, empty file.

**Must keep:** `quay list` output stays exactly as it is.
**Off limits:** syncing calendars.
**Decided:** one `.ics` file per berth per month.
**Delegated:** event IDs, time zones, flag names.
**Ask me:** anything that writes to the bookings file.
**UI:** none
"""


class CheckCard(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.dir.cleanup)
        self.root = Path(self.dir.name)

    def run_card(self, text):
        path = self.root / "card.md"
        path.write_text(text)
        out = subprocess.run([sys.executable, str(SCRIPT), str(path), "--root", str(self.root)],
                             capture_output=True, text=True)
        return out.returncode, out.stdout

    def test_complete_card_is_ready(self):
        code, out = self.run_card(GOOD)
        self.assertEqual(code, 0, out)
        self.assertIn("card: ready", out)
        self.assertIn("ui: none", out)

    def test_missing_slot_is_named(self):
        code, out = self.run_card(GOOD.replace("**Ask me:** anything that writes to the bookings file.\n", ""))
        self.assertEqual(code, 1)
        self.assertIn("missing: Ask me", out)

    def test_one_example_is_too_few(self):
        code, out = self.run_card(GOOD.replace("2. B3 has no bookings in 2026-12. The export still writes a valid, empty file.\n", ""))
        self.assertEqual(code, 1)
        self.assertIn("examples: 1, need 2 to 5", out)

    def test_six_examples_is_too_many(self):
        extra = "".join(f"{n}. Example number {n} with a value.\n" for n in range(3, 7))
        code, out = self.run_card(GOOD.replace("**Must keep:**", extra + "\n**Must keep:**"))
        self.assertEqual(code, 1)
        self.assertIn("examples: 6, need 2 to 5", out)

    def test_outcome_cannot_be_none(self):
        code, out = self.run_card(GOOD.replace(
            "**Outcome:** A dock crew member imports one berth's arrivals for a month into their phone calendar.",
            "**Outcome:** None"))
        self.assertEqual(code, 1)
        self.assertIn("empty: Outcome", out)

    def test_none_is_a_valid_answer_for_the_lists(self):
        code, out = self.run_card(GOOD.replace("**Off limits:** syncing calendars.", "**Off limits:** None"))
        self.assertEqual(code, 0, out)

    def test_unstated_ui_defaults_to_reuse(self):
        code, out = self.run_card(GOOD.replace("**UI:** none\n", ""))
        self.assertEqual(code, 0, out)
        self.assertIn("ui: reuse (default)", out)

    def test_unknown_ui_level_fails(self):
        code, out = self.run_card(GOOD.replace("**UI:** none", "**UI:** fancy"))
        self.assertEqual(code, 1)
        self.assertIn("ui: fancy is not one of none, reuse, reference, new", out)

    def test_reference_needs_a_reference_line(self):
        code, out = self.run_card(GOOD.replace("**UI:** none", "**UI:** reference"))
        self.assertEqual(code, 1)
        self.assertIn("missing: Reference", out)
        code, out = self.run_card(GOOD.replace("**UI:** none", "**UI:** reference\n**Reference:** Google Calendar's import dialog"))
        self.assertEqual(code, 0, out)

    def test_new_ui_needs_a_ui_brief_on_disk(self):
        card = GOOD.replace("**UI:** none", "**UI:** new\n**UI brief:** docs/specs/2026-11-cal/ui-brief.md")
        code, out = self.run_card(card)
        self.assertEqual(code, 1)
        self.assertIn("ui brief not found: docs/specs/2026-11-cal/ui-brief.md", out)
        brief = self.root / "docs/specs/2026-11-cal/ui-brief.md"
        brief.parent.mkdir(parents=True)
        brief.write_text("# UI brief\n")
        code, out = self.run_card(card)
        self.assertEqual(code, 0, out)

    def test_long_card_fails_the_size_cap(self):
        padding = "".join(f"- solution detail line {n}\n" for n in range(30))
        code, out = self.run_card(GOOD + padding)
        self.assertEqual(code, 1)
        self.assertIn("too long:", out)

    def test_missing_file_is_reported(self):
        out = subprocess.run([sys.executable, str(SCRIPT), str(self.root / "nope.md")], capture_output=True, text=True)
        self.assertEqual(out.returncode, 2)
        self.assertIn("no card at", out.stdout)


if __name__ == "__main__":
    unittest.main()
