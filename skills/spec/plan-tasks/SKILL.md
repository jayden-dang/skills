---
name: plan-tasks
description: Use when a design is approved and the tasks.md implementation plan
  (vertical-slice tasks with requirement footers and behavior tests) needs writing,
  after design-solution and before the execute family (build-in-waves /
  build-by-story / build-inline).
---

Produce `docs/specs/<YYYY-MM-DD>-<feature>/tasks.md` from the approved requirements
and design. Start from the skill set's `templates/tasks.md` — resolve `templates/`
as `${CLAUDE_PLUGIN_ROOT}/templates` when installed as a plugin, otherwise
`../../../templates` relative to this SKILL.md. Every slot in a task block
(**Files**, **Interfaces**, **Depends-on**, **Steps**, `_Requirements:_`) is
REQUIRED. Do **not** author per-task risk labels, decision-surface flags, or a
Human-review-order section — risk is measured by select-review-sample risk globs
against the actual diff; review units are **derived** from user stories at
`build-by-story` time (see that skill).

Create a todo per step (1–4, plus 5 if the repo uses an issue tracker) before starting, and complete them in order — this skill owns its own list, distinct from `design-solution`'s upstream and the execute family's downstream. Check each off only when its **Done when:** is met.

Write for an implementer who is skilled but knows NOTHING about this codebase
or problem domain, and will see ONLY their own task plus the Global
Constraints. Every name, path, command, and type they need must be in the task.

## Step 1: Header and Global Constraints

Goal (one sentence), Architecture (2–3 sentences), Tech Stack. Header also
carries the bookkeeping field:

```
Execution-mode: <unset | continuous | story-unit>
```

Leave `Execution-mode: unset` while planning — never invent continuous/story-unit
from plan size, band, or habit. Route choice and mode write-back live only at
**Exit** (and in the chosen execute skill).

Then **Global Constraints**: project-wide rules copied verbatim from the design
and `docs/agents/project.md` — test/lint/typecheck commands, naming and i18n
rules, forbidden changes. Every task's requirements implicitly include this
section; it travels with each task brief. When `## Team` is present with a
non-empty **roster** or band override, derive the **band** and apply
**packaging** from that section only: Solo tasks avoid fake multi-assignee
theater; Small/Multi may add optional freeform owner/review notes (never a new
required task field). Missing Team → pre-feature default.

When a `docs/architecture/` spine exists, also fold its hard `**ARCH-N**` invariants
into Global Constraints so every task inherits them; no spine, nothing to fold. And
source the human-facing engineering rules (naming, i18n, house rules) from
`docs/product/guidelines.md` when it exists, otherwise from `docs/agents/project.md` as
above — the guidelines doc, when present, is where those rules live.

**Done when:** Goal, Architecture, Tech Stack, `Execution-mode:` (typically
`unset`), and Global Constraints are written, and every command, naming/i18n
rule, and `ARCH-N` invariant in that section is copied verbatim from its source
file rather than paraphrased.

## Step 2: File structure first

Map every file the plan creates or modifies, with one-line responsibilities,
BEFORE writing tasks. A file not in the map should not be touched by any task.

**Done when:** every file the plan will create or modify appears in the map
with a one-line responsibility.

## Step 3: Tasks as vertical slices

**Contract — a task is a vertical slice:** the smallest unit that carries its own
test cycle and deserves its own review verdict. Split only where a reviewer could
reject one task while approving its neighbor.

**Shape:** one demoable end-to-end outcome per task when the work is one user
story. Prefactoring that only enables a later slice is its **own earlier task**
("make the change easy, then make the easy change") with `Depends-on` edges —
not a license to bury horizontal layers inside a story task.

Each task:
- **Files:** Create / Modify / Test with **hardened** path tokens: each path in
  backticks (e.g. `` `src/foo/bar.ts` ``). Line numbers or ranges, when stated,
  MUST NOT be glued into the path token (`path:86-103` is forbidden); put ranges
  in surrounding prose or a separate annotation. P1 ownership extraction still
  accepts legacy glued forms in already-written tasks.md — this grammar is for
  **new** plans only.
