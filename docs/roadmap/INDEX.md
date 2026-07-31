# Roadmap: Skills

Status: Draft
Date: 2026-07-29

<!--
The program layer: milestone INTENT, above any single feature and below the product
vision. Optional — only multi-milestone projects need it. `plan-milestones` authors it;
`status-roadmap` derives progress from it without writing anything.

This file owns intent only: outcomes, ordering, membership, dependencies, commitments,
blockers, deferrals, goal dispositions. It never records how far a feature has got —
that lives once, as `Status:` in the feature's own requirements.md, mirrored into its
docs/specs/INDEX.md row. Every heading below is a REQUIRED slot — fill it or write
`None`.

Structural rules — AUTHORITATIVE. Both `plan-milestones` (before its approval gate) and
`status-roadmap` (as finding R11) validate against this list. A roadmap is structurally
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
| MILE-1 | Reviewable delivery | A multi-person team can review skill-set changes as risk-aware, story-sized PRs whose commits and PR description explain the change on their own | none | Planned |
| MILE-2 | Faithful history | A reviewer reads a history and an explainer that match how the work will actually integrate, whatever branch it targets and however messily it was committed | MILE-1 | Planned |

## MILE-1 — Reviewable delivery

**Outcome:** A multi-person team can review skill-set changes as risk-aware, story-sized PRs instead of one mega-branch — single-task work that touches risky paths gets a review prompt, multi-story features can be reviewed one user story at a time into the feature branch while the full triad stays intact, and every PR arrives with commits and a description that explain the change itself rather than naming an identifier the reviewer cannot resolve.
**Goals:** GOAL-1, GOAL-2, GOAL-3, GOAL-4, GOAL-5
**Members:**
- **ROAD-1** risk-glob-review-prompts — Surfaces: `skills/ship/land-branch/SKILL.md`, `skills/spec/plan-tasks/SKILL.md`, `templates/tasks.md`, `skills/spec/plan-tasks/TESTS.md`, `AGENTS.md`, `tests/unknowns/`, `docs/guide/skills/brief-team.md` (shared with ROAD-2: `skills/spec/plan-tasks/SKILL.md`, `templates/tasks.md`)
- **ROAD-2** story-derived-review-units — Surfaces: `skills/spec/specify-behavior/SKILL.md`, `skills/spec/plan-tasks/SKILL.md`, `skills/execution/build-story-units/SKILL.md`, `skills/execution/build-continuous/SKILL.md` (mode gate / write-handoff), `templates/requirements.md`, `templates/tasks.md` (shared with ROAD-1: `skills/spec/plan-tasks/SKILL.md`, `templates/tasks.md`)
- **ROAD-3** reviewer-facing-change-authoring — Surfaces: `skills/ship/package-change/`, `skills/ship/land-branch/SKILL.md`, `skills/execution/build-continuous/SKILL.md`, `skills/execution/build-story-units/SKILL.md`, `skills/execution/build-inline/SKILL.md`, `skills/setup/configure-repo/SKILL.md`, `templates/agents/project.md`, `docs/agents/project.md` (shared with ROAD-1: `skills/ship/land-branch/SKILL.md`; shared with ROAD-2: execute family)
**Depends-on:** none
**Commitment:** Planned
**Closed:** None
**Deferred:** None
**Blockers:** None

## MILE-2 — Faithful history

**Outcome:** A reviewer reads a history and an explainer that match how the work will actually integrate — a branch whose commits were made messily can be reshaped into the approved commit map on request, and an explainer packet describes the change against the branch the work merges into rather than the repository's default branch.
**Goals:** GOAL-1, GOAL-3
**Members:**
- **ROAD-4** gated-history-rewriting — Surfaces: `skills/ship/package-change/` (shared with ROAD-3)
- **ROAD-5** shared-base-resolution-for-explainers — Surfaces: `skills/review/brief-team/SKILL.md`, `docs/specs/2026-07-27-brief-team/`
- **ROAD-6** supersede-linkage-for-decision-records — Surfaces: `skills/ship/record-verdict/SKILL.md`, `skills/ship/record-verdict/RECORD.md`, `skills/ship/record-verdict/validate-records.sh`, `skills/ship/land-branch/SKILL.md`
**Depends-on:** MILE-1
**Commitment:** Planned
**Closed:** None
**Deferred:** None
**Blockers:** ROAD-4 is conditional on demonstrated demand for automated history rewriting; ROAD-5 requires a `realign-spec` pass because it edits a shipped, spec'd feature; ROAD-6 must teach-pack `record-verdict` to write both directions of `Supersedes:`/`Superseded-by:` in one publish, because its validator scans the whole decisions directory and a one-sided write fails the publish it belongs to.

## Goal dispositions

Every live `GOAL-N` in `docs/product/vision.md` that no milestone cites belongs here, so
that a goal is never silently dropped (S6).

| Goal | Disposition | Date | Reason |
|---|---|---|---|
| *(none — every live GOAL-N is cited by a milestone)* | | | |
