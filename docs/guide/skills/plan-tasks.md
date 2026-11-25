# `plan-tasks`

> The buildable plan. Vertical slices with bite-sized TDD steps, written for an implementer who knows nothing about this codebase and will see only their own task.

|  |  |
|---|---|
| **Bucket** | spec |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | `requirements.md`, `design.md`, `templates/tasks.md`, `docs/agents/project.md`, `docs/agents/issue-tracker.md` |
| **Writes** | `docs/specs/<date>-<feature>/tasks.md`, the spec's `INDEX.md` row, an independent review under `.skills/`, optionally **one feature issue** on the tracker |
| **Calls** | [`audit-trace`](audit-trace.md), an independent plan review subagent, then the execute family via [`isolate-workspace`](isolate-workspace.md) |
| **Called by** | [`design-solution`](design-solution.md) |

## When it fires

After the design is Approved and before any implementation. It turns `design.md` into `tasks.md` — the breakdown into buildable, test-tagged, traceable tasks. The governing constraint shapes everything: write for an implementer who is skilled but knows **nothing** about this codebase or problem domain, and who will see only the task delta plus references to canonical project artifacts. Every name, path, command, and type they need must be inside the task or its referenced artifact.

## The five steps

Starting from `templates/tasks.md`, the skill walks five steps.

1. **Header and Global Constraints** — the canonical source path and content hash, referenced by every task.
2. **File structure first** — the map that bounds what any task may touch.
3. **Tasks as vertical slices** — each with Files, Interfaces, Depends-on, TDD steps, and a footer.
4. **Coverage and consistency check** — the subtle one, plus an independent plan review.
5. **Optional publish to the issue tracker**, then the exit offering three execution routes.

## Global Constraints anchor every task

The header states Goal (one sentence), Architecture (two or three sentences), and Tech Stack. Then **Global Constraints** identifies the canonical source path and content hash for project-wide test, lint, typecheck, naming, i18n, and forbidden-change rules. Every task references this source and carries only the compact delta needed for its semantic unit.

## File structure before any task

Before writing a single task, the skill maps every file the plan creates or modifies, each with a one-line responsibility. The rule is sharp: a file not in this map should not be touched by any task. The map is what keeps independent tasks from colliding on the same file with different assumptions.

## Tasks as vertical slices

Keep modules and test steps that deliver one independently reviewable
outcome in the same task. Name the specific failing observation and the
command that collects it. Write the test source during implementation.

The right-sizing rule: a task is the smallest unit that carries its own test cycle and deserves its own review verdict — split only where a reviewer could reject one task while approving its neighbor. Tasks are **vertical slices** (demoable end-to-end) rather than horizontal layers; if a slice needs prefactoring, that prefactoring is its own earlier task — "make the change easy, then make the easy change".

Each task carries five blocks:

- **Files** — Create / Modify (exact paths, line ranges when known) / Test.
- **Interfaces** — Consumes and Produces: the names and types neighboring tasks share. This is how an isolated implementer learns what to call things.
- **Depends-on** — the earlier tasks this one truly needs (interface it Consumes, files it builds on), as `Depends-on: Task 2, Task 4` or `Depends-on: none`. This is the ready-set signal: tasks that share no files or interfaces may run together only when worktree isolation is safe. Omit the line to fall back to strict serial order. Over-declaring serializes needlessly; under-declaring is caught by the executor's disjoint-surface check before it can collide.
- **Steps** name the check to extend, the failing observation, the command,
  and the implementation scope. A task ends with a focused passing run
  and a conventional commit. Implementation is where the test and code are written.
- **Footer** — `_Requirements: CODE-N.M, CODE-N.M_`, the IDs this task implements or guards. Every task has one.

**No placeholders.** "TBD", "add appropriate error handling", "similar to Task 3", or a type referenced but defined in no task — each of these is a plan bug fixed before the plan ships.

## The coverage check — footer citation is not test coverage

Step 4 is the subtle one, and getting it right is the point of the skill.

- **Run the [`audit-trace`](audit-trace.md) check:** every Approved requirement must be cited by at least one task footer. An uncited ID means the plan is incomplete, or the requirement should be struck through with a reason.
- **Behavior coverage.** For each cited requirement, name the test or
  acceptance step that will check the outcome in domain language. Several
  requirements can share one well-chosen check. IDs stay in the docs.
- **Reconcile against the design's seam table.** Every planned observation
  needs a verification step on its agreed seam.
- **Type/name consistency** across tasks: the same function has the same name and signature everywhere it is mentioned.
- **Spec alignment:** re-read `requirements.md` once, checking each criterion against the task that claims it.
- **Upstream sync-back:** if planning reveals a requirement is *wrong or infeasible as written* — not merely uncovered — you correct it in `requirements.md` and re-surface for approval. You never bury a workaround in a task that leaves the requirement lying.

Then the **independent plan review**, dispatched not self-run. The doc-only checks above stay in this context; the codebase comparison does not. A review subagent gets the plan, `requirements.md`, `design.md`, and the repo, and verifies against real code every symbol, signature, path, import, and **hardcoded test value** the plan asserts — a fabricated golden or a guessed API is the classic plan defect. It cites `file:line`, defaults to flag, writes to `.skills/<slug>-plan-review.md`, and you fix before offering execution.

