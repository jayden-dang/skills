"""GOAL-N identity in the vision template and this repo's own approved vision."""

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TEMPLATE = REPO / "templates" / "product-vision.md"
LIVE_VISION = REPO / "docs" / "product" / "vision.md"
ESTABLISH = REPO / "skills" / "project" / "define-project" / "SKILL.md"

BOLD_GOAL = re.compile(r"\*\*(GOAL-\d+)\*\*")
GOALS_SECTION = re.compile(r"(?ms)^## Goals\n(.*?)(?=^## )")


def goals_block(path):
    match = GOALS_SECTION.search(path.read_text())
    assert match, f"no ## Goals section in {path}"
    return match.group(1)


def live_ids(path):
    """IDs surviving strikethrough removal — the same rule audit-trace applies to ARCH-N."""
    text = re.sub(r"~~[^~]*~~", "", goals_block(path))
    return BOLD_GOAL.findall(text)


class VisionGoalIds(unittest.TestCase):
    def test_template_goals_are_ided(self):
        """RMAP-2.7 — the template's Goals section carries bold GOAL-N IDs."""
        self.assertTrue(live_ids(TEMPLATE), "template Goals section has no **GOAL-N**")

    def test_live_vision_is_migrated(self):
        """RMAP-2.8 — this repo's own approved vision carries GOAL-N on every goal."""
        block = goals_block(LIVE_VISION)
        bullets = [ln for ln in block.splitlines() if ln.strip().startswith("- ")]
        self.assertTrue(bullets, "no goal bullets found")
        unided = [ln for ln in bullets if not BOLD_GOAL.search(ln)]
        self.assertEqual([], unided, f"goals still lack IDs: {unided}")

    def test_live_vision_ids_are_unique(self):
        """RMAP-2.8 — a duplicate GOAL-N would make every citation ambiguous."""
        ids = live_ids(LIVE_VISION)
        self.assertTrue(ids, "no live GOAL-N in the vision — uniqueness would pass vacuously")
        self.assertEqual(len(ids), len(set(ids)), f"duplicate GOAL-N: {ids}")

    def test_establish_project_assigns_and_migrates(self):
        """RMAP-2.7 RMAP-2.8 RMAP-2.9 — create assigns, update migrates, approved goals are immutable."""
        text = ESTABLISH.read_text()
        self.assertIn("GOAL-N", text)
        self.assertRegex(text, r"(?i)strikethrough")
        self.assertRegex(text, r"(?i)document order")


if __name__ == "__main__":
    unittest.main()
