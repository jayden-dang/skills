# TESTS.md — board

## 2026-11-15 — absorbed show-run-status as mode file(s)

On the owner's word (2026-11-15: simplify the set around idea, shape and go, inside the skill
listing budget, without losing quality). Moved whole, not rewritten: show-run-status → `run-status.md`.
`SKILL.md` points at each file on an observable condition, and the description took over the
absorbed triggers. The absorbed skills' own records are appended at the end of this file.

Checked on Sonnet and Haiku against the frozen routing suite (`.skills/fixtures/routing/suite.py`,
153 first messages: the four cluster sets, 24 trim-check messages, and the older skills' own 26
trigger evals): 153 of 153 reached the expected owner on both models, before the description trims
and after. One ticket was run from `/idea` through `/shape` and `/go` before and after
(`.skills/fixtures/baselines/`): same stops for the operator, same artifacts. A real Claude Code
session at the default listing budget shows every one of the 59 descriptions; with 80 it showed 26
skills by name only.

Not covered: each mode file was not re-run on its own scenario. The absorbed skills' contract
evals, which cited headings of a `SKILL.md` that no longer exists, were dropped.

## 2026-11-15 — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). This skill is read-only and never
took its consent from being typed, so the body is unchanged. The description became trigger +
outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`.skills/fixtures/routing/listing.py`), 22 first messages (`cluster-a-messages.md`), one
subagent per model answering which one skill it loads first for each. Messages are batched in one
context, one rep per model, which is lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, 48 listed) — s | before — h | after (52 listed) — s | after — h |
|---|---|---|---|---|
| should fire here (1, 6, 10; held out 17) | NONE on all | NONE, or `craft-page` for the dashboard asks | `board` on all | `board` on all |
| the other 9 near-miss messages | none routed here | none | none routed here | none |

Should-fire messages: what's waiting on me this morning? · what are the agents working on right now · anything I need to merge or answer today? standup in ten minutes · catch me up, I've been out since Thursday. what needs me?. Near misses that stayed with their owners: "what is ROAD-81 and can
we start it?" (`brief-road`), "move sharing ahead of search on the roadmap" and "put ROAD-12 on
hold" (`plan-milestones`), "review the billing branch before I merge it" (`inspect-change`),
"tell my manager in two lines what we shipped this week" (`speak-outer`), "build me a status page
for our public API uptime" (`craft-page` or none).

## 2026-11-15 — 1.3.0 (follow-ups a skill could not file)

`board.py` prints a `Not filed (drafts in .skills/inbox)` section under Waiting on you: one line
per `.skills/inbox/*.md`, its first line and its path, `none` when the folder is empty or absent.
Test-first: `test_board.py::TestLocalDrafts`, three tests red on the missing section, then green
(13 tests). Why the section exists: `audit-shipped` TESTS.md, 2026-11-15.

Fixture: two `quayside` repos (`.skills/fixtures/make-quayside.sh`, `GATE=1`) holding the three
inbox files an `/audit-shipped` 1.1.0 run left, each naming Minh as the one who approves tickets.
Prompt: "/board — What's waiting on me this morning? Standup is in ten minutes." Scored from the reply.

| | 1.2.0 text, new script — s | 1.2.0 — h | 1.3.0 — s | 1.3.0 — h |
|---|---|---|---|---|
| the three files reported under Waiting on you | yes | yes | yes | yes |
| what to do with them | "file it or drop it" | "file it with `/triage` or drop it" | opened each: "send it to Minh, then file it or delete it" | the slot's words, files not opened, Minh not named |
| tracker writes | 0 | 0 | 0 | 0 |

The Iron Law carried the new section with no text. The slot line was added for the action: both
1.2.0 runs told Lan to file tickets that this repo lets only Minh approve. Haiku repeats the slot
without opening the files, so on Haiku the approver's name still comes from the file, not the report.

## 2026-10-19 — 1.0.0 (closed workflow W6)

Fixture: `harbor-ledger` + overlays `latefee-plan`, `fmt-plan`, then `scenarios/gh-board.sh`
(the board on a stateful `bin/gh`, never GitHub) and `scenarios/gh-roles.sh` (the four
newer state roles mapped to `status:*` labels). Scored by `scenarios/wf-score.py` and the
final report. Design: `docs/design/2026-10-19-closed-workflow.md`.
Before the run, `scenarios/wf-pre-pr.sh` opens PR #14 for #21 with "Closes #21" and a "Needs a
decision before merge" section, and takes #21 off the ready column without adding
`in-review`. The board then has:
- PR #14 with its parked decision;
- #25 `needs-info`, with a question to Lan;
- #26 `ready-for-human`, held by Minh;
- #27 untriaged;
- #22 and #23 eligible, with #22 blocked by #21;
- #24 `ready-for-agent` with no spec.

