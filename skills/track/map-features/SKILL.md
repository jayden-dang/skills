---
name: map-features
version: 1.1.0
description: Backfills Feature code lines, ROAD bindings, OWNS gaps,
  DEPENDS_ON candidates, domain boundaries, Recognized catalog cards, and OBS
  dispositions into SSOT after you confirm each proposal. Run with
  /map-features.
disable-model-invocation: true
---

# Map Features

Brownfield SSOT backfill for the feature-ID / catalog layer. Sibling of
`configure-repo` and `scan-architecture`: **propose → human confirm → additive
write only**.

Model-invoked skills that see mapping gaps MUST **name** `/map-features` for the
user and MUST NOT auto-invoke this skill (ARCH-5).

Catalog shape (flat vs sharded) and card grammar live in
`skills/execution/load-subgraph/references/catalog-query.md` — load it when
emitting Domain / Recognized / OBS rows.

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
   | Domain boundary | Sharded router missing a domain for a clear surface-root cluster; or user asks to add a domain | Router row + `docs/specs/catalog/<domain>.md` with empty feature-card table header if missing. **Flat INDEX:** no write — list as deferred optional shard (`catalog-query.md`) |
   | Recognized capability | Spoken/INDEX CODE with no triad; or a confirmed capability boundary without requirements yet | Compact catalog card only: flat INDEX row **or** shard card (Code, maturity/Status, one-line capability, match terms, 1–3 surface roots, Spec `—` if no triad). **Never** scaffold `requirements.md` / design / tasks |
   | OBS disposition | Pending/reopened `OBS-<6hex>` in active overlay | **promote** → Recognized card (same write as above) + remove active card + tombstone `promoted→CODE`; **absorb** → tombstone `absorbed→CODE` + remove active (OWNS Files stays a separate OWNS-gap proposal); **dismiss** → tombstone + remove active. Never mint CODE: the confirmed row must include the exact CODE string the user accepted |

3. Present every proposal. Write **only** rows the user explicitly confirms.
   Declined rows stay untouched. For Recognized / OBS promote, the confirm must
   include the **CODE token** (suggestion allowed; silent invention forbidden).
4. Unconfirmed DEPENDS_ON candidates MUST NOT become load-subgraph edges (that
   skill has no DEPENDS_ON pass).
5. If CODE cannot be resolved and the user has not confirmed a CODE on that row,
   list it as a first-class gap. MUST NOT key the feature by directory slug in
   user-facing results.
6. MUST NOT write `docs/specs/GRAPH.md` or any graph projection.
7. MUST NOT create a full triad (requirements/design/tasks) from this skill —
   name `frame-change` / `specify-behavior` when normative SHALLs are needed.

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
- Leaving a promoted OBS in `active/` without a tombstone

## Done when

Every proposal was shown; only confirmed rows written additively; declined left
intact; OBS dispositions tombstoned when confirmed; remaining gaps listed for
the user.
