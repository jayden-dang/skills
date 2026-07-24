"""Structural surfaces for allocate-attention (ATTN)."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/review/allocate-attention/SKILL.md"
REFS = ROOT / "skills/review/allocate-attention/references"
PLUGIN = ROOT / ".claude-plugin/plugin.json"


class TestAttnSurfaces(unittest.TestCase):
    def test_ATTN_1_1_skill_frontmatter_user_invoked(self):
        """ATTN-1.1 skill name and user-invoked flag."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("name: allocate-attention", text)
        self.assertIn("disable-model-invocation: true", text)

    def test_ATTN_1_1_description_carries_outcome_and_triggers(self):
        """ATTN-1.1 description = trigger + outcome noun, with literal phrasings."""
        text = SKILL.read_text(encoding="utf-8")
        head = text.split("---")[1].lower()
        for phrase in (
            "what should i review first",
            "spot check",
            "too much to review",
            "residue",
            "sample",
        ):
            self.assertIn(phrase, head, f"description missing trigger phrase: {phrase}")

    def test_ATTN_1_1_registered_in_plugin_manifest(self):
        """ATTN-1.1 package path registered in plugin."""
        self.assertTrue(SKILL.is_file())
        data = json.loads(PLUGIN.read_text(encoding="utf-8"))
        self.assertIn("./skills/review/allocate-attention", data["skills"])

    def test_ATTN_1_5_no_adverse_claim_for_absence(self):
        """ATTN-1.5 absence of a run carries no adverse claim."""
        text = SKILL.read_text(encoding="utf-8").lower()
        self.assertIn("carries no adverse claim", text)

    def test_ATTN_2_3_2_4_default_base_cascade(self):
        """ATTN-2.3 ATTN-2.4 two-pass base cascade then hard-fail."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("refs/remotes/origin/HEAD", text)
        self.assertIn("git rev-parse --verify", text)
        self.assertRegex(text, r"`main`.{0,20}`master`")
        self.assertRegex(text, r"(?i)hard-fail.{0,120}explicit base")

    def test_ATTN_2_2_default_range_is_merge_base(self):
        """ATTN-2.2 default range is merge-base(default_base, HEAD)..HEAD."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("merge-base", text)
        self.assertRegex(text, r"merge-base\([^)]{0,40}\)\.\.HEAD")

    def test_ATTN_2_5_local_only_no_network(self):
        """ATTN-2.5 ATTN-11.3 local git only, no network."""
        text = SKILL.read_text(encoding="utf-8").lower()
        self.assertIn("no network", text)

    def test_ATTN_2_6_empty_range_hard_fails(self):
        """ATTN-2.6 empty range hard-fails with no allocation."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("git rev-list --count", text)
        self.assertRegex(text, r"(?i)empty range")

    def test_ATTN_2_7_dirty_tree_notice(self):
        """ATTN-2.7 uncommitted work excluded with one notice."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("git ls-files --others --exclude-standard", text)
        self.assertRegex(text, r"(?i)uncommitted work is not included")

    def test_ATTN_3_1_partition_depth_two(self):
        """ATTN-3.1 every changed file maps to exactly one depth-2 unit key."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("git diff --name-only", text)
        self.assertRegex(text, r"(?i)first two segments")
        self.assertRegex(text, r"(?i)exactly one")

    def test_ATTN_3_2_binding_is_mechanical_not_judgment(self):
        """ATTN-3.2 binding membership is a fixed git/grep pass, never model judgment."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("git diff --numstat", text)
        self.assertRegex(text, r"(?i)never (a )?model judgment|not by model judgment")

    def test_ATTN_3_3_3_4_no_cap_on_binding_hits(self):
        """ATTN-3.3 ATTN-3.4 binding hits are uncapped."""
        text = SKILL.read_text(encoding="utf-8").lower()
        self.assertIn("no cap", text)

    def test_ATTN_3_5_all_units_bind_means_whole_range(self):
        """ATTN-3.5 if every unit fires, the whole range is the sample."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?i)whole range is the sample|the whole range as the sample")

    def test_ATTN_3_6_five_binding_signals_present(self):
        """ATTN-3.6 the five signals B1..B5 are defined with fixed rules."""
        text = SKILL.read_text(encoding="utf-8")
        for sig in ("B1", "B2", "B3", "B4", "B5"):
            self.assertIn(f"**{sig}**", text, f"missing binding signal {sig}")

    def test_ATTN_11_2_passive_data_rule(self):
        """ATTN-11.2 range text is passive data, never instructions."""
        text = SKILL.read_text(encoding="utf-8").lower()
        self.assertIn("passive data", text)

    def test_ATTN_3_2_signals_reference_exists(self):
        """ATTN-3.2 ARCH-2 risk globs live in a reference with an absent-section no-op."""
        text = (REFS / "signals.md").read_text(encoding="utf-8")
        self.assertIn("## Attention signals", text)
        self.assertRegex(text, r"(?i)absent.{0,80}default")


if __name__ == "__main__":
    unittest.main()
