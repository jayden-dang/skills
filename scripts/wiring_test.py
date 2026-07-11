"""Wiring assertions for the feature-graph and traceability linters.

These pin the invariants that let the skills, templates, README, and DESIGN.md
actually run the linters: every consumer spells the real `python3
scripts/<name>.py` invocation, the graph query fails open when the linter is
absent, the spec templates demand no linter/graph annotations, and — the guard
that keeps this from rotting — no skill, doc, or template anywhere names a
retired `.mjs` linter.
"""
import os
import re
import unittest

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_SCRIPTS_DIR)


def _read(rel):
    with open(os.path.join(_REPO_ROOT, rel), "r", encoding="utf-8") as fh:
        return fh.read()


_I = re.IGNORECASE


class BrainstormWiringTest(unittest.TestCase):
    def test_brainstorm_wires_the_graph_query(self):
        """brainstorm calls the graph query, presents cards, and notes fail-open."""
        t = _read("skills/discovery/brainstorm/SKILL.md")
        self.assertRegex(t, r"check_graph\.py --query", "brainstorm calls the query")
        self.assertRegex(t, re.compile(r"card", _I), "presents cards")
        self.assertRegex(t, re.compile(r"overlap check unavailable", _I), "fail-open note")

    def test_brainstorm_step1_done_when_states_overlaps(self):
        """brainstorm step-1 Done-when states overlaps or their absence."""
        t = _read("skills/discovery/brainstorm/SKILL.md")
        self.assertRegex(
            t,
            re.compile(r"share[sd]? .*surface|no existing feature", _I),
            "state overlaps or none",
        )


class SyncSpecWiringTest(unittest.TestCase):
    def test_sync_spec_regenerates_and_stages_graph_md(self):
        """sync-spec regenerates and stages GRAPH.md via the Python linter."""
        t = _read("skills/track/sync-spec/SKILL.md")
        self.assertRegex(t, r"check_graph\.py --harvest", "regenerates GRAPH.md")
        self.assertRegex(
            t,
            re.compile(r"GRAPH\.md[\s\S]{0,40}stage it into this sync-spec commit", _I),
            "stages GRAPH.md into the commit",
        )


class SetupRepoRemedyWiringTest(unittest.TestCase):
    def test_names_setup_repo_as_the_remedy_once_and_still_fails_open(self):
        """brainstorm and code-review name setup-repo as the remedy, once, and still fail open."""
        for rel in ("skills/discovery/brainstorm/SKILL.md", "skills/review/code-review/SKILL.md"):
            t = _read(rel)
            self.assertRegex(
                t, re.compile(r"not installed[\s\S]{0,160}setup-repo", _I),
                f"{rel}: remedy names setup-repo",
            )
            self.assertRegex(
                t, re.compile(r"once per session", _I),
                f"{rel}: the remedy is stated once, not every query",
            )
            self.assertRegex(
                t, re.compile(r"never block|continue", _I),
                f"{rel}: still fails open",
            )


class TemplatesWiringTest(unittest.TestCase):
    def test_spec_templates_demand_no_new_fields_for_the_graph(self):
        """The spec templates demand no linter/graph annotations (no authoring burden)."""
        for rel in ("templates/requirements.md", "templates/design.md", "templates/tasks.md"):
            t = _read(rel)
            self.assertNotRegex(
                t,
                re.compile(r"check[-_](trace|graph)|vendor[-_]linters|GRAPH\.md", _I),
                f"{rel} must not require any linter/graph annotation",
            )

    def test_project_md_template_invokes_the_python_linters(self):
        """The project.md template's Trace and Graph rows invoke the Python linters."""
        t = _read("templates/agents/project.md")
        self.assertRegex(
            t,
            re.compile(r"^\|\s*Trace\s*\|.*python3\s+\S*check_trace\.py", re.MULTILINE),
            "Trace row invokes check_trace.py via python3",
        )
        self.assertRegex(
            t,
            re.compile(r"^\|\s*Graph\s*\|.*python3\s+\S*check_graph\.py --verify", re.MULTILINE),
            "Graph row invokes check_graph.py --verify via python3",
        )

    def test_pre_push_hook_template_runs_both_python_linters(self):
        """The pre-push hook template runs check_trace.py and check_graph.py --verify."""
        t = _read("templates/githooks/pre-push")
        self.assertRegex(t, r"python3\s+\S*check_trace\.py", "pre-push runs check_trace.py")
        self.assertRegex(
            t, r"python3\s+\S*check_graph\.py --verify", "pre-push runs check_graph.py --verify"
        )


