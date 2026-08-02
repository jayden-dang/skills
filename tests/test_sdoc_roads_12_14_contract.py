"""ROAD-12/13/14 + full Hybrid 1A First-class completion contracts."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "project" / "define-system-doc"
CATALOG = SKILL / "catalog" / "CATALOG.md"
AUDIT = ROOT / "skills" / "execution" / "audit-trace" / "SKILL.md"
DESIGN = ROOT / "skills" / "spec" / "design-solution" / "SKILL.md"
ROOT_CAUSE = ROOT / "skills" / "execution" / "root-cause" / "SKILL.md"
CUT = ROOT / "skills" / "ship" / "cut-release" / "SKILL.md"
VAPI = ROOT / "skills" / "acceptance" / "validate-api" / "SKILL.md"
VUI = ROOT / "skills" / "acceptance" / "validate-ui" / "SKILL.md"
GUIDE = ROOT / "docs" / "guide" / "concepts" / "system-docs.md"

SURFACE = (
    "standards/api",
    "standards/ui",
    "standards/accessibility",
    "standards/security-coding",
    "standards/observability",
)
SECURITY = ("security/threat-model", "security/posture", "security/compliance")
OPS = (
    "ops/deployment",
    "ops/reliability",
    "ops/observability",
    "ops/disaster-recovery",
    "ops/runbooks",
)


class TestAllHybrid1AFirstClass(unittest.TestCase):
    def test_all_36_first_class(self):
        text = CATALOG.read_text()
        rows = re.findall(
            r"\|\s*`([^`]+)`\s*\|\s*(First-class|Recognized|Deferred)\s*\|",
            text,
        )
        self.assertEqual(len(rows), 36)
        for key, mat in rows:
            self.assertEqual(mat, "First-class", f"{key} is {mat}")


class TestSurfaceStandards(unittest.TestCase):
    def test_packages_and_templates(self):
        for key in SURFACE:
            short = key.split("/")[-1]
            self.assertTrue((SKILL / "templates" / "standards" / f"{short}.md").is_file())
            self.assertTrue((SKILL / "validators" / "standards" / f"{short}.md").is_file())
            self.assertRegex(CATALOG.read_text(), rf"`{re.escape(key)}`\s*\|\s*First-class")

    def test_validate_api_ui_hooks(self):
        api = VAPI.read_text()
        ui = VUI.read_text()
        self.assertIn("standards/api", api)
        self.assertIn("/define-system-doc standards/api", api)
        self.assertIn("consult-recipe.md", api)
        self.assertIn("never auto-invoke", api.lower())
        self.assertIn("standards/ui", ui)
        self.assertIn("accessibility", ui)
        self.assertIn("/define-system-doc standards/", ui)
        self.assertIn("never auto-invoke", ui.lower())


class TestSecurityAndIds(unittest.TestCase):
    def test_security_packages(self):
        for key in SECURITY:
            short = key.split("/")[-1]
            self.assertTrue((SKILL / "templates" / "security" / f"{short}.md").is_file())
            self.assertRegex(CATALOG.read_text(), rf"`{re.escape(key)}`\s*\|\s*First-class")

    def test_design_security_reliability_fields(self):
        text = DESIGN.read_text()
        self.assertIn("`Security:`", text)
        self.assertIn("`Reliability:`", text)
        self.assertIn("TB-N", text)
        self.assertIn("SLO-N", text)
        self.assertIn("ARCH-only", text)

    def test_audit_trace_system_ids(self):
        text = AUDIT.read_text()
        for code in ("E6", "E7", "E8", "E9", "E10"):
            self.assertIn(f"**{code}**", text)
        self.assertIn("Security:", text)
        self.assertIn("Reliability:", text)
        self.assertIn("TB-N", text)
        self.assertIn("SLO-N", text)
        self.assertIn("live system ID", text)
        self.assertIn("uncited", text)


class TestOps(unittest.TestCase):
    def test_ops_packages(self):
        for key in OPS:
            short = key.split("/")[-1]
            self.assertTrue((SKILL / "templates" / "ops" / f"{short}.md").is_file())
            self.assertRegex(CATALOG.read_text(), rf"`{re.escape(key)}`\s*\|\s*First-class")

    def test_root_cause_after_phase2(self):
        text = ROOT_CAUSE.read_text()
        self.assertIn("Only after Phase 2", text)
        self.assertIn("ops/runbooks", text)
        self.assertIn("consult-recipe.md", text)
        self.assertIn("red loop", text.lower())

    def test_cut_release_deployment_narrative(self):
        text = CUT.read_text()
        self.assertIn("ops/deployment", text)
        self.assertIn("MUST NOT replace", text)
        self.assertIn("project.md", text)
        self.assertIn("consult-recipe.md", text)


class TestGuideComplete(unittest.TestCase):
    def test_guide_mentions_system_ids_and_all_first_class(self):
        g = GUIDE.read_text()
        self.assertIn("All 36 Hybrid 1A catalog rows are First-class", g)
        self.assertIn("TB-N", g)
        self.assertIn("SLO-N", g)
        self.assertIn("E6", g)


if __name__ == "__main__":
    unittest.main()
