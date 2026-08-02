# Requirements: Feature-subgraph retrieval upgrade (Wave A)

Feature code: FSUBR
Status: Implemented
Date: 2026-08-02
Approved: 2026-08-02 (user)
Implemented: 2026-08-02 (build-in-waves on main)

Upgrades ask-time feature-subgraph **retrieval quality** on top of Implemented
**FSUB** (`Reuse: FSUB`): path- and term-grounded neighbor evidence, tightened
P1 OWNS extraction, a query-local `cluster` digest over **exactly one** focus CODE, grounded-claim
protocol, and conditional callers beyond frame-change / inspect-change.

**Baseline.** FSUB remains the Implemented derivation product
(`docs/specs/2026-08-01-feature-subgraph/`). FSUBR defines **only the Wave A
delta**. Path OVERLAP between FSUB and FSUBR is **intentional evidence**, not
ownership noise. Agents execute recipes in
`skills/execution/load-subgraph/references/passes.md` (and envelope); the
test-side reference under `tests/feature-subgraph/` locks recipe math.

**Implementation packaging (frame-locked):** Approach **A** — in-place delta on
the existing `load-subgraph` surface (not a parallel v2 skill). **Ceremony tier:
2.**

**Namespaces.** No new ID grammar. Node kinds remain those FSUB allows. FSUBR
does not mint requirement IDs for FSUB’s original criteria; it cites FSUB
behavior only via guards and Reuse.

**Evidence that shaped the frame.** Live registry diagnosis showed P1
first-block-only parse plus Files-body bleed into Step/unittest prose producing
code-shaped OWNS tokens and a 10/11 mega-component at low k. Clean-graph spikes
favored query-local clusters over global partitions. Delivery items 5–6 (P6
DEPENDS_ON, work-graph adapters) are committed follow-ons outside this feature.

---

## 1. Path- and term-grounded neighbor envelope

**Story:** As an agent loading feature neighbors, I want concrete path and term
evidence plus typed traces on each neighbor, so that reuse and overlap claims
are grounded without pasting whole specs.

- **FSUBR-1.1** WHEN `load-subgraph` returns a neighbors (or equivalent neighbor-list) payload THE SYSTEM SHALL set `schema_version` to `"1.1"`.
- **FSUBR-1.2** WHEN a neighbor entry is emitted THE SYSTEM SHALL CONTINUE TO include `shared_paths` as the **integer** ranking field equal to the cardinality of the shared meaningful path set (FSUB-2.3 ranking semantics).
- **FSUBR-1.3** WHEN a neighbor entry is emitted THE SYSTEM SHALL CONTINUE TO include `via` as exactly one of `path`, `term`, or `both`.
- **FSUBR-1.4** WHEN a neighbor entry is emitted THE SYSTEM SHALL include `path_evidence` with `items` (repo-relative path strings from the shared meaningful set, deterministically ordered) of length at most **5**.
- **FSUBR-1.5** WHEN a neighbor entry is emitted and more shared meaningful paths exist than fit in `path_evidence.items` THE SYSTEM SHALL set `path_evidence.truncated` to true; otherwise THE SYSTEM SHALL set it to false.
- **FSUBR-1.6** WHEN a neighbor entry is emitted THE SYSTEM SHALL include `term_evidence` with `items` of length at most **5** (matched seed terms for that feature, deterministically ordered).
- **FSUBR-1.7** WHEN a neighbor entry is emitted and more matching seed terms exist than fit in `term_evidence.items` THE SYSTEM SHALL set `term_evidence.truncated` to true; otherwise THE SYSTEM SHALL set it to false.
- **FSUBR-1.8** WHEN a neighbor entry is emitted THE SYSTEM SHALL include plural typed `via_traces` that keep path-overlap evidence and term-match evidence as **separate** trace objects.
- **FSUBR-1.9** WHEN producing Wave A `via_traces` THE SYSTEM SHALL emit only the kinds `path_overlap` and `term_match`.
- **FSUBR-1.10** WHEN skill prose describes consumers of `via_traces` THE SYSTEM SHALL require callers to **ignore unknown future trace kinds** while continuing to consume core fields (`schema_version`, `shared_paths`, `via`, `path_evidence`, `term_evidence`, `owns_coverage`, advisory banner).
- **FSUBR-1.11** WHEN emitting the envelope THE SYSTEM SHALL NOT include an untyped `provenance` or `edge_extensions` bag.
- **FSUBR-1.12** WHEN emitting Wave A traces THE SYSTEM SHALL NOT define P6 DEPENDS_ON or work-graph adapter trace kinds.

