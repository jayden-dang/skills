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

The right-sizing rule: a task is the smallest unit that carries its own test cycle and deserves its own review verdict — split only where a reviewer could reject one task while approving its neighbor. Tasks are **vertical slices** (demoable end-to-end) rather than horizontal layers; if a slice needs prefactoring, that prefactoring is its own earlier task — "make the change easy, then make the easy change".

Each task carries five blocks:

- **Files** — Create / Modify (exact paths, line ranges when known) / Test.
- **Interfaces** — Consumes and Produces: the names and types neighboring tasks share. This is how an isolated implementer learns what to call things.
- **Depends-on** — the earlier tasks this one truly needs (interface it Consumes, files it builds on), as `Depends-on: Task 2, Task 4` or `Depends-on: none`. This is the ready-set signal: tasks that share no files or interfaces may run together only when worktree isolation is safe. Omit the line to fall back to strict serial order. Over-declaring serializes needlessly; under-declaring is caught by the executor's disjoint-surface check before it can collide.
- **Steps** — bite-sized checkboxes, 2 to 5 minutes each, following the TDD cycle: write the failing test (complete code) → run and expect the stated failure → implement (complete code) → run and expect pass → commit with an `Implements: CODE-N.M` trailer. Exact commands and expected output, every time.
- **Footer** — `_Requirements: CODE-N.M, CODE-N.M_`, the IDs this task implements or guards. Every task has one.

**No placeholders.** "TBD", "add appropriate error handling", "similar to Task 3", or a type referenced but defined in no task — each of these is a plan bug fixed before the plan ships.

## The coverage check — footer citation is not test coverage

Step 4 is the subtle one, and getting it right is the point of the skill.

- **Run the [`audit-trace`](audit-trace.md) check:** every Approved requirement must be cited by at least one task footer. An uncited ID means the plan is incomplete, or the requirement should be struck through with a reason.
- **Test coverage, not just citation.** Every requirement ID must *also* appear in a **test annotation** inside some task's steps — `[CODE-N.M]` in a Vitest title, `/// REQ: CODE-N.M` on a Rust test, `@CODE-N.M` in a Playwright tag — not merely in a footer. This is the trap: a footer citation with no tagged test **passes audit-trace now** (Approved satisfies the W1 warning) but **fails E2** the instant the feature is marked Implemented, because E2 requires every requirement in an Implemented spec to have a test reference. A guard or negative requirement counts only if a real test asserts it; when a behavior cannot be unit-tested in isolation, tag the e2e task or an existing test that already exercises it — one test may carry several IDs.
- **Reconcile against the design's seam table.** Every ID in every row of `design.md`'s seam table must be tagged on a test in the plan. An ID the design promised to cover but the plan left untagged is *dropped coverage* — you add the test, you do not renumber.
- **Type/name consistency** across tasks: the same function has the same name and signature everywhere it is mentioned.
- **Spec alignment:** re-read `requirements.md` once, checking each criterion against the task that claims it.
- **Upstream sync-back:** if planning reveals a requirement is *wrong or infeasible as written* — not merely uncovered — you correct it in `requirements.md` and re-surface for approval. You never bury a workaround in a task that leaves the requirement lying.

The five checks the coverage step is reconciling against, from the [`audit-trace`](audit-trace.md) check's own finding set:

| Code | Meaning |
|---|---|
| **E1** | a task or test cites an ID defined in no requirements file |
| **E2** | an Implemented/Shipped spec has a requirement with zero test references |
| **E3** | the same ID is defined more than once |
| **W1** | an Approved spec has a requirement not cited by any task |
| **W2** | a requirements file is missing its Status line or feature code |

The plan is written while the spec is Approved, so the linter is enforcing W1 — every requirement cited by a task. But the plan must be built to survive the flip to Implemented, when E2 turns on and a footer without a tagged test becomes a hard error. That is why "footer citation is not test coverage" is a check the plan runs *now*, against a failure that only fires *later*.

Then the **independent plan review**, dispatched not self-run. The doc-only checks above stay in this context; the codebase comparison does not. A review subagent gets the plan, `requirements.md`, `design.md`, and the repo, and verifies against real code every symbol, signature, path, import, and **hardcoded test value** the plan asserts — a fabricated golden or a guessed API is the classic plan defect. It cites `file:line`, defaults to flag, writes to `.skills/<slug>-plan-review.md`, and you fix before offering execution.

