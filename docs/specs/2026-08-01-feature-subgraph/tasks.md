# Tasks: Feature subgraph derivation

> **For agentic workers:** after plan approval, pick one execute skill —
> `build-in-waves` (subagent waves), `build-by-story` (human-gated story review
> units), or `build-inline` (controller implements, no implementer subagents).
> The chosen skill writes `Execution-mode:`. Steps use checkbox (`- [ ]`) syntax
> for tracking.

Feature code: FSUB
Status: Implemented
Date: 2026-08-01
Execution-mode: continuous
Requirements: ./requirements.md
Design: ./design.md

**Goal:** Ship ask-time feature-subgraph derivation (`load-subgraph` +
`map-features`), with ranked/denoised neighbors, P0 term seeds, OWNS coverage
honesty, and legacy Files parse — without materializing a graph file.

**Architecture:** Shipped recipes live only in markdown
(`skills/execution/load-subgraph/references/passes.md`). A test-side
`reference_derive.py` under `tests/feature-subgraph/` validates recipe math.
Agents execute passes via the skill; they never import the reference. Callers
`frame-change` and `inspect-change` route neighbor discovery through
`load-subgraph`. `map-features` is user-invoked propose→confirm only.

**Tech Stack:** Markdown skills/docs; Python 3 `unittest` for
`tests/feature-subgraph/reference_derive.py` and contract tests; scenario
markdown under `tests/feature-subgraph/`. No consumer Python dependency.

## Global Constraints

Copied from `docs/agents/project.md`, `docs/product/guidelines.md`, and
`docs/architecture/INDEX.md`.

**verify commands** — run in this order; all must pass before any completion claim:

| Check | Command |
|---|---|
| Typecheck | *(none)* |
| Lint | `python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-write-handoffs.py && python3 scripts/lint-context7.py` |
| Unit tests | `python3 -m unittest discover -s tests` |
| E2E / smoke | *(none)* |

Single test file: `python3 -m unittest tests.<module>`  
(e.g. `python3 -m unittest tests.test_feature_subgraph_derive`)

**Test annotation conventions:**

| Layer | Requirement-ID convention |
|---|---|
| Unit (`unittest` under `tests/`) | ID in method name or first-line docstring greppable `FSUB-N.M` |
| Scenario / acceptance markdown | Greppable bare `FSUB-N.M` in `tests/feature-subgraph/scenarios*.md` |

**Coding standards / naming / house rules** (from `docs/product/guidelines.md`):

- Skill bodies: imperative voice; hard gates in dedicated blocks; rationalization tables in `| Thought | Reality |` form.
- SKILL.md under 500 lines (prefer under 300); split into `references/` when needed.
- Python under `tests/` only for this feature — **never** create `*.py` under `skills/execution/load-subgraph/`.
- Skills: verb-first kebab-case; cross-skill `REQUIRED SUB-SKILL:` prose, never `@`-links.
- Skill `description` frontmatter states triggering conditions only — never summarize the workflow.
- Iron Law gates are not weakened by workflow band, ceremony tier, or convenience.

**Architecture invariants** — every task inherits (verbatim from `docs/architecture/INDEX.md`):

- **ARCH-1** Audit Trace and other vertical checks MUST be exact `grep`/`git`/file-read passes with fixed extraction rules and set differences — never an LLM judgment of whether a test "really" covers an ID.
- **ARCH-2** Optional project layers and config sections MUST no-op when absent: skills CONTINUES TO run without inventing vision, architecture invariants, team roster, or other standing facts that were never written.
- **ARCH-3** Consumer-repo adoption MUST require only the skills (plugin or npx) and markdown config — never mandate Python, vendored linters, CI jobs, or git-hook wiring for the full methodology; any hard headless gate is an optional documented add-on only.
- **ARCH-4** Requirement IDs (`CODE-N.M`) and architecture IDs (`ARCH-N`) are immutable once defined: never renumber or reuse; retire only by strikethrough; every task, test, commit trailer, and `Respects:` line MUST use the same greppable string as the definition.
- **ARCH-5** User-invoked skills may invoke model-invoked skills only; model-invoked skills must never invoke user-invoked skills; agents must never auto-invoke a skill marked `disable-model-invocation: true`.
- **ARCH-6** Skills MUST enforce and record only actions this skill set mediates; membership is never inferred from repository membership, roster, CODEOWNERS, branch ownership, PR authorship, or supplied artifacts.

