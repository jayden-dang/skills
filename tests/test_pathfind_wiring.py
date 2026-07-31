"""pathfind registration and neighbor wiring contracts.

PFIND-1.1 registration; later tasks extend neighbor assertions.
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "discovery" / "pathfind" / "SKILL.md"
AGENTS = REPO / "AGENTS.md"
README = REPO / "README.md"
PLUGIN = REPO / ".claude-plugin" / "plugin.json"
MARKET = REPO / ".claude-plugin" / "marketplace.json"


TEMPLATE_TRACKER = REPO / "templates" / "agents" / "issue-tracker.md"
DOCS_TRACKER = REPO / "docs" / "agents" / "issue-tracker.md"


class PathfindTrackerSeeds(unittest.TestCase):
    def test_PFIND_6_1_6_3_pathfind_ops_in_templates(self):
        """PFIND-6.1 PFIND-6.3 — Pathfind operations seeded; skill reads issue-tracker.md."""
        for path in (TEMPLATE_TRACKER, DOCS_TRACKER):
            text = path.read_text()
            self.assertIn("Pathfind operations", text, f"{path} missing Pathfind operations")
            self.assertIn("pathfind:map", text)
            self.assertIn("pathfind:clarify", text)
            self.assertRegex(text, r"(?i)frontier|claim|block", msg=str(path))
        skill = SKILL.read_text()
        self.assertIn("docs/agents/issue-tracker.md", skill)


class PathfindRegistration(unittest.TestCase):
    def test_PFIND_1_1_skill_file_exists_and_user_invoked(self):
        """PFIND-1.1 — skill exists under discovery/pathfind with disable-model-invocation."""
        self.assertTrue(SKILL.exists(), "skills/discovery/pathfind/SKILL.md missing")
        text = SKILL.read_text()
        self.assertIn("name: pathfind", text)
        self.assertIn("disable-model-invocation: true", text)

    def test_PFIND_1_1_registered_in_both_manifests(self):
        """PFIND-1.1 — plugin and marketplace list the skill path."""
        for manifest in (PLUGIN, MARKET):
            body = manifest.read_text()
            self.assertIn("./skills/discovery/pathfind", body, f"{manifest.name} missing pathfind")
            json.loads(body)

    def test_PFIND_1_1_named_in_agents_and_readme(self):
        """PFIND-1.1 — roster documents name pathfind as user-invoked discovery skill."""
        agents = AGENTS.read_text()
        readme = README.read_text()
        self.assertIn("pathfind", agents)
        self.assertIn("pathfind", readme)
        # User-invoked list or discovery row should mark it (U) or list under user-invoked
        self.assertTrue(
            re.search(r"pathfind.*\(U\)|`pathfind`.*user-invoked|user-invoked.*pathfind", agents, re.I)
            or ("pathfind" in agents and "disable-model-invocation" in SKILL.read_text()),
            "pathfind should appear as user-invoked in AGENTS.md inventory",
        )

    def test_PFIND_1_1_iron_laws_survive(self):
        """Guard — AGENTS.md Iron Laws survive registration edit."""
        agents = AGENTS.read_text()
        for law in ("Gate 1 — NO-CODE", "Gate 2 — TEST-FIRST", "Gate 3 — ROOT-CAUSE", "Gate 4 — EVIDENCE"):
            self.assertIn(law, agents)


if __name__ == "__main__":
    unittest.main()
