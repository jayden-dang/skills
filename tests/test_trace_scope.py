"""Guard: trace's ID scope stays CODE-N.M and ARCH-N only.

This is a regression guard, not a driver of new behaviour — it protects a boundary that
already holds today, so it passes on its first run by design. RMAP-2.10 is a
SHALL CONTINUE TO guard criterion, and a guard's failure mode is a future edit.
"""

import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TRACE = REPO / "skills" / "execution" / "trace" / "SKILL.md"
PLANNING_NAMESPACES = ("GOAL-", "MILE-", "ROAD-")
TRACE_FINDINGS = ("E1", "E2", "E3", "E4", "E5", "W1", "W2", "W3")


class TraceScope(unittest.TestCase):
    def test_trace_never_reads_planning_namespaces(self):
        """RMAP-2.10 — planning-ID integrity belongs to check-roadmap, not trace."""
        text = TRACE.read_text()
        leaked = [ns for ns in PLANNING_NAMESPACES if ns in text]
        self.assertEqual([], leaked, f"trace has grown planning-ID scope: {leaked}")

    def test_trace_finding_set_is_unchanged(self):
        """RMAP-2.10 — the E1-E5 / W1-W3 finding set is intact."""
        text = TRACE.read_text()
        missing = [c for c in TRACE_FINDINGS if f"**{c}**" not in text]
        self.assertEqual([], missing, f"trace finding codes missing: {missing}")

    def test_trace_does_not_read_the_roadmap(self):
        """RMAP-2.10 — trace's inputs stay docs/specs, docs/architecture and the test roots."""
        text = TRACE.read_text()
        self.assertNotIn("docs/roadmap", text)


if __name__ == "__main__":
    unittest.main()