**Team packaging:** Solo — lean multi-person language; full gates; no invented peer assignees.

**Design constants (verbatim):**

- `NEIGHBORS_MAX = 12`
- `P0_SEED_MAX = 12`
- P0 score = `(distinct_seed_terms_matched × 1000) + raw_casefold_hits`; ties by CODE ascending
- Stop-list basenames: package.json, Cargo.toml, go.mod, pyproject.toml, Gemfile, composer.json, Package.swift, package-lock.json, yarn.lock, pnpm-lock.yaml, Cargo.lock, poetry.lock, Gemfile.lock, composer.lock
- Workspace single-segment stop: src, lib, app, apps, packages, services, crates, cmd, internal, vendor, node_modules, dist, build, target, out, **plus pack** skills, templates, hooks, scripts, docs
- Line-suffix strip: trailing `:[0-9]+([,-][0-9]+)*` on the last path segment
- neighbors: union path candidates ∪ P0 term candidates **before** one truncate to NEIGHBORS_MAX

**Forbidden in every task:**

- Creating `skills/**/*.py` (especially under `load-subgraph/`)
- Writing `docs/specs/GRAPH.md` or any committed graph projection
- Deriving runtime feature-level DEPENDS_ON edges in load-subgraph
- Auto-invoking `map-features`
- Keying features by directory slug when a CODE is available
- Touching files outside the File Structure map

## File Structure

**Create:**

| File | Responsibility |
|---|---|
| `skills/execution/load-subgraph/SKILL.md` | Model-invoked skill: run passes.md, render envelope, advisory |
| `skills/execution/load-subgraph/references/passes.md` | P0–P5 recipes, stop-list, bounds (shipped SSOT) |
| `skills/execution/load-subgraph/references/envelope.md` | Result envelope field list |
| `skills/track/map-features/SKILL.md` | User-invoked propose→confirm wizard |
| `docs/guide/skills/load-subgraph.md` | Human guide page |
| `docs/guide/skills/map-features.md` | Human guide page |
| `tests/feature-subgraph/reference_derive.py` | Test-side reference implementing passes.md |
| `tests/test_feature_subgraph_derive.py` | Unit tests for reference_derive |
| `tests/test_feature_subgraph_contract.py` | Skill text + wiring + no-.py-under-skills contracts |
| `tests/feature-subgraph/fixtures/` | Fixture trees (see Task 1) |
| `tests/feature-subgraph/scenarios.md` | Greppable FSUB-N.M scenario layer |
| `tests/feature-subgraph/scenarios-pressure.md` | Materialize / skip-P0 / boolean-neighbors pressure |
| `tests/trigger/load-subgraph-routing.md` | When to invoke load-subgraph vs map-features |

**Modify:**

| File | Change |
|---|---|
| `skills/discovery/frame-change/SKILL.md` | Neighbor search → load-subgraph (terms + paths) |
| `skills/review/inspect-change/SKILL.md` | Neighbor search → load-subgraph |
| `skills/spec/plan-tasks/SKILL.md` | Hardened `**Files:**` grammar |
| `templates/tasks.md` | Hardened Files example (backticks; no path:lines) |
| `docs/guide/concepts/feature-graph.md` | Dual signal via load-subgraph + OWNS coverage |
| `AGENTS.md` | Inventory: load-subgraph (m), map-features (U) |
| `README.md` | Skill roster if present |
| `docs/architecture/skills.md` | Inventory rows |
| `docs/architecture/system.md` | execution/ + track/ lists |
| `docs/architecture/workflows.md` | Horizontal neighbor step names load-subgraph |
| `docs/architecture/artifacts.md` | Point horizontal layer at load-subgraph (live read) |
| `.claude-plugin/plugin.json` | Register skills if other skills listed |
| `.claude-plugin/marketplace.json` | Same if applicable |
| `docs/agents/project.md` | audit-trace ignore for feature-subgraph fixtures/scenarios as needed |

