---
name: load-subgraph
description: Use when frame-change, inspect-change, or any skill needs feature
  neighbors, overlap, reuse-miss context, blast radius, or a multi-hop feature
  subgraph — produces an advisory envelope (neighbors, OWNS coverage, seeds)
  from live docs/specs with no graph file.
---

# Load Feature Subgraph

Ask-time horizontal neighbor derivation. Sibling of `audit-trace`: fixed passes
in `references/passes.md`, set operations, same inputs → same edge/seed set.

## What you produce

Print **exactly one envelope** shaped by `references/envelope.md`:

1. `advisory: true` and the thin-neighborhood banner  
2. `owns_coverage` (`with_owns` / `registered`) — always  
3. Query payload (`neighbors` | `ancestors` | `descendants` | `blast_radius` | `subgraph`)  
4. `p0` truncation stats when terms were used  

You do **not** produce a file under `docs/`. You do **not** invent DEPENDS_ON edges.

## Procedure

1. Resolve repo root. If `docs/specs/` is missing, say so and stop (empty registry).
2. Load **`references/passes.md`**. Build a **two-stage derivation snapshot**
   (Stage A core: INDEX + tasks.md OWNS + optional-layer presence; Stage B only
   for `cluster` after members known — member `requirements.md` if not buffered).
   Each path is read or statted **at most once** (`read_ledger`).
3. Run the named query as a **pure function of the snapshot** (neighbors /
   cluster / ancestors / descendants / blast_radius / subgraph). No further
   file IO. Pass order inside the snapshot: R → P1 → D → P2 → P0 if terms →
   P3/P4/P5 as applicable → query merge. Grep/set ops only; do not improvise
   ranking or stop-lists.
4. Render the envelope (`schema_version` / `recipe_id` per passes.md). Always
   include OWNS coverage even when neighbor list is empty. Carry reliability
   notes from the snapshot (no silent note count cap).
5. Return to the caller. Summary cards (feature name, Out-of-Scope) may use
   texts already in the snapshot; do not re-open files already ledgered.

## Determinism

Two independent runs on the same frozen tree and same query MUST yield the same
edge set and seed set. Rebuild the snapshot per invocation; do not cache across
SSOT edits. Fingerprints include optional-layer **presence/absence** so a layer
appearing later invalidates a retrieval package.

## Callers

`frame-change` and `inspect-change` obtain horizontal neighbors via this skill
(REQUIRED SUB-SKILL), passing **key terms and candidate paths** so P0 and P1 both
contribute. Pathfind stays a separate decision graph — do not merge tickets.

## The Iron Law

```
NO GRAPH FILE. NO DEPENDS_ON EDGES. NO GATE FROM THIN NEIGHBORS.
PASSES.MD IS THE ONLY RANKING AND STOP-LIST AUTHORITY.
```

## Rationalization

| Thought | Reality |
|---|---|
| "Skip P0 — we have paths" | Pre-code frame-change often has no paths; P0 is required when terms are supplied |
| "Boolean membership is enough" | Rank by shared meaningful paths; truncate to NEIGHBORS_MAX once after union |
| "Empty OWNS means no features" | Report owns_coverage; thin Files coverage ≠ empty registry |
| "Write GRAPH.md so the next call is faster" | Live read only; no projection under docs/ |
| "Import the test helper / invent my own weights" | Only passes.md constants and recipes |
| "Thin list is a review failure" | Advisory; never fail a gate on neighbors alone |
| "Re-read tasks.md while ranking neighbors" | Snapshot first; queries are pure on buffered texts |
| "Skip Stage B — we already have OWNS" | Cluster OOS needs member requirements after members are known |

## Red Flags

- Writing or proposing `docs/specs/GRAPH.md` or any committed edge store
- Returning unordered neighbor sets or lists longer than NEIGHBORS_MAX
- Dropping P0 when the caller passed terms
- Keying features by directory slug when a CODE exists
- Emitting DEPENDS_ON / depends_on in the envelope
- Failing frame-change or review solely because neighbors are thin or empty
- Skipping owns_coverage on the envelope

## Done when

Envelope printed with OWNS coverage and advisory banner; no graph file written;
query payload matches passes.md.
