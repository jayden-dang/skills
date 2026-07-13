"""Tests for scripts/lint-handoffs.py.

No `docs/agents/project.md` exists, so there is no requirement-ID convention to
tag against. Test names carry the defect ID instead (LINT-N), per the `tdd`
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
    "lint_handoffs", REPO / "scripts" / "lint-handoffs.py"
)
lint_handoffs = importlib.util.module_from_spec(_spec)
sys.modules["lint_handoffs"] = lint_handoffs
_spec.loader.exec_module(lint_handoffs)


def make_tree(tmp: Path, skills: dict[str, str]) -> Path:
    """Build a fixture skill tree. `skills` maps name -> full SKILL.md text."""
    for name, text in skills.items():
        d = tmp / "skills" / "bucket" / name
        d.mkdir(parents=True)
        (d / "SKILL.md").write_text(text)
    return tmp


def skill(name: str, body: str, user_invoked: bool = False, description: str = "x") -> str:
    fm = f"---\nname: {name}\ndescription: {description}\n"
    if user_invoked:
        fm += "disable-model-invocation: true\n"
    fm += "---\n"
    return fm + body


class TestScanSeam(unittest.TestCase):
    def test_LINT_0_scan_reports_a_dead_handoff(self):
        """A body directing the agent to invoke a user-invoked skill is a failure."""
        with tempfile.TemporaryDirectory() as tmp:
            root = make_tree(
                Path(tmp),
                {
                    "triage": skill("triage", "\n# Triage\n", user_invoked=True),
                    "caller": skill("caller", "\n# Caller\n\ninvoke `triage` now.\n"),
                },
            )
            failures = lint_handoffs.scan(root)
            self.assertEqual(len(failures), 1)
            self.assertEqual(failures[0].caller, "caller")
            self.assertEqual(failures[0].target, "triage")

    def test_LINT_0_clean_tree_reports_nothing(self):
        """Naming a user-invoked skill for the user to run is legal."""
        with tempfile.TemporaryDirectory() as tmp:
            root = make_tree(
                Path(tmp),
                {
                    "triage": skill("triage", "\n# Triage\n", user_invoked=True),
                    "caller": skill(
                        "caller", "\n# Caller\n\nTell the user to run `/triage`.\n"
                    ),
                },
            )
            self.assertEqual(lint_handoffs.scan(root), [])


class TestLineNumbers(unittest.TestCase):
    def test_LINT_1_line_number_is_the_real_file_line(self):
        """The reported line must be clickable — i.e. the true file line.

        Frontmatter is 4 lines (`---`, name, description, `---`), so the body
        starts at file line 5 and the violation below sits on file line 8.
        """
        with tempfile.TemporaryDirectory() as tmp:
            root = make_tree(
                Path(tmp),
                {
                    "triage": skill("triage", "\n# Triage\n", user_invoked=True),
                    "caller": skill("caller", "\n# Caller\n\ninvoke `triage` now.\n"),
                },
            )
            text = (root / "skills/bucket/caller/SKILL.md").read_text()
            true_line = text.split("\n").index("invoke `triage` now.") + 1
            self.assertEqual(true_line, 8)  # independent of the code under test

            self.assertEqual(lint_handoffs.scan(root)[0].line, true_line)


class TestPatternAuthoring(unittest.TestCase):
    def test_LINT_2_a_pattern_may_contain_a_regex_quantifier(self):
        """Adding `delegate\\s{1,3}to` must work — braces are regex, not format slots."""
        with tempfile.TemporaryDirectory() as tmp:
            root = make_tree(
                Path(tmp),
                {
                    "triage": skill("triage", "\n# Triage\n", user_invoked=True),
                    "caller": skill("caller", "\n# Caller\n\nJust delegate  to `triage`.\n"),
                },
            )
            with unittest.mock.patch.object(
                lint_handoffs, "INVOKE", [r"delegate\s{1,3}to `{name}`"]
            ):
                failures = lint_handoffs.scan(root)
            self.assertEqual(len(failures), 1)
            self.assertEqual(failures[0].target, "triage")


class TestWrappedPhrasing(unittest.TestCase):
    def test_LINT_4_a_handoff_wrapped_across_a_newline_is_caught(self):
        """Prose is hard-wrapped, so a phrasing can straddle a line break."""
        with tempfile.TemporaryDirectory() as tmp:
            root = make_tree(
                Path(tmp),
                {
                    "triage": skill("triage", "\n# Triage\n", user_invoked=True),
                    "caller": skill(
                        "caller",
                        "\n# Caller\n\nWhen the idea is really a bug report, hand off to\n"
                        "`triage` instead.\n",
                    ),
                },
            )
            failures = lint_handoffs.scan(root)
            self.assertEqual(len(failures), 1, "wrapped hand-off went undetected")
            self.assertEqual(failures[0].line, 8)  # the line the phrasing starts on


class TestSlashForm(unittest.TestCase):
    def test_LINT_5_invoke_phrasing_in_slash_form_is_caught(self):
        """``invoke `/triage` `` is as dead a hand-off as ``invoke `triage` ``."""
        with tempfile.TemporaryDirectory() as tmp:
            root = make_tree(
                Path(tmp),
                {
                    "triage": skill("triage", "\n# Triage\n", user_invoked=True),
                    "caller": skill("caller", "\n# Caller\n\nJust invoke `/triage`.\n"),
                },
            )
            failures = lint_handoffs.scan(root)
            self.assertEqual(len(failures), 1, "slash form slipped through")

    def test_LINT_5_naming_the_command_for_the_user_stays_legal(self):
        """The guard: `run `/triage`` is the CORRECT phrasing and must not fire."""
        with tempfile.TemporaryDirectory() as tmp:
            root = make_tree(
                Path(tmp),
                {
                    "triage": skill("triage", "\n# Triage\n", user_invoked=True),
                    "caller": skill(
                        "caller",
                        "\n# Caller\n\nTell the user to run `/triage` — user-invoked.\n",
                    ),
                },
            )
            self.assertEqual(lint_handoffs.scan(root), [])


class TestDelegatePhrasing(unittest.TestCase):
    """LINT-6: `delegate to `x`` is an invoke phrasing and must be caught.

    The trap: the only `delegate` in the repo is *conjugated* — "delegates to" —
    so the obvious `delegate\\s+to` pattern would match nothing at all. A pattern
    that never fires looks exactly like a pattern that isn't there.
    """

    def _scan_body(self, body: str):
        with tempfile.TemporaryDirectory() as tmp:
            root = make_tree(
                Path(tmp),
                {
                    "triage": skill("triage", "\n# Triage\n", user_invoked=True),
                    "caller": skill("caller", f"\n# Caller\n\n{body}\n"),
                },
            )
            return lint_handoffs.scan(root)

    def test_LINT_6_bare_delegate_to(self):
        self.assertEqual(len(self._scan_body("Just delegate to `triage`.")), 1)

    def test_LINT_6_conjugated_delegates_to(self):
        """The exact shape that already exists in correct-course/SKILL.md:79."""
        self.assertEqual(len(self._scan_body("It delegates to `triage`.")), 1)

    def test_LINT_6_delegating_to(self):
        self.assertEqual(len(self._scan_body("Consider delegating to `triage`.")), 1)

    def test_LINT_6_intervening_words(self):
        self.assertEqual(len(self._scan_body("Delegate the whole job to `triage`.")), 1)

    def test_LINT_6_slash_form(self):
        self.assertEqual(len(self._scan_body("Delegate to `/triage`.")), 1)

    def test_LINT_6_delegation_to_the_user_is_legal(self):
        """The guard: naming the command for the human is the CORRECT phrasing."""
        self.assertEqual(
            self._scan_body("Delegation is the user's call — tell them to run `/triage`."),
            [],
        )


class TestDeduplication(unittest.TestCase):
    def test_LINT_3_one_bad_line_is_reported_once(self):
        """"hand off to `x`" matches two INVOKE patterns; it is still one defect."""
        with tempfile.TemporaryDirectory() as tmp:
            root = make_tree(
                Path(tmp),
                {
                    "triage": skill("triage", "\n# Triage\n", user_invoked=True),
                    "caller": skill("caller", "\n# Caller\n\nHand off to `triage`.\n"),
                },
            )
            failures = lint_handoffs.scan(root)
            self.assertEqual(len(failures), 1, f"double-counted: {failures}")


if __name__ == "__main__":
    unittest.main()
