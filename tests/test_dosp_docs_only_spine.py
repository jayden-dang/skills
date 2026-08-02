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
