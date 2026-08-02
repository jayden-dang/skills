# Tasks: Feature-subgraph retrieval upgrade (Wave A)

> **For agentic workers:** after plan approval, pick one execute skill —
> `build-in-waves` (subagent waves), `build-by-story` (human-gated story review
> units), or `build-inline` (controller implements, no implementer subagents).
> The chosen skill writes `Execution-mode:`. Steps use checkbox (`- [ ]`) syntax
> for tracking.

Feature code: FSUBR
Status: Implemented
Date: 2026-08-02
Execution-mode: continuous
Requirements: ./requirements.md
Design: ./design.md

**Goal:** Ship FSUBR Wave A: tightened P1 OWNS, schema 1.1 path/term evidence,
query-local `cluster`, derivation snapshot, caller prose, and guide inventory —
all on the existing `load-subgraph` surface (Approach A).

**Architecture:** In-place delta on `passes.md` / `envelope.md` / pack-only
`reference_derive.py` with a two-stage in-memory `DerivationSnapshot` (Stage A
core, Stage B cluster OOS). Queries are pure functions of the snapshot (zero file
IO). Skill prose wires C1′ callers and grounded claims. No on-disk cache, no
GRAPH.md, no P6.

**Tech Stack:** Markdown skills; Python 3 `unittest` under `tests/`; fixtures under
`tests/feature-subgraph/fixtures/`. No new runtime dependencies.

## Global Constraints

**verify commands — run in this order; all must pass before any completion claim**
(from `docs/agents/project.md`):

| Check | Command |
|---|---|
| Lint | `python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-handoffs.py && python3 scripts/lint-context7.py` |
| Unit tests | `python3 -m unittest discover -s tests` |

Single test file: `python3 -m unittest tests.<module>`  
(e.g. `python3 -m unittest tests.test_feature_subgraph_derive`)

**Pack fixture IDs:** unit/scenario tests for this skill set may embed greppable
`FSUBR-N.M` tokens in method docstrings or scenario markdown (DOSP-2.5 /
`docs/agents/project.md` pack fixture note). Do not teach consumer apps to embed
IDs in application tests.

**Engineering rules** (from `docs/product/guidelines.md`):

- Skill bodies: imperative voice; hard gates in dedicated blocks; rationalization tables in `| Thought | Reality |` form.
- SKILL.md under 500 lines (prefer under 300).
- No production app code in this repository — content is skills, templates, hooks, and docs.
- Deterministic checks via fixed `grep`/`git`/set ops — no freeform judgment when a set-difference will do.
- Comments default zero; no requirement IDs in application source/commits (pack test fixtures may cite IDs).
- Cross-skill references use `REQUIRED SUB-SKILL:` prose, never `@`-links.
- Iron Law gates are not weakened by ceremony tier or convenience.

**Architecture invariants** (from `docs/architecture/INDEX.md`):

- **ARCH-1** Audit Trace and other vertical checks MUST be exact `grep`/`git`/file-read passes with fixed extraction rules and set differences — never an LLM judgment of whether a test "really" covers an ID.
- **ARCH-2** Optional project layers and config sections MUST no-op when absent.
- **ARCH-3** Consumer-repo adoption MUST require only the skills and markdown config — never mandate Python under skills for the methodology; no Neo4j/Tree-sitter mandate.
- **ARCH-4** Requirement IDs and ARCH-N are immutable once defined.
- **ARCH-5** Model-invoked skills must never auto-invoke user-invoked skills.

**FSUBR design freezes (implement exactly):**

- `CLUSTER_K = 1`, `CLUSTER_MEMBERS_MAX = 8`, `PATH_EVIDENCE_MAX = 5`, `TERM_EVIDENCE_MAX = 5`
- `OOS_ITEM_MAX = 6`, `OOS_TEXT_CEILING = 1200` display code points
- `schema_version = "1.1"`, `recipe_id = "fsubr-1.1"`
- Note kinds: `p1_block_skipped`, `p1_file_unreadable`, `cluster_focus_invalid`
- No silent note count cap (dedupe kind+code+detail only)
- Classifier and snapshot rules as in `design.md` Architecture §§0–1

