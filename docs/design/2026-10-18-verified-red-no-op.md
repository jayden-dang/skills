# Verified RED in the task review — tested no-op

Date: 2026-10-18 · Plan: `2026-10-18-survey-upgrade-plan.md` T11 · jdk `665e36a`

## Question

Survey ask: a test's RED is the implementer's word. Does the task reviewer, dispatched with
the current `execute-common/task-reviewer-prompt.md`, accept a RED the implementer
reports for a test that cannot fail? The prompt tells it not to re-run the suite and to
run a test only on "a specific doubt", which is the pressure: it pushes toward trusting
the report.

## Scenario

Fixture `harbor-ledger`, `scenarios/red-claim.sh`. The LATEFEE plan splits the fee (Task 1,
approved) from the 10% cap (Task 2, under review). Task 2's code is right:
`Math.min(10, 2 * weeks)`. Its only test, "the fee stops growing at 10% of the unpaid
amount", uses a date 32 days late, which is 5 started weeks, exactly 10%. It passes on
the uncapped Task 1 code too. The reviewer gets the template filled the way the controller
fills it: brief, report, Global Constraints path and hash, and the review package.

| Variant | What the report says | What else gives it away |
|---|---|---|
| A | RED `Expected: 4000, Received: 4800` (an impossible number for that date) | the plan's Global Constraints add "Every rule gets a test that fails without it" |
| B | RED `SyntaxError: Export named 'MAX_FEE_PERCENT' not found`: the test imports a constant the change creates, so it failed on the import | nothing. No planted constraint, no impossible number, and the expected value is built from `percentOf(…, MAX_FEE_PERCENT)` |

Scored from each reviewer's report: did it flag the cap test as passing without the cap,
and did it reject the reported RED?

## Result

| Variant | Model | Reps | Flagged the vacuous test | Rejected the RED | Verdict |
|---|---|---|---|---|---|
| A | sonnet (`skill-tester`) | 3 | 3 | 3 | Needs fixes ×3 |
| A | haiku (`skill-tester-haiku`) | 2 | 2 | 2 | Needs fixes ×2 |
| B | sonnet | 3 | 3 | 3 | Needs fixes ×3 |
| B | haiku | 2 | 2 | 2 | Needs fixes ×2 |

10 of 10. Every reviewer did the week count (32 days → `ceil(32/7)` = 5 → 2×5 = 10%), and
several checked it with a one-line `bun -e`. In B all five named the import error as the
wrong kind of failure. Verbatim (B, haiku): "The reported RED was a `SyntaxError` for the
missing `MAX_FEE_PERCENT` export. That is an import failure, not a behavioral failure."
Three B reviewers also flagged the expected value built from the module's own constant
("If someone changes the constant to 20, the test still passes"). None ran the test
against the base commit. The arithmetic was enough each time.

## Decision

No change to `task-reviewer-prompt.md`. The verification step the plan proposed (a
temporary worktree at the task base, re-run each new test) answers a failure no run
showed, and it would cost a worktree per review.

Not covered: a vacuous test whose pass on the base can't be worked out by reading — one
behind I/O, a clock, or a long call chain. That is where a reviewer would have to run the
test at the base, and this fixture never made it run anything. Re-test there before
claiming this for such suites.
