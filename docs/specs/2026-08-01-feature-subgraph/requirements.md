# Requirements: Feature subgraph derivation

Feature code: FSUB
Status: Implemented
Date: 2026-08-01
Approved: 2026-08-01 (user)
Implemented: 2026-08-01 (build-inline on main)

Adds an **ask-time derivation layer** over existing feature IDs so discovery and
review skills can query multi-hop neighbors, ancestors, blast radius, and a
bounded subgraph without materializing a graph file. Ships two skills:
model-invoked `load-subgraph` (sibling of `audit-trace`) and user-invoked
`map-features` (sibling of `configure-repo` / `scan-architecture`).

**Namespaces this feature consumes.** Feature codes (`CODE`), requirement IDs
(`CODE-N.M`), architecture IDs (`ARCH-N`), roadmap IDs (`MILE-N`, `ROAD-N`), and
product goals (`GOAL-N`) stay owned by their existing skills. FSUB mints no new
ID grammar; path tokens are not IDs.

**Ownership split.** Spec SSOT remains `requirements.md` / `design.md` /
`tasks.md` / `docs/specs/INDEX.md` / roadmap / architecture. FSUB **derives**
edges at ask time and may **propose** additive SSOT edits only through
`map-features` with human confirmation. Vertical trace stays `audit-trace`.
Pathfind keeps its own decision graph.

**Evidence that shaped the frame.** Across two consumer repos, optional
hand-declared edges (e.g. INDEX `Roadmap item`) filled ~10% of rows. Mandatory
`**Files:**` blocks already yield hundreds of path tokens and dozens of
OVERLAPS edges with zero new authoring. Denoising is load-bearing: one
cross-cutting feature owning 106 paths dominated 10 of the top 12 derived
overlap pairs when ranking was boolean. Term matching remains load-bearing at
frame-change time, when candidate paths often do not yet exist.

## 1. Load a derived feature subgraph at ask time

**Story:** As an agent running a discovery or review skill, I want a bounded
subgraph of existing feature IDs computed on demand from SSOT, so that I can
reason about neighbors and blast radius without a generated graph file.

