---
name: map-features
version: 1.3.0
description: Confirm-then-write catalog mapping — dispose OBS/OWNS gaps, optionally export or materialize INDEX workbenches when Catalog sync is index-only.
disable-model-invocation: true
---

# Map Features

Brownfield / catalog SSOT ops for the feature-ID layer. Sibling of
`configure-repo` and `reconcile-features`: **propose → human confirm → additive
write only**.

Model-invoked skills that see mapping gaps MUST **name** `/map-features` for the
user and MUST NOT auto-invoke this skill.

Load `load-subgraph`’s `catalog-query.md` when emitting Domain / Recognized / OBS
rows — that file is the one home for mode detect and card fields. Overlay
tombstones follow `reconcile-features` layout (`tombstones.jsonl`); do not load
that file into chat. Export cell rules: `references/export-fields.md`.

## Preflight

Before any mode:

1. If `docs/specs/INDEX.md` is missing → **stop**. Name `/configure-repo` (seed
   INDEX). Do not invent an INDEX from chat memory.
2. Read `Catalog sync:` from `docs/agents/project.md` (Project posture).

| Value | Allowed modes |
|---|---|
| `index-only` | `dispose` · `export` · `materialize` |
| `full-triad` / `unset` / absent | `dispose` only |

Ask the user which mode to run when unclear. Never run `export` / `materialize`
unless Catalog sync is **`index-only`**.

| Mode | Direction | On confirm |
|---|---|---|
| **dispose** | OBS / brownfield gaps → catalog | Proposal kinds below |
| **export** | Local triad → INDEX | Refresh INDEX (± shard) cells per `export-fields.md` |
| **materialize** | INDEX CODE → local workbench | Draft stubs from `templates/triad-stub/` with fingerprint |

## Procedure — dispose (default)

1. Scan (do not write yet):
   - `docs/specs/` INDEX + requirements/tasks (and `docs/specs/catalog/` when
     sharded)
   - roadmap if present
   - optional high-churn paths
   - `.skills/reverse-features/active/*.md` + matching `observations/` when present
2. Build a proposal list of these kinds only:

   | Kind | Detect | On **confirm**, write |
   |---|---|---|
   | Missing Feature code | `requirements.md` lacks `Feature code:` but has a registry home | that file’s `Feature code:` line only |
   | Empty ROAD bind | INDEX Roadmap cell empty/`—` and a live `ROAD-N` is a candidate | INDEX cell only — **never invent** a new `ROAD-N` |
   | OWNS gap | significant path not in any feature’s denoised OWNS | a **Files edit proposal** for the owning feature’s `tasks.md` |
   | DEPENDS_ON candidate | `Reuse:` / `Interfaces: Consumes` naming another feature | optional Reuse **prose** after confirm — **never** a load-subgraph edge |
   | Domain boundary | Sharded router missing a domain; or user asks to add a domain | Sharded: router + shard stub. Flat: deferred |
   | Recognized capability | Spoken/INDEX CODE with no triad; or confirmed capability without requirements | Compact catalog card only. Never scaffold a triad in dispose |
   | OBS disposition | Pending/reopened `OBS-<6hex>` in active overlay | **promote** / **absorb** / **dismiss** + tombstone. Promote writes Recognized card |

3. **OBS provenance:** when proposing Recognized capability or OBS disposition,
   attach matching `observation_id` (and surface_roots) from active overlay /
   observation json when path/term overlap is clear. Prefer promote of an existing
   OBS over a free-floating Recognized row for the same surface.
4. **Batch confirm UX:** group proposals (e.g. Core / Integrations / Docs). Accept
   batch confirms like `Confirm P01-P06; decline P07-P15` or
   `Confirm batch Core`. Still require explicit CODE tokens on promote/absorb rows.
5. Present every proposal. Write **only** rows the user explicitly confirms.
6. MUST NOT write `docs/specs/GRAPH.md`. In **dispose**, MUST NOT create a triad.
7. If the scan finds nothing, say so and stop.

## Procedure — export (`index-only` only)

1. Confirm Catalog sync is `index-only`; else refuse and name `/configure-repo`.
2. For each CODE the user selects (or all with local triad):
   - Resolve Spec path from INDEX / shard.
   - Missing triad → gap (suggest `materialize`).
   - Propose cell updates per `references/export-fields.md` only.
3. Show before/after dry-run. Write confirmed cells only. Never stage triad files.

## Procedure — materialize (`index-only` only)

1. Confirm Catalog sync is `index-only`; else refuse and name `/configure-repo`.
2. Confirm gitignore includes `templates/gitignore-index-only.snippet` (or offer to
   append with yes). Warn: never `git add -f` triad dirs.
3. User picks INDEX CODE(s).
4. Resolve Spec dir under `docs/specs/`.
   - Missing dir → propose create stubs.
   - Existing files **without** `<!-- map-features-materialize-stub: v1 -->` →
     **refuse clobber** (list paths); ask user.
   - Existing files **only** stub-fingerprinted → may refresh stubs on confirm.
5. Propose `requirements.md` / `design.md` / `tasks.md` from `templates/triad-stub/`
   (CODE + title from INDEX, Status Draft, fingerprint comment).
6. On confirm: write. Remind: not Approved; `specify-behavior` before SHALLs.

## Rationalization

| Thought | Reality |
|---|---|
| "No INDEX — I'll write one from the proposal table now" | Preflight stop; `/configure-repo` seeds INDEX first |
| "I'll wire DEPENDS_ON into the subgraph now" | Proposals until confirmed prose; load-subgraph never reads them as edges |
| "Slug folder name is fine as the CODE" | CODE only from INDEX / Feature code: / confirmed row |
| "Confirm later, write now" | No write without explicit confirm |
| "OBS-5682de is obviously LABL" | Promote is a proposal; CODE confirmed per row |
| "Materialize even though Catalog sync is unset" | export/materialize require index-only |
| "Overwrite their half-written requirements" | Refuse without stub fingerprint |
| "git add -f the stubs" | Defeats index-only; refuse |

## Red Flags

- Writing without INDEX preflight / without per-row (or batch) confirm
- Inventing ROAD-N or unconfirmed CODE
- Scaffolding a triad in **dispose**
- export/materialize when Catalog sync ≠ `index-only`
- Clobbering non-stub triad files
- Leaving promoted OBS in `active/` without tombstone
- Writing `OBS-*` into a Code cell
- Inventing Approved EARS inside stubs

## Done when

Preflight passed; mode explicit; proposals shown (with OBS provenance when
available); only confirmed writes applied; stubs Draft + fingerprinted when
materialized; gaps listed.
