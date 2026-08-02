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


class TestFSUBRP1Owns(unittest.TestCase):
    """FSUBR P1 multi-block extract, classifier, reliability notes."""

    def _paths(self, result):
        if isinstance(result, dict):
            return result["paths"]
        return result

    def _notes(self, result):
        if isinstance(result, dict):
            return result.get("notes") or []
        return []

    def _files_body(self, *lines: str) -> str:
        return "### Task\n\n**Files:**\n" + "\n".join(lines) + "\n\n**Reuse:** none\n"

    def test_FSUBR_2_1_2_9_multi_block_retains_later_task_paths(self):
        """FSUBR-2.1 FSUBR-2.9 later-task Files paths retained."""
        root = FIX / "p1-later-files"
        result = rd.owns_result_for_code(root, "LATER")
        paths = self._paths(result)
        self.assertIn("src/first.ts", paths)
        self.assertIn("src/later.ts", paths)

    def test_FSUBR_2_2_2_3_stops_at_reuse_not_step_prose(self):
        """FSUBR-2.2 FSUBR-2.3 Files ends at Reuse; prose outside not extracted."""
        text = (
            "### Task 1\n\n"
            "**Files:**\n"
            "- Create: `src/keep.ts`\n"
            "**Reuse:** none\n\n"
            "After reuse mention `src/outside.ts` and self.assertEqual\n"
        )
        result = rd.extract_owns_from_tasks_text(text)
        paths = self._paths(result)
        self.assertIn("src/keep.ts", paths)
        self.assertNotIn("src/outside.ts", paths)
        self.assertNotIn("self.assertEqual", paths)

    def test_FSUBR_2_2_fence_internal_heading_not_boundary(self):
        """FSUBR-2.2 ### inside fence does not end Files section."""
        root = FIX / "p1-fence-heading"
        result = rd.owns_result_for_code(root, "FENCE")
        paths = self._paths(result)
        self.assertIn("src/before.ts", paths)
        self.assertIn("src/after.ts", paths)

    def test_FSUBR_2_4_2_5_2_6_classifier_decision_table(self):
        """FSUBR-2.4 FSUBR-2.5 FSUBR-2.6 decision-table pos/neg rows."""
        # labeled / backticked accepts
        labeled = self._files_body(
            "- Create: `AGENTS.md`",
            "- Create: `Makefile`",
            "- Create: `weird.xyz`",
            "- Create: `self.assertEqual`",
            "- Modify: `.gitignore`",
            "- Create: `src/app/App.tsx`",
            "- Create: `.claude-plugin/plugin.json`",
            "- Test: `foo.py`",
        )
        lp = self._paths(rd.extract_owns_from_tasks_text(labeled))
        for token in (
            "AGENTS.md",
            "Makefile",
            "weird.xyz",
            "self.assertEqual",
            ".gitignore",
            "src/app/App.tsx",
            ".claude-plugin/plugin.json",
            "foo.py",
        ):
            self.assertIn(token, lp, f"labeled/backticked should accept {token!r}")

        # unquoted prose accepts
        prose_ok = self._files_body(
            "README.md assertions.md Makefile .gitignore",
            "src/app/App.tsx AGENTS.md foo.py",
        )
        op = self._paths(rd.extract_owns_from_tasks_text(prose_ok))
        for token in (
            "README.md",
            "assertions.md",
            "Makefile",
            ".gitignore",
            "src/app/App.tsx",
            "AGENTS.md",
            "foo.py",
        ):
            self.assertIn(token, op, f"unquoted_prose should accept {token!r}")

        # unquoted prose rejects
        prose_bad = self._files_body(
            "pass. contract. self.assertEqual unittest.TestCase",
            "json.loads re.search nothing weird.xyz",
            ". ..",
        )
        bp = self._paths(rd.extract_owns_from_tasks_text(prose_bad))
        for token in (
            "pass.",
            "contract.",
            "self.assertEqual",
            "unittest.TestCase",
            "json.loads",
            "re.search",
            "nothing",
            "weird.xyz",
            ".",
            "..",
        ):
            self.assertNotIn(token, bp, f"unquoted_prose should reject {token!r}")

        # slash_path accepts
        slash = self._files_body("src/app/App.tsx .claude-plugin/plugin.json")
        sp = self._paths(rd.extract_owns_from_tasks_text(slash))
        self.assertIn("src/app/App.tsx", sp)
        self.assertIn(".claude-plugin/plugin.json", sp)

        # fixture tree also covers mixed labeled + prose surface
        root = FIX / "p1-classifier"
        fixture_paths = self._paths(rd.owns_result_for_code(root, "CLS"))
        self.assertIn("AGENTS.md", fixture_paths)
        self.assertIn("src/app/App.tsx", fixture_paths)
        self.assertNotIn("pass.", fixture_paths)
        self.assertNotIn("json.loads", fixture_paths)
        self.assertNotIn("nothing", fixture_paths)

    def test_FSUBR_2_7_2_8_legacy_forms_and_line_suffix(self):
        """FSUBR-2.7 FSUBR-2.8 legacy bullets/prose + glued line-suffix strip."""
        root = FIX / "legacy-glued-lines"
        result = rd.owns_result_for_code(root, "ALPHA")
        paths = self._paths(result)
        self.assertIn("src/app/App.tsx", paths)
        self.assertIn("skills/foo/SKILL.md", paths)
        self.assertIn("tests/test_alpha.py", paths)
        self.assertIn("lib/util/dates.ts", paths)
        self.assertNotIn("src/app/App.tsx:86,1030", paths)

    def test_FSUBR_10_3_malformed_last_block_skips_keeps_siblings(self):
        """FSUBR-10.3 unclosed fence last block → p1_block_skipped; prior paths kept."""
        root = FIX / "p1-malformed-block"
        result = rd.owns_result_for_code(root, "MAL")
        paths = self._paths(result)
        notes = self._notes(result)
        self.assertIn("src/ok.ts", paths)
        self.assertIn("src/also.ts", paths)
        self.assertNotIn("src/lost.ts", paths)
        kinds = {n.get("kind") for n in notes}
        self.assertIn("p1_block_skipped", kinds)

    def test_FSUBR_10_4_unreadable_tasks_emits_note_empty_paths(self):
        """FSUBR-10.4 unreadable tasks.md → p1_file_unreadable; sibling features continue."""
        root = FIX / "p1-unreadable"
        bad = rd.owns_result_for_code(root, "BAD")
        good = rd.owns_result_for_code(root, "GOOD")
        self.assertEqual(self._paths(bad), set())
        kinds = {n.get("kind") for n in self._notes(bad)}
        self.assertIn("p1_file_unreadable", kinds)
        self.assertIn("src/good.ts", self._paths(good))

    def test_FSUBR_10_4_missing_tasks_empty_no_unreadable_note(self):
        """FSUBR-10.4 missing tasks.md → empty OWNS, no p1_file_unreadable."""
        root = FIX / "p1-missing-tasks"
        result = rd.owns_result_for_code(root, "MISS")
        self.assertEqual(self._paths(result), set())
        kinds = {n.get("kind") for n in self._notes(result)}
        self.assertNotIn("p1_file_unreadable", kinds)

    def test_FSUBR_10_3_notes_not_silently_capped(self):
        """FSUBR-10.3 reliability notes retained (no silent count drop)."""
        text = (
            "### Task A\n\n**Files:**\n- Create: `src/a.ts`\n```python\nx\n\n"
            "### Task B\n\n**Files:**\n- Create: `src/b.ts`\n```python\ny\n"
        )
        # two unclosed fences if each block fails independently — at least one note
        result = rd.extract_owns_from_tasks_text(text)
        notes = self._notes(result)
        skipped = [n for n in notes if n.get("kind") == "p1_block_skipped"]
        self.assertGreaterEqual(len(skipped), 1)


