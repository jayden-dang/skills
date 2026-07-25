"""Roadmap template slot contract."""

import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TEMPLATE = REPO / "templates" / "roadmap-INDEX.md"

SLOTS = [
    "Status:",
    "**Outcome:**",
    "**Goals:**",
    "**Members:**",
    "Surfaces:",
    "**Depends-on:**",
    "**Commitment:**",
    "**Closed:**",
    "**Deferred:**",
    "**Blockers:**",
    "## Goal dispositions",
]


class RoadmapTemplateSlots(unittest.TestCase):
    def test_template_exists_with_status_field(self):
        """RMAP-1.1 RMAP-1.16 — the template exists and carries a top-level Status field."""
        self.assertTrue(TEMPLATE.is_file(), f"missing {TEMPLATE}")
        self.assertRegex(TEMPLATE.read_text(), r"(?m)^Status: Draft$")

    def test_every_required_slot_present(self):
        """RMAP-1.2 RMAP-1.3 RMAP-1.15 RMAP-1.20 — milestone, item, disposition and surface slots."""
        text = TEMPLATE.read_text()
        missing = [s for s in SLOTS if s not in text]
        self.assertEqual([], missing, f"template is missing slots: {missing}")

    def test_structural_rule_block_is_complete(self):
        """RMAP-1.2 — the comment block defines S1 through S7 as the authoritative rule list."""
        text = TEMPLATE.read_text()
        missing = [f"S{n}" for n in range(1, 8) if f"S{n}" not in text]
        self.assertEqual([], missing, f"rule block is missing: {missing}")


if __name__ == "__main__":
    unittest.main()
