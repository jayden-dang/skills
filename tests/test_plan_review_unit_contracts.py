"""Contracts for plan-level review: Execution-mode field; no dead Risk/HRO slots."""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WRITE_PLAN = REPO / "skills" / "spec" / "plan-tasks" / "SKILL.md"
TASKS_TPL = REPO / "templates" / "tasks.md"
WRITE_REQ = REPO / "skills" / "spec" / "specify-behavior" / "SKILL.md"
REQ_TPL = REPO / "templates" / "requirements.md"
EXECUTE = REPO / "skills" / "execution" / "build-in-waves" / "SKILL.md"
STORY_UNIT = REPO / "skills" / "execution" / "build-by-story" / "story-unit-mode.md"
BUILD_BY_STORY = REPO / "skills" / "execution" / "build-by-story" / "SKILL.md"
FINISH = REPO / "skills" / "ship" / "land-branch" / "SKILL.md"
AGENTS = REPO / "AGENTS.md"


class WritePlanContracts(unittest.TestCase):
    def setUp(self):
        self.wp = WRITE_PLAN.read_text()
        self.tpl = TASKS_TPL.read_text()

    def test_execution_mode_required_header(self):
        self.assertIn("Execution-mode:", self.wp)
        self.assertIn("Execution-mode:", self.tpl)
        self.assertRegex(self.wp, r"continuous.*story-unit|story-unit.*continuous")
        # Empty mode blocks Approved
        self.assertRegex(
            self.wp,
            r"Execution-mode.*(Approved|approval)|Status: Approved.*Execution-mode",
            msg="skill must tie Execution-mode to plan approval",
        )

    def test_no_risk_decision_surface_or_human_review_order(self):
        # Template must not pre-print dead slots (agents fill templates).
        self.assertNotIn("**Risk:**", self.tpl)
        self.assertNotIn("**Decision surface:**", self.tpl)
        self.assertNotIn("## Human review order", self.tpl)
        # Skill must not list them as REQUIRED task slots.
        self.assertNotRegex(
            self.wp,
            r"Every slot in a task block[^\n]*Risk",
        )
        self.assertNotIn("## Human review order", self.wp)


class WriteRequirementsContracts(unittest.TestCase):
    def setUp(self):
        self.wr = WRITE_REQ.read_text()
        self.tpl = REQ_TPL.read_text()

    def test_nfr_section_kind_in_template_and_skill(self):
        self.assertIn("**Section-kind:** nfr", self.tpl)
        self.assertIn("Section-kind", self.wr)
        self.assertRegex(self.wr, r"(?i)absent\s*=\s*story")

    def test_story_quality_approval_gate(self):
        self.assertRegex(
            self.wr,
            r"demoable act|one demoable|ONE demoable",
            msg="story quality bar missing",
        )
        self.assertRegex(
            self.wr,
            r"Status: Approved|refuse.*Approved|Approved.*confirm",
            msg="approval gate must own story quality",
        )


class ExecutePlanContracts(unittest.TestCase):
    def setUp(self):
        self.ep = EXECUTE.read_text()
        self.su = STORY_UNIT.read_text() if STORY_UNIT.is_file() else ""

    def test_story_unit_mode_and_preflight(self):
        # continuous skill hands off story-unit; recipes live under build-by-story
        self.assertIn("story-unit", self.ep)
        self.assertIn("Execution-mode", self.ep)
        self.assertIn("build-by-story", self.ep)
        bbs = BUILD_BY_STORY.read_text()
        self.assertIn("story-unit-mode.md", bbs)
        self.assertTrue(STORY_UNIT.is_file(), "recipe must live beside build-by-story")
        self.assertIn("Derive partition", self.su)
        self.assertIn("Unit table", self.su)

    def test_unit_barrier_and_unit_review(self):
        self.assertRegex(self.su, r"Unit <k>: complete|Unit .*complete")
        self.assertRegex(self.su, r"task-reviewer|unit scope")
        self.assertRegex(self.su, re.compile(r"chat-only is\s+not a mode change", re.I))

    def test_finish_branch_risk_recipe(self):
        text = FINISH.read_text()
        self.assertIn("risk glob", text)
        self.assertIn("multi_task", text)
        self.assertIn("risk_hit", text)
        self.assertIn("**Done when:**", text)


class AgentsContracts(unittest.TestCase):
    def test_agents_does_not_require_human_review_order(self):
        text = AGENTS.read_text()
        # May mention history; must not list Human review order as a live required task slot
        self.assertNotRegex(
            text,
            r"Human review order.*REQUIRED|REQUIRED.*Human review order",
        )


if __name__ == "__main__":
    unittest.main()
