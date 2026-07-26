---
name: write-plan
description: Use when a design is approved and the implementation plan — the tasks.md
  that breaks the design into buildable, test-tagged, traceable tasks — needs
  to be written, after write-design and before any implementation or
  execute-plan.
---

Produce `docs/specs/<YYYY-MM-DD>-<feature>/tasks.md` from the approved requirements
and design. Start from the skill set's `templates/tasks.md` — resolve `templates/`
as `${CLAUDE_PLUGIN_ROOT}/templates` when installed as a plugin, otherwise
`../../../templates` relative to this SKILL.md. Every slot in a task block
(**Files**, **Interfaces**, **Depends-on**, **Risk**, **Decision surface**,
**Steps**, `_Requirements:_`) is REQUIRED.

Create a todo per step (1–4, plus 5 if the repo uses an issue tracker) before starting, and complete them in order — this skill owns its own list, distinct from `write-design`'s upstream and `execute-plan`'s downstream. Check each off only when its **Done when:** is met.

Write for an implementer who is skilled but knows NOTHING about this codebase
or problem domain, and will see ONLY their own task plus the Global
Constraints. Every name, path, command, and type they need must be in the task.

## Step 1: Header and Global Constraints

Goal (one sentence), Architecture (2–3 sentences), Tech Stack. Then **Global
Constraints**: project-wide rules copied verbatim from the design and
`docs/agents/project.md` — test/lint/typecheck commands, naming and i18n
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

**Done when:** Goal, Architecture, Tech Stack, and Global Constraints are
written, and every command, naming/i18n rule, and `ARCH-N` invariant in that
section is copied verbatim from its source file rather than paraphrased.

## Step 2: File structure first

Map every file the plan creates or modifies, with one-line responsibilities,
BEFORE writing tasks. A file not in the map should not be touched by any task.

**Done when:** every file the plan will create or modify appears in the map
with a one-line responsibility.

## Step 3: Tasks as vertical slices

