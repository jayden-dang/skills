"""Guard: audit-trace's ID scope stays CODE-N.M and ARCH-N only (docs-only).

RMAP-2.10 — planning namespaces stay out of audit-trace.
DOSP — finding set no longer includes E2; inputs are specs (+ optional architecture).
"""

import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
AUDIT_TRACE = REPO / "skills" / "execution" / "audit-trace" / "SKILL.md"
PLANNING_NAMESPACES = ("GOAL-", "MILE-", "ROAD-")
# DOSP: E2 retired
AUDIT_TRACE_FINDINGS = ("E1", "E3", "E4", "E5", "W1", "W2", "W3")


class AuditTraceScope(unittest.TestCase):
    def test_trace_never_reads_planning_namespaces(self):
        """RMAP-2.10 — planning-ID integrity belongs to refresh-roadmap-status, not trace."""
        text = AUDIT_TRACE.read_text()
        leaked = [ns for ns in PLANNING_NAMESPACES if ns in text]
        self.assertEqual([], leaked, f"audit-trace has grown planning-ID scope: {leaked}")

    def test_trace_finding_set_is_docs_only(self):
        """DOSP + RMAP-2.10 — E1/E3–E5/W1–W3 present; E2 absent."""
        text = AUDIT_TRACE.read_text()
        missing = [c for c in AUDIT_TRACE_FINDINGS if f"**{c}**" not in text]
        self.assertEqual([], missing, f"audit-trace finding codes missing: {missing}")
        self.assertNotRegex(text, r"\|\s*\*\*E2\*\*\s*\|")

    def test_trace_does_not_read_the_roadmap(self):
        """RMAP-2.10 — audit-trace's inputs stay docs/specs and docs/architecture."""
        text = AUDIT_TRACE.read_text()
        self.assertNotIn("docs/roadmap", text)


if __name__ == "__main__":
    unittest.main()
