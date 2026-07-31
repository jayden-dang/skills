"""The evidence-gathering budget is fixed and independent of member count.

ASSESS-6.1 says assess-milestone completes with one full read of each source artifact and
a number of git commands independent of the milestone's member count. The same two things
make that checkable without an entry point as for status-roadmap (RMAP-4.1): the skill's
documented pass set is a fixed count with no per-member pass, and a scale fixture exists
that those same passes cover.
"""

import re
import subprocess
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "track" / "assess-milestone" / "SKILL.md"
SCALE = Path(__file__).resolve().parent / "milestone-assessment" / "fixtures" / "scale-50-members"

MEMBERS = 50


class PassBudget(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text()
        self.section = self.text[
            self.text.index("## Resolve the scope") : self.text.index("## Judge the milestone")
        ]

    def test_pass_count_is_fixed(self):
        """ASSESS-6.1 — exactly eight numbered passes (0-7), so the budget is a constant."""
        passes = re.findall(r"(?m)^\*\*(\d+)\. ", self.section)
        self.assertEqual(
            ["0", "1", "2", "3", "4", "5", "6", "7"], passes, f"pass set changed: {passes}"
        )

    def test_no_pass_is_per_member(self):
        """ASSESS-6.1 — a pass described as running per member breaks the budget."""
        offenders = [
            phrase
            for phrase in ("for each member", "per member", "for each item", "per item", "for every member")
            if phrase in self.section.lower()
        ]
        self.assertEqual([], offenders, f"a pass is described per-member: {offenders}")

    def test_git_use_is_bounded(self):
        """ASSESS-6.1 — git appears in the passes a bounded number of times."""
        git_calls = re.findall(r"(?m)^\s*git\s", self.section)
        self.assertLessEqual(len(git_calls), 4, f"unbounded git use in the passes: {git_calls}")

    def test_cost_is_stated_as_member_independent(self):
        """ASSESS-6.1 — the skill says out loud that member count does not change the cost."""
        flat = re.sub(r"\s+", " ", self.text)
        self.assertIn("Nothing here loops over members", flat)


class ScaleFixture(unittest.TestCase):
    def test_fixture_is_at_the_declared_scale(self):
        """ASSESS-6.1 — the fixture really holds at least 50 members, each bound once."""
        roadmap = (SCALE / "roadmap-INDEX.md").read_text()
        specs = (SCALE / "specs-INDEX.md").read_text()
        roads = re.findall(r"(?m)^- \*\*(ROAD-\d+)\*\*", roadmap)
        rows = re.findall(r"(?m)^\| ([A-Z][A-Z0-9]{1,11}) \|", specs)
        self.assertGreaterEqual(len(roads), MEMBERS)
        self.assertEqual(len(roads), len(rows), "every member must bind exactly one feature")
        self.assertEqual(len(set(roads)), len(roads), "duplicate ROAD-N in the scale fixture")

    def test_one_grep_covers_every_member(self):
        """ASSESS-6.1 — the documented membership pass matches all members in one read."""
        found = subprocess.run(
            ["grep", "-cE", r"^- \*\*ROAD-[0-9]+\*\*", str(SCALE / "roadmap-INDEX.md")],
            capture_output=True, text=True, check=True,
        )
        self.assertGreaterEqual(int(found.stdout.strip()), MEMBERS)

    def test_fixture_holds_one_milestone_so_scale_is_the_only_variable(self):
        """ASSESS-6.1 — extra milestones would confound the per-member measurement."""
        miles = re.findall(r"(?m)^## (MILE-\d+)", (SCALE / "roadmap-INDEX.md").read_text())
        self.assertEqual(["MILE-1"], miles)


if __name__ == "__main__":
    unittest.main()
