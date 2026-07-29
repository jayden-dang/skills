"""prepare-change conventions: bounded, once per session, uncached, labelled."""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CONV = REPO / "skills" / "ship" / "prepare-change" / "conventions.md"


class PrepareChangeConventions(unittest.TestCase):
    def setUp(self):
        self.assertTrue(CONV.exists(), "conventions.md missing")
        self.text = CONV.read_text()

    def test_PCHG_4_2_three_rung_ladder_in_order(self):
        """PCHG-4.2 — declared artifacts, then bounded subject sample, then fallback."""
        rungs = ["machine-enforced", "non-merge commit subjects", "neutral"]
        positions = [self.text.find(r) for r in rungs]
        self.assertNotIn(-1, positions)
        self.assertEqual(positions, sorted(positions))

    def test_PCHG_4_2_sample_bound_is_twenty(self):
        """PCHG-4.2 — the sample is bounded at 20 subjects."""
        self.assertRegex(self.text, r"at most the 20 most recent non-merge commit subjects")

    def test_PCHG_4_3_no_bodies_or_diffs(self):
        """PCHG-4.3 — historical bodies and diffs are never read during inference."""
        self.assertRegex(self.text, r"(?i)never read .{0,40}(bod|diff)")

    def test_PCHG_4_4_mixed_stops_sampling(self):
        """PCHG-4.4 — a mixed sample falls to the fallback instead of widening."""
        self.assertIn("never widened", self.text)

    def test_PCHG_4_5_pr_conventions_separate(self):
        """PCHG-4.5 — PR structure comes from templates and guidance, not history."""
        self.assertIn("pull-request template", self.text)
        self.assertRegex(self.text, r"(?i)not .{0,30}commit history")

    def test_PCHG_4_1_12_1_once_per_session(self):
        """PCHG-4.1 PCHG-12.1 — resolution happens at most once per session."""
        self.assertIn("at most once per session", self.text)

    def test_PCHG_4_6_inferred_is_labelled_advisory(self):
        """PCHG-4.6 — a history-derived convention is labelled inferred and advisory."""
        self.assertIn("inferred", self.text)
        self.assertIn("advisory", self.text)

    def test_PCHG_4_6_fallback_grade_is_one_of_the_three_enum_values(self):
        """PCHG-4.6 — the grade enum is closed to three values, and every
        ladder rung (including both fallbacks) states one of them explicitly
        instead of hedging with a fourth value like `declared-equivalent`."""
        self.assertNotIn("declared-equivalent", self.text)
        self.assertIn(
            "one of `declared` | `machine-enforced` | `inferred`", self.text
        )
        # Rung 3 (commit fallback) must name its grade as an instruction.
        self.assertRegex(
            self.text, r"Grade this rung `declared`"
        )
        # The PR-structure fallback must also state its grade explicitly.
        self.assertRegex(
            self.text, r"fallback shape[^.]*\)\s+and grade it `declared`"
        )

    def test_PCHG_4_7_no_persistent_cache(self):
        """PCHG-4.7 — nothing is persisted between sessions."""
        self.assertRegex(self.text, r"(?i)no (persistent )?cache|never persist")


if __name__ == "__main__":
    unittest.main()
