# Requirements: Milestone assessment

Feature code: ASSESS
Status: Implemented
Date: 2026-07-26

Adds the semantic half of the milestone close. `refresh-roadmap-status` reports whether a
milestone's structure is sound; `assess-milestone` judges whether its **outcome** was
achieved, records that judgment durably, and gates the close on an explicit human
disposition.

**Namespaces this feature consumes.** `MILE-N` and `ROAD-N` (owned by `plan-milestones`),
`GOAL-N` (owned by `define-project` via `vision.md`), feature codes and `CODE-N.M`
(owned by `specify-behavior`). It introduces no new ID namespace: an assessment is
identified by its milestone and its ordinal within that milestone's file.

**Ownership split.** `docs/roadmap/INDEX.md` keeps owning planning intent and is written
only by `plan-milestones`. `docs/roadmap/assessments/<MILE-N>.md` owns outcome truth and is
written only by `assess-milestone`. Neither writes into the other's artifact. Recorded in
[ADR 0002](../../adr/0002-outcome-truth-outside-the-roadmap.md).

**Reconciles with RMAP.** RMAP's Out-of-Scope section reserved this work under the name
`retrospective` and excluded four things this feature now includes: judging whether a
milestone outcome was achieved, consuming attention residue, routing findings by concern,
and the `Closed` marker's use as a resolved git range. It also excluded a *team-ceremony*
retrospective and an action-item bucket — both of which stay excluded here. That reconciling
note was written into RMAP's Out-of-Scope section on 2026-07-26, dated and in place.

## 1. Resolve the assessment scope from artifacts

**Story:** As a developer preparing to close a milestone, I want the assessment's scope and
evidence rebuilt from tracked artifacts rather than session memory, so that the verdict
rests on what the repo records and not on what a conversation happens to remember.

- **ASSESS-1.1** WHERE `docs/roadmap/INDEX.md` does not exist THE SYSTEM SHALL report that no milestone scope exists and exit without writing a file or producing a verdict.
- **ASSESS-1.2** WHEN `assess-milestone` runs and `docs/roadmap/INDEX.md` exists THE SYSTEM SHALL resolve the target milestone to exactly one live, non-struck-through `MILE-N`.
- **ASSESS-1.3** IF the target milestone does not resolve to exactly one live `MILE-N` THEN THE SYSTEM SHALL report the ambiguity and withhold the outcome verdict.
- **ASSESS-1.4** WHEN a milestone is resolved THE SYSTEM SHALL derive its membership as the live `ROAD-N` items recorded under it that its `Deferred:` slot does not list.
- **ASSESS-1.5** WHEN membership is derived THE SYSTEM SHALL resolve each member to exactly one feature code bound to it in `docs/specs/INDEX.md`.
- **ASSESS-1.6** IF a member resolves to no feature code, or to more than one, THEN THE SYSTEM SHALL report the unresolved binding and withhold the outcome verdict.
- **ASSESS-1.7** WHEN a member's `ROAD-N` has moved between milestones since it was created THE SYSTEM SHALL resolve its binding by that unchanged ID.
- **ASSESS-1.8** WHEN a milestone is resolved THE SYSTEM SHALL resolve its committed baseline as the full SHA of the single commit that introduced that milestone's current `Committed` state into `docs/roadmap/INDEX.md`.
- **ASSESS-1.9** WHEN a milestone is resolved THE SYSTEM SHALL resolve exactly one candidate closing revision, expressed as a full commit SHA, and hold it immutable for the remainder of the invocation.
- **ASSESS-1.10** IF the committed baseline does not resolve to exactly one commit, or the candidate closing revision does not resolve to exactly one commit, THEN THE SYSTEM SHALL report the failure and withhold the outcome verdict.
- **ASSESS-1.11** WHEN a milestone is resolved THE SYSTEM SHALL evaluate the shared roadmap structural rules over it before assessing its outcome.
- **ASSESS-1.12** IF a structural rule that withholds `refresh-roadmap-status`'s next-action recommendation fires for the resolved milestone THEN THE SYSTEM SHALL report that finding and withhold the outcome verdict.

