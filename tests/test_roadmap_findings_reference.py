"""Shared roadmap findings reference: R1-R11 stated in exactly one place."""

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
REFERENCE = REPO / "templates" / "roadmap-findings.md"
CHECK_ROADMAP = REPO / "skills" / "track" / "status-roadmap" / "SKILL.md"

CODES = [f"R{n}" for n in range(1, 12)]
WITHHOLDING = {"R2", "R4", "R9", "R10", "R11"}
ROW = r"(?m)^\| \*\*(R\d+)\*\* \|"


class SharedFindingsReference(unittest.TestCase):
    def setUp(self):
        self.reference = REFERENCE.read_text()
        self.check_roadmap = CHECK_ROADMAP.read_text()

    def test_reference_defines_every_code_once_in_order(self):
        """ASSESS-5.3 — the reference is the single statement of R1-R11."""
        self.assertEqual(re.findall(ROW, self.reference), CODES)

    def test_reference_names_the_withholding_set(self):
        """ASSESS-5.3 — the withholding subset is stated, never re-derived by a reader."""
        marked = set(
            re.findall(r"(?m)^\| \*\*(R\d+)\*\* \|.*\| \*\*yes\*\* \|$", self.reference)
        )
        self.assertEqual(marked, WITHHOLDING)

    def test_check_roadmap_defers_instead_of_restating(self):
        """ASSESS-5.4 — the rules moved; status-roadmap keeps no second copy."""
        self.assertIsNone(re.search(ROW, self.check_roadmap))
        self.assertIn("templates/roadmap-findings.md", self.check_roadmap)

    def test_check_roadmap_still_declares_itself_read_only(self):
        """ASSESS-5.4 — the extraction touches rules only, not the skill's contract."""
        self.assertIn("read-only", self.check_roadmap)


if __name__ == "__main__":
    unittest.main()