- **FSUB-1.1** THE SYSTEM SHALL expose a model-invoked skill named `load-subgraph` under `skills/execution/load-subgraph/` that does not carry `disable-model-invocation: true`.
- **FSUB-1.2** WHEN `load-subgraph` runs THE SYSTEM SHALL derive edges only from live SSOT files under the consumer repo (`docs/specs/**` including `requirements.md`, `design.md`, and `tasks.md`; `docs/specs/INDEX.md`; `docs/roadmap/INDEX.md` when present; `docs/architecture/**` and feature `design.md` files when present) using fixed extraction rules and set operations — verified by two independent runs on the same fixture yielding the same edge set and seed set.
- **FSUB-1.3** WHEN `load-subgraph` runs THE SYSTEM SHALL NOT write `docs/specs/GRAPH.md`, any JSON or other graph projection under `docs/`, or any other committed materialization of the edge set.
- **FSUB-1.4** THE SYSTEM SHALL allow only these node kinds in a subgraph: `GOAL-N`, `MILE-N`, `ROAD-N`, feature `CODE`, story `CODE-N`, criterion `CODE-N.M`, `ARCH-N`, and path tokens — and SHALL NOT invent a parallel ID namespace.
- **FSUB-1.5** WHEN pass **P0 (TERMS)** runs with one or more key terms (from a new idea, a frame-change scan, or a diff summary) THE SYSTEM SHALL match those terms across `docs/specs/` (at least `requirements.md`, `design.md`, and `tasks.md` prose) and emit every matching feature's `CODE` as a seed node — the same dual-signal role key-term grep has today in the feature-overlap doctrine.
- **FSUB-1.6** WHEN pass **P1 (OWNS)** runs THE SYSTEM SHALL associate each feature `CODE` with the set of path tokens extracted from that feature's `tasks.md` `**Files:**` blocks (Create / Modify / Move / Test and equivalent labels).
- **FSUB-1.7** WHEN pass **P2 (OVERLAPS)** runs THE SYSTEM SHALL emit an undirected edge between two distinct feature codes whose denoised OWNS sets (story 2) have a non-empty intersection.
- **FSUB-1.8** WHEN pass **P3 (IMPLEMENTS)** runs and `docs/specs/INDEX.md` exists THE SYSTEM SHALL emit `CODE → ROAD-N` for every INDEX row whose Roadmap-item cell is a live `ROAD-N`, and SHALL treat empty, `—`, or missing cells as absent edges (not errors).
- **FSUB-1.9** WHEN pass **P4 (CONTAINS)** runs and `docs/roadmap/INDEX.md` exists THE SYSTEM SHALL emit containment edges for milestone membership (`MILE-N` contains its member `ROAD-N` items) and, where Goals: cite `GOAL-N`, for `GOAL-N` → `MILE-N`.
- **FSUB-1.10** WHEN pass **P5 (RESPECTS)** runs and `docs/architecture/` exists THE SYSTEM SHALL include `Respects: ARCH-N` citations from feature `design.md` files as edges in the subgraph view without re-implementing or replacing `audit-trace` E4/E5/W3.
- **FSUB-1.11** THE SYSTEM SHALL support at least these queries, each computed at ask time as set closure over P0 seeds and P1–P5 edges: `ancestors(CODE)`, `descendants(MILE-N)`, `neighbors(CODE)`, `blast_radius(path)`, and `subgraph(seed)` where seed is one or more terms, codes, or paths — and WHEN seed includes terms THE SYSTEM SHALL resolve those terms to `CODE` nodes via P0 before expanding.
- **FSUB-1.12** WHEN `load-subgraph` returns neighbors, overlaps, or a subgraph for discovery or review THE SYSTEM SHALL treat that result as advisory best-effort and SHALL NOT fail a gate, block `frame-change`, or fail a review solely because of overlap or neighbor findings.
- **FSUB-1.13** WHEN `load-subgraph` runs THE SYSTEM SHALL NOT derive feature-level `DEPENDS_ON` edges (P6 runtime derivation is out of scope for this feature).
- **FSUB-1.14** WHEN keying a feature node THE SYSTEM SHALL use the feature's registered `CODE` from `docs/specs/INDEX.md` and/or the `Feature code:` line in `requirements.md`, and SHALL NOT key nodes by directory slug alone when a `CODE` is available.
- **FSUB-1.15** WHEN `frame-change` or `inspect-change` needs horizontal feature neighbors THE SYSTEM SHALL obtain the neighbor set via `load-subgraph` — including P0 term seeds and P1 path-derived structure — so that set subsumes both neighbor signals of the feature-overlap doctrine (candidate paths **and** key terms), and SHALL CONTINUE TO present neighbors as summary cards without blocking the gate.
- **FSUB-1.16** WHEN `load-subgraph` returns a neighbor, overlap, or subgraph result THE SYSTEM SHALL report **OWNS derivation coverage** alongside it — the count of registered features with a non-empty OWNS set over the count of total registered features — so a thin neighborhood is visible as thin rather than presented as an authoritative empty or complete answer.

## 2. Denoise OVERLAPS and rank neighbors

**Story:** As a developer reading `neighbors(CODE)`, I want shared-path noise
removed and results ranked by meaningful overlap, so that a cross-cutting feature
does not drown every neighbor list.

- **FSUB-2.1** WHEN pass P2 builds the shared-path set for OVERLAPS THE SYSTEM SHALL exclude path tokens that are manifests, lockfiles, or workspace-root tokens (the stop-list defined in FSUB-2.4) from that shared set.
- **FSUB-2.2** WHEN matching path tokens for OWNS equality or OVERLAPS intersection THE SYSTEM SHALL NOT expand a path token into its ancestor directories; matching SHALL be at file granularity, or on an explicitly declared directory ownership token only (a token that names a directory as owned, without treating every parent prefix as owned).
- **FSUB-2.3** WHEN `neighbors(CODE)` is computed THE SYSTEM SHALL return a list ordered by descending count of shared *meaningful* path tokens (paths remaining after FSUB-2.1), truncated to a fixed maximum length recorded in the `load-subgraph` skill body, and SHALL NOT return an unordered boolean membership set as the primary neighbor result.
- **FSUB-2.4** THE SYSTEM SHALL define the stop-list to include at least: common manifest basenames (`package.json`, `Cargo.toml`, `go.mod`, `pyproject.toml`, `Gemfile`, `composer.json`, `Package.swift`); common lockfile basenames (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `Cargo.lock`, `poetry.lock`, `Gemfile.lock`, `composer.lock`); and workspace-root tokens that are only a single path segment from the set `{src, lib, app, apps, packages, services, crates, cmd, internal, vendor, node_modules, dist, build, target, out}` (case-sensitive as written in the token after normalization). Design SHALL extend this list for pack-shaped repos (e.g. top-level segments such as `skills`, `templates`, `hooks`, `scripts` when they appear as sole path-segment tokens) without shrinking the minimum set above.
- **FSUB-2.5** IF after denoising two features share zero meaningful path tokens THEN THE SYSTEM SHALL NOT emit an OVERLAPS edge between them solely because they shared stop-listed tokens.
- **FSUB-2.6** WHEN ranking neighbors THE SYSTEM SHALL count each distinct meaningful path token once per pair (set cardinality of the intersection), so that a feature with a large OWNS set does not outrank others except by shared meaningful paths — verified by a fixture where a 100+-path feature shares one meaningful file with A and a small feature shares three meaningful files with A, and `neighbors(A)` ranks the small feature above the large one.

