# Requirements: Sharded Module Graph

Feature code: MODGRAPH
Status: Implemented
Date: 2026-07-11

Slice M2 of the enterprise context layer. Reorganizes the feature graph around
the modules M1 (MODMAP) introduced: features are grouped into per-module shards
so the graph never renders as one unbounded file, and the query is bounded so a
hub file can't drown the ranking. Depends on M1's `load_manifest` and
`resolve_module`. Design context: `scratchpad/ENTERPRISE-CONTEXT-DESIGN.md`.

Scope boundary (agreed with the user): M2 does **basic** homing — group a
feature by running `resolve_module` on its owned paths at render time. The
sophisticated policy (split-signal on owns-spanning, cross-cutting facets, a
`Module:` override) is **M3**, not here.

Vocabulary: a feature's **home module** is the single module whose folders own
all of that feature's owned paths; a **shard** is the generated per-module file
listing the features homed to it; the **index** is the top-level `GRAPH.md`
listing modules and the cross-module shared surface.

## 1. Home each feature to a module

**Story:** As the graph renderer, I want each feature grouped under the module
that owns its code, so the graph can be split by module instead of listed flat.

- **MODGRAPH-1.1** WHEN harvesting with a valid manifest present THE SYSTEM SHALL
  resolve each feature's **complete** set of owned paths against the manifest
  (via M1's `resolve_module`) to determine its home module — the full owned set,
  never the card-capped list that elides paths past the display cap.
- **MODGRAPH-1.2** WHEN every owned path of a feature resolves to the same single
  module THE SYSTEM SHALL home that feature to that module.
- **MODGRAPH-1.3** IF a feature has no owned paths, or its owned paths resolve to
  zero modules, or they resolve to more than one distinct module THEN THE SYSTEM
  SHALL place that feature in the `(unassigned)` bucket.

## 2. Render the sharded graph

**Story:** As a maintainer of a large repo, I want the graph split into a small
top index plus one bounded file per module, so no single file grows without
limit as features accumulate.

- **MODGRAPH-2.1** WHERE a valid manifest is present THE SYSTEM SHALL render the
  top-level `GRAPH.md` as a module index listing each module by code and name.
- **MODGRAPH-2.2** THE SYSTEM SHALL include in the index a cross-module
  shared-surface table listing each path referenced by features in two or more
  different home modules, naming those modules.
- **MODGRAPH-2.3** THE SYSTEM SHALL write one shard file per module with at least
  one homed feature at `<specsDir>/modules/<CODE>.md`, containing a compact row
  per homed feature — its code, name, and owned-path summary — not a full
  summary card.
- **MODGRAPH-2.4** WHEN one or more features are `(unassigned)` THE SYSTEM SHALL
  write an `(unassigned)` shard listing them, so no feature is dropped from the
  rendered graph.
- **MODGRAPH-2.5** THE SYSTEM SHALL render the index and every shard
  deterministically — modules, features, and paths in a stable sorted order — so
  a re-render with unchanged specs is byte-identical.
- **MODGRAPH-2.6** WHEN harvesting with a manifest THE SYSTEM SHALL delete any
  previously generated shard file that the current render does not produce, so
  the committed shard set stays exact.
- **MODGRAPH-2.7** THE SYSTEM SHALL mark the index and every shard with the
  "generated — do not edit by hand" banner.

## 3. Bound the query

**Story:** As a gate consuming the graph (brainstorm dedup, code-review
reuse-miss), I want the most relevant neighbors first and a hard cap on how many
I load, so a hub file every feature touches doesn't bury the real signal.

- **MODGRAPH-3.1** WHEN scoring a query result THE SYSTEM SHALL weight each
  overlapping path by the inverse of the number of features that reference it, so
  a path shared by many features contributes less than one shared by few.
- **MODGRAPH-3.2** WHEN two results have different weighted scores THE SYSTEM
  SHALL order the higher-scored result first, replacing the raw overlap-count
  ordering that ties to alphabetical when every candidate shares one hub path.
- **MODGRAPH-3.3** THE SYSTEM SHALL return at most a configured maximum number of
  full cards, ordered by score.
- **MODGRAPH-3.4** IF more results match than that maximum THEN THE SYSTEM SHALL
  report the number of omitted results rather than dropping them silently.
- **MODGRAPH-3.5** THE SYSTEM SHALL truncate each returned card's out-of-scope
  entries to their first sentence.

## 4. Verify shards; degrade and preserve

**Story:** As a repo owner, I want the sharded graph kept honest the same way the
flat one was, and I want a repo that never adopted modules to behave exactly as
before.

- **MODGRAPH-4.1** WHEN `--verify` runs with a valid manifest present THE SYSTEM
  SHALL report an error if the committed `GRAPH.md` index, the set of committed
  per-module shard files, or any shard's content differs from a fresh render.
- **MODGRAPH-4.2** (guard) WHERE no manifest is present THE SYSTEM SHALL CONTINUE
  TO render `GRAPH.md` as the flat document (`## Cards` + `## Shared surface`)
  and verify it as before, writing no shard files.
- **MODGRAPH-4.3** (guard) WHEN a manifest is present THE SYSTEM SHALL CONTINUE TO
  run M1's boundary verification (orphan, double-mapped, stale-glob) as part of
  `--verify`.
- **MODGRAPH-4.4** (guard) WHEN a manifest is present THE SYSTEM SHALL CONTINUE TO
  check that every harvested feature code is registered in `INDEX.md`.
- **MODGRAPH-4.5** (guard) WHEN returning query results THE SYSTEM SHALL CONTINUE
  TO carry each result's feature `code`, `name`, and summary card, so existing
  consumers keep working despite the new ranking and cap.
- **MODGRAPH-4.6** (guard) THE SYSTEM SHALL CONTINUE TO run with no top-level side
  effects on import.

## Out of Scope

- **Rich feature homing** — the split-signal on owns-spanning, cross-cutting
  facets, and a `Module:` header override — is M3. M2 buckets every ambiguous
  feature as `(unassigned)` and does not try to resolve it.
- **Per-module standards** (M5) and **gate integration** (M6): M2 changes the
  ranking/cap the gates consume, but wiring `brainstorm`/`code-review`/`sync-spec`
  to the sharded layout and cards is M6.
- **The brownfield on-ramp** (M4): M2 assumes the manifest already exists.
- **Semantic/embedding ranking** — the IDF weight is purely structural
  (reference frequency), not content similarity.
- **Changing the manifest format or boundary checks** — those are M1; M2 only
  reads the manifest and re-runs M1's checks unchanged.