## 2. Tighten P1 OWNS extraction

**Story:** As a developer relying on path evidence and clusters, I want OWNS
tokens taken only from real Files sections across all tasks, so that code prose
and missed later tasks no longer invent false overlaps.

- **FSUBR-2.1** WHEN pass P1 extracts OWNS for a feature THE SYSTEM SHALL parse **every** `**Files:**` / `Files:` block in that feature’s `tasks.md`, not only the first block.
- **FSUBR-2.2** WHEN pass P1 determines the end of a Files section THE SYSTEM SHALL end the section at the **next section or task** boundary, recognizing at least Reuse, Interfaces, Depends-on, and Steps as section boundaries (exact header syntax may be extended in design via fixtures).
- **FSUBR-2.3** WHEN pass P1 extracts path-like tokens from prose THE SYSTEM SHALL do so **only within** the Files section bounds of FSUBR-2.2.
- **FSUBR-2.4** WHEN pass P1 considers a candidate token that is **code/prose-shaped** under the deterministic rules frozen in design/`passes.md` THE SYSTEM SHALL **reject** that token from OWNS.
- **FSUBR-2.5** WHEN pass P1 considers a candidate token that is a valid root-level filename, a **dotfile**, an extension-bearing path, or a slash-bearing repo-relative path and that token passes denoise THE SYSTEM SHALL **accept** it into OWNS (subject to other P1 rules).
- **FSUBR-2.6** WHEN pass P1 rules for accept/reject are verified THE SYSTEM SHALL include fixtures with both **positive** accepts and **negative** rejects for the FSUBR-2.4 / FSUBR-2.5 boundary.
- **FSUBR-2.7** (guard) WHEN pass P1 runs THE SYSTEM SHALL CONTINUE TO accept FSUB legacy Files forms (bulleted Create/Modify/Move/Test, inline prose **inside** Files, optional backticks).
- **FSUBR-2.8** (guard) WHEN a path token carries a glued line/range suffix THE SYSTEM SHALL CONTINUE TO strip that suffix per FSUB-3.2.
- **FSUBR-2.9** WHEN pass P1 is verified THE SYSTEM SHALL include a fixture that retains real paths from **later** task Files blocks that a first-block-only parse would miss.

## 3. Query-local cluster digest

**Story:** As an agent framing or planning work around a focus feature, I want a
bounded local cluster of overlapping features with path evidence and Out-of-Scope
union, so that I see the local surface without a global community partition.

Callers that start from terms or paths SHALL resolve those seeds to feature codes
**before** invoking `cluster` and SHALL supply one focus CODE. The `cluster` query
itself does not accept an ambiguous multi-CODE focus set.

