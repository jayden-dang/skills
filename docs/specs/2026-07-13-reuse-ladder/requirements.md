# Requirements: Reuse-first ladder in write-design and write-plan

Feature code: REUSE
Status: Implemented
Date: 2026-07-13

<!--
Bakes a component/library-level reuse-before-build discipline (adapted from the
external Ponytail skill) into the design→plan phase, so the methodology stops
designing and tasking new code where a helper, the stdlib, a platform feature, or
an already-installed dependency already does the job. Scope is the `write-design`
and `write-plan` skills ONLY. "THE SYSTEM" here means the skill set — the agent
executing these SKILL.md files.

This complements, and does not duplicate, the existing feature-level reuse machinery
(`brainstorm`/`code-review` feature-overlap, the `write-design` scan subagent and
deletion test): those work at the whole-feature or interface-depth level; this works
at the component/library level.

Verification: this repo validates skills by baseline runs, not an automated harness.
Every requirement below is covered by a documented baseline scenario tagged
`[REUSE-N.M]`; `trace`'s E2 is documented-exempt here.
-->

## 1. The reuse ladder in write-design

**Story:** As a designer, I want a reuse-before-build check climbed against real
evidence of what already exists, so a design does not commit to new code where a
helper, the stdlib, a platform feature, or an installed dependency already does it.

- **REUSE-1.1** WHEN `write-design` authors a component in Step 2 (Architecture) THE
  SYSTEM SHALL climb a seven-rung reuse ladder — (1) does it need to exist at all
  (YAGNI), (2) already in this codebase, (3) standard library or language builtin,
  (4) a platform / framework / runtime feature, (5) an already-installed dependency,
  (6) can it be one line, (7) only then the minimum new code that works — stopping at
  the highest rung that holds before committing to build the component.
- **REUSE-1.2** THE SYSTEM SHALL feed the ladder from the Step-1 scan digest of what
  exists today and climb it only after understanding the problem (tracing the real
  flow the change touches) — the ladder is a reflex applied on that evidence, not a
  separate research pass.
- **REUSE-1.3** THE SYSTEM SHALL NOT use the ladder to prune away input validation at
  trust boundaries, error handling that prevents data loss, security, accessibility,
  or anything the requirements explicitly requested.

## 2. Recording the reuse decision in the design

**Story:** As a reviewer, I want each design component to state what it reuses versus
what it genuinely builds, so over-building and dependency bloat are visible at the
design approval gate rather than discovered in code.

- **REUSE-2.1** WHERE `write-design` authors an architecture section THE SYSTEM SHALL
  record a `Reuse: <rung> — <concrete target>` line beside that section's `Satisfies:`
  line, naming the highest rung that held and the concrete existing artifact it builds
  on (or `none — new code (rung 7)` when nothing lower held).
- **REUSE-2.2** IF a component resolves to rung 7 (new code) THEN THE SYSTEM SHALL
  record on its `Reuse:` line a one-line justification for why no lower rung held.
- **REUSE-2.3** WHERE the design introduces a brand-new third-party dependency (rung 5
  adding a dependency rather than reusing one) THE SYSTEM SHALL surface it as a distinct
  callout at the design approval gate.
- **REUSE-2.4** THE SYSTEM SHALL keep the `Reuse:` line and the new-dependency callout
  advisory — surfaced for the user at the approval gate, never a hard blocker.

## 3. Carrying the reuse decision into the plan

**Story:** As an implementer working from a single task, I want to be told what
existing code to build on, so I do not reimplement what already exists.

- **REUSE-3.1** WHERE `write-plan` authors a task THE SYSTEM SHALL add a `Reuse:` line
  to that task's Files block, naming the concrete existing code, library, or pattern the
  task builds on, so the implementer brief carries "build on these, do not reimplement".
- **REUSE-3.2** THE SYSTEM SHALL keep each task's `Reuse:` line consistent with the
  `Reuse:` line of the design section that task implements.

## 4. Enforcement through the existing Step-4 coverage passes

**Story:** As a maintainer, I want the reuse decision verified inside the two skills'
own coverage checks, so the `Reuse:` line carries weight without adding new machinery.

- **REUSE-4.1** WHEN `write-design` runs its Step-4 coverage self-check THE SYSTEM SHALL
  verify that every architecture section carries a `Reuse:` line and that every rung-7 or
  new-dependency line carries its justification.
- **REUSE-4.2** WHEN `write-plan` runs its Step-4 coverage/consistency check THE SYSTEM
  SHALL flag as a component-level reuse-miss any task whose Files **Create** something the
  scan digest or an already-installed dependency already provides.
- **REUSE-4.3** WHEN `write-plan` runs its Step-4 check THE SYSTEM SHALL flag any task
  whose `Reuse:` line is inconsistent with the design section it implements.

## 5. Composition with the existing levers, and additivity

**Story:** As a maintainer, I want the ladder to sit cleanly beside the scan subagent
and the deletion test, so the three stay distinct and a repo with no reuse opportunities
is unaffected.

- **REUSE-5.1** THE SYSTEM SHALL state the scan → ladder → deletion-test relationship in
  `write-design`: the Step-1 scan gathers what exists, the ladder decides *whether* to
  build, and the deletion test applies only to rung-7 new code to keep its interface deep.
- **REUSE-5.2** (guard) THE SYSTEM SHALL CONTINUE TO run the Step-1 scan subagent and the
  deletion test unchanged — the ladder consumes the scan and precedes the deletion test,
  replacing neither.
- **REUSE-5.3** (guard) WHERE a feature's design or plan has no reuse opportunity THE
  SYSTEM SHALL CONTINUE TO produce the existing `write-design` and `write-plan` structure
  (`Satisfies:` lines, Files Create/Modify/Test, Interfaces, Depends-on, Steps, footers)
  unchanged — the `Reuse:` line is additive and introduces no new hard approval gate.

## Non-functional requirements

Considered per the four quality attributes for this pure-markdown methodology change:

- **Performance** — None. The feature is authoring guidance in two SKILL.md files; it adds
  no runtime path.
- **Reliability** — None. No runtime, no data, no recovery surface.
- **Security** — Satisfied by **REUSE-1.3** (the carve-out): reuse-pruning may never remove
  input validation at trust boundaries or security measures. Not a separate NFR criterion.
- **Accessibility** — Satisfied by **REUSE-1.3**: reuse-pruning may never remove accessibility.
  Not a separate NFR criterion.

## Out of Scope

- **`code-review` and the independent plan-review subagent.** This feature does not add or
  change any reuse check in the review skills; the component-level `reuse-miss` term is
  borrowed from `code-review`, but `code-review` itself is unchanged.
- **`execute-plan`'s task brief.** Threading the `Reuse:` line into the implementer dispatch
  is deliberately excluded; the `Reuse:` line reaches the implementer via the task text only.
- **Ponytail's intensity modes (lite / full / ultra).** The repo favors one consistent
  discipline over selectable modes; no mode switch is added.
- **A new skill.** This extends two existing skills; the skill count stays 36.
- **A hard reuse gate.** Nothing here blocks approval or a commit; the ladder, the `Reuse:`
  line, the new-dependency callout, and the reuse-miss flag are all advisory.
- **Feature-level overlap detection.** That remains `brainstorm` step 1 and `code-review`
  step 3a; this feature operates only at the component/library level.