The step is done when every requirement ID has both a task footer and a tagged test, [`audit-trace`](audit-trace.md) is clean, the design's seam-table IDs are all covered, and the placeholder scan is clean.

## Publishing and the three exits

Step 5 is optional: if the repo uses an issue tracker (`docs/agents/issue-tracker.md`), publish **one feature issue** for the plan (default **Publish unit: feature**). Plan tasks stay in `tasks.md` — they are not tracker issues and not default sub-issues. The issue body describes behavior and interfaces and **never file paths**, carries the **union** of requirement IDs under `Requirements covered:`, cites the plan path and any bound `ROAD-N` / `MILE-N`, and is what the feature PR closes. Legacy one-issue-per-task is only when config or the user explicitly opts in.

After the written plan is Approved, the exit offers **exactly three execute routes** — no separate continuous/story-unit interview. `Execution-mode:` may stay `unset` at approval; the chosen skill writes the matching value on start:

| Route | Meaning |
|---|---|
| [`build-in-waves`](build-in-waves.md) | Subagent waves (writes `continuous`; prefer [`isolate-workspace`](isolate-workspace.md)) |
| [`build-by-story`](build-by-story.md) | Human-gated story review units (writes `story-unit`; prefer isolate-workspace) |
| [`build-inline`](build-inline.md) | Controller implements; no implementer subagents (bookkeeping `continuous`; no unit barriers) |

The spec's `INDEX.md` row is updated to note the plan exists.

## Worked example

Continuing `SHELL` — the left icon rail — from the [`design-solution`](design-solution.md) page. One task, sliced vertically from click to rendered panel:

```md
### Task 2: Activate a module on rail click

**Files:**
- Modify: src/shell/module-store.ts
- Test: src/shell/module-store.test.ts

**Interfaces:**
- Consumes: Module { id: string; label: string }
- Produces: moduleStore.setActive(id: string): void

- [ ] **Step 1: failing test**
  test('activates the clicked module [SHELL-1.1]', () => {
    store.setActive('notes')
    expect(store.activeModule).toBe('notes')
  })
  Run: `npx vitest run src/shell/module-store.test.ts` — expect: fail,
  `setActive is not a function`.

- [ ] **Step 2: implement** … Run: same command — expect: pass.
- [ ] **Step 3: commit** — trailer `Implements: SHELL-1.1`.

_Requirements: SHELL-1.1_
```

Reading the task against the five steps:

- **Step 1's** Global Constraints — the Vitest command, the lint rule, the forbidden changes — are copied at the top of the file, so this implementer needs nothing but the task and that block.
- **Step 2's** file map already listed `src/shell/module-store.ts`, so touching it here is legal; a file the map omitted could not be touched.
- **Step 3** made this a vertical slice from click to state change, right-sized to one test cycle, with complete test and implementation code and a footer.
- **Step 4** is where both `[SHELL-1.1]` in the title and `SHELL-1.1` in the footer matter: the footer alone satisfies audit-trace's W1 while `SHELL` is Approved, but only the tagged test keeps it clean under E2 once `SHELL` is Implemented.

The footer cites `SHELL-1.1` and the test title tags `[SHELL-1.1]` — both are required. `SHELL-1.2` and `SHELL-1.3` from the design's seam table each get their own tagged test in their own task; the coverage check confirms none of the three seam-table IDs was left with a footer citation but no tagged test, the failure that would surface as E2 the moment `SHELL` is marked Implemented.

## Why it is written the way it is

The plan is where an approved intent becomes something a stranger can build without ever seeing the design conversation — so the skill optimizes relentlessly for the isolated implementer: verbatim constraints, a bounding file map, complete code in every step, no placeholders. The coverage check is the most careful part because it guards a gap the other checks miss: a footer alone satisfies today's linter but leaves a requirement untested, and that debt comes due exactly when the feature ships. Dispatching the codebase comparison to a fresh reviewer catches the defect that self-review structurally cannot — the confidently guessed API or fabricated golden value that reads fine on the page and fails on first run.

## See also

- [Traceability](../concepts/traceability.md) — footer citation versus tagged-test coverage
- [`audit-trace`](audit-trace.md) — the check this step runs, and its E1/E2/E3/W1/W2 findings
- [`design-solution`](design-solution.md) — the seam table this plan must reconcile against
- [`build-in-waves`](build-in-waves.md) · [`build-by-story`](build-by-story.md) · [`build-inline`](build-inline.md) — execute-family routes