**Hardened Files grammar** for this plan: paths in backticks; no `path:lines` glued suffixes.

## File Structure

| Path | Responsibility |
|---|---|
| `skills/execution/load-subgraph/references/passes.md` | P1 multi-block, classifier, snapshot stages, neighbors 1.1, cluster, notes |
| `skills/execution/load-subgraph/references/envelope.md` | schema 1.1 neighbor + cluster payload shapes |
| `skills/execution/load-subgraph/SKILL.md` | Procedure: snapshot then query; no GRAPH; advisory |
| `tests/feature-subgraph/reference_derive.py` | Pack oracle: extract_owns, snapshot, queries, read_ledger |
| `tests/feature-subgraph/fixtures/p1-classifier/` | Pos/neg decision-table fixtures |
| `tests/feature-subgraph/fixtures/p1-malformed-block/` | Last-block unclosed fence |
| `tests/feature-subgraph/fixtures/p1-unreadable/` | Invalid UTF-8 or FS-fail adapter |
| `tests/feature-subgraph/fixtures/p1-later-files/` | Later-task path retention |
| `tests/feature-subgraph/fixtures/p1-fence-heading/` | `###` inside fence not boundary |
| `tests/test_feature_subgraph_derive.py` | Unit tests for oracle (extend) |
| `tests/test_feature_subgraph_contract.py` | Source/scenario contracts (extend) |
| `tests/feature-subgraph/scenarios.md` | Scenario coverage tokens |
| `skills/discovery/frame-change/SKILL.md` | neighbors 1.1 + grounded claims |
| `skills/review/inspect-change/SKILL.md` | same |
| `skills/discovery/clarify-decisions/SKILL.md` | nested/standalone package rules |
| `skills/spec/design-solution/SKILL.md` | Step 1 retrieval |
| `skills/spec/plan-tasks/SKILL.md` | post file-map blast_radius + cluster |
| `skills/execution/root-cause/SKILL.md` | post-Phase-2 retrieval; never RED |
| `docs/guide/concepts/feature-graph.md` | Horizontal doctrine + cluster |
| `docs/guide/START-HERE.md` | Entry map consistency |
| `docs/guide/skills/README.md` | Skill list consistency |
| `docs/guide/skills/load-subgraph.md` | if present — cluster docs |
| `AGENTS.md` / `docs/architecture/skills.md` / `workflows.md` | inventory if they name horizontal steps |

---

### Task 1: P1 multi-block extract + classifier + reliability notes

**Files:**
- Modify: `tests/feature-subgraph/reference_derive.py`
- Modify: `skills/execution/load-subgraph/references/passes.md`
- Create: `tests/feature-subgraph/fixtures/p1-classifier/`
- Create: `tests/feature-subgraph/fixtures/p1-malformed-block/`
- Create: `tests/feature-subgraph/fixtures/p1-unreadable/`
- Create: `tests/feature-subgraph/fixtures/p1-later-files/`
- Create: `tests/feature-subgraph/fixtures/p1-fence-heading/`
- Modify: `tests/test_feature_subgraph_derive.py`
- Modify: `tests/feature-subgraph/scenarios.md`

**Reuse:** rung 2 — `extract_owns_from_tasks_text` and denoise/stop-lists in `reference_derive.py` / `passes.md` Pass P1

**Interfaces:**
- Consumes: existing denoise, line-suffix strip, registry helpers
- Produces: `extract_owns_from_tasks_text(text) -> {paths: set[str], notes: list[dict]}` with kinds `p1_block_skipped`; multi-block fence-aware stop; classifier per design decision table

**Depends-on:** none

- [ ] **Step 1: Failing tests — classifier decision table + multi-block + malformed last-block + unreadable**

