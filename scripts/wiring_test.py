"""Port of scripts/check-graph.wiring.test.mjs (the oracle) — SKILL.md and
template marker assertions for the feature-graph wiring across brainstorm,
sync-spec, setup-repo, code-review, verify, and the shipped templates.

Ported from scripts/check-graph.wiring.test.mjs. Expected patterns are copied
from the oracle's own regexes, never invented fresh from reading the target
files under test.

No requirement ID this file needs is a Fixture ID: every `[FGRAPH-N.M]` tag
below is a genuine Citation for a real assertion, so none is assembled at
runtime — the brief's "assemble Fixture IDs at runtime" rule does not apply
here because this file introduces no example/test-data ID, only real ones.
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
        """[FGRAPH-7.1][FGRAPH-7.2][FGRAPH-7.5][FGRAPH-9.6] brainstorm wires the graph query."""
        t = _read("skills/discovery/brainstorm/SKILL.md")
        # Task 11 (PYPORT-4.3) rewired this surface onto the Python linter; pin the
        # Python form rather than the retired `.mjs` invocation.
        self.assertRegex(t, r"check_graph\.py --query", "FGRAPH-7.1: brainstorm calls the query")
        self.assertRegex(t, re.compile(r"card", _I), "FGRAPH-7.2: presents cards")
        self.assertRegex(
            t, re.compile(r"overlap check unavailable", _I), "FGRAPH-7.5/9.6: fail-open note"
        )

    def test_brainstorm_step1_done_when_states_overlaps(self):
        """[FGRAPH-7.3][FGRAPH-7.4] brainstorm step-1 Done-when states overlaps."""
        t = _read("skills/discovery/brainstorm/SKILL.md")
        self.assertRegex(
            t,
            re.compile(r"share[sd]? .*surface|no existing feature", _I),
            "FGRAPH-7.3/7.4: state overlaps or none",
        )


class SyncSpecWiringTest(unittest.TestCase):
    def test_sync_spec_regenerates_and_stages_graph_md(self):
        """[FGRAPH-8.1][FGRAPH-8.2] sync-spec regenerates and stages GRAPH.md."""
        t = _read("skills/track/sync-spec/SKILL.md")
        self.assertRegex(t, r"check-graph(?:\.mjs)? --harvest", "FGRAPH-8.1: regenerates")
        self.assertRegex(
            t,
            re.compile(r"GRAPH\.md[\s\S]{0,40}stage it into this sync-spec commit", _I),
            "FGRAPH-8.2: stages GRAPH.md into the commit",
        )


class SetupRepoRemedyWiringTest(unittest.TestCase):
    def test_names_setup_repo_as_the_remedy_once_and_still_fails_open(self):
        """[FGRAPH-11.10][FGRAPH-11.11][FGRAPH-11.12] brainstorm and code-review name
        setup-repo as the remedy, once, and still fail open."""
        for rel in ("skills/discovery/brainstorm/SKILL.md", "skills/review/code-review/SKILL.md"):
            t = _read(rel)
            self.assertRegex(
                t, re.compile(r"not installed[\s\S]{0,160}setup-repo", _I),
                f"{rel}: FGRAPH-11.10 remedy names setup-repo",
            )
            self.assertRegex(
                t, re.compile(r"once per session", _I),
                f"{rel}: FGRAPH-11.11 the remedy is stated once, not every query",
            )
            self.assertRegex(
                t, re.compile(r"never block|continue", _I),
                f"{rel}: FGRAPH-11.12 still fails open",
            )


class TemplatesWiringTest(unittest.TestCase):
    def test_spec_templates_demand_no_new_fields_for_the_graph(self):
        """[FGRAPH-11.13] the spec templates demand no new fields for the graph."""
        for rel in ("templates/requirements.md", "templates/design.md", "templates/tasks.md"):
            t = _read(rel)
            self.assertNotRegex(
                t,
                re.compile(r"check-graph|GRAPH\.md", _I),
                f"{rel} must not require graph annotations (no authoring burden)",
            )

    def test_project_md_template_carries_a_graph_row_beside_the_trace_row(self):
        """[FGRAPH-11.4] the project.md template carries a Graph row beside the Trace row."""
        # Task 11 (PYPORT-4.1) rewired this surface onto the Python linters; pin the
        # Python form rather than the retired `.mjs` invocation.
        t = _read("templates/agents/project.md")
        self.assertRegex(
            t, re.compile(r"^\|\s*Trace\s*\|.*check_trace\.py", re.MULTILINE),
            "guard: the Trace row still exists",
        )
        self.assertRegex(
            t, re.compile(r"^\|\s*Graph\s*\|.*check_graph\.py --verify", re.MULTILINE),
            "FGRAPH-11.4: a Graph row runs check-graph --verify",
        )

    def test_pre_push_hook_template_runs_both_linters(self):
        """[FGRAPH-11.5] the pre-push hook template runs both linters."""
        # Task 11 (PYPORT-4.2) rewired this surface onto the Python linters; pin the
        # Python form rather than the retired `.mjs` invocation.
        t = _read("templates/githooks/pre-push")
        self.assertRegex(t, r"check_trace\.py", "guard: the trace lint still runs")
        self.assertRegex(t, r"check_graph\.py --verify", "FGRAPH-11.5: the graph freshness lint runs too")


class SetupRepoWiringTest(unittest.TestCase):
    def test_setup_repo_vendors_the_linters_and_reports_drift(self):
        """[FGRAPH-11.1][FGRAPH-11.3] setup-repo vendors the linters and reports drift."""
        # Task 11 (PYPORT-4.3) rewired this surface onto the Python linters; pin the
        # Python form rather than the retired `.mjs` invocation.
        t = _read("skills/setup/setup-repo/SKILL.md")
        self.assertRegex(t, r"vendor_linters\.py --install", "FGRAPH-11.1: setup-repo installs the linters")
        self.assertRegex(t, r"vendor_linters\.py --check", "FGRAPH-11.3: setup-repo checks for drift")
        self.assertRegex(
            t, re.compile(r"drift[\s\S]{0,240}offer to update", _I),
            "FGRAPH-11.3: drift is reported and an update offered",
        )

    def test_ci_opt_in_appends_the_graph_lint_additively(self):
        """[FGRAPH-11.6][FGRAPH-11.7] the CI opt-in appends the graph lint additively."""
        t = _read("skills/setup/setup-repo/SKILL.md")
        at = t.find("checks in CI")
        self.assertNotEqual(at, -1, "guard: the CI opt-in section exists")
        opt_in = t[at:at + 600]
        self.assertRegex(opt_in, r"check_graph\.py --verify", "FGRAPH-11.6: the graph lint is appended to CI")
        self.assertRegex(
            opt_in, re.compile(r"do not author a new pipeline", _I),
            "FGRAPH-11.7: still additive, no new pipeline",
        )

    def test_proving_gate_seeds_graph_md_and_dead_check_graph_is_a_wiring_failure(self):
        """[FGRAPH-11.8][FGRAPH-11.9] the proving gate seeds GRAPH.md and treats a dead
        check-graph as a wiring failure."""
        t = _read("skills/setup/setup-repo/SKILL.md")
        self.assertRegex(t, r"check_graph\.py --harvest", "FGRAPH-11.8: seeds GRAPH.md once")
        self.assertRegex(
            t, re.compile(r"check_graph\.py[\s\S]{0,300}wiring failure", _I),
            "FGRAPH-11.9: a check-graph that cannot execute is a wiring failure",
        )


class VerifyWiringTest(unittest.TestCase):
    def test_verify_runs_check_graph_verify_with_a_runnable_command(self):
        """[FGRAPH-6.4] verify runs check-graph --verify with a runnable command."""
        # The bare `check-graph` binary does not exist on PATH; every consumer must
        # spell the real invocation. Rejects the old broken form rather than
        # enshrining it. Task 11 (PYPORT-4.3) rewired this surface onto the Python
        # linter; pin the Python form rather than the retired `node ... .mjs` one.
        self.assertRegex(
            _read("skills/execution/verify/SKILL.md"), r"python3\s+\S*check_graph\.py --verify"
        )


class CodeReviewWiringTest(unittest.TestCase):
    def test_code_review_runs_the_duplication_query_and_fails_open(self):
        """[FGRAPH-10.1][FGRAPH-10.5] code-review runs the duplication query and fails open."""
        # Task 11 (PYPORT-4.3) rewired this surface onto the Python linter; pin the
        # Python form rather than the retired `.mjs` invocation.
        t = _read("skills/review/code-review/SKILL.md")
        self.assertRegex(t, r"check_graph\.py --query", "FGRAPH-10.1: code-review calls the query on changed files")
        self.assertRegex(t, re.compile(r"overlap check unavailable", _I), "FGRAPH-10.5: fail-open note")

    def test_spec_subagent_gets_neighbor_cards_and_a_reuse_miss_directive(self):
        """[FGRAPH-10.2][FGRAPH-10.3] Spec subagent gets neighbor cards and a reuse-miss directive."""
        t = _read("skills/review/code-review/SKILL.md")
        self.assertRegex(t, re.compile(r"overlapping feature", _I), "FGRAPH-10.2: overlapping features named")
        self.assertRegex(t, re.compile(r"neighbor cards", _I), "FGRAPH-10.2: neighbor cards injected into the Spec brief")
        self.assertRegex(t, re.compile(r"reuse-miss", _I), "FGRAPH-10.3: reuse-miss finding directive")
        self.assertRegex(t, re.compile(r"reimplement", _I), "FGRAPH-10.3: cites reimplementing neighbor behavior")

    def test_no_overlap_statement(self):
        """[FGRAPH-10.4] no-overlap statement."""
        t = _read("skills/review/code-review/SKILL.md")
        self.assertRegex(t, re.compile(r"no existing feature shares", _I), "FGRAPH-10.4: states no overlap and injects nothing")

    def test_two_axis_review_is_preserved(self):
        """[FGRAPH-10.6] two-axis review is preserved."""
        t = _read("skills/review/code-review/SKILL.md")
        self.assertRegex(t, r"\*\*Standards subagent\*\*", "FGRAPH-10.6: Standards subagent still present")
        self.assertRegex(t, r"\*\*Spec subagent\*\*", "FGRAPH-10.6: Spec subagent still present")


class PythonConsumerSurfacesWiringTest(unittest.TestCase):
    """Port of scripts/check-graph.wiring.test.mjs's Python-era additions (Task 11).

    These assert the consumer surfaces (templates, skills, README, DESIGN.md) name
    the Python linters — `scripts/check_trace.py`, `scripts/check_graph.py`,
    `scripts/vendor_linters.py` — invoked with `python3`, rather than the retiring
    `.mjs` forms. No requirement ID here is a Fixture ID: every `[PYPORT-N.M]` tag
    is a genuine Citation for a real assertion below.
    """

    def test_project_md_template_names_the_interpreter(self):
        """[PYPORT-4.1] the Trace and Graph rows invoke the Python linters."""
        t = _read("templates/agents/project.md")
        self.assertRegex(
            t,
            re.compile(r"^\|\s*Trace\s*\|.*python3\s+\S*check_trace\.py", re.MULTILINE),
            "PYPORT-4.1: Trace row invokes check_trace.py via python3",
        )
        self.assertRegex(
            t,
            re.compile(r"^\|\s*Graph\s*\|.*python3\s+\S*check_graph\.py --verify", re.MULTILINE),
            "PYPORT-4.1: Graph row invokes check_graph.py --verify via python3",
        )

    def test_pre_push_runs_both_python_linters(self):
        """[PYPORT-4.2] the hook template runs check_trace.py and check_graph.py --verify."""
        t = _read("templates/githooks/pre-push")
        self.assertRegex(t, r"python3\s+\S*check_trace\.py", "PYPORT-4.2: pre-push runs check_trace.py")
        self.assertRegex(
            t, r"python3\s+\S*check_graph\.py --verify", "PYPORT-4.2: pre-push runs check_graph.py --verify"
        )

    def test_skills_name_the_python_linters(self):
        """[PYPORT-4.3] setup-repo, brainstorm, code-review, verify all name the .py linters."""
        setup_repo = _read("skills/setup/setup-repo/SKILL.md")
        self.assertRegex(setup_repo, r"vendor_linters\.py --install", "setup-repo: python vendor install")
        self.assertRegex(setup_repo, r"vendor_linters\.py --check", "setup-repo: python vendor check")
        self.assertRegex(setup_repo, r"check_trace\.py", "setup-repo: names check_trace.py")
        self.assertRegex(setup_repo, r"check_graph\.py --harvest", "setup-repo: names check_graph.py --harvest")
        self.assertRegex(setup_repo, r"check_graph\.py --verify", "setup-repo: names check_graph.py --verify")
        self.assertNotRegex(setup_repo, r"vendor-linters\.mjs", "setup-repo: no stale .mjs vendor command")

        brainstorm = _read("skills/discovery/brainstorm/SKILL.md")
        self.assertRegex(brainstorm, r"check_graph\.py --query", "brainstorm: names check_graph.py --query")
        self.assertNotRegex(brainstorm, r"check-graph\.mjs", "brainstorm: no stale .mjs invocation")

        code_review = _read("skills/review/code-review/SKILL.md")
        self.assertRegex(code_review, r"check_graph\.py --query", "code-review: names check_graph.py --query")
        self.assertNotRegex(code_review, r"check-graph\.mjs", "code-review: no stale .mjs invocation")

        verify = _read("skills/execution/verify/SKILL.md")
        self.assertRegex(verify, r"check_trace\.py", "verify: names check_trace.py")
        self.assertRegex(verify, r"check_graph\.py --verify", "verify: names check_graph.py --verify")
        self.assertNotRegex(verify, r"check-graph\.mjs|check-trace\.mjs", "verify: no stale .mjs invocation")

    def test_readme_has_a_node_free_install(self):
        """[PYPORT-4.4] README documents git clone + link-skills.sh or the plugin."""
        t = _read("README.md")
        self.assertRegex(t, re.compile(r"no node runtime", _I), "PYPORT-4.4: states no Node runtime required")
        self.assertRegex(t, r"git clone", "PYPORT-4.4: documents git clone")
        self.assertRegex(t, r"link-skills\.sh", "PYPORT-4.4: documents link-skills.sh")

    def test_design_md_inventory_lists_the_linters_and_graph_md(self):
        """[PYPORT-4.5] DESIGN.md's script inventory and artifact model are current."""
        t = _read("DESIGN.md")
        self.assertRegex(t, r"check_trace\.py", "PYPORT-4.5: script inventory lists check_trace.py")
        self.assertRegex(t, r"check_graph\.py", "PYPORT-4.5: script inventory lists check_graph.py")
        self.assertRegex(t, r"vendor_linters\.py", "PYPORT-4.5: script inventory lists vendor_linters.py")
        self.assertRegex(t, r"docs/specs/GRAPH\.md", "PYPORT-4.5: artifact model lists docs/specs/GRAPH.md")

    def test_setup_repo_treats_a_dead_interpreter_as_a_wiring_failure(self):
        """[PYPORT-4.6] the proving gate classifies an unrunnable linter as wiring."""
        t = _read("skills/setup/setup-repo/SKILL.md")
        self.assertRegex(
            t,
            re.compile(r"check_trace\.py[\s\S]{0,250}python3[\s\S]{0,150}wiring failure", _I),
            "PYPORT-4.6: a dead python3 interpreter running check_trace.py is a wiring failure",
        )

    def test_spec_templates_demand_no_new_fields(self):
        """[PYPORT-5.5] no graph/linter annotation is required in the spec triad."""
        for rel in ("templates/requirements.md", "templates/design.md", "templates/tasks.md"):
            t = _read(rel)
            self.assertNotRegex(
                t,
                re.compile(r"check[-_](trace|graph)|vendor[-_]linters|GRAPH\.md", _I),
                f"{rel} must not require any linter/graph annotation (no authoring burden)",
            )

    def test_shell_scripts_stay_dependency_free(self):
        """[PYPORT-5.6] task-brief, review-package, link-skills.sh, session-start.sh are bash."""
        for rel in (
            "scripts/task-brief",
            "scripts/review-package",
            "scripts/link-skills.sh",
            "templates/session-start.sh",
        ):
            t = _read(rel)
            self.assertTrue(
                t.startswith("#!/usr/bin/env bash"),
                f"{rel} must keep its bash shebang (stays dependency-free)",
            )
            # A comment may *mention* python (e.g. "no node/jq/python" to explain why
            # none is needed) — what must never appear is an actual invocation of it.
            self.assertNotRegex(
                t, r"(?m)^[^#\n]*\bpython3?\b", f"{rel} must not invoke a Python interpreter"
            )

    def test_graph_query_still_fails_open(self):
        """[PYPORT-5.7] brainstorm and code-review continue when the graph linter is absent."""
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


if __name__ == "__main__":
    unittest.main()