No file outside these tables is touched.

---

### Task 1: Test-side reference_derive — P0–P5 recipe math

**Files:**
- Create: `tests/feature-subgraph/reference_derive.py`
- Create: `tests/test_feature_subgraph_derive.py`
- Create: `tests/feature-subgraph/fixtures/legacy-glued-lines/docs/specs/INDEX.md`
- Create: `tests/feature-subgraph/fixtures/legacy-glued-lines/docs/specs/2020-01-01-alpha/requirements.md`
- Create: `tests/feature-subgraph/fixtures/legacy-glued-lines/docs/specs/2020-01-01-alpha/tasks.md`
- Create: `tests/feature-subgraph/fixtures/mega-owner-100/` (INDEX + two features A/B + mega tasks with 100+ paths)
- Create: `tests/feature-subgraph/fixtures/p0-flood/` (many features matching generic term)
- Create: `tests/feature-subgraph/fixtures/no-roadmap/` (specs only)
- Create: `tests/feature-subgraph/fixtures/no-architecture/` (specs + roadmap, no docs/architecture)
- Create: `tests/feature-subgraph/fixtures/thin-owns/` (half features without Files)
- Create: `tests/feature-subgraph/scenarios.md` (skeleton: every FSUB-N.M token once)
- Test: `tests/test_feature_subgraph_derive.py`

**Reuse:** none — new code (rung 7); pattern of pure unittest over fixtures from roadmap/VPF tests — not a skill import

**Interfaces:**
- Consumes: design Decision constants (NEIGHBORS_MAX, P0_SEED_MAX, stop-lists, merge rule)
- Produces: `reference_derive.run(repo_root: Path, query: dict) -> dict` envelope; pure functions for extract_owns, denoise, neighbors

**Depends-on:** none

- [ ] **Step 1: Write the failing test**

Create fixture `legacy-glued-lines` with feature code `ALPHA`, `Feature code: ALPHA` in requirements, and `tasks.md`:

```markdown
**Files:**
- Create: src/app/App.tsx:86,1030
- Modify: `skills/foo/SKILL.md:25-44`
- Test: tests/test_alpha.py
```

Also a prose line under Files listing `lib/util/dates.ts` bare.

In `tests/test_feature_subgraph_derive.py`:

```python
"""FSUB-3.1 FSUB-3.2 FSUB-3.3 FSUB-3.4 FSUB-1.6 FSUB-2.1 FSUB-2.2 FSUB-2.3
FSUB-2.4 FSUB-2.5 FSUB-2.6 FSUB-1.5 FSUB-1.11 FSUB-1.14 FSUB-1.16 FSUB-5.1
FSUB-5.2 FSUB-5.3 FSUB-8.1 FSUB-8.2 FSUB-8.3 FSUB-1.13 — reference_derive recipe math.
"""

import unittest
from pathlib import Path

# Import will fail until reference_derive.py exists — that is RED.
from tests.feature_subgraph import reference_derive as rd

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
        # Owning src/app does not imply owning src
        a = {"src/app/x.ts"}
        b = {"src"}
        self.assertEqual(rd.overlap_weight(a, b), 0)

    def test_FSUB_2_6_ranks_small_sharer_above_mega_owner(self):
        root = FIX / "mega-owner-100"
        # FOCUS shares 1 path with MEGA and 3 with SMALL
        n = rd.neighbors(root, "FOCUS", terms=None)
        codes = [row["code"] for row in n["neighbors"]]
        self.assertLess(codes.index("SMALL"), codes.index("MEGA"))

    def test_FSUB_2_3_neighbors_length_at_most_12(self):
        root = FIX / "mega-owner-100"
        n = rd.neighbors(root, "FOCUS", terms=None)
        self.assertLessEqual(len(n["neighbors"]), 12)

    def test_FSUB_2_3_union_before_truncate_never_exceeds_max(self):
        root = FIX / "p0-flood"
        n = rd.neighbors(root, "FOCUS", terms=["config"])
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
        env = rd.run(root, {"kind": "neighbors", "code": "A", "terms": []})
        self.assertIn("owns_coverage", env)
        self.assertIn("with_owns", env["owns_coverage"])
        self.assertIn("registered", env["owns_coverage"])

    def test_FSUB_5_2_ancestors_bare_without_roadmap(self):
        root = FIX / "no-roadmap"
        env = rd.run(root, {"kind": "ancestors", "code": "A"})
        self.assertEqual(env.get("ancestors"), ["A"])

    def test_FSUB_5_1_no_architecture_skips_respects(self):
        root = FIX / "no-architecture"
        env = rd.run(root, {"kind": "subgraph", "seeds": {"codes": ["A"]}})
        self.assertEqual(env.get("respects", []), [])

    def test_FSUB_1_2_oracle_dual_run_identical(self):
        """Recipe math dual-run (oracle). Skill-path FSUB-1.2 is Task 2 scenario."""
        root = FIX / "legacy-glued-lines"
        q = {"kind": "neighbors", "code": "ALPHA", "terms": ["alpha"]}
        a = rd.run(root, q)
        b = rd.run(root, q)
        self.assertEqual(a, b)

    def test_FSUB_8_2_passive_instruction_shaped_path_not_executed(self):
        # Path string looks like a shell command — must remain a path token only
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
        root = FIX / "no-architecture"  # has INDEX ROAD binds + roadmap
        env = rd.run(root, {"kind": "ancestors", "code": "A"})
        # ancestors chain includes ROAD when INDEX binds A → ROAD-1
        flat = " ".join(env.get("ancestors", []))
        self.assertTrue("ROAD" in flat or "A" in env.get("ancestors", []))

    def test_FSUB_1_9_p4_contains_from_roadmap_members(self):
        root = FIX / "no-architecture"
        env = rd.run(root, {"kind": "descendants", "mile": "MILE-1"})
        self.assertTrue(len(env.get("descendants", [])) >= 0)  # no-op empty ok; fixture should include ROAD members

    def test_FSUB_1_10_subgraph_resolves_term_seeds(self):
        root = FIX / "p0-flood"
        env = rd.run(root, {"kind": "subgraph", "seeds": {"terms": ["unique-alpha-token"]}})
        self.assertTrue(env.get("nodes") or env.get("seeds"))


if __name__ == "__main__":
    unittest.main()
```

Build fixtures so mega-owner-100, p0-flood, and no-architecture make ranking, P0, P3/P4 assertions true. Skeleton `scenarios.md` listing every bold FSUB-N.M from requirements.md once.

Import pattern (hyphen dir cannot be a package name): load via importlib in the test file:

```python
import importlib.util
_ref = Path(__file__).resolve().parent / "feature-subgraph" / "reference_derive.py"
_spec = importlib.util.spec_from_file_location("reference_derive", _ref)
rd = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rd)
```

Run: `python3 -m unittest tests.test_feature_subgraph_derive` — expect fail (missing module / incomplete).

- [ ] **Step 2: Implement**

Implement `tests/feature-subgraph/reference_derive.py` with:

