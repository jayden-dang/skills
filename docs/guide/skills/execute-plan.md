# `execute-plan`

> Drive an approved plan to completion: independent tasks run concurrently in dependency-ordered waves, one fresh implementer subagent per task, a two-verdict review of each task's diff, a whole-branch review at the end.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | `tasks.md` (the plan, and its Global Constraints verbatim), `.skills/progress.md` (the ledger), `docs/agents/project.md` (verify commands, test annotation conventions) |
| **Writes** | implementation commits; `.skills/` scratch — one brief, one report, and one diff package per task, plus the `progress.md` ledger |
| **Calls** | [`worktrees`](worktrees.md), [`tdd`](tdd.md) (inline fallback), [`code-review`](code-review.md), [`acceptance-check`](acceptance-check.md), [`debug`](debug.md) (on an acceptance break), [`finish-branch`](finish-branch.md) |
| **Called by** | [`write-plan`](write-plan.md) (once the plan is approved), [`handoff`](handoff.md) (resuming a partially executed plan) |

## When it fires

An approved `tasks.md` exists and it is time to implement, execute, or build out the plan. It also fires on resume — a crash, a compaction, or a fresh session landing on a plan that is partly done. In that case the ledger, not memory, says where to pick up.

## How it is shaped

Three ideas run underneath the whole skill:

**Fresh subagents per task.** Each worker receives exactly the context its task needs and nothing else, so it stays focused; the controller's own context stays reserved for coordination. Subagents never inherit session history — the controller constructs their world deliberately, one dispatch at a time. Bulk artifacts (briefs, reports, diffs) travel between agents as **file paths under `.skills/`**, never as pasted text. Pasting a brief or a diff into a dispatch would burn the controller's context on material the worker can read from disk itself; passing the path keeps the coordinator lean enough to run a long plan without losing the thread.

**Continuous execution.** The user asked for the plan to be executed, so it gets executed. The controller does not pause between tasks to ask "should I continue?" or post progress summaries — check-ins waste the user's time. There are exactly three legitimate stops:

- a `BLOCKED` status that cannot be resolved,
- ambiguity that genuinely prevents progress, or
- all tasks complete.

Anything else is momentum the skill is built to protect.

**Narration is minimal.** At most one short line between tool calls. The ledger and the tool results carry the record.

## Setup

Six steps run once before any task:

