"""Fixture-set validity for refresh-roadmap-status.

What this test can and cannot prove: a markdown skill has no entry point Python can call,
so this does NOT assert that refresh-roadmap-status emits R1-R11. Reading each fixture's declared
expectation and comparing it to itself would pass no matter what the skill said. What is
deterministically checkable is asserted here — the fixture set is complete, and each
fixture genuinely carries the defect its name claims. Skill behaviour over these fixtures
is verified by tests/roadmap/scenarios-refresh-roadmap-status.md.
"""

import re
import unittest
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / "roadmap" / "fixtures"

# case directory -> the R-code its expected-findings.txt must name (None = must be clean)
CASES = {
    "clean": None,
    "dangling-goal": "R1",
    "uncovered-goal": "R2",
    "duplicate-goal": "R3",
    "road-in-two-milestones": "R4",
    "unresolved-binding": "R5",
    "conflicting-binding": "R6",
    "unspecced-item": "R7",
    "unplanned-feature": "R8",
    "premature-closure": "R9",
    "status-mismatch": "R10",
    "forward-dependency": "R11",
    "missing-outcome": "R11",
    "retired-depends-on": "R11",
    "unparseable": "R11",
}
BASE_MEMBERS = ("roadmap-INDEX.md", "specs-INDEX.md", "vision.md", "expected-findings.txt")
WITHHOLDING = {"R2", "R4", "R9", "R10", "R11"}


def read(case, member):
    return (FIXTURES / case / member).read_text()


def codes(case):
    text = read(case, "expected-findings.txt")
    return {ln.strip() for ln in text.splitlines() if ln.strip() and not ln.startswith("#")}


def live_ids(text, prefix):
    """IDs surviving strikethrough removal — the rule audit-trace applies to ARCH-N."""
    return re.findall(rf"\*\*({prefix}-\d+)\*\*", re.sub(r"~~[^~]*~~", "", text))


class FixtureSet(unittest.TestCase):
    def test_every_case_is_a_complete_miniature_repo(self):
        """RMAP-3.1 — every fixture supplies the inputs the passes read."""
        for case in CASES:
            for member in BASE_MEMBERS:
                with self.subTest(case=case, member=member):
                    self.assertTrue((FIXTURES / case / member).is_file())

    def test_expectations_name_the_declared_code(self):
        """RMAP-3.2 RMAP-3.4 RMAP-3.5 RMAP-3.6 RMAP-3.7 RMAP-3.8 RMAP-3.15 RMAP-3.19 RMAP-4.4"""
        for case, code in CASES.items():
            with self.subTest(case=case):
                declared = codes(case)
                if code is None:
                    self.assertEqual(set(), declared)
                else:
                    self.assertIn(code, declared)

    def test_clean_fixture_is_genuinely_clean(self):
        """RMAP-3.9 RMAP-3.12 RMAP-3.14 — the clean case must carry no defect at all."""
        self.assertEqual(set(), codes("clean"))
        roadmap = read("clean", "roadmap-INDEX.md")
        miles = live_ids(roadmap, "MILE")
        roads = live_ids(roadmap, "ROAD")
        self.assertEqual(len(miles), len(set(miles)), "clean fixture duplicates a MILE-N")
        self.assertEqual(len(roads), len(set(roads)), "clean fixture duplicates a ROAD-N")

    def test_duplicate_goal_fixture_really_repeats_a_goal(self):
        """RMAP-3.20 — the fixture carries the defect, not just the label."""
        ids = live_ids(read("duplicate-goal", "vision.md"), "GOAL")
        self.assertNotEqual(len(ids), len(set(ids)), "no repeated GOAL-N in the fixture")

    def test_road_in_two_milestones_fixture_really_double_lists(self):
        """RMAP-3.4 — the same ROAD-N sits under two milestone headings."""
        text = read("road-in-two-milestones", "roadmap-INDEX.md")
        blocks = re.split(r"(?m)^## MILE-\d+", text)[1:]
        self.assertGreaterEqual(len(blocks), 2, "fixture needs at least two milestones")
        owners = [set(live_ids(b, "ROAD")) for b in blocks]
        self.assertTrue(set.intersection(*owners), "no ROAD-N shared across milestones")

    def test_status_mismatch_fixture_really_disagrees(self):
        """RMAP-3.19 — the INDEX row and the requirements file record different statuses."""
        index_row = re.search(
            r"^\|\s*\w+\s*\|[^|]*\|[^|]*\|\s*(\w+)\s*\|", read("status-mismatch", "specs-INDEX.md"), re.M
        )
        self.assertIsNotNone(index_row, "no feature row in the fixture's spec index")
        spec_status = re.search(r"(?m)^Status:\s*(\w+)", read("status-mismatch", "requirements.md"))
        self.assertIsNotNone(spec_status, "fixture needs a requirements.md carrying Status:")
        self.assertNotEqual(index_row.group(1), spec_status.group(1), "the two statuses agree")

    def test_forward_dependency_fixture_really_points_forward(self):
        """RMAP-4.4 — a Depends-on names a milestone appearing later in the table."""
        text = read("forward-dependency", "roadmap-INDEX.md")
        order = re.findall(r"(?m)^\|\s*(MILE-\d+)\s*\|", text)
        self.assertGreaterEqual(len(order), 2)
        offenders = [
            (mile, dep)
            for mile, dep in re.findall(r"(?m)^\|\s*(MILE-\d+)\s*\|[^|]*\|[^|]*\|\s*(MILE-\d+)\s*\|", text)
            if order.index(dep) > order.index(mile)
        ]
        self.assertTrue(offenders, "no forward dependency present in the fixture")

    def test_missing_outcome_fixture_really_omits_one(self):
        """RMAP-4.4 — at least one milestone block has an empty or absent Outcome."""
        text = read("missing-outcome", "roadmap-INDEX.md")
        blocks = re.split(r"(?m)^## MILE-\d+", text)[1:]
        # [ \t] rather than \s — \s crosses the newline and matches the next field's marker.
        empty = [b for b in blocks if not re.search(r"\*\*Outcome:\*\*[ \t]*\S", b)]
        self.assertTrue(empty, "every milestone in the fixture has an outcome")

    def test_withholding_set_is_declared_per_fixture(self):
        """RMAP-3.16 — a fixture whose code withholds says so, so the ladder can be checked."""
        for case, code in CASES.items():
            if code in WITHHOLDING:
                with self.subTest(case=case):
                    self.assertIn(
                        "withholds",
                        read(case, "expected-findings.txt"),
                        f"{case} declares {code} but does not record that it withholds",
                    )


if __name__ == "__main__":
    unittest.main()