Add tests in `tests/test_feature_subgraph_derive.py` with greppable docstrings containing the IDs below. Cover every design decision-table row (pos/neg), later-task path retention, fence-internal `###` not stopping Files, malformed **last** unclosed fence keeping prior sibling paths, missing `tasks.md` empty without unreadable note, and unreadable via invalid UTF-8 fixture or injected FS error (not missing path).

Run: `python3 -m unittest tests.test_feature_subgraph_derive -v`  
Expect: failures on new assertions (old first-block behavior / wrong accepts).

- [ ] **Step 2: Implement extract + passes.md Pass P1**

Implement design Architecture §1 exactly: multi-block, fence-aware stop, reject-unsafe-first, provenance, broad-ext / known-root / labeled rules, `p1_block_skipped` / missing vs unreadable. Sync `passes.md` recipes to match (agent SSOT).

Run: `python3 -m unittest tests.test_feature_subgraph_derive -v` — expect pass.

- [ ] **Step 3: Commit**

`git commit` with domain subject describing P1 OWNS tightening (no requirement IDs in commit message per DOSP).

_Requirements: FSUBR-2.1, FSUBR-2.2, FSUBR-2.3, FSUBR-2.4, FSUBR-2.5, FSUBR-2.6, FSUBR-2.7, FSUBR-2.8, FSUBR-2.9, FSUBR-10.3, FSUBR-10.4_

---

### Task 2: DerivationSnapshot two-stage + read_ledger

**Files:**
- Modify: `tests/feature-subgraph/reference_derive.py`
- Modify: `skills/execution/load-subgraph/references/passes.md`
- Modify: `skills/execution/load-subgraph/SKILL.md`
- Modify: `tests/test_feature_subgraph_derive.py`
- Modify: `tests/feature-subgraph/scenarios.md`

**Reuse:** rung 7/2 — new snapshot structure inside oracle; extends FSUB one-pass pattern

**Interfaces:**
- Consumes: `extract_owns_from_tasks_text` from Task 1; registry load
- Produces: `build_snapshot(repo_root, query) -> DerivationSnapshot` with `source_texts`, `source_bytes`, `owns`, `notes`, `fingerprints` (incl. optional-layer presence), `read_ledger`; Stage B only for cluster after members known; queries must not open files

**Depends-on:** Task 1

- [ ] **Step 1: Failing tests — read_ledger uniqueness + pure query IO**

Tests: after `build_snapshot` + `neighbors`/`cluster`, each path appears at most once in `read_ledger`; running a query with an IO-disabled adapter (raise on any read) succeeds when snapshot is prebuilt; missing tasks.md does not emit `p1_file_unreadable`.

Run: `python3 -m unittest tests.test_feature_subgraph_derive -v` — expect fail until snapshot exists.

- [ ] **Step 2: Implement snapshot stages + wire `run()`**

Implement design §0. Document Stage A/B in `passes.md` and SKILL.md procedure. Fingerprints SHA-256 of bytes; absent optional layers recorded as `present: false`.

Run: same unittest — expect pass.

- [ ] **Step 3: Commit**

Domain-subject commit for derivation snapshot / read-once.

_Requirements: FSUBR-10.1_

---

### Task 3: Neighbors envelope schema 1.1

**Files:**
- Modify: `tests/feature-subgraph/reference_derive.py`
- Modify: `skills/execution/load-subgraph/references/envelope.md`
- Modify: `skills/execution/load-subgraph/references/passes.md`
- Modify: `tests/test_feature_subgraph_derive.py`
- Modify: `tests/feature-subgraph/scenarios.md`

**Reuse:** rung 2 — existing neighbors merge / ranking (`shared_paths` int, via)

**Interfaces:**
- Consumes: snapshot OWNS + source texts
- Produces: neighbors payload with `schema_version: "1.1"`, `path_evidence`, `term_evidence`, `via_traces` (`path_overlap` | `term_match` always present), `notes`; path items lex asc; term casefold dedupe; no provenance bag / depends_on

**Depends-on:** Task 2

- [ ] **Step 1: Failing tests — schema 1.1 fields**