## 2. Record the assessment as an append-only artifact

**Story:** As a developer returning to a project months later, I want every milestone
judgment preserved with its evidence and its attributions intact, so that what was decided,
on what basis, and by whom survives the conversation that produced it.

- **ASSESS-2.1** WHEN an assessment is produced THE SYSTEM SHALL record it in `docs/roadmap/assessments/<MILE-N>.md`, creating that file when it does not exist.
- **ASSESS-2.2** THE SYSTEM SHALL record each assessment as a distinct `Assessment <N>` block holding the committed baseline, the candidate closing revision, the roadmap revision assessed, the evidence gathered, and the agent's verdict.
- **ASSESS-2.3** WHEN a further assessment is appended THE SYSTEM SHALL leave every earlier `Assessment` block byte-identical.
- **ASSESS-2.4** WHEN a further assessment is appended THE SYSTEM SHALL record `Supersedes: Assessment <N-1>` and the reason for reassessment in the new block.
- **ASSESS-2.5** THE SYSTEM SHALL append a further assessment only when the requested closing revision differs from the recorded candidate closing revision, or when material evidence has changed since the previous assessment.
- **ASSESS-2.6** WHEN a close completes successfully THE SYSTEM SHALL leave the assessment file unchanged.
- **ASSESS-2.7** WHEN an assessment is written THE SYSTEM SHALL record its `Human disposition` as `Pending`.
- **ASSESS-2.8** WHEN a human disposition arrives for an assessment whose recorded candidate closing revision equals the requested closing revision THE SYSTEM SHALL record that disposition against that same assessment block.
- **ASSESS-2.9** WHILE an assessment's current `Human disposition` holds a terminal value THE SYSTEM SHALL reject any further disposition recorded against that assessment.
- **ASSESS-2.10** IF a disposition or a close is requested against a closing revision that differs from the recorded candidate closing revision THEN THE SYSTEM SHALL report the recorded assessment superseded and require a new `Assessment` block.
- **ASSESS-2.11** THE SYSTEM SHALL record the agent's verdict and rationale under `Agent assessment`, and the human's action and rationale under `Human disposition`, attributed separately.
- **ASSESS-2.12** WHEN a human overrides the agent's verdict THE SYSTEM SHALL leave the `Agent assessment` unchanged and record the replacement verdict under `Human disposition`.
- **ASSESS-2.13** WHERE the human supplies a rationale THE SYSTEM SHALL record that rationale verbatim.
- **ASSESS-2.14** THE SYSTEM SHALL record every `Human disposition` value as exactly one of `Pending`, `Deferred`, `Accepted`, or `Overridden`.
- **ASSESS-2.15** THE SYSTEM SHALL treat `Pending` and `Deferred` as non-terminal dispositions and `Accepted` and `Overridden` as terminal dispositions.
- **ASSESS-2.16** WHEN a disposition value is recorded THE SYSTEM SHALL append it to that assessment block's dated disposition history, leaving earlier entries unchanged, and take the latest entry as the current disposition.
- **ASSESS-2.17** WHILE an assessment's recorded candidate closing revision equals the requested closing revision THE SYSTEM SHALL treat that assessment as valid, whatever commits have landed since it was written.

## 3. Judge the milestone against its recorded intent

**Story:** As a developer closing a milestone, I want the outcome judged against the intent
that was written down, with the evidence named, so that "delivered" means something a later
reader can check rather than something a model asserted.

