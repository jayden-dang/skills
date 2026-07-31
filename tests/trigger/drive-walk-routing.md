# Trigger routing — `walk-product` / `drive-walk` / `validate-ui`

Audit Trace-ignored. Description routing for the colliding acceptance triple.
`author-skills` requires should-fire / should-not-fire pairs tested together.

**Status:** query set written; live multi-model routing not re-run on this ship
(only `grok-4.5` available). Use as the held-out set when a full trigger pass
is scheduled. Descriptions under test live in:

- `skills/acceptance/walk-product/SKILL.md`
- `skills/acceptance/drive-walk/SKILL.md`
- `skills/acceptance/validate-ui/SKILL.md`

## Disambiguators (expected)

| Skill | Observable predicate |
|---|---|
| `walk-product` | Need to **author** a checkable HTML guide for a human (or human + later driver) |
| `drive-walk` | A guide **already exists**; cases must be **executed** now with FE+BE evidence |
| `validate-ui` | Need **committed** Playwright/e2e specs that join the verify suite |

## Should-fire → `drive-walk`

1. "Run the walk-product guide at `.skills/note-walk-product.html` end to end in Chrome"
2. "Work through every case in the walk-product file and fix what breaks"
3. "Resume the half-finished walk-product run — ledger is in `.skills/`"
4. "Test every walk-product case against the local app and check the backend stored it"
5. "Agent-drive the walk-product checklist we already generated"
6. "Execute the walk-product HTML and mark each case pass/fail with evidence"
7. "The guide exists; don't hand it to me — you drive it"
8. "Re-run walk-product cases after the delete bug fix"

## Should-fire → `walk-product` (must not pick drive)

1. "Produce a walk-product test guide for the notes feature"
2. "I want a checkable HTML artifact to tick off while I try the app myself"
3. "Build the manual walk-product pass for every user-facing ability"
4. "Human eyeball guide for badge colors and empty states"

## Should-fire → `validate-ui` (must not pick drive)

1. "Write Playwright e2e specs for the create-note flow and commit them"
2. "Set up Chromium e2e harness and cover NOTE-1.1 for CI"
3. "Promote the acceptance checklist into durable UI tests"

## Should-not-fire either drive or walk-product alone

1. "Unit tests are green — validate-feature the feature before merge" → `validate-feature`
2. "curl the notes API for NOTE-1.1" → `validate-api`
3. "The delete endpoint returns 204 but list still shows the row" → `root-cause`

## Recording results

| Query # | Expected | Observed model / choice | Pass? |
|---|---|---|---|
| (fill when run) | | | |
