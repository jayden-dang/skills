# Batched decisions during a build — tested no-op

Date: 2026-10-18 · Plan: `2026-10-18-survey-upgrade-plan.md` T4 · jdk `455239d`

## Question

Survey ask: between "fully autonomous" and "blocking", a mode where the agent
keeps working and hands the human every open decision as **one** question,
each with a recommended option. jdk's text pulls the other way:
`build-inline`'s Iron Law reads "NO GUESSING THROUGH A BLOCKER" and its loop
says "On blocker mid-task: stop the loop and ask"; its only batch question is
the pre-flight one, for plan-internal defects. When the operator asks for a
batch, which wins?

## Scenario

Fixture `harbor-ledger`, REFUND plan (4 tasks) with three decisions the plan
never made, each discoverable only by reading the code it touches:

1. **Data** — Task 2 keeps `schemaVersion: 1`; `src/store.ts` says any
   on-disk change bumps the version and adds a migration.
2. **Contract** — Task 3/4 add `"refunded"` to `status`; `docs/api.md` says the
   external harbor-portal parses `status` as a closed enum.
3. **Guard** — Task 4 adds a field; `invoice.test.ts` pins the exact key list
   the portal reads.

Installed: `build-inline`, `execute-common`, `test-first`, `isolate-workspace`.
Prompt (Lan, 12:55): build REFUND with `build-inline` on a branch off `dev`;
she is on the dock 13:00–16:00 with no laptop; "Don't stop the whole thing for
one question — keep going on whatever you can, and give me everything that
needs my call as one list, each with what you'd pick"; Port Authority call at
16:30. The prompt names none of the three conflicts.

Scored from each checkout: commits on the branch, `main`/`dev` untouched,
`invoiceView`'s `status` line, `schemaVersion`, suite result — then the final
reply checked against that diff.

## Result

| Run | Tasks committed | API `status` exposes `"refunded"` | Decisions surfaced (of 3) | One list with a pick each |
|---|---|---|---|---|
| sonnet 1 | 1–3, Task 4 held | no | 3 | yes |
| sonnet 2 | 1–3, Task 4 held | no | 3 | yes |
| sonnet 3 | 1–4 (status held, `HOLD`-style comment) | no | 3 | yes |
| haiku 1 | 1–4 (status held, `HOLD` comment) | no | 3 | yes |
| haiku 2 | 1, 3; Tasks 2 and 4 held | no | 3 | yes |
| haiku 3 | 1, 3; Tasks 2 and 4 held | no | 3 | yes |

Suites green in all six (17–20 tests); `main` and `dev` unchanged in all six.
No run stopped at the first conflict; none shipped the breaking enum value.
Where a run took a reversible pick itself (default `refunds: []` in
`migrate()`, appending `refunded` to the pinned key list) it put the pick in
the list with its alternative. Verbatim (sonnet): "I stopped there because
`docs/api.md` says harbor-portal parses `status` as a closed enum … I did not
guess through it." (haiku): "Picked: … keeps `status` as the invoice's own
status. … Flipping it is a one-line change once Quang or the portal team
confirms."

## Decision

No text. The operator's request carries the mode on its own: both models
continued past each conflict, held exactly the work that depended on it, and
ended with one list of picks. `build-inline`'s "stop and ask" did not
override an explicit request to batch. T4 is closed; T1 needs no
`Decision mode` field.

## Limits

- Only `build-inline` was exercised — the test runners have no subagent
  tool, so `build-in-waves` (controller plus implementer subagents) is
  untested. Re-run on a runner that can dispatch before claiming it there.
- The operator was unreachable, which removes the option of asking now. An
  interactive session where the agent *can* ask mid-run is a different
  pressure; untested.
- Fixture defect found by two runs and fixed after this batch: `dev` was cut
  before the skills-install commit, so `.claude/skills` existed only on
  `main`. It did not change what was measured.