- **FSUBR-3.1** WHEN `cluster` is invoked THE SYSTEM SHALL require exactly one focus CODE and reject zero or multiple focus CODEs.
- **FSUBR-3.2** THE SYSTEM SHALL NOT name or ship a global `communities()` registry partition in FSUBR.
- **FSUBR-3.3** WHEN `cluster` builds the eligible non-focus set after P1 tightening (story 2) THE SYSTEM SHALL treat a non-focus feature as **eligible if and only if** its meaningful OVERLAPS weight against the focus is **≥ fixed integer `k`** (the threshold of FSUBR-3.4); deterministic ranking and the member cap then determine which eligible members are **returned**.
- **FSUBR-3.4** WHEN `cluster` applies the OVERLAPS weight threshold `k` THE SYSTEM SHALL use a **fixed integer** frozen in design/`passes.md`/fixtures (chosen from P1 golden fixtures) and SHALL NOT adapt that threshold at runtime. (`k` is at least 1 so eligibility implies positive weight.)
- **FSUBR-3.5** WHEN `cluster` returns members THE SYSTEM SHALL include the **focus** in the member list.
- **FSUBR-3.6** WHEN `cluster` returns members THE SYSTEM SHALL rank non-focus members with a deterministic sort key and tie-break frozen in design/`passes.md` (focus placement in the list is fixed by design, e.g. first).
- **FSUBR-3.7** WHEN `cluster` returns members THE SYSTEM SHALL apply a member cap that **includes the focus** and **never exceeds `NEIGHBORS_MAX`**.
- **FSUBR-3.8** WHEN `1 + (count of eligible non-focus members) > member cap` THE SYSTEM SHALL set `members_truncated` to true; otherwise THE SYSTEM SHALL set it to false. (The cap includes the focus, so truncation is true when focus plus eligible non-focus count exceeds the cap.)
- **FSUBR-3.9** WHEN `cluster` returns a non-focus member THE SYSTEM SHALL attach a bounded, deterministically ordered **path-evidence list** of shared meaningful paths with the focus (same cap and `truncated` honesty rules as Story 1 `path_evidence`: at most 5 items; `truncated` true when more shared meaningful paths exist than listed).
- **FSUBR-3.10** WHEN `cluster` returns a result THE SYSTEM SHALL report **`owns_coverage`** with the same meaning as FSUB-1.16 (count of registered features with non-empty OWNS over registered total).
- **FSUBR-3.11** WHEN `cluster` builds the Out-of-Scope union THE SYSTEM SHALL collect Out-of-Scope items from member features and **dedupe by deterministic normalized text**.
- **FSUBR-3.12** WHEN `cluster` emits a deduped Out-of-Scope item THE SYSTEM SHALL retain **source-CODE attribution** for that item.
- **FSUBR-3.13** WHEN `cluster` emits the Out-of-Scope union THE SYSTEM SHALL apply both a fixed **item-count cap** and a fixed **total text-size ceiling** (integers frozen in design/`passes.md`/fixtures).
- **FSUBR-3.14** WHEN either OOS cap drops content THE SYSTEM SHALL set `oos_truncated` to true; otherwise THE SYSTEM SHALL set it to false.
- **FSUBR-3.15** WHEN deduping Out-of-Scope items THE SYSTEM SHALL NOT use LLM similarity.

## 4. Grounded horizontal claims

**Story:** As a reviewer reading agent conclusions about overlap or reuse, I want
every such claim tied to CODE, edge kind, and path or term evidence, so that
thin neighborhoods are not presented as complete.

- **FSUBR-4.1** WHEN an agent states an overlap, reuse-miss, or Out-of-Scope / “already declined” conclusion drawn from `load-subgraph` THE SYSTEM SHALL require that claim to cite at least one **feature CODE**, an **edge kind** (or trace kind), and a **path or term** from the envelope or cluster card.
- **FSUBR-4.2** WHEN an agent is about to conclude that no relevant feature exists and `owns_coverage.with_owns < owns_coverage.registered` THE SYSTEM SHALL require the agent to state the **exact** `owns_coverage` values (`with_owns`, `registered`, and ratio or equivalent) **before** that absence conclusion.
- **FSUBR-4.3** WHEN an agent is about to conclude that no relevant feature exists and the neighbor or cluster result is empty THE SYSTEM SHALL require the agent to state that emptiness **before** that absence conclusion.
- **FSUBR-4.4** WHEN retrieval results inform design or planning THE SYSTEM SHALL treat them as **advisory input only** and SHALL NOT invent `Reuse:`, `Respects:`, `**Files:**` paths, or root-cause hypotheses solely from the envelope.

## 5. Retrieval for clarify-decisions

**Story:** As an agent running clarify-decisions on feature work, I want the
retrieval package reused or loaded once at the right time, so that interview
cards start from grounded neighbors without needless re-derives.

- **FSUBR-5.1** WHEN `clarify-decisions` runs nested under a parent that already produced a retrieval package, and that package remains valid under FSUBR-9.14, THE SYSTEM SHALL **reuse** that package; otherwise THE SYSTEM SHALL rederive.
- **FSUBR-5.2** WHEN `clarify-decisions` runs **standalone** for feature work and no parent package exists THE SYSTEM SHALL load retrieval **once** before the first interview card.
- **FSUBR-5.3** WHEN `clarify-decisions` is in progress and any derivation source input changes, or any material scope, terms, or paths change, THE SYSTEM SHALL rederive the retrieval package.

## 6. Retrieval for design-solution

