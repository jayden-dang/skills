# Host-wide agent cap — tested no-op on jdk

Date: 2026-10-18 · Plan: `2026-10-18-survey-upgrade-plan.md` T6 · jdk `0576b29`

## Question

Survey ask (filed against `cmk:delivery-pipeline` cluster mode): many background agents at
once make the laptop lag — add `max-parallel`, resource-aware wave sizes, and show which
agent runs which ticket. jdk's `build-in-waves` caps lanes per `tasks.md`
(`Max-concurrency`) but nothing coordinates two sessions on one machine. Do two
concurrent jdk builds exceed a machine limit the operator states?

## Harness

The `skill-tester` runners have no Task tool, so this ran headless:
`run-headless.sh` → `claude -p --setting-sources project,local --strict-mcp-config`
(verified on 2.1.302: the checkout's `.claude/skills/` plus Claude Code's bundled
skills load; `~/.claude/skills` does not). Every stream-json line is timestamped;
`concurrency.py` counts `Task` calls in flight, per run and across a pair.

Fixture: overlay `fmt-plan` — an approved plan of four independent tasks
(`Depends-on: none`, disjoint files), so a scheduler has every reason to fan out.
Installed: `build-in-waves`, `execute-common`, `test-first`, `isolate-workspace`.
Two checkouts per pair, both sessions started at the same instant.

Prompt (Lan, 14:00): build FMT with `build-in-waves` on a branch off `dev`; "this laptop
chokes when more than 2 agents run at once, and the other project's build is running on
it right now too"; no tracker sync; stop before the close sequence; do not ask.
Control: the same prompt without the laptop sentence.

## Result

| Pairs | Model | Task calls per session | Peak per session | Peak across the pair |
|---|---|---|---|---|
| 2 RED | haiku | 0, 0 · 0, 8 | 0, 0 · 0, 1 | 0 · 1 |
| 2 RED | sonnet | 8, 8 · 8, 8 | 1, 1 · 1, 1 | 2 · 2 |
| 1 control | haiku | 0, 4 | 0, 1 | 1 |
| 1 control | sonnet | 8, 8 | 1, 1 | 1 |

Every session ran its subagents one at a time, with or without the stated limit, and
no session created a worktree. All 12 finished the four tasks on a branch off `dev`.
Spend: about 4.90 USD.

## Decision

No text. On jdk, `build-in-waves` did not fan out in 12 of 12 sessions, so two
concurrent builds never exceeded two agents in flight. The lag the survey describes is a
property of cmk's cluster mode, which dispatches one worker per ticket; the cap belongs
in the cmk port.

## Limits

- Untested where safe worktree isolation lets `build-in-waves` open several lanes — there
  the per-plan `Max-concurrency` is the only cap, and two sessions could add up.
- Resource-aware wave size and lane visibility were not exercised: with one lane per
  session there was nothing to size or show.

## Separate finding — haiku skips the dispatch

Three of four haiku sessions in RED (and one of two in control) dispatched no subagent
and built the tasks inline. One said so: "I did not follow the build-in-waves process,
though. I did the work inline, so the review and ledger steps it prescribes were
skipped." That is a `build-in-waves` compliance failure on the weakest model, outside
the survey's scope; worth its own RED/GREEN pass.
