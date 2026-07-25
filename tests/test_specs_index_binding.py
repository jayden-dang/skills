"""The Roadmap item binding column in the spec-index template and its consumers."""

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TEMPLATE = REPO / "templates" / "specs-INDEX.md"
LIVE_INDEX = REPO / "docs" / "specs" / "INDEX.md"
WRITE_REQS = REPO / "skills" / "spec" / "write-requirements" / "SKILL.md"
GUIDE_COPIES = [
    REPO / "docs" / "guide" / "concepts" / "artifacts.md",
    REPO / "docs" / "guide" / "concepts" / "feature-graph.md",
]

HEADER = re.compile(r"^\|\s*Code\s*\|\s*Feature\s*\|\s*Spec\s*\|\s*Status\s*\|\s*Roadmap item\s*\|", re.M)
STALE_HEADER = re.compile(r"^\|\s*Code\s*\|\s*Feature\s*\|\s*Spec\s*\|\s*Status\s*\|\s*$", re.M)


class BindingColumn(unittest.TestCase):
    def test_template_declares_the_column(self):
        """RMAP-2.4 — the registry template carries a Roadmap item column."""
        self.assertRegex(TEMPLATE.read_text(), HEADER)

    def test_template_row_shows_an_empty_binding_is_legal(self):
        """RMAP-2.5 — the template shows the no-roadmap case, so an empty cell is not a defect."""
        self.assertIn("—", TEMPLATE.read_text())

    def test_live_index_has_the_column(self):
        """RMAP-2.4 — this repo's own registry carries it too."""
        self.assertRegex(LIVE_INDEX.read_text(), HEADER)

    def test_write_requirements_owns_the_binding_write(self):
        """RMAP-2.4 RMAP-2.6 — Step 1 stays the sole registrar and now records the binding."""
        text = WRITE_REQS.read_text()
        self.assertIn("Roadmap item", text)
        self.assertIn("ROAD-", text)
        # Registration ownership is unchanged: the code is still picked and registered here.
        self.assertRegex(text, r"(?s)## Step 1: Register the feature code")

    def test_no_guide_doc_still_shows_the_four_column_table(self):
        """RMAP-2.4 — the copies in the guide do not contradict the template."""
        stale = [p.name for p in GUIDE_COPIES if STALE_HEADER.search(p.read_text())]
        self.assertEqual([], stale, f"guide docs still show the old table: {stale}")


if __name__ == "__main__":
    unittest.main()
