"""Author-skills quality contracts for system-docs-related skill text.

RED/GREEN: structural + wording quality gates for skills touched by Hybrid 1A work.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DSD = ROOT / "skills" / "project" / "define-system-doc"
RECIPE = DSD / "consult-recipe.md"
DSD_SKILL = DSD / "SKILL.md"

CONSUMERS = [
    ROOT / "skills" / "spec" / "plan-tasks" / "SKILL.md",
    ROOT / "skills" / "spec" / "design-solution" / "SKILL.md",
    ROOT / "skills" / "discovery" / "frame-change" / "SKILL.md",
    ROOT / "skills" / "review" / "inspect-change" / "SKILL.md",
    ROOT / "skills" / "acceptance" / "validate-feature" / "SKILL.md",
    ROOT / "skills" / "acceptance" / "validate-api" / "SKILL.md",
    ROOT / "skills" / "acceptance" / "validate-ui" / "SKILL.md",
    ROOT / "skills" / "execution" / "test-first" / "SKILL.md",
    ROOT / "skills" / "execution" / "root-cause" / "SKILL.md",
    ROOT / "skills" / "ship" / "cut-release" / "SKILL.md",
]


def _frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return ""
    return text.split("---", 2)[1]


class TestDefineSystemDocAuthorQuality(unittest.TestCase):
    def test_user_invoked_description_is_plain_deliverable_line(self):
        fm = _frontmatter(DSD_SKILL.read_text())
        self.assertIn("disable-model-invocation: true", fm)
        # Human-facing deliverable; not a model trigger pack of "Use when… or when…"
        self.assertIn("Authors or updates one Hybrid 1A", fm)
        self.assertNotIn("or when a consumer skill names", fm)
        self.assertIn("/define-system-doc", fm)

    def test_has_iron_law_rationalizations_red_flags(self):
        text = DSD_SKILL.read_text()
        self.assertIn("## The Iron Law", text)
        self.assertIn("## Rationalizations", text)
        self.assertIn("## Red Flags", text)
        self.assertIn("NEVER SEED AN EMPTY", text)

    def test_authority_is_general_not_map_only(self):
        text = DSD_SKILL.read_text()
        self.assertIn("## Authority", text)
        # must not title authority as codebase/map only
        self.assertNotIn("## Authority (codebase/map)", text)
        self.assertIn("entry package may specialize", text.lower() or "specialize" in text.lower())
        self.assertTrue(
            "entry package" in text.lower() and "Approved" in text
        )

    def test_consult_recipe_exists_and_is_one_home(self):
        self.assertTrue(RECIPE.is_file())
        r = RECIPE.read_text()
        self.assertIn("one home", r.lower())
        self.assertIn("NEVER auto-invoke", r)
        self.assertIn("Hard constraints outrank", r)


class TestConsumerConsultPointers(unittest.TestCase):
    def test_consumers_point_at_recipe_not_required_subskill_user_skill(self):
        for path in CONSUMERS:
            text = path.read_text()
            # no dead-end handoff
            self.assertIsNone(
                re.search(r"REQUIRED SUB-SKILL:.*define-system-doc", text),
                f"{path} must not REQUIRED SUB-SKILL user-invoked define-system-doc",
            )
            if "define-system-doc" in text or "system-doc" in text.lower():
                self.assertIn(
                    "consult-recipe.md",
                    text,
                    f"{path} should point at consult-recipe.md when consulting system docs",
                )

    def test_frame_change_product_section_not_glued_to_scan(self):
        text = (ROOT / "skills" / "discovery" / "frame-change" / "SKILL.md").read_text()
        # product context must close before the heavier scan paragraph
        self.assertIn("### Product context docs (optional)", text)
        self.assertIn("consult-recipe.md", text)
        # the scan subagent sentence must stand as its own paragraph start
        self.assertIn("For anything heavier", text)
        # must not append scan text onto NEVER auto-invoke line without break
        bad = re.search(
            r"auto-invoke `define-system-doc` \(ARCH-5\)\. For anything heavier",
            text,
        )
        self.assertIsNone(bad, "product context was glued to scan paragraph")

    def test_plan_tasks_has_unified_system_docs_section(self):
        text = (ROOT / "skills" / "spec" / "plan-tasks" / "SKILL.md").read_text()
        self.assertIn("System docs consult during File Structure", text)
        self.assertIn("consult-recipe.md", text)
        # old verbose multi-headers should be gone
        self.assertNotIn("### Codebase Map consult (optional system-doc)", text)
        self.assertNotIn("### Engineering standards docs (optional)", text)

    def test_design_solution_unified_optional_table(self):
        text = (ROOT / "skills" / "spec" / "design-solution" / "SKILL.md").read_text()
        self.assertIn("### Optional system docs (consult recipe)", text)
        self.assertIn("consult-recipe.md", text)
        self.assertNotIn("### Security and reliability standing docs (optional)", text)
        self.assertNotIn("### Codebase navigation docs (optional)", text)

    def test_root_cause_still_protects_red_loop(self):
        text = (ROOT / "skills" / "execution" / "root-cause" / "SKILL.md").read_text()
        self.assertIn("never replaces the red loop", text.lower() or "red loop" in text.lower())
        self.assertIn("Only after Phase 2", text)
        self.assertIn("consult-recipe.md", text)


class TestNoNewRationalizationHoles(unittest.TestCase):
    def test_cut_release_deployment_not_replace_commands(self):
        text = (ROOT / "skills" / "ship" / "cut-release" / "SKILL.md").read_text()
        self.assertIn("MUST NOT replace", text)
        self.assertIn("project.md", text)
        self.assertIn("consult-recipe.md", text)

    def test_consumers_name_exact_suggest_slash_command(self):
        """Suggestion protocol: name /define-system-doc <entry-key>, not bare prose."""
        must_name = [
            ROOT / "skills" / "discovery" / "frame-change" / "SKILL.md",
            ROOT / "skills" / "acceptance" / "validate-feature" / "SKILL.md",
            ROOT / "skills" / "acceptance" / "validate-api" / "SKILL.md",
            ROOT / "skills" / "acceptance" / "validate-ui" / "SKILL.md",
            ROOT / "skills" / "execution" / "test-first" / "SKILL.md",
            ROOT / "skills" / "execution" / "root-cause" / "SKILL.md",
            ROOT / "skills" / "review" / "inspect-change" / "SKILL.md",
        ]
        for path in must_name:
            text = path.read_text()
            self.assertIn(
                "/define-system-doc",
                text,
                f"{path.name}: must name the exact /define-system-doc suggest action",
            )
            self.assertIn("never auto-invoke", text.lower())


if __name__ == "__main__":
    unittest.main()
