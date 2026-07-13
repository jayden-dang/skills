# Requirements: Correct-course — mid-flight plan-invalidation router

Feature code: CCOURSE
Status: Approved
Date: 2026-07-13

<!--
Adds a model-invoked `correct-course` skill (track/ bucket) for the mid-execution
moment when a discovery falsifies an already-approved plan. It is a THIN ROUTER:
it diagnoses, classifies the lowest invalidated artifact with evidence, and routes
to the right re-entry point — it never rewrites requirements/design/plan/tasks/trace
itself (write-* own content; sync-spec owns reconciliation). "THE SYSTEM" here means
the skill set — the agent executing these SKILL.md files.

This feature's only edit to an existing skill is a guarded change to
`execute-plan` (the hand-off trigger). Everything else is additive.

Verification: this repo validates skills by baseline runs, not an automated
harness. Every requirement below is covered by a documented baseline scenario
(recorded at plan time and cited as coverage for the `trace` check); no automated
test code is added by this feature.
-->

## 1. Trigger and hand-off from execute-plan

**Story:** As an agent executing an approved plan, I want a mid-flight discovery
that invalidates the plan to route into a structured correction instead of
dead-ending at "escalate to the user", so the divergence is handled at the seam
where it surfaces.

- **CCOURSE-1.1** WHEN `execute-plan` reaches its BLOCKED diagnose branch for "the
  plan itself is wrong" THE SYSTEM SHALL pause execution and hand off to
  `correct-course` (invoke it directly) rather than dead-end at escalate-to-user.
- **CCOURSE-1.2** WHEN `execute-plan`'s circuit breaker trips (a finding survived 3
  fix→re-review cycles) THE SYSTEM SHALL run a root-cause analysis and hand off to
  `correct-course` only IF that analysis concludes the lowest invalidated artifact
  is above the current task; otherwise it continues the existing escalate/fix flow.
- **CCOURSE-1.3** THE SYSTEM SHALL expose `correct-course` as a model-invoked skill
  (no `disable-model-invocation`) located at `skills/track/correct-course/`, also
  directly user-invokable.
- **CCOURSE-1.4** (guard) WHEN `execute-plan` reaches a BLOCKED status it cannot
  resolve for a reason other than "the plan itself is wrong", genuine ambiguity,
  or all-tasks-complete THE SYSTEM SHALL CONTINUE TO handle that stop exactly as
  today, without routing to `correct-course`.
- **CCOURSE-1.5** (guard) WHEN `execute-plan` runs its pre-flight plan review
  (pre-dispatch internal-consistency scan) THE SYSTEM SHALL CONTINUE TO batch its
  findings into one question to the user as today, unaffected by `correct-course`.

## 2. Phase 1 — diagnose, then stop for approval

**Story:** As a user, I want to be shown exactly what went wrong before anything is
rewritten, and to hold the go/no-go, so a plan is never silently rewritten behind
my back.

- **CCOURSE-2.1** WHEN `correct-course` begins THE SYSTEM SHALL produce a structured
  diagnosis notice covering What is wrong or changed, Where the deviation occurred,
  Why the current plan is no longer valid, How it impacts the remaining execution,
  and any other context needed to decide.
- **CCOURSE-2.2** WHEN the diagnosis notice is presented THE SYSTEM SHALL STOP and
  require the user's explicit go/no-go before performing any classification or
  touching any artifact.
- **CCOURSE-2.3** IF the user declines to proceed at the diagnosis gate THEN THE
  SYSTEM SHALL make no spec or code change and return control without a rewind.

## 3. Phase 2 — classify the lowest invalidated artifact

**Story:** As a user approving a rewind, I want the divergence classified to the
lowest level that is genuinely broken, with evidence, so the correction never
rewinds further up the chain than the discovery actually requires.

- **CCOURSE-3.1** WHEN classification runs THE SYSTEM SHALL identify the lowest level
  in the chain that is genuinely invalidated — one of Task-local, Plan, Design,
  Requirements, or Vision — and cite the evidence supporting that determination.
- **CCOURSE-3.2** THE SYSTEM SHALL NOT select a level higher than the lowest
  genuinely-invalidated artifact; rewinding higher "to be safe" without evidence for
  the higher level is prohibited.
- **CCOURSE-3.3** WHEN classification completes THE SYSTEM SHALL present a change
  proposal stating the chosen level, its evidence, and the proposed re-entry, and
  SHALL require the user's approval of that proposal before routing.
- **CCOURSE-3.4** THE SYSTEM SHALL keep the change proposal ephemeral — presented in
  the conversation for the go/no-go — and SHALL NOT create a standalone
  change-proposal artifact on disk.
- **CCOURSE-3.5** WHEN classification runs THE SYSTEM SHALL treat every rewind as
  driven by newly discovered evidence, recording for the duration of the in-flight
  plan which evidence has already been classified and acted on.
- **CCOURSE-3.6** IF a divergence would re-classify the same already-acted-on evidence
  to the same lowest invalidated artifact without new evidence THEN THE SYSTEM SHALL
  NOT re-enter that level again and SHALL escalate to the user, breaking the
  `execute-plan` → `correct-course` loop.

## 4. Route to the correct re-entry point

**Story:** As a user, I want each classification level to re-enter the workflow at
the matching skill and run that skill's own approval gate, so a rewind reuses the
existing chain rather than a bespoke path.