**RED, no skill.** Prompt: "What's waiting on me this morning? Standup is in ten minutes."

| | h1 | h2 | s1 |
|---|---|---|---|
| PR #14's decision | yes | yes | yes |
| #25's question | yes | yes | yes |
| #27 untriaged | no | no | yes |
| #24 ready with no spec | no ("approved for November") | no | no |

**GREEN (1.0.0).** `scripts/board.py` prints every section, always. A `Board and repo
disagree` section catches a ready ticket with no approved spec, an open PR's ticket with
no `in-review` role, an open ticket whose spec is `Implemented` or `Shipped`, and a ticket
with two state roles. Prompt: "/board — What's waiting on me this morning? …"

| | h1 | h2 | s1 |
|---|---|---|---|
| ran `board.py` | yes | yes | yes |
| PR decision quoted, #25 question, #27 to triage | yes | yes | yes |
| #24 named as not eligible, spec missing | yes | yes | yes |
| #21's PR without `in-review` named | yes | yes | yes |
| tracker writes | 0 | 0 | 0 |

Not covered: Linear (run with `--issues` and `--prs` files), Notion drafts passed with
`--drafts`, and a board of more than 30 tickets.

## 2026-10-19 — 1.0.1, found by the klynt dogfood (closed workflow W9)

`/board` ran on the real KlyntLabs/klynt board through `/tmp/klynt-dogfood/bin/gh`: reads go
to GitHub, writes are logged and never sent. Both haiku and sonnet ran `board.py`, and 0
writes reached GitHub. But the script told them that the four stale `ready-for-agent`
tickets (#258, #253, #252, #243) had "no spec" and should be swapped to `shaping`. Their
specs are `Implemented`. Two causes:
- **Link in the Spec cell.** klynt writes it as a markdown link, `[spec](../dir/)`, and the
  script read only a bare path or a `` `path` ``.
- **Blank line inside the table.** `learning.md` has one, and the script took the next row
  (CFGC) as a new header, so CFGC, QUIZ and FLASH were lost.

1.0.1 finds columns by header name, reads a link target, treats a header as the row a
`|---|` line follows, and also matches a `[CODE]` title. On the same board it now reports
five open tickets whose spec reads `Implemented`: the four, plus #261 [CCOL], which the T20
dogfood had missed.

## 1.0.2 — tier-1 fixes (2026-10-19), W10

`board.py` counts a `bug` as eligible ("eligible, tier-1 fix") when its `Requirements
covered:` IDs are all defined in a `requirements.md` or in `docs/specs/fixes.md`, with
one of them a `SHALL CONTINUE TO` guard. Such a ticket never draws an "open, but <CODE>
reads Implemented" line, because a bug on a shipped feature is normal.

Checked deterministically on the W10 fixture:
- #28 with BERTH-4.1 and its guard 4.2: `eligible, tier-1 fix`, and no disagreement line.
- The same ticket with its `Requirements covered:` removed: `NOT eligible`, plus "#28 is
  ready, but its spec is missing".

## 2026-10-30 — Shaping shows who is framing (1.0.2 → 1.1.0)

Source: the klynt frame-change. A ROAD's claim is the assigned tracker issue, opened before
framing. `board.py` already fetched assignees but printed them only for Human-only, so a
ticket being framed by someone else looked free.

Test-first: `scripts/test_board.py` feeds two shaping tickets (#301 assigned to alice, #302
unassigned). It failed with `'alice' not found in '- #301 ROAD-6 desktop foundation — no spec
yet'`. After the change it passes: Shaping lines read `— alice — no spec yet` and
`— unassigned — …`, with `(you)` when the assignee is the session user. The SKILL text gains a
half-line naming it. No agent run was needed: the reply quotes the script's output.

Not changed: `/idea` assigning the operator at file time. The harness classifier denies
`gh issue create` from test agents even against a stub, so that edit has no runnable test yet.

## 2026-11-01 — native edges and private ticket records (`board.py`)

Probe on the old script. A blocked ticket filed the way `publish-issues` prescribed, `## Blocked by`
then `- #1`, printed with no block. A `plan-tasks` issue in a repo with git-ignored specs, with no
`[CODE]` and no `Requirements covered:`, printed "its spec is missing".

`test_board.py` RED: an open native edge printed no block, two private records resolved no feature, and
a `gh` rejecting `blockedBy` lost the list. The closed-edge, `Blocked by:` line, shared tier-1,
`_pending-` and no-key tests passed before the change and guard it. GREEN: all 10 pass. `test_lanes.py`
is unchanged and passes.

---

# Merged from `show-run-status` — now `run-status.md` beside this skill

## 2026-11-15 — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). This skill is read-only and never
took its consent from being typed, so the body is unchanged. The description became trigger +
outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`.skills/fixtures/routing/listing.py`), 22 first messages (`cluster-a-messages.md`), one
subagent per model answering which one skill it loads first for each. Messages are batched in one
context, one rep per model, which is lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, 48 listed) — s | before — h | after (52 listed) — s | after — h |
|---|---|---|---|---|
| should fire here (2, 9; held out 18) | NONE on all | NONE, or `craft-page` for the dashboard asks | `show-run-status` on all | `show-run-status` on all |
| the other 9 near-miss messages | none routed here | none | none routed here | none |

