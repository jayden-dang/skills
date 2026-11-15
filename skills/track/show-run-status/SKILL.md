---
name: show-run-status
version: 1.1.0
description: "Use when someone asks where one feature's build stands right now: is it done, what is left, why did the run stop, is it waiting on them. Produces a status report for that one build, read from the plan, ledger, git, tests, ticket and pull request at once. Not for every open ticket (board) or the roadmap (refresh-roadmap-status)."
---

# Show Run Status

Answer "where are we with `<CODE>`?" for a build that is running or stopped mid-way —
in the time it takes to walk into a meeting. Roadmap-level standing is
`/refresh-roadmap-status`; this is one feature's run.

## The Iron Law

```
EVERY LINE OF THE REPORT COMES FROM collect.sh. NO SOURCE IS SKIPPED.
```

Six baseline reports on one stopped build, without this skill, each read the sources
it happened to open. All six caught the stale ledger and the red working tree. Two
missed the decision parked for the operator in `implementation-notes.md` — one then
advised doing the very change that was parked. Two never said the last commit was
unpushed. Five said nothing true about the tracker ticket, still `ready-for-agent` and
unassigned while the work was half done.

## 1. Collect

Resolve `<CODE>` from what the operator named, else the feature on the current branch.
Run `scripts/collect.sh <CODE>` beside this file, from the repo root. It prints seven
sections — plan, ledger, git, tests, waiting on a person, tracker, pull request and
checks — and runs only the project's unit-test command. Change nothing else.
*Done when: all seven sections are in front of you.*

## 2. Report — these slots, in this order

1. **Done** — each task with the commit that delivers it (match commit subjects to the
   plan's task titles). Git wins over the ledger; a ledger line git contradicts goes
   to slot 6.
2. **In flight** — uncommitted changes and the task they belong to; the test result,
   saying whether it ran with uncommitted changes in it.
3. **Waiting on you** — every entry from "waiting on a person", with its options as
   written. `none` only when the section printed `none found`. Never recommend an
   option here as if it were decided.
4. **Not shipped yet** — unpushed commits (count, newest subject), PR, checks — as the
   `git` and `pull request` sections print them.
5. **Tracker** — the ticket's status and assignee as printed, and whether they match
   slots 1–2.
6. **Sources that disagree** — each mismatch in one line: which source says what, and
   which one is right.

Then one line the operator can say out loud, drawn only from slots 1–4.

## Red Flags

- A status line with no section of `collect.sh` behind it
- "Waiting on you: none" when the section printed an entry
- Recommending the parked option as the next step
- Omitting the tracker because "it is just bookkeeping"
