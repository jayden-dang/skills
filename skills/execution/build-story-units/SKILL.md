---
name: build-story-units
description: Use when an approved tasks.md has Execution-mode story-unit and
  needs human-gated review-unit execution — derived units, unit barriers,
  mode-change write-back, resume via unit ledger lines — through whole-branch
  review.
---

# Build Story Units

Drive an approved **story-unit** plan to completion: derive review units from
requirement stories, implement unit-by-unit with fresh subagents, stop for a
human after each unit, resume from the unit ledger, finish with whole-branch
review.

**This is not continuous execution.** Continuous multi-task orchestration
without unit barriers is `build-continuous`. Controller-implements-without-subagents
is `build-inline`. If `Execution-mode:` is `continuous`, stop and use
`build-continuous` instead. If the user wants no subagents, name `build-inline`.

**Why fresh subagents:** each worker gets only its task brief; bulk artifacts
travel as paths under `.skills/`, never pasted session history.

**Narration:** at most one short line between tool calls. Ledger + tool results
carry the record.

## The Iron Law

```
NO NEXT UNIT WITHOUT HUMAN UNLOCK (OR A WRITTEN MODE CHANGE)
```

Agent-clean is not human unlock. EOD, demo pressure, and "whole PR later" do
not drop the barrier. "Stop stopping" is a **mode change**: write
`Execution-mode: continuous` into `tasks.md` before dropping barriers.

## Iron laws (story-unit)

1. **Review units are derived**, never authored in `tasks.md` (ignore PM
   "Human review order" comments for partition).
2. After each unit's tasks are clean: **unit agent review → STOP for human →
   unlock**.
3. **"continue"** after looking = next unit only. **"stop stopping" /
   "just run it all"** = write `Execution-mode: continuous` into `tasks.md`
   first, then hand remaining work to `build-continuous`. Chat-only is not a mode
   change.
4. Ledger `Unit <k>: complete (tasks …, range <base>..<head>)` — resume reads it.
5. **Whole-branch agent review still runs** after the last unit. Human unit
   reviews are not a substitute.

| Thought | Reality |
|---|---|
| "User said keep going — no need to edit tasks.md" | "Stop stopping" is a **mode change**; write the header or the plan lies |
| "Unit agent review was clean — skip human barrier" | Agent unit review is not the human stop |
| "EOD / whole PR later — drop unit stops" | Time and later review do not rewrite Execution-mode |
| "continue means run everything left" | "continue" unlocks **one** next unit; run-it-all needs mode-change language |
| "PM review waves are clearer than stories" | Partition is derived from requirement story IDs, not authored lists |

## Setup

1. **Mode gate.** Read `Execution-mode:` from `tasks.md`. Must be `story-unit`.
   If `continuous` → use `build-continuous`. If missing/`unset`/invalid → ask, write
   the chosen value, proceed only if the result is `story-unit`. Never invent
   continuous. *Done when: header is `story-unit`.*
2. **Workspace check — route-work first.** Isolate in a worktree, or implement on the
   current branch? Do not create a worktree unasked. Isolation → REQUIRED
   SUB-SKILL: use `isolate-workspace`. Current branch is main/master → separate
   explicit consent before any implementation. *Done when: workspace choice is
   clear.*
3. **Ledger check.** Ensure `.skills/` is git-ignored:
   `grep -qxF '.skills/' .gitignore 2>/dev/null || { printf '.skills/\n' >> .gitignore && git commit -m 'chore: ignore local skills artifacts' -- .gitignore; }`
   Read `.skills/progress.md` if present. Every complete task **and** complete
   unit line is authoritative — resume at the first task not listed; skip units
   already ledgered complete. *Done when: next task/unit is known.*
4. **Read the plan.** Read `tasks.md` once. Copy **Global Constraints**
   verbatim for every reviewer dispatch. If `docs/agents/project.md` is missing,
   say so, suggest `configure-repo`, take verify commands from Global Constraints.
   When `## Team` has roster/band, load band **packaging** only — never skip
   dual-verdict review for Solo. *Done when: constraints captured word-for-word.*
5. **Derive units — GATE.** Load `story-unit-mode.md` beside this file. Run
   **Derive partition** + **File count** + print the **Unit table**. Hard-fail
   blocks dispatch. *Done when: table printed; hard-fails resolved or reported.*
6. **Todos — GATE.** One todo per task via TodoWrite before any dispatch.
   *Done when: todo list mirrors the plan.*
7. **Pre-flight plan review.** One batch question for plan-internal defects
   before dispatch. Clean scan → no comment. *Done when: conflicts ruled or none.*
8. **Unit order.** Topo-sort units (edge if any task in U depends on any task
   in V); tie-break lowest story number. Inside a unit, order tasks by
   Depends-on (serial default — parallel waves inside a unit are out of scope
   for this skill). *Done when: unit sequence is fixed.*

## Per-unit loop

For each unit U in order:

### A. Tasks in the unit

For each Task N in U (Depends-on order):

1. **Record base.** `BASE=$(git rev-parse HEAD)`.
2. **Build brief.** Task N block + verbatim Global Constraints →
   `.skills/task-N-brief.md`. Include relevant `**ARCH-N**` when a
   `docs/architecture/` spine exists.