Should-fire messages: where is the SPAY build at? it was running when I left · the LATEFEE run stopped overnight. what's done and what's left? · is CSV-export finished? I can't tell if the agent got through review. Near misses that stayed with their owners: "what is ROAD-81 and can
we start it?" (`brief-road`), "move sharing ahead of search on the roadmap" and "put ROAD-12 on
hold" (`plan-milestones`), "review the billing branch before I merge it" (`inspect-change`),
"tell my manager in two lines what we shipped this week" (`speak-outer`), "build me a status page
for our public API uptime" (`craft-page` or none).

## 2026-10-18 — 1.0.0

Roster: sonnet (`skill-tester`), haiku (`skill-tester-haiku`). Fixture `harbor-ledger` +
`scenarios/refund-midrun.sh`: a REFUND `build-in-waves` run stopped mid-wave on
`feature/refund`, with a bare `origin`. The sources disagree on purpose:

| Fact (pass rule) | Where it lives |
|---|---|
| F1 Tasks 1–3 committed (ledger says Task 3 "in progress") | git |
| F2 Task 4 started, uncommitted | working tree |
| F3 suite red with the uncommitted edit (green at HEAD) | `bun test` |
| F4 a decision parked for Lan: ship `"refunded"` vs keep `status` | `.skills/REFUND/implementation-notes.md` |
| F5 Task 3 commit not pushed; no PR | upstream, code host |
| F6 ticket still `ready-for-agent`, unassigned | `.scratch/refund/issues/01-…` |

Installed beside: `build-in-waves`, `execute-common`, `refresh-roadmap-status`. Prompt (Lan,
15:58): "Quick — where are we with REFUND? Port Authority call in 2 minutes and they will
ask." … "Change nothing — just find out." GREEN prefixes `/show-run-status — `. Scored by
reading each reply against the six facts; writes checked by `snapshot.sh` + `git diff`.

### RED — no skill, 6 runs

| | s1 | s2 | s3 | h1 | h2 | h3 |
|---|---|---|---|---|---|---|
| F1 F2 F3 | ✓✓✓ | ✓✓✓ | ✓✓✓ | ✓✓✓ | ✓✓✓ | ✓✓✓ |
| F4 parked decision | ✗ | ✗ | ✓ | ✓ | ✓ | ✓ |
| F5 unpushed commit | ✗ | ✓ | ✗ | ✓ | ✓ | ✓ |
| F6 stale ticket | ✓ | ✗ ("I did not read it") | ~ unassigned, not called stale | ✗ | ✗ | ✗ |
| wrote nothing | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

Verbatim:

- s1, F4 missed and inverted — its next step: "switch `invoiceView` to `refundStatus`",
  the change parked until Lan chose.
- s2, F6: "I found no tracker ticket status for REFUND. The tracker is local, under
  `.scratch/refund`, and I did not read it."
- s2, F4 missed: "So the test probably needs updating to allow the one new field."

Failure class: the report depends on which sources the agent happens to open → a
check that must not vary → deterministic primitive `scripts/collect.sh` (seven fixed
sections, each printing even when empty) plus a REQUIRED six-slot report. Counters
carry 2/6 parked-decision misses (one inverted), 2/6 unpushed misses, 5/6 tracker misses.

### GREEN — skill at `.claude/skills/show-run-status/`, 6 runs

| | s1 | s2 | s3 | h1 | h2 | h3 |
|---|---|---|---|---|---|---|
| F1 F2 F3 | ✓ ~ ✓ | ✓✓✓ | ✓✓✓ | ✓✓✓ | ✓✓✓ | ✓✓✓ |
| F4 parked decision, both options, none chosen | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| F5 unpushed commit named; no PR | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| F6 stale ticket called out | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| wrote nothing (snapshot + diff) | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

All three recorded misses cleared on both models. s1's say-out-loud line read "Task 4
hasn't started" while its slot 2 said the uncommitted edit might be Task 4 — a summary that
contradicts its own slot, not a missing source. h3 guessed the uncommitted edit leaned to
option (a) (it is (b)'s shape) and marked the guess unconfirmed. Neither recurs in the other
five; no REFACTOR edit.
