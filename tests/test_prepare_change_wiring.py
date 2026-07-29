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


if __name__ == "__main__":
    unittest.main()