class SetupRepoWiringTest(unittest.TestCase):
    def test_setup_repo_vendors_the_linters_and_reports_drift(self):
        """setup-repo vendors the linters and reports drift."""
        t = _read("skills/setup/setup-repo/SKILL.md")
        self.assertRegex(t, r"vendor_linters\.py --install", "setup-repo installs the linters")
        self.assertRegex(t, r"vendor_linters\.py --check", "setup-repo checks for drift")
        self.assertRegex(
            t, re.compile(r"drift[\s\S]{0,240}offer to update", _I),
            "drift is reported and an update offered",
        )

    def test_ci_opt_in_appends_the_graph_lint_additively(self):
        """The CI opt-in appends the graph lint additively."""
        t = _read("skills/setup/setup-repo/SKILL.md")
        at = t.find("checks in CI")
        self.assertNotEqual(at, -1, "guard: the CI opt-in section exists")
        opt_in = t[at:at + 600]
        self.assertRegex(opt_in, r"check_graph\.py --verify", "the graph lint is appended to CI")
        self.assertRegex(
            opt_in, re.compile(r"do not author a new pipeline", _I),
            "still additive, no new pipeline",
        )

    def test_proving_gate_seeds_graph_md_and_dead_linters_are_wiring_failures(self):
        """The proving gate seeds GRAPH.md and treats an unrunnable linter as a wiring failure."""
        t = _read("skills/setup/setup-repo/SKILL.md")
        self.assertRegex(t, r"check_graph\.py --harvest", "seeds GRAPH.md once")
        self.assertRegex(
            t, re.compile(r"check_graph\.py[\s\S]{0,300}wiring failure", _I),
            "a check-graph that cannot execute is a wiring failure",
        )
        self.assertRegex(
            t,
            re.compile(r"check_trace\.py[\s\S]{0,250}python3[\s\S]{0,150}wiring failure", _I),
            "a dead python3 interpreter running check_trace.py is a wiring failure",
        )


class VerifyWiringTest(unittest.TestCase):
    def test_verify_runs_the_python_linters_with_runnable_commands(self):
        """verify runs check_graph.py --verify and names check_trace.py, both runnable."""
        t = _read("skills/execution/verify/SKILL.md")
        self.assertRegex(t, r"python3\s+\S*check_graph\.py --verify", "runs check_graph.py --verify")
        self.assertRegex(t, r"check_trace\.py", "names check_trace.py")


class CodeReviewWiringTest(unittest.TestCase):
    def test_code_review_runs_the_duplication_query_and_fails_open(self):
        """code-review runs the duplication query and fails open."""
        t = _read("skills/review/code-review/SKILL.md")
        self.assertRegex(t, r"check_graph\.py --query", "code-review calls the query on changed files")
        self.assertRegex(t, re.compile(r"overlap check unavailable", _I), "fail-open note")

    def test_spec_subagent_gets_neighbor_cards_and_a_reuse_miss_directive(self):
        """Spec subagent gets neighbor cards and a reuse-miss directive."""
        t = _read("skills/review/code-review/SKILL.md")
        self.assertRegex(t, re.compile(r"overlapping feature", _I), "overlapping features named")
        self.assertRegex(t, re.compile(r"neighbor cards", _I), "neighbor cards injected into the Spec brief")
        self.assertRegex(t, re.compile(r"reuse-miss", _I), "reuse-miss finding directive")
        self.assertRegex(t, re.compile(r"reimplement", _I), "cites reimplementing neighbor behavior")

    def test_no_overlap_statement(self):
        """code-review states the no-overlap case and injects nothing."""
        t = _read("skills/review/code-review/SKILL.md")
        self.assertRegex(t, re.compile(r"no existing feature shares", _I), "states no overlap and injects nothing")

    def test_two_axis_review_is_preserved(self):
        """The two-axis (Standards / Spec) review is preserved."""
        t = _read("skills/review/code-review/SKILL.md")
        self.assertRegex(t, r"\*\*Standards subagent\*\*", "Standards subagent still present")
        self.assertRegex(t, r"\*\*Spec subagent\*\*", "Spec subagent still present")


