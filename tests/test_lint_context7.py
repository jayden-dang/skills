"""Tests for scripts/lint-context7.py.

No `docs/agents/project.md` exists, so there is no requirement-ID convention to
tag against. Test names carry the defect ID instead (CTX-N), per the `tdd`
fallback. Run: python3 -m unittest discover -s tests -v
"""

import importlib.util
import sys
import tempfile
import unittest
import unittest.mock
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# The script is not an importable module name (hyphen), so load it by path.
_spec = importlib.util.spec_from_file_location(
    "lint_context7", REPO / "scripts" / "lint-context7.py"
)
lint_context7 = importlib.util.module_from_spec(_spec)
sys.modules["lint_context7"] = lint_context7
_spec.loader.exec_module(lint_context7)


def make_tree(tmp: Path, skills: dict[str, str]) -> Path:
    """Build a fixture skill tree. `skills` maps name -> full SKILL.md text."""
    for name, text in skills.items():
        d = tmp / "skills" / "bucket" / name
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(text)
    return tmp


def skill(name: str, body: str) -> str:
    return f"---\nname: {name}\ndescription: x\n---\n{body}"


class TestDriftCaught(unittest.TestCase):
    def test_CTX_0_a_required_skill_without_context7_is_a_failure(self):
        """The core guard: drop the Context7 reference and the linter fires."""
        with tempfile.TemporaryDirectory() as tmp:
            root = make_tree(
                Path(tmp),
                {
                    "research": skill("research", "\nPrefer the Context7 MCP.\n"),
                    "write-design": skill("write-design", "\n# Design\n\nNo mention here.\n"),
                },
            )
            with unittest.mock.patch.object(
                lint_context7, "REQUIRE", {"research", "write-design"}
            ):
                failures = lint_context7.scan(root)
            self.assertEqual(len(failures), 1)
            self.assertEqual(failures[0].skill, "write-design")
            self.assertEqual(failures[0].reason, "no-mention")

    def test_CTX_0_all_required_skills_mentioning_it_is_clean(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_tree(
                Path(tmp),
                {
                    "research": skill("research", "\nPrefer the Context7 MCP.\n"),
                    "write-design": skill("write-design", "\nLook it up via Context7.\n"),
                },
            )
            with unittest.mock.patch.object(
                lint_context7, "REQUIRE", {"research", "write-design"}
            ):
                self.assertEqual(lint_context7.scan(root), [])


class TestSelfDrift(unittest.TestCase):
    def test_CTX_1_a_require_entry_with_no_skill_file_is_a_failure(self):
        """A rename that outran REQUIRE must fail loudly, not pass silently.

        The lesson from lint-handoffs LINT-6: a check that points at nothing
        looks identical to a check that isn't there. If `write-design` were
        renamed, `REQUIRE` would still list it — and this guard catches that.
        """
        with tempfile.TemporaryDirectory() as tmp:
            root = make_tree(
                Path(tmp),
                {"research": skill("research", "\nPrefer the Context7 MCP.\n")},
            )
            with unittest.mock.patch.object(
                lint_context7, "REQUIRE", {"research", "write-design"}
            ):
                failures = lint_context7.scan(root)
            self.assertEqual(len(failures), 1)
            self.assertEqual(failures[0].skill, "write-design")
            self.assertEqual(failures[0].reason, "missing-skill")


class TestCaseInsensitive(unittest.TestCase):
    def test_CTX_2_lowercase_context7_counts_as_a_reference(self):
        """A `context7` in a code fence or `.mcp.json` snippet is still a live mention."""
        with tempfile.TemporaryDirectory() as tmp:
            root = make_tree(
                Path(tmp),
                {"research": skill("research", "\nAdd `context7` to .mcp.json.\n")},
            )
            with unittest.mock.patch.object(lint_context7, "REQUIRE", {"research"}):
                self.assertEqual(lint_context7.scan(root), [])


class TestRealRepo(unittest.TestCase):
    def test_CTX_3_the_shipped_skill_set_is_clean(self):
        """The real REQUIRE set, scanned against the real repo, must pass."""
        self.assertEqual(lint_context7.scan(REPO), [])


if __name__ == "__main__":
    unittest.main()
