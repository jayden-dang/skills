---
name: write-roadmap
description: Use when a project's milestones need planning, sequencing, replanning, or
  ANY edit to an existing roadmap — produces or revises docs/roadmap/INDEX.md, the
  milestone intent registry carrying stable MILE-N and ROAD-N IDs that later
  feature specs bind to. Triggers on "plan the milestones", "build a roadmap",
  "what order should we build this in", "break this project into milestones", and
  on a brainstorm that decomposed work into several independent sub-features —
  and equally on every change to a roadmap that already exists, such as "update
  the roadmap", "drop this item", "we're not doing X anymore", "reorder the
  milestones", "move sharing ahead of search", "reword this outcome", "commit to
  the next milestone", "this milestone shipped", or any request that edits
  docs/roadmap/INDEX.md. Not for one feature's requirements
  (write-requirements), and not for reporting where the plan currently stands
  (check-roadmap).
---

# Write Roadmap

Author and maintain `docs/roadmap/INDEX.md` — the program layer between the product
vision and any single feature's spec. It answers *which milestones exist, in what order,
holding which work, and which of them we have actually committed to.*

**Where this sits:** `establish-project` (vision) → **`write-roadmap`** (milestones) →
`brainstorm` → `write-requirements` → … A roadmap item becomes a feature when
`write-requirements` registers a code for it; this skill never registers one.

## The Iron Law

```
THE ROADMAP RECORDS INTENT. PROGRESS IS DERIVED, NEVER STORED HERE.
```

Intent is what no tool can work out for itself: the outcome a milestone promises, the
order, what belongs to it, what was deferred and why, and whether a human has committed
to it. Progress is already written down once — as `Status:` in each feature's own
`requirements.md`, mirrored into its `docs/specs/INDEX.md` row.

So this file gets **no** progress column, **no** per-milestone status field, **no** change
log of status transitions, and **no** percentage complete. A second copy of status drifts
from the first, and the moment it drifts nobody can tell which one is lying. `/check-roadmap`
derives the current picture on demand from the specs and git.

`Commitment` is not progress. `Planned | Committed | Closed` records a *human decision*
— nobody can derive whether you have committed to a milestone. Keep it; keep nothing that
tracks how far the work has got.

## Modes

Pick by what exists. Ask only if genuinely unclear.

- **create** — no `docs/roadmap/INDEX.md`. Author it.
- **update** — it exists. Revise it against a change signal.

Templates resolve as `${CLAUDE_PLUGIN_ROOT}/templates` when installed as a plugin, else
`../../../templates` relative to this file. Every heading in `templates/roadmap-INDEX.md`
is a REQUIRED slot — fill it or write `None`. Its comment block carries the authoritative
structural rules **S1–S7** and the ID rules; read them there rather than restating them.

## Create

