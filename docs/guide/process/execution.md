# Phase 3 — Execution

**Skills:** [`worktrees`](../skills/worktrees.md) → [`execute-plan`](../skills/execute-plan.md), governed throughout by [`tdd`](../skills/tdd.md), [`debug`](../skills/debug.md), and [`verify`](../skills/verify.md)

**Produces:** commits, tests, a progress ledger, and a branch ready for review.

## Isolate first

`worktrees` runs before the first file is edited. Its order of preference is strict, and the reason is stated plainly: **never fight the harness.**

1. **Detect isolation that already exists.** Compare `git rev-parse --git-dir` against `--git-common-dir`. If they differ you are probably in a linked worktree — but guard against submodules first, since `git rev-parse --show-superproject-working-tree` printing a path means you are in a submodule, not a worktree.
2. **Use the harness's native workspace tool** if one exists. A native tool manages placement, branching, and cleanup itself; creating a manual worktree alongside it leaves phantom state the harness cannot see.
3. **Fall back to `git worktree`**, into `.worktrees/`.

Before creating anything inside a project-local directory, the directory must be confirmed git-ignored — and the `.gitignore` entry is deliberately **left as an uncommitted working-tree change**. Git honors it immediately, and committing it here would write a commit to the user's *current* branch, the exact thing this skill promises not to touch.

Then install dependencies (auto-detected from lockfiles) and run the **clean baseline**:

- **Baseline green** → proceed.
- **Baseline red** → **stop and ask the user.** Starting on a failing baseline makes it impossible to tell your bugs from pre-existing ones.

## The execution engine

`execute-plan` drives the approved plan to completion: one fresh implementer subagent per task, a two-verdict review of each task's diff, and a whole-branch review at the end.

**Why fresh subagents.** Each worker receives exactly the context its task needs and nothing else, so it stays focused; the controller's context stays reserved for coordination. Subagents never inherit session history — you *construct their world*. Bulk artifacts (briefs, reports, diffs) travel between agents as **file paths under `.skills/`**, never as pasted text.

**Continuous execution.** The user asked you to execute the plan, so execute it. Do not pause between tasks to ask "should I continue?" or post progress summaries — check-ins waste the user's time. The only legitimate stops are a `BLOCKED` status you cannot resolve, ambiguity that genuinely prevents progress, or all tasks complete.

### Setup

Five steps, of which two are easy to skip and expensive to have skipped:

- **Workspace check.** Never begin implementation on `main`/`master` without the user's explicit consent.
- **Ledger check.** `.skills/` is git-ignored, then `.skills/progress.md` is read. **Every task it marks complete IS complete** — resume at the first task it does not list.
- **Read the plan once**, copying the Global Constraints **verbatim**. They get pasted into every reviewer dispatch unmodified.
- **Todos**, one per task.
- **Pre-flight plan review.** Scan the plan once for internal defects — tasks that contradict each other or the Global Constraints, and anything the plan explicitly *mandates* that a reviewer would flag as a defect (an assertion-free test, a copy-pasted logic block). Batch **all** findings into **one** question to the user, each shown beside the plan text that mandates it. One interrupt, not one per discovery mid-run.

### The per-task loop

```
 1. BASE=$(git rev-parse HEAD)              ← before dispatch, always
 2. task-brief <tasks.md> N                 → .skills/task-N-brief.md
 3. dispatch a FRESH implementer            (implementer-prompt.md; model stated explicitly)
 4. answer its questions completely         never rush it into implementation
 5. handle the status                       DONE / DONE_WITH_CONCERNS / NEEDS_CONTEXT / BLOCKED
 6. review-package $BASE $(git rev-parse HEAD)   → .skills/review-<b>..<h>.diff
 7. dispatch a task reviewer                (task-reviewer-prompt.md; two verdicts)
 8. fix loop                                → fix subagent → RE-REVIEW → repeat until clean
 9. resolve ⚠️ cannot-verify-from-diff items
10. append one line to .skills/progress.md
11. go straight to Task N+1
```

Three details in there carry most of the weight.

**`BASE` is recorded before dispatch, never `HEAD~1`.** `HEAD~1` silently drops every commit of a multi-commit task except the last, so the reviewer sees a fraction of the change and approves it.