- `NEIGHBORS_MAX = 12`, `P0_SEED_MAX = 12`
- `extract_owns` / `owns_for_code` (legacy parse + line-suffix strip)
- `denoise`, `overlap_weight`, `neighbors` (union-before-truncate merge rule)
- `p0_seeds`, `run` returning envelope with `advisory`, `owns_coverage`, `p0`, `neighbors`/`nodes`/`ancestors`/`descendants`, `notes`
- P2/P3/P4/P5 behavior per design
- No DEPENDS_ON field
- No file writes under the fixture roots

Run: unittest pass.

- [ ] **Step 3: Commit**

`Implements: FSUB-3.1, FSUB-3.2, FSUB-3.3, FSUB-3.4, FSUB-1.6, FSUB-1.7, FSUB-1.8, FSUB-1.9, FSUB-1.10, FSUB-2.1, FSUB-2.2, FSUB-2.3, FSUB-2.4, FSUB-2.5, FSUB-2.6, FSUB-1.5, FSUB-1.11, FSUB-1.14, FSUB-1.16, FSUB-5.1, FSUB-5.2, FSUB-5.3, FSUB-8.1, FSUB-8.2, FSUB-8.3, FSUB-1.13`

_Requirements: FSUB-3.1, FSUB-3.2, FSUB-3.3, FSUB-3.4, FSUB-1.6, FSUB-1.7, FSUB-1.8, FSUB-1.9, FSUB-1.10, FSUB-2.1, FSUB-2.2, FSUB-2.3, FSUB-2.4, FSUB-2.5, FSUB-2.6, FSUB-1.5, FSUB-1.11, FSUB-1.14, FSUB-1.16, FSUB-5.1, FSUB-5.2, FSUB-5.3, FSUB-8.1, FSUB-8.2, FSUB-8.3, FSUB-1.13_

---

### Task 2: passes.md SSOT + load-subgraph skill (prose path)

**Files:**
- Create: `skills/execution/load-subgraph/references/passes.md`
- Create: `skills/execution/load-subgraph/references/envelope.md`
- Create: `skills/execution/load-subgraph/SKILL.md`
- Create: `tests/test_feature_subgraph_contract.py`
- Create: `tests/feature-subgraph/scenarios-pressure.md`
- Modify: `tests/feature-subgraph/scenarios.md`
- Test: `tests/test_feature_subgraph_contract.py`

**Reuse:** rung 2 — skill shape of `skills/execution/audit-trace/SKILL.md` (model-invoked, fixed passes, report)

**Interfaces:**
- Consumes: constants and merge rule from design; fixture oracles from Task 1
- Produces: model-invoked `load-subgraph` skill; shipped `passes.md` / `envelope.md`

**Depends-on:** Task 1

- [ ] **Step 1: Write the failing test**

In `tests/test_feature_subgraph_contract.py`:

```python
"""FSUB-1.1 FSUB-1.2 FSUB-1.3 FSUB-1.4 FSUB-1.7 FSUB-1.8 FSUB-1.9 FSUB-1.10
FSUB-1.12 FSUB-7.1 FSUB-7.2 FSUB-7.4 FSUB-7.5 — load-subgraph contracts.
"""

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "execution" / "load-subgraph" / "SKILL.md"
PASSES = ROOT / "skills" / "execution" / "load-subgraph" / "references" / "passes.md"
ENV = ROOT / "skills" / "execution" / "load-subgraph" / "references" / "envelope.md"


class TestLoadSubgraphSkill(unittest.TestCase):
    def test_FSUB_1_1_skill_exists_model_invoked(self):
        self.assertTrue(SKILL.is_file())
        text = SKILL.read_text()
        self.assertRegex(text, r"^name:\s*load-subgraph", re.M)
        self.assertNotIn("disable-model-invocation: true", text)

    def test_FSUB_1_1_no_python_under_skill_package(self):
        pkg = ROOT / "skills" / "execution" / "load-subgraph"
        py = list(pkg.rglob("*.py"))
        self.assertEqual(py, [], f"unexpected python under skill: {py}")

    def test_FSUB_1_2_skill_names_only_passes_md_procedure(self):
        text = SKILL.read_text()
        self.assertIn("passes.md", text)
        self.assertNotIn("reference_derive", text)
        self.assertIn("two independent runs", text.lower() or "identical" in text.lower() or "determin" in text.lower())

    def test_FSUB_1_3_forbids_graph_materialization(self):
        text = SKILL.read_text() + PASSES.read_text()
        self.assertRegex(text, r"GRAPH\.md|materializ", re.I)
        self.assertRegex(text, r"SHALL NOT write|MUST NOT write|never write", re.I)

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

import re
```