1. **Read the inputs.** `docs/product/vision.md` when it exists — its `**GOAL-N**` IDs are
   what milestones cite. `docs/specs/INDEX.md` for features that already exist (a
   brownfield project's shipped work belongs in an early milestone, not nowhere). The
   decomposition you were handed, if you came from `brainstorm`.
   *Done when: you can name the goals in play and the work already shipped.*
2. **Fill the template** to `docs/roadmap/INDEX.md`. One `MILE-N` per milestone; one
   `ROAD-N` per item, under exactly one milestone, identified by ID and slug.
   *Done when: every REQUIRED slot is filled or reads `None`.*
3. **Group by user value.** A milestone's `Outcome:` is one sentence naming what a person
   can do once it lands — testable by a reader who has not seen the code. A milestone whose
   outcome can only be phrased as work performed ("the storage layer is rewritten") is a
   technical layer, not a milestone: fold it into the milestone whose outcome it enables.
   Prefer fewer and larger milestones when the design is settled; split where early
   feedback could redirect what follows.
   *Done when: every milestone has an outcome a reader could test it against.*
4. **Cite goals.** WHERE `docs/product/vision.md` exists, each milestone's `Goals:` names
   the live `GOAL-N` IDs it serves, and every live goal no milestone cites is recorded under
   `## Goal dispositions` as `Deferred` or `Out-of-scope` with a date and a reason. WHERE no
   vision exists, write `Goals: None` and leave the dispositions table empty.
   *Done when: no live goal is unaccounted for, or there is no vision.*
5. **Declare surfaces.** Each item's `Surfaces:` names the components or paths it is
   expected to touch, or `None` with a reason when the surface is not yet knowable.
   *Done when: every item has a surface line.*
6. Run **## The approval gate**.

## Update

The change signal is a new milestone, a reordering, a scope change, a commitment, a
closure, or an item that is no longer wanted.

**Every ID already in the file is permanent.** Reordering the milestone table changes the
order; it changes no ID. An item that moves to another milestone keeps its `ROAD-N`. Retire
an ID only by strikethrough with a reason — `~~**ROAD-4**~~ dropped 2026-07-25: no custom
search UI` — so the history stays readable and no future reference dangles.

**An item you no longer want is deferred, not deleted.** It moves to its milestone's
`Deferred:` slot with a date and a reason. Deleting the line destroys the one record that
the option was ever considered, which is exactly what a reader six months later needs.

**A material change to an `Approved` roadmap demotes it.** Set `Status: Draft`, then run
the gate again. Material means: any milestone's outcome, membership, ordering, commitment
state, or goal citations. Presenting edited content under an `Approved` stamp tells every
later reader that a version nobody approved was approved.

**Record a closure.** When a milestone's commitment becomes `Closed`, write the release tag
or commit into its `Closed:` slot — that marker is how a later reader resolves what shipped
in it.

*Done when: the change is applied, no ID moved or vanished, and the gate has run.*

## The approval gate

<HARD-GATE>
Validate S1–S7 from the template's rule block. Report every defect you find and STOP —
a roadmap with a structural defect does not reach the user for approval. When the file is
clean, present it WHOLE and STOP. `Status: Approved` is written only after the user has
explicitly approved it. Conversational agreement is not approval; a roadmap you approved
yourself was never approved.
</HARD-GATE>

Walk S1–S7 as a checklist, naming each defect and where it sits. Then present the file and
stop. On approval, set `Status: Approved` and tell the user that `/check-roadmap` reports
where the plan stands whenever they want it.

**Done when:** the S1–S7 walk is clean, the user has approved the written file, and
`Status:` reads `Approved`.

## What this skill never writes

`docs/specs/INDEX.md` belongs to `write-requirements`, which is the sole registrar of
feature codes. A roadmap item is a `ROAD-N` and a slug until a feature spec binds to it —
so the roadmap carries no feature codes, and this skill leaves that file untouched.

## Rationalizations

Every row below is a verbatim rationalization from a baseline run, or its direct echo.

| Thought | Reality |
|---|---|
| "A status column would make this trackable" | It makes it *stale*. Feature progress lives in `requirements.md` `Status:`, mirrored into the INDEX row. `/check-roadmap` derives the rest |
| "I'll add a change log so status history survives" | That is the same second copy wearing a different hat. Git already holds the history of this file |
| "Reuse the feature lifecycle at milestone granularity" | `Draft → Approved → Implemented → Shipped` describes a *spec*. A milestone carries a commitment, not a lifecycle |
| "Sharing matters more now, so it should be MILE-2" | Order is table position; identity is the ID. Move the row, keep the number |
| "I renumbered so the order reads naturally" | Every renumber silently repoints anything that cited the old number |
| "We are not doing it, so remove the line" | Defer it with a date and a reason. A deleted item takes its rationale with it |
| "It is a planning artifact, so no approval gate applies" | The gate is what makes the roadmap a commitment rather than a draft someone wrote. It applies |
| "The user is the approver and they asked for this edit, so it stays Approved" | They asked for the *edit*, not for the result to be pre-approved. Demote to `Draft` and show them what they now own |
| "I signed off two weeks ago, this is just an amendment" | An amended plan is a different plan. It gets its own approval |
| "No template exists here, so I'll invent a shape" | `templates/roadmap-INDEX.md` is the shape. Two invented shapes cannot be checked by one rule set |

## Red flags — stop

- You are about to add a column, field, or section that records how far work has got
- You are about to change a number that already exists in the file
- You are about to delete a line naming an item rather than deferring it
- You are about to write `Status: Approved` without the user having said so in this session
- You are about to write a feature code into the roadmap
- A milestone's outcome describes work performed rather than something a person can do

## No-op

If asked to consult a roadmap when `docs/roadmap/INDEX.md` does not exist, say the project
has no roadmap layer and that this skill can author one — then stop. The layer is optional;
the feature flow works fully without it, and nothing here is a gate on that flow.
