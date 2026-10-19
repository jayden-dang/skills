# One closed workflow — the ticket is the hub

Date: 2026-10-19. Status: **Approved 2026-10-19; W0–W10 done.** Method: `author-skills`.
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
| `/board [ID]` | The board, by state, led by **Waiting on you**: In review, Needs input with its question, Human-only, and drafts awaiting sign-off. With an ID it gives that ticket's build detail. | own collector; `show-run-status` for one ticket |
| `/cut-release` | Done → Shipped (exists; stays user-only because it crosses to production). | — |

`/status` is taken by Claude Code itself (account and connection status), so the board
command is `/board`.

A `disable-model-invocation` skill cannot be invoked by another skill, so the routes need
model-invocable targets. **`deliver-issues` drops the flag** (`/go` invokes it). `show-run-status` keeps it: `/board #N` names it for the operator rather than invoking it. Their
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
| W6 | `/board`, Waiting on you first | with today's skills, "what's waiting on me" misses In review, Human-only, or a parked question |
| W7 | `/idea`, `/shape`, `/go` entries; drop the flag on `deliver-issues` and `show-run-status` | trigger tests both ways; `/go LED-7` builds one named ticket |
| W8 | Guide: one workflow page leading START-HERE, AGENTS.md routing, CHANGELOG (with the missing `execute-common` 2.11/2.12 and `run-spike` 2.0.0 entries) | — |
| W9 | Dogfood on a real GitHub board | — |

> **Status**
>
> - W0 done: `bin/gh` is a stateful issue store; scenarios `gh-board.sh`, `gh-roles.sh`, `gh-light.sh`, `gh-released.sh`, `gh-release-steps.sh`, `wf-run.sh` and `wf-score.py`.
> - W1 shipped with W2: `configure-repo` 1.13.0 and the four roles in `triage-labels.md`.
> - W2 shipped: `execute-common` 2.13.0. RED 0/3 claimed; GREEN claim 5/5 after the pointer fix.
> - W3 shipped: `land-branch` 4.5.0. RED `Closes #23` 1/3, in-review 0/3, closed after merge 1/3; GREEN `Closes` 5/6, in-review 4/4 where `land-branch` ran.
> - W4 shipped as `deliver-issues` 1.1.0: a ready ticket that cannot be built leaves the ready column for `shaping` with a comment. RED 0/3, GREEN 3/3. The parked-question-as-`needs-info` part has no run in any `TESTS.md`.
> - W5 shipped: `cut-release` 1.3.0. RED 0/3 changed the ticket; GREEN haiku 2/2, sonnet 1/1.
> - W6 shipped: `board` 1.0.0. RED 2/3 missed the untriaged ticket and 0/3 caught the ready ticket with no spec; GREEN 3/3 on both, 0 tracker writes.
> - W7 shipped: `idea` 1.0.0 (GREEN 3/3 on one state role and the frame comment), `shape` 1.0.0 (2/2), `go` 1.0.0 and `deliver-issues` 2.0.0 (`/go #23` built only #23 and kept the claim, in-review, `Closes` chain; 0/3 should-not-fire runs loaded a skill). `plan-tasks` 1.9.0 is the RED behind `shape`: 2/3 left two state roles, GREEN 4/4.
> - W8 done: this sync (workflow guide, AGENTS.md, START-HERE, skill pages, CHANGELOG).
> - W9 pending: dogfood on a real GitHub board.

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

## 8. W9 — dogfood on the klynt board (2026-10-19)

KlyntLabs/klynt (GitHub). The owner approved these writes: the four `status:*` labels,
closing the implemented tickets, triage, and one `/idea` ticket. The mapping went in as
a PR. All skill runs were headless sonnet or haiku, from a sandbox clone of the owner's
checkout with its remote removed. The owner's checkout and its 18 unpushed commits were
not touched.

| Step | Writes | Result |
|---|---|---|
| `/board`, read-only through the `gh` guard (haiku, sonnet) | 0 | Both ran `board.py`. It called the four stale `ready-for-agent` tickets spec-less: klynt's catalog writes the Spec cell as a markdown link, and `learning.md` has a blank line inside its table. **Fixed in `board` 1.0.1**, and the same table bug in `land-branch` 4.5.1 (`owner-notice.py`). Re-run: five open tickets whose spec reads `Implemented`: #258, #253, #252, #243, and #261 [CCOL], which T20 had missed. |
| Labels | 4 created | `status:shaping`, `status:building`, `status:in-review`, `status:shipped` |
| Mapping | PR #265 | `docs/agents/triage-labels.md` gains the four roles, on a branch from `origin/dev` |
| Close the implemented | 5 closed | Each closed with a comment citing the spec path, `Status: Implemented` and the commit. None was marked shipped, since no release is confirmed. |
| `/triage` #262, #260, #242 (sonnet) | 0, then 6 | The first run stopped for confirmation, as the skill says. After the owner chose: #242 `ready-for-agent`, #262 and #260 `ready-for-human`, each with a brief and one state label. |
| `/idea` (sonnet) | 1 issue, 1 edit, 1 comment | #266 "Export flashcard review history as CSV", `status:shaping`, with a frame comment. It found that FLASH-12.3 must change for the export. It reported that `docs/guide/workflow.md` is missing in the consuming repo, **fixed in `idea`, `shape` and `go` 1.0.1**. |
| `/board` after | 0 | #266 Shaping; #262 and #260 Human-only; PR #265 In review; #242 Ready but flagged as having no spec. |

**Open design gap (W10).** `/triage` makes a confirmed bug `ready-for-agent` with an agent
brief. `/go` (`deliver-issues`) and `/board` count a ticket as Ready only when its spec
triad is `Approved`. So #242 sits in Ready, but nothing will build it. There are two ways
to close the gap, and the owner decides:
- Triage puts a bug that needs a root cause into `shaping`. Then `/shape` runs
  `root-cause` and writes the mini-spec.
- `deliver-issues` gains a tier-1 lane: a ticket with a triage agent brief goes through
  `root-cause`, then a `test-first` fix, then review, then landing.

## 9. W10: bugs reach Ready through Shaping (2026-10-19), option A

The owner chose to route bugs through Shaping.

| Skill | RED | GREEN |
|---|---|---|
| `triage` 1.1.0: a bug whose cause is still open goes to `shaping` | klynt #242: 3/4 recommended `ready-for-agent` | 3/3 `status:shaping`, 0 writes |
| `shape` 1.1.0: tier 1 ends Ready, with `Requirements covered: <fix>, <guard>` | 0/3 left a ticket `/go` could take | 3/3 |
| `deliver-issues` 2.1.0: a tier-1 fix is eligible and built with `test-first` | 3/3 bounced #28 back to Shaping | 3/3 claimed → PR `Closes #28` → in-review → closed on merge |
| `board` 1.0.2: a tier-1 fix is eligible, and a bug on a shipped feature is not reported as disagreeing | — | checked deterministically, both directions |

On klynt, #242 still carries `ready-for-agent` from the W9 triage. Under 1.1.0 it belongs in
`status:shaping`. That is a tracker write, so it is left for the owner.
