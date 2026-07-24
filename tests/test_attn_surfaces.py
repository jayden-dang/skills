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

    def test_ATTN_4_2_binding_hits_are_immovable(self):
        """ATTN-4.2 a binding hit is never removed from the sample."""
        text = SKILL.read_text(encoding="utf-8").lower()
        self.assertIn("never remove", text)

    def test_ATTN_4_3_reason_must_be_distinct_and_concrete(self):
        """ATTN-4.3 agent-add reasons: normalized-unique AND name a path in the unit."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?i)distinct")
        self.assertRegex(text, r"(?i)concrete")
        self.assertIn("git diff --name-only", text)
        self.assertRegex(text, r"(?i)stays in the residue|remains in the residue")

    def test_ATTN_4_5_declined_unit_becomes_residue(self):
        """ATTN-4.5 declining a sampled unit moves it to residue, never 'sampled'."""
        text = SKILL.read_text(encoding="utf-8").lower()
        self.assertIn("declin", text)
        # `\s+` not a literal space: prose wraps these phrases across lines, and
        # markdown bold can sit between the words. Same reason lint-handoffs.py
        # spells its phrasings with `\s+`.
        self.assertRegex(text, r"moves?\s+it\s+to\s+the\W*\s*residue|moves?\s+to\s+the\W*\s*residue")

    def test_ATTN_5_1_5_2_floor_of_one_total_order(self):
        """ATTN-5.1 ATTN-5.2 floor pick uses a three-key total order, never empty."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?i)changed lines")
        self.assertRegex(text, r"(?i)files changed")
        self.assertRegex(text, r"(?i)unit key.{0,40}ascending|ascending.{0,40}byte order")
        self.assertRegex(text, r"(?i)never\s+present\s+an\s+empty\s+sample")

    def test_ATTN_6_1_6_2_claim_and_refuter(self):
        """ATTN-6.1 ATTN-6.2 each sampled unit pairs a claim with its refuter."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("Claim:", text)
        self.assertIn("Refuted by:", text)
        self.assertIn("file:line", text)

    def test_ATTN_6_3_silence_is_not_consent(self):
        """ATTN-6.3 no disposition prints undispositioned, never accepted."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("undispositioned", text)
        self.assertRegex(text, r"(?i)silence\s+is\s+never\s+consent")

    def test_ATTN_6_4_disposition_recorded_verbatim(self):
        """ATTN-6.4 a stated disposition is recorded in the user's own words."""
        text = SKILL.read_text(encoding="utf-8").lower()
        self.assertRegex(text, r"own\s+words")

    def test_ATTN_7_1_7_2_residue_named_and_counted(self):
        """ATTN-7.1 ATTN-7.2 residue is agent-verdict-only, itemised and counted."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("RESIDUE", text)
        self.assertRegex(text, r"(?i)agent\s+verdicts\s+only")

    def test_ATTN_7_3_residue_words_barred(self):
        """ATTN-7.3 residue is never called reviewed/cleared/approved/safe."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?i)never\s+describe\s+the\s+residue\s+as")
        for word in ("reviewed", "cleared", "approved", "safe"):
            self.assertIn(word, text)

    def test_ATTN_7_4_one_allocation_per_run(self):
        """ATTN-7.4 exactly one allocation covers the whole range."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?i)(one|exactly\s+one)\s+allocation\s+per\s+run")

    def test_ATTN_8_1_no_file_by_default(self):
        """ATTN-8.1 conversational output; no file written by default."""
        text = SKILL.read_text(encoding="utf-8").lower()
        self.assertRegex(text, r"writes?\s+\W*no\W*\s*file")

    def test_ATTN_8_3_in_tree_path_hard_fails(self):
        """ATTN-8.3 an in-tree output path hard-fails with no fallthrough."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("git rev-parse --show-toplevel", text)
        self.assertRegex(text, r"(?i)no\s+silent\s+fallthrough|do\s+not\s+silent-fallthrough")

    def test_ATTN_8_4_rerun_is_the_recovery_path(self):
        """ATTN-8.4 re-running over the same range reproduces the allocation."""
        text = SKILL.read_text(encoding="utf-8").lower()
        self.assertIn("re-run", text)

    def test_ATTN_11_4_fail_closed_no_partial(self):
        """ATTN-11.4 a step that cannot complete yields no partial allocation."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?i)no\s+\W*partial\s+allocation")


if __name__ == "__main__":
    unittest.main()
