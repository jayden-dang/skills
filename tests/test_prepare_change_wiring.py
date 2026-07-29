"""prepare-change registration: the skill exists, is model-invoked, and is installable."""
import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "ship" / "prepare-change" / "SKILL.md"
AGENTS = REPO / "AGENTS.md"
README = REPO / "README.md"
PLUGIN = REPO / ".claude-plugin" / "plugin.json"
MARKET = REPO / ".claude-plugin" / "marketplace.json"


class PrepareChangeRegistration(unittest.TestCase):
    def test_PCHG_11_13_skill_file_exists_and_is_model_invoked(self):
        """PCHG-11.13 — the skill exists and no disable-model-invocation key is set."""
        self.assertTrue(SKILL.exists(), "skills/ship/prepare-change/SKILL.md missing")
        text = SKILL.read_text()
        self.assertIn("name: prepare-change", text)
        self.assertNotIn("disable-model-invocation", text)

    def test_PCHG_11_13_phases_named_in_order(self):
        """PCHG-11.13 — the six phases appear in the documented order."""
        text = SKILL.read_text()
        phases = ["Resolve base", "Resolve conventions", "Gather context",
                  "Resolve tickets", "Author commits", "Write package"]
        positions = [text.find(p) for p in phases]
        self.assertNotIn(-1, positions, f"missing phase among {phases}")
        self.assertEqual(positions, sorted(positions), "phases are out of order")

    def test_PCHG_11_13_registered_in_both_manifests(self):
        """PCHG-11.13 — plugin and marketplace manifests list the skill path."""
        for manifest in (PLUGIN, MARKET):
            self.assertIn("./skills/ship/prepare-change", manifest.read_text(),
                          f"{manifest.name} does not list prepare-change")
            json.loads(manifest.read_text())

    def test_PCHG_11_13_named_in_agents_and_readme(self):
        """PCHG-11.13 — the roster documents name the skill."""
        self.assertIn("prepare-change", AGENTS.read_text())
        self.assertIn("prepare-change", README.read_text())

    def test_PCHG_11_13_iron_laws_unchanged(self):
        """PCHG-11.13 — the four Iron Laws and the forbidden-pattern list survive the AGENTS.md edit."""
        agents = AGENTS.read_text()
        for law in ("Gate 1 — NO-CODE", "Gate 2 — TEST-FIRST",
                    "Gate 3 — ROOT-CAUSE", "Gate 4 — EVIDENCE"):
            self.assertIn(law, agents)
        self.assertIn("## 9. Forbidden Patterns", agents)
        self.assertIn(
            "Start implementation on main/master without explicit user consent",
            agents,
        )


EXEC = REPO / "skills" / "execution" / "execute-plan" / "SKILL.md"


class ExecutePlanTail(unittest.TestCase):
    def setUp(self):
        self.text = EXEC.read_text()

    def test_PCHG_9_1_prepare_change_runs_before_finish_branch(self):
        """PCHG-9.1 — prepare-change sits between acceptance and finish-branch."""
        tail = self.text.split("## After the Last Task")[1]
        acceptance = tail.find("acceptance-check")
        prepare = tail.find("prepare-change")
        finish = tail.find("finish-branch")
        self.assertNotEqual(prepare, -1, "prepare-change is not in the closing sequence")
        self.assertLess(acceptance, prepare, "prepare-change runs before acceptance")
        self.assertLess(prepare, finish, "prepare-change runs after finish-branch")

    def test_PCHG_11_7_closing_order_preserved(self):
        """PCHG-11.7 — review, fixer, polish, acceptance keep their order."""
        tail = self.text.split("## After the Last Task")[1]
        for earlier, later in (("code-review", "polish"), ("polish", "acceptance-check")):
            self.assertLess(tail.find(earlier), tail.find(later))

    def test_PCHG_11_8_continuous_mode_still_never_pauses(self):
        """PCHG-11.8 — the no-pause red flag survives."""
        self.assertIn("Pause between tasks to ask permission to continue", self.text)

    def test_PCHG_11_9_ledger_append_survives(self):
        """PCHG-11.9 — the per-task ledger append is unchanged."""
        self.assertIn(".skills/progress.md", self.text)
        self.assertRegex(self.text, r"Task N: complete \(commits")


