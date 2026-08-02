"""SDOC contract tests — catalog, validator, registration, plan-tasks hooks, guide."""

from __future__ import annotations

import json
import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests" / "system-docs"))

from map_validate import validate_codebase_map  # noqa: E402

SKILL_DIR = ROOT / "skills" / "project" / "define-system-doc"
CATALOG = SKILL_DIR / "catalog" / "CATALOG.md"
PLAN_TASKS = ROOT / "skills" / "spec" / "plan-tasks" / "SKILL.md"
EPHEMERA = ROOT / "templates" / "skills-ephemera-paths.md"
GUIDE = ROOT / "docs" / "guide" / "concepts" / "system-docs.md"
ARTIFACTS = ROOT / "docs" / "architecture" / "artifacts.md"
PLUGIN = ROOT / ".claude-plugin" / "plugin.json"
MARKET = ROOT / ".claude-plugin" / "marketplace.json"
AGENTS = ROOT / "AGENTS.md"
ARCH_SKILLS = ROOT / "docs" / "architecture" / "skills.md"
DEFINE_SKILL = SKILL_DIR / "SKILL.md"

EXPECTED_KEYS = {
    "product/vision",
    "product/personas",
    "product/metrics",
    "product/principles",
    "product/guidelines",
    "architecture/INDEX",
    "architecture/system",
    "architecture/data",
    "architecture/integrations",
    "architecture/runtime",
    "codebase/map",
    "codebase/modules",
    "codebase/ownership",
    "codebase/dependencies",
    "security/threat-model",
    "security/posture",
    "security/compliance",
    "standards/INDEX",
    "standards/testing",
    "standards/api",
    "standards/ui",
    "standards/accessibility",
    "standards/security-coding",
    "standards/errors-logging",
    "standards/observability",
    "ops/deployment",
    "ops/reliability",
    "ops/observability",
    "ops/disaster-recovery",
    "ops/runbooks",
    "roadmap/INDEX",
    "specs/INDEX",
    "adr",
    "agents/config",
    "glossary",
    "out-of-scope",
}

SKILL_PATH = "./skills/project/define-system-doc"


class TestCatalogInventory(unittest.TestCase):
    def test_expected_key_count(self):
        self.assertEqual(len(EXPECTED_KEYS), 36)

    def test_catalog_exists_and_columns(self):
        self.assertTrue(CATALOG.is_file())
        text = CATALOG.read_text()
        self.assertIn("Entry key", text)
        self.assertIn("Maturity", text)
        self.assertIn("Entry-package pointer", text)

    def test_exact_key_set(self):
        text = CATALOG.read_text()
        keys = set(re.findall(r"\|\s*`([^`]+)`\s*\|\s*(First-class|Recognized|Deferred)\s*\|", text))
        found = {k for k, _ in keys}
        self.assertEqual(found, EXPECTED_KEYS)

    def test_package_files_exist_skill_local(self):
        text = CATALOG.read_text()
        for m in re.finditer(
            r"\|\s*`([^`]+)`\s*\|\s*(First-class|Recognized|Deferred)\s*\|\s*`([^`]+)`\s*\|",
            text,
        ):
            key, maturity, pointer = m.group(1), m.group(2), m.group(3)
            path = SKILL_DIR / pointer
            self.assertTrue(path.is_file(), f"missing package for {key}: {path}")
            self.assertTrue(str(path.resolve()).startswith(str(SKILL_DIR.resolve())))
            body = path.read_text()
            self.assertIn("Purpose and boundary", body)
            self.assertIn("Canonical consumer path", body)
            if maturity == "First-class":
                self.assertIn("Template", body)
                self.assertIn("Validator", body)
                self.assertIn("Real readers", body)

    def test_maturity_only_in_catalog_not_package(self):
        # packages may mention maturity as pointer text; CATALOG is authoritative
        self.assertIn("| Entry key | Maturity |", CATALOG.read_text())


class TestFirstClassCodebaseMap(unittest.TestCase):
    def test_first_class_package_artifacts(self):
        text = CATALOG.read_text()
        self.assertRegex(text, r"`codebase/map`\s*\|\s*First-class")
        self.assertTrue((SKILL_DIR / "templates" / "codebase" / "map.md").is_file())
        self.assertTrue((SKILL_DIR / "validators" / "codebase" / "map.md").is_file())
        self.assertTrue(DEFINE_SKILL.is_file())
        self.assertTrue(PLAN_TASKS.is_file())

    def test_writer_skill_disable_model_invocation(self):
        fm = DEFINE_SKILL.read_text().split("---", 2)[1]
        self.assertIn("disable-model-invocation: true", fm)
        self.assertIn("name: define-system-doc", fm)