## 3. Parse legacy `**Files:**` for P1

**Story:** As a developer on a repo whose `tasks.md` files predate the hardened
grammar, I want P1 to extract the same ownership paths the prototype measured, so
that derivation works on existing specs — not only on newly written plans.

- **FSUB-3.1** WHEN pass P1 extracts path tokens THE SYSTEM SHALL accept the **legacy** `**Files:**` forms in existing `tasks.md` files: (a) bulleted `Create:` / `Modify:` / `Move:` / `Test:` lines with a path after the label; (b) inline prose under `**Files:**` that lists paths; (c) path tokens with or without surrounding backticks.
- **FSUB-3.2** WHEN a path token carries a trailing line or range suffix glued to the path — including `:N`, `:N-M`, `:N,M`, and `:N-M,P` forms (e.g. `src/app/App.tsx:86,1030` or `SKILL.md:25-44`) — THE SYSTEM SHALL strip that suffix and keep the path portion as the OWNS token.
- **FSUB-3.3** WHEN pass P1 runs over a fixture of pre-hardening `tasks.md` text containing both bulleted Create/Modify lines and glued line-range suffixes THE SYSTEM SHALL extract every intended file path and SHALL NOT drop a path solely because it used the legacy form — verified by a unit fixture whose expected OWNS set is fixed in the test.
- **FSUB-3.4** (guard) WHEN pass P1 runs THE SYSTEM SHALL CONTINUE TO derive OWNS from legacy `**Files:**` forms in already-written `tasks.md` files even after a hardened authoring grammar exists for new plans.

## 4. Harden `**Files:**` grammar for new plans

**Story:** As a developer writing a new `tasks.md` under `plan-tasks`, I want a
hardened `**Files:**` grammar so that future OWNS extraction does not depend on
stripping glued line ranges from newly authored plans.

- **FSUB-4.1** WHEN `plan-tasks` authors a **new** task's `**Files:**` block THE SYSTEM SHALL require the **hardened** grammar: each path token appears in backticks; line numbers or ranges, when stated, are not glued into the path token (they may appear in surrounding prose or a separate annotation, not as `path:lines` inside the path token).
- **FSUB-4.2** THE SYSTEM SHALL update `templates/tasks.md` and `skills/spec/plan-tasks/SKILL.md` so the hardened `**Files:**` grammar is the documented authoring rule for new plans.

## 5. No-op when optional layers are absent

**Story:** As a developer on a thin consumer repo without roadmap or architecture
docs, I want subgraph queries to degrade cleanly, so that FSUB does not invent
standing facts (ARCH-2).

- **FSUB-5.1** WHERE `docs/architecture/` does not exist THE SYSTEM SHALL no-op pass P5 and SHALL NOT invent `ARCH-N` nodes or RESPECTS edges.
- **FSUB-5.2** WHERE `docs/roadmap/INDEX.md` does not exist THE SYSTEM SHALL no-op passes P3 and P4 for roadmap structure, SHALL NOT invent `MILE-N` or `ROAD-N` nodes, and WHEN `ancestors(CODE)` is requested THE SYSTEM SHALL return the bare feature (and any non-roadmap edges that still apply) without erroring.
- **FSUB-5.3** WHERE a feature has no `tasks.md` or no `**Files:**` block THE SYSTEM SHALL give that feature an empty OWNS set and SHALL NOT fabricate paths.

