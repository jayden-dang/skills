# `plan-milestones`

> Between the product vision and any single feature's spec sits the program layer: which milestones exist, in what order, holding which work — and which of them a human has actually committed to.

|  |  |
|---|---|
| **Bucket** | project |
| **Invocation** | model-invocable — fires on roadmap planning and on **any** edit to an existing roadmap |
| **Reads** | `templates/roadmap-INDEX.md`; `docs/product/vision.md` (`GOAL-N` citations); `docs/specs/INDEX.md` (work that already exists) |
| **Writes** | `docs/roadmap/INDEX.md` — nothing else |
| **Calls** | nothing |
| **Called by** | [`frame-change`](frame-change.md), when its step-5 decomposition names two or more independent sub-features |

## When it fires

Whenever milestones need planning, sequencing, or replanning — and equally on every change to a roadmap that already exists: dropping an item, reordering milestones, rewording an outcome, committing to the next milestone, recording a closure. A direct file edit to `docs/roadmap/INDEX.md` bypasses the gate that makes the roadmap a commitment rather than a draft, so those edits come through here.

## Intent, not progress

The one rule the whole skill turns on:

```
THE ROADMAP RECORDS INTENT. PROGRESS IS DERIVED, NEVER STORED HERE.
```

Intent is what nothing can work out for itself — the outcome a milestone promises, the order, its membership, what was deferred and why, and whether a human committed to it. Progress is already written once, as `Status:` in each feature's `requirements.md`, mirrored into its `docs/specs/INDEX.md` row.

So the roadmap carries no progress column, no per-milestone status field, no change log of transitions, and no percent-complete. A second copy of status drifts from the first, and once it drifts nobody can tell which is lying. [`status-roadmap`](status-roadmap.md) derives the live picture on demand instead.

`Commitment` — `Planned | Committed | Closed` — is kept, because *whether you have committed* is a human decision nobody can derive. That is a different thing from how far the work has got.

This was not an argument from taste. A baseline agent with no skill invented **two** progress stores unprompted: a `Status` column reusing `Draft → Approved → Implemented → Shipped` at milestone granularity, and a change log "as the mechanism for recording status changes over time". The rule exists because that is the default reflex.

## Three ID namespaces, three owners

| ID | Lives in | Owned by |
|---|---|---|
| `GOAL-N` | `docs/product/vision.md` | [`anchor-project`](anchor-project.md) |
| `MILE-N`, `ROAD-N` | `docs/roadmap/INDEX.md` | this skill |
| feature codes, `CODE-N.M` | `docs/specs/` | [`specify-behavior`](specify-behavior.md) |

A roadmap item is a `ROAD-N` plus a slug until a feature spec binds to it. This skill never writes a feature code and never touches `docs/specs/INDEX.md` — that file has exactly one registrar.

## Stability without immutability-by-decree

`MILE-N` and `ROAD-N` are stable from first definition, retired only by strikethrough with a reason. Two consequences worth stating plainly:

- **Order is table position; identity is the ID.** Moving Sharing ahead of Search reorders rows. It does not renumber anything.
- **An item you no longer want is deferred, not deleted.** It moves to its milestone's `Deferred:` slot with a date and a reason, because a deleted line takes its rationale with it.

Note that `ARCH-4` covers `CODE-N.M` and `ARCH-N` only. These namespaces are governed by the skill's own rules, not by that invariant — a deliberate choice, so planning IDs can be reshuffled while unstarted without breaking a repo-wide invariant.

## The approval gate

The skill validates the seven structural rules `S1`–`S7` carried in the template's comment block — the same set [`status-roadmap`](status-roadmap.md) re-checks as finding `R11`. Any defect is reported and the roadmap does not reach the user for approval. When clean, the whole file is presented and the skill stops; `Status: Approved` is written only after an explicit approval.

A material change to an already-approved roadmap — outcome, membership, ordering, commitment state, or goal citations — sets `Status: Draft` and re-enters that gate. An amended plan is a different plan.

## Two rules deliberately absent

Forward-dependency detection and surface-overlap consolidation were specified, tested, and **retired** — fresh baseline agents did both unprompted, so writing them in would have been no-op text. Forward dependencies are still caught structurally, by `S4` in the rule block and by `status-roadmap`'s `R11`. The `Surfaces:` slot stays, because it is the data that makes overlap visible; what went away is the instruction to reason about it.

## Optionality

The layer is optional and gates nothing. Route Worked to consult a roadmap that does not exist, the skill says so and offers to author one. The feature flow runs fully without it.

## See also

- [`status-roadmap`](status-roadmap.md) — derives where the plan stands; never writes
- [`anchor-project`](anchor-project.md) — the vision and `ARCH-N` spine above this layer
- [`frame-change`](frame-change.md) — hands its multi-subsystem decomposition here
