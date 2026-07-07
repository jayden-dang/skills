---
name: write-plan
description: Use when a design is approved and the implementation plan needs to be written — after write-design, before any implementation starts
---

Produce `docs/specs/<date>-<feature>/tasks.md` from the approved requirements
and design. Start from `templates/tasks.md`.

Write for an implementer who is skilled but knows NOTHING about this codebase
or problem domain, and will see ONLY their own task plus the Global
Constraints. Every name, path, command, and type they need must be in the task.

## Step 1: Header and Global Constraints

Goal (one sentence), Architecture (2–3 sentences), Tech Stack. Then **Global
Constraints**: project-wide rules copied verbatim from the design and
`docs/agents/project.md` — test/lint/typecheck commands, naming and i18n
rules, forbidden changes. Every task's requirements implicitly include this
section; it travels with each task brief.

## Step 2: File structure first

Map every file the plan creates or modifies, with one-line responsibilities,
BEFORE writing tasks. A file not in the map should not be touched by any task.

## Step 3: Tasks as vertical slices

Right-size: a task is the smallest unit that carries its own test cycle and
deserves its own review verdict — split only where a reviewer could reject one
task while approving its neighbor. Prefer vertical slices (demoable
end-to-end) over horizontal layers; if a slice needs prefactoring, that
prefactoring is its own earlier task ("make the change easy, then make the
easy change").

Each task:
- **Files:** Create / Modify (exact paths, line ranges when known) / Test.
- **Interfaces:** Consumes / Produces — the names and types neighboring tasks
  share. This block is how an isolated implementer learns what to call things.
- **Steps:** bite-sized checkboxes (2–5 min each) following the TDD cycle:
  failing test (complete code) → run, expect the stated failure → implement
  (complete code) → run, expect pass → commit with an
  `Implements: CODE-N.M` trailer.
- **Footer:** `_Requirements: CODE-N.M, CODE-N.M_` — the IDs this task
  implements or guards. Every task has one.

**No placeholders.** "TBD", "add appropriate error handling", "similar to
Task 3", or a type referenced but defined in no task — each of these is a plan
bug. Fix it before the plan ships.

## Step 4: Coverage and consistency check

- Run `check-trace`: every Approved requirement must be cited by ≥1 task
  footer. Uncited IDs mean the plan is incomplete (or the requirement should
  be struck through with a reason).
- Type/name consistency across tasks: the same function must have the same
  name and signature in every task that mentions it.
- Spec alignment: re-read requirements.md once, checking each criterion
  against the task that claims it.
- Upstream sync-back: if planning reveals a requirement is *wrong or infeasible
  as written* — not merely uncovered — correct it in requirements.md and
  re-surface for approval. Do not bury a workaround in a task that leaves the
  requirement lying; a plan that satisfies a false requirement ships the falsehood.

**Done when:** check-trace reports no uncited Approved requirements and the
placeholder scan is clean.

## Step 5 (optional): Publish to the issue tracker

If the repo uses one (`docs/agents/issue-tracker.md`), publish each task as an
issue in dependency order — native sub-issues and blocking links where
supported; body describes behavior and interfaces (never file paths), includes
acceptance criteria and a `Requirements covered:` list.

## Exit

Offer exactly two execution routes: `execute-plan` (recommended) in an
isolated workspace via `worktrees`, or inline execution for environments
without subagents. Update the spec's INDEX.md row to note the plan exists.