3. **Dispatch a FRESH implementer** using the template at
   `../build-continuous/implementer-prompt.md` (one home for the implementer
   contract — do not fork it). Dispatch inventory only: one-line placement,
   brief path as requirements, interfaces prior tasks cannot know, ambiguity
   resolutions, report path `.skills/task-N-report.md`, explicit model. Never
   session history. Never the whole plan file.
4. **Answer questions** fully before the implementer proceeds.
5. **Handle status** (table below). Work must be committed on DONE.
6. **Package diff** → `.skills/review-<base7>..<head7>.diff`:
   `git log $BASE..HEAD --oneline`, `git diff --stat $BASE HEAD`,
   `git diff -U10 $BASE HEAD`. Never `HEAD~1` as base.
7. **Task reviewer** via `../build-continuous/task-reviewer-prompt.md` with brief,
   report, diff package, verbatim Global Constraints, explicit model. Spine
   present → also REQUIRED SUB-SKILL: use `judge-invariants`; `violates` enters
   the fix loop.
8. **Fix loop.** Critical/Important → fix subagent (re-run covering tests under
   `test-first`, append to same report) → **re-review**. Same finding survives 3
   cycles → stop; if plan/design/requirements invalidated, REQUIRED SUB-SKILL:
   use `reroute-plan`; else escalate. Never fix in controller context. Minors
   → ledger for whole-branch triage.
9. **Resolve ⚠️ items** the reviewer could not prove-claim from the diff.
10. **Ledger task.** `Task N: complete (commits <base7>..<head7>, review clean)`.
    Mark todo done.

### B. Unit barrier (after every task in U is ledgered)

Load `story-unit-mode.md` **Per-unit barrier** and run it in full. The human-facing
STOP message MUST fill every REQUIRED slot in that recipe — no freeform
abbreviation under time pressure.

**Unlock:**

| User says | Action |
|---|---|
| continue / LGTM / looks good (after looking) | Ledger `Unit <k>: complete (tasks …, range <base>..<head>)`. Next unit only. Mode stays `story-unit`. |
| stop stopping / just run it all | Write `Execution-mode: continuous` into `tasks.md` (commit if tracked). Ledger this unit complete. REQUIRED SUB-SKILL: use `build-continuous` for remaining tasks (no further unit barriers). |
| stop / hold / changes needed | Stay stopped; do not start the next unit. |

### C. Next unit

Resume the per-unit loop. After the last unit's unlock and ledger line →
**After the last unit**.

## Implementer status handling

| Status | Your move |
|---|---|
| **DONE** | Package diff → task review. |
| **DONE_WITH_CONCERNS** | Read concerns **and** `.skills/implementation-notes.md`. Plan-falsifying deviation → REQUIRED SUB-SKILL: use `reroute-plan`. Missing notes while claiming deviation → re-dispatch to log first. |
| **NEEDS_CONTEXT** | Supply what was named; re-dispatch same model. |
| **BLOCKED** | Context → supply; ceiling → stronger model; too large → split; plan wrong → REQUIRED SUB-SKILL: use `reroute-plan`. |

Cap redispatches at 2 per task; still not DONE → escalate to the user.

## Model tiering

State the model **explicitly on every dispatch**.

- **Cheap:** transcription / single-file mechanical fixes.
- **Mid floor:** every reviewer; every implementer working from prose.
- **Top:** design judgment, broad codebase understanding, whole-branch review.

## Reviewer-prompt hygiene

- Never pre-judge findings in the dispatch ("do not flag X", "Minor at most").
- A plan-mandated defect is still a finding — ask the user which governs.
- No open-ended "check everything" directives without a concrete reason.
- Do not re-run tests the implementer already evidenced in the report.

## Durable progress

- Start: read `.skills/progress.md`; trust it and `git log` over memory.
- Never re-dispatch a task or re-open a unit the ledger marks complete.
- After compaction, resume at the first task without a complete line; unit
  complete lines mean the human barrier already closed for that unit.
- `.skills/` is git-ignored scratch; if wiped, reconstruct from `git log`.

## After the last unit

1. **Whole-branch review.** REQUIRED SUB-SKILL: use `inspect-change` with base =
   `git merge-base main HEAD` — never a mid-branch or last-unit-only range.
   Feed ledger Minors for triage. Top model tier.
2. **One fixer** for the full findings list → re-review.
3. **Polish Diff.** REQUIRED SUB-SKILL: use `polish-diff` on the whole-branch diff
   (before acceptance).
4. **Acceptance.** REQUIRED SUB-SKILL: use `validate-feature`. Breaks →
   `root-cause`, then promote to committed ID-tagged tests.
5. **Prepare.** REQUIRED SUB-SKILL: use `package-change`.
6. **Finish.** REQUIRED SUB-SKILL: use `land-branch`.

## Red Flags — Never

- Start the next unit (or ledger unit complete as if unlocked) without human
  unlock or a written mode change
- Treat "stop stopping" as chat-only without writing `Execution-mode: continuous`
- Over-read "continue" as run-all-remaining-units
- Author or prefer PM review-order lists over derived story units
- Skip unit agent review and send the raw unit to the human first
- Skip whole-branch review because every unit was human-approved
- Use `HEAD~1` as a review base
- Hand a subagent the whole plan file
- Move on with open Critical/Important findings
- Fix reviewer findings in the controller context
- Re-dispatch work the ledger marks complete
- Dispatch before the todo list exists
- Implement on main/master without explicit consent
- Create a worktree without asking
- Silently switch to continuous rules while the header still says story-unit
