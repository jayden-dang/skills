"""SDST contract tests — standards core First-class + guidelines migration."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "project" / "define-system-doc"
CATALOG = SKILL / "catalog" / "CATALOG.md"
PLAN = ROOT / "skills" / "spec" / "plan-tasks" / "SKILL.md"
TEST_FIRST = ROOT / "skills" / "execution" / "test-first" / "SKILL.md"
INSPECT = ROOT / "skills" / "review" / "inspect-change" / "SKILL.md"
DEFINE_PROJECT = ROOT / "skills" / "project" / "define-project" / "SKILL.md"
GUIDE = ROOT / "docs" / "guide" / "concepts" / "system-docs.md"
GUIDELINES = ROOT / "docs" / "product" / "guidelines.md"
STD_INDEX = ROOT / "docs" / "standards" / "INDEX.md"
STD_TEST = ROOT / "docs" / "standards" / "testing.md"
STD_ERR = ROOT / "docs" / "standards" / "errors-logging.md"

KEYS = ("standards/INDEX", "standards/testing", "standards/errors-logging")


class TestStandardsFirstClass(unittest.TestCase):
    def test_catalog(self):
        cat = CATALOG.read_text()
        for key in KEYS:
            self.assertRegex(cat, rf"`{re.escape(key)}`\s*\|\s*First-class")
            short = key.split("/")[-1]
            self.assertTrue((SKILL / "templates" / "standards" / f"{short}.md").is_file())
            self.assertTrue((SKILL / "validators" / "standards" / f"{short}.md").is_file())

    def test_inventory_36(self):
        keys = re.findall(
            r"\|\s*`([^`]+)`\s*\|\s*(First-class|Recognized|Deferred)\s*\|",
            CATALOG.read_text(),
        )
        self.assertEqual(len(keys), 36)


class TestGuidelinesMigration(unittest.TestCase):
    def test_standards_ssot_exists(self):
        for p in (STD_INDEX, STD_TEST, STD_ERR):
            self.assertTrue(p.is_file(), p)
            self.assertIn("Status: Approved", p.read_text())

    def test_guidelines_is_pointer_not_parallel_body(self):
        text = GUIDELINES.read_text()
        self.assertIn("docs/standards/", text)
        self.assertIn("pointer", text.lower())
        # must not restate full coding standards body
        self.assertNotIn("SKILL.md under 500 lines", text)
        self.assertIn("Canonical standards", text)


class TestHooks(unittest.TestCase):
    def test_plan_tasks_prefers_standards(self):
        text = PLAN.read_text()
        self.assertIn("docs/standards/", text)
        self.assertIn("legacy", text.lower())
        self.assertIn("consult-recipe.md", text)
        self.assertIn("standards/INDEX", text)

    def test_test_first_testing_doc(self):
        text = TEST_FIRST.read_text()
        self.assertIn("Testing standards doc", text)
        self.assertIn("standards/testing", text)
        self.assertIn("never auto-invoke", text.lower())

    def test_inspect_change_standards_sources(self):
        text = INSPECT.read_text()
        self.assertIn("docs/standards/", text)
        self.assertIn("consult-recipe.md", text)

    def test_define_project_migration(self):
        text = DEFINE_PROJECT.read_text()
        self.assertIn("docs/standards/", text)
        self.assertIn("pointer", text.lower())


class TestGuide(unittest.TestCase):
    def test_guide_lists_standards(self):
        g = GUIDE.read_text()
        for key in KEYS:
            self.assertIn(key, g)
        self.assertIn("Guidelines migration", g)


if __name__ == "__main__":
    unittest.main()
