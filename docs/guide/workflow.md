# The workflow: five commands, one board

Every piece of work is a ticket. A ticket is always in exactly one state. Each move between
states belongs to exactly one command or one person, so the board always tells the
truth about what waits on whom.

Design and evidence: `docs/design/2026-10-19-closed-workflow.md`.

## The five commands

| Command | What you get |
|---|---|
| `/idea <text>` | The idea is a ticket in Shaping, with its tier and its open questions |
| `/shape #N` | The spec (or the root cause, for a bug), stopping at each approval. When the plan is approved, the ticket is Ready |
| `/go [#N…]` | Each named ticket, or every Ready one, built, reviewed and opened as a PR. One message at the end |
| `/board` | Everything waiting on you, what the agents are doing, and where the board and the repo disagree |
| `/cut-release` | A release. The tickets it ships read `shipped` |

Every other skill still works when you type it (`/deliver-issues`, `/show-run-status`,
`/triage`, `/sweep-backlog`, …). The five are the short path.

## The states

```
          you                        you                       you
          approve                    answer                    merge
             ▼                          ▼                         ▼
Inbox ──► Shaping ──► Ready ──► Building ──► In review ──► Done ──► Shipped
  │          │          │          │   ▲          │
  │          ▼          │          ▼   │          ▼
  │     Needs input ◄───┴──── Needs input ◄── (review needs you)
  ▼
Won't do                 Human-only
```

| State | Label role (`docs/agents/triage-labels.md`) | Who moves it in | Who moves it out |
|---|---|---|---|
| Inbox | `needs-triage` | `/idea`, `/triage` | `/idea` (after framing), `/triage` |
| Shaping | `shaping` | `/idea`, `/shape`, `/go` (a ready ticket with no spec) | **you approve**; then `plan-tasks` publishes it Ready |
| Ready | `ready-for-agent` | `plan-tasks`, `/publish-issues`, `/triage` | the build that claims it |
| Building | `building` + assignee | the build's tracker sync (`execute-common`) | `land-branch` when the PR opens |
| In review | `in-review` | `land-branch` | **you merge**; `Closes #N` closes it |
| Done | closed | the merge | `/cut-release` |
| Shipped | `shipped` | `/cut-release` | — |
| Needs input | `needs-info` | whoever asks you a question, on the ticket | **you answer** |
| Human-only | `ready-for-human` | `/triage` | you |
| Won't do | `wontfix` | you, or `/triage` and `/sweep-backlog` on your word | — |

You own three gates: **approve** (a spec, a plan, or a Notion draft when `Draft surface`
is `notion`), **answer** a question on a ticket, and **merge** a PR. Agents do the rest,
and they write state and comments only on the ticket they are working.

## A day with it

1. `/idea Vessel owners get an SMS when an invoice goes overdue` → #28 in Shaping, tier 2,
   four open questions on the ticket.
2. `/shape #28` → `requirements.md`, waiting for your approval. `/board` lists it under
   Shaping with that line. You approve; `/shape #28` again writes the design, then the
   plan. Approving the plan makes #28 Ready.
3. Before you leave: `/go`. Every Ready ticket is claimed (Building), built, reviewed and
   opened as a PR (In review). A ticket labelled Ready with no spec goes back to Shaping
   with a comment saying what it lacks. You get one message.
4. Next morning: `/board` → "Waiting on you: PR #14 (decision: …), PR #15, #25's
   question." You answer and merge; the merges close the tickets.
5. End of the sprint: `/cut-release` → v0.5.0, and its tickets read `shipped`.

A bug takes the same road. `/triage` confirms it and sends it to Shaping while the cause is
open. `/shape #N` runs `root-cause`. When you accept the cause and approve the fix
requirement and its `SHALL CONTINUE TO` guard, the ticket is Ready with `Requirements
covered:` naming both. `/go` then builds it test-first.

## Setting it up

`/configure-repo` maps the state roles to your tracker's labels. Four of them are newer:
`shaping`, `building`, `in-review` and `shipped`, proposed as `status:<role>`. Creating
the labels is a tracker write, so it asks first. On Linear, map each role to a workflow
state.
