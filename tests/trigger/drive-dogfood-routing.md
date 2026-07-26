# Trigger routing — `dogfood` / `drive-dogfood` / `acceptance-ui`

Trace-ignored. Description routing for the colliding acceptance triple.
`writing-skills` requires should-fire / should-not-fire pairs tested together.

**Status:** query set written; live multi-model routing not re-run on this ship
(only `grok-4.5` available). Use as the held-out set when a full trigger pass
is scheduled. Descriptions under test live in:

- `skills/acceptance/dogfood/SKILL.md`
- `skills/acceptance/drive-dogfood/SKILL.md`
- `skills/acceptance/acceptance-ui/SKILL.md`

## Disambiguators (expected)

| Skill | Observable predicate |
|---|---|
| `dogfood` | Need to **author** a checkable HTML guide for a human (or human + later driver) |
| `drive-dogfood` | A guide **already exists**; cases must be **executed** now with FE+BE evidence |
| `acceptance-ui` | Need **committed** Playwright/e2e specs that join the verify suite |

## Should-fire → `drive-dogfood`

1. "Run the dogfood guide at `.skills/note-dogfood.html` end to end in Chrome"
2. "Work through every case in the dogfood file and fix what breaks"
3. "Resume the half-finished dogfood run — ledger is in `.skills/`"
4. "Test every dogfood case against the local app and check the backend stored it"
5. "Agent-drive the dogfood checklist we already generated"
6. "Execute the dogfood HTML and mark each case pass/fail with evidence"
7. "The guide exists; don't hand it to me — you drive it"
8. "Re-run dogfood cases after the delete bug fix"

## Should-fire → `dogfood` (must not pick drive)

1. "Produce a dogfood test guide for the notes feature"
2. "I want a checkable HTML artifact to tick off while I try the app myself"
3. "Build the manual dogfood pass for every user-facing ability"
4. "Human eyeball guide for badge colors and empty states"

## Should-fire → `acceptance-ui` (must not pick drive)

1. "Write Playwright e2e specs for the create-note flow and commit them"
2. "Set up Chromium e2e harness and cover NOTE-1.1 for CI"
3. "Promote the acceptance checklist into durable UI tests"

## Should-not-fire either drive or dogfood alone

1. "Unit tests are green — acceptance-check the feature before merge" → `acceptance-check`
2. "curl the notes API for NOTE-1.1" → `acceptance-api`
3. "The delete endpoint returns 204 but list still shows the row" → `debug`

## Recording results

| Query # | Expected | Observed model / choice | Pass? |
|---|---|---|---|
| (fill when run) | | | |
