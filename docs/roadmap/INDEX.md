# Roadmap: Skills

Status: Approved
Date: 2026-08-02

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
| MILE-3 | System documentation model | An adopter can discover, author, and have skills consult optional Hybrid 1A system docs (product, architecture, codebase, security, standards, ops) without empty-forest setup, invented standing facts, or fake skill readers | none | Closed |
| MILE-1 | Reviewable delivery | A multi-person team can review skill-set changes as risk-aware, story-sized PRs whose commits and PR description explain the change on their own | none | Planned |
| MILE-2 | Faithful history | A reviewer reads a history and an explainer that match how the work will actually integrate, whatever branch it targets and however messily it was committed | MILE-1 | Planned |

## MILE-3 — System documentation model

**Outcome:** An adopter can discover, author, and have skills consult optional Hybrid 1A system docs (product, architecture, codebase, security, standards, ops) without empty-forest setup, invented standing facts, or fake skill readers — and every Hybrid 1A catalog row is First-class before this milestone is complete.
**Goals:** GOAL-1, GOAL-2, GOAL-3, GOAL-4, GOAL-5
**Members:**
- **ROAD-7** system-docs-core-codebase-map — Surfaces: `skills/project/define-system-doc/SKILL.md`, `skills/project/define-system-doc/catalog/CATALOG.md`, `skills/project/define-system-doc/catalog/entries/codebase/map.md`, `skills/project/define-system-doc/templates/codebase/map.md`, `skills/project/define-system-doc/validators/codebase/map.md`, `templates/skills-ephemera-paths.md`, `docs/guide/concepts/system-docs.md`, `docs/architecture/artifacts.md`, `skills/spec/plan-tasks/SKILL.md`, `AGENTS.md`, pack tests under `tests/` for catalog/guide sync and codebase/map workflow contracts; packaging baseline for skill-local resources vs documented root-templates fallback
- **ROAD-8** system-docs-codebase-navigation — Surfaces: `skills/project/define-system-doc/catalog/entries/codebase/modules.md`, `skills/project/define-system-doc/catalog/entries/codebase/ownership.md`, `skills/project/define-system-doc/catalog/entries/codebase/dependencies.md`, `skills/project/define-system-doc/templates/codebase/`, `skills/project/define-system-doc/validators/codebase/`, `skills/spec/design-solution/SKILL.md`, `skills/spec/plan-tasks/SKILL.md`, `skills/review/inspect-change/SKILL.md`, pack tests under `tests/`
- **ROAD-9** system-docs-product-context — Surfaces: `skills/project/define-project/SKILL.md`, `skills/project/define-system-doc/catalog/entries/product/personas.md`, `skills/project/define-system-doc/catalog/entries/product/metrics.md`, `skills/project/define-system-doc/catalog/entries/product/principles.md`, `skills/project/define-system-doc/templates/product/`, `skills/project/define-system-doc/validators/product/`, `skills/discovery/frame-change/SKILL.md`, `skills/acceptance/validate-feature/SKILL.md`, `docs/guide/concepts/system-docs.md`, pack tests under `tests/`
- **ROAD-10** system-docs-architecture-shape — Surfaces: `skills/project/define-project/SKILL.md`, `skills/project/define-system-doc/catalog/entries/architecture/system.md`, `skills/project/define-system-doc/catalog/entries/architecture/data.md`, `skills/project/define-system-doc/catalog/entries/architecture/integrations.md`, `skills/project/define-system-doc/catalog/entries/architecture/runtime.md`, `skills/project/define-system-doc/templates/architecture/`, `skills/project/define-system-doc/validators/architecture/`, `skills/spec/design-solution/SKILL.md`, `docs/architecture/INDEX.md` (spine ownership remains define-project), pack tests under `tests/`
- **ROAD-11** system-docs-standards-core — Surfaces: `skills/project/define-system-doc/catalog/entries/standards/INDEX.md`, `skills/project/define-system-doc/catalog/entries/standards/testing.md`, `skills/project/define-system-doc/catalog/entries/standards/errors-logging.md`, `skills/project/define-system-doc/templates/standards/`, `skills/project/define-system-doc/validators/standards/`, `skills/project/define-project/SKILL.md` (guidelines migration: legacy fallback only until migrated; pointer only afterward; never a parallel SSOT with `docs/standards/`), `skills/spec/plan-tasks/SKILL.md`, `skills/execution/test-first/SKILL.md`, `skills/review/inspect-change/SKILL.md`, pack tests under `tests/`
- **ROAD-12** system-docs-surface-standards — Surfaces: `skills/project/define-system-doc/catalog/entries/standards/api.md`, `skills/project/define-system-doc/catalog/entries/standards/ui.md`, `skills/project/define-system-doc/catalog/entries/standards/accessibility.md`, `skills/project/define-system-doc/catalog/entries/standards/security-coding.md`, `skills/project/define-system-doc/catalog/entries/standards/observability.md`, `skills/project/define-system-doc/templates/standards/`, `skills/project/define-system-doc/validators/standards/`, `skills/spec/design-solution/SKILL.md`, `skills/spec/plan-tasks/SKILL.md`, `skills/acceptance/validate-api/SKILL.md`, `skills/acceptance/validate-ui/SKILL.md`, `skills/review/inspect-change/SKILL.md`, pack tests under `tests/`
- **ROAD-13** system-docs-security-trace — Surfaces: `skills/project/define-system-doc/catalog/entries/security/threat-model.md`, `skills/project/define-system-doc/catalog/entries/security/posture.md`, `skills/project/define-system-doc/catalog/entries/security/compliance.md`, `skills/project/define-system-doc/templates/security/`, `skills/project/define-system-doc/validators/security/`, `skills/spec/design-solution/SKILL.md`, `skills/execution/audit-trace/SKILL.md`, pack tests under `tests/` for `TB-N`/`THR-N`/`CMP-N` definition extraction and `Security:` citation integrity
- **ROAD-14** system-docs-operations-reliability — Surfaces: `skills/project/define-system-doc/catalog/entries/ops/deployment.md`, `skills/project/define-system-doc/catalog/entries/ops/reliability.md`, `skills/project/define-system-doc/catalog/entries/ops/observability.md`, `skills/project/define-system-doc/catalog/entries/ops/disaster-recovery.md`, `skills/project/define-system-doc/catalog/entries/ops/runbooks.md`, `skills/project/define-system-doc/templates/ops/`, `skills/project/define-system-doc/validators/ops/`, `skills/execution/root-cause/SKILL.md`, `skills/ship/cut-release/SKILL.md`, `skills/execution/audit-trace/SKILL.md`, pack tests under `tests/` for `SLO-N` definition extraction and `Reliability:` citation integrity
**Depends-on:** none
**Commitment:** Closed
**Closed:** 38240cd91d039ff12dc11c42bb6e37bca7006eda
**Deferred:** None
**Blockers:** ROAD-7 must investigate the observed flat-install root-templates fallback gap (skill-local siblings present; documented root templates path not reachable); repair in ROAD-7 if small and in-scope, otherwise replan. Existing-artifact First-class baseline defects discovered during ROAD-7 are replanned explicitly, not pre-invented as repair items. Milestone completion criteria (full Hybrid 1A First-class coverage, real-reader verification, catalog/guide sync, clean system-ID audits) are verified through `/assess-milestone`, not a separate audit-only ROAD.