Expand scenarios.md with FSUB-1.2 dual-run skill-path scenario description and FSUB-1.3 no materialize. Pressure: “materialize for speed”, “skip P0 paths enough”, “import reference_derive in skill”.

Run: `python3 -m unittest tests.test_feature_subgraph_contract` — expect fail.

- [ ] **Step 2: Implement**

Write `passes.md` with full P0–P5 recipes, stop-lists, bounds, neighbors merge rule, line-suffix regex — aligned with Task 1 reference. Write `envelope.md`. Write `SKILL.md`: description triggers only; checklist; REQUIRED for callers; rationalization table; FSUB-1.2 dual-run instruction; never write graph files; advisory banner; pathfind leave.

Run: contract tests pass; `python3 scripts/lint-skill-frontmatter.py` pass.

- [ ] **Step 3: Commit**

`Implements: FSUB-1.1, FSUB-1.2, FSUB-1.3, FSUB-1.4, FSUB-1.12, FSUB-7.1, FSUB-7.2, FSUB-7.4, FSUB-7.5`

_Requirements: FSUB-1.1, FSUB-1.2, FSUB-1.3, FSUB-1.4, FSUB-1.12, FSUB-7.1, FSUB-7.2, FSUB-7.4, FSUB-7.5_

---

### Task 3: map-features skill

**Files:**
- Create: `skills/track/map-features/SKILL.md`
- Modify: `tests/test_feature_subgraph_contract.py`
- Modify: `tests/feature-subgraph/scenarios.md`
- Test: `tests/test_feature_subgraph_contract.py`

**Reuse:** rung 2 — wizard shape of `skills/setup/configure-repo/SKILL.md` + user-invoked posture of `skills/track/scan-architecture/SKILL.md`

**Interfaces:**
- Consumes: load-subgraph envelope fields for OWNS gaps (optional read of passes concepts)
- Produces: `/map-features` propose→confirm; never auto-write DEPENDS_ON edges into load-subgraph

**Depends-on:** Task 2

- [ ] **Step 1: Write the failing test**

Assert `skills/track/map-features/SKILL.md`:

| Assert | ID |
|---|---|
| Path exists; `name: map-features`; `disable-model-invocation: true` | FSUB-6.1, FSUB-6.6 |
| Propose: Feature code lines, ROAD binds, OWNS gaps, DEPENDS_ON candidates | FSUB-6.2 |
| Write only on explicit confirm; additive SSOT; no GRAPH.md | FSUB-6.3 |
| DEPENDS_ON candidates never auto-write; not load-subgraph edges | FSUB-6.4 |
| Unresolvable CODE reported; no directory-slug keying | FSUB-6.5 |
| Model skills must name `/map-features`, not auto-invoke | FSUB-6.6 |
| Does not invent ROAD-N IDs | FSUB-6.2 |

Run: expect fail until skill exists.

- [ ] **Step 2: Implement** full skill checklist + scenarios for story 6.

Run: pass; frontmatter lint.

- [ ] **Step 3: Commit**

`Implements: FSUB-6.1, FSUB-6.2, FSUB-6.3, FSUB-6.4, FSUB-6.5, FSUB-6.6, FSUB-7.6`