Assert integer `shared_paths` still ranks; path_evidence max 5 + truncated; term_evidence rules; via_traces kinds only path_overlap/term_match; notes include P1 notes when present.

Run: `python3 -m unittest tests.test_feature_subgraph_derive -v` — expect fail.

- [ ] **Step 2: Implement neighbors 1.1 in oracle + envelope.md + passes.md**

Run: unittest — expect pass.

- [ ] **Step 3: Commit**

Domain-subject commit for path/term-grounded neighbor envelope.

_Requirements: FSUBR-1.1, FSUBR-1.2, FSUBR-1.3, FSUBR-1.4, FSUBR-1.5, FSUBR-1.6, FSUBR-1.7, FSUBR-1.8, FSUBR-1.9, FSUBR-1.10, FSUBR-1.11, FSUBR-1.12, FSUBR-9.3_

---

### Task 4: cluster query

**Files:**
- Modify: `tests/feature-subgraph/reference_derive.py`
- Modify: `skills/execution/load-subgraph/references/envelope.md`
- Modify: `skills/execution/load-subgraph/references/passes.md`
- Modify: `tests/test_feature_subgraph_derive.py`
- Modify: `tests/feature-subgraph/scenarios.md`

**Reuse:** rung 2 — P2 weights from snapshot OWNS; new query pure on snapshot

**Interfaces:**
- Consumes: snapshot Stage A OWNS; Stage B loads member requirements for OOS only via snapshot build
- Produces: `cluster(focus)` payload: focus first; eligible iff weight ≥ 1; `CLUSTER_MEMBERS_MAX=8`; `members_truncated = (1+eligible_non_focus_count) > 8`; non-focus `path_evidence`; OOS union with normalize key / display text / sources / caps; reject 0/many focus

**Depends-on:** Task 2, Task 3

- [ ] **Step 1: Failing tests — focus reject, one-path eligibility, high-degree truncation, OOS**

Include post-P1 goldens: single shared path eligible; high-degree truncated; OOS ceiling on display text.

Run: unittest — expect fail.

- [ ] **Step 2: Implement cluster + Stage B OOS load in snapshot path**

Queries remain zero-IO after snapshot complete. Document in passes.md.

Run: unittest — expect pass.

- [ ] **Step 3: Commit**

Domain-subject commit for query-local cluster digest.

_Requirements: FSUBR-3.1, FSUBR-3.2, FSUBR-3.3, FSUBR-3.4, FSUBR-3.5, FSUBR-3.6, FSUBR-3.7, FSUBR-3.8, FSUBR-3.9, FSUBR-3.10, FSUBR-3.11, FSUBR-3.12, FSUBR-3.13, FSUBR-3.14, FSUBR-3.15_

---

### Task 5: Caller skills + grounded claims + package validity prose

**Files:**
- Modify: `skills/discovery/frame-change/SKILL.md`
- Modify: `skills/review/inspect-change/SKILL.md`
- Modify: `skills/discovery/clarify-decisions/SKILL.md`
- Modify: `skills/spec/design-solution/SKILL.md`
- Modify: `skills/spec/plan-tasks/SKILL.md`
- Modify: `skills/execution/root-cause/SKILL.md`
- Modify: `skills/execution/load-subgraph/SKILL.md`
- Modify: `tests/test_feature_subgraph_contract.py`
- Modify: `tests/feature-subgraph/scenarios.md`
- Modify: `tests/feature-subgraph/scenarios-pressure.md` (if present)

**Reuse:** rung 2 — existing REQUIRED SUB-SKILL load-subgraph call sites; extend

**Interfaces:**
- Consumes: envelope 1.1 + cluster query names
- Produces: skill prose for C1′ moments; grounded-claim protocol; package fingerprint validity (SHA-256 + presence); no-op/thin/no invent; no build callers; no disk cache

**Depends-on:** Task 3, Task 4

- [ ] **Step 1: Failing contract/scenario tests**

