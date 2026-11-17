# `go`

> The named tickets, or every Ready one, built, reviewed and opened as a pull request each, ending in one message.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invoked when its description matches, or `/go` |
| **Reads** | what [`go`](go.md) reads |
| **Writes** | what `go` writes: one branch and one pull request per ticket, and the state changes on each ticket |
| **Calls** | [`go`](go.md) |
| **Called by** | nobody yet — it fires on what the user asks, or on `/go` |

## When it fires

When tickets are Ready and you want them turned into pull requests while you are away. It is the third of the [five commands](../workflow.md), after [`/shape`](shape.md).

## What it does

It runs [`go`](go.md). With IDs (`/go #23 #31`), the run covers those tickets only and every other ticket keeps its state. With no IDs it covers every Ready ticket. Each ticket is claimed (`building` and an assignee) when its build starts and moves to `in-review` when its pull request opens, with `Closes #N` in the body.

It ends with `go`' one message: a row per ticket, then every **Needs a decision before merge** item.

## What the tests showed

With `/go #23` as a user-invoked skill, one haiku run built only #23, so scoping was already a no-op; that run also skipped the claim at the start. `/go` exists as one of the five short commands, and `go` became model-invocable (2.0.0) so that `/go` can invoke it. With `/go #23`, the run built only #23, claimed it, moved it to `in-review`, and put `Closes #23` in the pull request. See `skills/execution/go/TESTS.md`.

## Modes folded in (2026-11-15)

Each is a file beside `SKILL.md`, opened on the condition `SKILL.md` names.

- `deliver.md` — the delivery run itself: the frontier of ready tickets, one build, review and pull request per ticket, one message at the end.

## Tending the PRs before the message (1.4.0, 2026-11-17)

Inside a run, `land-branch` opens each PR and returns without waiting on its checks, so the next
ticket starts at once. Once every ticket has its PR, the run tends each one, the lowest in a stack
first, in `land-branch`'s tend mode. That takes it to merge-ready or a named blocker, and the
message gives each PR's merge state. Nothing is merged.

## See also

- [The workflow](../workflow.md) — the states and who moves each one
- [`go`](go.md) — the skill it runs
- [`/board`](board.md) — what the run left waiting on you
- Design: `docs/design/2026-10-19-closed-workflow.md`
