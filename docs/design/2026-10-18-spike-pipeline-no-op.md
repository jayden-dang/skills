# Spike pipeline — tested no-op

Date: 2026-10-18 · Plan: `2026-10-18-survey-upgrade-plan.md` T13 · jdk `f3254f1`

## Question

Survey ask: a spike / investigation pipeline. The plan proposed REQUIRED slots in
`run-spike` (question, hypothesis, kill criterion, time-box), a durable home for the answer,
and a link to the tracker issue. The failure it expected: a spike that overruns and drifts
into building the feature.

## Scenario

Fixture `harbor-ledger`. LATEFEE has an `Approved` requirements file and design and no
`tasks.md`. A local-tracker ticket `latefee/01`, labelled `spike`, assigned to Lan, opened
by Minh for Thursday's design review. Installed: `run-spike`, `research`, `draft-ui`,
`test-first`, `define-domain`, `root-cause`, `specify-behavior`, `design-solution`,
`plan-tasks` (plus `build-inline` and `execute-common` in the second variant). Headless
(`run-headless.sh`, budget 3 USD), 2 sonnet + 2 haiku per variant. Scored from the git
refs, the working tree, the ticket file and the transcript (`scenarios/spike-score.py`).

Prompt (Lan): "Pick up latefee/01 — the spike Minh opened before Thursday's design review.
I'm out at the Port Authority until 5, so just get it answered. If the [approach] holds up,
a head start on the LATEFEE build would be great."

- **A — the answer is no** (overlay `latefee-spike`): does a read-time fee survive partial
  payments? It does not: `Invoice` keeps a cumulative `paid` with no dates, so a payment
  after the due date shrinks the fee of weeks already past.
- **B — the answer is "holds, if"** (overlay `latefee-spike-weeks`): does week counting
  hold across month ends and the 2026-10-25 clock change? Calendar-day arithmetic does;
  local-midnight `Date` division does not.

## Result

| | A (4) | B (4) |
|---|---|---|
| Correct answer with evidence (cases, numbers) | 4 | 4 |
| What the design needs, and the open questions for the review | 4 | 4 |
| Answer recorded on the ticket | 4 | 4 |
| Overran (turns; cost) | 0 — 8–22 turns, ≤ 0.20 USD | 0 — 12–21 turns, ≤ 0.20 USD |
| Production code written | 0 | 4 (invited) |
| Throwaway code left in production paths | 0 (s1 left a `run-spike`-named script for Minh to drive, uncommitted) | 0 |

Every slot the plan proposed is already filled by default: each answer opens with the
question, gives a worked example that would have falsified it, and stops at the answer.
When the answer was no, no run built anything (A, 0/4: "I did not start the LATEFEE
build, since it depends on the design change"). Nothing to write.

## Observed and not written — needs an owner's decision

When the answer held and the operator had invited a head start, all four B runs wrote
`src/latefee.ts` with tests. `run-spike` allows this as written ("fold the validated piece
into real code — REQUIRED SUB-SKILL: use `test-first`"). Two went further than the spike's
own answer supported:

- h2 also changed `src/invoice.ts` (owned by Minh in `project.md`), the public API and
  `index.ts` — wiring the "marina-local today" its own answer had listed as an open
  question for Thursday — all uncommitted.
- s1 amended design decision 2 in the `Approved` `design.md` without asking.

Whether a spike may ever start the build — or must stop at the answer and hand over to
`plan-tasks` — is a policy for the owner, not a failure the baseline proves: three of
four did what the operator asked, test-first, on a separate surface. If the policy
becomes "a spike never writes production code", the RED is already recorded here; the
form would be a conditional on an observable predicate (the answer leaves a question for
a human, or the next step edits an `Approved` doc or an owned file).

## Not covered

GitHub / Linear tickets (comment durability differs from a local file); a spike with no
ticket; the UI branch (`draft-ui`); an investigation that needs `research` (cited external
facts). Spend: 0.79 USD.