- **Reuse:** the concrete existing code, library, or pattern this task builds on — carried down
  verbatim from the design section's `Reuse:` line, same `<rung> — <concrete target>` grammar,
  so the implementer is told to build on it, not reimplement it (e.g. `Reuse: existing —
  src/util/dates:parseISO (rung 2)`, copied verbatim from the design section's `Reuse:` line).
  Step 4 checks it against the design's `Reuse:` line, so copy rather than reinterpret.
- **Interfaces:** Consumes / Produces — the names and types neighboring tasks
  share. This block is how an isolated implementer learns what to call things.
- **Depends-on:** the earlier tasks this one truly needs — those whose
  interface it Consumes or whose files it builds on — as `Depends-on: Task 2,
  Task 4`, or `Depends-on: none` when it has no prerequisite. This is the
  parallelism signal: two tasks that share no files and no interface declare no
  edge, so `build-in-waves` can run them together in one parallel wave. Omit the
  line and the task falls back to depending on every prior task — safe but fully
  serial. Over-declaring needlessly serializes; under-declaring is caught by the
  executor's file-disjoint check before it can collide.
- **Steps:** bite-sized checkboxes (2–5 min each) following the TDD cycle:
  failing test (complete code describing **behavior**, not embedding requirement
  IDs in application/test source) → run, expect the stated failure → implement
  (complete code) → run, expect pass → commit with a conventional subject that
  explains the change (no `Implements:` / `Guards:` trailer required or taught).
- **Footer:** `_Requirements: CODE-N.M, CODE-N.M_` — the IDs this task
  implements or guards. Every task has one. **Default: one story's IDs** (same
  story number N). Multi-story footers **merge** those stories into one review
  unit under `build-by-story` (plan-quality signal — not a ban, not a reason to
  lie about Depends-on). IDs live in this footer (and in requirements/design),
  not in production source or test titles.

`Depends-on` governs build waves. Never reorder or narrow dependencies solely to
tidy review units if that would lie about what the task needs.

| Thought | Reality |
|---|---|
| "Prefactor first is always right — make the change easy" | Prefactor via Depends-on is fine; review units still follow story citations at build-by-story |
| "I'll add Risk: high so reviewers notice" | No such field. Risk globs on the actual diff replace agent labels |
| "I'll write Human review order so the human knows what to read first" | Superseded: story-derived units are the review order; an authored second list dies without a consumer |

**No placeholders.** "TBD", "add appropriate error handling", "similar to
Task 3", or a type referenced but defined in no task — each of these is a plan
bug. Fix it before the plan ships.

**Done when:** every file in Step 2's map is covered by at least one task, and
each task is written as a vertical slice carrying its own test cycle. Whether
the slots and placeholders are clean is Step 4's check, not this one.

## Step 4: Coverage and consistency check

- Run the audit-trace check (REQUIRED SUB-SKILL: use `audit-trace`): every Approved
  requirement must be cited by ≥1 task footer. Uncited IDs mean the plan is
  incomplete (or the requirement should be struck through with a reason).
  audit-trace is **docs-only** — it does not require IDs in test source.
- **Behavior coverage via steps, not ID strings in code:** every requirement ID
  in a footer must have a corresponding TDD step (or explicit manual/acceptance
  step) that asserts the **behavior** in domain language. Do **not** require
  `[CODE-N.M]`, `/// REQ:`, or `@CODE-N.M` inside planned test source. Map IDs
  to tests in the task report / Spec review, not in production trees.
- **Reconcile against the design's seam table:** if `design.md` has a "Seams
  for testing" table, every ID in every row must have a planned test or
  acceptance step at that seam. An ID the design promised to cover but the plan
  left without a behavior test is *dropped coverage* — add the step, don't renumber.
- Type/name consistency across tasks: the same function must have the same
  name and signature in every task that mentions it.
- **Component-level reuse-miss:** flag any task whose Files **Create** something the scan digest
  or an already-installed dependency already provides — build on it instead of rebuilding it.
  This is the task-granularity sibling of the `reuse-miss` `inspect-change` raises for feature
  overlap; it is an advisory finding, not a hard block.
- **Reuse consistency:** flag any task whose `Reuse:` line disagrees with the `Reuse:` line of
  the design section it implements.
- Spec alignment: re-read requirements.md once, checking each criterion
  against the task that claims it.
- Upstream sync-back: if planning reveals a requirement is *wrong or infeasible
  as written* — not merely uncovered — correct it in requirements.md and
  re-surface for approval. Do not bury a workaround in a task that leaves the
  requirement lying; a plan that satisfies a false requirement ships the falsehood.

