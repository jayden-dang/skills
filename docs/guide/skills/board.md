# `board`

> Everything on the board by state, starting with what waits on you, and every place the board and the repo disagree. Writes nothing.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | `/board` (user-invoked; `disable-model-invocation: true`) |
| **Reads** | `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, every open ticket and open PR, and the Notion drafts not yet signed off when `Draft surface` is `notion`. All of it goes through `scripts/board.py` |
| **Writes** | nothing, ever |
| **Calls** | nothing. Names [`/shape`](shape.md), [`/triage`](triage.md) and [`/show-run-status`](show-run-status.md) as the next step for a line |
| **Called by** | nobody — it is user-invoked |

## When it fires

When you sit down and want to know what is waiting on you and what the agents are doing. It is the fourth of the [five commands](../workflow.md). One feature's build in detail is [`/show-run-status`](show-run-status.md); the roadmap is [`/refresh-roadmap-status`](refresh-roadmap-status.md).

## What it does

It runs `scripts/board.py`, which prints every section every time. On GitHub it asks `gh` itself. On any other tracker the skill writes the open tickets and PRs as JSON first, using the ops in `docs/agents/issue-tracker.md`.

The report has three parts, in this order:

1. **Waiting on you.** Each open PR to review and merge (with its parked decision quoted), each `needs-info` question, each Shaping ticket, each untriaged ticket, each Human-only ticket, and each Notion draft awaiting sign-off. Each line carries the one thing to do.
2. **With agents.** What is being built and by whom, then the ready tickets that [`/go`](go.md) would take next.
3. **Board and repo disagree.** A ready ticket with no approved spec, an open PR whose ticket lacks `in-review`, an open ticket whose spec reads `Implemented` or `Shipped`, and a ticket with two state roles. Each line comes with the edit that fixes it. The skill does not make the edit.

It closes with one sentence you can say at standup.

## What the tests showed

Three runs without the skill, asked "What's waiting on me this morning?", all found the open PR's parked decision and the `needs-info` question. Two never mentioned an untriaged ticket, and none noticed a ticket labelled `ready-for-agent` with no spec behind it.

With the skill, all three ran the script and named all four. No run wrote to the tracker. See `skills/track/board/TESTS.md`.

Not covered: Linear, Notion drafts passed with `--drafts`, and a board of more than 30 tickets.

## See also

- [The workflow](../workflow.md) — the states and who moves each one
- [`/show-run-status`](show-run-status.md) — one feature's build in detail
- [`/sweep-backlog`](sweep-backlog.md) — your own assigned tickets, with one question
- Design: `docs/design/2026-10-19-closed-workflow.md`
