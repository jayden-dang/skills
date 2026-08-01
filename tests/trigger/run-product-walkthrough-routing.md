# Trigger routing — `review-product-flow` / `vet-product-flow` / `run-product-walkthrough` / `validate-ui`

Audit Trace-ignored. Description routing for the colliding acceptance set
(author / vet / drive / committed e2e). `author-skills` requires should-fire /
should-not-fire pairs tested together.

**Status:** query set written; live multi-model routing not re-run on this ship
(only `grok-4.5` available). Use as the held-out set when a full trigger pass
is scheduled. Descriptions under test live in:

- `skills/acceptance/review-product-flow/SKILL.md`
- `skills/acceptance/vet-product-flow/SKILL.md`
- `skills/acceptance/run-product-walkthrough/SKILL.md`
- `skills/acceptance/validate-ui/SKILL.md`

Peer detail for judgment vs neighbors: `tests/trigger/vet-product-flow-routing.md`.

## Disambiguators (expected)

| Skill | Observable predicate |
|---|---|
| `review-product-flow` | Need to **author** a checkable HTML guide for a human (or human + later driver) |
| `vet-product-flow` | Run file exists; need **isolated** missing-situation judgment **before dogfood** |
| `run-product-walkthrough` | A guide **already exists**; cases must be **executed** now with FE+BE evidence |
| `validate-ui` | Need **committed** Playwright/e2e specs that join the verify suite |

## Should-fire → `run-product-walkthrough`

1. "Run the review-product-flow guide at `.skills/note-review-product-flow.html` end to end in Chrome"
2. "Work through every case in the review-product-flow file and fix what breaks"
3. "Resume the half-finished review-product-flow run — ledger is in `.skills/`"
4. "Test every review-product-flow case against the local app and check the backend stored it"
5. "Agent-drive the review-product-flow checklist we already generated"
6. "Execute the review-product-flow HTML and mark each case pass/fail with evidence"
7. "The guide exists; don't hand it to me — you drive it"
8. "Re-run review-product-flow cases after the delete bug fix"

## Should-fire → `review-product-flow` (must not pick drive)

1. "Produce a review-product-flow test guide for the notes feature"
2. "I want a checkable HTML artifact to tick off while I try the app myself"
3. "Build the manual review-product-flow pass for every user-facing ability"
4. "Human eyeball guide for badge colors and empty states"

## Should-fire → `validate-ui` (must not pick drive)

1. "Write Playwright e2e specs for the create-note flow and commit them"
2. "Set up Chromium e2e harness and cover NOTE-1.1 for CI"
3. "Promote the acceptance checklist into durable UI tests"

## Should-fire → `vet-product-flow` (must not pick author or drive)

1. "Vet the finished guide for missing situations before dogfood"
2. "Isolated judgment: is the run file complete for the implementation?"

## Should-not-fire either drive or review-product-flow alone

1. "Unit tests are green — validate-feature the feature before merge" → `validate-feature`
2. "curl the notes API for NOTE-1.1" → `validate-api`
3. "The delete endpoint returns 204 but list still shows the row" → `root-cause`

## Recording results

| Query # | Expected | Observed model / choice | Pass? |
|---|---|---|---|
| (fill when run) | | | |
