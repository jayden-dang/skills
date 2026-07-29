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


if __name__ == "__main__":
    unittest.main()
