"""SDPR + SDAS contract tests — product context and architecture shape First-class."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "project" / "define-system-doc"
CATALOG = SKILL / "catalog" / "CATALOG.md"
FRAME = ROOT / "skills" / "discovery" / "frame-change" / "SKILL.md"
VALIDATE = ROOT / "skills" / "acceptance" / "validate-feature" / "SKILL.md"
DESIGN = ROOT / "skills" / "spec" / "design-solution" / "SKILL.md"
DEFINE_PROJECT = ROOT / "skills" / "project" / "define-project" / "SKILL.md"
GUIDE = ROOT / "docs" / "guide" / "concepts" / "system-docs.md"

PRODUCT = ("product/personas", "product/metrics", "product/principles")
ARCH = (
    "architecture/system",
    "architecture/data",
    "architecture/integrations",
    "architecture/runtime",
)


class TestProductFirstClass(unittest.TestCase):
    def test_catalog_and_artifacts(self):
        cat = CATALOG.read_text()
        for key in PRODUCT:
            self.assertRegex(cat, rf"`{re.escape(key)}`\s*\|\s*First-class")
            short = key.split("/")[-1]
            self.assertTrue((SKILL / "templates" / "product" / f"{short}.md").is_file())
            self.assertTrue((SKILL / "validators" / "product" / f"{short}.md").is_file())
            pkg = (SKILL / "catalog" / "entries" / f"{key}.md").read_text()
            self.assertIn("frame-change", pkg)
            self.assertIn("validate-feature", pkg)

    def test_frame_change_hooks(self):
        text = FRAME.read_text()
        self.assertIn("Product context docs", text)
        self.assertIn("/define-system-doc product/", text)
        self.assertIn("NEVER", text)
        self.assertIn("auto-invoke", text.lower())

    def test_validate_feature_hooks(self):
        text = VALIDATE.read_text()
        self.assertIn("Product context docs", text)
        self.assertIn("/define-system-doc product/", text)
        self.assertIn("NEVER", text)


class TestArchitectureShapeFirstClass(unittest.TestCase):
    def test_catalog_and_artifacts(self):
        cat = CATALOG.read_text()
        for key in ARCH:
            self.assertRegex(cat, rf"`{re.escape(key)}`\s*\|\s*First-class")
            short = key.split("/")[-1]
            self.assertTrue((SKILL / "templates" / "architecture" / f"{short}.md").is_file())
            self.assertTrue((SKILL / "validators" / "architecture" / f"{short}.md").is_file())

    def test_design_solution_shape_hooks(self):
        text = DESIGN.read_text()
        self.assertIn("Architecture shape docs", text)
        self.assertIn("/define-system-doc architecture/", text)
        self.assertIn("never redefine", text.lower())
        self.assertIn("NEVER", text)

    def test_define_project_handoff(self):
        text = DEFINE_PROJECT.read_text()
        self.assertIn("define-system-doc", text)
        self.assertIn("product/personas", text)
        self.assertIn("architecture/system", text)


class TestShared(unittest.TestCase):
    def test_inventory_36(self):
        keys = re.findall(
            r"\|\s*`([^`]+)`\s*\|\s*(First-class|Recognized|Deferred)\s*\|",
            CATALOG.read_text(),
        )
        self.assertEqual(len(keys), 36)

    def test_guide_lists_entries(self):
        g = GUIDE.read_text()
        for key in PRODUCT + ARCH:
            self.assertIn(key, g)


if __name__ == "__main__":
    unittest.main()