**Story:** As an agent designing a solution, I want a fresh retrieval after the
scan digest and before the reuse ladder, so that Reuse and Respects suggestions
start from the current feature surface.

- **FSUBR-6.1** WHEN `design-solution` reaches Step 1 after the scan digest and before the reuse ladder THE SYSTEM SHALL run a **fresh** retrieval seeded with the feature CODE, requirement terms, and candidate paths.

## 7. Retrieval for plan-tasks

**Story:** As an agent writing the implementation plan, I want blast-radius and
cluster context after the file map and before task bodies, so that planned Files
reflect neighboring ownership.

- **FSUBR-7.1** WHEN `plan-tasks` has completed its Step 2 file map and before writing task bodies THE SYSTEM SHALL run retrieval **once** over the complete candidate path set for blast-radius context.
- **FSUBR-7.2** WHEN `plan-tasks` has completed its Step 2 file map and before writing task bodies THE SYSTEM SHALL invoke `cluster` using the feature CODE as the single focus.

## 8. Retrieval for root-cause

**Story:** As an agent investigating a failure, I want feature-ownership context
only after the problem is reproduced and minimized, so that retrieval never
replaces the red-capable loop.

- **FSUBR-8.1** WHEN `root-cause` has completed Phase 2 (reproduce/minimize) and produced a path or stable term, and before Phase 3 hypotheses THE SYSTEM SHALL run retrieval for context.
- **FSUBR-8.2** (guard) WHEN `root-cause` runs Phases 1–2 THE SYSTEM SHALL NOT use retrieval as the red-capable feedback loop.

## 9. Guard existing methodology and FSUB baseline

**Story:** As a maintainer of the skill set, I want FSUBR to extend retrieval
without reintroducing graph SSOT, P6 edges, pathfind merge, hard gates, or
silent inventory drift.

### Files expected to change (Wave A)

| Path / area | Behavior at risk | Guard / note |
|---|---|---|
| `skills/execution/load-subgraph/references/passes.md` | P0–P5 recipes, P1 OWNS, queries | FSUBR-9.1–9.3; stories 1–3 |
| `skills/execution/load-subgraph/references/envelope.md` | Envelope field contract | stories 1, 3 |
| `skills/execution/load-subgraph/SKILL.md` | Skill procedure / callers | FSUBR-9.1–9.3 |
| `tests/feature-subgraph/**`, `tests/test_feature_subgraph_*.py` | Recipe oracle & fixtures | FSUBR-9.4 |
| `skills/discovery/frame-change/SKILL.md` | Neighbor load + presentation | FSUBR-9.8; story 4 |
| `skills/review/inspect-change/SKILL.md` | Neighbor load + Spec brief | FSUBR-9.8; story 4 |
| `skills/discovery/clarify-decisions/SKILL.md` | Interview retrieval moments | story 5 |
| `skills/spec/design-solution/SKILL.md` | Step 1 retrieval | story 6 |
| `skills/spec/plan-tasks/SKILL.md` | Post file-map retrieval | story 7 |
| `skills/execution/root-cause/SKILL.md` | Post-Phase-2 retrieval | story 8 |
| `docs/guide/concepts/feature-graph.md` | Horizontal doctrine text | FSUBR-9.3 |
| `docs/guide/START-HERE.md` | Entry map / chain names | FSUBR-9.9 |
| `docs/guide/skills/README.md` | Skill inventory listing | FSUBR-9.9 |
| AGENTS / `docs/architecture/skills.md` / `workflows.md` (if inventory lists callers) | Packaging discoverability | FSUBR-9.10 — **no behavior to guard** beyond listing accuracy |

### Regression / no-edit surfaces (must keep working; not primary edit targets)

| Path / area | Guard |
|---|---|
| `skills/execution/audit-trace/**` | FSUBR-9.5 |
| `skills/discovery/pathfind/**` | FSUBR-9.6 |
| `docs/specs/2026-08-01-feature-subgraph/**` (FSUB triad) | FSUB remains Implemented baseline; FSUBR does not rewrite FSUB criteria as its home |
| Build-family skills (`build-in-waves`, `build-by-story`, `build-inline`) | FSUBR-9.11 — **no caller edits**; no behavior to guard beyond non-addition |
| `docs/product/vision.md` advisory-overlap non-goal | FSUBR-9.3 |