class GraphFailOpenTest(unittest.TestCase):
    def test_graph_query_still_fails_open(self):
        """brainstorm and code-review continue when the graph linter is absent."""
        for rel in ("skills/discovery/brainstorm/SKILL.md", "skills/review/code-review/SKILL.md"):
            t = _read(rel)
            self.assertRegex(
                t,
                re.compile(r"check_graph\.py[\s\S]{0,40}absent", _I),
                f"{rel}: names check_graph.py as possibly absent",
            )
            self.assertRegex(
                t, re.compile(r"overlap check unavailable", _I), f"{rel}: fail-open note present"
            )
            self.assertRegex(
                t, re.compile(r"never block|continue", _I), f"{rel}: still fails open, never blocks"
            )


class InstallDocsWiringTest(unittest.TestCase):
    def test_readme_has_a_node_free_install(self):
        """README documents git clone + link-skills.sh and states no Node runtime is required."""
        t = _read("README.md")
        self.assertRegex(t, re.compile(r"no node runtime", _I), "states no Node runtime required")
        self.assertRegex(t, r"git clone", "documents git clone")
        self.assertRegex(t, r"link-skills\.sh", "documents link-skills.sh")

    def test_design_md_inventory_lists_the_linters_and_graph_md(self):
        """DESIGN.md's script inventory and artifact model name the Python linters and GRAPH.md."""
        t = _read("DESIGN.md")
        self.assertRegex(t, r"check_trace\.py", "script inventory lists check_trace.py")
        self.assertRegex(t, r"check_graph\.py", "script inventory lists check_graph.py")
        self.assertRegex(t, r"vendor_linters\.py", "script inventory lists vendor_linters.py")
        self.assertRegex(t, r"docs/specs/GRAPH\.md", "artifact model lists docs/specs/GRAPH.md")


class NoStaleLinterReferencesTest(unittest.TestCase):
    """The anti-drift guard: no skill, doc, or template may name a retired `.mjs`
    linter. Scans the whole consumer-facing tree (skills, templates, docs, and
    the two root docs) so a stale `check-trace.mjs` / `check-graph.mjs` /
    `vendor-linters.mjs` reference can never reappear undetected. `scripts/` is
    deliberately not scanned: this test file itself must name those strings to
    forbid them."""

    _FORBIDDEN = re.compile(r"(check-trace|check-graph|vendor-linters)\.mjs")
    _ROOTS = ("skills", "templates", "docs")
    _ROOT_FILES = ("README.md", "DESIGN.md")

    def _offenders(self, text):
        return sorted(set(self._FORBIDDEN.findall(text)))

    def test_no_mjs_linter_reference_anywhere_in_the_tree(self):
        hits = []
        for root in self._ROOTS:
            base = os.path.join(_REPO_ROOT, root)
            for dirpath, dirnames, filenames in os.walk(base):
                dirnames[:] = [d for d in dirnames if not d.startswith(".")]
                for name in filenames:
                    full = os.path.join(dirpath, name)
                    try:
                        text = open(full, "r", encoding="utf-8").read()
                    except (OSError, UnicodeDecodeError):
                        continue
                    if self._FORBIDDEN.search(text):
                        hits.append(os.path.relpath(full, _REPO_ROOT))
        for rel in self._ROOT_FILES:
            if self._FORBIDDEN.search(_read(rel)):
                hits.append(rel)
        self.assertEqual(
            hits, [], f"retired .mjs linter reference(s) found in: {sorted(set(hits))}"
        )


if __name__ == "__main__":
    unittest.main()