Right-size: a task is the smallest unit that carries its own test cycle and
deserves its own review verdict — split only where a reviewer could reject one
task while approving its neighbor. Prefer vertical slices (demoable
end-to-end) over horizontal layers; if a slice needs prefactoring, that
prefactoring is its own earlier task ("make the change easy, then make the
easy change").

Each task:
- **Files:** Create / Modify (exact paths, line ranges when known) / Test.
- **Reuse:** the concrete existing code, library, or pattern this task builds on — carried down
  verbatim from the design section's `Reuse:` line, same `<rung> — <concrete target>` grammar,
  so the implementer is told to build on it, not reimplement it (e.g. `Reuse: existing —
  src/util/dates:parseISO (rung 2)`, copied verbatim from the design section's `Reuse:` line).
  Keep it consistent with the `Reuse:` line of the design section this task implements.
- **Interfaces:** Consumes / Produces — the names and types neighboring tasks
  share. This block is how an isolated implementer learns what to call things.
- **Depends-on:** the earlier tasks this one truly needs — those whose
  interface it Consumes or whose files it builds on — as `Depends-on: Task 2,
  Task 4`, or `Depends-on: none` when it has no prerequisite. This is the
  parallelism signal: two tasks that share no files and no interface declare no
  edge, so `execute-plan` runs them together in one wave. Omit the line and the
  task falls back to depending on every prior task — safe but fully serial.
  Over-declaring needlessly serializes; under-declaring is caught by the
  executor's file-disjoint check before it can collide.
- **Risk:** `high` | `med` | `low` — blast radius if the task's approach is wrong.
  **high** when the task sets or changes data model / migrations, public
  interfaces, shared types, API contracts, auth or security boundaries, or
  user-facing behavior. **low** when it is mechanical (rename, move, wire-up,
  copy). **med** otherwise.
- **Decision surface:** `yes` | `no` — `yes` when a human is likely to reverse
  or reshape the task's approach on review; `no` for mechanical work the agent
  can own once the high-risk neighbors are right.
- **Steps:** bite-sized checkboxes (2–5 min each) following the TDD cycle:
  failing test (complete code) → run, expect the stated failure → implement
  (complete code) → run, expect pass → commit with an
  `Implements: CODE-N.M` trailer.
- **Footer:** `_Requirements: CODE-N.M, CODE-N.M_` — the IDs this task
  implements or guards. Every task has one.

**Human review order (REQUIRED section, after all tasks).** A short list of
task numbers ordered for the **approving human**, not for `execute-plan`:
highest **Risk** / `Decision surface: yes` first; mechanical `low` / `no` last.
`Depends-on` still governs build waves — do **not** reorder tasks solely to
satisfy review attention if that would lie about dependencies. The review list
is how the plan surfaces decisions the human can still kill before code.

| Thought | Reality |
|---|---|
| "Prefactor first is always right — make the change easy" | Execution order can still prefactor first via Depends-on; the **review** list still leads with the type/API/behavior decision the prefactor serves |
| "Risk is obvious from the title" | Unannotated plans bury high-blast work under renames; the slots are the contract |
| "I'll only annotate high-risk tasks" | Every task has **Risk** and **Decision surface** — low/no is an explicit claim |
| "Demo in 15 minutes — skip fancy annotations" | Dropping **Risk**, **Decision surface**, or **Human review order** for any reason (time, demo, authority, "obvious" mechanical work) means the plan is incomplete — do not present `tasks.md` until every task and the review list are filled |

**No placeholders.** "TBD", "add appropriate error handling", "similar to
Task 3", or a type referenced but defined in no task — each of these is a plan
bug. Fix it before the plan ships.

**Done when:** every file in Step 2's map is covered by at least one task, and
each task is written as a vertical slice carrying its own test cycle. Whether
the slots and placeholders are clean is Step 4's check, not this one.

## Step 4: Coverage and consistency check

- Run the trace check (REQUIRED SUB-SKILL: use `trace`): every Approved
  requirement must be cited by ≥1 task footer. Uncited IDs mean the plan is
  incomplete (or the requirement should be struck through with a reason).
- **Test coverage, not just citation:** every requirement ID must also appear
  in a **test annotation** inside some task's steps (`[CODE-N.M]` in a Vitest
  title, `/// REQ: CODE-N.M` on a Rust test, `@CODE-N.M` in a Playwright tag) —
  not merely in a footer. A footer citation with no tagged test passes
  the trace check now (Approved → W1) but fails **E2** the moment the feature is
  marked Implemented. A guard or negative requirement counts only if a real
  test asserts it; when a behavior can't be unit-tested in isolation, tag the
  e2e task or an existing test that already exercises it — one test may carry
  several IDs.
- **Reconcile against the design's seam table:** if `design.md` has a "Seams
  for testing" table, every ID in every row must be tagged on a test in the
  plan. An ID the design promised to cover but the plan left untagged is
  *dropped coverage* — add the test, don't renumber.
- Type/name consistency across tasks: the same function must have the same
  name and signature in every task that mentions it.
- **Component-level reuse-miss:** flag any task whose Files **Create** something the scan digest
  or an already-installed dependency already provides — build on it instead of rebuilding it.
  This is the task-granularity sibling of the `reuse-miss` `code-review` raises for feature
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
subagent with the plan, requirements.md, design.md, and the repo; have it verify
against real code every symbol, signature, path, import, and **hardcoded test
value** the plan asserts — a fabricated golden or a guessed API is the classic
plan defect — citing `file:line` and defaulting to flag. Findings to
`.skills/<slug>-plan-review.md`; fix before offering execution. (No subagents? Do the
comparison yourself against the code.)

**Done when:** every requirement ID has both a task footer and a tagged test,
the trace check is clean, the design's seam-table IDs are all covered, the
placeholder scan is clean, every task has **Risk** and **Decision surface**,
and **Human review order** lists decision-heavy tasks before mechanical ones.

## Step 5 (optional): Publish to the issue tracker

If the repo uses one (`docs/agents/issue-tracker.md`), publish each task as an
issue in dependency order — native sub-issues and blocking links where
supported; body describes behavior and interfaces (never file paths), includes
acceptance criteria and a `Requirements covered:` list.

This is the heavyweight, traceable publish path — each issue carries its
requirement IDs. For capturing work that never went through the spec triad (a
raw conversation or idea), the user runs `file-issues` instead; do not duplicate
these tasks there.

**Done when:** every task in `tasks.md` has an issue, each issue carries its
`Requirements covered:` list, and the blocking links match the plan's
dependency order. No tracker configured → this step is skipped, not pending.

## Exit

Present the FILE to the user and STOP for approval — conversational agreement is not
approval; the written plan is what gets approved, and `execute-plan` runs only on an
approved `tasks.md`. On approval set `Status: Approved` and offer exactly two
execution routes: `execute-plan` (recommended) in an isolated workspace via
`worktrees`, or inline execution for environments without subagents. Confirm the
feature's row in `docs/specs/INDEX.md` carries the same `Status:` as its
`requirements.md`.

**Done when:** the user has approved the written `tasks.md`, its `Status:` line reads
`Approved`, and the INDEX.md row agrees.