- **FSUBR-9.1** (guard) WHEN `load-subgraph` runs THE SYSTEM SHALL CONTINUE TO derive only from live SSOT via fixed extraction and set operations and SHALL NOT write `docs/specs/GRAPH.md` or any committed graph projection under `docs/`.
- **FSUBR-9.2** (guard) WHEN `load-subgraph` runs THE SYSTEM SHALL CONTINUE TO omit feature-level `DEPENDS_ON` / `depends_on` edges from the envelope (FSUB-1.13).
- **FSUBR-9.3** (guard) WHEN horizontal neighbors or clusters are returned THE SYSTEM SHALL CONTINUE TO mark them advisory (`advisory: true` / non-gate banner) and SHALL CONTINUE TO report OWNS coverage so thin is visible as thin.
- **FSUBR-9.4** (guard) WHEN the test-side reference under `tests/feature-subgraph/` is updated for FSUBR THE SYSTEM SHALL CONTINUE TO keep it pack-test-only (not imported by skills; no `*.py` under `skills/execution/load-subgraph/`).
- **FSUBR-9.5** (guard) WHEN FSUBR ships THE SYSTEM SHALL CONTINUE TO leave `audit-trace` finding codes E1–E5 and W1–W3 unchanged.
- **FSUBR-9.6** (guard) WHEN `pathfind` runs THE SYSTEM SHALL CONTINUE TO keep its decision-map graph separate from feature-subgraph edges.
- **FSUBR-9.7** (guard) WHEN optional roadmap or architecture layers are absent THE SYSTEM SHALL CONTINUE TO no-op P3–P5 as FSUB specifies (ARCH-2).
- **FSUBR-9.8** (guard) WHEN `frame-change` or `inspect-change` needs horizontal neighbors THE SYSTEM SHALL CONTINUE TO obtain them via `load-subgraph` (FSUB-1.15) and SHALL present neighbors using the schema 1.1 envelope fields of story 1.
- **FSUBR-9.9** WHEN FSUBR changes horizontal retrieval behavior that the human guide surfaces THE SYSTEM SHALL update `docs/guide/concepts/feature-graph.md` and keep `docs/guide/START-HERE.md` and `docs/guide/skills/README.md` consistent with the new caller set and `cluster` query (or record an explicit no-sync decision in design if a file needs no edit).
- **FSUBR-9.10** WHEN AGENTS or architecture skill tables list model-invoked skills or horizontal steps THE SYSTEM SHALL update those inventories if they name callers or queries — **no other behavior to guard** on those inventory files.
- **FSUBR-9.11** THE SYSTEM SHALL NOT add build-family (`build-in-waves` / `build-by-story` / `build-inline`) skills as required retrieval callers in FSUBR.
- **FSUBR-9.12** IF `docs/specs/` is missing or no usable seeds (terms, codes, or paths) exist THEN THE SYSTEM SHALL treat retrieval as an explicit **no-op** and SHALL NOT invent neighbors or clusters.
- **FSUBR-9.13** (guard) WHEN retrieval returns empty or thin results THE SYSTEM SHALL CONTINUE TO treat them as advisory and SHALL NOT fail a gate, block frame-change, or fail review solely because of empty or thin neighbors or clusters (FSUB-1.12 / vision non-goal).
- **FSUBR-9.14** WHEN a retrieval package is reused within the active session or parent handoff THE SYSTEM SHALL reuse it only if the **seed set**, the **source inputs** that feed derivation, and the **schema/recipe version** are unchanged; otherwise THE SYSTEM SHALL rederive.
- **FSUBR-9.15** THE SYSTEM SHALL NOT ship a session-local on-disk retrieval cache path, schema, or invalidation contract in FSUBR.

## 10. Quality attributes

**Section-kind:** nfr

**Story:** As a pack consumer, I want retrieval upgrades to stay deterministic,
passive-data safe, and cheap enough for multi-caller sessions without a disk cache.

