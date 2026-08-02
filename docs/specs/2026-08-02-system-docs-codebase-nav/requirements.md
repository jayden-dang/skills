# Requirements: System-docs codebase navigation

Feature code: SDCN
Status: Implemented
Date: 2026-08-02
Roadmap item: ROAD-8

<!-- Extends SDOC platform. IDs freeze on approval. -->

## 1. First-class codebase navigation entries

**Story:** As a skill-set author, I want `codebase/modules`, `codebase/ownership`, and `codebase/dependencies` to be First-class catalog entries, so that agents can author and consult module boundaries, ownership, and dependency direction.

- **SDCN-1.1** THE SYSTEM SHALL ship skill-local templates and structural validators under `skills/project/define-system-doc/templates/codebase/` and `validators/codebase/` for entry keys `codebase/modules`, `codebase/ownership`, and `codebase/dependencies`.
- **SDCN-1.2** THE SYSTEM SHALL mark each of those three keys `First-class` in `CATALOG.md` only when SDOC First-class package evidence holds (entry package, template, validator, writer `define-system-doc`, ≥1 named reader with full reader tests a–d, guide coverage).
- **SDCN-1.3** THE SYSTEM SHALL use the same consumer authority pattern as `codebase/map` for each single-file entry: **Approved** means canonical file has `Status: Approved` and that entry's structural validator returns pass; otherwise Absent or Non-authoritative.
- **SDCN-1.4** Canonical consumer paths SHALL be `docs/codebase/modules.md`, `docs/codebase/ownership.md`, and `docs/codebase/dependencies.md` respectively.
- **SDCN-1.5** Structural validators SHALL be deterministic (required headings/slots, tables or `None — <reason>`, no unresolved blockers, no forbidden placeholders TBD/TODO/.../lorem, Status Approved for write readiness) and SHALL NOT claim semantic understanding of prose.
- **SDCN-1.6** THE SYSTEM SHALL CONTINUE TO keep `codebase/map` First-class and the Hybrid 1A inventory set of 36 keys unchanged (no added/removed inventory keys).

## 2. Author via define-system-doc

**Story:** As a skill-mediated actor, I want `/define-system-doc codebase/modules|ownership|dependencies` to run the existing one-artifact workflow, so that I can produce Approved navigation docs without a separate author skill.

- **SDCN-2.1** WHEN the actor invokes `/define-system-doc` with one of `codebase/modules`, `codebase/ownership`, or `codebase/dependencies` THE SYSTEM SHALL apply the define-system-doc procedure (bounded resolve, ephemera, evidence grades, structural validate, explicit approve, canonical write only).
- **SDCN-2.2** THE SYSTEM SHALL NOT create empty sibling navigation files when authoring one entry.
- **SDCN-2.3** (guard) WHEN authoring these entries THE SYSTEM SHALL CONTINUE TO enforce SDOC no-mediated-Draft, non-SSOT proposal, and targeted-patch rules.

## 3. plan-tasks consults navigation docs

**Story:** As a skill-mediated actor planning work, I want plan-tasks to consult Approved modules/ownership/dependencies when applicable, so that File Structure respects module and dependency rules.

- **SDCN-3.1** WHEN plan-tasks is writing File Structure and an Approved authoritative `docs/codebase/modules.md` is available THE SYSTEM SHALL consult it for module boundary placement guidance within hard constraints.
- **SDCN-3.2** WHEN plan-tasks is writing File Structure and an Approved authoritative `docs/codebase/dependencies.md` is available THE SYSTEM SHALL consult it so planned paths do not propose forbidden dependency directions within hard constraints.
- **SDCN-3.3** WHEN plan-tasks is writing File Structure and an Approved authoritative `docs/codebase/ownership.md` is available THE SYSTEM SHALL consult it for ownership notes in packaging language when Team band uses ownership (and otherwise may record ownership as advisory prose).
- **SDCN-3.4** WHERE any of those docs is absent or non-authoritative THE SYSTEM SHALL CONTINUE without failing solely for that absence (no-op).
- **SDCN-3.5** WHEN placement or dependency direction is materially uncertain because a relevant navigation doc is not authoritative THE SYSTEM SHALL suggest at most once per entry key per plan-tasks run the exact `/define-system-doc <entry-key>` action, never auto-invoke, suppress after decline for the rest of the run.
- **SDCN-3.6** Hard constraints (approved requirements/design, ARCH-N, standing project constraints) SHALL outrank navigation docs; on conflict surface, preserve hard constraint, suggest map/nav update via define-system-doc, never auto-invoke.
- **SDCN-3.7** (guard) WHEN only `codebase/map` is relevant THE SYSTEM SHALL CONTINUE TO apply existing SDOC plan-tasks Codebase Map rules.

