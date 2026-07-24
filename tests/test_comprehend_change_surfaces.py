"""Structural surfaces for comprehend-change (XDIFF)."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/review/comprehend-change/SKILL.md"
PLUGIN = ROOT / ".claude-plugin/plugin.json"
SHELL = ROOT / "skills/review/comprehend-change/shell/packet.html"
REFS = ROOT / "skills/review/comprehend-change/references"


class TestComprehendChangeSurfaces(unittest.TestCase):
    def test_XDIFF_1_1_1_2_skill_frontmatter(self):
        """XDIFF-1.1 XDIFF-1.2 skill name and user-invoked flag."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("name: comprehend-change", text)
        self.assertIn("disable-model-invocation: true", text)
        self.assertRegex(text, r"(?i)comprehend|self-check")

    def test_XDIFF_8_2_package_and_plugin(self):
        """XDIFF-8.2 package path registered in plugin."""
        self.assertTrue(SKILL.is_file())
        data = json.loads(PLUGIN.read_text(encoding="utf-8"))
        self.assertIn("./skills/review/comprehend-change", data["skills"])

    def test_XDIFF_8_4_no_saas_requirement_in_skill(self):
        """XDIFF-8.4 skill must not require Notion/SaaS as product path."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertNotRegex(text, r"(?i)required.*notion|must use notion")

    def test_XDIFF_4_1_4_2_4_11_shell_exists_offline(self):
        """XDIFF-4.1 XDIFF-4.2 XDIFF-4.11 self-contained shell template."""
        text = SHELL.read_text(encoding="utf-8")
        self.assertIn('id="background"', text)
        self.assertIn('id="intuition"', text)
        self.assertIn('id="code"', text)
        self.assertIn('id="quiz"', text)
        self.assertRegex(text, r"white-space:\s*pre(-wrap)?")
        self.assertNotRegex(text, r"https?://cdn\.|fonts\.googleapis")

    def test_XDIFF_5_3_5_4_9_2_quiz_interaction_hooks(self):
        """XDIFF-5.3 XDIFF-5.4 XDIFF-9.2 quiz feedback + shuffle + focus."""
        text = SHELL.read_text(encoding="utf-8")
        self.assertRegex(text, r"shuffle|seed|correctIndex")
        self.assertRegex(text, r"focus-visible|:focus")
        self.assertRegex(text, r"correct|incorrect|feedback", re.I)

    def test_XDIFF_7_2_7_3_escape_and_no_diff_script_injection(self):
        """XDIFF-7.2 XDIFF-7.3 escape path; content is data not instructions."""
        text = SHELL.read_text(encoding="utf-8")
        self.assertRegex(text, r"__PACKET_DATA__|PACKET_DATA|escapeHtml|escape")

    def test_XDIFF_7_1_reference_pack_present(self):
        """XDIFF-7.1 passive-data-safety reference exists with passive data rule."""
        p = REFS / "passive-data-safety.md"
        text = p.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?i)passive data")

    def test_XDIFF_7_1_8_1_supporting_ref_files_and_package_complete(self):
        """XDIFF-7.1 XDIFF-8.1 shell + references + SKILL complete the package."""
        base = ROOT / "skills/review/comprehend-change"
        self.assertTrue((base / "SKILL.md").is_file())
        self.assertTrue((base / "shell/packet.html").is_file())
        for name in (
            "references/quiz-quality.md",
            "references/dec-whitelist.md",
            "references/html-constraints.md",
            "references/passive-data-safety.md",
        ):
            self.assertTrue((base / name).is_file(), name)
        q = (base / "references/quiz-quality.md").read_text(encoding="utf-8")
        self.assertRegex(q, r"(?i)five|5")
        self.assertRegex(q, r"(?i)trivial")
        d = (base / "references/dec-whitelist.md").read_text(encoding="utf-8")
        self.assertIn("Human-Accepted-Risk:", d)
        self.assertIn("Human-Response-If-Wrong:", d)
        self.assertIn("Evidence:", d)

    def test_XDIFF_skill_body_cascade_and_gates(self):
        """XDIFF-1.3 XDIFF-1.4 XDIFF-1.5 XDIFF-1.6 XDIFF-2.1 XDIFF-2.2 XDIFF-2.3 XDIFF-2.4 XDIFF-2.5 XDIFF-2.6 XDIFF-2.7 XDIFF-3.1 XDIFF-3.2 XDIFF-3.3 XDIFF-3.4 XDIFF-3.5 XDIFF-4.3 XDIFF-4.4 XDIFF-4.5 XDIFF-4.6 XDIFF-4.7 XDIFF-4.8 XDIFF-4.9 XDIFF-4.10 XDIFF-4.12 XDIFF-5.1 XDIFF-5.2 XDIFF-5.5 XDIFF-5.6 XDIFF-5.7 XDIFF-5.8 XDIFF-5.9 XDIFF-6.6 XDIFF-6.7 XDIFF-9.1 XDIFF-10.6 body contracts."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?i)The Iron Law")
        self.assertRegex(text, r"(?i)## Red flags")
        self.assertRegex(text, r"(?i)pure.?untracked")
        self.assertRegex(text, r"(?i)tracked.?dirty|working tree vs")
        self.assertRegex(text, r"(?i)truly.?clean")
        self.assertRegex(text, r"(?i)scope notice")
        self.assertRegex(text, r"(?i)symbolic-ref|origin/HEAD")
        self.assertRegex(text, r"(?i)hard-fail|hard fail|hard-stop|hard stop")
        self.assertRegex(text, r"(?i)include-untracked")
        self.assertRegex(text, r"(?i)\.gitignore")
        self.assertRegex(text, r"(?i)exactly five|exactly 5|five medium")
        self.assertRegex(text, r"(?i)never omit|not omit|no omit.*trivial|trivial")
        self.assertRegex(text, r"(?i)never claim.*pass|do not claim.*pass|never.*passed the quiz")
        self.assertRegex(text, r"(?i)record-decision")
        self.assertRegex(text, r"(?i)docs/decisions")
        self.assertRegex(text, r"(?i)design-page")
        self.assertRegex(text, r"(?i)outside.*worktree|outside the.*repo|outside git")
        self.assertRegex(text, r"(?i)comprehension-")
        self.assertRegex(text, r"(?i)COMPREHEND_CHANGE_OUTPUT_DIR|Output-dir")
        self.assertRegex(text, r"(?i)Background")
        self.assertRegex(text, r"(?i)Intuition")
        self.assertRegex(text, r"(?i)ASCII")
        self.assertRegex(text, r"(?i)auto-run|soft-prompt|ship-menu|finish-branch")
        self.assertRegex(text, r"(?i)outbound")
        self.assertRegex(text, r"(?i)partial.*HTML|PARTIAL SUCCESS HTML")
        self.assertRegex(text, r"(?i)WHEN.*quiz-quality\.md|load `references/quiz-quality")
        self.assertRegex(text, r"(?i)silent-fallthrough|silent fallthrough")

    def test_XDIFF_dec_protocol(self):
        """XDIFF-6.1 XDIFF-6.2 XDIFF-6.3 XDIFF-6.4 XDIFF-6.5 XDIFF-6.8 XDIFF-6.9 XDIFF-6.10 DEC enrichment."""
        text = SKILL.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?i)docs/decisions")
        self.assertRegex(text, r"(?i)forward-cite|forward cite|mechanically cites")
        self.assertRegex(text, r"(?i)same-feature|recent")
        self.assertRegex(text, r"(?i)explicit")
        self.assertRegex(text, r"≤5|<=5|at most 5|cap")
        self.assertRegex(text, r"(?i)DEC-\*")
        self.assertIn("Human-Accepted-Risk:", text)
        self.assertRegex(text, r"(?i)reverse-link|reverse link")

    def test_XDIFF_8_3_guide_exists(self):
        """XDIFF-8.3 human guide path."""
        p = ROOT / "docs/guide/skills/comprehend-change.md"
        text = p.read_text(encoding="utf-8")
        self.assertRegex(text, r"(?i)cascade|untracked|quiz|decision record")

    def test_XDIFF_10_1_through_10_5_10_7_10_8_10_9_neighbors(self):
        """XDIFF-10.1 XDIFF-10.2 XDIFF-10.3 XDIFF-10.4 XDIFF-10.5 XDIFF-10.7 XDIFF-10.8 XDIFF-10.9
        neighbors must not soft-prompt or require comprehend-change."""
        forbidden_callers = [
            "skills/ship/finish-branch/SKILL.md",
            "skills/ship/release/SKILL.md",
            "skills/review/code-review/SKILL.md",
            "skills/execution/execute-plan/SKILL.md",
            "skills/ship/record-decision/SKILL.md",
        ]
        for rel in forbidden_callers:
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertNotRegex(
                text,
                r"(?i)comprehend-change|REQUIRED SUB-SKILL: use `comprehend-change`",
            )
        skill = SKILL.read_text(encoding="utf-8")
        self.assertRegex(skill, r"(?i)digest")
        self.assertRegex(skill, r"(?i)not.*digest|never.*digest|not named.*digest")
        self.assertRegex(skill, r"(?i)design-page.*optional|optional.*design-page")
        self.assertIn("comprehend-change", (ROOT / "AGENTS.md").read_text(encoding="utf-8"))
        self.assertIn(
            "comprehend-change",
            (ROOT / "docs/architecture/skills.md").read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
