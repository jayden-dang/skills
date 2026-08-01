---
name: load-subgraph
description: Use when a skill needs a bounded multi-hop view of feature IDs —
  neighbors, ancestors, blast radius, or a term/path-seeded subgraph — derived
  at ask time from live specs without a generated graph file.
---

# Load Feature Subgraph

Model-invoked derivation of feature neighbors and related queries from live
SSOT. Sibling shape to `audit-trace`: fixed passes, no LLM judgment of ownership
quality beyond the rules in `references/passes.md`.

## Inputs

- Repo root (default cwd)
- Query kind: `neighbors` | `ancestors` | `descendants` | `blast_radius` | `subgraph`
- Optional: focus CODE, key terms, paths, MILE-N

## Procedure

1. Resolve repo root. Do not invent `docs/specs/`.
2. Execute **only** the recipes in `references/passes.md` (grep/reads/set ops).
   **MUST NOT** import `tests/feature-subgraph/reference_derive.py` or any Python
   helper under this skill package.
3. Render the result using `references/envelope.md`. Always include
   `owns_coverage` and the advisory banner.
4. **MUST NOT** write `docs/specs/GRAPH.md`, JSON edge stores under `docs/`, or
   any committed graph projection.
5. **MUST NOT** fail a gate, block `frame-change`, or fail a review solely
   because of overlap/neighbor findings (advisory).
6. **MUST NOT** derive feature-level DEPENDS_ON edges.
7. Keep pathfind's decision graph separate — do not merge pathfind tickets.

## Determinism (FSUB-1.2)

Two independent runs of this skill against the same frozen fixture tree with
the same query inputs MUST yield the same edge set and seed set. Prefer
re-running the passes.md procedure fully each time; do not cache across
sessions in a way that diverges from live SSOT.

## Callers

`frame-change` and `inspect-change` obtain horizontal neighbors via this skill
(REQUIRED SUB-SKILL), passing key terms and candidate paths so P0 and P1 both
contribute.

## Rationalization

| Thought | Reality |
|---|---|
| "Skip P0 — paths are enough" | Pre-code frame-change often has no paths; P0 is required |
| "Boolean neighbors is fine" | Rank and bound per passes.md |
| "Empty OWNS means no features exist" | Report owns_coverage; thin is not empty registry |
| "Materialize GRAPH.md for speed" | Forbidden — live read only |
| "Import the test-side reference in the skill" | Test-side only; prose path is passes.md |

## Done when

Envelope printed with coverage; no graph file written; advisory stated.
