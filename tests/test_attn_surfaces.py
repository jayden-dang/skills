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


if __name__ == "__main__":
    unittest.main()