SETUP = REPO / "skills" / "setup" / "setup-repo" / "SKILL.md"
TEMPLATE = REPO / "templates" / "agents" / "project.md"
PROJECT = REPO / "docs" / "agents" / "project.md"


class SetupRepoDefaultBase(unittest.TestCase):
    def setUp(self):
        self.text = SETUP.read_text()

    def test_PCHG_10_1_decision_exists_in_the_walk(self):
        """PCHG-10.1 — a lettered decision asks for the default PR base."""
        self.assertRegex(self.text, r"### J\. Default PR base")
        self.assertRegex(self.text, r"decisions below \(A–J")

    def test_PCHG_10_2_suggestions_never_selectors(self):
        """PCHG-10.2 — topology and common names are suggestions only."""
        section = self.text.split("### J. Default PR base")[1].split("###")[0]
        self.assertIn("suggestion", section.lower())
        self.assertRegex(section, r"(?i)never (pre-)?select|no value is pre-selected")

    def test_PCHG_10_3_written_in_step_4(self):
        """PCHG-10.3 — Step 4 writes the confirmed value into project.md. Scoped
        tightly to '## 4. Write' before asserting: 'Default PR base' and
        'docs/agents/project.md' both recur elsewhere in this long file (decision
        J's own explainer paragraph names both), so an unscoped find/regex would
        pass even if Step 4 never mentioned the field."""
        start = self.text.find("## 4. Write")
        end = self.text.find("## 5. Offer the session-start hook")
        self.assertNotEqual(start, -1, "'## 4. Write' heading not found")
        self.assertNotEqual(end, -1, "'## 5. Offer the session-start hook' heading not found")
        step4 = self.text[start:end]
        self.assertIn("Default PR base", step4, "Step 4 has no Default PR base write item")
        self.assertIn("docs/agents/project.md", step4, "Step 4 item doesn't name its target file")

    def test_PCHG_10_4_template_carries_the_slot(self):
        """PCHG-10.4 — the seed template carries the field."""
        self.assertIn("Default PR base:", TEMPLATE.read_text())

    def test_PCHG_10_5_declining_writes_nothing(self):
        """PCHG-10.5 — declining leaves the field absent and defers to per-invocation
        ask. Section J is the last '###' heading in the file, so splitting on '###'
        alone bleeds all the way to EOF and would match Step 4 item 6's unrelated
        'declined' text for decision I; scope to the '## 3.' heading that actually
        closes section J."""
        start = self.text.find("### J. Default PR base")
        end = self.text.find("## 3. Draft and confirm")
        self.assertNotEqual(start, -1, "'### J. Default PR base' heading not found")
        self.assertNotEqual(end, -1, "'## 3. Draft and confirm' heading not found")
        section_j_only = self.text[start:end]
        self.assertRegex(section_j_only, r"(?i)declin\w+",
                          "decision J's own text never mentions declining")

    def test_PCHG_11_10_one_decision_at_a_time(self):
        """PCHG-11.10 — the one-at-a-time walk rule survives."""
        self.assertIn("strictly one at a time", self.text)

    def test_PCHG_11_11_additive_rule(self):
        """PCHG-11.11 — the additive write rule survives."""
        self.assertIn("existing files are edited in place, never clobbered", self.text)

    def test_PCHG_11_12_verification_gate(self):
        """PCHG-11.12 — Step 6's verification gate survives."""
        self.assertIn("Prove the configuration actually works", self.text)

    def test_PCHG_10_3_this_repo_configured(self):
        """PCHG-10.3 — this repository declares its own default PR base."""
        self.assertRegex(PROJECT.read_text(), r"\*\*Default PR base:\*\* `\w[\w./-]*`")


if __name__ == "__main__":
    unittest.main()