**Fixes are never applied in the controller's context.** Critical or Important findings go to a *fix subagent*, which re-runs the covering tests and appends its results to the same report file. Then the task is **re-reviewed**. Fixing findings yourself pollutes the controller context that must survive the whole plan. Minor findings are recorded in the ledger for the final review to triage — an unrecorded roll-up is a silent discard.

**The ledger is the source of truth.** Conversation memory does not survive compaction. From the skill:

> Controllers that lost their place have re-dispatched entire completed task sequences — the single most expensive failure this loop has.

After compaction or resume, trust `.skills/progress.md` and `git log` over your own recollection. The commits the ledger names exist in git even when your context no longer remembers writing them.

### Implementer statuses

| Status | The controller's move |
|---|---|
| **DONE** | Package the diff and send it to review |
| **DONE_WITH_CONCERNS** | Read the concerns *first*. Correctness or scope doubts get resolved before review; observations get noted in the ledger |
| **NEEDS_CONTEXT** | Supply the missing file, interface, or decision it named, then re-dispatch on the same model |
| **BLOCKED** | Diagnose: missing context → supply it; reasoning ceiling → stronger model; task too large → split it; the plan is wrong → escalate to the user |

Never ignore an escalation, and **never force the same model to retry with nothing changed.** A stuck implementer means something must change before the next attempt.

### Model tiering

State the model **explicitly on every dispatch** — an omitted model inherits your session's, usually the most capable and most expensive.

- **Cheap tier:** transcription tasks (the plan text contains the complete code, so the work is typing plus testing) and single-file mechanical fixes.
- **Mid tier, as a floor:** every reviewer, and every implementer working from prose. *Turn count beats token price* — cheap models routinely take two to three times the turns on multi-step work and cost more overall.
- **Top tier:** tasks needing design judgment or broad codebase understanding, and the final whole-branch review.

### Reviewer-prompt hygiene

**Never pre-judge findings.** If a dispatch contains "do not flag X", "treat it as Minor at most", or "the plan chose this" — stop. That is pre-judging, usually to spare yourself a review loop.

**A plan-mandated defect is still a finding.** The plan does not grade its own work. Present the finding *and* the mandating plan text to the user and ask which governs.

## The three disciplines that govern everything

**`tdd`** runs inside every implementer. No production code without a failing test first; tests only at seams the design pre-agreed; every test carries its requirement ID.

**`debug`** runs whenever anything behaves unexpectedly. Its Phase 1 is a gate: before any theory-building, construct and *run* a red-capable command — one that is red now because of this exact bug and goes green when it is fixed. *Build the right feedback loop and the bug is 90% fixed.* Three failed fix attempts means stop: the architecture is in question, not your latest hypothesis.

**`verify`** runs before anything that implies success. Identify the proving command, run it fresh and complete, read the full output, confirm it supports the claim. Skip any step and you are lying, not verifying.

## After the last task

1. **Whole-branch review** via [`code-review`](../skills/code-review.md), with base = `git merge-base main HEAD` — never a mid-branch sha. Run on the top model tier, pointed at the ledger's Minor-findings list for triage.
2. **One fixer.** If the review returns findings, dispatch **one** fix subagent carrying the complete list. Never one fixer per finding — each extra fixer rebuilds context and re-runs suites, and a per-finding fix wave can cost more than the whole plan did. Re-review after.
3. **Acceptance** via [`acceptance-check`](../skills/acceptance-check.md).
4. **Finish** via [`finish-branch`](../skills/finish-branch.md).

## Inline fallback

No subagent capability? Same loop, no dispatches: implement each task yourself, in order, from its brief, using `tdd` for every step. Keep the same ledger appends and the same end-of-plan `code-review`. On a blocker, a failing verification, or a plan gap — stop and ask the user. Never guess through it.

## Next

→ [Phase 4 — Review and acceptance](review-and-acceptance.md)

## See also

- [The gates](../concepts/gates.md) — `tdd`, `debug`, and `verify` in detail
- [`execute-plan`](../skills/execute-plan.md) — the full loop and its twelve red flags
- [The artifact model](../concepts/artifacts.md) — what lives in `.skills/`
