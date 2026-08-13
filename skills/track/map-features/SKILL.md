---
name: map-features
version: 1.0.0
description: Backfills Feature code lines, ROAD bindings, OWNS gaps, and
  DEPENDS_ON candidates into SSOT after you confirm each proposal. Run with
  /map-features.
disable-model-invocation: true
---

# Map Features

Brownfield SSOT backfill for the feature-ID layer. Sibling of `configure-repo`
and `scan-architecture`: **propose → human confirm → additive write only**.

Model-invoked skills that see mapping gaps MUST **name** `/map-features` for the
user and MUST NOT auto-invoke this skill (ARCH-5).

## Procedure

1. Scan `docs/specs/` (INDEX + requirements/tasks), roadmap if present, optional
   high-churn paths. Do not write yet.
2. Build a proposal list of these kinds only:

   | Kind | Detect | On **confirm**, write |
   |---|---|---|
   | Missing Feature code | `requirements.md` lacks `Feature code:` but has a registry home | that file’s `Feature code:` line only |
   | Empty ROAD bind | INDEX Roadmap cell empty/`—` and a live `ROAD-N` is a candidate | INDEX cell only — **never invent** a new `ROAD-N` |
   | OWNS gap | significant path not in any feature’s denoised OWNS | a **Files edit proposal** for the owning feature’s `tasks.md` (Create/Modify/Test line). Do **not** invent freeform “owns:” prose as SSOT |
   | DEPENDS_ON candidate | `Reuse:` / `Interfaces: Consumes` naming another feature | optional design.md or tasks Reuse **prose** after confirm — **never** a load-subgraph edge |

3. Present every proposal. Write **only** rows the user explicitly confirms.
   Declined rows stay untouched.
4. Unconfirmed DEPENDS_ON candidates MUST NOT become load-subgraph edges (that
   skill has no DEPENDS_ON pass).
5. If CODE cannot be resolved from INDEX or `Feature code:`, list it as a
   first-class gap. MUST NOT key the feature by directory slug in user-facing
   results.
6. MUST NOT write `docs/specs/GRAPH.md` or any graph projection.

## Rationalization

| Thought | Reality |
|---|---|
| "I'll wire DEPENDS_ON into the subgraph now" | Candidates stay proposals until confirmed prose; load-subgraph never reads them as edges |
| "Slug folder name is fine as the CODE" | CODE only from INDEX / Feature code:; otherwise report a gap |
| "Empty ROAD cell — mint ROAD-99" | Never invent ROAD-N; only bind to a live ID |
| "I'll just write owns: paths into design.md" | OWNS SSOT is tasks.md Files lines; propose a Files edit |
| "Confirm later, write now to save a turn" | No write without explicit confirm on that proposal |

## Red Flags

- Auto-writing any proposal without a yes on that row
- Inventing ROAD-N or CODE values
- Treating unconfirmed DEPENDS_ON as graph edges
- Writing GRAPH.md or a JSON edge store
- Silencing “can’t resolve CODE” by using a directory name

## Done when

Every proposal was shown; only confirmed rows written additively; declined left
intact; remaining gaps listed for the user.