- **ASSESS-3.1** WHEN a milestone is assessed THE SYSTEM SHALL judge its `Outcome:` sentence as achieved or not achieved and record the evidence the judgment rests on.
- **ASSESS-3.2** WHEN a milestone is assessed THE SYSTEM SHALL judge, for each `GOAL-N` it cites that resolves to exactly one live, non-struck-through goal, whether that goal advanced, and record the evidence for each.
- **ASSESS-3.3** WHEN a milestone is assessed THE SYSTEM SHALL judge, for each item its `Deferred:` slot lists, whether the recorded date and reason name a real deferral with a destination, and report each that does not.
- ~~**ASSESS-3.4**~~ retired 2026-07-26: false premise. It read "WHERE an allocation … exists", implying a discoverable artifact, but `select-review-sample` persists none by default — `skills/review/select-review-sample/SKILL.md:38` ends its run with "no file exists unless they asked for one". Superseded by ASSESS-3.11.
- ~~**ASSESS-3.5**~~ retired 2026-07-26: same false premise as ASSESS-3.4. Superseded by ASSESS-3.12.
- **ASSESS-3.6** WHEN a milestone is assessed THE SYSTEM SHALL record the counts of roadmap items added to, moved out of, and deferred from it between its committed baseline and its candidate closing revision, and the elapsed time between those two points.
- **ASSESS-3.7** THE SYSTEM SHALL record the ASSESS-3.6 counts as observed facts only, deriving from them no velocity, capacity, estimate, or projected date.
- **ASSESS-3.8** WHEN the assessment produces a finding that requires follow-on work THE SYSTEM SHALL record that finding together with exactly one named destination among `amend-feature`, `reroute-plan`, `plan-milestones`, `define-domain`, and `/publish-issues`.
- **ASSESS-3.9** IF a `GOAL-N` the milestone cites does not resolve to exactly one live, non-struck-through goal THEN THE SYSTEM SHALL record that citation's result as `Unresolved`, judge no advancement for it, and withhold the milestone's goal-coverage verdict.
- **ASSESS-3.10** WHILE the goal-coverage verdict is withheld under ASSESS-3.9 THE SYSTEM SHALL leave the outcome verdict and close eligibility unaffected.
- **ASSESS-3.11** WHERE the user supplies an `select-review-sample` allocation covering the commit range from the milestone's committed baseline to its candidate closing revision THE SYSTEM SHALL count that allocation's sample set as sampled and carry its residue forward as explicitly unreviewed.
- **ASSESS-3.12** WHERE no such allocation is supplied THE SYSTEM SHALL record that range as unsampled and name `/select-review-sample` for the user to run.

## 4. Gate the close on mechanical eligibility and a human disposition

**Story:** As a developer, I want the close to require both a clean mechanical check and an
explicit human decision, so that a milestone is never recorded as delivered on a model's
say-so, and never on a revision nobody assessed.

