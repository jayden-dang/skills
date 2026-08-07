---
name: build-by-story
description: Use when an approved tasks.md has Execution-mode story-unit and
  needs human-gated review-unit execution — derived units, unit barriers,
  mode-change write-back, resume via unit ledger lines — through whole-branch
  review.
---

Ephemera paths: resolve `FEATURE_CODE` / `<CODE>` then follow `templates/skills-ephemera-paths.md` (feature root `.skills/<CODE>/`).


# Build By Story

Drive an approved **story-unit** plan to completion: derive review units from
requirement stories, implement unit-by-unit with fresh subagents, stop for a
human after each unit, resume from the unit ledger, finish with whole-branch
review.

Continuous multi-task orchestration without unit barriers is `build-in-waves`.
Controller-implements-without-subagents is `build-inline`. Invoking this skill
selects **story-unit** execution. If the header already says `continuous`, hand
off to `build-in-waves`. If the user wants no subagents, name `build-inline`.

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
   first, then hand remaining work to `build-in-waves`. Chat-only is not a mode
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

## Mode ownership

Align `tasks.md` to the story-unit route and continue:

| `Execution-mode:` on `tasks.md` | Action |
|---|---|
| `story-unit` | Proceed |
| `continuous` | REQUIRED SUB-SKILL: use `build-in-waves` |
| missing / `unset` / invalid | Write `Execution-mode: story-unit` into `tasks.md` (commit if tracked). Proceed |

## Setup

1. **Mode ownership.** Apply the table above. *Done when: header is `story-unit`
   and you stay on this skill, or you have handed off to `build-in-waves`.*
2. **Session preflight — two questions:**
   1. **Issue tracker sync.** Read `docs/agents/issue-tracker.md` when present.
      IF a tracker is configured (github / gitlab / linear / local / other named
      backend) → ask whether this build should sync with that tracker (bind
      issues to the branch, pull ticket IDs into briefs/ledger, use the
      tracker's wayfinding ops for status). IF yes → resolve ticket IDs from
      branch name, plan, or a short user list; record them under `.skills/` for
      implementer briefs and later `package-change`. IF no, or the file is
      absent / declares no tracker → empty ticket set; continue (unconfigured
      tracker is normal, not a failure).
   2. **Workspace / branch.** Isolate in a worktree, or implement on the current
      branch? Do not create a worktree unasked. Isolation → REQUIRED SUB-SKILL:
      use `isolate-workspace`. Current branch is main/master → separate explicit
      consent before any implementation.
   *Done when: tracker choice (or empty set) and workspace choice are clear.*
3. **Ledger check.** Ensure `.skills/` is git-ignored:
   `grep -qxF '.skills/' .gitignore 2>/dev/null || { printf '.skills/\n' >> .gitignore && git commit -m 'chore: ignore local skills artifacts' -- .gitignore; }`
   Read `.skills/<CODE>/progress.md` if present. Every complete task **and** complete
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
6. **Todos — GATE.** Via TodoWrite before any dispatch: **one todo per task**
   **and** one terminal todo **Polish Diff** (whole-branch `polish-diff` before
   acceptance — created now, not later).
   *Done when: the list mirrors the plan **and** includes the polish-diff todo.*
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
   `.skills/<CODE>/task-N-brief.md`. Include relevant `**ARCH-N**` when a
   `docs/architecture/` spine exists. WHEN preflight recorded ticket IDs,
   list them in the brief so implementers and later `package-change` share one
   set.
3. **Dispatch a FRESH implementer** using the template at
   `../build-in-waves/implementer-prompt.md` (one home for the implementer
   contract — do not fork it). Dispatch inventory only: one-line placement,
   brief path as requirements, interfaces prior tasks cannot know, ambiguity
   resolutions, report path `.skills/<CODE>/task-N-report.md`, explicit model. Never
   session history. Never the whole plan file.
4. **Answer questions** fully before the implementer proceeds.
5. **Handle status** (table below). Work must be committed on DONE.
6. **Package diff** → `.skills/<CODE>/review-<base7>..<head7>.diff`:
   `git log $BASE..HEAD --oneline`, `git diff --stat $BASE HEAD`,
   `git diff -U10 $BASE HEAD`. Never `HEAD~1` as base.
7. **Task reviewer** via `../build-in-waves/task-reviewer-prompt.md` with brief,
   report, diff package, verbatim Global Constraints, explicit model. Spine
   present → also REQUIRED SUB-SKILL: use `review-invariants`; `violates` enters
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
| stop stopping / just run it all | Write `Execution-mode: continuous` into `tasks.md` (commit if tracked). Ledger this unit complete. REQUIRED SUB-SKILL: use `build-in-waves` for remaining tasks (no further unit barriers). |
| stop / hold / changes needed | Stay stopped; do not start the next unit. |

### C. Next unit

Resume the per-unit loop. After the last unit's unlock and ledger line →
**After the last unit**.

## Implementer status handling

| Status | Your move |
|---|---|
| **DONE** | Package diff → task review. |
| **DONE_WITH_CONCERNS** | Read concerns **and** `.skills/<CODE>/implementation-notes.md`. Entries must match the nine-field **Deviations** recipe in `../build-in-waves/implementer-prompt.md`. Missing notes path, incomplete fields, or five-field-only while claiming deviation → incomplete — re-dispatch to log first. **Map impact** `reroute-plan` / `realign-spec` or plan-falsifying → REQUIRED SUB-SKILL: use `reroute-plan` (do not accept as clean DONE). |
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

- Start: read `.skills/<CODE>/progress.md`; trust it and `git log` over memory.
- Never re-dispatch a task or re-open a unit the ledger marks complete.
- After compaction, resume at the first task without a complete line; unit
  complete lines mean the human barrier already closed for that unit.
- `.skills/` is git-ignored scratch; if wiped, reconstruct from `git log`.

## After the last unit

1. **Whole-branch review.** REQUIRED SUB-SKILL: use `inspect-change` with base =
   `git merge-base main HEAD` — never a mid-branch or last-unit-only range.
   Feed ledger Minors for triage. Top model tier.
2. **One fixer** for the full findings list → re-review.
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
- Dispatch before the todo list exists (tasks **and** polish-diff)
- Skip `polish-diff`, leave its todo open, or move to acceptance/package/land without it
- Implement on main/master without explicit consent
- Create a worktree without asking
- Silently switch to continuous rules while the header still says story-unit