**Independent plan review — dispatch, don't self-review.** The checks above are
doc-only and stay here; the codebase comparison does not. Dispatch a review
subagent with the plan, requirements.md, design.md, and the repo; have it prove-claim
against real code every symbol, signature, path, import, and **hardcoded test
value** the plan asserts — a fabricated golden or a guessed API is the classic
plan defect — citing `file:line` and defaulting to flag. Findings to
`.skills/<CODE>/plan-review.md`; fix before offering execution. (No subagents? Do the
comparison yourself against the code.)

**Done when:** every requirement ID has a task footer and a planned behavior
test/acceptance step at an agreed seam, the docs-only audit-trace check is clean,
the design's seam-table IDs are all covered, and the placeholder scan is clean.

## Step 5 (optional): Publish to the issue tracker

If the repo uses one (`docs/agents/issue-tracker.md`), publish each task as an
issue in dependency order — native sub-issues and blocking links where
supported; body describes behavior and interfaces (never file paths), includes
acceptance criteria and a `Requirements covered:` list.

This is the heavyweight, traceable publish path — each issue carries its
requirement IDs. For capturing work that never went through the spec triad (a
raw conversation or idea), the user runs `publish-issues` instead; do not duplicate
these tasks there.

**Done when:** every task in `tasks.md` has an issue, each issue carries its
`Requirements covered:` list, and the blocking links match the plan's
dependency order. No tracker configured → this step is skipped, not pending.

## Exit

1. **Present the FILE and STOP.** Conversational agreement is not approval; the
   written plan is what gets approved. The execute family runs only on an
   approved `tasks.md`.
2. **On approval:** set `Status: Approved`. Leave `Execution-mode:` as `unset`
   (or untouched). Do **not** write `continuous` or `story-unit` yourself.
3. **Offer exactly three execute routes** — one question, three skills. Do **not**
   first ask continuous vs story-unit; that interview is dead. Mode write-back is
   owned by the skill the user picks.

| Route | Meaning |
|---|---|
| **`build-in-waves`** | Subagent waves, no human pause between tasks (writes `Execution-mode: continuous`). Prefer `isolate-workspace` first. |
| **`build-by-story`** | Subagent path with human-gated review units derived from stories (writes `Execution-mode: story-unit`). Prefer `isolate-workspace` first. |
| **`build-inline`** | Controller implements sequentially with `test-first`, no implementer subagents (writes `Execution-mode: continuous` as bookkeeping; **does not** run unit barriers). |

4. **On pick:** name the skill and hand off — REQUIRED SUB-SKILL: use
   `build-in-waves`, `build-by-story`, or `build-inline` as chosen. For the two
   subagent routes, prefer REQUIRED SUB-SKILL: use `isolate-workspace` first when
   no isolated workspace exists yet.
5. **INDEX:** confirm the feature's row in `docs/specs/INDEX.md` carries the same
   `Status:` as its `requirements.md`.

| Thought | Reality |
|---|---|
| "PM said just mark Approved — continuous is obvious" | Approval is the written plan. Offer the three skills; do not invent mode |
| "Standup in five — skip asking which execute skill" | Time changes *when* you ask, not whether a route is named |
| "Four tasks → default build-in-waves" | No size-based default. User picks one of the three |
| "I'll ask continuous vs story-unit, then offer routes" | Redundant. One question: which of the three skills |
| "User said approve and start building — write continuous and go" | Approve + offer three routes. "Start building" is not a route pick |
| "I'll write Execution-mode now so the plan looks complete" | Completeness is Status + route name. Mode is written by the execute skill |

### Red Flags — Exit

- Asking continuous vs story-unit before (or instead of) the three-skill offer
- Setting `Status: Approved` while inventing `Execution-mode: continuous`
- Offering only one route, or skipping the offer after approval
- Writing `Execution-mode:` in plan-tasks instead of letting the execute skill do it
- Treating "LGTM, build it" as a silent default to `build-in-waves`

**Done when:** the written `tasks.md` is approved, `Status:` reads `Approved`,
one of the three execute skills is named (and handed off when the user picks),
`Execution-mode:` was not invented here, and the INDEX.md row agrees.
