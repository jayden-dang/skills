# `show-run-status`

> Where one feature's build stands right now, read from every source at once, in time to say it out loud before a meeting.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | `/show-run-status` (user-invoked; `disable-model-invocation: true`) |
| **Reads** | everything `scripts/collect.sh <CODE>` prints: the plan, the ledger, git, the unit tests, entries waiting on a person, the tracker ticket, and the pull request with its checks |
| **Writes** | nothing. The only command it runs besides reading is the project's unit-test command |
| **Calls** | nothing |
| **Called by** | nobody — it is user-invoked |

## When it fires

When you ask "where are we with `<CODE>`?" about a build that is running or stopped halfway. The code is the one you name, else the feature on the current branch. For standing across the whole roadmap, use [`/refresh-roadmap-status`](refresh-roadmap-status.md). This skill is one feature's run.

## One script, seven sections

`scripts/collect.sh` prints seven sections, even when one is empty: plan, ledger, git, tests, waiting on a person, tracker, and pull request and checks. Every line of the report must come from one of them. No source is skipped, because the report used to depend on which files the agent happened to open.

## The report

Six slots, in this order:

1. **Done.** Each task with the commit that delivers it. Git wins over the ledger.
2. **In flight.** Uncommitted changes, the task they belong to, and the test result, saying whether the tests ran with uncommitted changes in them.
3. **Waiting on you.** Every parked decision with its options as written. It never recommends one as if it were decided.
4. **Not shipped yet.** Unpushed commits, the pull request and its checks.
5. **Tracker.** The ticket's status and assignee, and whether they match slots 1 and 2.
6. **Sources that disagree.** Each mismatch in one line, with which source is right.

It ends with one line you can say out loud, drawn only from slots 1 to 4.

## What the tests showed

Six runs without the skill, on a build stopped halfway. All six found the committed tasks, the uncommitted edit and the red suite. Two missed the decision parked for the operator, and one of them then advised doing the very change that was parked. Two did not say the last commit was unpushed. Five said nothing true about the ticket, which was still `ready-for-agent` and unassigned.

With the skill, all six runs named the parked decision with both options and no pick, the unpushed commit, the stale ticket, and wrote nothing. See `skills/track/show-run-status/TESTS.md`.

## See also

- [`build-in-waves`](build-in-waves.md) — the run this skill reports on
- [`refresh-roadmap-status`](refresh-roadmap-status.md) — the same question for the whole plan
- [`write-handoff`](write-handoff.md) — a resumable document when you stop for the day
