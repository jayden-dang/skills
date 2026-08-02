"""DOSP — docs-only spine source contracts (pack product fixtures).

Greppable requirement tokens for pack fixtures: DOSP-1.1 DOSP-1.2 DOSP-1.3
DOSP-1.4 DOSP-1.5 DOSP-1.6 DOSP-6.3 DOSP-7.1 DOSP-7.2 (and later tasks add more).
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AUDIT_TRACE = REPO / "skills" / "execution" / "audit-trace" / "SKILL.md"
SCENARIOS = REPO / "tests" / "docs-only-spine" / "scenarios.md"
PRESSURE = REPO / "tests" / "docs-only-spine" / "scenarios-pressure.md"

# Task 1 finding set after reshape (no E2)
DOCS_ONLY_FINDINGS = ("E1", "E3", "E4", "E5", "W1", "W2", "W3")


PLAN_TASKS = REPO / "skills" / "spec" / "plan-tasks" / "SKILL.md"
TEMPLATES_TASKS = REPO / "templates" / "tasks.md"
TEST_FIRST = REPO / "skills" / "execution" / "test-first" / "SKILL.md"
IMPLEMENTER = (
    REPO / "skills" / "execution" / "build-in-waves" / "implementer-prompt.md"
)
REVIEWER = (
    REPO / "skills" / "execution" / "build-in-waves" / "task-reviewer-prompt.md"
)
BUILD_INLINE = REPO / "skills" / "execution" / "build-inline" / "SKILL.md"


class DospPlanExecuteNoIdInCode(unittest.TestCase):
    """DOSP-2.1 DOSP-2.2 DOSP-3.1 DOSP-3.3 DOSP-4.1 DOSP-4.2 DOSP-6.2"""

    def test_plan_tasks_no_implements_or_test_annotation_mandate(self) -> None:
        text = PLAN_TASKS.read_text()
        self.assertNotIn("`Implements: CODE-N.M` trailer", text)
        self.assertNotIn("fails **E2**", text)
        self.assertNotIn("**test annotation** inside some task's steps", text)
        self.assertIn("task footer", text.lower())

    def test_templates_tasks_no_implements_trailer(self) -> None:
        text = TEMPLATES_TASKS.read_text()
        self.assertNotIn("Implements:", text)

    def test_test_first_no_mandatory_annotation_table(self) -> None:
        text = TEST_FIRST.read_text()
        self.assertNotIn("/// REQ: CODE-N.M", text)
        self.assertIn("docs-only", text.lower())

    def test_implementer_comment_and_no_id_in_code(self) -> None:
        text = IMPLEMENTER.read_text()
        self.assertNotIn("every test carries its requirement ID", text)
        self.assertNotIn("Implements: [CODE]-N.M", text)
        self.assertIn("zero", text.lower())
        self.assertIn("feature code", text.lower())

    def test_reviewer_spec_walk_without_test_id_mandate(self) -> None:
        text = REVIEWER.read_text()
        self.assertIn("requirement IDs", text)
        self.assertNotIn("Does each carry its requirement ID?", text)

    def test_build_inline_no_trailer_or_id_tag_mandate(self) -> None:
        text = BUILD_INLINE.read_text()
        self.assertNotIn("Implements: CODE-N.M", text)
        self.assertNotIn(
            "Every test carries its requirement ID per `docs/agents/project.md`",
            text,
        )


PACKAGE_CHANGE = REPO / "skills" / "ship" / "package-change" / "SKILL.md"
CUT_RELEASE = REPO / "skills" / "ship" / "cut-release" / "SKILL.md"
POLISH = REPO / "skills" / "review" / "polish-diff" / "SKILL.md"
GUIDELINES = REPO / "docs" / "product" / "guidelines.md"
AGENTS = REPO / "AGENTS.md"
ARCH_INDEX = REPO / "docs" / "architecture" / "INDEX.md"
REALIGN = REPO / "skills" / "track" / "realign-spec" / "SKILL.md"
PROVE = REPO / "skills" / "execution" / "prove-claim" / "SKILL.md"
LOAD_SUB = REPO / "skills" / "execution" / "load-subgraph" / "SKILL.md"
CONFIGURE = REPO / "skills" / "setup" / "configure-repo" / "SKILL.md"


class DospShipAndDoctrine(unittest.TestCase):
    """DOSP-2.3 DOSP-2.4 DOSP-2.5 DOSP-3.2 DOSP-3.4 DOSP-4.3 DOSP-4.4 DOSP-5.* DOSP-6.1"""

    def test_package_change_no_required_implements_trailers(self) -> None:
        text = PACKAGE_CHANGE.read_text()
        self.assertNotIn(
            "Place requirement and\n   feature IDs only in `Implements:`",
            text,
        )
        self.assertIn("docs/specs", text)

    def test_cut_release_no_trailer_parse(self) -> None:
        text = CUT_RELEASE.read_text()
        self.assertNotIn("Group commits by their requirement-ID trailers", text)
        self.assertIn("docs/specs", text)

    def test_polish_and_guidelines_comments(self) -> None:
        self.assertIn("Comment discipline", POLISH.read_text())
        # Comment house rule lives in standards SSOT after ROAD-11 migration;
        # guidelines.md is a pointer only.
        standards = (REPO / "docs" / "standards" / "INDEX.md").read_text()
        self.assertIn("Comments (default zero)", standards)
        self.assertIn("docs/standards/", GUIDELINES.read_text())

    def test_agents_docs_only_spine(self) -> None:
        text = AGENTS.read_text()
        self.assertIn("docs-only", text.lower())
        self.assertNotIn("| Playwright test |", text)
        self.assertNotIn("| Commit message | `Implements:", text)

    def test_arch4_docs_side(self) -> None:
        text = ARCH_INDEX.read_text()
        self.assertIn("docs-side", text)
        self.assertIn("MUST NOT be required to embed", text)

    def test_realign_implemented_without_test_grep(self) -> None:
        text = REALIGN.read_text()
        self.assertNotIn("covered by a test", text)
        self.assertIn("docs-only audit-trace", text)

    def test_prove_claim_docs_only(self) -> None:
        text = PROVE.read_text()
        self.assertIn("docs-only audit-trace", text)

    def test_load_subgraph_still_present(self) -> None:
        self.assertTrue(LOAD_SUB.is_file())
        self.assertIn("load-subgraph", LOAD_SUB.read_text())

    def test_configure_repo_no_annotation_mandate(self) -> None:
        text = CONFIGURE.read_text()
        self.assertNotIn("every test carries the requirement ID it covers", text)
        self.assertIn("docs-only", text.lower())


class DospAuditTraceDocsOnly(unittest.TestCase):
    def setUp(self) -> None:
        self.text = AUDIT_TRACE.read_text()

    def test_DOSP_1_3_no_E2_in_finding_table(self) -> None:
        """DOSP-1.3 — E2 retired; no covering-test error code."""
        # Table row form **E2** must not appear as a finding code definition
        self.assertIsNone(
            re.search(r"\|\s*\*\*E2\*\*\s*\|", self.text),
            "audit-trace still defines finding **E2**",
        )
        # Must not reintroduce E2 as an active error rule
        self.assertNotIn(
            "not in `testCovered`",
            self.text,
        )

    def test_DOSP_1_1_1_2_no_test_coverage_pass(self) -> None:
        """DOSP-1.1 DOSP-1.2 — no pass that greps test/app trees for IDs."""
        self.assertNotIn("**4. Test coverage**", self.text)
        self.assertNotIn("testCovered", self.text)
        # Default app/test roots used for coverage greps
        self.assertNotIn("src-tauri crates app lib packages", self.text)
        self.assertNotRegex(
            self.text,
            r"grep -roE '\[A-Z\]\[A-Z0-9\]\{1,11\}-\[0-9\]",
            "audit-trace still has a test-tree ID grep",
        )

    def test_DOSP_1_4_E1_is_task_citations_only(self) -> None:
        """DOSP-1.4 — E1 from task cites, not test files."""
        self.assertNotIn("taskCited ∪ testCovered", self.text)
        self.assertNotIn("taskCited ∪", self.text)
        # Positive: E1 mentions task
        self.assertRegex(
            self.text,
            r"\*\*E1\*\*.*task",
            re.I | re.S,
        )

    def test_DOSP_1_6_description_not_covering_test(self) -> None:
        """DOSP-1.6 — frontmatter purpose is docs/spec integrity."""
        # Frontmatter is between first --- pair
        fm = self.text.split("---", 2)[1]
        self.assertNotIn("covering test", fm)
        self.assertNotIn("covering tests", fm)

    def test_DOSP_1_5_6_3_retains_E3_W_and_ARCH_and_decisions(self) -> None:
        """DOSP-1.5 DOSP-6.3 — E3/W1/W2/E4/E5/W3 and decision-record pass remain."""
        for code in DOCS_ONLY_FINDINGS:
            self.assertIn(f"**{code}**", self.text, f"missing finding {code}")
        self.assertIn("validate-records.sh", self.text)
        self.assertIn("--mode=audit-trace", self.text)

    def test_DOSP_7_1_inputs_are_specs_not_app_trees(self) -> None:
        """DOSP-7.1 — inputs section does not list application test roots for coverage."""
        # After reshape, Inputs should not describe searching crates/src for coverage
        inputs = self.text
        if "## Inputs" in inputs:
            block = inputs.split("## Inputs", 1)[1].split("## ", 1)[0]
            self.assertNotIn("Default roots to search", block)
            self.assertNotIn("src-tauri", block)

    def test_scenarios_list_task1_ids(self) -> None:
        """Pack fixtures list Task 1 IDs (DOSP-2.5 exception)."""
        body = SCENARIOS.read_text()
        for token in (
            "DOSP-1.1",
            "DOSP-1.2",
            "DOSP-1.3",
            "DOSP-1.4",
            "DOSP-1.5",
            "DOSP-1.6",
            "DOSP-6.3",
            "DOSP-7.1",
            "DOSP-7.2",
        ):
            self.assertIn(token, body)

    def test_pressure_doc_exists(self) -> None:
        self.assertTrue(PRESSURE.is_file())


if __name__ == "__main__":
    unittest.main()
