# `sweep-backlog`

> Your assigned tickets in one classified, ordered list, with one question for every call that needs you. Nothing is written to the tracker until you answer.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | `/sweep-backlog` (user-invoked; `disable-model-invocation: true`) |
| **Reads** | `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, every open ticket assigned to you (body, comments, `Blocked by:`), and git history on all branches through `scripts/landed.sh` |
| **Writes** | nothing until you answer the question. After that, status changes and a why-comment on each ticket you decided |
| **Calls** | nothing. Names [`/publish-issues`](publish-issues.md) when a new ticket is needed |
| **Called by** | nobody — it is user-invoked |

## When it fires

When you want to walk into planning with a clean list of your own tickets. "Me" is the name you give, else `git config user.name`. Tickets that have not been triaged yet belong to [`/triage`](triage.md); this skill reads tickets that already passed it.

## What it does

It reads every open ticket assigned to you, including the comments. Tickets assigned to other people are counted, not listed.

Then it runs `scripts/landed.sh` over all of them. The script finds commits that name a ticket ID, says whether each one is on the default branch, and lists the branches that hold it. A ticket with a commit row is never called `ready` from reading the checked-out code, because that code is only one branch.

Each ticket gets exactly one class, first match wins:

| Class | Rule |
|---|---|
| `landed` | a commit names it. The reply says where |
| `duplicate` | another ticket of yours asks for the same outcome |
| `obsolete` | a later comment or doc says the need is gone, quoted with its date |
| `blocked-external` | someone outside the team must act first |
| `blocked` | `Blocked by:` names an open ticket |
| `ready` | none of the above |

The `ready` and `blocked` tickets are put in dependency order.

## The reply

Three parts, in this order:

1. **The list.** One line per ticket: ID, title, class and the evidence.
2. **One question.** Every decision only you can make, such as keep or close a duplicate pair, close an obsolete ticket, or close a landed one now. One item per ticket, each with a **Pick** and one line of why. You answer "all picks" or name the numbers to change. Tickets that are only waiting stay out of the question.
3. **Counts.** Tickets read, how many belong to others, and that nothing has been written yet.

## After you answer

It applies exactly what you answered. Status values come from `docs/agents/triage-labels.md`, never a word it invents. Each change gets a comment that cites the evidence. It reads every edited ticket back and reports what changed.

## What the tests showed

Six runs without the skill, on a backlog of 10 tickets. All six missed that one ticket was already fixed on a branch other than the one checked out. Five of six edited the tracker before asking, using four different status words, and three of those closed tickets the TPM had approved. Only one of six asked a single question with picks.

With the skill, all six runs found the fix on `dev`, left the tracker unchanged and asked exactly the three real decisions, one per ticket. See `skills/track/sweep-backlog/TESTS.md`.

## See also

- [`triage`](triage.md) — the incoming queue this skill starts after
- [`publish-issues`](publish-issues.md) — where new tickets come from
- [`refresh-roadmap-status`](refresh-roadmap-status.md) — standing at the roadmap level instead of your own tickets
