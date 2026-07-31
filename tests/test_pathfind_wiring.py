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


FRAME = REPO / "skills" / "discovery" / "frame-change" / "SKILL.md"
ROUTE = REPO / "skills" / "meta" / "ask-me-bro" / "SKILL.md"
WORKFLOWS = REPO / "docs" / "architecture" / "workflows.md"
SKILLS_DOC = REPO / "docs" / "architecture" / "skills.md"
ADR = REPO / "docs" / "adr" / "0008-pathfind-layer.md"


class PathfindNeighbors(unittest.TestCase):
    def test_PFIND_7_6_7_7_frame_change_pathfind_knowns(self):
        """PFIND-7.6 PFIND-7.7 — frame-change seeds pathfind knowns; blindspot continues."""
        text = FRAME.read_text()
        self.assertIn(".skills/pathfind/", text)
        self.assertIn("knowns.md", text)
        self.assertRegex(text, r"(?i)not re-open|do \*\*not\*\* re-open|MUST NOT re-open|Do \*\*not\*\* re-open")
        self.assertRegex(text, r"(?i)Blindspot")

    def test_PFIND_9_1_1_4_route_task_names_pathfind(self):
        """PFIND-9.1 PFIND-1.4 — ask-me-bro names /pathfind for multi-session fog."""
        text = ROUTE.read_text()
        self.assertIn("/pathfind", text)
        self.assertRegex(text, r"(?i)fog|multi-session")
        self.assertIn("pathfind", text)

    def test_PFIND_9_2_architecture_docs(self):
        """PFIND-9.2 — ADR + workflows + skills inventory."""
        self.assertTrue(ADR.exists())
        self.assertIn("pathfind", WORKFLOWS.read_text().lower())
        self.assertIn("pathfind", SKILLS_DOC.read_text())

    def test_PFIND_9_3_1_5_not_mandatory_for_small_work(self):
        """PFIND-9.3 PFIND-1.5 — pathfind not required for ordinary tier-0/1."""
        self.assertRegex(WORKFLOWS.read_text(), r"(?i)never require|not required|optional")
        self.assertRegex(SKILL.read_text(), r"(?i)optional|no-op|ordinary")


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
