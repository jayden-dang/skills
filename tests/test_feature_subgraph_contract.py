"""FSUB-1.1 FSUB-1.2 FSUB-1.3 FSUB-1.4 FSUB-1.12 FSUB-1.15 FSUB-4.1 FSUB-4.2
FSUB-6.1 FSUB-6.2 FSUB-6.3 FSUB-6.4 FSUB-6.5 FSUB-6.6 FSUB-7.1 FSUB-7.2
FSUB-7.3 FSUB-7.4 FSUB-7.5 FSUB-7.6 FSUB-7.7 — skill and wiring contracts.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "execution" / "load-subgraph" / "SKILL.md"
PASSES = ROOT / "skills" / "execution" / "load-subgraph" / "references" / "passes.md"
ENV = ROOT / "skills" / "execution" / "load-subgraph" / "references" / "envelope.md"
MAP = ROOT / "skills" / "track" / "map-features" / "SKILL.md"
FRAME = ROOT / "skills" / "discovery" / "frame-change" / "SKILL.md"
INSPECT = ROOT / "skills" / "review" / "inspect-change" / "SKILL.md"
PLAN = ROOT / "skills" / "spec" / "plan-tasks" / "SKILL.md"
TEMPLATE = ROOT / "templates" / "tasks.md"
FEATURE_GRAPH = ROOT / "docs" / "guide" / "concepts" / "feature-graph.md"
SCENARIOS = ROOT / "tests" / "feature-subgraph" / "scenarios.md"


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
            re.search(r"two independent runs|determin", text, re.I),
            "skill must state dual-run / determinism",
        )

    def test_FSUB_1_3_forbids_graph_materialization(self):
        text = SKILL.read_text() + PASSES.read_text()
        self.assertRegex(text, r"GRAPH\.md|materializ", re.I)
        self.assertRegex(text, r"MUST NOT write|SHALL NOT write|never write|Forbidden", re.I)

    def test_FSUB_1_12_advisory_not_a_gate(self):
        text = SKILL.read_text()
        self.assertRegex(text, r"advisory|not a (hard )?gate|never fail a gate", re.I)

    def test_FSUB_7_4_pathfind_separate(self):
        text = SKILL.read_text()
        self.assertRegex(text, r"pathfind", re.I)

    def test_FSUB_1_10_queries_named(self):
        text = PASSES.read_text() + SKILL.read_text()
        for q in ("neighbors", "ancestors", "descendants", "blast_radius", "subgraph"):
            self.assertIn(q, text)

    def test_FSUB_passes_documents_P0_through_P5_and_bounds(self):
        text = PASSES.read_text()
        for token in ("P0", "P1", "P2", "P3", "P4", "P5", "NEIGHBORS_MAX", "P0_SEED_MAX", "12"):
            self.assertIn(token, text)

    def test_FSUB_envelope_documents_owns_coverage(self):
        text = ENV.read_text()
        self.assertIn("owns_coverage", text)
        self.assertIn("advisory", text)


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
        self.assertRegex(text, r"OWNS|ownership|Files", re.I)
        self.assertRegex(text, r"DEPENDS_ON|Depends-on|Consumes", re.I)
        self.assertRegex(text, r"confirm", re.I)
        self.assertRegex(text, r"MUST NOT auto|never auto|not auto-write", re.I)
        self.assertRegex(text, r"slug|directory", re.I)
        self.assertRegex(text, r"/map-features|name.*map-features", re.I)


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


if __name__ == "__main__":
    unittest.main()
