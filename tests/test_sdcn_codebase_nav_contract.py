"""SDCN contract tests — modules/ownership/dependencies First-class + reader hooks."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "project" / "define-system-doc"
CATALOG = SKILL / "catalog" / "CATALOG.md"
PLAN = ROOT / "skills" / "spec" / "plan-tasks" / "SKILL.md"
DESIGN = ROOT / "skills" / "spec" / "design-solution" / "SKILL.md"
INSPECT = ROOT / "skills" / "review" / "inspect-change" / "SKILL.md"
GUIDE = ROOT / "docs" / "guide" / "concepts" / "system-docs.md"

NAV_KEYS = ("codebase/modules", "codebase/ownership", "codebase/dependencies")


class TestFirstClassNavEntries(unittest.TestCase):
    def test_catalog_first_class(self):
        text = CATALOG.read_text()
        for key in NAV_KEYS:
            self.assertRegex(text, rf"`{re.escape(key)}`\s*\|\s*First-class")

    def test_templates_and_validators_exist(self):
        for key in NAV_KEYS:
            short = key.split("/")[-1]
            self.assertTrue((SKILL / "templates" / "codebase" / f"{short}.md").is_file())
            self.assertTrue((SKILL / "validators" / "codebase" / f"{short}.md").is_file())
            pkg = SKILL / "catalog" / "entries" / f"{key}.md"
            body = pkg.read_text()
            self.assertIn("templates/codebase/", body)
            self.assertIn("validators/codebase/", body)
            self.assertIn("plan-tasks", body)
            self.assertIn("design-solution", body)
            self.assertIn("inspect-change", body)

    def test_inventory_still_36(self):
        text = CATALOG.read_text()
        keys = set(
            re.findall(
                r"\|\s*`([^`]+)`\s*\|\s*(First-class|Recognized|Deferred)\s*\|",
                text,
            )
        )
        self.assertEqual(len(keys), 36)


class TestPlanTasksNavReader(unittest.TestCase):
    def setUp(self):
        self.text = PLAN.read_text()

    def test_applicability_and_entries(self):
        self.assertIn("System docs consult during File Structure", self.text)
        self.assertIn("consult-recipe.md", self.text)
        for key in NAV_KEYS:
            self.assertIn(key, self.text)

    def test_consult_noop_suggest(self):
        self.assertIn("absent", self.text.lower())
        self.assertIn("codebase/modules", self.text)
        self.assertIn("auto-invoke", self.text.lower())

    def test_hard_constraints_outrank(self):
        self.assertIn("hard constraint", self.text.lower())


class TestDesignSolutionNavReader(unittest.TestCase):
    def setUp(self):
        self.text = DESIGN.read_text()

    def test_applicability(self):
        self.assertIn("Optional system docs (consult recipe)", self.text)
        self.assertIn("cross-module", self.text)

    def test_consult_noop_suggest_no_auto(self):
        self.assertIn("consult-recipe.md", self.text)
        self.assertIn("modules,ownership,dependencies", self.text.replace(" ", "") or "modules" in self.text)
        self.assertIn("/define-system-doc", self.text)
        self.assertIn("never auto-invoke", self.text.lower())


class TestInspectChangeNavReader(unittest.TestCase):
    def setUp(self):
        self.text = INSPECT.read_text()

    def test_section_present(self):
        self.assertIn("Codebase navigation docs", self.text)
        self.assertIn("3c.", self.text)
        self.assertIn("consult-recipe.md", self.text)

    def test_advisory_and_no_auto(self):
        self.assertIn("advisory", self.text.lower())
        self.assertIn("auto-invoke", self.text.lower())
        self.assertIn("access-control", self.text.lower())


class TestGuideNav(unittest.TestCase):
    def test_guide_lists_nav_entries(self):
        text = GUIDE.read_text()
        for key in NAV_KEYS:
            self.assertIn(key, text)
        self.assertIn("design-solution", text)
        self.assertIn("inspect-change", text)


if __name__ == "__main__":
    unittest.main()
