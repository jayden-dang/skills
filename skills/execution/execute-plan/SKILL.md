---
name: execute-plan
description: Use when an approved tasks.md exists and it is time to implement it, or when resuming a partially executed plan after a crash, compaction, or a fresh session.
---

# Execute Plan

Drive an approved plan to completion: one fresh implementer subagent per task, a two-verdict review of each task's diff, a whole-branch review at the end.

**Why fresh subagents:** each worker receives exactly the context its task needs and nothing else, so it stays focused; your own context stays reserved for coordination. Subagents never inherit session history — you construct their world. Bulk artifacts (briefs, reports, diffs) travel between agents as file paths under `.skills/`, never as pasted text.

**Continuous execution:** the user asked you to execute the plan, so execute it. Do not pause between tasks to ask "should I continue?" or post progress summaries — check-ins waste the user's time. The only legitimate stops: a BLOCKED status you cannot resolve, ambiguity that genuinely prevents progress, or all tasks complete.

**Narration:** at most one short line between tool calls. The ledger and tool results carry the record.

## Setup

1. **Workspace check.** Never begin implementation on main/master without the user's explicit consent. If no isolated workspace exists yet — REQUIRED SUB-SKILL: use `worktrees`. *Done when: you are on a dedicated branch with a clean baseline.*
2. **Ledger check.** Read `.skills/progress.md` if it exists. Every task it marks complete IS complete — resume at the first task it does not list. *Done when: you know which task is next.*
3. **Read the plan.** Read tasks.md in full, once. Copy the **Global Constraints** section verbatim — you will paste it into every reviewer dispatch unmodified. If `docs/agents/project.md` is missing, say so, suggest running `setup-repo`, and take verify commands from the plan's Global Constraints instead. *Done when: constraints are captured word-for-word.*
4. **Todos.** Create one todo per task. *Done when: the todo list mirrors the plan.*
5. **Pre-flight plan review.** Scan the plan once for internal defects: tasks that contradict each other or the Global Constraints, and anything the plan explicitly mandates that a reviewer would flag as a defect (an assertion-free test, a copy-pasted logic block). Batch ALL findings into ONE question to the user — each finding shown beside the plan text that mandates it, asking which governs — before any dispatch. One interrupt, not one per discovery mid-run. A clean scan needs no comment. *Done when: the user has ruled on every conflict, or the scan found none.*

## Per-Task Loop

For Task N:

1. **Record the base.** `BASE=$(git rev-parse HEAD)` — before dispatch, always. *Done when: the sha is noted.*
2. **Build the brief.** Run `task-brief <tasks.md> N` (repo script; it extracts Task N plus the Global Constraints into `.skills/task-N-brief.md` and prints the path). *Done when: the brief file exists.*
3. **Dispatch a FRESH implementer** using `implementer-prompt.md` (beside this file). The dispatch contains exactly: one line placing the task in the project; the brief path, introduced as "this brief is your requirements — read it before anything else"; interfaces and decisions from earlier tasks the brief cannot know; your resolution of any ambiguity you spotted in the brief; the report path `.skills/task-N-report.md`; the model, stated explicitly. Never session history. Never the plan file. Exact values (numbers, magic strings, signatures) live only in the brief. *Done when: the dispatch matches this inventory and nothing more.*
4. **Answer questions.** If the implementer asks anything, answer completely before letting it proceed. Never rush it into implementation. *Done when: no open questions.*
5. **Handle the status** per the table below. *Done when: status is DONE and the work is committed.*
6. **Package the diff.** Run `review-package $BASE $(git rev-parse HEAD)` (repo script; prints the path of the bundle it wrote). BASE is the sha from step 1 — **never `HEAD~1`**, which silently drops every commit of a multi-commit task except the last. *Done when: the package path is printed.*
7. **Dispatch a task reviewer** using `task-reviewer-prompt.md` (beside this file) with: the brief path, the report path, the diff package path, the Global Constraints verbatim, and an explicit model. *Done when: both verdicts are back.*
8. **Fix loop.** Critical or Important findings → dispatch a fix subagent (implementer contract: it re-runs the covering tests — name them in the dispatch; a one-line fix does not need the whole suite — and appends its results to the same report file) → **re-review**. Repeat until the reviewer approves. Never fix findings yourself in the controller context — that pollutes it. Minor findings → record in the ledger for the final review to triage; an unrecorded roll-up is a silent discard. *Done when: the re-review is clean.*
9. **Resolve ⚠️ items.** Requirements the reviewer could not verify from the diff (they live in unchanged code or span tasks) come back to you flagged — you hold the plan context the reviewer lacks. Confirm each yourself; a real gap counts as a failed spec verdict: back to step 8. *Done when: every flagged item is confirmed covered or fixed.*
10. **Ledger.** Append one line to `.skills/progress.md`: `Task N: complete (commits <base7>..<head7>, review clean)`. Mark the todo done. *Done when: the line is written.*
11. **Next task.** Go straight to Task N+1. *Done when: the loop restarts or no tasks remain.*

