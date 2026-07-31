# Roadmap: <Project Name>

Status: Draft
Date: <YYYY-MM-DD>

<!--
The program layer: milestone INTENT, above any single feature and below the product
vision. Optional — only multi-milestone projects need it. `plan-milestones` authors it;
`refresh-roadmap-status` derives progress from it without writing anything.

This file owns intent only: outcomes, ordering, membership, dependencies, commitments,
blockers, deferrals, goal dispositions. It never records how far a feature has got —
that lives once, as `Status:` in the feature's own requirements.md, mirrored into its
docs/specs/INDEX.md row. Every heading below is a REQUIRED slot — fill it or write
`None`.

Structural rules — AUTHORITATIVE. Both `plan-milestones` (before its approval gate) and
`refresh-roadmap-status` (as finding R11) validate against this list. A roadmap is structurally
defective when any of these does not hold:

  S1  every MILE-N and ROAD-N is defined exactly once
  S2  every ROAD-N sits under exactly one milestone
  S3  every milestone carries a non-empty Outcome sentence
  S4  no Depends-on names a milestone appearing later in the milestone table
  S5  every Depends-on resolves to exactly one live, non-struck-through MILE-N
  S6  every live GOAL-N in vision.md is cited by a milestone or listed under
      Goal dispositions
  S7  the milestone table and every milestone block parse

ID rules:
- Grammar: **MILE-<n>** and **ROAD-<n>**, flat and repo-wide.
- Stable from first definition. Retire by strikethrough with a reason
  (~~**MILE-3**~~ superseded by MILE-5) — never renumber, never reuse.
- A ROAD-N keeps its ID when it moves between milestones.
- Milestone ORDER is table row order; milestone IDENTITY is the MILE-N. Reordering the
  table never renumbers anything.
- ITEM order is list position within a milestone's Members, and it carries the build
  order: an item is buildable once the items above it are done. Same rule as milestones —
  order is position, identity is the ID, so resequencing members renumbers nothing.
- GOAL-N is defined in docs/product/vision.md and only cited here. Feature codes are
  defined in docs/specs/INDEX.md and never written here — a roadmap item is identified
  by its ROAD-N and slug until a feature spec binds to it.
-->

| ID | Milestone | Outcome | Depends-on | Commitment |
|---|---|---|---|---|
| MILE-1 | <name> | <one testable user-value sentence> | none | Committed |
| MILE-2 | <name> | <one testable user-value sentence> | MILE-1 | Planned |

## MILE-1 — <name>

**Outcome:** <one sentence a reader could test the milestone against — what a user can
do once it lands, not what was built>
**Goals:** GOAL-1, GOAL-2
**Members:**
- **ROAD-1** <slug> — Surfaces: `src/<area>/`, `src/<file>.ts`
- **ROAD-2** <slug> — Surfaces: None — <reason the surface is not yet knowable>
**Depends-on:** none
**Commitment:** Committed <YYYY-MM-DD>
**Closed:** None
**Deferred:** None
**Blockers:** None

## MILE-2 — <name>

**Outcome:** <one testable user-value sentence>
**Goals:** GOAL-3
**Members:**
- **ROAD-3** <slug> — Surfaces: `src/<area>/`
**Depends-on:** MILE-1
**Commitment:** Planned
**Closed:** None
**Deferred:** <ROAD-N slug → MILE-N (YYYY-MM-DD, reason)>
**Blockers:** None

## Goal dispositions

Every live `GOAL-N` in `docs/product/vision.md` that no milestone cites belongs here, so
that a goal is never silently dropped (S6).

| Goal | Disposition | Date | Reason |
|---|---|---|---|
| GOAL-4 | Out-of-scope | <YYYY-MM-DD> | <why this goal is not being pursued> |
| GOAL-5 | Deferred | <YYYY-MM-DD> | <what has to be true before it returns> |
