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


if __name__ == "__main__":
    unittest.main()