The step is done when every requirement has a task citation and a behavioral
check, [`audit-trace`](audit-trace.md) is clean, and the plan has no placeholders.

## A change map, when you ask for one

If you ask to see what the plan changes (a picture, a diagram, a map), the presentation includes a change map. It is a page at `.skills/<CODE>/change-map.html`, drawn through [`craft-page`](craft-page.md). It shows every file in the plan's `Files` lines, docs included, marked new or changed, with its owner from `docs/agents/project.md`. It also shows the calls the plan adds, each outside consumer of a changed surface, and any other unshipped plan that touches the same file, drawn as a collision with each plan's own wording. A picture drawn inline in the reply does not count as the map. Without the request, no map is made.

## Publishing and the three exits

Step 5 is optional: if the repo uses an issue tracker (`docs/agents/issue-tracker.md`), publish **one feature issue** for the plan (default **Publish unit: feature**). Plan tasks stay in `tasks.md` — they are not tracker issues and not default sub-issues. The issue follows `docs/agents/issue-tracker.md` **Issue format**, and is what the feature PR closes. Its estimate is revised from the approved plan unless you named one. When the specs are committed, its last lines carry the **union** of requirement IDs under `Requirements covered:`, the plan path, and any bound `ROAD-N` / `MILE-N`. When `git check-ignore` says the plan is ignored (specs kept local, as in a company repo you use the set in alone), those three lines are left out and the title drops its `[CODE]` prefix: the people reading the tracker cannot open the spec, so the issue has to read whole on its own. The IDs then go on the ticket's line in `.skills/<CODE>/tickets.md`, where `/board` and `/go` read them. Legacy one-issue-per-task is only when config or the user explicitly opts in.

When the feature already has a ticket, because you named it or `/shape` recorded it, publishing updates that ticket in place and creates nothing. The new state role replaces the ticket's current state role in the same edit, so a ticket that was `shaping` ends as `ready-for-agent` with one state role, not two.

### One triad, one plan

Write every vertical slice of the approved design and requirements into this `tasks.md`. One feature triad is one plan. `frame-change` / `plan-milestones` own independent subsystems or a new feature shape, not leftover slices of this triad. Prefer **3–8** TDD checkboxes per task; paths/types stay in Files/Interfaces/Reuse — long narration → execute brief.

### Exit routes

After the written plan is Approved, the exit offers **exactly three execute routes** — no separate continuous/story-unit interview. `Execution-mode:` stays `unset` at approval; the chosen skill writes the matching value on start.

When the feature is user-facing UI/UX, Team is Solo/Small, or requirements have ≥2 behavioral stories, mark **`build` (story mode) (Recommended)** first — still offer all three; still wait for an explicit pick. That mark is **not** writing `Execution-mode` (no size-based silent waves / mode invent).

| Route | Meaning |
|---|---|
| [`build`](build.md) (story mode) | Human-gated story review units (writes `story-unit`; prefer [`isolate-workspace`](isolate-workspace.md)) |
| [`build`](build.md) (wave mode) | Subagent waves (writes `continuous`; prefer isolate-workspace) |
| [`build`](build.md) (inline mode) | Controller implements; no implementer subagents (bookkeeping `continuous`; no unit barriers) |

The spec's `INDEX.md` row is updated to note the plan exists.

## Worked example

Continuing `SHELL` — the left icon rail — from the [`design-solution`](design-solution.md) page. One task, sliced vertically from click to rendered panel:

```md
### Task 2: Activate a module on rail click

**Files:**
- Modify: `src/shell/rail.tsx`
- Test: `tests/e2e/rail.spec.ts`

**Reuse:** existing rail interaction fixture and module store.

**Interfaces:**
- Consumes: Module { id: string; label: string }
- Consumes: moduleStore.setActive(id: string): void
- Produces: The clicked module's panel.

**Depends-on:** none

- [ ] Extend the rail interaction test. With Home active, click Notes and
  expect the Notes panel to render. RED reaches the panel assertion and
  observes Home still active. Run `./scripts/check rail`.
- [ ] Wire the click to the selected module and rerun that same check.
- [ ] Commit the rail activation behavior.

_Requirements: SHELL-1.1_
```

Reading the task against the five steps:

- **Step 1's** Global Constraints — the Vitest command, the lint rule, the forbidden changes — are copied at the top of the file, so this implementer needs nothing but the task and that block.
- **Step 2's** file map lists the rail and its existing interaction check.
- **Step 3** keeps one outcome from click to panel in one task.
- **Step 4** checks the footer against the named observation. Other rows
  can reuse a check when its assertions distinguish their failure cases.

## Why it is written the way it is

The plan gives an isolated implementer the constraints, paths, interfaces,
and exact observations that define the work. Independent review checks those
claims against the code before implementation.

## See also

- [Traceability](../concepts/traceability.md) — footer citation versus tagged-test coverage
- [`audit-trace`](audit-trace.md) — the check this step runs, and its E1/E2/E3/W1/W2 findings
- [`design-solution`](design-solution.md) — the seam table this plan must reconcile against
- [`build`](build.md) (wave mode) · [`build`](build.md) (story mode) · [`build`](build.md) (inline mode) — execute-family routes
