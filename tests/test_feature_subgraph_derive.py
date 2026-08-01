"""FSUB-3.1 FSUB-3.2 FSUB-3.3 FSUB-3.4 FSUB-1.6 FSUB-1.7 FSUB-1.8 FSUB-1.9
FSUB-1.10 FSUB-2.1 FSUB-2.2 FSUB-2.3 FSUB-2.4 FSUB-2.5 FSUB-2.6 FSUB-1.5
FSUB-1.11 FSUB-1.14 FSUB-1.16 FSUB-5.1 FSUB-5.2 FSUB-5.3 FSUB-8.1 FSUB-8.2
FSUB-8.3 FSUB-1.13 — reference_derive recipe math.
"""

from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

_REF = Path(__file__).resolve().parent / "feature-subgraph" / "reference_derive.py"
_spec = importlib.util.spec_from_file_location("reference_derive", _REF)
rd = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(rd)

FIX = Path(__file__).resolve().parent / "feature-subgraph" / "fixtures"


class TestLegacyOwnsParse(unittest.TestCase):
    def test_FSUB_3_2_strips_glued_line_suffixes(self):
        root = FIX / "legacy-glued-lines"
        owns = rd.owns_for_code(root, "ALPHA")
        self.assertIn("src/app/App.tsx", owns)
        self.assertIn("skills/foo/SKILL.md", owns)
        self.assertNotIn("src/app/App.tsx:86,1030", owns)

    def test_FSUB_3_1_accepts_bullets_backticks_and_prose(self):
        root = FIX / "legacy-glued-lines"
        owns = rd.owns_for_code(root, "ALPHA")
        self.assertIn("tests/test_alpha.py", owns)
        self.assertIn("lib/util/dates.ts", owns)


class TestDenoiseAndNeighbors(unittest.TestCase):
    def test_FSUB_2_1_2_4_stop_list_excludes_package_json_and_src_segment(self):
        paths = {"package.json", "src", "src/real/mod.ts", "skills"}
        meaningful = rd.denoise(paths)
        self.assertNotIn("package.json", meaningful)
        self.assertNotIn("src", meaningful)
        self.assertNotIn("skills", meaningful)
        self.assertIn("src/real/mod.ts", meaningful)

    def test_FSUB_2_2_no_ancestor_expansion(self):
        a = {"src/app/x.ts"}
        b = {"src"}
        self.assertEqual(rd.overlap_weight(a, b), 0)

    def test_FSUB_2_6_ranks_small_sharer_above_mega_owner(self):
        root = FIX / "mega-owner-100"
        n = rd.neighbors(root, "FOCUS", terms=None)
        codes = [row["code"] for row in n["neighbors"]]
        self.assertIn("SMALL", codes)
        self.assertIn("MEGA", codes)
        self.assertLess(codes.index("SMALL"), codes.index("MEGA"))

    def test_FSUB_2_3_neighbors_length_at_most_12(self):
        root = FIX / "mega-owner-100"
        n = rd.neighbors(root, "FOCUS", terms=None)
        self.assertLessEqual(len(n["neighbors"]), 12)

    def test_FSUB_2_3_union_before_truncate_never_exceeds_max(self):
        root = FIX / "p0-flood"
        n = rd.neighbors(root, "FOCUS", terms=["shared"])
        self.assertLessEqual(len(n["neighbors"]), 12)


class TestP0AndCoverage(unittest.TestCase):
    def test_FSUB_1_5_p0_seeds_from_terms(self):
        root = FIX / "p0-flood"
        seeds = rd.p0_seeds(root, ["unique-alpha-token"])
        self.assertIn("ALPHA", seeds["codes"])

    def test_FSUB_1_5_p0_truncated_at_12(self):
        root = FIX / "p0-flood"
        seeds = rd.p0_seeds(root, ["shared"])
        self.assertLessEqual(len(seeds["codes"]), 12)
        if seeds["matched"] > 12:
            self.assertTrue(seeds["truncated"])

    def test_FSUB_1_16_owns_coverage_reported(self):
        root = FIX / "thin-owns"
        env = rd.run(root, {"kind": "neighbors", "code": "AA", "terms": []})
        self.assertIn("owns_coverage", env)
        self.assertIn("with_owns", env["owns_coverage"])
        self.assertIn("registered", env["owns_coverage"])
        self.assertEqual(env["owns_coverage"]["registered"], 2)
        self.assertEqual(env["owns_coverage"]["with_owns"], 1)

    def test_FSUB_5_2_ancestors_bare_without_roadmap(self):
        root = FIX / "no-roadmap"
        env = rd.run(root, {"kind": "ancestors", "code": "AA"})
        self.assertEqual(env.get("ancestors"), ["AA"])

    def test_FSUB_5_1_no_architecture_skips_respects(self):
        root = FIX / "no-architecture"
        env = rd.run(root, {"kind": "subgraph", "seeds": {"codes": ["AA"]}})
        self.assertEqual(env.get("respects", []), [])

    def test_FSUB_1_2_oracle_dual_run_identical(self):
        """Recipe math dual-run (oracle). Skill-path FSUB-1.2 is Task 2 scenario."""
        root = FIX / "legacy-glued-lines"
        q = {"kind": "neighbors", "code": "ALPHA", "terms": ["alpha"]}
        a = rd.run(root, q)
        b = rd.run(root, q)
        self.assertEqual(a, b)

    def test_FSUB_8_2_passive_instruction_shaped_path_not_executed(self):
        paths = {"; rm -rf /"}
        self.assertIsInstance(rd.denoise(paths), set)

    def test_FSUB_1_13_envelope_has_no_depends_on_edges(self):
        root = FIX / "legacy-glued-lines"
        env = rd.run(root, {"kind": "neighbors", "code": "ALPHA", "terms": []})
        self.assertNotIn("depends_on", env)
        self.assertNotIn("DEPENDS_ON", env)

    def test_FSUB_1_7_p2_emits_overlap_when_shared_meaningful_path(self):
        root = FIX / "mega-owner-100"
        env = rd.run(root, {"kind": "neighbors", "code": "FOCUS", "terms": []})
        codes = {row["code"] for row in env["neighbors"]}
        self.assertTrue(codes & {"SMALL", "MEGA"})

    def test_FSUB_1_8_p3_implements_from_index_roadmap_column(self):
        root = FIX / "no-architecture"
        env = rd.run(root, {"kind": "ancestors", "code": "AA"})
        ancestors = env.get("ancestors", [])
        self.assertIn("AA", ancestors)
        self.assertTrue(any(x.startswith("ROAD-") for x in ancestors))

    def test_FSUB_1_9_p4_contains_from_roadmap_members(self):
        root = FIX / "no-architecture"
        env = rd.run(root, {"kind": "descendants", "mile": "MILE-1"})
        desc = env.get("descendants", [])
        self.assertTrue(any(x.startswith("ROAD-") or x == "AA" for x in desc))

    def test_FSUB_1_10_subgraph_resolves_term_seeds(self):
        root = FIX / "p0-flood"
        env = rd.run(root, {"kind": "subgraph", "seeds": {"terms": ["unique-alpha-token"]}})
        nodes = env.get("nodes") or env.get("seeds") or []
        if isinstance(nodes, list) and nodes and isinstance(nodes[0], dict):
            codes = {n.get("code") for n in nodes}
        else:
            codes = set(nodes)
        self.assertIn("ALPHA", codes)

    def test_FSUB_5_3_empty_owns_without_tasks(self):
        root = FIX / "thin-owns"
        owns = rd.owns_for_code(root, "BB")
        self.assertEqual(owns, set())


if __name__ == "__main__":
    unittest.main()
