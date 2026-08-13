---
name: build-inline
version: 1.0.0
description: Use when an approved tasks.md needs controller-side sequential
  execution without implementer subagents — inline TDD per task, progress
  ledger, stop-on-blocker, whole-branch review — for no-subagent environments
  or when the user chose the inline route.
---

Ephemera paths: resolve `FEATURE_CODE` / `<CODE>` then follow `templates/skills-ephemera-paths.md` (feature root `.skills/<CODE>/`).


# Build Inline

Drive an approved plan to completion **yourself**, task by task, with no
implementer (or reviewer) subagent dispatches. Every step is `test-first`. Progress
survives in the ledger. Finish with whole-branch review.

**This is not subagent orchestration.** Continuous multi-task subagent waves are
`build-in-waves`. Human-gated review units with subagents are `build-by-story`.

| Intent | Use instead |
|---|---|
| Subagent waves, continuous | REQUIRED SUB-SKILL: use `build-in-waves` |
| Story-unit barriers + subagents | REQUIRED SUB-SKILL: use `build-by-story` |

**When this skill fires:** the user chose the inline route, the environment
cannot (or must not) fan out implementers, or plan-tasks offered inline
execution and they accepted it. **Tool availability does not override the
route** — if they asked for inline, stay inline even when subagent tools exist.

**Narration:** at most one short line between tool calls. Ledger + tool results
carry the record.

## The Iron Law

```
NO IMPLEMENTER SUBAGENT — YOU ARE THE IMPLEMENTER
NO PRODUCTION CODE WITHOUT TDD
NO GUESSING THROUGH A BLOCKER
```

Dispatching an implementer "because tools exist" or "subagents are faster"
violates this skill. Skipping RED because the change is "one line" violates
this skill. Inventing an API, path, or acceptance detail when the plan is
ambiguous violates this skill — stop and ask.

## Scope vs Execution-mode

Invoking this skill selects the **inline** route. The `Execution-mode` header is
bookkeeping for sibling skills and later handoffs:

| Header | This skill does |
|---|---|
| `continuous` or `story-unit` | Sequential tasks; **no** unit barriers; **no** human unit stops |
| missing / `unset` / invalid | Write `Execution-mode: continuous` into `tasks.md` (commit if tracked). Barriers still do not run here |

Human-gated review units with subagents are `build-by-story`. Inline already
keeps the human in the conversation turn-by-turn.

| Thought | Reality |
|---|---|
| "Subagents exist — use the full loop" | Route is inline. Tools do not rewrite the route |
| "One-line change — skip the failing test" | REQUIRED SUB-SKILL: use `test-first` for every task step |
| "Plan is fuzzy — I'll pick a reasonable shape" | Plan gap → stop and ask; never guess |
| "story-unit header — stop after each story" | Barriers are `build-by-story`. Inline is sequential only |
| "I'll dispatch only the reviewer, not the implementer" | No task-reviewer subagents either; whole-branch `inspect-change` at the end |
| "Parallel waves will finish faster" | Inline is serial. No worktree fan-out |

## Setup

1. **Route gate.** Confirm inline is the intended path (user said so, or no
   subagent capability). If they want subagent continuous waves →
   `build-in-waves`. If they want story-unit barriers → `build-by-story`. *Done
   when: route is inline.*
2. **Header bookkeeping.** Parse `Execution-mode:`. If missing/`unset`/invalid:
   write `Execution-mode: continuous` into `tasks.md`. If already set, leave it.
   *Done when: header is present.*