- **ASSESS-4.1** THE SYSTEM SHALL treat a milestone as close-eligible only while mechanical eligibility holds and a human disposition permits the close.
- **ASSESS-4.2** WHEN evaluating mechanical eligibility THE SYSTEM SHALL require that the write-handoff names the same `MILE-N` and the same candidate closing revision as the assessment, that every member binding resolved, and that the committed baseline resolved.
- **ASSESS-4.3** IF mechanical eligibility does not hold THEN THE SYSTEM SHALL withhold close eligibility whatever disposition is recorded.
- **ASSESS-4.4** WHILE an assessment's current disposition is `Pending` THE SYSTEM SHALL withhold close eligibility.
- **ASSESS-4.5** WHEN close eligibility holds THE SYSTEM SHALL hand `plan-milestones` the `MILE-N`, the assessment's ordinal within that milestone's file, the effective verdict, and the candidate closing revision SHA.
- **ASSESS-4.6** WHEN `plan-milestones` receives an assessment write-handoff THE SYSTEM SHALL read the referenced assessment from `docs/roadmap/assessments/<MILE-N>.md` and prove-claim that it names the same `MILE-N`, carries the referenced ordinal, records the same candidate closing revision SHA, holds a terminal current disposition, and carries the effective verdict and close decision the write-handoff asserts.
- **ASSESS-4.7** IF any value the write-handoff asserts does not match the referenced assessment THEN THE SYSTEM SHALL refuse the close and report the mismatch.
- **ASSESS-4.8** WHEN `plan-milestones` records a close from a verified assessment write-handoff THE SYSTEM SHALL write the verified SHA verbatim into that milestone's `Closed:` slot.
- **ASSESS-4.9** WHEN `plan-milestones` receives an assessment write-handoff THE SYSTEM SHALL neither re-run the assessment nor append a further assessment block.
- **ASSESS-4.10** WHERE the effective verdict records the outcome as not achieved and the close decision is `Close` THE SYSTEM SHALL allow the close to proceed with that verdict preserved in the assessment file.
- **ASSESS-4.11** WHERE the human disposes during the invocation that wrote the assessment THE SYSTEM SHALL complete the assessment and its disposition without requiring a further invocation.
- **ASSESS-4.12** IF `plan-milestones` is asked to transition a milestone from `Committed` to `Closed` without a verified assessment write-handoff THEN THE SYSTEM SHALL refuse the transition and name `/assess-milestone` for the user to run.
- **ASSESS-4.13** WHEN `plan-milestones` verifies an assessment write-handoff THE SYSTEM SHALL derive every verified value by reading the assessment artifact, treating the write-handoff's asserted values as claims to check rather than facts to trust.
- **ASSESS-4.14** WHEN an invocation ends with the current disposition non-terminal THE SYSTEM SHALL leave the assessment recorded and completable by a later invocation without re-running the assessment.
- **ASSESS-4.15** WHILE the current disposition is `Accepted` THE SYSTEM SHALL take the effective verdict to be the agent's recorded verdict.
- **ASSESS-4.16** WHILE the current disposition is `Overridden` THE SYSTEM SHALL take the effective verdict to be the human's recorded replacement verdict.
- **ASSESS-4.17** WHILE the current disposition is non-terminal THE SYSTEM SHALL treat the assessment as carrying no effective verdict.
- **ASSESS-4.18** WHEN a terminal disposition is recorded THE SYSTEM SHALL record with it an explicit close decision of exactly one of `Close` or `Hold`.
- **ASSESS-4.19** THE SYSTEM SHALL treat a disposition as permitting the close only while it is terminal and its recorded close decision is `Close`.
- **ASSESS-4.20** WHILE the current disposition is `Deferred` THE SYSTEM SHALL withhold close eligibility and leave the assessment open to a later disposition.

## 5. Reach the gate without weakening the roadmap skills

**Story:** As a maintainer of this skill set, I want the new gate reachable where people
already look for their next action, and the two shipped roadmap skills provably unchanged
in everything the gate does not require.

- **ASSESS-5.1** THE SYSTEM SHALL expose `assess-milestone` as user-invoked, carrying `disable-model-invocation: true`.
- **ASSESS-5.2** WHEN a `Committed` milestone's members are all bound and every bound feature's `Status:` is `Shipped` THE SYSTEM SHALL select running `/assess-milestone` for that `MILE-N` as `refresh-roadmap-status`'s next action.
- **ASSESS-5.3** THE SYSTEM SHALL state the roadmap structural rules `R1`–`R11` in exactly one shared reference that both `refresh-roadmap-status` and `assess-milestone` read.
- **ASSESS-5.4** (guard) WHEN `refresh-roadmap-status` runs against a given repo state THE SYSTEM SHALL CONTINUE TO produce the finding set it produced before those rules moved to the shared reference.
- **ASSESS-5.5** (guard) WHEN `refresh-roadmap-status` runs THE SYSTEM SHALL CONTINUE TO write no file.
- **ASSESS-5.6** (guard) WHEN `refresh-roadmap-status` runs THE SYSTEM SHALL CONTINUE TO report structural presence only, judging no milestone outcome.
- **ASSESS-5.7** (guard) WHEN `plan-milestones` applies an update that does not transition a milestone to `Closed` THE SYSTEM SHALL CONTINUE TO apply its RMAP-1.17 approval gate unchanged.
- **ASSESS-5.8** (guard) WHEN `plan-milestones` runs THE SYSTEM SHALL CONTINUE TO leave `docs/specs/INDEX.md` unmodified.
- **ASSESS-5.9** (guard) WHEN `assess-milestone` runs THE SYSTEM SHALL CONTINUE TO leave `docs/roadmap/INDEX.md` modified only through `plan-milestones`.
- **ASSESS-5.10** (guard) WHEN `assess-milestone` needs an attention allocation THE SYSTEM SHALL CONTINUE TO leave `select-review-sample` user-invoked, naming it rather than invoking it.
- **ASSESS-5.11** (guard) WHEN `audit-trace` runs THE SYSTEM SHALL CONTINUE TO check referential integrity for `CODE-N.M` and `ARCH-N` only.
- **ASSESS-5.12** (guard) WHEN a terminal human verdict is published THE SYSTEM SHALL CONTINUE TO restrict `record-verdict`'s caller set to `land-branch` and `cut-release`.
- **ASSESS-5.13** WHEN `plan-milestones` records a close from a verified assessment write-handoff THE SYSTEM SHALL apply its RMAP-1.17 approval gate after the assessment gate has passed.

