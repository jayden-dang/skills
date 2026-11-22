Ephemera paths: resolve `FEATURE_CODE` / `<CODE>` then follow `templates/skills-ephemera-paths.md` (feature root `.skills/<CODE>/`). Resolve pack seeds in this order, first path that exists: (1) `templates/` beside this SKILL.md, (2) `${CLAUDE_PLUGIN_ROOT}/templates` when that variable is set, (3) `../../../templates` relative to this SKILL.md.

# Build In Waves

Drive an approved **continuous** plan to completion through one dependency-aware
scheduler. A ready set of one task runs serially; a ready set of independent,
surface-disjoint tasks may run in parallel worktrees. Related tasks in one
dependency lane may reuse bounded worker and reviewer leases. Every task keeps
its own commit, report, evidence, and two verdicts; there is **no human pause
between tasks**.

**Context rule:** a fresh context is the default at a semantic-unit boundary or
after a hard lease trigger. Inside a valid lane lease, resume the role context
and pass only the task delta. Bulk artifacts travel as file paths under
`.skills/`, never as pasted text.

**Narration:** at most one short line between tool calls. Ledger + tool results
carry the record.

**Shared controller recipe:** read `common.md` beside this file.
Load `common.md` when Setup preflight / ledger / todos or
After the Last Task starts. That file is the one home for those steps and
for the close-sequence predicates.
This file owns continuous-mode scheduling and barriers. The shared task
lifecycle lives in `task-lifecycle.md` and is loaded once.

## Mode ownership

Invoking this skill selects **continuous** execution. Align `tasks.md` to that
route and continue:

| `Execution-mode:` on `tasks.md` | Action |
|---|---|
| `continuous` | Proceed |
| `story-unit` | read `story.md` beside this file and follow it |
| missing / `unset` / invalid | Write `Execution-mode: continuous` into `tasks.md` (commit if tracked). Proceed |

Unit barriers, unit derivation, and human unit stops live only in
the story mode (`story.md`).

| Thought | Reality |
|---|---|
| "Header says story-unit — stay and run waves anyway" | Hand off to the story mode (`story.md`) |
| "I'll derive units as a size signal then continuous" | Waves come from Depends-on only |
| "Lead wants human stops — pause inside continuous" | Human-gated stops are the story mode (`story.md`) |
| "The tasks are small and fully specified — I'll write them myself" | Size never changes the route. Code written by the controller is the inline mode (`inline.md`); here every task gets its own implementer dispatch and its own review. In the baseline, 2 of 4 runs wrote all four tasks in the controller and only then dispatched reviewers — one reviewed all four in a single batch |

## Setup

1. **Mode ownership.** Apply the table above. *Done when: header is `continuous`
   and you stay on this skill, or you have handed off to the story mode (`story.md`).*
2. **Session preflight.** Apply `common.md` **Session preflight**.
   *Done when: that section's Done when holds.*
3. **Ledger check.** Apply `common.md` **Ledger check**.
   *Done when: next task is known.*
4. **Read the plan.** Read `tasks.md` in full once. Record the Global
   Constraints path and content hash for dispatch; the brief points to the
   canonical section instead of pasting it into every reviewer prompt. If
   `docs/agents/project.md` is missing, say so, suggest `configure-repo`, and
   take verify commands from Global Constraints.
   When `## Team` has roster/band, load band **packaging** only — never skip
   dual-verdict review for Solo. *Done when: constraints captured word-for-word.*
5. **Todos — GATE.** Apply `common.md` **Todos — GATE**.
   *Done when: the list mirrors the plan **and** includes the Close branch todo.*
6. **Pre-flight plan review.** Scan once for internal defects (contradictions,
   assertion-free tests, copy-pasted logic the plan mandates). Batch ALL findings
   into ONE question to the user before dispatch. Clean scan → no comment.
   *Done when: conflicts ruled or none.*
7. **Ready-set planning.** Read every task's `Depends-on:` and `Files:` block.
   Named tasks must land first; `Depends-on: none` means no prerequisite; an
   absent line means every earlier task is a prerequisite. Compute the next
   ready set from the dependency graph. A ready set may fan out only when its
   surfaces are disjoint and the runtime has safe worktree isolation. Apply an
   approved `Max-concurrency` cap when present; missing means `auto`.
   *Done when: every task has a dependency position, surface-overlap result,
   and effective lane/concurrency decision.*

## Continuous scheduler

Load `task-lifecycle.md` for the one task loop. The scheduler
supplies the task ID, lane, current base revision, brief path, report path,
review package path, and active lease IDs; the lifecycle owns dispatch, status,
review, fix, evidence, and ledger rules.

Before each worker or reviewer resume, apply **Resume or start fresh** from
`runtime-binding.md`. Record the reason on every fresh start
and carry continuity through the capsule and ledger.

### Ready sets, lanes, and barriers

1. Compute the next ready set from `Depends-on:`. A task is ready only after all
   prerequisites are ledgered clean.
2. If the set has one task, run the shared task lifecycle on the feature branch.
3. If the set has multiple tasks, prove each pair's `Files:` surfaces are
   disjoint and check `worktree_isolation`. Overlap or missing isolation reduces
   the effective set to serial; record the degradation in the runtime sidecar.
4. For a parallel set, record `WBASE`. Reuse a lane that still exists, so its
   build cache stays warm — a fresh worktree rebuilds from cold. Lane directory
   exists: `git -C .worktrees/<branch>-lane<k> switch -c <branch>-taskN WBASE`;
   missing: `git worktree add .worktrees/<branch>-lane<k> -b <branch>-taskN WBASE`.
   Invoke the shared lifecycle. A worker/reviewer lease may continue across
   ready sets only along its own dependency lane.
