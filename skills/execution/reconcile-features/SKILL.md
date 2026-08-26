---
name: reconcile-features
version: 1.0.0
description: >
  Use when external commits, a pull/merge, brownfield code, or a missing feature
  owner must be mapped back onto the capability catalog — reverse tracking,
  changes-since-checkpoint, observed capability candidates, OBS overlay,
  known-impact vs new-capability vs no-spec-impact — and the deliverable is a
  bounded advisory reconciliation envelope plus local `.skills/reverse-features/`
  index. Not for writing requirements (specify-behavior), backfilling confirmed
  registry rows (/map-features), docs-only ID audit (audit-trace), or ask-time
  neighbors (load-subgraph).
---

# Reconcile Features

Read-only reverse track from git/code evidence onto the capability catalog.
Sibling of `load-subgraph` (horizontal neighbors) and `audit-trace` (vertical
IDs): this skill answers **what changed out there, and which Recognized features
or OBS candidates own it?**

## The Iron Law

```
NO FEATURE CODE MINT. NO SPECS WRITE. NO CONSUMING-REPO CI.
ONE OVERLAY ROOT. INDEX THEN ADVANCE. ENVELOPE.md IS THE SHAPE.
```

## What you produce

Print **exactly one** envelope shaped by `references/envelope.md`
(`schema_version: "1"`, `recipe_id: "rfeat-1.0"`). When `.skills/` is writable
and ignored, also index active OBS cards under `.skills/reverse-features/` per
`references/passes.md`.

You do **not** invent Feature CODEs. You do **not** write `docs/specs/**`. You
do **not** add hooks, workflows, or tracked scripts to the consuming repo. You
do **not** write `docs/specs/GRAPH.md`. You do **not** Approve requirements from
code.

## Procedure

1. Resolve the consuming repo root and mode (`changes-since-checkpoint`, `full`,
   or `brownfield-bootstrap`).
2. Load **`references/passes.md`** and run its passes in order — rename-aware
   `git diff --name-status -z -M`, generated-path drop, catalog Files/surface
   roots, active overlay + tombstone lookup, classify, cap.
3. Load **`references/envelope.md`** and render the envelope. Banner always.
4. Index pending/reopened OBS into `active/<domain>.md` + `observations/OBS-*.json`,
   then advance `state.json` (`last_reconciled_sha = head`). Stateless if not
   writable: still print the envelope with `checkpoint.advanced_to: null`.
5. Return the envelope to the caller. Unresolved `pending` findings must be
   surfaced before `frame-change` / `realign-spec` decisions on those surfaces.
   Name `/map-features` for confirm-then-write backfill; never auto-invoke it.

## Callers

| Skill | When |
|---|---|
| `frame-change` | After pull/merge or when INDEX may miss external work — before tier/requirements |
| `inspect-change` | When changed paths have no Recognized owner but look behavior-bearing |
| `realign-spec` | Optional pre-check: which CODEs the range actually touched |
| standalone | User asks to reverse-track, reconcile since checkpoint, or bootstrap OBS from code |

## Rationalization

| Thought | Reality |
|---|---|
| "Mint LABL — the crate is obviously that feature" | CODE only after human disposition via frame-change /map-features; this skill emits OBS ids |
| "Lead said sync specs to the code" | Code is evidence; Approved SHALLs need specify-behavior approval |
| "Add a CI drift workflow so teammates comply" | Zero-footprint: no consuming-repo automation |
| "Write `.skills/reconcile/` — close enough" | Only `.skills/reverse-features/`; other roots are recipe bugs |
| "Use OBS-LABL so promotion is obvious" | OBS id is `OBS-<6hex>` from evidence locators, never a proto-CODE |
| "Don't advance checkpoint while OBS pending" | Advance after active-shard index; pending stays queryable in active/ |
| "No specs dir — invent Approved requirements for the audit" | Brownfield bootstrap writes OBS only; configure-repo / frame-change come next |
| "GRAPH.md will help the PM browse" | No committed graph; catalog + local overlay only |
| "uncertain is basically no-spec-impact" | uncertain stays unresolved; never silent-clean |
| "Skip git diff — I already know the paths" | Pass 2 is mandatory; locators come from rename-aware inventory |

## Red Flags

- Creating Feature CODE / INDEX rows / requirements from this skill
- Writing under any overlay root other than `.skills/reverse-features/`
- OBS ids shaped like Feature CODEs (`OBS-LABL`, `OBS-DRFT`, …)
- Refusing checkpoint advance solely because findings are pending
- Adding `.github/workflows/**`, git hooks, or tracked reconciler scripts to the target
- Writing `GRAPH.md` or treating Graphify as required (deferred in rfeat-1.0)
- Calling the range clean while any finding is `uncertain` or `pending`
- Auto-invoking `/map-features` or `/configure-repo`

## Done when

Envelope printed with schema 1 / rfeat-1.0; findings classified by the pass
rules; overlay indexed (or explicit stateless); checkpoint advanced per passes.md
or explicitly null; no CODE mint; no specs write; no consuming-repo CI.
