# `go`

> The named tickets, or every Ready one, built, reviewed and opened as a pull request each, ending in one message.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | `/go [#N…]` (user-invoked; `disable-model-invocation: true`) |
| **Reads** | what [`deliver-issues`](deliver-issues.md) reads |
| **Writes** | what `deliver-issues` writes: one branch and one pull request per ticket, and the state changes on each ticket |
| **Calls** | [`deliver-issues`](deliver-issues.md) |
| **Called by** | nobody — it is user-invoked |

## When it fires

When tickets are Ready and you want them turned into pull requests while you are away. It is the third of the [five commands](../workflow.md), after [`/shape`](shape.md).

## What it does

It runs [`deliver-issues`](deliver-issues.md). With IDs (`/go #23 #31`), the run covers those tickets only and every other ticket keeps its state. With no IDs it covers every Ready ticket. Each ticket is claimed (`building` and an assignee) when its build starts and moves to `in-review` when its pull request opens, with `Closes #N` in the body.

It ends with `deliver-issues`' one message: a row per ticket, then every **Needs a decision before merge** item.

## What the tests showed

With `/deliver-issues #23` as a user-invoked skill, one haiku run built only #23, so scoping was already a no-op; that run also skipped the claim at the start. `/go` exists as one of the five short commands, and `deliver-issues` became model-invocable (2.0.0) so that `/go` can invoke it. With `/go #23`, the run built only #23, claimed it, moved it to `in-review`, and put `Closes #23` in the pull request. See `skills/execution/go/TESTS.md`.

## See also

- [The workflow](../workflow.md) — the states and who moves each one
- [`deliver-issues`](deliver-issues.md) — the skill it runs
- [`/board`](board.md) — what the run left waiting on you
- Design: `docs/design/2026-10-19-closed-workflow.md`
