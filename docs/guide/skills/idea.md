# `idea`

> An idea becomes a ticket on the board, framed, waiting in Shaping with its tier and its open questions.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | `/idea <the idea>` (user-invoked; `disable-model-invocation: true`) |
| **Reads** | `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, the repo's working agreement for new tickets |
| **Writes** | one ticket and one comment on it, or a draft naming who must approve it when the working agreement gates new tickets |
| **Calls** | [`frame-change`](frame-change.md) |
| **Called by** | nobody — it is user-invoked |

## When it fires

When you have an idea and want it on the board, not in your head. It is the first of the [five commands](../workflow.md); [`/shape #N`](shape.md) is the next.

## What it does

1. **File it.** One ticket: the title is the idea in a line, the body is your words verbatim plus anything you linked. It gets exactly one state role, `needs-triage`. If the working agreement gates new tickets, it drafts the ticket, creates nothing, and says who must approve it.
2. **Frame it.** It runs [`frame-change`](frame-change.md) on the idea.
3. **Record the frame.** In one edit the ticket swaps `needs-triage` for `shaping`. A comment carries the stated tier, the neighbours found, and the open questions, numbered. Tier 0 skips Shaping: the ticket goes straight to `ready-for-agent`.

It ends with the ticket's URL and the next command, `/shape #N`.

## What the tests showed

Without the skill, with an open working agreement, all three runs filed a ticket. One labelled it `needs-info` and `status:shaping` at once, so the board showed it in two columns, and nothing recorded the frame on the ticket. With an agreement that gates new tickets, both runs drafted and named the approver, which is correct.

With the skill, all three filed with `needs-triage`, stated tier 2, swapped to `status:shaping` as the only state role, and commented the tier and numbered questions. See `skills/track/idea/TESTS.md`.

Not covered: tier 0, which should go straight to Ready.

## See also

- [The workflow](../workflow.md) — the five commands and the states
- [`/shape`](shape.md) — the next command
- [`frame-change`](frame-change.md) — the framing it runs
- [`/triage`](triage.md) — the same inbox, for tickets other people file
- Design: `docs/design/2026-10-19-closed-workflow.md`
