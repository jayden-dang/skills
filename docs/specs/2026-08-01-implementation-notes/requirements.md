# Requirements: Mid-build implementation notes

Feature code: IMPN
Status: Implemented
Date: 2026-08-01

## 1. Classified deviation log during execute

**Story:** As a developer or controller watching an agent implement an approved plan, I want every territory-forced change logged with why it changed and what kind of unknown it was, so that good requirements/design/tasks stay the map while mid-build surprises are still visible and reviewable.

- **IMPN-1.1** WHEN an implementer (or build-inline controller) hits a territory fact that forces a different approach than the task brief or plan THE SYSTEM SHALL append one entry to `.skills/<CODE>/implementation-notes.md` before finishing that task, using the field set in IMPN-1.2.
- **IMPN-1.2** WHEN a deviation entry is written THE SYSTEM SHALL include all of these fields (each non-empty): **Task**, **Unknown class**, **Map said**, **Territory showed**, **Deviation**, **Cause**, **Choice**, **Map impact**, **Revisit**.
- **IMPN-1.3** WHEN **Unknown class** is set THE SYSTEM SHALL use exactly one of: `known-unknown` · `unknown-known` · `unknown-unknown` · `assumption-break` · `blindspot`.
- **IMPN-1.4** WHEN **Map impact** is set THE SYSTEM SHALL use exactly one of: `none` · `revisit-only` · `reroute-plan` · `realign-spec`.
- **IMPN-1.5** WHEN writing a deviation entry THE SYSTEM SHALL prefer a conservative choice that preserves existing behavior and keeps blast radius inside the task's files, and SHALL record that choice under **Choice**.
- **IMPN-1.6** WHEN a deviation falsifies the approved plan, design, or requirements (or requires changing a shared public contract outside the task) THE SYSTEM SHALL set **Map impact** to `reroute-plan` or `realign-spec` as fits, SHALL NOT silently stretch the brief, and SHALL stop for `reroute-plan` (or human escalation) rather than only logging and continuing as if the map were intact.
- **IMPN-1.7** WHEN a task finishes with a plan/territory mismatch THE SYSTEM SHALL treat a report or status that claims concerns or deviations without citing `.skills/<CODE>/implementation-notes.md` as incomplete (controller MUST re-dispatch or fix before accepting DONE_WITH_CONCERNS / complete).

## 2. Same contract on every execute route

**Story:** As a user who picks build-in-waves, build-by-story, or build-inline, I want the same implementation-notes contract so route choice does not drop mid-build learning.

- **IMPN-2.1** WHEN `build-in-waves` or `build-by-story` dispatches an implementer THE SYSTEM SHALL require the implementer prompt's Deviations section to prescribe the field set in IMPN-1.2 (not the legacy five-field-only shape without Unknown class / Map said / Territory showed / Map impact).
- **IMPN-2.2** WHEN `build-inline` runs a task THE SYSTEM SHALL require the controller Deviations step to use the same field set as IMPN-1.2.
- **IMPN-2.3** THE SYSTEM SHALL CONTINUE TO keep a single notes file per feature at `.skills/<CODE>/implementation-notes.md` (SKNS path grammar) and SHALL NOT invent a second mid-build unknowns file parallel to it.

## 3. Surface notes after the build

**Story:** As a human resuming, packaging, or landing a branch, I want to see that mid-build deviations exist and which ones need map attention, so that surprises are not buried in chat.

- **IMPN-3.1** WHEN `write-handoff` runs and `.skills/<CODE>/implementation-notes.md` has one or more deviation entries THE SYSTEM SHALL include the notes path and a one-line summary that includes the count of entries whose **Map impact** is not `none` (or state zero non-none if all are `none`).
- **IMPN-3.2** WHEN `package-change` authors reviewer-facing package text and notes exist with any **Map impact** other than `none` THE SYSTEM SHALL mention the notes path once as authority for mid-build why (without dumping the full file into the PR body).
- **IMPN-3.3** WHEN `land-branch` runs and notes exist THE SYSTEM SHALL CONTINUE TO mention the notes path once when deviations are present, and SHALL mention when any entry has **Map impact** of `reroute-plan` or `realign-spec` still unresolved (human judgment — not auto-block if the user already accepted).

## 4. Guards — discovery knowns and Iron Laws

**Story:** As a maintainer of the unknowns loop, I want mid-build notes to complement discovery knowns without replacing them or weakening gates.

- **IMPN-4.1** (guard) WHEN frame-change / clarify-decisions write knowns inventories THE SYSTEM SHALL CONTINUE TO own pre-implementation known knowns / known unknowns / unknown knowns / assumptions / blindspot — implementation-notes SHALL NOT replace that inventory.
- **IMPN-4.2** (guard) WHEN a deviation is logged with **Map impact** `none` or `revisit-only` THE SYSTEM SHALL CONTINUE TO leave approved requirements/design/tasks text unchanged unless the user later runs realign-spec or amend-feature.
- **IMPN-4.3** (guard) WHEN execute family runs THE SYSTEM SHALL CONTINUE TO require test-first, prove-claim, and no silent production shortcuts — implementation-notes logging is additive, not a substitute for TDD or for stopping on blockers.
- **IMPN-4.4** (guard) WHEN SKNS path grammar applies THE SYSTEM SHALL CONTINUE TO write notes under `.skills/<CODE>/implementation-notes.md` only.

Touched surfaces for guard scan:

| Surface | Outcome |
|---|---|
| `skills/execution/build-in-waves/implementer-prompt.md` | field set upgrade (IMPN-2.1) |
| `skills/execution/build-in-waves/SKILL.md`, `build-by-story/SKILL.md` | DONE_WITH_CONCERNS + notes incomplete rule (IMPN-1.7) |
| `skills/execution/build-inline/SKILL.md` | Deviations step field set (IMPN-2.2) |
| `skills/execution/build-in-waves/TESTS.md` | pressure scenarios for new fields |
| `skills/track/write-handoff/SKILL.md` | IMPN-3.1 |
| `skills/ship/package-change/SKILL.md`, `land-branch/SKILL.md` | IMPN-3.2–3.3 |
| `templates/skills-ephemera-paths.md` | optional basename note for notes fields (docs only) |
| Discovery knowns skills | unchanged (IMPN-4.1) |

## 5. Quality attributes

**Section-kind:** nfr

**Story:** As a stakeholder, I want measurable quality targets for this feature, so that how-well is not left implicit.

- **Performance:** None — markdown append only.
- **Security:** None — git-ignored local ephemera only.
- **Reliability:** **IMPN-5.1** WHEN two deviations are logged for different tasks THE SYSTEM SHALL keep them as separate entries in the same notes file (append-only; no overwrite of prior entries) — verified by source contract and scenario pressure.
- **Accessibility:** None — no human-facing UI.

## Out of Scope

- Auto-rewriting approved `requirements.md` / `design.md` / `tasks.md` from notes.
- A second mid-build file (e.g. `unknowns.md`) parallel to implementation-notes.
- Changing discovery knowns inventory field names or clarify-decisions card taxonomy.
- HTML implementation-notes (markdown only for this feature).
- Blocking land-branch hard-fail solely on open revisit entries (surface only).
- Personal OS paths.

## Open Questions

None — locked close package 2026-08-01 (map/territory mid-build notes).
