"""prepare-change base resolution: declared, asked, never inferred from topology."""
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "ship" / "prepare-change" / "SKILL.md"


class PrepareChangeBase(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text()

    def test_PCHG_2_1_2_2_2_3_2_4_ladder_in_order(self):
        """PCHG-2.1 PCHG-2.2 PCHG-2.3 PCHG-2.4 — four rungs, in order, ending in ask."""
        rungs = ["explicit base", "existing PR", "Default PR base:", "ask the user"]
        positions = [self.text.find(r) for r in rungs]
        self.assertNotIn(-1, positions, f"missing rung among {rungs}")
        self.assertEqual(positions, sorted(positions), "base ladder rungs out of order")

    def test_PCHG_2_6_no_topology_fallback(self):
        """PCHG-2.6 — origin/HEAD, main, master, and fork-point are named as forbidden."""
        self.assertRegex(
            self.text,
            r"(?s)NEVER[^\n]*origin/HEAD|SHALL NOT[^\n]*origin/HEAD|never[^\n]*origin/HEAD",
            msg="prepare-change does not forbid topology-based base selection",
        )
        for token in ("fork-point", "`main`", "`master`"):
            self.assertIn(token, self.text)

    def test_PCHG_2_7_writes_no_project_config(self):
        """PCHG-2.7 — the skill never writes docs/agents/project.md."""
        self.assertRegex(self.text, r"never writes? .{0,40}project\.md|writes no project configuration")

    def test_PCHG_2_5_head_equals_default_asks(self):
        """PCHG-2.5 — head == configured default always asks, invocation-scoped."""
        self.assertIn("head branch is the configured", self.text)
        self.assertIn("this invocation only", self.text)

    def test_PCHG_2_8_names_setup_repo_when_absent(self):
        """PCHG-2.8 — absent config continues session-only and names /setup-repo."""
        self.assertIn("/setup-repo", self.text)

    def test_PCHG_2_9_2_10_memoized_and_revalidated(self):
        """PCHG-2.9 PCHG-2.10 — memoized for the session; re-asked when it stops resolving."""
        self.assertIn("memoize", self.text.lower())
        self.assertIn("no longer resolves", self.text)


if __name__ == "__main__":
    unittest.main()
