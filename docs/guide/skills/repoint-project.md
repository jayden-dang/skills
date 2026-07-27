# `repoint-project`

> When product intent changes and shipped code no longer matches, produce a
> disposition ledger before anyone rewrites the vision layer.

|  |  |
|---|---|
| **Bucket** | project |
| **Invocation** | `/repoint-project` (user-invoked; `disable-model-invocation: true`) |
| **Reads** | `docs/product/vision.md`, `docs/architecture/`, `docs/specs/INDEX.md`, shipped feature requirements, the code they name |
| **Writes** | `docs/product/pivot-ledger.md` (or `.skills/pivot-ledger.md`) only |
| **Calls** | names `/establish-project` (update) after confirmation; never invokes user-invoked skills |
| **Called by** | nobody auto — offered by `establish-project` update when a pivot collides with shipped reality; named by `correct-course` on Vision-level rewinds with collisions |

## When it fires

A decided (or proposed) product pivot — new goals, users, non-goals, or
invariants — that **contradicts** at least one shipped/Implemented feature, live
`GOAL-N`, live `ARCH-N`, or hard constraint. Not for pure wording edits, not for
vision-neutral refactors (`improve-architecture`), not for "make the spec match
the code" (`sync-spec`), not for mid-plan invalidation alone (`correct-course`).

## Iron Law

No `vision.md` or `architecture/` rewrite for a pivot until every contradicted
shipped feature and live `ARCH-N` has a **user-confirmed** disposition in the
ledger. Deadlines change *when* you report, never *what must be true* first.

## The ledger

Each row: candidate (feature / goal / invariant / non-goal), disposition
(Keep / Adapt / Retire / Deprecate / Freeze / Carve out / Accept debt / Unknown),
entrenchment (shipped? schema? API? one-way door?), rationale. Proposed rows are
agent-authored; confirmed rows are decisions.

## What it deliberately does not do

- Does not write `docs/product/vision.md` or `docs/architecture/**` —
  `/establish-project` owns those files
- Does not challenge "whether to pivot" as a hard gate (models already do that
  without skill text — verified RED S2)
- Does not restate how to sunset a feature (models already refuse bare-delete —
  verified RED S3)

## See also

- [`establish-project`](establish-project.md) — sole writer of the vision layer
- [`improve-architecture`](improve-architecture.md) — vision-neutral deepening
- [`sync-spec`](sync-spec.md) — code is truth → fix the triad
- [`correct-course`](correct-course.md) — mid-flight plan invalidation router