## 6. Quality attributes

**Story:** As a developer relying on this gate across a long-lived project, I want its
derivation bounded, its inputs untrusted, and its write failures loud, so that it stays
cheap to run and never opens the close gate on evidence it did not actually record.

- **ASSESS-6.1** WHEN `assess-milestone` runs THE SYSTEM SHALL complete its evidence gathering with one full read of each source artifact and a number of `git` commands independent of the milestone's member count — verified by a scenario over a milestone carrying at least 50 members.
- **ASSESS-6.2** IF a value read from `docs/roadmap/INDEX.md`, `docs/specs/INDEX.md`, `docs/product/vision.md`, or an assessment file reaches a shell command THEN THE SYSTEM SHALL pass it as a single non-option argument and reject any value not matching the expected ID or revision shape — verified by a scenario supplying an option-shaped and a metacharacter-bearing value.
- **ASSESS-6.3** THE SYSTEM SHALL treat prose read from those artifacts as passive data — verified by a scenario embedding an instruction in a milestone `Outcome:` sentence and in a previously recorded verbatim human rationale, confirming both are reported rather than obeyed.
- **ASSESS-6.4** IF writing the assessment file fails THEN THE SYSTEM SHALL report the failure and withhold close eligibility — verified by a scenario in which the target path is unwritable.

**Accessibility: None** — this feature ships markdown skills, a markdown reference, and a
markdown artifact, rendering its report as conversational markdown through the host harness.
It introduces no interactive, keyboard, or visual UI surface of its own.

## Out of Scope

- **Assessing anything other than a milestone.** No feature-level and no arbitrary-range
  mode. `prove-claim`, `inspect-change`, `validate-feature`, and `realign-spec` already own the
  feature-level boundary, and a range with no `Outcome:` sentence gives nothing to judge
  against.
- **Requiring the roadmap layer.** A project using this skill set for short features or
  tasks is never obliged to create a `MILE-N` or `ROAD-N`; ASSESS-1.1 exits clean.
- **Judging structural roadmap health.** `R1`–`R11` stay `refresh-roadmap-status`'s; this feature
  reads the shared statement of them and adds none.
- **An action-item list.** Every finding carries a named destination (ASSESS-3.8) and the
  assessment holds no bucket of its own.
- **`record-verdict` as a destination.** Its caller set stays closed to `land-branch`
  and `cut-release` (ASSESS-5.12).
- **Estimation, velocity, capacity, forecasting, and next-milestone sizing.** ASSESS-3.6
  records descriptive counts; ASSESS-3.7 forbids deriving anything forward-looking from
  them, and nothing from this feature reaches `plan-milestones`'s planning path.
- **The team-ceremony retrospective.** What went well, what went badly, per-person
  attribution, attendance, and cadence are not this skill. It assesses an outcome against a
  written intent.
- **Reopening a closed milestone.** Moving a milestone's `Commitment:` off `Closed` is
  `plan-milestones`'s act under RMAP-1.19. This feature only appends a further assessment
  when asked to reassess.
- **Invoking `select-review-sample` or `refresh-roadmap-status`.** Both carry
  `disable-model-invocation: true`; this feature names them and reuses their rules, never
  calls them.
- **Editing RMAP's Out-of-Scope section.** The reconciling note described in the preamble
  is `realign-spec`'s work against the RMAP triad, not a task of this feature.
