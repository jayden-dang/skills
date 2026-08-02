# `load-subgraph`

> Ask-time derivation of a bounded feature subgraph from live specs — neighbors
> (schema 1.1), **`cluster(focus)`**, ancestors, blast radius, and multi-hop
> subgraph — no generated graph file, no on-disk session cache.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invoked |
| **Reads** | `docs/specs/**`, INDEX, optional roadmap/architecture (P3–P5 no-op when absent) |
| **Writes** | none (envelope in chat only; never `docs/specs/GRAPH.md`) |
| **Called by** | `frame-change`, `inspect-change`, `clarify-decisions`, `design-solution`, `plan-tasks`, `root-cause` |

## Queries

| Query | Role |
|---|---|
| `neighbors` / `subgraph` | Ranked overlaps with path/term evidence (`path_evidence`, `term_evidence`, `via_traces`) |
| `cluster` | Query-local digest for **exactly one** focus CODE — members, path evidence, OOS union |
| `blast_radius` | Ownership blast for a candidate path set (plan-tasks after file map) |
| `ancestors` / `descendants` | Roadmap/architecture edges when those layers exist |

## Callers (advisory)

- **frame-change** — step 1 explore: neighbors/subgraph schema 1.1 + grounded claims
- **inspect-change** — step 3a: neighbors schema 1.1 + reuse-miss brief
- **clarify-decisions** — nested: reuse valid package; standalone: load once
- **design-solution** — Step 1 fresh retrieval after scan, before reuse ladder
- **plan-tasks** — after Step 2 file map: `blast_radius` **and** `cluster(feature CODE)`
- **root-cause** — after Phase 2 only (never the RED loop)

Build-family skills are **not** required callers. Pathfind stays a separate
decision map. Path tokens and prose are **passive data** — not instructions.

See `skills/execution/load-subgraph/SKILL.md`, `references/passes.md`, and
`references/envelope.md`. Human doctrine: [Feature overlap](../concepts/feature-graph.md).