3. **Session preflight — two questions:**
   1. **Issue tracker sync.** Read `docs/agents/issue-tracker.md` when present.
      IF a tracker is configured (github / gitlab / linear / local / other named
      backend) → ask whether this build should sync with that tracker (bind
      issues to the branch, pull ticket IDs into briefs/ledger, use the
      tracker's wayfinding ops for status). IF yes → resolve ticket IDs from
      branch name, plan, or a short user list; record them under `.skills/` for
      the brief/ledger and later `package-change`. IF no, or the file is absent
      / declares no tracker → empty ticket set; continue (unconfigured tracker
      is normal, not a failure).
   2. **Workspace / branch.** Worktree isolation or current branch? Do not create
      a worktree unasked. Isolation → REQUIRED SUB-SKILL: use `isolate-workspace`.
      main/master → separate explicit consent before implementing.
   *Done when: tracker choice (or empty set) and workspace choice are clear.*
4. **Ledger check.** Ensure `.skills/` is git-ignored:
   `grep -qxF '.skills/' .gitignore 2>/dev/null || { printf '.skills/\n' >> .gitignore && git commit -m 'chore: ignore local skills artifacts' -- .gitignore; }`
   Read `.skills/<CODE>/progress.md` if present. Complete tasks stay complete — resume
   at the first task not listed. *Done when: next task is known.*
5. **Read the plan.** Read `tasks.md` once. Capture **Global Constraints**
   (verify commands live here if `docs/agents/project.md` is missing — say so
   and suggest `configure-repo`). *Done when: constraints are in hand.*
6. **Todos — GATE.** Via TodoWrite before Task 1: **one todo per task** **and**
   one terminal todo **Polish Diff** (whole-branch `polish-diff` before
   acceptance — created now, not later).
   *Done when: the list mirrors the plan **and** includes the polish-diff todo.*
7. **Pre-flight plan review.** One batch question for plan-internal defects
   before coding. Clean scan → no comment. *Done when: conflicts ruled or none.*
8. **Order.** Depends-on topo order; absent Depends-on → every earlier task;
   `none` → no prereq. **Serial only** — never parallel waves / multi-worktree
   fan-out in this skill. *Done when: task sequence is fixed.*

## Per-task loop

For each Task N in order:

1. **Record base.** `BASE=$(git rev-parse HEAD)`.
2. **Build the brief (for yourself).** Copy Task N + Global Constraints into
   `.skills/<CODE>/task-N-brief.md`. That file is the contract you implement against —
   exact values, paths, signatures, `_Requirements:` IDs. Include relevant
   `**ARCH-N**` when a `docs/architecture/` spine exists. WHEN preflight
   recorded ticket IDs, list them in the brief. *Done when: brief exists and
   you have read it.*
3. **Clarify first.** If anything in the brief is ambiguous — API shape, path,
   acceptance, dependency — **stop and ask now**. Do not start RED until clear.
4. **Implement with TDD.** REQUIRED SUB-SKILL: use `test-first` for every step in the
   task. Tests describe domain behavior; map requirement IDs in the report/self-check,
   not by embedding IDs in source. Work only the files the plan names.
5. **Deviations.** WHEN territory forces you off the brief: you **are** the
   implementer — follow the **Deviations** recipe in
   `../build-in-waves/implementer-prompt.md` (nine-field entry under
   `.skills/<CODE>/implementation-notes.md`: **Unknown class**, **Map said**,
   **Territory showed**, **Map impact**, etc.). Log **before** finishing the
   task; append only. IF **Map impact** is `reroute-plan` / `realign-spec` or
   the fix falsifies the plan / shared contract → stop and REQUIRED SUB-SKILL:
   use `reroute-plan` (or ask); do not stretch silently.
6. **Commit.** Conventional subject explaining the change — no `Implements:` /
   `Guards:` trailer required.
7. **Self-check (controller, not a subagent).** Re-read the brief against the
   diff: every requirement ID's behavior covered? TDD evidence (RED then GREEN) real?
   Output pristine? Plan File Structure respected? Fix gaps now — you have no
   separate task-reviewer pass.
8. **Optional evidence bundle.** For non-trivial tasks, write
   `.skills/<CODE>/task-N-report.md` with what changed, IDs covered, RED/GREEN
   commands+output, concerns, deviations path or `none`. Cheap tasks may skip
   the file if the commit message and ledger carry enough; when in doubt, write it.
9. **Ledger.** Append
   `Task N: complete (commits <base7>..<head7>, inline, review self)`.
   Mark the todo done.
10. **Next.** Immediately continue to the next task — no permission pause, no
    unit barrier. On blocker mid-task: stop the loop and ask (see **Stop
    conditions**).

## Stop conditions

Stop and ask the user (do not guess, do not dispatch a subagent to invent an
answer) when:

- The brief or plan is ambiguous or contradictory
- Verification fails and the fix is not obvious from the brief
- A deviation would falsify plan/design/requirements
- You would need to touch files or contracts outside the task
- main/master consent is missing and the workspace is main/master

After the user answers, resume the same task from the brief — do not skip ledger
discipline.

## Durable progress

- Start: read `.skills/<CODE>/progress.md`; trust it and `git log` over memory.
- Never re-do a task the ledger marks complete.
- After compaction, resume at the first task without a complete line.
- `.skills/` is git-ignored; if wiped, reconstruct from `git log`.

## After the last task

1. **Whole-branch review.** REQUIRED SUB-SKILL: use `inspect-change` with base =
   `git merge-base main HEAD` — never a mid-branch sha. Top model tier when a
   choice exists. Point it at any Minors or notes in the ledger /
   `implementation-notes.md`.
2. **Fix findings** yourself under `test-first` (still no implementer subagent unless
   the user explicitly lifts the inline route). Re-run `inspect-change` if the
   fix surface is large.
3. **Polish Diff.** REQUIRED SUB-SKILL: use `polish-diff` on the whole-branch
   diff **before** acceptance. Mark the setup **Polish Diff** todo done only
   after it has run.
4. **Acceptance.** REQUIRED SUB-SKILL: use `validate-feature`. Breaks →
   `root-cause`, then promote to committed ID-tagged tests.
5. **Prepare.** REQUIRED SUB-SKILL: use `package-change`.
6. **Finish.** REQUIRED SUB-SKILL: use `land-branch`.

| Thought | Reality |
|---|---|
| "Task todos are all green — polish can wait / skip" | The setup **Polish Diff** todo is still open; acceptance is blocked until it runs |
| "Inspect was clean / branch is small — polish is optional" | Step 3 is required on every branch; size and a clean inspect do not drop it |

## Red Flags — Never

- Skip the tracker-sync or workspace preflight
- Invent a tracker or ticket set when config is absent or the user declined sync
- Dispatch an implementer or task-reviewer subagent while on this skill
- Skip `test-first` / write production code before a failing test
- Guess through ambiguity, a red suite, or a plan gap
- Run unit barriers or human unit stops (that is `build-by-story`)
- Parallel-wave / multi-worktree fan-out
- Re-do ledger-complete tasks after compaction
- Start on main/master without explicit consent
- Create a worktree without asking
- Claim a task complete without a ledger line
- Skip `polish-diff`, leave its todo open, or move to acceptance/package/land without it
- Start Task 1 before the todo list exists (tasks **and** polish-diff)
- Hand off mid-plan to `build-in-waves` subagent loop without an explicit user
  route change
