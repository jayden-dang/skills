---
name: map-features
version: 1.3.1
description: Confirm-then-write feature catalog changes — dispose OBS gaps, or export/materialize when Catalog sync is index-only.
disable-model-invocation: true
---

# Map Features

Confirm-then-write ops for the feature catalog (`docs/specs/INDEX.md` ± shards).
Sibling of `configure-repo` and `reconcile-features`.

Model-invoked skills that see mapping gaps MUST **name** `/map-features` for the
user and MUST NOT auto-invoke this skill.

**Load when needed:** `load-subgraph`’s `catalog-query.md` (card grammar);
`references/export-fields.md` (export cells); `templates/` (stubs, gitignore).
Do not paste `tombstones.jsonl` into chat.

## Preflight

1. Missing `docs/specs/INDEX.md` → **stop**. Name `/configure-repo`. Do not invent INDEX.
2. Read `Catalog sync:` from `docs/agents/project.md`:

| Catalog sync | Modes allowed |
|---|---|
| `index-only` | `dispose` · `export` · `materialize` |
| `full-triad` / unset / absent | `dispose` only |

Ask which mode when unclear. Never run `export` / `materialize` unless sync is `index-only`.

## Mode recipes

### dispose (default)

Scan INDEX / tasks / roadmap / `.skills/reverse-features/active/` (+ observation
json when needed). Propose **only** these kinds:

| Kind | On confirm |
|---|---|
| Missing Feature code | `Feature code:` line in requirements |
| Empty ROAD bind | INDEX Roadmap cell → live `ROAD-N` only (never mint) |
| OWNS gap | `tasks.md` Files Create/Modify/Test line |
| DEPENDS_ON candidate | Reuse prose only — never a load-subgraph edge |
| Domain boundary | Sharded router + shard stub; flat = deferred |
| Recognized capability | Compact catalog card (Spec may be `—`); **no triad** |
| OBS disposition | promote / absorb / dismiss + tombstone; promote writes Recognized card |

**OBS provenance:** when path/term overlap is clear, attach `observation_id` (+
surface_roots). Prefer promoting that OBS over a free-floating Recognized row.

**Batch confirm:** group (Core / Integrations / Docs). Accept
`Confirm P01-P06; decline P07-P15` or `Confirm batch Core`. Promote/absorb rows
still need an explicit CODE token.

Write only confirmed rows. No `GRAPH.md`. No triad scaffold in dispose.

### export (`index-only`)

Refuse unless Catalog sync is `index-only` (name `/configure-repo`). For each
selected CODE with a local triad, propose INDEX/shard cell updates per
`references/export-fields.md`. Dry-run before/after. Never stage triad files.
Missing triad → gap; suggest `materialize`.

### materialize (`index-only`)

Refuse unless Catalog sync is `index-only`. Confirm or offer
`templates/gitignore-index-only.snippet`; warn against `git add -f`.

For each CODE, resolve Spec dir under `docs/specs/`:

- Missing → propose Draft stubs from `templates/triad-stub/`
- Files without `<!-- map-features-materialize-stub: v1 -->` → **refuse clobber**
- Stub-fingerprinted only → may refresh on confirm

Stubs: Status Draft, CODE + title from INDEX, no invented Approved EARS. After
write, name `specify-behavior` when SHALLs are needed.

## Rationalization

| Thought | Reality |
|---|---|
| "No INDEX — write one from my proposal table" | Preflight stop; `/configure-repo` seeds INDEX |
| "Slug folder is the CODE" | CODE from INDEX / Feature code: / confirmed row only |
| "Confirm later, write now" | No write without explicit confirm |
| "OBS-5682de is obviously LABL" | Promote proposes; CODE confirmed per row |
| "Materialize while Catalog sync is unset" | export/materialize require index-only |
| "Overwrite their half-written requirements" | Refuse without stub fingerprint |
| "git add -f the stubs" | Defeats index-only; refuse |
| "I'll auto-run map-features from reconcile" | User-invoked only; other skills name `/map-features` |

## Red Flags

- Skipping INDEX preflight or inventing INDEX
- Writing without per-row or batch confirm
- Inventing ROAD-N or unconfirmed CODE
- Scaffolding a triad in dispose
- export/materialize when Catalog sync ≠ `index-only`
- Clobbering non-stub triad files
- Leaving promoted OBS in `active/` without a tombstone
- Writing `OBS-*` into a Code cell
- Inventing Approved EARS in stubs

## Done when

Preflight passed; mode explicit; proposals shown (OBS provenance when available);
only confirmed writes applied; materialized stubs are Draft + fingerprinted;
gaps listed.
