# RED baselines — RMAP roadmap layer

Recorded per the `writing-skills` Iron Law: no new skill and no edit to a skill ships
without a failing test first, and the failures must be **observed**, not guessed.

**IDs in this file are baseline records, not coverage.** It is Trace-ignored.

## Method

Three baseline agents, each given a realistic user request and no roadmap skill.

**First run was contaminated and is discarded for two of three agents.** The spec triad
(`docs/specs/2026-07-25-roadmap/`) and `templates/roadmap-INDEX.md` had already been
committed, so agents A and C read them off disk and complied — agent C cited RMAP-1.11,
RMAP-1.17 and RMAP-1.19 by ID. That measures compliance, not baseline behavior. Only
agent B was usable, because it never consulted the spec.

**Re-run** against a sanitized copy of the repo with `docs/specs/`, `tests/`, and
`templates/roadmap-INDEX.md` removed. Verified by `grep -rl 'RMAP-\|MILE-\|ROAD-\|roadmap-INDEX'`
returning nothing before dispatch.

| Agent | Request | Environment |
|---|---|---|
| A | Author a roadmap for a note app from four work items plus two stated dependencies | sanitized |
| B | Review and finalize a hand-written draft roadmap containing a forward dependency and a surface repeated across three milestones | scratchpad, never read the spec |
| C | Apply three material changes to an already-approved roadmap | sanitized |

## Confirmed failures

### RMAP-1.1 — no durable, conventional home

B wrote the roadmap to a scratchpad temp directory. A invented
`docs/product/roadmap.md`, reasoning that the product-docs layer "holds only those two
files — a roadmap is an addition to that layer". Two agents, two different locations,
neither reproducible.

### RMAP-1.2 — no testable outcome; commitment conflated with progress

A's table columns were `ID | Milestone | Depends on | Status | Notes`. No milestone
carried an outcome sentence a reader could test it against, and there was no commitment
state distinct from progress.

### RMAP-1.7 — a dropped item is deleted, not deferred

C, asked to drop one item:

> "item-4: removed entirely. […] `item-4 search-ui` was deleted along with its
> separating comma; no other reference to item-4 existed in the file."

No date, no reason, no record that the item ever existed.

### RMAP-1.11 / RMAP-1.12 — renumbering under reorder

B, after moving a milestone earlier:

> "I renumbered so Storage rework runs second (right after Capture), pushing Search and
> Sharing to third and fourth"

C did **not** fail this — it kept `M1`/`M2`/`M3` and moved only row position, reasoning
from "AGENTS.md ID rule, applied here by analogy". One of two baselines failed, so the
rule is load-bearing but not universally missing.

### RMAP-1.17 — no approval gate

All three agents finalized without stopping. A's rationalization, verbatim:

> "nothing in this doc modifies shipped product behavior, code, or other files — it is a
> new, standalone planning artifact the user asked for directly, so none of this repo's
> approval gates (which govern requirements/code changes) apply."

### RMAP-1.19 — `Approved` survives a material change

C left `Status: Approved` untouched after dropping a member, reordering milestones, and
rewriting an outcome sentence. Verbatim rationalization:

> "you are the approving stakeholder and you are the one directing this exact edit right
> now, in real time — this isn't drift or a third party's unilateral change to an
> approved artifact, it's you exercising your own approval authority to amend it."

This is the sharpest rationalization in the set and needs an explicit counter.

### RMAP-1.20 — no surface declaration

Neither A nor B recorded which components or paths a milestone's items would touch, so
nothing existed for a consolidation check to run against.

### Decision 1 (derive, never store) — the strongest failure

A invented **two** roadmap-level progress stores unprompted:

> "Status values — Reuses this repo's existing feature-status vocabulary (Draft →
> Approved → Implemented → Shipped) at milestone granularity"

and

> "Added a `Change log` section (dated bullet entries […]) as the mechanism for recording
> status changes over time"

Left alone, an agent rebuilds exactly the duplicated, drift-prone status store the design
rejects. This validates the derive-not-store decision empirically rather than by argument.

## No failure observed — candidate no-ops

### RMAP-1.5 — forward dependency

B caught it unprompted, first finding, correctly diagnosed:

> "Milestone 2 (Search) is scheduled before Milestone 3 (Storage rework) even though
> Search's own 'Needs' column names Storage rework as a prerequisite — a direct ordering
> violation."

### RMAP-1.6 — surface-overlap consolidation

B caught the repeated surface unprompted and consolidated it:

> "'rework note model' is repeated as a task line under three separate milestones […]
> even though it is the actual deliverable of Storage rework alone — redundant/duplicated
> work."

A independently did the same thing while authoring, elevating the shared storage rework
into its own milestone rather than duplicating it under two dependents.

Both behaviors appeared without any skill. Per `writing-skills`, text with no failure
behind it is a no-op.

**Ruled 2026-07-25: both retired by strikethrough** in `requirements.md`, with this file
as the stated evidence. Neither rule is written into `write-roadmap`. What survives:
forward dependencies are still caught structurally by S4 in the template rule block, the
authoring gate (RMAP-1.18), and `check-roadmap`'s R11; the `Surfaces:` slot is retained by
RMAP-1.20 because it is the input that makes overlap visible — the retired part is the
instruction to reason about it, not the data.
