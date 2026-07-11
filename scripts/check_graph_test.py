"""Unit tests for scripts/check_graph.py pure functions.

Expected values are asserted independently, not recomputed from check_graph.py
under test.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

import check_graph

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PY_CLI = os.path.join(_SCRIPTS_DIR, "check_graph.py")

CFG = {
    "sourceRoots": ["src", "src-tauri", "tests", "test", "crates", "app", "lib", "packages"],
    "sourceExts": ["ts", "tsx", "js", "jsx", "mjs", "rs", "css", "scss"],
}


class _FixtureTestCase(unittest.TestCase):
    """Shared fixture builders for harvest/render/query/config tests."""

    def _tmp_repo(self, files):
        """Create a temp repo tree from {relative_path: content}; return its root."""
        root = tempfile.mkdtemp(prefix="check-graph-")
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        for rel, content in files.items():
            full = os.path.join(root, rel)
            os.makedirs(os.path.dirname(full), exist_ok=True)
            with open(full, "w", encoding="utf-8") as fh:
                fh.write(content)
        return root

    def _spec_fixture(self, features):
        """Build a docs/specs tree from `features`, return its path.

        Each `features` entry is a dict with keys slug, code, name, and optionally
        oos (list), design (str), tasks (str), used to render each feature's
        requirements.md (and optional design.md / tasks.md).
        """
        root = tempfile.mkdtemp(prefix="check-graph-")
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        specs = os.path.join(root, "docs", "specs")
        for f in features:
            d = os.path.join(specs, f["slug"])
            os.makedirs(d, exist_ok=True)
            oos_bullets = "\n".join(f"- {x}" for x in f.get("oos", []))
            req_text = (
                f"# Requirements: {f['name']}\n"
                f"Feature code: {f['code']}\n"
                "Status: Approved\n\n"
                "## Out of Scope\n"
                f"{oos_bullets}\n"
            )
            with open(os.path.join(d, "requirements.md"), "w", encoding="utf-8") as fh:
                fh.write(req_text)
            if f.get("design"):
                with open(os.path.join(d, "design.md"), "w", encoding="utf-8") as fh:
                    fh.write(f["design"])
            if f.get("tasks"):
                with open(os.path.join(d, "tasks.md"), "w", encoding="utf-8") as fh:
                    fh.write(f["tasks"])
        return specs


class NormalizePathTest(unittest.TestCase):
    def test_normalize_path_strips_locators_and_quoting(self):
        """normalizePath strips locators and quoting."""
        self.assertEqual(check_graph.normalize_path("`Editor.tsx:208`"), "Editor.tsx")
        self.assertEqual(check_graph.normalize_path("App.tsx:127,172"), "App.tsx")
        self.assertEqual(
            check_graph.normalize_path("src/components/Editor.tsx (~208-221)"),
            "src/components/Editor.tsx",
        )
        self.assertEqual(check_graph.normalize_path('"src/lib/x.ts"'), "src/lib/x.ts")
        self.assertEqual(check_graph.normalize_path("`Editor.tsx:208` (~208-221)"), "Editor.tsx")
        self.assertEqual(check_graph.normalize_path("./scripts/check_graph.py"), "scripts/check_graph.py")


class IsSourcePathTest(unittest.TestCase):
    def test_is_source_path_accepts_real_paths_rejects_junk(self):
        """isSourcePath accepts real paths, rejects junk."""
        self.assertTrue(check_graph.is_source_path("src/components/Editor.tsx", CFG))
        self.assertTrue(check_graph.is_source_path("raki-domain/src/inline.rs", CFG))
        self.assertFalse(check_graph.is_source_path("src-tauri/", CFG))  # bare root, no filename
        self.assertFalse(check_graph.is_source_path(".spec.ts", CFG))  # bare extension, no name
        self.assertFalse(check_graph.is_source_path("the quick brown", CFG))

    def test_is_source_path_rejects_glob_tokens(self):
        """isSourcePath rejects glob tokens."""
        self.assertFalse(check_graph.is_source_path("e2e/*.spec.ts", CFG), "glob token is not a concrete path")
        self.assertFalse(check_graph.is_source_path("src/*.ts", CFG))
        self.assertTrue(check_graph.is_source_path("src/real.ts", CFG), "concrete path is unaffected")


class DedupeByFullestTest(unittest.TestCase):
    def test_dedupe_by_fullest_collapses_basename_into_full_path(self):
        """dedupeByFullest collapses basename into full path."""
        out = check_graph.dedupe_by_fullest(
            ["Editor.tsx", "src/components/Editor.tsx", "src/lib/x.ts"]
        )
        self.assertEqual(
            sorted(out), ["src/components/Editor.tsx", "src/lib/x.ts"]
        )


class ClassifyRoleTest(unittest.TestCase):
    def test_classify_role_create_signal_owns_else_touches(self):
        """classifyRole: create signal owns, else touches."""
        self.assertEqual(
            check_graph.classify_role("- Create: `src/x.ts` — new picker", None), "owns"
        )
        self.assertEqual(check_graph.classify_role("add a new file src/y.ts", None), "owns")
        self.assertEqual(
            check_graph.classify_role("- Modify: `src/x.ts` (extract helper)", None), "touches"
        )
        self.assertEqual(
            check_graph.classify_role("reuse `src/x.ts` from the plugin", None), "touches"
        )
        self.assertEqual(
            check_graph.classify_role("`src/x.ts` is referenced here", "create"), "owns"
        )  # block wins
        self.assertEqual(
            check_graph.classify_role("`src/x.ts` mentioned in prose", None), "touches"
        )  # safe default
        self.assertEqual(
            check_graph.classify_role(
                "Modify the config to add a new dependency version check", None
            ),
            "touches",
        )
        self.assertEqual(
            check_graph.classify_role(
                "Add a toggle for the new settings pane while modifying things", None
            ),
            "touches",
        )


class CapListTest(unittest.TestCase):
    def test_cap_list_under_cap_returns_items_unchanged(self):
        """capList leaves a list at or under cap untouched."""
        items = ["a", "b", "c"]
        self.assertEqual(check_graph.cap_list(items, 5), items)

    def test_cap_list_over_cap_truncates_with_elision_marker(self):
        """capList truncates over-cap lists with a "+N more" marker."""
        # 20 items, cardCap 5 -> 5 items + 1 elision marker, marker text
        # matches /\+15 more/.
        many = [f"No feature number {i}" for i in range(20)]
        result = check_graph.cap_list(many, 5)
        self.assertEqual(len(result), 6, "5 items + 1 elision marker")
        self.assertEqual(result[:5], many[:5])
        self.assertRegex(result[5], r"\+15 more")


class ExtractOutOfScopeTest(unittest.TestCase):
    def test_extract_out_of_scope_reads_bullet_list(self):
        """extractOutOfScope reads the Out of Scope bullet list."""
        # A requirements.md body with an Out of Scope bullet list and its
        # expected extract_out_of_scope result.
        req_text = (
            "# Requirements: Card feature\n"
            "Feature code: CARD\n"
            "Status: Approved\n\n"
            "## Out of Scope\n"
            "- No time zones\n"
            "- No recurrence\n"
        )
        self.assertEqual(
            check_graph.extract_out_of_scope(req_text), ["No time zones", "No recurrence"]
        )

    def test_extract_out_of_scope_missing_heading_returns_empty(self):
        """extractOutOfScope returns [] when no heading is present."""
        req_text = "# Requirements: Only\nFeature code: ONLY\nStatus: Approved\n"
        self.assertEqual(check_graph.extract_out_of_scope(req_text), [])


class ExtractInterfacesTest(unittest.TestCase):
    def test_extract_interfaces_lean_single_line_entries(self):
        """extractInterfaces yields lean single-line entries:
        top-level bullets, no bare labels, no prose after em-dash, no nested-vs-top-level
        duplication."""
        # A design.md Interfaces body and its expected extract_interfaces result.
        body = (
            "**Interfaces:**\n"
            "- Produces:\n"
            "  - `doThing(x) → y` — long prose description that should be dropped after the em dash\n"
            "- `helper()` — details\n"
        )
        result = check_graph.extract_interfaces([body])
        self.assertIn("doThing(x) → y", result, "nested substance kept as a signature-only entry, prose after em-dash dropped")
        self.assertIn("helper()", result, "top-level bullet truncated at the em-dash to its signature")
        self.assertFalse(any(s.strip().lower().rstrip(":") == "produces" for s in result), "bare section-lead label dropped")
        self.assertFalse(any("long prose" in s for s in result), "prose after em-dash never leaks into any entry")
        self.assertEqual(len(result), 2, "no nested-vs-top-level duplication — exactly the two substantive entries")


class LoadConfigTest(_FixtureTestCase):
    def test_load_config_raises_never_exits(self):
        """load_config raises ConfigError instead of killing the process."""
        root = self._tmp_repo({"docs/agents/trace.json": "{ not json"})
        with self.assertRaises(check_graph.ConfigError):
            check_graph.load_config(root)

    def test_load_config_missing_file_falls_back_to_defaults(self):
        """a repo with no trace.json falls back to DEFAULTS."""
        root = self._tmp_repo({})
        self.assertEqual(check_graph.load_config(root), check_graph.DEFAULTS)

    def test_load_config_deep_merges_graph_key_over_defaults(self):
        """load_config deep-merges the nested "graph" key over DEFAULTS.graph."""
        root = self._tmp_repo(
            {"docs/agents/trace.json": '{"specsDir": "specs", "graph": {"cardCap": 3}}'}
        )
        cfg = check_graph.load_config(root)
        self.assertEqual(cfg["specsDir"], "specs")
        self.assertEqual(cfg["graph"]["cardCap"], 3)
        # unspecified graph sub-keys still come from DEFAULTS.graph
        self.assertEqual(cfg["graph"]["sourceRoots"], check_graph.DEFAULTS["graph"]["sourceRoots"])


class HarvestTest(_FixtureTestCase):
    def test_harvest_builds_owns_touches_from_design_and_tasks(self):
        """harvest builds owns/touches from design+tasks."""
        specs = self._spec_fixture(
            [
                {
                    "slug": "a-base",
                    "code": "BASE",
                    "name": "Base",
                    "tasks": "**Files:**\n- Create: `src/core/engine.ts`\n- Create: `src/core/util.ts`\n",
                },
                {
                    "slug": "b-ext",
                    "code": "EXT",
                    "name": "Extension",
                    "tasks": "**Files:**\n- Modify: `src/core/engine.ts` (extend)\n- Create: `src/ext/plugin.ts`\n",
                },
            ]
        )
        g = check_graph.harvest(specs)
        base = next(f for f in g["features"] if f["code"] == "BASE")
        ext = next(f for f in g["features"] if f["code"] == "EXT")
        self.assertIn("src/core/engine.ts", base["owns"])
        self.assertIn("src/core/engine.ts", ext["touches"])
        self.assertIn("src/ext/plugin.ts", ext["owns"])

    def test_harvest_reverse_index_and_shared_surface(self):
        """reverse index + shared surface."""
        specs = self._spec_fixture(
            [
                {"slug": "a-base", "code": "BASE", "name": "Base", "tasks": "- Create: `src/core/engine.ts`\n"},
                {"slug": "b-ext", "code": "EXT", "name": "Extension", "tasks": "- Modify: `src/core/engine.ts`\n"},
            ]
        )
        g = check_graph.harvest(specs)
        self.assertEqual(
            sorted(r["code"] for r in g["reverse"]["src/core/engine.ts"]), ["BASE", "EXT"]
        )
        shared = next(s for s in g["shared"] if s["path"] == "src/core/engine.ts")
        self.assertEqual(len(shared["refs"]), 2, "referenced by 2 features -> shared")

    def test_harvest_cross_feature_basename_fullpath_merge(self):
        """cross-feature basename/full-path merge in the reverse index."""
        specs = self._spec_fixture(
            [
                {"slug": "a-aaa", "code": "AAA", "name": "Aaa", "tasks": "- Create: `mathInputExtension.ts`\n"},
                {
                    "slug": "b-bbb",
                    "code": "BBB",
                    "name": "Bbb",
                    "tasks": "- Modify: `src/components/mathInputExtension.ts`\n",
                },
            ]
        )
        g = check_graph.harvest(specs)
        keys = [k for k in g["reverse"] if "mathInputExtension.ts" in k]
        self.assertEqual(
            keys, ["src/components/mathInputExtension.ts"], "one merged key, canonicalized to the fullest form"
        )
        self.assertEqual(
            sorted(r["code"] for r in g["reverse"]["src/components/mathInputExtension.ts"]),
            ["AAA", "BBB"],
        )
        shared = next(s for s in g["shared"] if s["path"] == "src/components/mathInputExtension.ts")
        self.assertEqual(len(shared["refs"]), 2, "shared with 2 refs, not 2 separate 1-ref entries")

    def test_harvest_guard_ordinary_same_full_path_sharing_still_detected(self):
        """guard: same-full-path sharing across features still detected after cross-feature dedup."""
        specs = self._spec_fixture(
            [
                {
                    "slug": "a-inltask",
                    "code": "INLTASK",
                    "name": "InlTask",
                    "tasks": "- Create: `src/components/inlineTaskDecorations.ts`\n",
                },
                {
                    "slug": "b-chipui",
                    "code": "CHIPUI",
                    "name": "ChipUi",
                    "tasks": "- Modify: `src/components/inlineTaskDecorations.ts`\n",
                },
            ]
        )
        g = check_graph.harvest(specs)
        shared = next(s for s in g["shared"] if s["path"] == "src/components/inlineTaskDecorations.ts")
        self.assertEqual(sorted(r["code"] for r in shared["refs"]), ["CHIPUI", "INLTASK"])

    def test_harvest_requirements_only_yields_empty_manifest(self):
        """a feature with only requirements.md yields an empty manifest, no error."""
        specs = self._spec_fixture([{"slug": "a", "code": "ONLY", "name": "Only"}])
        f = next(x for x in check_graph.harvest(specs)["features"] if x["code"] == "ONLY")
        self.assertEqual(f["owns"], [])
        self.assertEqual(f["touches"], [])

    def test_harvest_block_label_does_not_leak_past_blank_line_or_heading(self):
        """scanSurface: blockLabel does not leak past a blank line or heading."""
        specs = self._spec_fixture(
            [
                {
                    "slug": "a-leak",
                    "code": "LEAK",
                    "name": "Leak",
                    "design": "**Files:**\n- Create: `src/new/thing.ts`\n\n## Notes\nSee also `src/old/legacy.ts`.\n",
                }
            ]
        )
        f = next(x for x in check_graph.harvest(specs)["features"] if x["code"] == "LEAK")
        self.assertIn("src/new/thing.ts", f["owns"], "the actually-created file is owned")
        self.assertIn("src/old/legacy.ts", f["touches"], "a mere reference after the block ended is only touched")
        self.assertNotIn("src/old/legacy.ts", f["owns"], "stale create block label must not leak onto later prose")

    def test_harvest_ignores_paths_inside_fenced_code_blocks(self):
        """scanSurface ignores paths inside fenced code blocks."""
        specs = self._spec_fixture(
            [
                {
                    "slug": "a",
                    "code": "FENCE",
                    "name": "Fence",
                    "tasks": '**Files:**\n- Create: `src/real.ts`\n\n```js\nimport x from "src/fake.ts";\nconst p = "App.tsx";\n```\n',
                }
            ]
        )
        f = next(x for x in check_graph.harvest(specs)["features"] if x["code"] == "FENCE")
        self.assertIn("src/real.ts", f["owns"], "unfenced Create path kept")
        self.assertNotIn("src/fake.ts", f["owns"] + f["touches"], "fenced path excluded")
        self.assertNotIn("App.tsx", f["owns"] + f["touches"], "fenced path excluded")

    def test_harvest_owns_beats_touches_across_dedup_within_feature(self):
        """owns beats touches across basename/fullpath dedup within a feature."""
        specs = self._spec_fixture(
            [
                {
                    "slug": "a-dedup",
                    "code": "DEDUP",
                    "name": "Dedup",
                    "tasks": "- Create: `engine.ts`\n",
                    "design": "This references the existing `src/core/engine.ts` module.\n",
                }
            ]
        )
        f = next(x for x in check_graph.harvest(specs)["features"] if x["code"] == "DEDUP")
        self.assertIn(
            "src/core/engine.ts", f["owns"], "owns must win over touches after dedup collapses basename into full path"
        )
        self.assertNotIn("src/core/engine.ts", f["touches"])

    def test_harvest_excludes_glob_token_paths(self):
        """harvest excludes glob-token paths from owns/touches."""
        specs = self._spec_fixture(
            [
                {
                    "slug": "a-glob",
                    "code": "GLOB",
                    "name": "Glob",
                    "tasks": "**Files:**\n- Modify: `e2e/*.spec.ts`\n- Create: `src/real.ts`\n",
                }
            ]
        )
        f = next(x for x in check_graph.harvest(specs)["features"] if x["code"] == "GLOB")
        self.assertTrue("src/real.ts" in f["owns"] or "src/real.ts" in f["touches"], "concrete path kept")
        self.assertNotIn("e2e/*.spec.ts", f["owns"] + f["touches"], "glob token excluded")

    def test_harvest_excludes_command_only_paths(self):
        """a path appearing only on a command-invocation line is excluded."""
        specs = self._spec_fixture(
            [
                {
                    "slug": "a-cmd",
                    "code": "CMDONLY",
                    "name": "CmdOnly",
                    "tasks": "**Steps:**\nRun `node scripts/check-trace.js`\n",
                }
            ]
        )
        f = next(x for x in check_graph.harvest(specs)["features"] if x["code"] == "CMDONLY")
        self.assertNotIn(
            "scripts/check-trace.js",
            f["owns"] + f["touches"],
            "path seen only on a command-invocation line must be excluded from the manifest",
        )

    def test_harvest_keeps_path_in_both_modify_bullet_and_command_line(self):
        """a path in both a Modify bullet and a command line is still kept."""
        specs = self._spec_fixture(
            [
                {
                    "slug": "a-mix",
                    "code": "CMDMIX",
                    "name": "CmdMix",
                    "tasks": "**Files:**\n- Modify: `src/x.ts`\n\n**Steps:**\nRun `vitest src/x.ts`\n",
                }
            ]
        )
        f = next(x for x in check_graph.harvest(specs)["features"] if x["code"] == "CMDMIX")
        self.assertTrue(
            "src/x.ts" in f["owns"] or "src/x.ts" in f["touches"],
            "a path with at least one non-command occurrence must still be kept",
        )

    def test_harvest_guard_unfenced_paths_not_over_filtered(self):
        """guard: the 1.7/1.8 filters do not over-reach on ordinary unfenced paths."""
        specs = self._spec_fixture(
            [
                {
                    "slug": "a-keep",
                    "code": "KEEPALL",
                    "name": "KeepAll",
                    "design": "- Create: `src/keep1.ts`\n- Modify: `src/keep2.ts`\nSee also `src/keep3.ts` for context.\n",
                }
            ]
        )
        f = next(x for x in check_graph.harvest(specs)["features"] if x["code"] == "KEEPALL")
        surface = f["owns"] + f["touches"]
        self.assertIn("src/keep1.ts", surface, "unfenced Create bullet path kept")
        self.assertIn("src/keep2.ts", surface, "unfenced Modify bullet path kept")
        self.assertIn("src/keep3.ts", surface, "prose backtick path kept")

    def test_harvest_guard_mid_line_command_word_not_misclassified(self):
        """guard: a command word used as ordinary prose must not drop a real surface path."""
        specs = self._spec_fixture(
            [
                {
                    "slug": "a-prose",
                    "code": "PROSE",
                    "name": "Prose",
                    "design": "See the git log entry referencing `src/onlyhere.ts` for context on this node in the tree.\n",
                }
            ]
        )
        f = next(x for x in check_graph.harvest(specs)["features"] if x["code"] == "PROSE")
        surface = f["owns"] + f["touches"]
        self.assertIn(
            "src/onlyhere.ts",
            surface,
            'prose use of "git"/"node" as ordinary English words must not exclude a real path',
        )

    def test_harvest_card_carries_name_owns_out_of_scope(self):
        """card carries name, owns, and out-of-scope."""
        specs = self._spec_fixture(
            [
                {
                    "slug": "a",
                    "code": "CARD",
                    "name": "Card feature",
                    "oos": ["No time zones", "No recurrence"],
                    "tasks": "- Create: `src/card.ts`\n",
                }
            ]
        )
        f = next(x for x in check_graph.harvest(specs)["features"] if x["code"] == "CARD")
        self.assertEqual(f["name"], "Card feature")
        self.assertIn("src/card.ts", f["owns"])
        self.assertEqual(f["oos"], ["No time zones", "No recurrence"])

    def test_harvest_interfaces_drop_bare_labels_keep_substance(self):
        """interfaces drop bare Produces/Consumes labels, keep substance."""
        specs = self._spec_fixture(
            [
                {
                    "slug": "a",
                    "code": "IF2",
                    "name": "If2",
                    "design": "**Interfaces:**\n- Produces:\n  - `doThing(x) → y`\n- Consumes: `helper()`\n",
                }
            ]
        )
        f = next(x for x in check_graph.harvest(specs)["features"] if x["code"] == "IF2")
        self.assertTrue(any("doThing" in s for s in f["interfaces"]), "substance kept")
        self.assertTrue(any("helper" in s for s in f["interfaces"]), "inline consumes substance kept")
        self.assertFalse(
            any(re.match(r"^(produces|consumes):?$", s.strip(), re.IGNORECASE) for s in f["interfaces"]),
            "no bare label entries",
        )

    def test_harvest_card_lists_capped_at_card_cap(self):
        """card lists are capped at cardCap."""
        many = [f"No feature number {i}" for i in range(20)]
        specs = self._spec_fixture([{"slug": "a", "code": "CAP", "name": "Cap", "oos": many}])
        cfg = {**check_graph.DEFAULTS, "graph": {**check_graph.DEFAULTS["graph"], "cardCap": 5}}
        f = next(x for x in check_graph.harvest(specs, cfg)["features"] if x["code"] == "CAP")
        self.assertEqual(len(f["oos"]), 6, "5 items + 1 elision marker")
        self.assertRegex(f["oos"][5], r"\+15 more")

    def test_harvest_cap_does_not_drop_shared_path_from_reverse_index(self):
        """cap on owns/touches does not drop a shared path from the reverse index."""
        owned = [f"src/gen/file{str(i).zfill(2)}.ts" for i in range(13)]
        specs = self._spec_fixture(
            [
                {
                    "slug": "a-base",
                    "code": "BASE",
                    "name": "Base",
                    "tasks": "".join(f"- Create: `{p}`\n" for p in owned),
                },
                {"slug": "b-ext", "code": "EXT", "name": "Extension", "tasks": f"- Modify: `{owned[-1]}`\n"},
            ]
        )
        g = check_graph.harvest(specs)
        base = next(f for f in g["features"] if f["code"] == "BASE")
        shared = owned[-1]
        self.assertEqual(len(base["owns"]), 13, "card field is capped at 12 + 1 elision marker")
        self.assertRegex(base["owns"][12], r"\+1 more")
        self.assertNotIn(shared, base["owns"], "the 13th file is elided from the capped card field")
        self.assertIn(shared, g["reverse"], "the 13th file must still appear in the reverse index")
        self.assertEqual(sorted(r["code"] for r in g["reverse"][shared]), ["BASE", "EXT"])
        shared_entry = next(s for s in g["shared"] if s["path"] == shared)
        self.assertEqual(len(shared_entry["refs"]), 2)

    def test_harvest_vanilla_specs_yield_nonempty_graph(self):
        """harvest needs no new fields — vanilla specs yield a non-empty graph."""
        specs = self._spec_fixture(
            [
                {
                    "slug": "plain",
                    "code": "PLAIN",
                    "name": "Plain feature",
                    "design": "### Component\nLives in `src/plain/core.ts`.\n",
                    "tasks": "**Files:**\n- Create: `src/plain/core.ts`\n- Modify: `src/plain/wire.ts`\n",
                }
            ]
        )
        f = next(x for x in check_graph.harvest(specs)["features"] if x["code"] == "PLAIN")
        self.assertGreaterEqual(len(f["owns"]) + len(f["touches"]), 2, "surface harvested from standard specs alone")


class RenderGraphMdTest(_FixtureTestCase):
    def test_render_graph_md_deterministic_and_banner_marked(self):
        """renderGraphMd is deterministic and banner-marked."""
        specs = self._spec_fixture(
            [
                {"slug": "b", "code": "BBB", "name": "B", "tasks": "- Create: `src/b.ts`\n- Modify: `src/shared.ts`\n"},
                {"slug": "a", "code": "AAA", "name": "A", "tasks": "- Create: `src/shared.ts`\n"},
            ]
        )
        g = check_graph.harvest(specs)
        once = check_graph.render_graph_md(g)
        twice = check_graph.render_graph_md(check_graph.harvest(specs))
        self.assertEqual(once, twice, "identical input -> byte-identical output")
        self.assertRegex(once, r"GENERATED")
        self.assertLess(once.index("AAA"), once.index("BBB"), "cards ordered by code")
        self.assertRegex(once, r"(?s)src/shared\.ts.*AAA:owns.*BBB:touches")

    def test_render_graph_md_byte_identical_across_independent_harvests(self):
        """guard: renderGraphMd(harvest(fixture)) is byte-identical across two independent harvests."""
        specs = self._spec_fixture(
            [
                {
                    "slug": "a-aaa",
                    "code": "AAA",
                    "name": "Aaa",
                    "tasks": "- Create: `mathInputExtension.ts`\n- Modify: `e2e/*.spec.ts`\n",
                    "design": "**Interfaces:**\n- Produces:\n  - `doThing(x) → y` — long prose\n",
                },
                {
                    "slug": "b-bbb",
                    "code": "BBB",
                    "name": "Bbb",
                    "tasks": "Run `node scripts/build.js`\n- Modify: `src/components/mathInputExtension.ts`\n",
                },
            ]
        )
        once = check_graph.render_graph_md(check_graph.harvest(specs))
        twice = check_graph.render_graph_md(check_graph.harvest(specs))
        self.assertEqual(once, twice, "two independent harvests of the same fixture must render byte-identical markdown")

    def test_render_graph_md_empty_specs_well_formed(self):
        """empty specs render a well-formed empty graph."""
        root = self._tmp_repo({})
        g = check_graph.harvest(os.path.join(root, "docs", "specs"))
        md = check_graph.render_graph_md(g)
        self.assertRegex(md, r"GENERATED")
        self.assertRegex(md, r"## Cards")

    def test_render_graph_md_pure_no_file_side_effects(self):
        """renderGraphMd is a pure string function — no file side effects."""
        specs = self._spec_fixture([{"slug": "a", "code": "PURE", "name": "Pure", "tasks": "- Create: `src/pure.ts`\n"}])
        g = check_graph.harvest(specs)
        before = set(os.listdir(specs))
        result = check_graph.render_graph_md(g)
        self.assertIsInstance(result, str)
        after = set(os.listdir(specs))
        self.assertEqual(before, after, "renderGraphMd must not write any file into specsDir")
        self.assertFalse(
            os.path.exists(os.path.join(specs, "GRAPH.md")), "renderGraphMd must never write GRAPH.md itself"
        )


class QueryTest(_FixtureTestCase):
    def test_query_by_path_returns_ranked_overlapping_features(self):
        """query by path returns ranked overlapping features."""
        specs = self._spec_fixture(
            [
                {"slug": "a", "code": "AAA", "name": "A", "tasks": "- Create: `src/x.ts`\n- Create: `src/y.ts`\n"},
                {"slug": "b", "code": "BBB", "name": "B", "tasks": "- Create: `src/y.ts`\n"},
            ]
        )
        g = check_graph.harvest(specs)
        res = check_graph.query(g, paths=["src/x.ts", "src/y.ts"])
        self.assertEqual(res[0]["code"], "AAA", "AAA overlaps 2 -> ranked first")
        self.assertEqual(res[1]["code"], "BBB", "BBB overlaps 1")
        self.assertTrue(res[0]["card"], "result carries the card")

    def test_query_by_keyword_matches_name_and_out_of_scope(self):
        """query by keyword matches name and out-of-scope."""
        specs = self._spec_fixture(
            [{"slug": "a", "code": "PICK", "name": "Picker widget", "oos": ["No time zones"], "tasks": "- Create: `src/p.ts`\n"}]
        )
        g = check_graph.harvest(specs)
        self.assertEqual(check_graph.query(g, keywords=["picker"])[0]["code"], "PICK")
        self.assertEqual(check_graph.query(g, keywords=["time zone"])[0]["code"], "PICK")
        self.assertEqual(check_graph.query(g, keywords=["nonexistent"]), [])

    def test_query_by_path_ranks_higher_overlap_first(self):
        """query by path ranks a 2-overlap feature above a 1-overlap feature, deterministic tie-break."""
        specs = self._spec_fixture(
            [
                {"slug": "z", "code": "ZZZ", "name": "Z", "tasks": "- Create: `src/only.ts`\n"},
                {"slug": "a", "code": "AAA", "name": "A", "tasks": "- Create: `src/one.ts`\n- Create: `src/two.ts`\n"},
            ]
        )
        g = check_graph.harvest(specs)
        res = check_graph.query(g, paths=["src/one.ts", "src/two.ts", "src/only.ts"])
        self.assertEqual([r["code"] for r in res], ["AAA", "ZZZ"], "higher overlap count ranks first regardless of code order")
        self.assertEqual(res[0]["overlapPaths"], ["src/one.ts", "src/two.ts"], "overlapPaths lists the actually-overlapping paths, sorted")

    def test_query_ties_broken_by_code_ascending_not_path_argument_order(self):
        """query breaks a genuine overlap-count tie by code ascending, not path-argument order."""
        specs = self._spec_fixture(
            [
                {"slug": "z", "code": "ZZZ", "name": "Zebra widget", "tasks": "- Create: `src/z.ts`\n"},
                {"slug": "a", "code": "AAA", "name": "Alpha widget", "tasks": "- Create: `src/a.ts`\n"},
            ]
        )
        g = check_graph.harvest(specs)
        res = check_graph.query(g, paths=["src/z.ts", "src/a.ts"])
        self.assertEqual([r["code"] for r in res], ["AAA", "ZZZ"], "equal overlap count -> ascending by code, not path-argument order")


class CliTest(_FixtureTestCase):
    """CLI black-box tests: subprocess against check_graph.py, no reach into internals."""

    def test_runs_from_a_symlinked_path(self):
        """a linter under a symlinked dir executes its CLI."""
        specs = self._spec_fixture(
            [{"slug": "a", "code": "SYMLINK", "name": "Symlink widget", "tasks": "- Create: `src/s.ts`\n"}]
        )
        root = os.path.dirname(os.path.dirname(specs))
        real_dir = tempfile.mkdtemp(prefix="check-graph-real-")
        self.addCleanup(shutil.rmtree, real_dir, ignore_errors=True)
        shutil.copy(PY_CLI, os.path.join(real_dir, "check_graph.py"))
        # macOS: /tmp is itself a symlink to /private/tmp, so this also covers
        # the case where the *containing directory* is already symlinked.
        link_dir = os.path.join(tempfile.gettempdir(), f"check-graph-link-{os.getpid()}")
        if os.path.exists(link_dir) or os.path.islink(link_dir):
            os.remove(link_dir)
        os.symlink(real_dir, link_dir)
        self.addCleanup(lambda: os.path.exists(link_dir) and os.remove(link_dir))
        script_path = os.path.join(link_dir, "check_graph.py")
        result = subprocess.run(
            [sys.executable, script_path, "--harvest", "--root", root], capture_output=True, text=True
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(
            os.path.exists(os.path.join(specs, "GRAPH.md")),
            "the CLI invoked through the symlinked path must actually run and write GRAPH.md",
        )

    def test_import_does_not_run_main(self):
        """importing the module executes no CLI."""
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import check_graph, sys\n"
                "assert callable(check_graph.main)\n"
                "assert callable(check_graph._invoked_as_script)\n"
                "sys.exit(0)\n",
            ],
            cwd=_SCRIPTS_DIR,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, "", "importing the module must produce no stdout")
        self.assertEqual(result.stderr, "", "importing the module must produce no stderr")

    def test_bad_trace_json_exits_1_with_our_wording(self):
        """the CLI converts ConfigError to exit 1."""
        root = self._tmp_repo({"docs/agents/trace.json": "{ not json"})
        result = subprocess.run(
            [sys.executable, PY_CLI, "--harvest", "--root", root], capture_output=True, text=True
        )
        expected_path = os.path.join(root, "docs/agents/trace.json")
        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "")
        self.assertEqual(result.stderr, f"check-graph: could not parse {expected_path}: invalid JSON\n")
        # no runtime-authored exception text (e.g. CPython's
        # "Expecting property name enclosed in double quotes...").
        self.assertNotIn("Expecting", result.stderr)

    def test_verify_exits_zero_on_fresh_harvest(self):
        """--verify exits 0 when GRAPH.md is fresh."""
        specs = self._spec_fixture(
            [{"slug": "a", "code": "FRESH", "name": "Fresh widget", "tasks": "- Create: `src/fresh.ts`\n"}]
        )
        root = os.path.dirname(os.path.dirname(specs))
        with open(os.path.join(specs, "INDEX.md"), "w", encoding="utf-8") as fh:
            fh.write("| FRESH | Fresh widget | ./a/ | Approved |")
        harvest_result = subprocess.run(
            [sys.executable, PY_CLI, "--harvest", "--root", root], capture_output=True, text=True
        )
        self.assertEqual(harvest_result.returncode, 0, harvest_result.stderr)
        self.assertTrue(os.path.exists(os.path.join(specs, "GRAPH.md")), "harvest must write GRAPH.md")
        verify_result = subprocess.run(
            [sys.executable, PY_CLI, "--verify", "--root", root], capture_output=True, text=True
        )
        self.assertEqual(verify_result.returncode, 0, verify_result.stdout + verify_result.stderr)
        self.assertIn("OK", verify_result.stdout)

    def test_valueless_keyword_flag_exits_zero_with_empty_result(self):
        """a trailing --keyword with no value degrades to no keyword, not a crash."""
        specs = self._spec_fixture(
            [{"slug": "a", "code": "NOVAL", "name": "Noval widget", "tasks": "- Create: `src/n.ts`\n"}]
        )
        root = os.path.dirname(os.path.dirname(specs))
        # --keyword is the last token, with no value following it.
        result = subprocess.run(
            [sys.executable, PY_CLI, "--query", "--json", "--root", root, "--keyword"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout), [])

    def test_flags_accepted_unchanged(self):
        """every documented flag is accepted; unknown flags are ignored."""
        specs = self._spec_fixture(
            [{"slug": "a", "code": "FLAGT", "name": "Flag test", "tasks": "- Create: `src/f.ts`\n"}]
        )
        root = os.path.dirname(os.path.dirname(specs))
        with open(os.path.join(specs, "INDEX.md"), "w", encoding="utf-8") as fh:
            fh.write("| FLAGT | Flag test | ./a/ | Approved |")
        query_result = subprocess.run(
            [
                sys.executable,
                PY_CLI,
                "--query",
                "--json",
                "--path",
                "src/f.ts",
                "--keyword",
                "flag",
                "--root",
                root,
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(query_result.returncode, 0, query_result.stderr)
        parsed = json.loads(query_result.stdout)
        self.assertEqual(parsed[0]["code"], "FLAGT")

        harvest_result = subprocess.run(
            [sys.executable, PY_CLI, "--harvest", "--root", root], capture_output=True, text=True
        )
        self.assertEqual(harvest_result.returncode, 0, harvest_result.stderr)
        self.assertTrue(os.path.exists(os.path.join(specs, "GRAPH.md")))
        verify_result = subprocess.run(
            [sys.executable, PY_CLI, "--verify", "--root", root], capture_output=True, text=True
        )
        self.assertEqual(verify_result.returncode, 0, verify_result.stdout + verify_result.stderr)

        # unknown flags must be ignored silently (argparse would exit 2)
        unknown_result = subprocess.run(
            [sys.executable, PY_CLI, "--bogus-flag", "--root", root], capture_output=True, text=True
        )
        self.assertEqual(
            unknown_result.returncode, 0, "unknown flags must be ignored, not rejected: " + unknown_result.stderr
        )

    def test_harvest_writes_graph_md_and_leaves_index_untouched(self):
        """--harvest writes GRAPH.md and leaves INDEX.md untouched."""
        specs = self._spec_fixture([{"slug": "a", "code": "AAA", "name": "A", "tasks": "- Create: `src/a.ts`\n"}])
        root = os.path.dirname(os.path.dirname(specs))
        with open(os.path.join(specs, "INDEX.md"), "w", encoding="utf-8") as fh:
            fh.write("ORIGINAL")
        result = subprocess.run([sys.executable, PY_CLI, "--harvest", "--root", root], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        with open(os.path.join(specs, "GRAPH.md"), "r", encoding="utf-8") as fh:
            self.assertRegex(fh.read(), "AAA")
        with open(os.path.join(specs, "INDEX.md"), "r", encoding="utf-8") as fh:
            self.assertEqual(fh.read(), "ORIGINAL")

    def test_query_emits_fresh_json_to_stdout_without_a_prior_harvest(self):
        """--query emits fresh JSON to stdout."""
        specs = self._spec_fixture([{"slug": "a", "code": "AAA", "name": "A", "tasks": "- Create: `src/a.ts`\n"}])
        root = os.path.dirname(os.path.dirname(specs))
        # No GRAPH.md written; query must still work via a fresh harvest.
        self.assertFalse(os.path.exists(os.path.join(specs, "GRAPH.md")))
        result = subprocess.run(
            [sys.executable, PY_CLI, "--query", "--path", "src/a.ts", "--json", "--root", root],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = json.loads(result.stdout)
        self.assertEqual(parsed[0]["code"], "AAA")

    def test_verify_fails_on_stale_passes_when_fresh(self):
        """--verify fails on stale, passes when fresh."""
        specs = self._spec_fixture([{"slug": "a", "code": "AAA", "name": "A", "tasks": "- Create: `src/a.ts`\n"}])
        root = os.path.dirname(os.path.dirname(specs))
        with open(os.path.join(specs, "INDEX.md"), "w", encoding="utf-8") as fh:
            fh.write("| AAA | A | ./a/ | Approved |")

        def verify():
            return subprocess.run([sys.executable, PY_CLI, "--verify", "--root", root], capture_output=True, text=True)

        self.assertEqual(verify().returncode, 1, "no GRAPH.md yet -> stale")
        harvest_result = subprocess.run([sys.executable, PY_CLI, "--harvest", "--root", root], capture_output=True, text=True)
        self.assertEqual(harvest_result.returncode, 0, harvest_result.stderr)
        self.assertEqual(verify().returncode, 0, "after harvest -> fresh")
        with open(os.path.join(specs, "GRAPH.md"), "a", encoding="utf-8") as fh:
            fh.write("\nhand edit\n")
        self.assertEqual(verify().returncode, 1, "hand edit -> stale again")

    def test_verify_fails_on_a_code_absent_from_index(self):
        """--verify fails on a code absent from INDEX.md."""
        specs = self._spec_fixture([{"slug": "a", "code": "GHOST", "name": "Ghost", "tasks": "- Create: `src/g.ts`\n"}])
        root = os.path.dirname(os.path.dirname(specs))
        with open(os.path.join(specs, "INDEX.md"), "w", encoding="utf-8") as fh:
            fh.write("| OTHER | x | ./x/ | Draft |")
        subprocess.run([sys.executable, PY_CLI, "--harvest", "--root", root], capture_output=True, text=True)
        result = subprocess.run([sys.executable, PY_CLI, "--verify", "--root", root], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertRegex(result.stdout + result.stderr, "GHOST")

    def test_reads_only_markdown_no_network_build_or_subprocess(self):
        """check_graph.py reads only markdown — no network/build/subprocess calls."""
        with open(os.path.join(_SCRIPTS_DIR, "check_graph.py"), "r", encoding="utf-8") as fh:
            src = fh.read()
        self.assertNotRegex(
            src,
            re.compile(r"^\s*(import|from)\s+(subprocess|socket|urllib\S*|http\.client)\b", re.MULTILINE),
            "no network/process imports",
        )
        self.assertNotRegex(src, r"\burlopen\s*\(", "no network call")
        self.assertNotRegex(src, r"\bsubprocess\.\w+\s*\(", "no subprocess/build calls")
        self.assertNotRegex(src, r"\bos\.(system|popen)\s*\(", "no shell-out calls")

    def test_check_trace_test_suite_still_passes(self):
        """the existing check_trace_test.py suite still passes."""
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "check_trace_test"],
            cwd=_SCRIPTS_DIR,
            capture_output=True,
            text=True,
        )
        self.assertEqual(
            result.returncode, 0, "check_graph must not disturb check_trace: " + result.stdout + result.stderr
        )


class LoadManifestTest(unittest.TestCase):
    def test_absent_modules_key_disables_layer_MODMAP_1_1_4_1(self):
        # covers MODMAP-1.1, MODMAP-4.1
        mods, errs = check_graph.load_manifest({"specsDir": "docs/specs", "graph": {}})
        self.assertEqual(mods, [])
        self.assertEqual(errs, [])

    def test_valid_entry_parsed_with_optional_fields_MODMAP_1_1_1_2(self):
        # covers MODMAP-1.1, MODMAP-1.2
        cfg = {"modules": [
            {"code": "BILLING", "name": "Billing", "owns": ["src/billing/**"],
             "layer": "domain", "owner": "@team-pay"}]}
        mods, errs = check_graph.load_manifest(cfg)
        self.assertEqual(errs, [])
        self.assertEqual(len(mods), 1)
        self.assertEqual(mods[0]["code"], "BILLING")
        self.assertEqual(mods[0]["owns"], ["src/billing/**"])
        self.assertEqual(mods[0]["layer"], "domain")
        self.assertEqual(mods[0]["owner"], "@team-pay")

    def test_missing_required_fields_error_MODMAP_1_3(self):
        # covers MODMAP-1.3
        cfg = {"modules": [{"code": "A1", "owns": ["src/**"]},
                           {"code": "B1", "name": "B", "owns": []},
                           {"name": "C", "owns": ["src/c/**"]}]}
        mods, errs = check_graph.load_manifest(cfg)
        blob = "\n".join(errs)
        self.assertIn("A1", blob)
        self.assertIn("B1", blob)
        self.assertIn("missing", blob.lower())

    def test_duplicate_code_error_MODMAP_1_4(self):
        # covers MODMAP-1.4
        cfg = {"modules": [{"code": "DUP", "name": "One", "owns": ["src/a/**"]},
                           {"code": "DUP", "name": "Two", "owns": ["src/b/**"]}]}
        _, errs = check_graph.load_manifest(cfg)
        self.assertTrue(any("duplicate" in e.lower() and "DUP" in e for e in errs))

    def test_malformed_code_error_MODMAP_1_5(self):
        # covers MODMAP-1.5
        cfg = {"modules": [{"code": "lower", "name": "L", "owns": ["src/l/**"]}]}
        _, errs = check_graph.load_manifest(cfg)
        self.assertTrue(any("malformed" in e.lower() and "lower" in e for e in errs))

    def test_code_length_bounds_MODMAP_1_5(self):
        # covers MODMAP-1.5
        def errs_for(code):
            return check_graph.load_manifest(
                {"modules": [{"code": code, "name": "n", "owns": ["src/**"]}]})[1]
        self.assertTrue(any("malformed" in e for e in errs_for("A")))       # 1 char
        self.assertTrue(any("malformed" in e for e in errs_for("A" * 13)))  # 13 chars
        self.assertEqual(errs_for("AB"), [])                                # 2 chars ok
        self.assertEqual(errs_for("A" * 12), [])                            # 12 chars ok

    def test_non_list_modules_is_error_not_crash_MODMAP_1_3(self):
        # covers MODMAP-1.3
        for bad in (True, 5, "AUTH"):
            mods, errs = check_graph.load_manifest({"modules": bad})
            self.assertEqual(mods, [])
            self.assertTrue(errs, f"a non-list modules value {bad!r} must yield an error, not a crash")

    def test_load_config_keeps_config_when_modules_present_MODMAP_4_4(self):
        # covers MODMAP-4.4
        root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, root)
        os.makedirs(os.path.join(root, "docs/agents"))
        with open(os.path.join(root, "docs/agents/trace.json"), "w") as fh:
            json.dump({"specsDir": "docs/specs",
                       "modules": [{"code": "M1", "name": "M", "owns": ["src/**"]}]}, fh)
        cfg = check_graph.load_config(root)
        self.assertEqual(cfg["specsDir"], "docs/specs")
        self.assertIn("sourceRoots", cfg["graph"])
        mods, errs = check_graph.load_manifest(cfg)
        self.assertEqual(errs, [])
        self.assertEqual(mods[0]["code"], "M1")


class GlobResolveTest(unittest.TestCase):
    def test_glob_subtree_and_segment_MODMAP_2_1(self):
        # covers MODMAP-2.1
        self.assertTrue(check_graph._glob_to_re("src/auth/**").match("src/auth"))
        self.assertTrue(check_graph._glob_to_re("src/auth/**").match("src/auth/login"))
        self.assertFalse(check_graph._glob_to_re("src/auth").match("src/auth/login"))
        self.assertTrue(check_graph._glob_to_re("packages/*").match("packages/api"))
        self.assertFalse(check_graph._glob_to_re("packages/*").match("packages/api/core"))

    def test_resolve_single_owner_MODMAP_2_1(self):
        # covers MODMAP-2.1
        mods = [{"code": "AUTH", "owns": ["src/auth/**"]},
                {"code": "BILL", "owns": ["src/billing/**"]}]
        self.assertEqual(check_graph.resolve_module("src/auth/login", mods), ["AUTH"])

    def test_resolve_double_mapped_MODMAP_2_2(self):
        # covers MODMAP-2.2
        mods = [{"code": "AAA", "owns": ["src/shared/**"]},
                {"code": "BBB", "owns": ["src/shared/**"]}]
        self.assertEqual(check_graph.resolve_module("src/shared/util", mods), ["AAA", "BBB"])

    def test_resolve_orphan_MODMAP_2_3(self):
        # covers MODMAP-2.3
        mods = [{"code": "AUTH", "owns": ["src/auth/**"]}]
        self.assertEqual(check_graph.resolve_module("src/unclaimed", mods), [])

    def test_resolve_preserves_digit_suffixed_folder_MODMAP_2_1(self):
        # covers MODMAP-2.1
        # guards against normalize_path stripping the trailing digit (store2->store)
        mods = [{"code": "STORE", "owns": ["src/store2/**"]}]
        self.assertEqual(check_graph.resolve_module("src/store2/db", mods), ["STORE"])


class EnumerateFoldersTest(_FixtureTestCase):
    def test_enumerates_repo_and_source_folders_MODMAP_3_1(self):
        # covers MODMAP-3.1
        root = self._tmp_repo({
            "src/auth/login.ts": "x",
            "src/auth/helpers/util.ts": "x",
            "src/assets/logo.png": "x",
            "src/container/inner/svc.ts": "x",
            "node_modules/pkg/index.ts": "x",
        })
        cfg = {"graph": {"sourceRoots": ["src"], "sourceExts": ["ts"], "cardCap": 12}}
        repo, source = check_graph.enumerate_folders(root, cfg)
        self.assertIn("src/auth", source)
        self.assertIn("src/auth/helpers", source)
        self.assertIn("src/container/inner", source)
        self.assertNotIn("src/assets", source)
        self.assertNotIn("src/container", source)
        self.assertIn("src/container", repo)
        self.assertTrue(all("node_modules" not in f for f in repo))


class VerifyBoundariesTest(_FixtureTestCase):
    def _cfg(self):
        return {"graph": {"sourceRoots": ["src"], "sourceExts": ["ts"], "cardCap": 12}}

    def test_orphan_folder_is_error_MODMAP_3_2(self):
        # covers MODMAP-3.2
        root = self._tmp_repo({"src/auth/a.ts": "x", "src/lonely/b.ts": "x"})
        mods = [{"code": "AUTH", "name": "A", "owns": ["src/auth/**"]}]
        errs, warns = check_graph._verify_boundaries(root, self._cfg(), mods)
        self.assertTrue(any("src/lonely" in e and "orphan" in e.lower() for e in errs))

    def test_double_mapped_folder_is_error_MODMAP_3_3(self):
        # covers MODMAP-3.3
        root = self._tmp_repo({"src/shared/a.ts": "x"})
        mods = [{"code": "AAA", "name": "A", "owns": ["src/shared/**"]},
                {"code": "BBB", "name": "B", "owns": ["src/**"]}]
        errs, _ = check_graph._verify_boundaries(root, self._cfg(), mods)
        self.assertTrue(any("src/shared" in e and "AAA" in e and "BBB" in e for e in errs))

    def test_stale_glob_is_warning_not_error_MODMAP_3_4(self):
        # covers MODMAP-3.4
        root = self._tmp_repo({"src/auth/a.ts": "x"})
        mods = [{"code": "AUTH", "name": "A", "owns": ["src/auth/**", "src/ghost/**"]}]
        errs, warns = check_graph._verify_boundaries(root, self._cfg(), mods)
        self.assertEqual(errs, [])
        self.assertTrue(any("src/ghost" in w and "AUTH" in w for w in warns))

    def test_full_coverage_is_clean_MODMAP_3_5(self):
        # covers MODMAP-3.5
        root = self._tmp_repo({"src/auth/a.ts": "x", "src/auth/sub/b.ts": "x"})
        mods = [{"code": "AUTH", "name": "A", "owns": ["src/auth/**"]}]
        errs, warns = check_graph._verify_boundaries(root, self._cfg(), mods)
        self.assertEqual(errs, [])
        self.assertEqual(warns, [])


class VerifyIntegrationTest(_FixtureTestCase):
    def _repo_with_specs(self, extra, trace):
        files = dict(extra)
        root = self._tmp_repo(files)
        os.makedirs(os.path.join(root, "docs/agents"), exist_ok=True)
        with open(os.path.join(root, "docs/agents/trace.json"), "w") as fh:
            json.dump(trace, fh)
        os.makedirs(os.path.join(root, "docs/specs"), exist_ok=True)
        open(os.path.join(root, "docs/specs/INDEX.md"), "w").close()
        # generate a non-stale GRAPH.md through the real harvest path so the two
        # existing --verify checks pass (no features -> empty, self-consistent).
        check_graph.main(["--harvest", "--root", root])
        return root

    def test_warnings_do_not_fail_the_gate_MODMAP_3_4_3_7(self):
        # covers MODMAP-3.4, MODMAP-3.7
        root = self._repo_with_specs(
            {"src/auth/a.ts": "x"},
            {"specsDir": "docs/specs",
             "modules": [{"code": "AUTH", "name": "A",
                          "owns": ["src/auth/**", "src/ghost/**"]}]})
        rc = check_graph.main(["--verify", "--root", root])
        self.assertEqual(rc, 0)

    def test_orphan_fails_the_gate_MODMAP_3_6(self):
        # covers MODMAP-3.6
        root = self._repo_with_specs(
            {"src/auth/a.ts": "x", "src/orphan/b.ts": "x"},
            {"specsDir": "docs/specs",
             "modules": [{"code": "AUTH", "name": "A", "owns": ["src/auth/**"]}]})
        rc = check_graph.main(["--verify", "--root", root])
        self.assertEqual(rc, 1)

    def test_no_manifest_behaves_as_before_MODMAP_4_2(self):
        # covers MODMAP-4.2
        root = self._repo_with_specs(
            {"src/whatever/a.ts": "x"}, {"specsDir": "docs/specs"})
        rc = check_graph.main(["--verify", "--root", root])
        self.assertEqual(rc, 0)

    def test_existing_checks_still_run_with_manifest_MODMAP_4_3(self):
        # covers MODMAP-4.3
        root = self._repo_with_specs(
            {"src/auth/a.ts": "x"},
            {"specsDir": "docs/specs",
             "modules": [{"code": "AUTH", "name": "A", "owns": ["src/auth/**"]}]})
        with open(os.path.join(root, "docs/specs/GRAPH.md"), "w") as fh:
            fh.write("stale content")
        rc = check_graph.main(["--verify", "--root", root])
        self.assertEqual(rc, 1)

    def test_invalid_manifest_fails_and_skips_coverage_MODMAP_1_3(self):
        # covers MODMAP-1.3
        import io
        import contextlib
        root = self._repo_with_specs(
            {"src/orphan/a.ts": "x"},
            {"specsDir": "docs/specs",
             "modules": [{"code": "AUTH", "owns": ["src/auth/**"]}]})  # missing name
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = check_graph.main(["--verify", "--root", root])
        out = buf.getvalue()
        self.assertEqual(rc, 1)                 # validity error fails the gate
        self.assertIn("missing 'name'", out)    # validity error reported
        self.assertNotIn("orphan", out)         # coverage pass was skipped

    def test_import_has_no_side_effects_MODMAP_4_5(self):
        # covers MODMAP-4.5
        import importlib
        import io
        import contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            mod = importlib.reload(check_graph)
        self.assertEqual(buf.getvalue(), "")    # importing runs no CLI/output
        self.assertTrue(hasattr(mod, "_run_verify"))


if __name__ == "__main__":
    unittest.main()