## 6. Backfill SSOT with map-features

**Story:** As a developer adopting the skill set on a brownfield repo, I want a
user-run wizard that proposes missing feature codes, ROAD bindings, ownership
gaps, and DEPENDS_ON *candidates*, so that SSOT improves only with my confirm.

- **FSUB-6.1** THE SYSTEM SHALL expose a user-invoked skill named `map-features` under `skills/track/map-features/` with `disable-model-invocation: true`.
- **FSUB-6.2** WHEN `map-features` runs THE SYSTEM SHALL scan the consumer repo and propose, without writing until confirmation: (a) missing `Feature code:` lines on `requirements.md` files that already sit under a registered or registrable feature; (b) empty INDEX `Roadmap item` cells when a live `ROAD-N` is a plausible bind; (c) OWNS gaps for significant code paths not claimed by any feature's denoised OWNS set; (d) feature-level **DEPENDS_ON candidates** derived from `Reuse:` and `Interfaces: Consumes` (and equivalent) as proposals only.
- **FSUB-6.3** WHEN `map-features` has proposals THE SYSTEM SHALL present them to the user and write only the proposals the user explicitly confirms, as additive edits to SSOT files — never a graph projection file.
- **FSUB-6.4** WHEN `map-features` proposes DEPENDS_ON candidates THE SYSTEM SHALL NOT auto-write those candidates and SHALL NOT cause `load-subgraph` to treat unconfirmed candidates as edges.
- **FSUB-6.5** IF `map-features` cannot resolve a feature's `CODE` from INDEX or a `Feature code:` line THEN THE SYSTEM SHALL report that gap as a first-class backfill item and SHALL NOT silently key the feature by directory slug in user-facing results.
- **FSUB-6.6** (guard) WHEN model-invoked skills detect brownfield mapping needs THE SYSTEM SHALL CONTINUE TO name `/map-features` for the user to run and MUST NOT auto-invoke it (ARCH-5).

## 7. Guard existing methodology behavior

**Story:** As a maintainer of the skill set, I want FSUB to extend horizontal
context without weakening vertical gates, pathfind, or task parallelism.

**Files this feature is expected to touch (guard inventory):**

| Path / area | Guard |
|---|---|
| `skills/execution/audit-trace/**` | FSUB-7.1 |
| `docs/product/vision.md` (non-goal line) | FSUB-7.2 |
| `templates/tasks.md`, `skills/spec/plan-tasks/SKILL.md` | FSUB-7.3, FSUB-3.4, story 4 |
| `skills/discovery/pathfind/**`, pathfind artifacts | FSUB-7.4 |
| `docs/architecture/artifacts.md` (live-read doctrine) | FSUB-7.5 |
| `docs/specs/INDEX.md` (registry role) | FSUB-7.6 |
| Task-level `Depends-on:` in plans | FSUB-7.7 |
| New: `skills/execution/load-subgraph/**`, `skills/track/map-features/**` | no prior behavior |
| Tests / guide / AGENTS inventory | no product behavior to guard beyond packaging |

- **FSUB-7.1** (guard) WHEN `load-subgraph` or `map-features` runs THE SYSTEM SHALL CONTINUE TO leave `audit-trace` finding codes E1–E5 and W1–W3 (and their semantics) unchanged — FSUB adds no new audit-trace E-codes for overlap or OWNS.
- **FSUB-7.2** (guard) WHEN feature-overlap or neighbor results are produced THE SYSTEM SHALL CONTINUE TO treat them as advisory best-effort, never a hard gate, matching `docs/product/vision.md` non-goal on perfect feature-overlap detection.
- **FSUB-7.3** (guard) WHEN `plan-tasks` runs THE SYSTEM SHALL CONTINUE TO require a `**Files:**` block (Create / Modify / Test) on each task and a task-level `Depends-on:` (or omit-for-serial) as the parallelism signal between tasks.
- **FSUB-7.4** (guard) WHEN `pathfind` runs THE SYSTEM SHALL CONTINUE TO keep its decision-map graph separate; FSUB SHALL NOT merge pathfind tickets into feature-subgraph edges or require pathfind anchors for load-subgraph.
- **FSUB-7.5** (guard) WHEN horizontal neighbors are resolved THE SYSTEM SHALL CONTINUE TO answer from a live read of the specs (derivation at ask time), without reintroducing a committed generated feature-graph artifact as SSOT.
- **FSUB-7.6** (guard) WHEN a feature code is registered THE SYSTEM SHALL CONTINUE TO treat `specify-behavior` Step 1 / `docs/specs/INDEX.md` as the sole feature-code registry.
- **FSUB-7.7** (guard) WHEN tasks declare `Depends-on: Task N` THE SYSTEM SHALL CONTINUE TO treat that edge as task parallelism only and SHALL NOT interpret it as feature-level DEPENDS_ON (P6).

