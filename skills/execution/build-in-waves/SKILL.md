---
name: build-in-waves
version: 1.1.1
description: Use when an approved tasks.md has Execution-mode continuous and needs
  subagent task-wave execution — dual-verdict review, parallel waves, resume after
  crash/compaction — through whole-branch review and land-branch.
---

Ephemera paths: resolve `FEATURE_CODE` / `<CODE>` then follow `templates/skills-ephemera-paths.md` (feature root `.skills/<CODE>/`).


# Build In Waves

Drive an approved **continuous** plan to completion: independent tasks run in
dependency-ordered waves, one fresh implementer subagent per task, a two-verdict
review of each task's diff, a whole-branch review at the end — **no human pause
between tasks**.

**Not this skill:**

| Intent | Use instead |
|---|---|
| `Execution-mode: story-unit` (human-gated review units) | REQUIRED SUB-SKILL: use `build-by-story` |
| No subagents / controller implements / user chose inline | REQUIRED SUB-SKILL: use `build-inline` |

**Why fresh subagents:** each worker receives exactly the context its task needs
and nothing else. Subagents never inherit session history — you construct their
world. Bulk artifacts travel as file paths under `.skills/`, never as pasted text.

**Narration:** at most one short line between tool calls. Ledger + tool results
carry the record.

**Shared controller recipe:** REQUIRED SUB-SKILL: use `execute-common`.
Load `../execute-common/SKILL.md` when Setup preflight / ledger / todos or
After the Last Task starts. That file is the one home for those steps and
for the polish / product-walk predicates.
This file owns continuous-mode, waves, and the per-task loop only.

## Mode ownership

Invoking this skill selects **continuous** execution. Align `tasks.md` to that
route and continue:

| `Execution-mode:` on `tasks.md` | Action |
|---|---|
| `continuous` | Proceed |
| `story-unit` | REQUIRED SUB-SKILL: use `build-by-story` |
| missing / `unset` / invalid | Write `Execution-mode: continuous` into `tasks.md` (commit if tracked). Proceed |

Unit barriers, unit derivation, and human unit stops live only in
`build-by-story`.

| Thought | Reality |
|---|---|
| "Header says story-unit — stay and run waves anyway" | Hand off to `build-by-story` |
| "I'll derive units as a size signal then continuous" | Waves come from Depends-on only |
| "Lead wants human stops — pause inside continuous" | Human-gated stops are `build-by-story` |

## Setup

1. **Mode ownership.** Apply the table above. *Done when: header is `continuous`
   and you stay on this skill, or you have handed off to `build-by-story`.*
2. **Session preflight.** Apply `../execute-common/SKILL.md` **Session preflight**.
   *Done when: that section's Done when holds.*
3. **Ledger check.** Apply `../execute-common/SKILL.md` **Ledger check**.
   *Done when: next task is known.*
4. **Read the plan.** Read `tasks.md` in full once. Copy **Global Constraints**
   verbatim for every reviewer dispatch. If `docs/agents/project.md` is missing,
   say so, suggest `configure-repo`, take verify commands from Global Constraints.
   When `## Team` has roster/band, load band **packaging** only — never skip
   dual-verdict review for Solo. *Done when: constraints captured word-for-word.*
5. **Todos — GATE.** Apply `../execute-common/SKILL.md` **Todos — GATE**.
   *Done when: the list mirrors the plan **and** includes the Close branch todo.*
6. **Pre-flight plan review.** Scan once for internal defects (contradictions,
   assertion-free tests, copy-pasted logic the plan mandates). Batch ALL findings
   into ONE question to the user before dispatch. Clean scan → no comment.
   *Done when: conflicts ruled or none.*
7. **Wave planning.** Read each task's `Depends-on:` line. Named tasks must land
   first; `Depends-on: none` = no prerequisite; **absent** line → depends on every
   earlier task. Topo-sort into waves. No Depends-on edges → one task per wave
   (strict serial). *Done when: every task sits in a wave.*

## Per-Task Loop

For Task N:

1. **Record the base.** `BASE=$(git rev-parse HEAD)` — before dispatch, always.
2. **Build the brief.** Task N block + verbatim Global Constraints →
   `.skills/<CODE>/task-N-brief.md`. Include relevant `**ARCH-N**` when a
   `docs/architecture/` spine exists. WHEN preflight recorded ticket IDs,
   list them in the brief so implementers and later `package-change` share one
   set. Apply Team band packaging to tone — never omit review obligations.
3. **Dispatch a FRESH implementer** using `implementer-prompt.md` (beside this
   file). Dispatch inventory only: one-line placement; brief path as requirements;
   interfaces/decisions prior tasks cannot know; ambiguity resolutions; report
   path `.skills/<CODE>/task-N-report.md`; explicit model. Never session history. Never
   the plan file.
4. **Answer questions** fully before the implementer proceeds.
5. **Handle the status** per the table below. Work committed on DONE.
6. **Package the diff** → `.skills/<CODE>/review-<base7>..<head7>.diff`:
   `git log $BASE..HEAD --oneline`, `git diff --stat $BASE HEAD`,
   `git diff -U10 $BASE HEAD`. Never `HEAD~1` as base.
7. **Dispatch a task reviewer** using `task-reviewer-prompt.md` with brief,
   report, diff package, verbatim Global Constraints, explicit model. Spine
   present → also REQUIRED SUB-SKILL: use `review-invariants`; `violates` enters
   the fix loop.
8. **Fix loop.** Critical/Important → fix subagent (re-run covering tests under
   `test-first`, append to same report) → **re-review**. Same finding survives 3 cycles
   → stop; plan/design/requirements invalidated → REQUIRED SUB-SKILL: use
   `reroute-plan`; else escalate. Never fix in controller context. Minors →
   ledger for whole-branch triage.
