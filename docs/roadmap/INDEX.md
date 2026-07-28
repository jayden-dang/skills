# Roadmap: Skills

Status: Approved
Date: 2026-07-28

<!--
The program layer: milestone INTENT, above any single feature and below the product
vision. Optional — only multi-milestone projects need it. `write-roadmap` authors it;
`check-roadmap` derives progress from it without writing anything.

This file owns intent only: outcomes, ordering, membership, dependencies, commitments,
blockers, deferrals, goal dispositions. It never records how far a feature has got —
that lives once, as `Status:` in the feature's own requirements.md, mirrored into its
docs/specs/INDEX.md row. Every heading below is a REQUIRED slot — fill it or write
`None`.

Structural rules — AUTHORITATIVE. Both `write-roadmap` (before its approval gate) and
`check-roadmap` (as finding R11) validate against this list. A roadmap is structurally
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
| MILE-1 | Reviewable delivery | A multi-person team can review skill-set changes as risk-aware, story-sized PRs instead of one mega-branch | none | Planned |

## MILE-1 — Reviewable delivery

**Outcome:** A multi-person team can review skill-set changes as risk-aware, story-sized PRs instead of one mega-branch — single-task work that touches risky paths gets a review prompt, and multi-story features can be reviewed one user story at a time into the feature branch while the full triad stays intact.
**Goals:** GOAL-1, GOAL-2, GOAL-3, GOAL-5
**Members:**
- **ROAD-1** risk-glob-review-prompts — Surfaces: `skills/ship/finish-branch/SKILL.md`, `skills/spec/write-plan/SKILL.md`, `templates/tasks.md`, `skills/spec/write-plan/TESTS.md`, `AGENTS.md`, `tests/unknowns/`, `docs/guide/skills/explain-change.md` (shared with ROAD-2: `skills/spec/write-plan/SKILL.md`, `templates/tasks.md`)
- **ROAD-2** story-derived-review-units — Surfaces: `skills/spec/write-requirements/SKILL.md`, `skills/spec/write-plan/SKILL.md`, `skills/execution/execute-plan/SKILL.md`, `templates/requirements.md`, `templates/tasks.md` (shared with ROAD-1: `skills/spec/write-plan/SKILL.md`, `templates/tasks.md`)
**Depends-on:** none
**Commitment:** Planned
**Closed:** None
**Deferred:** None
**Blockers:** None

## Goal dispositions

Every live `GOAL-N` in `docs/product/vision.md` that no milestone cites belongs here, so
that a goal is never silently dropped (S6).

| Goal | Disposition | Date | Reason |
|---|---|---|---|
| GOAL-4 | Deferred | 2026-07-28 | setup-repo already shipped; this milestone deliberately adds no consumer-repo config (project-level mode default was rejected) |
