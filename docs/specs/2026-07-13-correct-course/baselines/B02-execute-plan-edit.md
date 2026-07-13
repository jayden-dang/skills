# B02 — execute-plan edit

Baseline for Task 2: wiring two of `skills/execution/execute-plan/SKILL.md`'s escalation
signals to hand off to `correct-course`. Each scenario is walked by hand against the
edited skill body (this repo verifies skills by baseline scenario, not an automated
harness — see Global Constraints). RED = walked before the edit (the branch still
dead-ends at escalate-to-user, so the hand-off scenarios fail by definition); GREEN =
walked after the edit, confirmed to hold.

## S1 — Plan-is-wrong hand-off

In the **Implementer Status Handling** table, the **BLOCKED** row's final diagnose clause
— "the plan itself is wrong" — now pauses and hands off to `correct-course` instead of
dead-ending at escalate-to-user.

**Walk:** Read the BLOCKED row. Confirm the clause reads `the plan itself is wrong →
pause and REQUIRED SUB-SKILL: use \`correct-course\`.` Confirm the hand-off is written as
`` REQUIRED SUB-SKILL: use `correct-course` `` prose, never an `@`-link.

RED (before edit): the clause reads `the plan itself is wrong → escalate to the user` —
no hand-off exists, scenario fails.
GREEN (after edit): the clause routes to `correct-course` as above.

`[CCOURSE-1.1]`

## S2 — Circuit-breaker root-cause hand-off

In step 8's Fix loop, when a finding survives 3 fix→re-review cycles, the circuit breaker
runs a root-cause analysis to find the lowest invalidated artifact. If that artifact sits
above the current task (the plan, design, or requirements — not just this task's
approach), the breaker hands off to `correct-course`. A mere hard bug, where the
invalidation is task-local, still escalates to the user / stays in the fix flow exactly
as before — it does not route to `correct-course`.

**Walk:** Read the Circuit breaker sentence in step 8. Confirm it now reads: stop looping
→ run a root-cause analysis for the lowest invalidated artifact → if above the current
task (plan/design/requirements), `` REQUIRED SUB-SKILL: use `correct-course` ``;
otherwise escalate to the user with the finding and the three attempts, exactly as for
BLOCKED → never spend a fourth cycle on it. Confirm the task-local branch (a hard bug,
invalidation scoped to this task alone) is unchanged from today's escalate-to-user
behavior — it is the "otherwise" branch, not a hand-off.

RED (before edit): the sentence has no root-cause step — any 3-cycle survivor escalates
to the user unconditionally, with no `correct-course` hand-off possible; scenario fails.
GREEN (after edit): the root-cause branch exists and routes correctly by artifact level.

`[CCOURSE-1.2]`

## S3 — Guard, other stops unchanged

The other three BLOCKED diagnose branches (missing context, reasoning ceiling, task too
large), a BLOCKED you cannot resolve for another reason, genuine ambiguity, and
all-tasks-complete all behave exactly as today — none of them route to `correct-course`.

**Walk:** Read the BLOCKED row's first three clauses: `missing context → supply it and
re-dispatch`, `reasoning ceiling → re-dispatch on a stronger model`, `task too large →
split it into smaller dispatches` — confirm each is byte-for-byte identical to the
pre-edit text, with no mention of `correct-course`. Read the "only legitimate stops" line
("The only legitimate stops: a BLOCKED status you cannot resolve, ambiguity that
genuinely prevents progress, or all tasks complete") in the intro — confirm it is
unchanged and still names only those three cases, with no fourth case added. Confirm the
redispatch cap line ("Cap redispatches at 2 for the same task; if it is still not DONE
after the second, escalate to the user rather than burning a third.") is unchanged.

`[CCOURSE-1.4]`

## S4 — Guard, pre-flight unchanged

The pre-flight plan review (step 5 of Setup) still batches its findings into one
pre-dispatch question to the user, entirely unaffected by this feature.

**Walk:** Read step 5, "Pre-flight plan review." Confirm the text — including "Batch ALL
findings into ONE question to the user — each finding shown beside the plan text that
mandates it, asking which governs — before any dispatch. One interrupt, not one per
discovery mid-run." — is byte-for-byte identical to the pre-edit text, with no
`correct-course` reference added anywhere in the step.

`[CCOURSE-1.5]`

## Coverage self-check

Every one of Task 2's 4 IDs appears in at least one tag above: 1.1, 1.2, 1.4, 1.5 — 4 of
4, none missing, none double-defined.
