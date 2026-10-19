# One closed workflow — the ticket is the hub

Date: 2026-10-19. Status: **Approved by the owner 2026-10-19.** Method: `author-skills`.
Every transition ships only after its own RED.

## Contents

1. [Why](#1-why)
2. [The state machine](#2-the-state-machine)
3. [Who moves each transition](#3-who-moves-each-transition)
4. [Five commands](#4-five-commands)
5. [Configuration](#5-configuration)
6. [Tasks](#6-tasks)
7. [Decisions taken](#7-decisions-taken)

## 1. Why

jdk keeps two state systems that never meet.

- **The spec's `Status:`** (`Draft → Approved → In-progress → Implemented → Shipped`) has a
  writer and a reader at every step.
- **The tracker's state labels** are written at the two ends only.
  - `ready-for-agent` is applied by `triage`, `publish-issues` and `plan-tasks`. No skill
    removes it.
  - `ready-for-human` is applied by `triage`. No skill reads it.
  - Nothing marks a ticket as being built or in review.
  - A ticket closes only when the PR says `Closes #N`, and that happens only when the branch
    name carries the ID.

The T20 dogfood on klynt found all four `ready-for-agent` tickets already `Implemented` and
still labelled.

The owner's ask: one workflow that is simple to use and strong enough for people and
agents together. A board shows what waits on whom, and the person only does what only a
person can do.

## 2. The state machine

```
          person                     person                    person
          approves                   answers                   merges
             ▼                          ▼                         ▼
Inbox ──► Shaping ──► Ready ──► Building ──► In review ──► Done ──► Shipped
  │          │          │          │   ▲          │
  │          ▼          │          ▼   │          ▼
  │     Needs input ◄───┴──── Needs input ◄── (review needs a person)
  ▼
Won't do                 Human-only
```

| State | Meaning | Canonical role (`triage-labels.md`) | GitHub |
|---|---|---|---|
| Inbox | new, nobody has looked | `needs-triage` (exists) | label |
| Shaping | spec or root cause being written | `shaping` (new) | label |
| Ready | spec approved; anyone may take it | `ready-for-agent` (exists) | label |
| Building | claimed and being built | `building` (new) | label + assignee |
| In review | PR open, waiting on a person | `in-review` (new) | label |
| Needs input | waiting on one named question | `needs-info` (exists) | label + the question as a comment |
| Human-only | an agent cannot do it | `ready-for-human` (exists) | label |
| Done | merged | — | closed by the PR's `Closes #N` |
| Shipped | in a release | `shipped` (new) | label on the closed issue |
| Won't do | closed, not doing | `wontfix` (exists) | label + closed |

The canonical role names stay. `triage`, `publish-issues` and `sweep-backlog` keep
working unchanged, and only four roles are new. **One state label per open ticket**: a
transition removes the old state label in the same edit that adds the new one.

The spec's `Status:` stays the record of what was approved. The skill that moves a
ticket also moves its spec in the same step: Ready ↔ `Approved`, Building ↔
`In-progress`, Done ↔ `Implemented`, Shipped ↔ `Shipped`.

## 3. Who moves each transition

| Transition | Owner | Today | Task |
|---|---|---|---|
| (chat) → Inbox | `/idea`, at the operator's request | — | W7 |
| Inbox → Shaping | `frame-change`, once a tier ≥1 is stated on a ticket | — | W7 |
| Shaping → Ready | **person approves**; then `plan-tasks` publish or `publish-issues` | exists | — |
| Ready → Building | `execute-common` session preflight: claim (assignee + `building`) | **missing** | W2 |
| Building → In review | `land-branch` when the PR opens, plus `Closes #N` from the claimed ticket | **missing** | W3 |
| any → Needs input | the skill that parks the question: comment + `needs-info` | partial (PR note only) | W4 |
| Needs input → previous state | the skill that resumes, after reading the answer | — | W4 |
| In review → Done | **person merges**; the tracker closes it | exists if linked | W3 |
| Done → Shipped | `/cut-release` | **missing** | W5 |
| → Human-only, → Won't do | `triage`, `sweep-backlog` (on the operator's word) | exists | — |

A person owns three gates: approve, answer, merge. The TPM's Notion sign-off is the
approve gate when `Draft surface` is `notion` (T3c).

## 4. Five commands

| Command | Does | Routes to |
|---|---|---|
| `/idea <text>` | Files the idea as a ticket in Inbox and frames it (tier, neighbours, questions). | `frame-change` → `clarify-decisions`, `load-subgraph`, `research`, `run-spike` |
| `/shape <ID>` | Writes what the tier needs, then stops at the approve gate. | `specify-behavior`, `design-solution`, `plan-tasks`, or `root-cause` |
| `/go [ID…]` | Takes the named tickets, or every Ready one, to In review. One PR per ticket, one message at the end. | `deliver-issues` |
| `/status [ID]` | The board, by state, led by **Waiting on you**: In review, Needs input with its question, Human-only, and drafts awaiting sign-off. With an ID it gives that ticket's build detail. | own collector; `show-run-status` for one ticket |
| `/cut-release` | Done → Shipped (exists; stays user-only because it crosses to production). | — |

A `disable-model-invocation` skill cannot be invoked by another skill, so the routes need
model-invocable targets. **`deliver-issues` and `show-run-status` drop the flag.** Their
descriptions become model-facing routing lines, and `/deliver-issues` and
`/show-run-status` still work when typed. Every other skill is unchanged and still typed
by name when wanted. The guide leads with the five.

## 5. Configuration

- **`templates/agents/triage-labels.md`:** four new roles (`shaping`, `building`,
  `in-review`, `shipped`), each mapped to a repo label. The rule becomes "exactly one
  state role per open ticket".
- **`configure-repo`:** the label-mapping follow-up proposes `status:*` names for the new
  roles. Creating the labels is a tracker write, so the skill lists the `gh label create`
  commands for the operator unless they say to run them.
- **Linear:** each role maps to a workflow state name rather than a label. Labels are the
  first target (decision 2).

## 6. Tasks

Each task has RED on haiku and sonnet first, and is a tested no-op when the baseline
already complies.

| ID | Task | RED to show |
|---|---|---|
| W0 | Fixture: `bin/gh` grows a stateful issue store (labels, assignees, comments, close, `Closes #N` on a scripted merge) | — |
| W1 | Roles in `triage-labels.md` + `configure-repo` mapping | a configured repo has no state for "being built" or "in review" (structural; ships with W2) |
| W2 | Claim at Ready → Building (`execute-common` tracker-sync) | two `/deliver-issues` sessions take the same ticket; the ticket stays `ready-for-agent` while it is being built |
| W3 | In review and `Closes #N` (`land-branch`) | the PR opens and the ticket still reads Ready; the branch lacks the ID, so there is no `Closes`, and the merge leaves the ticket open (klynt 4/4) |
| W4 | Needs input on the ticket (`deliver-issues` / `execute-common`) | a parked question lives only in the PR or the final message; the board shows nothing waiting |
| W5 | Shipped (`cut-release`) | a release leaves the shipped tickets indistinguishable from merged-not-released |
| W6 | `/status` board, Waiting on you first | with today's skills, "what's waiting on me" misses In review, Human-only, or a parked question |
| W7 | `/idea`, `/shape`, `/go` entries; drop the flag on `deliver-issues` and `show-run-status` | trigger tests both ways; `/go LED-7` builds one named ticket |
| W8 | Guide: one workflow page leading START-HERE, AGENTS.md routing, CHANGELOG (with the missing `execute-common` 2.11/2.12 and `run-spike` 2.0.0 entries) | — |
| W9 | Dogfood on a real GitHub board | — |

Order: W0 → W1+W2 → W3 → W4 → W5 → W6 → W7 → W8 → W9. `execute-common` is touched by W2
and W4, so they run serially.

## 7. Decisions taken

The owner decided these on 2026-10-19.

1. **Budget.** The headless cap rises to 95 USD.
2. **Tracker order.** GitHub first, using labels. Linear maps the same roles to workflow
   states.
3. **Old commands stay.** The new commands wrap the old skills, and every old command still
   works.
4. **Agent writes on the ticket in hand.** The agent changes a ticket's state and comments
   on it without asking. Creating or closing a ticket still follows the repo's working
   agreement. `/idea` creates its ticket because the operator asked for it.