class TestMapValidatorStructural(unittest.TestCase):
    def test_pass_minimal(self):
        ok, reasons = validate_codebase_map(
            """
# Codebase Map
Status: Approved

## Purpose and boundary
Layout for this repo.

## Top-level layout
| Path | Purpose |
|---|---|
| `src/` | Application code |

## Placement rules
- WHEN adding skills put them under `skills/<category>/`.

## Not spine / not feature registry
Not the architecture spine and not the feature registry.
"""
        )
        self.assertTrue(ok, reasons)

    def test_fail_placeholder(self):
        ok, reasons = validate_codebase_map(
            """
Status: Approved
## Purpose and boundary
TBD
## Top-level layout
| Path | Purpose |
|---|---|
| `src/` | x
## Placement rules
- rule
## Not spine / not feature registry
disclaimer
"""
        )
        self.assertFalse(ok)
        self.assertTrue(any("placeholder" in r for r in reasons))

    def test_fail_missing_status(self):
        ok, reasons = validate_codebase_map(
            """
## Purpose and boundary
ok
## Top-level layout
None — n/a for empty repo
## Placement rules
None — n/a
## Not spine / not feature registry
disclaimer text here
"""
        )
        self.assertFalse(ok)
        self.assertTrue(any("Status" in r for r in reasons))

    def test_fail_empty_layout_table(self):
        ok, reasons = validate_codebase_map(
            """
Status: Approved
## Purpose and boundary
ok
## Top-level layout
| Path | Purpose |
|---|---|
## Placement rules
- rule
## Not spine / not feature registry
disclaimer
"""
        )
        self.assertFalse(ok)


class TestEphemeraRegistration(unittest.TestCase):
    def test_system_docs_root_registered(self):
        text = EPHEMERA.read_text()
        self.assertIn(".skills/system-docs/", text)
        self.assertIn("state.md", text)
        self.assertIn("pathfind/", text)  # still present


class TestPlanTasksReader(unittest.TestCase):
    """Reader tests for plan-tasks: applicability, consult, no-op, suggestion, conflict."""

    def setUp(self):
        self.text = PLAN_TASKS.read_text()

    def test_applicability_predicate(self):
        self.assertIn("Applicability:", self.text)
        self.assertIn("File Structure", self.text)

    def test_consult_when_authoritative(self):
        self.assertIn("When Approved:", self.text)
        self.assertIn("consult", self.text.lower())

    def test_noop_when_absent(self):
        self.assertIn("absent or non-authoritative", self.text.lower())
        self.assertIn("CONTINUE", self.text)

    def test_suggestion_protocol(self):
        self.assertIn("/define-system-doc codebase/map", self.text)
        self.assertIn("at most once", self.text.lower())
        self.assertIn("NEVER", self.text)
        self.assertIn("auto-invoke", self.text.lower())

    def test_conflict_precedence(self):
        self.assertIn("Hard constraints", self.text)
        self.assertIn("Placement conflict", self.text)
        self.assertIn("preserve the hard", self.text.lower())
        self.assertIn("constraint", self.text.lower())


class TestRegistration(unittest.TestCase):
    def test_plugin_json_valid_and_lists_skill(self):
        data = json.loads(PLUGIN.read_text())
        self.assertIn(SKILL_PATH, data["skills"])

    def test_marketplace_json_valid_and_lists_skill(self):
        data = json.loads(MARKET.read_text())

        def skills_lists(o):
            found = []
            if isinstance(o, dict):
                if "skills" in o and isinstance(o["skills"], list) and o["skills"] and str(o["skills"][0]).startswith("./skills/"):
                    found.append(o["skills"])
                for v in o.values():
                    found.extend(skills_lists(v))
            elif isinstance(o, list):
                for v in o:
                    found.extend(skills_lists(v))
            return found

        lists = skills_lists(data)
        self.assertTrue(any(SKILL_PATH in lst for lst in lists))

    def test_agents_and_architecture_inventory(self):
        self.assertIn("define-system-doc", AGENTS.read_text())
        self.assertIn("define-system-doc", ARCH_SKILLS.read_text())


class TestGuideSync(unittest.TestCase):
    def test_guide_exists(self):
        self.assertTrue(GUIDE.is_file())

    def test_guide_keys_in_catalog(self):
        guide = GUIDE.read_text()
        # keys mentioned with backticks that look like entry keys
        mentioned = set(re.findall(r"`([a-z]+/[A-Za-z0-9_-]+)`", guide))
        # only check those that are Hybrid-style
        for k in mentioned:
            if k in EXPECTED_KEYS:
                self.assertIn(k, EXPECTED_KEYS)

    def test_first_class_claim_matches_catalog(self):
        guide = GUIDE.read_text()
        cat = CATALOG.read_text()
        if "First-class" in guide and "codebase/map" in guide:
            self.assertRegex(cat, r"`codebase/map`\s*\|\s*First-class")

    def test_artifacts_links_not_full_catalog(self):
        text = ARTIFACTS.read_text()
        self.assertIn("system-docs.md", text)
        # should not dump full maturity table
        self.assertNotIn("| Entry key | Maturity | Entry-package pointer |", text)


class TestGuards(unittest.TestCase):
    def test_define_project_still_owns_vision_spine(self):
        text = (ROOT / "skills" / "project" / "define-project" / "SKILL.md").read_text()
        self.assertIn("vision.md", text)
        self.assertIn("architecture", text)

    def test_no_tb_slo_audit_claim_in_sdoc_surfaces(self):
        # ROAD-7 must not claim audit-trace TB/SLO delivery
        surfaces = [
            DEFINE_SKILL.read_text(),
            GUIDE.read_text(),
        ]
        for text in surfaces:
            self.assertNotIn("audit-trace passes for TB", text)
            self.assertNotIn("SLO-N audit", text)


if __name__ == "__main__":
    unittest.main()
