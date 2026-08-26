---
name: map-features
version: 1.1.1
description: Confirm-then-write brownfield backfill of feature IDs and catalog cards into specs.
disable-model-invocation: true
---

# Map Features

Brownfield SSOT backfill for the feature-ID / catalog layer. Sibling of
`configure-repo` and `scan-architecture`: **propose → human confirm → additive
write only**.

Model-invoked skills that see mapping gaps MUST **name** `/map-features` for the
user and MUST NOT auto-invoke this skill.

Load `load-subgraph`’s `catalog-query.md` when emitting Domain / Recognized / OBS
rows — that file is the one home for mode detect and card fields. Overlay
tombstones follow `reconcile-features` layout (`tombstones.jsonl`); do not load
that file into chat.

## Procedure

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
   | Recognized capability | Spoken/INDEX CODE with no triad; or a confirmed capability boundary without requirements yet | Compact catalog card only (grammar in `catalog-query.md`; Spec may be `—`). Never scaffold a triad. Do not write a second catalog row for a CODE that already exists |
   | OBS disposition | Pending/reopened `OBS-<6hex>` in active overlay; each row carries action `promote` \| `absorb` \| `dismiss` | **promote** → Recognized card + remove active + tombstone `promoted→CODE` on `tombstones.jsonl`; **absorb** → tombstone `absorbed→CODE` + remove active (OWNS Files stays a separate OWNS-gap proposal); **dismiss** → tombstone + remove active. Never write `OBS-*` into a Code cell |

3. Present every proposal. Write **only** rows the user explicitly confirms.
   Declined rows stay untouched. Promote and absorb confirms MUST include the
   exact CODE token on that row (suggestion allowed; silent invention forbidden).
   Dismiss does not take a CODE.
4. If CODE cannot be resolved and the user has not confirmed a CODE on that row,
   list it as a first-class gap. MUST NOT key the feature by directory slug in
   user-facing results.
5. MUST NOT write `docs/specs/GRAPH.md` or any graph projection.
6. MUST NOT create a full triad (requirements/design/tasks) from this skill —
   name `frame-change` / `specify-behavior` when normative SHALLs are needed.
7. If the scan finds nothing, say so and stop; do not invent kinds.

## Rationalization

| Thought | Reality |
|---|---|
| "I'll wire DEPENDS_ON into the subgraph now" | Candidates stay proposals until confirmed prose; load-subgraph never reads them as edges |
| "Slug folder name is fine as the CODE" | CODE only from INDEX / Feature code: / a CODE the user confirmed on that row |
| "Empty ROAD cell — mint ROAD-99" | Never invent ROAD-N; only bind to a live ID |
| "I'll just write owns: paths into design.md" | OWNS SSOT is tasks.md Files lines; propose a Files edit |
| "Confirm later, write now to save a turn" | No write without explicit confirm on that proposal |
| "OBS-5682de is obviously LABL — write INDEX now" | Promote is a proposal; CODE is confirmed per row; then card + tombstone |
| "Recognized means scaffold Draft requirements" | Card/INDEX only; triads are frame-change → specify-behavior |
| "Flat repo — invent a Domain router to look complete" | Domain writes only in sharded mode; flat defers sharding |

## Red Flags

- Auto-writing any proposal without a yes on that row
- Inventing ROAD-N, or writing a CODE the user did not confirm on that proposal
- Treating unconfirmed DEPENDS_ON as graph edges
- Writing GRAPH.md or a JSON edge store
- Silencing “can’t resolve CODE” by using a directory name
- Scaffolding a requirements/design/tasks triad from this skill
- Leaving a promoted OBS in `active/` without a tombstone on `tombstones.jsonl`
- Writing `OBS-*` into a canonical Code cell

## Done when

Every proposal was shown (or the scan found nothing); only confirmed rows written
additively; declined left intact; OBS dispositions tombstoned when confirmed;
remaining gaps listed for the user.