9. **Resolve ⚠️ items** the reviewer could not prove-claim from the diff.
10. **Ledger.** `Task N: complete (commits <base7>..<head7>, review clean)`.
    Mark todo done.
11. **Next.** Advance by wave order (see **Parallel waves**), not raw task
    number. No permission pause between tasks.

## Parallel waves

A single-task wave runs the Per-Task Loop on the branch — the common case. A wave
with two or more independent tasks runs them concurrently, each in its own
worktree, **only when `git worktree` is usable**; otherwise serial.

1. **Record the wave base.** `WBASE=$(git rev-parse HEAD)`.
2. **Prove surfaces are disjoint.** No two briefs Create/Modify the same file.
   Overlap → demote to serial; never parallel overlapping surfaces.
3. **Fan out — one worktree per task.** Stay in the primary worktree at WBASE.
   For each task: `git worktree add .isolate-workspace/<branch>-taskN -b <branch>-taskN WBASE`,
   run **Per-Task Loop steps 1–9** inside that worktree; hold ledger/advance for
   the barrier. Implementers run concurrently.
4. **Barrier, then merge in task order.** Only after every wave task passed
   review, merge each into the **feature branch** (never main/master) ascending
   task number (`git merge --no-ff <branch>-taskN`). Conflict → STOP and escalate;
   never resolve a wave merge blind.
5. **Ledger once, isolate-workspace down.**
   `Task N: complete (merged <branch>-taskN at <merge7>, review clean)` per task;
   mark todos; `git worktree remove` each.

## Implementer Status Handling

| Status | Your move |
|---|---|
| **DONE** | Package the diff → task review. |
| **DONE_WITH_CONCERNS** | Read concerns **and** `.skills/<CODE>/implementation-notes.md`. Entries must match the nine-field **Deviations** recipe in `implementer-prompt.md`. Missing notes path, incomplete fields, or five-field-only while claiming deviation → incomplete — re-dispatch to log first. **Map impact** `reroute-plan` / `realign-spec` or plan-falsifying → REQUIRED SUB-SKILL: use `reroute-plan` (do not accept as clean DONE). |
| **NEEDS_CONTEXT** | Supply what was named; re-dispatch same model. |
| **BLOCKED** | Context → supply; ceiling → stronger model; too large → split; plan wrong → REQUIRED SUB-SKILL: use `reroute-plan`. |

Cap redispatches at 2 per task; still not DONE → escalate to the user. Never
force the same model to retry with nothing changed.

## Model Tiering

State the model **explicitly on every dispatch** — omitted model inherits the
session's (usually most expensive).

- **Cheap:** transcription / single-file mechanical fixes.
- **Mid floor:** every reviewer; every implementer working from prose.
- **Top:** design judgment, broad codebase understanding, whole-branch review.

Scale reviewer tier to diff size and risk.

## Reviewer-Prompt Hygiene

- Never pre-judge findings ("do not flag X", "Minor at most", "the plan chose this").
- A plan-mandated defect is still a finding — ask which governs.
- No open-ended "check everything" without a concrete task-specific reason.
- Do not re-run tests the implementer already evidenced in the report.

## Durable Progress

Conversation memory does not survive compaction. Todos = live session view;
ledger = survives compaction. Never let one excuse skipping the other.

- On start, read `.skills/<CODE>/progress.md`; resume after the last complete task.
- After compaction, trust the ledger and `git log` over memory.
- Never re-dispatch a task the ledger marks complete.
- Crash mid-wave → discard unmerged isolate-workspace; re-run the whole wave off WBASE.
- `.skills/` is git-ignored; if wiped, reconstruct from `git log`.

## After the Last Task

Apply `../execute-common/SKILL.md` **Close sequence** in full — inspect-change,
one fixer, polish (only if the polish predicate holds), validate-feature,
product-walk (only if the walk predicate holds), package-change,
land-branch. Do not restate the steps here.

*Done when: that section's Done when holds.*

## Inline route

Controller-side sequential execution (no implementer subagents) is owned by
**build-inline**. If the user chose inline, or the environment cannot fan out
implementers: REQUIRED SUB-SKILL: use `build-inline`. Do not half-run this
skill's subagent loop without dispatches.

## Red Flags — Never

- Run this loop when `Execution-mode` is `story-unit` (hand off to `build-by-story`)
- Stay on this skill when the user chose inline / no subagents (hand off to
  `build-inline`)
- Run unit barriers, unit derivation, or human unit stops under continuous
- Pause between tasks to ask permission to continue
- Skip the tracker-sync or workspace preflight
- Invent a tracker or ticket set when config is absent or the user declined sync
- Run two implementers in the **same worktree**, or parallel without isolated
  isolate-workspace and a disjoint-surface check
- Merge or ledger a parallel wave before every task in it passed review
- Hand a subagent the whole plan file — the brief is its world
- Use `HEAD~1` as a review base
- Skip re-review after a fix, or accept a review missing either verdict
- Move to the next task with open Critical/Important findings
- Let implementer self-review substitute for task review
- Tell a reviewer what not to flag, or pre-rate severity in the dispatch
- Dispatch a reviewer without a diff package
- Re-dispatch a task the ledger marks complete
- Dispatch the first task before the todo list exists (tasks **and** Close branch)
- Skip the close sequence, silent-skip polish, or treat EOD/demo as a polish predicate
- Fix reviewer findings in the controller context
- Start implementation on main/master without explicit consent
- Create a worktree without asking, or treat "current branch" as consent for main/master