class TestFSUBRSnapshot(unittest.TestCase):
    """FSUBR-10.1 DerivationSnapshot two-stage + read_ledger + pure queries."""

    def test_FSUBR_10_1_read_ledger_path_at_most_once_neighbors(self):
        """FSUBR-10.1 after build_snapshot + neighbors, each path ≤1 in read_ledger."""
        root = FIX / "mega-owner-100"
        q = {"kind": "neighbors", "code": "FOCUS", "terms": []}
        snap = rd.build_snapshot(root, q)
        paths = [e["path"] for e in snap["read_ledger"]]
        self.assertEqual(len(paths), len(set(paths)), f"duplicate ledger paths: {paths}")
        rd.neighbors_from_snapshot(snap, "FOCUS", terms=None)
        paths_after = [e["path"] for e in snap["read_ledger"]]
        self.assertEqual(len(paths_after), len(set(paths_after)))
        self.assertEqual(paths, paths_after)

    def test_FSUBR_10_1_read_ledger_path_at_most_once_cluster(self):
        """FSUBR-10.1 after build_snapshot for cluster, each path ≤1 in read_ledger."""
        root = FIX / "mega-owner-100"
        q = {"kind": "cluster", "focus": "FOCUS"}
        snap = rd.build_snapshot(root, q)
        paths = [e["path"] for e in snap["read_ledger"]]
        self.assertEqual(len(paths), len(set(paths)), f"duplicate ledger paths: {paths}")
        # Stage B may load member requirements; still ≤1 per path
        for rel, text in snap.get("source_texts", {}).items():
            self.assertIsInstance(text, str)
        # pure cluster query (minimal) must not grow ledger
        if hasattr(rd, "cluster_from_snapshot"):
            rd.cluster_from_snapshot(snap, "FOCUS")
        paths_after = [e["path"] for e in snap["read_ledger"]]
        self.assertEqual(paths, paths_after)

    def test_FSUBR_10_1_query_pure_io_disabled_after_snapshot(self):
        """FSUBR-10.1 queries succeed with IO-disabled adapter when snapshot prebuilt."""
        root = FIX / "mega-owner-100"
        q = {"kind": "neighbors", "code": "FOCUS", "terms": ["shared"]}
        snap = rd.build_snapshot(root, q)
        ledger_before = list(snap["read_ledger"])

        class _Boom:
            def __getattr__(self, name):
                raise OSError(f"IO disabled: {name}")

        result = rd.neighbors_from_snapshot(snap, "FOCUS", terms=["shared"], fs=_Boom())
        self.assertIn("neighbors", result)
        codes = {row["code"] for row in result["neighbors"]}
        self.assertTrue(codes & {"SMALL", "MEGA"})
        self.assertEqual(snap["read_ledger"], ledger_before)

        env = rd.run_on_snapshot(snap, q, fs=_Boom())
        self.assertIn("neighbors", env)
        self.assertEqual(snap["read_ledger"], ledger_before)

    def test_FSUBR_10_1_missing_tasks_no_unreadable_note_in_snapshot(self):
        """FSUBR-10.1 missing tasks.md → empty OWNS, no p1_file_unreadable in snapshot."""
        root = FIX / "p1-missing-tasks"
        snap = rd.build_snapshot(root, {"kind": "neighbors", "code": "MISS", "terms": []})
        owns = snap["owns"].get("MISS", set())
        if isinstance(owns, dict):
            owns = owns.get("paths", set())
        self.assertEqual(owns, set())
        kinds = {n.get("kind") for n in snap.get("notes") or []}
        self.assertNotIn("p1_file_unreadable", kinds)

    def test_FSUBR_10_1_fingerprints_optional_layer_presence_sentinels(self):
        """FSUBR-10.1 absent optional layers recorded present:false in fingerprints."""
        root = FIX / "no-roadmap"
        snap = rd.build_snapshot(root, {"kind": "neighbors", "code": "AA", "terms": []})
        fps = snap["fingerprints"]
        self.assertIn("docs/roadmap/INDEX.md", fps)
        self.assertFalse(fps["docs/roadmap/INDEX.md"]["present"])
        # architecture also absent on this fixture
        self.assertIn("docs/architecture/INDEX.md", fps)
        self.assertFalse(fps["docs/architecture/INDEX.md"]["present"])
        # INDEX that was read is present with sha256
        self.assertTrue(fps["docs/specs/INDEX.md"]["present"])
        self.assertTrue(fps["docs/specs/INDEX.md"].get("sha256"))

    def test_FSUBR_10_1_schema_recipe_on_snapshot(self):
        """FSUBR-10.1 snapshot carries schema_version 1.1 and recipe_id fsubr-1.1."""
        root = FIX / "legacy-glued-lines"
        snap = rd.build_snapshot(root, {"kind": "neighbors", "code": "ALPHA", "terms": []})
        self.assertEqual(snap["schema_version"], "1.1")
        self.assertEqual(snap["recipe_id"], "fsubr-1.1")

    def test_FSUBR_10_1_cluster_stage_a_no_triad_preload(self):
        """Cluster: Stage A skips all-feature triad; Stage B loads member requirements only."""
        root = FIX / "p0-flood"
        q = {"kind": "cluster", "focus": "FOCUS"}
        snap = rd.build_snapshot(root, q)
        ledger_paths = [e["path"] for e in snap["read_ledger"]]
        members = rd._cluster_returned_members(snap["owns"], "FOCUS")
        # FOCUS has no shared paths with others → sole returned member
        self.assertEqual(members, ["FOCUS"])

        code_to_row = {r["code"]: r for r in snap["registry"]}
        focus_req = rd._feature_rel(code_to_row["FOCUS"], "requirements.md")
        # Member requirements appear once (Stage B) when not already buffered
        self.assertEqual(ledger_paths.count(focus_req), 1)
        self.assertIn(focus_req, snap["source_texts"])

        # Non-member requirements.md must not appear in the ledger
        for code, row in code_to_row.items():
            if code in members:
                continue
            non_req = rd._feature_rel(row, "requirements.md")
            self.assertNotIn(
                non_req,
                ledger_paths,
                f"non-member {code} requirements must not be in read_ledger",
            )
            non_design = rd._feature_rel(row, "design.md")
            self.assertNotIn(
                non_design,
                ledger_paths,
                f"non-member {code} design must not be in read_ledger",
            )

        # Cluster does not preload design.md for any feature in Stage A
        design_entries = [p for p in ledger_paths if p.endswith("/design.md")]
        self.assertEqual(design_entries, [])


if __name__ == "__main__":
    unittest.main()