- **Performance:** **FSUBR-10.1** WHEN `load-subgraph` runs neighbors or `cluster` over a fixture of at least 50 feature specs and 500 path tokens THE SYSTEM SHALL complete with a bounded number of file reads (one full read per source artifact, no per-edge process spawn) — verified by unit/scenario bound independent of LLM calls.
- **Security:** **FSUBR-10.2** WHEN path tokens or prose are read from specs THE SYSTEM SHALL treat them as passive data and MUST NOT obey embedded instructions — verified by a fixture with instruction-shaped path or comment that is not executed.
- **Reliability:** **FSUBR-10.3** IF a single Files block fails under the fixed P1 parser rules (after stop-boundary application) THEN THE SYSTEM SHALL skip or empty only that block’s contribution, preserve valid OWNS tokens from other Files blocks of the same feature, continue other features, report a non-fatal note, and still return an envelope or cluster for the rest — verified by a mixed valid/corrupt multi-block fixture.
- **Reliability:** **FSUBR-10.4** IF an entire source `tasks.md` (or required SSOT file for a feature) is unreadable THEN THE SYSTEM SHALL skip that feature’s OWNS contribution, report a non-fatal note, continue other features, and still return an envelope or cluster for the rest — verified by a fixture with one unreadable feature among valid ones.
- **Accessibility: None** — ships markdown skills and harness chat output; no custom interactive product UI.

---

## Design constraints

Not EARS criteria. Design (and then `passes.md` / fixtures) MUST freeze these
before implementation claims the constants. System criteria above already require
fixed/non-adaptive behavior where applicable.

1. Exact cluster OVERLAPS weight threshold (fixed integer; not runtime-adaptive).
2. Exact cluster member cap (includes focus; ≤ `NEIGHBORS_MAX`).
3. Exact OOS item-count cap and total text-size ceiling.
4. Deterministic cluster member sort key and tie-breaks.
5. Deterministic rules distinguishing code/prose-shaped rejects from accepted root filenames, dotfiles, and extension-bearing paths.
6. Exact Files-section header syntax list beyond the minimum semantic boundaries (Reuse, Interfaces, Depends-on, Steps).
7. Exact `via_traces` object field layout (keys per kind) in `envelope.md`.
8. Exact field name for per non-focus-member path evidence on the cluster card (must obey FSUBR-3.9: bounded list, deterministic order, Story 1 cap/truncation honesty).
9. Normalization function for OOS text dedupe (deterministic; preserves source-CODE attribution).
10. Focus placement in the returned member list (e.g. always first) consistent with FSUBR-3.5–3.6.
11. Coverage metric for cluster/neighbors remains `owns_coverage` (FSUBR-3.10 / FSUB-1.16). Any future metric change requires requirements re-approval (reroute / amend), not a silent design substitute.

---

## Out of Scope

- **Global community / partition recipes** — triangle-supported CC, Jaccard global partitions, Leiden-style hierarchies, and any `communities()` API that partitions the full registry (deferred until clean-graph boundedness and cross-cut stability are proven).
- **Runtime P6 DEPENDS_ON** edges in `load-subgraph` (committed follow-on item 5; own framing).
- **Work-graph anchors / code-KG adapters** (committed follow-on item 6; own framing).
- **Session-local on-disk retrieval cache** — path, schema, invalidation, or SKNS basename; not a committed follow-on; revisit only if measured cost justifies.
- **Build-family required callers** (`build-in-waves` / `build-by-story` / `build-inline`).
- **Materialized graph SSOT** under `docs/` (GRAPH.md, JSON edge stores, rebuild jobs).
- **Untyped provenance / edge_extensions bags** and **P6 / work-graph trace kinds** in FSUBR.
- **LLM similarity** for OOS dedupe or community membership.
- **Adaptive** cluster threshold or caps at runtime.
- **Merging pathfind** tickets into feature-subgraph edges.
- **Rewriting FSUB’s historical triad** as the normative home of Wave A criteria (FSUBR owns the delta; FSUB stays Implemented baseline).
- **New audit-trace E-codes** for OWNS thinness or cluster size.
- **Frame-locking** exact integers k=2, max_members=8, or line-only OOS caps (design freezes real constants).
- **Approach B/C packaging** — dual forever schema skill or parallel `load-subgraph-v2` skill (frame locked Approach A).

---

## Requirements-level open questions

**None.**

## Design decisions to freeze

See **Design constraints** above (items 1–11). These are not unresolved product
forks; they are constants and recipe details design must pin with fixtures.