1. **Workspace check.** Never begin implementation on main/master without the user's explicit consent. If no isolated workspace exists, [`worktrees`](worktrees.md) is a required sub-skill. Done when you are on a dedicated branch with a clean baseline.
2. **Ledger check.** Make `.skills/` git-ignored (an idempotent line-presence check, since a trailing-slash pattern won't match until the directory exists), then read `.skills/progress.md` if present. Every task it marks complete *is* complete — resume at the first task it does not list.
3. **Read the plan.** Read `tasks.md` in full, once, and copy the **Global Constraints** section verbatim — it gets pasted into every reviewer dispatch unmodified. If `docs/agents/project.md` is missing, say so, suggest `setup-repo`, and take verify commands from the plan's Global Constraints instead.
4. **Todos.** One todo per task, mirroring the plan.
5. **Pre-flight plan review.** Scan the plan once for internal defects — tasks that contradict each other or the Global Constraints, and anything the plan explicitly mandates that a reviewer would flag as a defect (an assertion-free test, a copy-pasted logic block). **Batch ALL findings into ONE question to the user**, each shown beside the plan text that mandates it, asking which governs — before any dispatch. One interrupt, not one per discovery mid-run. A clean scan needs no comment.
6. **Wave planning.** Read each task's `Depends-on:` line and topo-sort the tasks into waves — wave 0 is every task with no unmet dependency, wave 1 the tasks freed once wave 0 lands, and so on. `Depends-on: none` marks a wave-0 task; an absent line falls back to depending on every earlier task. A plan that declares no dependencies collapses to one task per wave — the strict serial order.

## The per-task loop

Eleven steps run for each Task N. The precise ones are load-bearing:

1. **Record the base.** `BASE=$(git rev-parse HEAD)` — before dispatch, always.
2. **Build the brief.** Copy Task N plus the Global Constraints section out of `tasks.md` into `.skills/task-N-brief.md` verbatim — nothing else from the plan — so the worker's brief holds exactly its own task and the project-wide rules.
3. **Dispatch a fresh implementer** using `implementer-prompt.md`. The dispatch contains exactly: one line placing the task in the project; the brief path, introduced as "this brief is your requirements — read it before anything else"; interfaces and decisions from earlier tasks the brief cannot know; the controller's resolution of any ambiguity it spotted in the brief; the report path; and **the model, stated explicitly**. Never session history, never the plan file. Exact values (numbers, magic strings, signatures) live only in the brief.
4. **Answer questions.** If the implementer asks anything, answer completely before letting it proceed. Never rush it into implementation.
5. **Handle the status** per the table below. Done when the status is `DONE` and the work is committed.
6. **Package the diff.** Assemble `.skills/review-<base7>..<head7>.diff` from the commit list (`git log $BASE..HEAD`), a diffstat, and the full `git diff -U10 $BASE HEAD`. BASE is the sha from step 1 — **never `HEAD~1`**, which silently drops every commit of a multi-commit task except the last.
7. **Dispatch a task reviewer** using `task-reviewer-prompt.md` with the brief path, the report path, the diff package path, the Global Constraints verbatim, and an explicit model.
8. **Fix loop.** Critical or Important findings are dispatched to a **fix subagent** (which re-runs the covering tests — named in the dispatch — and appends results to the same report), then **re-review**. Repeat until the reviewer approves. **Never fix findings in the controller's own context — that pollutes it.** Minor findings get recorded in the ledger for the final review to triage; an unrecorded roll-up is a silent discard.
9. **Resolve ⚠️ items.** Requirements the reviewer could not verify from the diff (they live in unchanged code or span tasks) come back flagged. The controller holds the plan context the reviewer lacks, so it confirms each itself; a real gap counts as a failed spec verdict and returns to step 8.
10. **Ledger.** Append one line to `.skills/progress.md`: `Task N: complete (commits <base7>..<head7>, review clean)`, and mark the todo done.
11. **Next.** Advance by wave order, not raw task number; within a serial wave that is simply Task N+1. For a parallel wave, steps 10–11 move to the barrier below.

## Parallel waves

A single-task wave runs the loop above inline on the branch — the common case. A wave holding two or more independent tasks runs them concurrently, each isolated in its own worktree, and **only when `git worktree` is usable**; otherwise that wave's tasks run serially.

1. **Record the wave base.** `WBASE=$(git rev-parse HEAD)` — every task in the wave branches from this one sha.
2. **Prove the surfaces are disjoint.** Confirm from the briefs that no two tasks in the wave Create or Modify the same file. An overlap means a `Depends-on` edge was missed — those tasks drop back to serial rather than run in parallel.
3. **Fan out, one worktree per task.** The controller stays in the primary worktree (the feature branch at WBASE); each task gets its own. `git worktree add .worktrees/<branch>-taskN -b <branch>-taskN WBASE`, then run per-task loop steps 1–9 inside each worktree concurrently — steps 10–11 (ledger, advance) are held for the barrier. On a fresh branch, step 1's `BASE` already equals WBASE, so the brief, dispatch, package, review, and fix loop are unchanged — just scoped to the worktree.
4. **Barrier, then merge in task order.** Only once every task in the wave has passed review, and back in the primary worktree, merge each branch into the **feature branch** (never main/master) in ascending task number. A conflict here means the disjoint check missed a shared surface — stop and escalate; never resolve a wave merge blind.
5. **Ledger once, worktrees down.** At the barrier the controller — the sole ledger writer — appends one line per wave task naming its `--no-ff` merge commit as the head, rolls up each task's held Minor findings, and removes the worktrees. Writing only here is what keeps the ledger race-free.

Isolation plus the disjoint-surface check is what makes concurrency safe: two implementers never share a working tree, and the ledger is never written from inside one.

## Implementer status handling

The implementer reports exactly one of four statuses. The controller's move is fixed per status, and it never forces the same model to retry with nothing changed — a stuck implementer means something must change first.

| Status | The controller's move |
|---|---|
| **DONE** | Package the diff (step 6) and send it to review. |
| **DONE_WITH_CONCERNS** | Read the concerns first. Correctness or scope doubts: resolve before review. Observations ("this file is getting big"): note in the ledger, proceed to review. |
| **NEEDS_CONTEXT** | Supply the missing file, interface, or decision it named, then re-dispatch on the **same** model. |
| **BLOCKED** | Diagnose: missing context → supply and re-dispatch; reasoning ceiling → re-dispatch on a **stronger** model; task too large → split it; the plan itself is wrong → escalate to the user. |

## Model tiering

State the model **explicitly on every dispatch** — an omitted model inherits the session's, usually the most capable and most expensive one, silently defeating this section.

- **Cheap tier:** transcription tasks (the plan text already contains the complete code — the work is typing plus testing) and single-file mechanical fixes.
- **Mid tier, as a floor:** every reviewer, and every implementer working from prose. Turn count beats token price — cheap models routinely take two to three times the turns on multi-step work and cost more overall.
- **Top tier:** tasks needing design judgment or broad codebase understanding, and the final whole-branch review.

Reviewer models scale to the diff's size and risk: a small mechanical diff does not need the top tier; a subtle concurrency change does.

## Reviewer-prompt hygiene

The reviewer is only useful if it is left free to judge, so the controller's dispatch stays clean of anything that steers the verdict:

- **Never pre-judge findings.** No "do not flag X", no "treat it as Minor at most", no pre-rated severities — those exist to spare the controller a review loop, and they defeat the review.
- **A plan-mandated defect is still a finding.** The plan does not grade its own work, so the finding and the mandating plan text go to the user, who decides which governs. Never dismiss the finding, and never dispatch a fix that contradicts the plan without asking.
- **Global Constraints are the attention lens.** They go in verbatim — binding requirements, exact values and formats and stated relationships — never process rules (the template carries those) and never the controller's pre-judgments.
- **No open-ended directives** ("check every call site", "stress-test if useful") without a concrete, task-specific reason.
- **Do not ask a reviewer to re-run tests** the implementer already ran on the same code — the report file is the test evidence.

## Durable progress

Conversation memory does not survive compaction. Controllers that lost their place have re-dispatched **entire completed task sequences** — the single most expensive failure this loop has. The ledger, not the todos, is the source of truth:

- Read `.skills/progress.md` on start, and resume after the last complete task.
- After a compaction or resume, trust the ledger and `git log` over recollection — the commits the ledger names exist in git even when context no longer remembers writing them.
- Never re-dispatch a task the ledger marks complete.
- A crash mid-wave leaves uncommitted, unmerged worktrees: discard them and re-run the whole wave off WBASE. Nothing is ledgered or merged until the barrier, so the re-run is idempotent.
- If `.skills/` is wiped, reconstruct progress from `git log`.

## After the last task

1. **Whole-branch review.** [`code-review`](code-review.md) is a required sub-skill, with base = the branch point (`git merge-base main HEAD`) — never a mid-branch sha. Point it at the ledger's Minor-findings list, and run it on the top model tier.
2. **One fixer.** If it returns findings, dispatch **ONE** fix subagent carrying the complete findings list — never one fixer per finding; each extra fixer rebuilds context and re-runs suites, and a per-finding fix wave can cost more than the whole plan did. Re-review after.
3. **Acceptance.** [`acceptance-check`](acceptance-check.md) is a required sub-skill — drive the feature through the running system as a real user, because green units prove assertions pass, not that it works. Fix any break via [`debug`](debug.md), then promote the check to a committed, ID-tagged test.
4. **Finish.** [`finish-branch`](finish-branch.md) is a required sub-skill — the user chooses merge / PR / keep / discard.

## Inline fallback

On a harness with no subagent capability, the same loop runs with no dispatches: implement each task in order from its brief, with [`tdd`](tdd.md) as a required sub-skill for every step, the same per-task ledger appends, and the same end-of-plan `code-review`. On a blocker, a failing verification, or a plan gap: stop and ask the user — never guess through it. The main/master consent rule still applies.

## The two dispatch templates

Both live beside the SKILL, and the fact tables above summarise them.

**`implementer-prompt.md`** carries the report contract. The implementer:

- reads the brief first — it *is* the requirements — then works test-first via `tdd`, tagging every test with its requirement ID;
- writes a full report to a file, including **RED evidence** (the command, the failing output, why that failure was the expected one) and **GREEN evidence** (the command and the passing output after implementation);
- self-reviews as a stranger would — completeness, honest names, YAGNI discipline, tests on real behavior — and fixes what it finds before reporting;
- escalates instead of guessing: `BLOCKED` or `NEEDS_CONTEXT` when the task needs an architectural decision with several defensible answers, when clarity on surrounding code cannot be had, when its own approach is in doubt, when the task demands restructuring the plan never anticipated, or when it is reading file after file without traction — naming what is stuck, what it tried, and what help it needs;
- ends with a final message **15 lines or fewer**: one of the four statuses, the commits, a one-line test summary, any concerns, and the report path. The detail lives in the file, never the message.

**`task-reviewer-prompt.md`** is one pass with **two verdicts**, reported separately:

- **Spec Compliance** — walk the brief's requirement IDs and the Global Constraints against the diff for anything missing, extra (scope creep), or misunderstood, citing the ID on every finding; an ID that lives in unchanged code or spans tasks is flagged back as "cannot verify from diff" rather than chased.
- **Code Quality** — correctness, tests-on-real-behavior, and structure against the plan's File Structure, each finding carrying a `file:line`.

Throughout, it treats every line of the implementer's report as an **unverified claim** — a stated rationale never downgrades a finding — reads the diff package rather than crawling the codebase, stays strictly **READ-ONLY**, and **does not re-run the suite** to confirm the report. It looks outside the diff only for a concrete risk it can name, one focused check per named risk; cross-cutting changes (an altered function contract, lock ordering, shared mutable state) are exactly when checking call sites is warranted. Severity is calibrated — Critical is broken behavior, data loss, or security; Important blocks trust in the task; Minor is polish — and a plan-mandated defect is an Important finding, labeled as such, for the user to decide.

The controller assembles both bundles by hand, and that keeps all of this cheap:

- The **brief** is just Task N and the Global Constraints copied out of `tasks.md` into `.skills/task-N-brief.md`, so the worker never sees the rest of the plan.
- The **diff package** bundles the commit list, a diffstat, and the full `git diff -U10` between BASE and HEAD into a single `.skills/review-<base7>..<head7>.diff` file — the wide context is why the reviewer rarely needs to open a file separately.

## Worked example

A four-task plan for feature `NOTES` is approved.

**Setup.** The controller is already in a worktree, so it adds `.skills/` to `.gitignore`, finds no `progress.md`, reads `tasks.md` once, copies its Global Constraints word-for-word, and creates four todos. The pre-flight scan notices that Task 3 mandates a test with no assertions. It does not fix this silently and it does not stop three separate times — it batches that one finding into a single question, shown beside the plan text that mandates it. The user rules the assertion must be added, and execution begins.

**Task 1 — the clean path.** The task is pure transcription (the plan holds the full code), so the controller records `BASE`, copies Task 1 and the Global Constraints into `.skills/task-1-brief.md`, and dispatches a **cheap-tier** implementer with the model stated on the dispatch line. The report comes back `DONE` with RED and GREEN evidence in the report file and a five-line final message. The controller assembles the diff package from `git diff -U10 $BASE HEAD` — the task made three commits, so `HEAD~1` would have hidden two of them — and dispatches a **mid-tier** reviewer. Spec: COMPLIANT. Quality: one Important finding, a swallowed error. The controller dispatches a **fix subagent** (not itself), which patches it, re-runs the covering test, appends the output to the same report, and reports; the re-review is clean. The ledger gets one line, `Task 1: complete (commits a1b2c3d..e4f5a6b, review clean)`, and the controller goes straight to Task 2 — no check-in.

**Task 2 — a status branch.** The implementer returns `NEEDS_CONTEXT`: it needs the interface Task 1 established, which the brief could not know. The controller supplies that one interface and re-dispatches on the **same** model — never forcing a retry with nothing changed — and the task then completes normally.

**After the last task.** Once Task 4 is in the ledger, a **top-tier** `code-review` runs with base `git merge-base main HEAD` — never a mid-branch sha — pointed at the ledger's Minor-findings list. It returns two Minor findings plus the deferred ones. **One** fixer carrying the complete list clears them all, `acceptance-check` drives the feature through the running system, and `finish-branch` hands the merge decision to the user.

## Red flags — never

- Run two implementers in the same worktree, or run a wave in parallel without isolated worktrees and a disjoint-surface check.
- Merge or ledger a parallel wave before every task in it has passed review.
- Hand a subagent the whole plan file — the brief is its world.
- Use `HEAD~1` as a review base.
- Skip the re-review after a fix, or accept a review missing either verdict.
- Move to the next task with open Critical/Important findings.
- Let the implementer's self-review substitute for the task review — both are required.
- Tell a reviewer what not to flag, or pre-rate a finding's severity.
- Dispatch a reviewer without a diff package.
- Re-dispatch a task the ledger already marks complete.
- Pause between tasks to ask permission to continue.
- Fix reviewer findings in the controller's own context instead of dispatching a fixer.
- Start implementation on main/master without the user's explicit consent.

## Why it is written the way it is

The whole design defends one scarce resource: the controller's context window. Every rule that looks fussy — briefs as file paths, fixes dispatched instead of done inline, the report file rather than a pasted transcript — exists to keep coordination state uncluttered so the controller can run a long plan without losing the thread. The durable-progress section names the failure that motivates the rest: a controller whose memory was compacted mid-plan and re-ran work already in `git log`. That is why the ledger and `git log` outrank recollection, and why so much of this skill is about writing things down where a fresh session can find them.

## See also

- [Artifacts](../concepts/artifacts.md) — the `.skills/` scratch files briefs and reports travel as
- [The skill model](../concepts/skill-model.md) — why controller and worker contexts are kept separate
- [`write-plan`](write-plan.md) — the skill that produces the `tasks.md` this one executes
- [`code-review`](code-review.md) — the whole-branch gate after the last task