## 4. design-solution consults navigation docs

**Story:** As a skill-mediated actor designing a feature, I want design-solution to consult Approved modules/ownership/dependencies when the design names modules or cross-boundary calls, so that Locality and Reuse respect standing navigation docs.

- **SDCN-4.1** WHEN design-solution is writing Architecture sections and an Approved authoritative modules or dependencies doc is available and the design names cross-module structure THE SYSTEM SHALL consult the applicable doc(s) within hard constraints.
- **SDCN-4.2** WHERE those docs are absent or non-authoritative THE SYSTEM SHALL CONTINUE design-solution without failing solely for that absence.
- **SDCN-4.3** WHEN module/dependency structure is material and the relevant doc is not authoritative THE SYSTEM SHALL suggest at most once per entry key per design-solution run `/define-system-doc <entry-key>`, never auto-invoke.
- **SDCN-4.4** THE SYSTEM SHALL list `design-solution` as a reader only for entries that gain this consult hook, with full reader tests (applicability, authoritative consult, no-op, suggestion).

## 5. inspect-change consults navigation docs

**Story:** As a skill-mediated actor reviewing a diff, I want inspect-change to consult Approved ownership/dependencies/modules when paths in the diff relate to those docs, so that Spec/Standards review can flag placement or dependency violations against standing rules.

- **SDCN-5.1** WHEN inspect-change is reviewing a diff and an Approved authoritative navigation doc is available and diff paths intersect its stated modules/ownership/dependency surface THE SYSTEM SHALL surface the doc as Spec/Standards context (advisory findings if the diff conflicts with documented rules, within hard constraints).
- **SDCN-5.2** WHERE docs are absent or non-authoritative THE SYSTEM SHALL CONTINUE inspect-change without failing solely for that absence.
- **SDCN-5.3** THE SYSTEM SHALL NEVER auto-invoke define-system-doc from inspect-change; optional suggestion at most once per entry key per inspect-change run when a conflict with missing nav doc would help.
- **SDCN-5.4** THE SYSTEM SHALL list `inspect-change` as a reader only with full reader tests.

## 6. Guide coverage

**Story:** As a human adopter, I want the system-docs guide to cover the three navigation entries, so that I know when to author them.

- **SDCN-6.1** THE SYSTEM SHALL update `docs/guide/concepts/system-docs.md` to describe modules, ownership, and dependencies First-class entries, canonical paths, and which skills consult them.
- **SDCN-6.2** Pack tests SHALL fail if the guide claims First-class for a row that is not First-class in CATALOG, or references unknown entry keys.

## 7. Quality attributes

**Section-kind:** nfr

**Story:** As a stakeholder, I want quality targets for navigation docs.

- **Performance:** None — documentation skills.
- **Security:** **SDCN-7.1** THE SYSTEM SHALL NOT treat ownership docs as access-control enforcement — they are documentation for agents/humans; verified by skill text stating advisory nature.
- **Reliability:** **SDCN-7.2** WHEN First-class is claimed THE SYSTEM SHALL fail pack tests if package evidence is incomplete (same completeness bar as SDOC-1.7).
- **Accessibility:** None — markdown docs.

## 8. Guards

| Area | Guard |
|---|---|
| define-system-doc | **SDCN-8.1** (guard) WHEN extending entries THE SYSTEM SHALL CONTINUE TO author exactly one artifact per invocation and keep skill-local catalog resolution. |
| plan-tasks map | **SDCN-8.2** (guard) WHEN adding nav consults THE SYSTEM SHALL CONTINUE TO honor Codebase Map consult rules from SDOC. |
| Hybrid inventory | **SDCN-8.3** (guard) THE SYSTEM SHALL CONTINUE TO list exactly 36 Hybrid 1A keys. |
| audit-trace TB/SLO | **SDCN-8.4** (guard) THE SYSTEM SHALL CONTINUE TO leave TB/THR/CMP/SLO audit-trace undelivered in this feature. |

## Out of Scope

- Security, standards, ops, product extensions First-class (later ROADs)
- Changing define-system-doc into multi-artifact authoring
- Enforcing ownership as CODEOWNERS generation (optional mention only)
- Semantic validators
- TB/THR/CMP/SLO IDs

## Open Questions

None.
