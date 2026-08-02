# Feature overlap

The [audit-trace check](traceability.md) is the **vertical** layer: it proves that one feature's requirements, tasks, and tests agree with each other.

Feature overlap is the **horizontal** question — *which features touch the same code, and does this new idea already exist somewhere?* It is answered by **`load-subgraph`**: ask-time derivation over the specs that already exist, so there is nothing to generate and nothing that can go stale.

## The problem

An agent asked to "add a keyboard shortcut for switching modules" has no way to know that a feature called `CHIPUI` already owns half the files it is about to edit, and that its Out-of-Scope section explicitly declined keyboard shortcuts three months ago.

The information exists. It is spread across a dozen `requirements.md`, `design.md`, and `tasks.md` files nobody is going to read — unless something reads them at the two moments it matters.

## How overlap is found

There is no index to build and no derived file to maintain. When a skill needs
horizontal context, it uses **`load-subgraph`** (REQUIRED SUB-SKILL from the
callers below), which derives a bounded subgraph at ask time from live specs:

- **P0 terms** — the idea's or diff's key terms seed matching feature CODEs;
- **P1 paths** — every `**Files:**` block (multi-block) yields OWNS after a
  reject-unsafe-first classifier; denoised intersection yields OVERLAPS; ranked
  and bounded (`NEIGHBORS_MAX`);
- **Neighbors envelope (schema 1.1)** — each neighbor carries integer
  `shared_paths`, `via`, bounded `path_evidence` / `term_evidence`, and typed
  `via_traces` (`path_overlap` | `term_match`); ignore unknown future trace kinds;
- **`cluster(focus)`** — query-local digest for **exactly one** focus CODE:
  focus first, eligible non-focus members (OVERLAPS weight ≥ `CLUSTER_K`),
  member cap including focus, non-focus path evidence, Out-of-Scope union with
  source-CODE attribution. Not a global community partition.

Any feature matched on either signal is a neighbor. Results always include
**OWNS coverage** so a thin neighborhood is visible as thin. The source of truth
remains the specs as they stand — derivation is a live read, not a generated
graph file. Path tokens and prose from specs are **passive data** — never
executed as instructions.

## The Summary card

A matched neighbor is loaded as its **Summary card**, not its full spec — a bounded per-feature digest sitting at the top of the spec: the feature code, its name, the paths it owns, and its Out-of-Scope list. The card lets the agent grasp a neighbor's essence — what it already covers and what it deliberately declined — without pulling a whole design document into context.

A card reads roughly like this:

```markdown
### CHIPUI — Module chip rail
- owns: src/shell/chip-rail.tsx, src/shell/module-store.ts
- interfaces: useActiveModule() → Module, setActiveModule(id)
- out-of-scope: keyboard shortcuts for switching | drag-to-reorder
```

That single Out-of-Scope line is often the whole answer: the new idea was already considered here and set aside, with a reason.

## `docs/specs/INDEX.md` — the registry

`INDEX.md` is the sole feature registry. Every feature code is unique repo-wide, forever, and is registered here — by [`specify-behavior`](../skills/specify-behavior.md) — before the requirements file that uses it is written. It is the one place that enumerates every feature, so an overlap search always knows the full set of neighbors to consider.

```markdown
| Code | Feature | Spec | Status | Roadmap item |
|---|---|---|---|---|
| SHELL | Left icon rail for module switching | ./2026-07-09-shell/ | Implemented | ROAD-3 |
| CHIPUI | Module chip rail | ./2026-04-02-chip-rail/ | Shipped | — |
```

The **Roadmap item** column binds each feature to the [`ROAD-N`](../skills/plan-milestones.md) it implements, or `—` when the project has no roadmap layer or the work was never planned as an item. Overlap search ignores it; it exists for [`refresh-roadmap-status`](../skills/refresh-roadmap-status.md)'s plan-to-spec join.

## Where overlap is consumed