- **CCOURSE-4.1** WHERE the classification is Task-local THE SYSTEM SHALL return to
  `execute-plan`/`tdd` to continue the work without rewinding any upstream artifact.
- **CCOURSE-4.2** WHERE the classification is Plan THE SYSTEM SHALL re-invoke
  `write-plan`.
- **CCOURSE-4.3** WHERE the classification is Design THE SYSTEM SHALL re-invoke
  `write-design`, which then flows forward into `write-plan`.
- **CCOURSE-4.4** WHERE the classification is Requirements THE SYSTEM SHALL re-invoke
  `write-requirements`, which then flows forward into design and plan.
- **CCOURSE-4.5** WHERE the classification is Vision AND `docs/product/vision.md`
  exists THE SYSTEM SHALL route the premise conflict to the vision layer; WHERE that
  file does not exist THE SYSTEM SHALL escalate to the user for a human decision and
  re-enter `brainstorm` only IF the user agrees the feature's premise is in question.
- **CCOURSE-4.6** WHEN `correct-course` re-enters a level THE SYSTEM SHALL invoke the
  re-entry sub-skill directly (not merely suggest that the user run it) and SHALL let
  that skill run its own normal approval gate before proceeding.

## 5. Thin router — delegate, reconcile, record, resume

**Story:** As a maintainer, I want `correct-course` to own only the routing decision
and delegate all content and bookkeeping, so it does not duplicate `write-*` or
`sync-spec` and cannot drift from them.

- **CCOURSE-5.1** THE SYSTEM SHALL NOT itself author or rewrite requirements, design,
  plan, tasks, or trace metadata; all spec-content generation is delegated to the
  `write-*` skills and all triad reconciliation is delegated to `sync-spec`.
- **CCOURSE-5.2** WHEN a re-entry changes already-approved artifacts or their trace
  links THE SYSTEM SHALL invoke `sync-spec` to reconcile `Status` and the trace after
  the re-entry skill's approval gate has passed.
- **CCOURSE-5.3** WHEN the final approved change carries an architectural consequence
  THE SYSTEM SHALL record it as an ADR via `domain-modeling`; WHERE the change is
  Task-local or Plan-level THE SYSTEM SHALL NOT record an ADR.
- **CCOURSE-5.4** THE SYSTEM SHALL NOT persist an ADR for a proposal the user has not
  approved.
- **CCOURSE-5.5** WHEN routing, reconciliation, and any ADR are complete THE SYSTEM
  SHALL return control to `execute-plan`, which resumes automatically against the
  corrected plan.

## 6. Boundaries against neighbouring skills

**Story:** As a maintainer, I want `correct-course` carved cleanly away from `amend`,
`sync-spec`, and `debug`, so it fires for the rewind decision and nothing else.

- **CCOURSE-6.1** THE SYSTEM SHALL scope `correct-course` to a mid-execution discovery
  that invalidates an in-flight approved plan, and SHALL defer to `amend` for a
  post-ship in-scope tweak to a shipped feature, and to `debug` for broken code that
  runs against a still-valid spec.
- **CCOURSE-6.2** THE SYSTEM SHALL make the rewind decision itself and SHALL treat
  `sync-spec` as one of its exits — the mechanical reconciler that runs after the
  decision — never as the maker of the decision.

## 7. Roster registration and integrity

**Story:** As a maintainer, I want the new skill registered consistently across every
roster surface, so the skill count and routing stay coherent.

- **CCOURSE-7.1** WHEN `correct-course` is added THE SYSTEM SHALL register it in
  `.claude-plugin/plugin.json`, `AGENTS.md` (file-org tree, quick-reference table, and
  counts), `DESIGN.md` (inventory and count), and `docs/guide/skills/` (a new page plus
  the README row and counts), moving every skill-count surface from 35 to 36.
- **CCOURSE-7.2** WHEN `correct-course` is added THE SYSTEM SHALL add an on-ramp for it
  in the `ask` router (`skills/meta/ask/SKILL.md`) keyed to a mid-execution discovery
  that invalidates the plan.
- **CCOURSE-7.3** THE SYSTEM SHALL author the `correct-course` frontmatter `description`
  without any unquoted colon-space (`": "`) sequence, so the frontmatter linter passes.

## Out of Scope

- **A new persisted change-proposal document class** — the proposal is ephemeral; the
  durable trace is the re-entry skills' new/retired IDs, `sync-spec`'s
  strikethrough-with-reason, the commit, and the conditional ADR.
- **Reimplementing `write-*` or `sync-spec` mechanics** — `correct-course` delegates all
  content and reconciliation; it holds no requirement/design/plan/trace editing logic.
- **Changing `execute-plan`'s pre-flight plan review, redispatch caps, or any stop other
  than the two named triggers** — the only `execute-plan` edits are the "plan itself is
  wrong" hand-off and the circuit-breaker root-cause branch.
- **Auto-rewinding without approval** — every rewind passes the diagnosis go/no-go and the
  change-proposal approval; `correct-course` never rewrites a plan silently.
- **Handling incoming external review feedback** — that remains `receive-review`;
  `correct-course` is for self-discovered plan invalidation during execution.
- **A blast-radius severity score or metrics** — classification names the lowest
  invalidated artifact with evidence, not a numeric score.