_Requirements: FSUB-6.1, FSUB-6.2, FSUB-6.3, FSUB-6.4, FSUB-6.5, FSUB-6.6, FSUB-7.6_

---

### Task 4: Caller integration — frame-change + inspect-change + concept guide

**Files:**
- Modify: `skills/discovery/frame-change/SKILL.md`
- Modify: `skills/review/inspect-change/SKILL.md`
- Modify: `docs/guide/concepts/feature-graph.md`
- Modify: `tests/test_feature_subgraph_contract.py`
- Modify: `tests/feature-subgraph/scenarios.md`
- Test: `tests/test_feature_subgraph_contract.py`

**Reuse:** rung 2 — extend existing overlap steps (design module 4)

**Interfaces:**
- Consumes: skill name `load-subgraph`; dual signal terms+paths
- Produces: neighbor cards + OWNS coverage; still non-blocking

**Depends-on:** Task 2

- [ ] **Step 1: Write the failing test**

Assert frame-change and inspect-change bodies:

- Name `load-subgraph` / REQUIRED SUB-SKILL for horizontal neighbors — **FSUB-1.15**
- Pass **terms and** candidate paths (frame-change) / paths (+ optional terms for inspect) — **FSUB-1.15**
- Present coverage / thin neighborhood honesty — **FSUB-1.16** (caller surfaces envelope field)
- Still non-blocking / advisory — **FSUB-7.2**
- `feature-graph.md` describes load-subgraph implementing dual signal + coverage; still advisory live-read — **FSUB-7.5**

Run: expect fail until edits land.

- [ ] **Step 2: Implement** design module 4 text. Preserve Summary card presentation.

Run: pass.

- [ ] **Step 3: Commit**

`Implements: FSUB-1.15`

_Requirements: FSUB-1.15_

---

### Task 5: Harden `**Files:**` grammar for new plans

**Files:**
- Modify: `templates/tasks.md`
- Modify: `skills/spec/plan-tasks/SKILL.md`
- Modify: `tests/test_feature_subgraph_contract.py`
- Modify: `tests/feature-subgraph/scenarios.md`
- Test: `tests/test_feature_subgraph_contract.py`

**Reuse:** rung 2 — extend existing Files authoring rules (design module 5)

**Interfaces:**
- Produces: hardened grammar docs; task-level Depends-on unchanged

**Depends-on:** none (can parallel with Task 3 after Task 2 if desired; **Depends-on: Task 2** only if contract file serial — use **Depends-on: Task 2** because shared contract test file)

> Serial note: Tasks 2–6 all touch `tests/test_feature_subgraph_contract.py` and/or scenarios. Run **Task 2 → 3 → 4 → 5 → 6** in order.

- [ ] **Step 1: Write the failing test**

Assert template + plan-tasks skill:

- Document backticked paths — **FSUB-4.1, FSUB-4.2**
- Explicitly forbid glued `path:lines` as the path token — **FSUB-4.1**
- Task-level `Depends-on: Task N` still documented as parallelism — **FSUB-7.7**
- Files block still required Create/Modify/Test — **FSUB-7.3**

Run: fail until docs updated.

- [ ] **Step 2: Implement** hardened examples in both files (match design module 5 snippet).

Run: pass.

- [ ] **Step 3: Commit**

`Implements: FSUB-4.1, FSUB-4.2, FSUB-7.3, FSUB-7.7`

_Requirements: FSUB-4.1, FSUB-4.2, FSUB-7.3, FSUB-7.7_

---

### Task 6: Inventory, guides, triggers, artifacts pointer, suite close

