"""FSUB-1.1 FSUB-1.2 FSUB-1.3 FSUB-1.4 FSUB-1.12 FSUB-1.15 FSUB-4.1 FSUB-4.2
FSUB-6.1 FSUB-6.2 FSUB-6.3 FSUB-6.4 FSUB-6.5 FSUB-6.6 FSUB-7.1 FSUB-7.2
FSUB-7.3 FSUB-7.4 FSUB-7.5 FSUB-7.6 FSUB-7.7 — skill and wiring contracts.

FSUBR callers / grounded claims / package validity:
FSUBR-4.1 FSUBR-4.2 FSUBR-4.3 FSUBR-4.4 FSUBR-5.1 FSUBR-5.2 FSUBR-5.3
FSUBR-6.1 FSUBR-7.1 FSUBR-7.2 FSUBR-8.1 FSUBR-8.2 FSUBR-9.8 FSUBR-9.11
FSUBR-9.12 FSUBR-9.13 FSUBR-9.14 FSUBR-9.15

FSUBR guide / inventory / carry-forward guards:
FSUBR-9.1 FSUBR-9.2 FSUBR-9.4 FSUBR-9.5 FSUBR-9.6 FSUBR-9.7 FSUBR-9.9
FSUBR-9.10 FSUBR-10.2
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "execution" / "load-subgraph" / "SKILL.md"
PASSES = ROOT / "skills" / "execution" / "load-subgraph" / "references" / "passes.md"
ENV = ROOT / "skills" / "execution" / "load-subgraph" / "references" / "envelope.md"
GROUNDED = (
    ROOT / "skills" / "execution" / "load-subgraph" / "references" / "grounded-claims.md"
)
MAP = ROOT / "skills" / "track" / "map-features" / "SKILL.md"
FRAME = ROOT / "skills" / "discovery" / "frame-change" / "SKILL.md"
INSPECT = ROOT / "skills" / "review" / "inspect-change" / "SKILL.md"
CLARIFY = ROOT / "skills" / "discovery" / "clarify-decisions" / "SKILL.md"
DESIGN = ROOT / "skills" / "spec" / "design-solution" / "SKILL.md"
PLAN = ROOT / "skills" / "spec" / "plan-tasks" / "SKILL.md"
ROOT_CAUSE = ROOT / "skills" / "execution" / "root-cause" / "SKILL.md"
CALLERS = (FRAME, INSPECT, CLARIFY, DESIGN, PLAN, ROOT_CAUSE)
TEMPLATE = ROOT / "templates" / "tasks.md"
FEATURE_GRAPH = ROOT / "docs" / "guide" / "concepts" / "feature-graph.md"
START_HERE = ROOT / "docs" / "guide" / "START-HERE.md"
SKILLS_README = ROOT / "docs" / "guide" / "skills" / "README.md"
LOAD_SUBGRAPH_GUIDE = ROOT / "docs" / "guide" / "skills" / "load-subgraph.md"
AGENTS = ROOT / "AGENTS.md"
ARCH_SKILLS = ROOT / "docs" / "architecture" / "skills.md"
ARCH_WORKFLOWS = ROOT / "docs" / "architecture" / "workflows.md"
AUDIT_TRACE = ROOT / "skills" / "execution" / "audit-trace" / "SKILL.md"
SCENARIOS = ROOT / "tests" / "feature-subgraph" / "scenarios.md"
PRESSURE = ROOT / "tests" / "feature-subgraph" / "scenarios-pressure.md"
BUILD_WAVES = ROOT / "skills" / "execution" / "build-in-waves" / "SKILL.md"
BUILD_STORY = ROOT / "skills" / "execution" / "build-by-story" / "SKILL.md"
BUILD_INLINE = ROOT / "skills" / "execution" / "build-inline" / "SKILL.md"


class TestLoadSubgraphSkill(unittest.TestCase):
    def test_FSUB_1_1_skill_exists_model_invoked(self):
        self.assertTrue(SKILL.is_file())
        text = SKILL.read_text()
        self.assertRegex(text, re.compile(r"^name:\s*load-subgraph\s*$", re.M))
        self.assertNotIn("disable-model-invocation: true", text)

    def test_FSUB_1_1_no_python_under_skill_package(self):
        pkg = ROOT / "skills" / "execution" / "load-subgraph"
        py = list(pkg.rglob("*.py"))
        self.assertEqual(py, [], f"unexpected python under skill: {py}")

    def test_FSUB_1_2_skill_names_only_passes_md_procedure(self):
        text = SKILL.read_text()
        self.assertIn("passes.md", text)
        self.assertNotRegex(text, r"(?i)import\s+reference_derive")
        self.assertTrue(
            re.search(r"two independent runs|same edge set|Determinism", text, re.I),
            "skill must state dual-run / determinism",
        )

    def test_FSUB_1_3_forbids_graph_materialization(self):
        text = SKILL.read_text() + PASSES.read_text()
        self.assertRegex(text, r"GRAPH\.md|graph file|projection", re.I)
        self.assertRegex(text, r"do not produce a file|never write|NO GRAPH FILE|no projection", re.I)

    def test_FSUB_1_12_advisory_not_a_gate(self):
        text = SKILL.read_text()
        self.assertRegex(text, r"advisory|not a hard gate|NO GATE FROM THIN", re.I)

    def test_FSUB_7_4_pathfind_separate(self):
        text = SKILL.read_text()
        self.assertRegex(text, re.compile(r"pathfind", re.I))

    def test_FSUB_1_10_queries_named(self):
        text = PASSES.read_text() + SKILL.read_text()
        for q in ("neighbors", "ancestors", "descendants", "blast_radius", "subgraph"):
            self.assertIn(q, text)

    def test_FSUB_passes_are_primitive_recipes_not_prose_only(self):
        text = PASSES.read_text()
        for token in (
            "Pass R",
            "Pass P1",
            "Pass P0",
            "Pass P2",
            "NEIGHBORS_MAX",
            "P0_SEED_MAX",
            "12",
            "Truncate once",
            "Union",
        ):
            self.assertIn(token, text)
        # Must not point shipped skill at test-side oracle as SSOT
        self.assertNotIn("tests/feature-subgraph/reference_derive.py", text)

    def test_FSUB_envelope_documents_owns_coverage(self):
        text = ENV.read_text()
        self.assertIn("owns_coverage", text)
        self.assertIn("advisory", text)

    def test_FSUB_skill_has_iron_law_and_red_flags(self):
        text = SKILL.read_text()
        self.assertIn("The Iron Law", text)
        self.assertIn("Red Flags", text)
        self.assertIn("owns_coverage", text)


class TestMapFeaturesSkill(unittest.TestCase):
    def test_FSUB_6_1_user_invoked_at_track_path(self):
        self.assertTrue(MAP.is_file())
        text = MAP.read_text()
        self.assertRegex(text, re.compile(r"^name:\s*map-features\s*$", re.M))
        self.assertIn("disable-model-invocation: true", text)

    def test_FSUB_6_2_through_6_6_proposal_rules(self):
        text = MAP.read_text()
        self.assertRegex(text, r"Feature code", re.I)
        self.assertRegex(text, r"ROAD|Roadmap", re.I)
        self.assertRegex(text, r"Files edit|tasks\.md", re.I)
        self.assertRegex(text, r"DEPENDS_ON|Depends-on|Consumes", re.I)
        self.assertRegex(text, r"confirm", re.I)
        self.assertRegex(text, r"MUST NOT auto|Auto-writing|without explicit confirm", re.I)
        self.assertRegex(text, r"slug|directory", re.I)
        self.assertRegex(text, r"/map-features")
        self.assertIn("Rationalization", text)
        self.assertIn("Red Flags", text)
        self.assertNotRegex(
            text,
            re.compile(r"^description:.*Use when", re.M | re.I),
        )


class TestCallersAndGrammar(unittest.TestCase):
    def test_FSUB_1_15_frame_change_uses_load_subgraph(self):
        text = FRAME.read_text()
        self.assertIn("load-subgraph", text)

    def test_FSUB_1_15_inspect_change_uses_load_subgraph(self):
        text = INSPECT.read_text()
        self.assertIn("load-subgraph", text)

    def test_FSUB_4_1_4_2_hardened_files_grammar(self):
        plan = PLAN.read_text()
        tmpl = TEMPLATE.read_text()
        combined = plan + tmpl
        self.assertIn("`", tmpl)  # backticks in template example
        self.assertRegex(combined, r"backtick|`path`|glued|path:lines|not glued", re.I)
        self.assertIn("Depends-on", plan)
        self.assertIn("Files:", plan)

    def test_FSUB_7_5_feature_graph_mentions_load_subgraph(self):
        text = FEATURE_GRAPH.read_text()
        self.assertIn("load-subgraph", text)

    def test_FSUB_all_requirement_ids_in_scenarios(self):
        req = (ROOT / "docs/specs/2026-08-01-feature-subgraph/requirements.md").read_text()
        ids = set(re.findall(r"\*\*(FSUB-\d+\.\d+)\*\*", req))
        scenarios = SCENARIOS.read_text()
        missing = sorted(i for i in ids if i not in scenarios)
        self.assertEqual(missing, [], f"missing from scenarios: {missing}")

    def test_FSUB_inventory_lists_both_skills(self):
        agents = (ROOT / "AGENTS.md").read_text()
        self.assertIn("load-subgraph", agents)
        self.assertIn("map-features", agents)


class TestFSUBRCallerSkills(unittest.TestCase):
    """FSUBR-4.* FSUBR-5.* FSUBR-6.1 FSUBR-7.* FSUBR-8.* FSUBR-9.8/11–15 prose anchors."""

    def test_FSUBR_9_8_frame_and_inspect_neighbors_schema_1_1(self):
        """FSUBR-9.8 frame-change and inspect-change use load-subgraph schema 1.1."""
        for path in (FRAME, INSPECT):
            text = path.read_text()
            self.assertIn("load-subgraph", text)
            self.assertRegex(text, r"schema[_\s-]*version|schema 1\.1|1\.1", re.I)
            self.assertRegex(text, r"path_evidence|term_evidence|via_traces", re.I)

    def test_FSUBR_4_1_grounded_claims_code_edge_path_or_term(self):
        """FSUBR-4.1 grounded claims cite CODE + edge/trace kind + path or term.

        One home: references/grounded-claims.md holds the recipe; callers point at it.
        """
        self.assertTrue(GROUNDED.is_file(), "grounded-claims.md is the one home")
        home = GROUNDED.read_text()
        self.assertRegex(
            home,
            re.compile(
                r"CODE.{0,80}(edge|trace).{0,80}(path|term)|"
                r"feature \*\*CODE\*\*.{0,80}(edge|trace).{0,80}(path|term)",
                re.I | re.S,
            ),
            "grounded-claims.md must require CODE+edge+path/term",
        )
        for path in CALLERS:
            text = path.read_text()
            self.assertRegex(
                text,
                re.compile(r"grounded-claims\.md", re.I),
                f"{path.name} must point at grounded-claims.md (one home)",
            )

    def test_FSUBR_4_2_owns_coverage_before_absence(self):
        """FSUBR-4.2 state exact owns_coverage before absence conclusion (one home)."""
        home = GROUNDED.read_text()
        self.assertIn("owns_coverage", home)
        self.assertRegex(
            home,
            re.compile(
                r"with_owns\s*<\s*registered|"
                r"owns_coverage.{0,120}(with_owns|registered)|"
                r"exact.{0,40}owns_coverage",
                re.I | re.S,
            ),
            "grounded-claims.md must require exact owns_coverage before absence",
        )
        for path in (FRAME, INSPECT):
            text = path.read_text()
            self.assertIn("owns_coverage", text)
            self.assertIn("grounded-claims.md", text)

    def test_FSUBR_4_3_empty_before_absence(self):
        """FSUBR-4.3 state emptiness before absence conclusion (one home)."""
        home = GROUNDED.read_text()
        self.assertRegex(
            home,
            re.compile(
                r"empt(y|iness).{0,80}(before|absence|first)|"
                r"state that empt|empty.{0,40}(neighbor|cluster|result)",
                re.I | re.S,
            ),
            "grounded-claims.md must require stating emptiness before absence",
        )
        for path in (FRAME, INSPECT):
            self.assertIn("grounded-claims.md", path.read_text())

    def test_FSUBR_4_4_advisory_no_invent(self):
        """FSUBR-4.4 advisory only — do not invent Reuse/Respects/Files/hypotheses."""
        home = GROUNDED.read_text()
        self.assertRegex(
            home,
            re.compile(
                r"advis(ory|ory input)|never invent|not invent",
                re.I,
            ),
            "grounded-claims.md must treat retrieval as advisory / no invent",
        )
        for path in (FRAME, INSPECT, DESIGN, PLAN, ROOT_CAUSE):
            text = path.read_text()
            self.assertRegex(
                text,
                re.compile(
                    r"grounded-claims\.md|advis(ory|ory input)|not invent|"
                    r"SHALL NOT invent|never invent",
                    re.I,
                ),
                f"{path.name} must point at home or restate advisory/no invent",
            )

    def test_FSUBR_5_1_5_2_5_3_clarify_nested_standalone_rederive(self):
        """FSUBR-5.1–5.3 nested reuse if valid; standalone load once; rederive on change."""
        text = CLARIFY.read_text()
        self.assertIn("load-subgraph", text)
        self.assertRegex(text, re.compile(r"\bnested\b", re.I))
        self.assertRegex(text, re.compile(r"\bstandalone\b", re.I))
        self.assertRegex(
            text,
            re.compile(
                r"reuse.{0,80}(package|valid|fingerprint)|"
                r"(package|valid|fingerprint).{0,80}reuse",
                re.I | re.S,
            ),
        )
        self.assertRegex(
            text,
            re.compile(
                r"standalone.{0,120}(once|load)|load.{0,40}once.{0,80}"
                r"(first|card|interview)",
                re.I | re.S,
            ),
        )
        self.assertRegex(
            text,
            re.compile(
                r"rederive|re-derive",
                re.I,
            ),
        )
        self.assertRegex(
            text,
            re.compile(
                r"(source|scope|term|path|fingerprint).{0,60}(change|differ)|"
                r"(change|differ).{0,60}(source|scope|term|path|fingerprint)",
                re.I | re.S,
            ),
        )

    def test_FSUBR_6_1_design_step1_fresh_retrieval(self):
        """FSUBR-6.1 design-solution Step 1 fresh retrieval before reuse ladder."""
        text = DESIGN.read_text()
        self.assertIn("load-subgraph", text)
        # Step 1 section should mention retrieval / load-subgraph
        step1 = re.search(
            r"## Step 1:.*?(?=## Step 2:|\Z)",
            text,
            re.S | re.I,
        )
        self.assertIsNotNone(step1, "design-solution must have Step 1 section")
        s1 = step1.group(0)
        self.assertRegex(s1, re.compile(r"load-subgraph|retrieval", re.I))
        self.assertRegex(
            text,
            re.compile(
                r"fresh.{0,40}(retrieval|load-subgraph)|"
                r"(retrieval|load-subgraph).{0,40}fresh",
                re.I | re.S,
            ),
        )
        self.assertRegex(
            text,
            re.compile(r"reuse ladder|before the reuse", re.I),
        )

    def test_FSUBR_7_1_7_2_plan_tasks_blast_radius_and_cluster(self):
        """FSUBR-7.1–7.2 plan-tasks after file map: blast_radius and cluster(feature CODE)."""
        text = PLAN.read_text()
        self.assertIn("load-subgraph", text)
        self.assertIn("blast_radius", text)
        self.assertRegex(text, re.compile(r"\bcluster\b", re.I))
        self.assertRegex(
            text,
            re.compile(
                r"cluster.{0,80}(feature CODE|focus|CODE)|"
                r"(feature CODE|focus CODE).{0,80}cluster",
                re.I | re.S,
            ),
        )
        self.assertRegex(
            text,
            re.compile(
                r"(file map|Step 2).{0,200}(blast_radius|cluster|load-subgraph)|"
                r"(blast_radius|cluster).{0,200}(file map|before writing task|task bodies)",
                re.I | re.S,
            ),
        )

    def test_FSUBR_8_1_8_2_root_cause_after_phase2_not_red(self):
        """FSUBR-8.1–8.2 root-cause retrieval after Phase 2 only; never RED loop."""
        text = ROOT_CAUSE.read_text()
        self.assertIn("load-subgraph", text)
        self.assertRegex(
            text,
            re.compile(
                r"Phase 2.{0,120}(load-subgraph|retrieval)|"
                r"(load-subgraph|retrieval).{0,120}Phase 2|"
                r"after Phase 2|completed Phase 2",
                re.I | re.S,
            ),
        )
        self.assertRegex(
            text,
            re.compile(
                r"(Phase 1|Phases 1|RED|red-capable).{0,100}"
                r"(not|never|SHALL NOT|do not).{0,60}(retrieval|load-subgraph)|"
                r"(not|never|SHALL NOT|do not).{0,60}(retrieval|load-subgraph)"
                r".{0,100}(Phase 1|Phases 1|RED|red-capable)",
                re.I | re.S,
            ),
        )

    def test_FSUBR_9_12_9_13_noop_thin_advisory(self):
        """FSUBR-9.12–9.13 no-op when no seeds/specs; thin remains advisory."""
        text = SKILL.read_text()
        self.assertRegex(
            text,
            re.compile(
                r"no-?op|missing.{0,40}docs/specs|no usable seeds|"
                r"SHALL NOT invent",
                re.I,
            ),
        )
        self.assertRegex(text, re.compile(r"advis(ory)|not a hard gate|NO GATE", re.I))

    def test_FSUBR_9_14_package_rederive_when_fingerprints_differ(self):
        """FSUBR-9.14 package validity: rederive when fingerprints/seeds/schema differ."""
        texts = [SKILL.read_text(), CLARIFY.read_text()]
        combined = "\n".join(texts)
        self.assertRegex(combined, re.compile(r"fingerprint", re.I))
        self.assertRegex(
            combined,
            re.compile(
                r"(rederive|re-derive).{0,80}(fingerprint|seed|schema|valid)|"
                r"(fingerprint|seed|schema).{0,80}(rederive|re-derive|invalid|differ|change)",
                re.I | re.S,
            ),
        )

    def test_FSUBR_9_15_no_disk_cache(self):
        """FSUBR-9.15 no on-disk session retrieval cache."""
        text = SKILL.read_text()
        self.assertRegex(
            text,
            re.compile(
                r"no (on-?disk|session-local|disk).{0,40}cache|"
                r"not.{0,20}(cache|write).{0,40}(disk|session)|"
                r"no.{0,20}disk cache",
                re.I,
            ),
        )

    def test_FSUBR_1_10_ignore_unknown_via_traces_kinds(self):
        """FSUBR-1.10 / callers: ignore unknown via_traces kinds."""
        texts = [SKILL.read_text(), ENV.read_text(), FRAME.read_text(), INSPECT.read_text()]
        hit = any(
            re.search(r"ignore unknown.{0,40}via_traces|unknown.{0,40}via_traces.{0,40}kind", t, re.I)
            for t in texts
        )
        self.assertTrue(
            hit,
            "load-subgraph skill or callers must say ignore unknown via_traces kinds",
        )
        # SKILL itself must state it for consumers
        self.assertRegex(
            SKILL.read_text(),
            re.compile(r"ignore unknown|unknown.{0,30}via_traces", re.I),
        )

    def test_FSUBR_load_subgraph_names_cluster_and_schema_1_1(self):
        """load-subgraph skill names cluster query and schema 1.1."""
        text = SKILL.read_text()
        self.assertIn("cluster", text)
        self.assertRegex(text, re.compile(r"schema_version|schema 1\.1|\"1\.1\"", re.I))

    def test_FSUBR_9_11_build_family_not_required_callers(self):
        """FSUBR-9.11 build-family skills are not required retrieval callers."""
        for path in (BUILD_WAVES, BUILD_STORY, BUILD_INLINE):
            if not path.is_file():
                continue
            text = path.read_text()
            # Must not require load-subgraph as a mandatory caller step
            self.assertNotRegex(
                text,
                re.compile(
                    r"REQUIRED SUB-SKILL:\s*use `load-subgraph`",
                    re.I,
                ),
                f"{path.name} must not be a required load-subgraph caller",
            )

    def test_FSUBR_caller_ids_in_scenarios(self):
        """FSUBR-4..8 and 9.8/11–15 tokens appear in scenarios index."""
        scenarios = SCENARIOS.read_text()
        ids = [
            "FSUBR-4.1",
            "FSUBR-4.2",
            "FSUBR-4.3",
            "FSUBR-4.4",
            "FSUBR-5.1",
            "FSUBR-5.2",
            "FSUBR-5.3",
            "FSUBR-6.1",
            "FSUBR-7.1",
            "FSUBR-7.2",
            "FSUBR-8.1",
            "FSUBR-8.2",
            "FSUBR-9.8",
            "FSUBR-9.11",
            "FSUBR-9.12",
            "FSUBR-9.13",
            "FSUBR-9.14",
            "FSUBR-9.15",
        ]
        missing = [i for i in ids if i not in scenarios]
        self.assertEqual(missing, [], f"missing from scenarios: {missing}")


class TestFSUBRGuideInventoryGuards(unittest.TestCase):
    """FSUBR-9.1–9.2, 9.4–9.7, 9.9–9.10, 10.2 — guides, inventory, carry-forward."""

    def test_FSUBR_9_9_feature_graph_cluster_and_callers(self):
        """FSUBR-9.9 feature-graph.md documents cluster + expanded callers + 1.1."""
        text = FEATURE_GRAPH.read_text()
        self.assertIn("load-subgraph", text)
        self.assertRegex(text, re.compile(r"\bcluster\b", re.I))
        self.assertRegex(
            text,
            re.compile(r"schema[_\s-]*version|schema 1\.1|path_evidence|term_evidence", re.I),
        )
        for caller in (
            "frame-change",
            "inspect-change",
            "clarify-decisions",
            "design-solution",
            "plan-tasks",
            "root-cause",
        ):
            self.assertIn(caller, text, f"feature-graph must name caller {caller}")

    def test_FSUBR_9_9_start_here_and_skills_readme_consistent(self):
        """FSUBR-9.9 START-HERE and skills README consistent with cluster + callers."""
        start = START_HERE.read_text()
        readme = SKILLS_README.read_text()
        guide = LOAD_SUBGRAPH_GUIDE.read_text()
        self.assertTrue(LOAD_SUBGRAPH_GUIDE.is_file())
        # cluster query surfaces in human guide pages
        self.assertRegex(
            start + readme + guide,
            re.compile(r"\bcluster\b", re.I),
            "START-HERE / skills README / load-subgraph guide must mention cluster",
        )
        # expanded callers appear across entry map / skill list / skill page
        combined = start + readme + guide
        for caller in (
            "clarify-decisions",
            "design-solution",
            "plan-tasks",
            "root-cause",
        ):
            self.assertIn(caller, combined, f"guides must surface caller {caller}")
        # load-subgraph skill page names cluster and core callers
        self.assertRegex(guide, re.compile(r"\bcluster\b", re.I))
        self.assertIn("frame-change", guide)
        self.assertIn("plan-tasks", guide)

    def test_FSUBR_9_10_inventory_lists_horizontal_steps(self):
        """FSUBR-9.10 AGENTS / architecture inventories list cluster or expanded callers."""
        agents = AGENTS.read_text()
        arch_skills = ARCH_SKILLS.read_text() if ARCH_SKILLS.is_file() else ""
        arch_wf = ARCH_WORKFLOWS.read_text() if ARCH_WORKFLOWS.is_file() else ""
        self.assertIn("load-subgraph", agents)
        # Horizontal neighbors inventory should mention cluster and/or extra callers
        horiz = "\n".join(
            line
            for line in agents.splitlines()
            if "horizontal" in line.lower() or "load-subgraph" in line
        )
        inv = horiz + "\n" + arch_skills + "\n" + arch_wf
        self.assertRegex(
            inv,
            re.compile(r"\bcluster\b", re.I),
            "AGENTS or architecture inventory that names load-subgraph must mention cluster",
        )
        # architecture skills inventory should name more than frame/inspect when listing callers
        if arch_skills:
            self.assertRegex(
                arch_skills,
                re.compile(
                    r"load-subgraph.{0,400}(plan-tasks|design-solution|clarify-decisions|root-cause|cluster)|"
                    r"(plan-tasks|design-solution|clarify-decisions|root-cause|cluster).{0,400}load-subgraph",
                    re.I | re.S,
                ),
                "docs/architecture/skills.md must list expanded retrieval callers or cluster",
            )

    def test_FSUBR_9_1_no_graph_md_write(self):
        """FSUBR-9.1 load-subgraph must not write GRAPH.md or docs/ graph projection."""
        text = SKILL.read_text() + PASSES.read_text()
        self.assertRegex(text, r"GRAPH\.md|graph file|projection", re.I)
        self.assertRegex(
            text,
            r"do not produce a file|never write|NO GRAPH FILE|no projection|not write",
            re.I,
        )
        # skill package must not create GRAPH.md under docs
        self.assertFalse(
            (ROOT / "docs" / "specs" / "GRAPH.md").is_file(),
            "docs/specs/GRAPH.md must not exist",
        )

    def test_FSUBR_9_2_no_depends_on_in_envelope(self):
        """FSUBR-9.2 envelope omits feature-level depends_on / DEPENDS_ON edges."""
        env_text = ENV.read_text()
        skill_text = SKILL.read_text() + PASSES.read_text()
        self.assertRegex(
            env_text + skill_text,
            re.compile(r"depends_on|DEPENDS_ON", re.I),
        )
        self.assertRegex(
            env_text + skill_text,
            re.compile(
                r"(never emit|omit|no |not |without |SHALL NOT).{0,40}depends_on|"
                r"depends_on.{0,40}(never|omit|not |forbidden|SHALL NOT)",
                re.I | re.S,
            ),
        )

    def test_FSUBR_9_4_no_python_under_skill_oracle_pack_only(self):
        """FSUBR-9.4 no *.py under load-subgraph skill; oracle stays pack-test-only."""
        pkg = ROOT / "skills" / "execution" / "load-subgraph"
        py = list(pkg.rglob("*.py"))
        self.assertEqual(py, [], f"unexpected python under skill: {py}")
        skill_text = SKILL.read_text() + PASSES.read_text()
        self.assertNotIn("tests/feature-subgraph/reference_derive.py", skill_text)
        self.assertNotRegex(skill_text, r"(?i)import\s+reference_derive")
        oracle = ROOT / "tests" / "feature-subgraph" / "reference_derive.py"
        self.assertTrue(oracle.is_file(), "pack oracle must remain under tests/")

    def test_FSUBR_9_5_audit_trace_e_codes_unchanged(self):
        """FSUBR-9.5 audit-trace finding codes E1–E5 and W1–W3 unchanged."""
        text = AUDIT_TRACE.read_text()
        for code in ("E1", "E3", "E4", "E5", "W1", "W2", "W3"):
            self.assertRegex(
                text,
                re.compile(rf"\b{code}\b"),
                f"audit-trace must still define {code}",
            )
        # E2 remains retired — do not reintroduce as active finding
        self.assertRegex(text, re.compile(r"Retired:.*\*\*E2\*\*|E2.*retired|not\s+emitted", re.I | re.S))

    def test_FSUBR_9_6_pathfind_separate_from_feature_subgraph(self):
        """FSUBR-9.6 pathfind decision-map stays separate from feature-subgraph edges."""
        text = SKILL.read_text()
        self.assertRegex(text, re.compile(r"pathfind", re.I))
        self.assertRegex(
            text,
            re.compile(
                r"pathfind.{0,80}(separate|not merge|distinct|never)|"
                r"(separate|not merge|distinct|never).{0,80}pathfind",
                re.I | re.S,
            ),
        )

    def test_FSUBR_9_7_optional_layers_noop_mentioned(self):
        """FSUBR-9.7 P3–P5 no-op when optional roadmap/architecture layers absent."""
        text = SKILL.read_text() + PASSES.read_text()
        self.assertRegex(
            text,
            re.compile(
                r"(P3|P4|P5|optional).{0,80}(no-?op|absent|missing)|"
                r"(no-?op|absent).{0,80}(roadmap|architecture|P3|P4|P5)",
                re.I | re.S,
            ),
        )

    def test_FSUBR_10_2_passive_data_prose(self):
        """FSUBR-10.2 skill treats path tokens / prose as passive data (not instructions)."""
        text = SKILL.read_text() + PASSES.read_text()
        self.assertRegex(
            text,
            re.compile(
                r"passive|not (obey|execute|run).{0,40}(instruction|path|prose)|"
                r"(path|prose|token).{0,60}(passive|not executed|data only)",
                re.I | re.S,
            ),
            "load-subgraph must state path/prose are passive data",
        )

    def test_FSUBR_guide_guard_ids_in_scenarios(self):
        """FSUBR-9.1–9.2, 9.4–9.7, 9.9–9.10, 10.2 tokens appear in scenarios index."""
        scenarios = SCENARIOS.read_text()
        ids = [
            "FSUBR-9.1",
            "FSUBR-9.2",
            "FSUBR-9.4",
            "FSUBR-9.5",
            "FSUBR-9.6",
            "FSUBR-9.7",
            "FSUBR-9.9",
            "FSUBR-9.10",
            "FSUBR-10.2",
        ]
        missing = [i for i in ids if i not in scenarios]
        self.assertEqual(missing, [], f"missing from scenarios: {missing}")


if __name__ == "__main__":
    unittest.main()