Assert skill bodies name: nested+standalone clarify; design Step 1; plan-tasks blast_radius **and** cluster(feature CODE); root-cause after Phase 2 only; grounded claims (CODE+edge+path/term); FSUBR-4.2 coverage statement; package rederive when fingerprints differ; ignore unknown via_traces kinds.

Run: `python3 -m unittest tests.test_feature_subgraph_contract -v` (and any scenario harness the pack uses) — expect fail until prose lands.

- [ ] **Step 2: Implement skill prose**

Edit each skill per design caller table. Keep rationalization tables. Do not exceed line budgets without splitting.

Run: contract tests — expect pass. Lint: `python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-handoffs.py`.

- [ ] **Step 3: Commit**

Domain-subject commit for retrieval callers and grounded claims.

_Requirements: FSUBR-4.1, FSUBR-4.2, FSUBR-4.3, FSUBR-4.4, FSUBR-5.1, FSUBR-5.2, FSUBR-5.3, FSUBR-6.1, FSUBR-7.1, FSUBR-7.2, FSUBR-8.1, FSUBR-8.2, FSUBR-9.8, FSUBR-9.11, FSUBR-9.12, FSUBR-9.13, FSUBR-9.14, FSUBR-9.15_

---

### Task 6: Guide, inventory, carry-forward guards

**Files:**
- Modify: `docs/guide/concepts/feature-graph.md`
- Modify: `docs/guide/START-HERE.md`
- Modify: `docs/guide/skills/README.md`
- Modify: `docs/guide/skills/load-subgraph.md` (create or update if missing)
- Modify: `AGENTS.md` (only if horizontal step inventory needs cluster/callers)
- Modify: `docs/architecture/skills.md` and/or `docs/architecture/workflows.md` (if they list horizontal neighbors)
- Modify: `tests/test_feature_subgraph_contract.py`
- Modify: `tests/feature-subgraph/scenarios.md`

**Reuse:** rung 2 — extend guide + guard scenarios

**Interfaces:**
- Consumes: shipped query/caller names from Tasks 3–5
- Produces: guide text for cluster + callers; contracts: no GRAPH.md write, no depends_on field, no `*.py` under skill dir, pathfind separate, audit-trace E-codes unchanged, P3–P5 no-op when layers absent

**Depends-on:** Task 5

- [ ] **Step 1: Failing source contracts**

Assert guides mention `cluster` and expanded callers; assert forbidden GRAPH/depends_on/skill-py patterns still enforced; ARCH-2 no-op fixtures still pass.

Run: contract unittest — expect fail until docs updated.

- [ ] **Step 2: Update docs + contracts**

Run: full `python3 -m unittest discover -s tests` and lints — expect pass.

- [ ] **Step 3: Commit**

Domain-subject commit for guide/inventory and guard contracts.

_Requirements: FSUBR-9.1, FSUBR-9.2, FSUBR-9.4, FSUBR-9.5, FSUBR-9.6, FSUBR-9.7, FSUBR-9.9, FSUBR-9.10, FSUBR-10.2_

---

## Coverage matrix (plan self-check)

| IDs | Task |
|---|---|
| 2.1–2.9, 10.3, 10.4 | Task 1 |
| 10.1 | Task 2 |
| 1.1–1.12, 9.3 | Task 3 |
| 3.1–3.15 | Task 4 |
| 4.1–4.4, 5.1–5.3, 6.1, 7.1–7.2, 8.1–8.2, 9.8, 9.11–9.15 | Task 5 |
| 9.1, 9.2, 9.4–9.7, 9.9, 9.10, 10.2 | Task 6 |

**67 IDs** each appear in exactly one task footer; each has a tagged test/scenario step in that task.

## Independent plan review notes

- Symbols: `extract_owns_from_tasks_text` exists at `tests/feature-subgraph/reference_derive.py` (~L142); extend not invent alternate name.
- No new Python under `skills/execution/load-subgraph/`.
- Verify commands and ARCH lines copied from project config / architecture INDEX.
- Plan author self-check: no TBD placeholders; hardened Files paths.