## MILE-1 — Reviewable delivery

**Outcome:** A multi-person team can review skill-set changes as risk-aware, story-sized PRs instead of one mega-branch — single-task work that touches risky paths gets a review prompt, multi-story features can be reviewed one user story at a time into the feature branch while the full triad stays intact, and every PR arrives with commits and a description that explain the change itself rather than naming an identifier the reviewer cannot resolve.
**Goals:** GOAL-1, GOAL-2, GOAL-3, GOAL-4, GOAL-5
**Members:**
- **ROAD-1** risk-glob-review-prompts — Surfaces: `skills/ship/land-branch/SKILL.md`, `skills/spec/plan-tasks/SKILL.md`, `templates/tasks.md`, `skills/spec/plan-tasks/TESTS.md`, `AGENTS.md`, `tests/unknowns/`, `docs/guide/skills/brief-team.md` (shared with ROAD-2: `skills/spec/plan-tasks/SKILL.md`, `templates/tasks.md`)
- **ROAD-2** story-derived-review-units — Surfaces: `skills/spec/specify-behavior/SKILL.md`, `skills/spec/plan-tasks/SKILL.md`, `skills/execution/build-by-story/SKILL.md`, `skills/execution/build-in-waves/SKILL.md` (mode gate / write-handoff), `templates/requirements.md`, `templates/tasks.md` (shared with ROAD-1: `skills/spec/plan-tasks/SKILL.md`, `templates/tasks.md`)
- **ROAD-3** reviewer-facing-change-authoring — Surfaces: `skills/ship/package-change/`, `skills/ship/land-branch/SKILL.md`, `skills/execution/build-in-waves/SKILL.md`, `skills/execution/build-by-story/SKILL.md`, `skills/execution/build-inline/SKILL.md`, `skills/setup/configure-repo/SKILL.md`, `templates/agents/project.md`, `docs/agents/project.md` (shared with ROAD-1: `skills/ship/land-branch/SKILL.md`; shared with ROAD-2: execute family)
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