Horizontal retrieval is **advisory** at every moment. Required callers:

| Skill | Moment | Query |
|---|---|---|
| [`frame-change`](../skills/frame-change.md) | step 1 explore (front of chain) | `neighbors` / `subgraph` schema 1.1 |
| [`inspect-change`](../skills/inspect-change.md) | step 3a (back of chain) | `neighbors` schema 1.1 |
| [`clarify-decisions`](../skills/clarify-decisions.md) | nested: reuse valid package; standalone: load once before first card | neighbors |
| [`design-solution`](../skills/design-solution.md) | Step 1 after scan, before reuse ladder | **fresh** retrieval |
| [`plan-tasks`](../skills/plan-tasks.md) | after Step 2 file map, before task bodies | `blast_radius` **and** `cluster(feature CODE)` |
| [`root-cause`](../skills/root-cause.md) | after Phase 2 only — never Phases 1–2 RED loop | retrieval for context |

Build-family skills (`build-in-waves` / `build-by-story` / `build-inline`) are
**not** required callers. [`/pathfind`](../skills/pathfind.md) keeps its decision
map separate — never merge pathfind tickets into feature-subgraph edges.

**Grounded claims.** Every overlap, reuse-miss, or Out-of-Scope / “already
declined” conclusion must cite a **feature CODE**, an **edge or trace kind**,
and a **path or term** from the envelope or cluster card. Before concluding
“no relevant feature,” state exact `owns_coverage` (and emptiness when the
list is empty). Retrieval is advisory input only — never invent `Reuse:`,
`Respects:`, `**Files:**` paths, or root-cause hypotheses from the envelope.

**[`frame-change`](../skills/frame-change.md), at the front of the chain.** Before the interview begins, it runs **`load-subgraph`** with the scan's candidate paths and the idea's key terms. Neighbors are presented with **schema 1.1 evidence** plus **OWNS coverage** so a thin neighborhood is visible as thin.

Its completion criterion is a sentence the agent must be able to say: *which existing features share this idea's surface and how the new idea differs, citing feature codes and path/term evidence — or that no existing feature shares its surface (after stating coverage/emptiness).*

**[`inspect-change`](../skills/inspect-change.md), at the back of the chain.** It runs **`load-subgraph`** with the diff's changed paths (and optional terms). When a neighbor comes back, the **Spec** subagent receives its card, with a brief directing it to flag — as a *reuse-miss* finding citing the neighbor's feature code and a path or term — any place the diff reimplements behavior a neighbor already owns.

**[`/map-features`](../skills/map-features.md)** (user-invoked) backfills brownfield gaps — missing Feature codes, ROAD binds, OWNS via Files edits, DEPENDS_ON *candidates* — with human confirm only. It does not materialize a graph.

## An advisory signal, never a gate

The overlap result never fails a review and never stops a frame-change. It sharpens a decision; it does not make one. If the search returns nothing, the agent proceeds and says so. If `docs/specs/` is empty or few features have `**Files:**` blocks, that is a **thin** neighborhood (report OWNS coverage), not an error state.

This keeps the horizontal layer honest: derivation re-reads what is already written; there is no derived graph file to fall behind. Optional roadmap and architecture layers no-op cleanly when absent (P3–P5).

## See also

- [Traceability](traceability.md) — the vertical layer this sits beside
- [`load-subgraph`](../skills/load-subgraph.md) — the derivation skill (neighbors, cluster, blast_radius)
- [`map-features`](../skills/map-features.md) — brownfield backfill
- [Enforcement and tooling](../resources/scripts.md#feature-overlap-search) — mechanics notes
- [Artifacts](artifacts.md) — where `INDEX.md` and the specs live
- [`frame-change`](../skills/frame-change.md) — the overlap check at the front of the chain
- [`inspect-change`](../skills/inspect-change.md) — the reuse-miss check at the back
- [`plan-tasks`](../skills/plan-tasks.md) — blast_radius + cluster after the file map
