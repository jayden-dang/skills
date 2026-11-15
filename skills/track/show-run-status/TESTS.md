# TESTS.md — show-run-status

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