## Implementer Status Handling

| Status | Your move |
|---|---|
| **DONE** | Package the diff (step 6) and send it to review. |
| **DONE_WITH_CONCERNS** | Read the concerns before anything else. Correctness or scope doubts: resolve them before review. Observations ("this file is getting big"): note in the ledger, proceed to review. |
| **NEEDS_CONTEXT** | Supply the missing file, interface, or decision it named, then re-dispatch on the same model. |
| **BLOCKED** | Diagnose: missing context → supply it and re-dispatch; reasoning ceiling → re-dispatch on a stronger model; task too large → split it into smaller dispatches; the plan itself is wrong → escalate to the user. |

Never ignore an escalation, and never force the same model to retry with nothing changed. A stuck implementer means something must change before the next attempt.

## Model Tiering

State the model **explicitly on every dispatch** — an omitted model inherits your session's, usually the most capable and most expensive, silently defeating this section.

- **Cheap tier:** transcription tasks (the plan text contains the complete code — the work is typing plus testing) and single-file mechanical fixes.
- **Mid tier, as a floor:** every reviewer, and every implementer working from prose. Turn count beats token price — cheap models routinely take two to three times the turns on multi-step work and cost more overall.
- **Top tier:** tasks needing design judgment or broad codebase understanding, and the final whole-branch review.

Scale reviewer models to the diff's size and risk: a small mechanical diff does not need the top tier; a subtle concurrency change does.

## Reviewer-Prompt Hygiene

- **Never pre-judge findings.** If your dispatch contains "do not flag X", "treat it as Minor at most", or "the plan chose this" — stop: you are pre-judging, usually to spare yourself a review loop. Let the reviewer raise it and adjudicate afterwards.
- **A plan-mandated defect is still a finding.** The plan does not grade its own work. Present the finding and the mandating plan text to the user and ask which governs — never dismiss the finding, never dispatch a fix that contradicts the plan without asking.
- The Global Constraints block is the reviewer's attention lens: binding requirements copied verbatim — exact values, exact formats, stated relationships between components. The template already carries the process rules.
- No open-ended directives ("check every call site", "run stress tests if useful") without a concrete, task-specific reason.
- Do not ask a reviewer to re-run tests the implementer already ran on the same code — the report file is the test evidence.

## Durable Progress

Conversation memory does not survive compaction. Controllers that lost their place have re-dispatched entire completed task sequences — the single most expensive failure this loop has. The ledger, not your todos, is the source of truth:

- On skill start, read `.skills/progress.md` if present; resume after the last complete task.
- After compaction or resume, trust the ledger and `git log` over your own recollection — the commits the ledger names exist in git even when your context no longer remembers writing them.
- Never re-dispatch a task the ledger marks complete.
- `.skills/` is git-ignored scratch; if it is wiped, reconstruct progress from `git log`.

## After the Last Task

1. **Whole-branch review.** REQUIRED SUB-SKILL: use `code-review` with base = the branch point (`git merge-base main HEAD`) — never a mid-branch sha. Point it at the ledger's Minor-findings list for triage. Run it on the top model tier. *Done when: the verdict is in.*
2. **One fixer.** If it returns findings, dispatch ONE fix subagent carrying the complete findings list — never one fixer per finding; each extra fixer rebuilds context and re-runs suites, and a per-finding fix wave can cost more than the whole plan did. Re-review after. *Done when: the review is clean.*
3. **Finish.** REQUIRED SUB-SKILL: use `finish-branch`. *Done when: the user has chosen merge / PR / keep / discard.*

## Inline Fallback (no subagent capability)

Same loop, no dispatches: implement each task yourself, in order, from its brief. REQUIRED SUB-SKILL: use `tdd` for every step. Keep the same ledger appends per task and the same end-of-plan review via `code-review`. On a blocker, a failing verification, or a plan gap: stop and ask the user — never guess through it. The main/master consent rule still applies.

## Red Flags — Never

- Run two implementers on the same plan in parallel (they will collide).
- Hand a subagent the whole plan file — the brief from `task-brief` is its world.
- Use `HEAD~1` as a review base.
- Skip the re-review after a fix, or accept a review missing either verdict.
- Move to the next task with open Critical/Important findings.
- Let the implementer's self-review substitute for the task review — both are required.
- Tell a reviewer what not to flag, or pre-rate a finding's severity in the dispatch.
- Dispatch a reviewer without a diff package — build it first and name the path.
- Re-dispatch a task the ledger already marks complete.
- Pause between tasks to ask permission to continue.
- Fix reviewer findings in your own context instead of dispatching a fixer.
- Start implementation on main/master without the user's explicit consent.
