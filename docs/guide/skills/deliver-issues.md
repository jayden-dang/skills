# `deliver-issues`

> Every eligible ticket on the board, through its own build, review and landing, in one unattended run that ends with one message.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invocable since 2.0.0; `/deliver-issues` still works when typed. [`/go`](go.md) is the short way in |
| **Reads** | `docs/agents/issue-tracker.md`, `docs/agents/project.md` (`Default PR base:`), each ticket's `Blocked by:`, and each feature's `requirements.md`, `design.md` and `tasks.md` |
| **Writes** | one branch and one pull request per eligible ticket, through the skills it calls |
| **Calls** | [`build-in-waves`](build-in-waves.md), [`inspect-change`](inspect-change.md) and [`land-branch`](land-branch.md) with action `pr`, once per ticket |
| **Called by** | [`/go`](go.md) |

## When it fires

When you want the board's ready tickets turned into pull requests while you are away. It is the multi-ticket version of what a single ticket gets.

## What it does

A ticket is eligible when its status is the tracker's ready state and its `requirements.md`, `design.md` and `tasks.md` all read `Status: Approved`. Each other ready ticket is listed with the piece it lacks. Eligible tickets are ordered by `Blocked by:`.

For each eligible ticket, in order:

1. Branch from `Default PR base:`. A ticket blocked by one delivered in this run branches from that ticket's branch.
2. Build it with `build-in-waves`.
3. Review it with `inspect-change`.
4. Land it with `land-branch` as a pull request. A stacked ticket's pull request is based on its blocker's branch.

The rule behind it: a board of tickets is not a reason to skip any of the three steps for one of them.

## Named tickets, claims and in-review

Since 2.0.0 the run covers the tickets you name and no others; with no names it covers every ready ticket, as before. Every other ticket keeps its state. A ready ticket that cannot be built, because it has no approved spec, moves to `shaping` with a comment naming what is missing (1.1.0), so it leaves the ready column. Each ticket it builds is claimed when its build starts and moves to `in-review` when its pull request opens, through [`execute-common`](execute-common.md) and [`land-branch`](land-branch.md). See [the workflow](../workflow.md).

## When a question comes up

A sub-skill that would normally stop and ask you does not stop here. It builds the option that leaves every documented contract as it is, heads that pull request with **Needs a decision before merge**, and carries on with the rest of the board. The pull request is where you decide. A denied command is treated the same way: it is not retried, the run takes a route that needs none of it, and the skipped step is recorded in that pull request.

## The message

One message at the end: a table with one row per ready ticket (its pull request and base, or not eligible and what it lacks), then every **Needs a decision before merge** item with its pull request and the option built.

## What the tests showed

Four runs without the skill, on a board of four ready tickets. None used a build or review skill and none landed through `land-branch`. They opened 1 to 3 pull requests each, none of them reviewed by anyone but the author. Haiku runs parked a ticket on a question, and the ticket waiting on it as well.

With the skill, sonnet delivered 3 pull requests, with the late-fee one stacked, and left the spec-less ticket alone. Two haiku runs on the final text each delivered 3, with the questions in the message. A full run costs 10 to 20 times a baseline run. See `skills/execution/deliver-issues/TESTS.md`.

Not covered by the tests: the host agent cap, a change of plan from you mid-run, and GitHub or Linear trackers.

## See also

- [`build-in-waves`](build-in-waves.md) — the build step
- [`land-branch`](land-branch.md) — the landing step
- [`show-run-status`](show-run-status.md) — where one feature's run stands
- [`publish-issues`](publish-issues.md) — how tickets reach the board
