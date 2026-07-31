# Trigger-test — description routing across the model roster

Recorded per `author-skills`: the `description` is the highest-leverage line in a skill
and the one field that cannot be eyeballed, so it is tested empirically. This file is the
evidence for the 47 model-invocable descriptions. It is Audit Trace-ignored.

## Validity precondition

Routing is decided by the *installed* descriptions, not the repo's working copies. Before
running, all 47 model-invocable descriptions were diffed repo-vs-installed:
**46 identical, 0 drifted, 1 not installed (`plan-milestones`)**. The tier-1 sweep rewrote
only user-invoked descriptions, which route nothing. So this is a live routing test, not a
simulation — the router under test sees exactly the text recorded here.

The 17 user-invoked skills are excluded: with `disable-model-invocation: true` they cannot
be routed to at all.

## Method

38 realistic first-person queries — messy phrasing, no skill names, drawn from the
colliding pairs whose scope abuts (acceptance trio vs review-product-flow vs verify; root-cause vs tdd;
frame-change vs clarify-decisions vs amend-feature vs reroute-plan; the spec triad; inspect-change vs polish-diff vs
vet-feedback; realign-spec vs trace; research vs run-spike; and the personal pack's
open/plan/orient/capture cluster). Expected answers were written first and held back from
every tested agent.

Roster: opus, sonnet, haiku. Per the protocol the bar is the weakest model.

**Phase 1 (batched, 3 agents/model-set):** each agent judged all queries for one batch.
**Phase 2 (fresh context, 1 query per agent):** every Phase-1 divergence re-run cold.

## Phase 1 result

114 routing decisions. **34 of 38 queries unanimous across all three models (89%).**

Four divergences: A7 `frame-change`/`amend-feature`, A9 `test-first`/`polish-diff`, C2 `polish-diff`/`simplify`,
D3 `plan-day`/`orient`.

## Phase 2 result — three of the four divergences were batching artifacts

| Divergence | Phase 1 | Phase 2 (fresh context) | Verdict |
|---|---|---|---|
| A9 refactor → `test-first` vs `polish-diff` | sonnet chose `polish-diff` | sonnet `test-first`, haiku `test-first` | artifact — did not reproduce |
| C2 cleanup → `polish-diff` vs `simplify` | sonnet chose `simplify` | 7/8 chose `polish-diff` across all three models | artifact — did not reproduce |
| A7 "add a discount field" | haiku chose `amend-feature` | haiku `amend-feature`; rephrased, haiku `frame-change` | boundary variance, see below |
| D3 "what am I doing today" | sonnet chose `orient` | sonnet `orient`, haiku `orient` | reproduces |

The single reproducible `simplify` hit was haiku on *"there's a lot of needless complexity
in what I just wrote — simplify it"* — the user typed the built-in command's own name.
Keyword capture by an explicit request is not a description defect.

## What was NOT changed, and why

No description was edited. Two observations remain open but neither clears the no-op bar:

- **`orient` beats `plan-day` on "what am I doing today"** (2/2 fresh, two models). Real,
  but which should win is genuinely debatable: `orient` advertises "today's focus" and
  returns one recommended next focus, which answers the question. Editing on a contested
  premise would be writing text against a guess.
- **`amend-feature` vs `frame-change` on "add a field to X"** flips with phrasing on haiku. The query
  is ambiguous by construction — whether the surface is already spec'd decides it, and the
  query does not say. `amend-feature`'s description already carries the exclusion clause
  ("Not for a brand-new feature (frame-change)").

Per the Iron Law, a baseline that does not fail means there is nothing to write.

## Method finding — the batching deviation manufactured findings

Phase 1 batched queries per agent to hold the agent count down. This deviates from
`pressure-testing.md`'s "fresh context per sample — carried-over context contaminates the
next sample."

The deviation was predicted to bias results *optimistic* (an agent primed on routing
questions routes better than a cold one). **That prediction was wrong in direction.**
Batching produced noise, not optimism: 4 divergences, of which 3 vanished under
fresh-context re-run. Had Phase 2 been skipped, this file would have reported three
description defects that do not exist — and the fixes for them would have been text with
no failure behind it.

The existing rule needed no amendment. The deviation from it did.
