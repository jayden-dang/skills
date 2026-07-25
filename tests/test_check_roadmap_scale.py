"""The derivation budget is fixed and independent of feature and milestone count.

RMAP-4.1 says check-roadmap completes with one full read of each source artifact and a
bounded number of git commands, independent of scale. Two things make that checkable
without an entry point: the skill's documented pass set is a fixed count with no per-item
pass, and a scale fixture exists that those same passes cover.
"""

import re
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "track" / "check-roadmap" / "SKILL.md"
SCALE = Path(__file__).resolve().parent / "roadmap" / "fixtures" / "scale"

FEATURES = 200
MILESTONES = 50
ITEMS_PER_MILESTONE = 4  # 50 x 4 = 200 items, one per feature


class PassBudget(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text()

    def test_pass_count_is_fixed(self):
        """RMAP-4.1 — exactly six numbered passes, so the budget is a constant."""
        passes = re.findall(r"(?m)^\*\*(\d+)\. ", self.text)
        self.assertEqual(["1", "2", "3", "4", "5", "6"], passes, f"pass set changed: {passes}")

    def test_no_pass_is_per_item(self):
        """RMAP-4.1 — a pass described as running per feature or per milestone breaks the budget."""
        section = self.text[self.text.index("## The passes"):self.text.index("## The rules")]
        offenders = [
            phrase
            for phrase in ("for each feature", "per feature", "for each milestone", "per milestone", "for each item")
            if phrase in section.lower()
        ]
        self.assertEqual([], offenders, f"a pass is described per-item: {offenders}")

    def test_git_use_is_bounded(self):
        """RMAP-4.1 — git appears in the passes a bounded number of times, not once per item."""
        section = self.text[self.text.index("## The passes"):self.text.index("## The rules")]
        git_calls = re.findall(r"(?m)^\s*git\s", section)
        self.assertLessEqual(len(git_calls), 2, f"unbounded git use in the passes: {git_calls}")


class ScaleFixture(unittest.TestCase):
    def test_fixture_is_at_the_declared_scale(self):
        """RMAP-4.1 — the fixture really holds 200 features and 50 milestones."""
        roadmap = (SCALE / "roadmap-INDEX.md").read_text()
        specs = (SCALE / "specs-INDEX.md").read_text()
        miles = re.findall(r"(?m)^## (MILE-\d+)", roadmap)
        roads = re.findall(r"(?m)^- \*\*(ROAD-\d+)\*\*", roadmap)
        rows = re.findall(r"(?m)^\| ([A-Z][A-Z0-9]{1,11}) \|", specs)
        self.assertEqual(MILESTONES, len(miles))
        self.assertEqual(FEATURES, len(roads))
        self.assertEqual(FEATURES, len(rows))
        self.assertEqual(len(set(miles)), len(miles), "duplicate MILE-N in the scale fixture")
        self.assertEqual(len(set(roads)), len(roads), "duplicate ROAD-N in the scale fixture")

    def test_every_pass_covers_the_fixture_in_one_read(self):
        """RMAP-4.1 — the documented greps match at the expected scale, one pass per file."""
        roadmap = SCALE / "roadmap-INDEX.md"
        found = subprocess.run(
            ["grep", "-cE", r"^- \*\*ROAD-[0-9]+\*\*", str(roadmap)],
            capture_output=True, text=True, check=True,
        )
        self.assertEqual(FEATURES, int(found.stdout.strip()))

    def test_fixture_is_clean_so_scale_is_the_only_variable(self):
        """RMAP-4.1 — a defect at scale would confound the budget measurement."""
        codes = {
            ln.strip()
            for ln in (SCALE / "expected-findings.txt").read_text().splitlines()
            if ln.strip() and not ln.startswith("#")
        }
        self.assertEqual(set(), codes, "the scale fixture must be structurally clean")


if __name__ == "__main__":
    unittest.main()
