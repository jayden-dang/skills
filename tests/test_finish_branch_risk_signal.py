"""land-branch risk signal: globs against the diff, not per-task Risk: slots."""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FINISH = REPO / "skills" / "ship" / "land-branch" / "SKILL.md"
XPLN_REQ = REPO / "docs" / "specs" / "2026-07-27-brief-team" / "requirements.md"
SCENARIOS = REPO / "tests" / "brief-team" / "scenarios.md"


class FinishBranchRiskSignal(unittest.TestCase):
    def setUp(self):
        self.text = FINISH.read_text()

    def test_names_both_optional_skills(self):
        """XPLN-5.6 XPLN-5.7 — land-branch still names both optional skills."""
        self.assertIn("/study-change", self.text)
        self.assertIn("/brief-team", self.text)

    def test_trigger_uses_risk_glob_not_risk_slot(self):
        """XPLN-5.6 — trigger is multi-task OR risk glob OR architecture-affecting."""
        # Old agent-authored field must be gone from the trigger prose.
        self.assertNotRegex(
            self.text,
            r"Risk\s*slot|Risk:\s*|non-low risk|whose \*\*Risk\*\*",
            msg="land-branch still keys off per-task Risk: labels",
        )
        self.assertRegex(
            self.text,
            r"risk glob|risk-glob|Risk globs",
            msg="land-branch must key off risk globs against the diff",
        )
        self.assertIn("multi-task", self.text)
        self.assertIn("architecture-affecting", self.text)

    def test_xpln_5_1_retired_and_5_6_defined(self):
        """XPLN-5.6 XPLN-5.7 — requirements carry the fix and guard; 5.1 struck."""
        req = XPLN_REQ.read_text()
        self.assertRegex(req, r"~~\*\*XPLN-5\.1\*\*~~")
        self.assertIn("**XPLN-5.6**", req)
        self.assertIn("**XPLN-5.7**", req)
        self.assertIn("risk glob", req)

    def test_scenarios_cite_new_ids(self):
        """Coverage tokens track live IDs, not the retired one as sole citation."""
        sc = SCENARIOS.read_text()
        self.assertIn("XPLN-5.6", sc)
        self.assertIn("XPLN-5.7", sc)
        # Retired ID may appear only as retirement note elsewhere; scenarios must
        # not claim XPLN-5.1 as live coverage.
        live = [
            line
            for line in sc.splitlines()
            if re.search(r"XPLN-5\.1\b", line) and "retired" not in line.lower()
        ]
        self.assertEqual([], live, f"scenarios still treat XPLN-5.1 as live: {live}")


if __name__ == "__main__":
    unittest.main()