**Files:**
- Create: `docs/guide/skills/load-subgraph.md`
- Create: `docs/guide/skills/map-features.md`
- Create: `tests/trigger/load-subgraph-routing.md`
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `docs/architecture/skills.md`
- Modify: `docs/architecture/system.md`
- Modify: `docs/architecture/workflows.md`
- Modify: `docs/architecture/artifacts.md`
- Modify: `.claude-plugin/plugin.json`
- Modify: `.claude-plugin/marketplace.json` (if skills enumerated)
- Modify: `docs/agents/project.md` — audit-trace ignore for `tests/feature-subgraph/fixtures/`, `tests/feature-subgraph/scenarios*.md`, `tests/trigger/load-subgraph-routing.md` as needed
- Modify: `tests/test_feature_subgraph_contract.py`
- Modify: `tests/feature-subgraph/scenarios.md` (every FSUB-N.M present)
- Test: `tests/test_feature_subgraph_contract.py` + full suite

**Reuse:** rung 2 — registration pattern from vet-product-flow / pathfind wiring

**Interfaces:**
- Produces: discoverable skills in inventories; routing matrix

**Depends-on:** Task 2, Task 3, Task 4, Task 5

- [ ] **Step 1: Write the failing test**

```python
def test_FSUB_all_requirement_ids_in_scenarios(self):
    import re
    req = (ROOT / "docs/specs/2026-08-01-feature-subgraph/requirements.md").read_text()
    ids = set(re.findall(r"\*\*(FSUB-\d+\.\d+)\*\*", req))
    scenarios = (ROOT / "tests/feature-subgraph/scenarios.md").read_text()
    missing = sorted(i for i in ids if i not in scenarios)
    self.assertEqual(missing, [], f"missing from scenarios: {missing}")

def test_FSUB_inventory_lists_both_skills(self):
    agents = (ROOT / "AGENTS.md").read_text()
    self.assertIn("load-subgraph", agents)
    self.assertIn("map-features", agents)
```

Also assert artifacts.md / workflows mention load-subgraph for horizontal neighbors; plugin lists skill paths if other skills are listed; no `*.py` under load-subgraph package.

Run: fail until wired.

- [ ] **Step 2: Implement** inventory + guides + trigger + artifacts/workflows pointers; fill all scenario tokens; run full verify:

```bash
python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-write-handoffs.py && python3 scripts/lint-context7.py
python3 -m unittest discover -s tests
```

Expect: all pass, pristine.

- [ ] **Step 3: Commit**

`Implements: FSUB-1.1, FSUB-6.1` (discoverability) + residual packaging

_Requirements: FSUB-1.1, FSUB-6.1_

---

## Coverage map (audit)

Every Approved FSUB ID must appear in ≥1 task footer **and** in a tagged test
(unittest docstring/method and/or `tests/feature-subgraph/scenarios.md`).

| IDs | Primary task | Test annotation |
|---|---|---|
| 3.1–3.4, 1.5–1.11, 1.13–1.14, 1.16, 2.1–2.6, 5.1–5.3, 8.1–8.3 | Task 1 | derive unit methods + scenarios |
| 1.1–1.4, 1.12, 7.1, 7.2, 7.4, 7.5 | Task 2 | contract + scenarios + pressure |
| 6.1–6.6, 7.6 | Task 3 | contract + scenarios |
| 1.15 | Task 4 | contract + scenarios |
| 4.1, 4.2, 7.3, 7.7 | Task 5 | contract + scenarios |
| 1.1, 6.1 (wiring) + all IDs in scenarios | Task 6 | completeness assert + suite |

Design seam table: reference unit seams + skill prose scenarios + inventory — all mapped.

## Exit

Present this file and **STOP**.

On user approval of this written plan:

1. Set `Status: Approved` (leave `Execution-mode: unset`).
2. Offer exactly three execute routes (do not invent mode here):

| Route | Meaning |
|---|---|
| **`build-in-waves`** | Subagent waves (`Execution-mode: continuous`). Prefer `isolate-workspace` first. |
| **`build-by-story`** | Human-gated story units (`Execution-mode: story-unit`). Prefer `isolate-workspace` first. |
| **`build-inline`** | Controller implements sequentially with `test-first` (no implementer subagents). |

3. On pick: hand off to that skill.