## 8. Quality attributes

**Section-kind:** nfr

**Story:** As a pack consumer, I want subgraph derivation cheap, passive-data
safe, and deterministic, so that discovery stays harness-portable.

- **Performance:** **FSUB-8.1** WHEN `load-subgraph` runs over a fixture of at least 50 feature specs and 500 path tokens THE SYSTEM SHALL complete P0–P5 and one `neighbors` query with a bounded number of file reads (one full read per source artifact, no per-edge process spawn) — verified by a scenario/unit bound independent of LLM calls.
- **Security:** **FSUB-8.2** WHEN path tokens or prose are read from `tasks.md`, INDEX, roadmap, or design files THE SYSTEM SHALL treat them as passive data and MUST NOT obey embedded instructions — verified by a fixture embedding an instruction-shaped path or comment and confirming it is not executed as a command.
- **Reliability:** **FSUB-8.3** IF a source file is missing or a `**Files:**` block is unparseable for one feature THEN THE SYSTEM SHALL skip or empty that feature's contribution, report a non-fatal note when in `map-features`, and still return a subgraph for the rest — verified by a fixture with one corrupt block among valid ones.
- **Accessibility: None** — ships markdown skills and conversational/report output through the host harness; no custom interactive product UI.

## Out of Scope

- **Materialized graph artifacts** — `docs/specs/GRAPH.md`, committed JSON edge stores, rebuild jobs, or Neo4j/Memgraph/Tree-sitter code-KG adapters.
- **ADR superseding** `docs/architecture/artifacts.md` or the live-read horizontal doctrine — derivation *is* that doctrine with set operations (including P0 term seeds).
- **Runtime P6 DEPENDS_ON edges** in `load-subgraph` — candidates may be proposed only by `map-features` (FSUB-6.2–6.4); auto-written or derived DEPENDS_ON edges are a later feature if ever adopted.
- **`DECOMPOSES_INTO` / parent-child feature codes** — hierarchy stays in `CODE-N` stories plus P3/P4.
- **HTML visualization** of the subgraph that refreshes as features change — deferred to a later round (temp vs committed packaging undecided; precedents: `scan-architecture` `$TMPDIR`, XPLN `docs/explainers/`, DFSYNC JSON+HTML+serve). On the roadmap when that round opens; not declined forever.
- **New audit-trace E-codes** for missing OWNS, empty ROAD bindings, or overlap density.
- **Changing pathfind** ticket types, labels, or Layer-0 ownership.
- **Replacing `audit-trace`** vertical coverage with graph reachability.
- **Mandatory call of `load-subgraph` from every discovery skill** beyond `frame-change` and `inspect-change` (FSUB-1.15); additional callers may be added later without expanding this feature's Out of Scope rejection.

## Open Questions

Resolved for approval 2026-08-01. Carry into **design** (not reopened as
requirements):

1. **P0 seed bound and ranking** — FSUB-2.3 bounds `neighbors()` by shared
   meaningful path count; P0 has no equivalent ceiling on term-seed size. A
   generic term matched across many specs can seed most of the registry before
   `subgraph(seed)` expands. Not a requirements regression (parity with today's
   key-term grep; FSUB-1.15). Design MUST decide a P0 seed bound and ranking
   alongside the `neighbors` bound N so term-channel noise is handled with the
   same explicitness as path-channel denoising (story 2) — not discovered during
   implementation.
2. Exact numeric bound N for `neighbors()` truncation (FSUB-2.3).
3. Concrete pack-shaped stop-list extension tokens beyond the FSUB-2.4 minimum
   (skills, templates, hooks, scripts, …).
4. Fixture paths and scenario layout under `tests/`.