5. After every task in the set has clean Standards and Spec verdicts, merge in
   deterministic task order. A conflict stops the scheduler; it is never solved
   blind. Then run the **wave gate** at the merged HEAD: compile and lint every
   target in the workspace (`project.md` **Wave gate**, else its typecheck and
   lint commands), judged against the lint baseline. Red → no ledger lines;
   REQUIRED SUB-SKILL: use `root-cause`, one fix dispatch, gate again. Green →
   one ledger line per task.
6. Recompute the ready set. There is no permission pause between tasks in
   continuous mode, and no task advances while its review barrier is open.
7. **Release before the next dispatch.** After every green wave gate, let `N` be
   the lanes the **next** ready set uses: its effective concurrency when above 1,
   otherwise 0 — a one-task set runs on the feature branch and an empty set is
   the end of the run. From the feature checkout:

   ```bash
   # every lane numbered above N
   git worktree remove .worktrees/<branch>-lane<k>
   # every lane numbered N or below
   git -C .worktrees/<branch>-lane<k> switch --detach
   # then every task branch this feature has merged
   for b in $(git for-each-ref --merged HEAD --format='%(refname:short)' 'refs/heads/<branch>-task*'); do
     git branch -d "$b"
   done
   ```

   Only `N` decides: a lane the next set does not use goes even when a later set
   will want it. PINWIN kept every lane "for the whole run": lane 3 sat 13 hours
   on a branch merged in wave 1, lanes 1 and 2 (about 32 GB by the last wave) sat
   idle through four serial tasks, and 17 merged task branches stayed behind. A
   cold rebuild is the accepted price.

   Use these exact forms, without `--force` or `-D`. A refused or denied command
   means that lane or branch stays: name it in the ledger and go on to the next
   step.

   *Done when: `git worktree list` shows at most `N` lanes, and each merged task
   branch is deleted or named in the ledger.*

## Implementer Status Handling

| Status | Your move |
|---|---|
| **DONE** | Package the diff → task review. |
| **DONE_WITH_CONCERNS** | Read concerns **and** `.skills/<CODE>/implementation-notes.md`. Entries must match the nine-field **Deviations** recipe in `implementer-prompt.md`. Missing notes path, incomplete fields, or five-field-only while claiming deviation → incomplete — re-dispatch to log first. **Map impact** `reroute-plan` / `realign-spec` or plan-falsifying → REQUIRED SUB-SKILL: use `reroute-plan` (do not accept as clean DONE). |
| **NEEDS_CONTEXT** | Supply what was named; re-dispatch same model. |
| **BLOCKED** | Context → supply; ceiling → a raise, only on the operator's word (`model-routing.md`); too large → split; plan wrong → REQUIRED SUB-SKILL: use `reroute-plan`. |

Cap redispatches at 2 per task; still not DONE → escalate to the user. Never
force the same model to retry with nothing changed.

The operator's message changes the plan — adds a constraint, cuts scope, drops a
requirement → REQUIRED SUB-SKILL: use `reroute-plan` before any spec or code edit.

## Model Tiering

State the model and effort **explicitly on every dispatch** — omitted model inherits the
session's (usually most expensive). REQUIRED: read `model-routing.md` beside this file and take
each dispatch's values from its role's row, in this harness's column. Going below a row needs
nobody; going above it needs the operator's word, as that file says.

## Reviewer-Prompt Hygiene

- A plan-mandated defect is still a finding — ask which governs.
- No open-ended "check everything" without a concrete task-specific reason.
- Do not re-run tests the implementer already evidenced in the report.

## Durable Progress

Todos are the live session view; the ledger survives compaction. After
compaction, trust the ledger and `git log` over conversation memory.

- Crash mid-wave → discard unmerged task branches, switch lane worktrees back
  to WBASE, and re-run the whole wave off WBASE; if `.skills/` (git-ignored) is wiped, reconstruct
  from `git log`.

## After the Last Task

Apply `common.md` **Close sequence** in full. Do not
restate or subset those steps here.

*Done when: that section's Done when holds.*

## Inline route

Controller-side sequential execution (no implementer subagents) is owned by
**the inline mode**. If the user chose inline, or the environment cannot fan out
implementers: read `inline.md` beside this file and follow it. Do not half-run this
skill's subagent loop without dispatches.

## Red Flags — Never

- Run this loop when `Execution-mode` is `story-unit` (hand off to the story mode (`story.md`))
- Stay on this skill when the user chose inline / no subagents (hand off to
  the inline mode (`inline.md`))
- Run unit barriers, unit derivation, or human unit stops under continuous
- Pause between tasks to ask permission to continue
- Run two implementers in the **same worktree**, or parallel without isolated
  isolate-workspace and a disjoint-surface check
- Merge a parallel wave before every task in it passed review, or ledger it before the wave gate is green
- Hand a subagent the whole plan file — the brief is its world
- Skip re-review after a fix, or accept a review missing either verdict
- Move to the next task with open Critical/Important findings
- Write a task's code in the controller instead of dispatching its implementer
- Review several tasks in one reviewer dispatch
- Let implementer self-review substitute for task review
- Tell a reviewer what not to flag, or pre-rate severity in the dispatch
- Dispatch a reviewer without a diff package
- Send a review to a named review agent from the roster or a plugin (`code-reviewer` and the like) instead of a general-purpose subagent carrying the contract
- Re-dispatch a task the ledger marks complete
