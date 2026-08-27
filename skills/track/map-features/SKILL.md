---
name: map-features
version: 1.2.0
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
that file into chat.

## Modes

Read `Catalog sync:` from `docs/agents/project.md` (Project posture):

| Value | Allowed modes |
|---|---|
| `index-only` | `dispose` · `export` · `materialize` |
| `full-triad` / `unset` / absent | `dispose` only |

Ask the user which mode to run when unclear. Never run `export` / `materialize`
unless Catalog sync is **`index-only`**.

| Mode | Direction | On confirm |
|---|---|---|
| **dispose** | OBS / brownfield gaps → catalog | Existing proposal kinds (below) |
| **export** | Local triad → INDEX | Refresh INDEX (± shard) **row fields** from local triad (title/status/path/surface roots when present) — **never** commit triad; never invent CODE/ROAD |
| **materialize** | INDEX CODE → local workbench | Create Draft stub triad at the INDEX Spec path using `templates/triad-stub/` — only if dir missing or user confirms overwrite of empty stubs |

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
   | OWNS gap | significant path not in any feature’s denoised OWNS | a **Files edit proposal** for the owning feature’s `tasks.md` (Create/Modify/Test line). Do **not** invent freeform “owns:” prose as SSOT |
   | DEPENDS_ON candidate | `Reuse:` / `Interfaces: Consumes` naming another feature | optional design.md or tasks Reuse **prose** after confirm — **never** a load-subgraph edge |
   | Domain boundary | Sharded router missing a domain for a clear surface-root cluster; or user asks to add a domain | Sharded: router row + shard stub per `catalog-query.md`. Flat: no write; list as deferred optional shard |
   | Recognized capability | Spoken/INDEX CODE with no triad; or a confirmed capability boundary without requirements yet | Compact catalog card only (grammar in `catalog-query.md`; Spec may be `—`). Never scaffold a triad in **dispose**. Do not write a second catalog row for a CODE that already exists |
   | OBS disposition | Pending/reopened `OBS-<6hex>` in active overlay; each row carries action `promote` \| `absorb` \| `dismiss` | **promote** → Recognized card + remove active + tombstone `promoted→CODE` on `tombstones.jsonl`; **absorb** → tombstone `absorbed→CODE` + remove active (OWNS Files stays a separate OWNS-gap proposal); **dismiss** → tombstone + remove active. Never write `OBS-*` into a Code cell |

3. Present every proposal. Write **only** rows the user explicitly confirms.
   Declined rows stay untouched. Promote and absorb confirms MUST include the
   exact CODE token on that row (suggestion allowed; silent invention forbidden).
   Dismiss does not take a CODE.
4. If CODE cannot be resolved and the user has not confirmed a CODE on that row,
   list it as a first-class gap. MUST NOT key the feature by directory slug in
   user-facing results.
5. MUST NOT write `docs/specs/GRAPH.md` or any graph projection.
6. In **dispose**, MUST NOT create a full triad — name `frame-change` /
   `specify-behavior` when normative SHALLs are needed. (**materialize** is the
   only mode that may create Draft stubs — see below.)
7. If the scan finds nothing, say so and stop; do not invent kinds.

## Procedure — export (`index-only` only)

1. Confirm Catalog sync is `index-only`; else refuse and name `/configure-repo`.
2. For each CODE the user selects (or “all with local triad present”):
   - Resolve Spec path from INDEX / shard card.
   - If local triad missing → list as gap (suggest `materialize`), do not invent.
   - Propose INDEX/shard field updates derived only from local files (title,
     status if Draft/Approved/Implemented/Shipped is explicit, Spec path,
     surface roots from tasks Files when clearly stable prefixes).
3. Show the diff proposal. Write only confirmed cells. Never stage triad files.

## Procedure — materialize (`index-only` only)

1. Confirm Catalog sync is `index-only`; else refuse and name `/configure-repo`.
2. Confirm `.gitignore` includes the index-only snippet (or offer to append
   `templates/gitignore-index-only.snippet` with explicit yes). Warn: never
   `git add -f` triad dirs.
3. User picks one or more INDEX CODEs.
4. For each CODE: resolve Spec dir relative to `docs/specs/`. If the directory
   already has non-stub content, refuse or ask — do not clobber.
5. Propose creating `requirements.md` / `design.md` / `tasks.md` from
   `templates/triad-stub/`, substituting CODE + title from INDEX, **Status: Draft**.
6. On confirm only: write stubs. Remind: not Approved; run `specify-behavior`
   before binding SHALLs. Do not invent EARS acceptance criteria.

## Rationalization

| Thought | Reality |
|---|---|
| "I'll wire DEPENDS_ON into the subgraph now" | Candidates stay proposals until confirmed prose; load-subgraph never reads them as edges |
| "Slug folder name is fine as the CODE" | CODE only from INDEX / Feature code: / a CODE the user confirmed on that row |
| "Empty ROAD cell — mint ROAD-99" | Never invent ROAD-N; only bind to a live ID |
| "I'll just write owns: paths into design.md" | OWNS SSOT is tasks.md Files lines; propose a Files edit |
| "Confirm later, write now to save a turn" | No write without explicit confirm on that proposal |
| "OBS-5682de is obviously LABL — write INDEX now" | Promote is a proposal; CODE is confirmed per row; then card + tombstone |
| "Recognized means scaffold Draft requirements" | In dispose: card/INDEX only. Stubs only in materialize under index-only |
| "Flat repo — invent a Domain router to look complete" | Domain writes only in sharded mode; flat defers sharding |
| "Materialize even though Catalog sync is unset" | export/materialize require index-only; otherwise dispose-only |
| "git add -f the stubs so CI sees them" | Defeats index-only; refuse and warn |

## Red Flags

- Auto-writing any proposal without a yes on that row
- Inventing ROAD-N, or writing a CODE the user did not confirm on that proposal
- Treating unconfirmed DEPENDS_ON as graph edges
- Writing GRAPH.md or a JSON edge store
- Silencing “can’t resolve CODE” by using a directory name
- Scaffolding a triad in **dispose** mode
- Running **export** / **materialize** when Catalog sync is not `index-only`
- Leaving a promoted OBS in `active/` without a tombstone on `tombstones.jsonl`
- Writing `OBS-*` into a canonical Code cell
- Inventing Approved EARS inside materialize stubs

## Done when

Mode was explicit; every proposal was shown (or the scan found nothing); only
confirmed rows written additively; declined left intact; OBS dispositions
tombstoned when confirmed; materialize stubs are Draft-only; remaining gaps
listed for the user.
