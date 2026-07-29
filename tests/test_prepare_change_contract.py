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

    def test_PCHG_2_9_manifest_field_distinct_from_config_field(self):
        """PCHG-2.9 — the manifest records the resolved value under `Base:`,
        never under the config field name `Default PR base:`, since the
        resolved value is a per-invocation value that may differ from the
        configured default."""
        self.assertRegex(self.text, r"manifest\s+as\s+`Base:`")
        self.assertNotRegex(self.text, r"manifest\s+as\s+`Default PR base:`")
        self.assertRegex(
            self.text,
            r"(?s)`Base:`.{0,120}resolved base for this invocation.{0,120}may differ from any configured `Default PR base:`",
        )


class PrepareChangeContext(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text()

    def test_PCHG_3_1_3_2_two_authorities(self):
        """PCHG-3.1 PCHG-3.2 — diff owns what changed; specs/ADRs/records own why."""
        self.assertIn("diff", self.text)
        self.assertRegex(self.text, r"(?s)what changed.{0,400}why")
        for src in ("docs/adr", "implementation-notes.md", "decision record"):
            self.assertIn(src, self.text)

    def test_PCHG_3_3_absent_context_omits_never_invents(self):
        """PCHG-3.3 — a missing why-source shortens the narrative, never fills it."""
        self.assertRegex(self.text, r"(?i)never invent")
        self.assertIn("omit", self.text.lower())

    def test_PCHG_3_4_loads_passive_data_contract_by_path(self):
        """PCHG-3.4 — the shared passive-data contract is loaded, not restated."""
        self.assertIn(
            "skills/review/explain-change/references/passive-data-safety.md", self.text
        )

    def test_PCHG_3_5_secrets_redacted_by_class(self):
        """PCHG-3.5 — secrets become class-named placeholders."""
        self.assertIn("[redacted:", self.text)

    def test_PCHG_3_6_3_7_locator_rule(self):
        """PCHG-3.6 PCHG-3.7 — only reachable paths are linked; the rest is inlined."""
        self.assertIn("tracked and reachable", self.text)
        self.assertRegex(self.text, r"(?s)promote.{0,60}inline")
        self.assertIn(".skills/", self.text)


if __name__ == "__main__":
    unittest.main()
