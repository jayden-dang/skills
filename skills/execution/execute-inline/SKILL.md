---
name: execute-inline
description: Use when an approved tasks.md needs controller-side sequential
  execution without implementer subagents — inline TDD per task, progress
  ledger, stop-on-blocker, whole-branch review — for no-subagent environments
  or when the user chose the inline route.
---

# Execute Inline

Drive an approved plan to completion **yourself**, task by task, with no
implementer (or reviewer) subagent dispatches. Every step is `tdd`. Progress
survives in the ledger. Finish with whole-branch review.

**This is not subagent orchestration.** Continuous multi-task subagent waves are
`execute-plan`. Human-gated review units with subagents are `execute-story`.

| Intent | Use instead |
|---|---|
| Subagent waves, continuous | REQUIRED SUB-SKILL: use `execute-plan` |
| Story-unit barriers + subagents | REQUIRED SUB-SKILL: use `execute-story` |

**When this skill fires:** the user chose the inline route, the environment
cannot (or must not) fan out implementers, or write-plan offered inline
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

`Execution-mode` on `tasks.md` still matters for **which sibling skill owns
subagent runs**, not for pauses inside this skill:

| Header | This skill does |
|---|---|
| `continuous` or `story-unit` | Sequential tasks; **no** unit barriers; **no** human stop between tasks for review units |
| missing / `unset` / invalid | Ask; write `continuous` or `story-unit` into the plan. Either value is fine for inline — barriers still do not run here |

If the user wants human-gated review units, they need `execute-story` (subagent
path), not a hybrid of inline + unit stops. Inline already keeps the human in
the conversation turn-by-turn.

| Thought | Reality |
|---|---|
| "Subagents exist — use the full loop" | Route is inline. Tools do not rewrite the route |
| "One-line change — skip the failing test" | REQUIRED SUB-SKILL: use `tdd` for every task step |
| "Plan is fuzzy — I'll pick a reasonable shape" | Plan gap → stop and ask; never guess |
| "story-unit header — stop after each story" | Barriers are `execute-story`. Inline is sequential only |
| "I'll dispatch only the reviewer, not the implementer" | No task-reviewer subagents either; whole-branch `code-review` at the end |
| "Parallel waves will finish faster" | Inline is serial. No worktree fan-out |

## Setup

1. **Route gate.** Confirm inline is the intended path (user said so, or no
   subagent capability). If they want subagent continuous → `execute-plan`.
   If they want story-unit barriers → `execute-story`. *Done when: route is
   inline.*
2. **Mode field.** Parse `Execution-mode:`. If missing/`unset`/invalid: ask,
   write the answer into `tasks.md`, continue. Do not invent continuous. *Done
   when: header is continuous or story-unit.*
3. **Workspace check — ask first.** Worktree isolation or current branch? Do
   not create a worktree unasked. Isolation → REQUIRED SUB-SKILL: use
   `worktrees`. main/master → separate explicit consent before implementing.
   *Done when: workspace choice is clear.*
4. **Ledger check.** Ensure `.skills/` is git-ignored:
   `grep -qxF '.skills/' .gitignore 2>/dev/null || { printf '.skills/\n' >> .gitignore && git commit -m 'chore: ignore local skills artifacts' -- .gitignore; }`
   Read `.skills/progress.md` if present. Complete tasks stay complete — resume
   at the first task not listed. *Done when: next task is known.*
5. **Read the plan.** Read `tasks.md` once. Capture **Global Constraints**
   (verify commands live here if `docs/agents/project.md` is missing — say so
   and suggest `setup-repo`). *Done when: constraints are in hand.*
6. **Todos — GATE.** One todo per task via TodoWrite before Task 1. *Done when:
   the list mirrors the plan.*
7. **Pre-flight plan review.** One batch question for plan-internal defects
   before coding. Clean scan → no comment. *Done when: conflicts ruled or none.*
8. **Order.** Depends-on topo order; absent Depends-on → every earlier task;
   `none` → no prereq. **Serial only** — never parallel waves / multi-worktree
   fan-out in this skill. *Done when: task sequence is fixed.*

## Per-task loop

For each Task N in order:

1. **Record base.** `BASE=$(git rev-parse HEAD)`.
2. **Build the brief (for yourself).** Copy Task N + Global Constraints into
   `.skills/task-N-brief.md`. That file is the contract you implement against —
   exact values, paths, signatures, `_Requirements:` IDs. Include relevant
   `**ARCH-N**` when a `docs/architecture/` spine exists. *Done when: brief
   exists and you have read it.*
3. **Clarify first.** If anything in the brief is ambiguous — API shape, path,
   acceptance, dependency — **stop and ask now**. Do not start RED until clear.
4. **Implement with TDD.** REQUIRED SUB-SKILL: use `tdd` for every step in the
   task. Every test carries its requirement ID per `docs/agents/project.md` (or
   Global Constraints if that file is absent). Work only the files the plan
   names.
5. **Deviations.** WHEN territory forces you off the brief: prefer the
   conservative choice; append to `.skills/implementation-notes.md` (Task /
   Deviation / Cause / Choice / Revisit) **before** finishing the task; if the
   only fix changes a shared contract or falsifies the plan → stop and REQUIRED
   SUB-SKILL: use `correct-course` (or ask), do not stretch silently.
6. **Commit.** Use the trailer the task names (e.g. `Implements: CODE-N.M`).
7. **Self-check (controller, not a subagent).** Re-read the brief against the
   diff: every requirement ID covered? TDD evidence (RED then GREEN) real?
   Output pristine? Plan File Structure respected? Fix gaps now — you have no
   separate task-reviewer pass.
8. **Optional evidence bundle.** For non-trivial tasks, write
   `.skills/task-N-report.md` with what changed, IDs covered, RED/GREEN
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

- Start: read `.skills/progress.md`; trust it and `git log` over memory.
- Never re-do a task the ledger marks complete.
- After compaction, resume at the first task without a complete line.
- `.skills/` is git-ignored; if wiped, reconstruct from `git log`.

## After the last task

1. **Whole-branch review.** REQUIRED SUB-SKILL: use `code-review` with base =
   `git merge-base main HEAD` — never a mid-branch sha. Top model tier when a
   choice exists. Point it at any Minors or notes in the ledger /
   `implementation-notes.md`.
2. **Fix findings** yourself under `tdd` (still no implementer subagent unless
   the user explicitly lifts the inline route). Re-run `code-review` if the
   fix surface is large.
3. **Polish.** REQUIRED SUB-SKILL: use `polish` on the whole-branch diff
   (before acceptance).
4. **Acceptance.** REQUIRED SUB-SKILL: use `acceptance-check`. Breaks →
   `debug`, then promote to committed ID-tagged tests.
5. **Prepare.** REQUIRED SUB-SKILL: use `prepare-change`.
6. **Finish.** REQUIRED SUB-SKILL: use `finish-branch`.

## Red Flags — Never

- Dispatch an implementer or task-reviewer subagent while on this skill
- Skip `tdd` / write production code before a failing test
- Guess through ambiguity, a red suite, or a plan gap
- Run unit barriers or human unit stops (that is `execute-story`)
- Parallel-wave / multi-worktree fan-out
- Re-do ledger-complete tasks after compaction
- Start on main/master without explicit consent
- Create a worktree without asking
- Claim a task complete without a ledger line
- Hand off mid-plan to `execute-plan` subagent loop without an explicit user
  route change
