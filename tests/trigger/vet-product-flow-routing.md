# Trigger routing — `vet-product-flow` vs author / walkthrough / validate-ui

Audit Trace-ignored. Description routing for judgment vs authoring vs drive vs
committed e2e. `author-skills` requires should-fire / should-not-fire pairs
tested together.

**Status:** query set written; live multi-model routing not re-run on this ship.
Use as the held-out set when a full trigger pass is scheduled. Descriptions
under test live in:

- `skills/acceptance/vet-product-flow/SKILL.md`
- `skills/acceptance/review-product-flow/SKILL.md`
- `skills/acceptance/run-product-walkthrough/SKILL.md`
- `skills/acceptance/validate-ui/SKILL.md`

## Disambiguators (expected)

| Skill | Observable predicate |
|---|---|
| `vet-product-flow` | Run file **exists**; need **isolated** judgment / missing-situation map **before dogfood** |
| `review-product-flow` | Need to **author** cases / produce the checkable guide |
| `run-product-walkthrough` | Guide exists; cases must be **executed** now with FE+BE evidence |
| `validate-ui` | Need **committed** Playwright/e2e specs that join the verify suite |

## Should-fire → `vet-product-flow`

1. "Vet the guide — is it complete for the implementation surface?"
2. "Isolated judgment pass on `.skills/notes-review-product-flow.json` before dogfood"
3. "Check for missing situations the shipped product already exposes"
4. "We finished authoring; required next is vet before run-product-walkthrough"
5. "Re-vet after we patched the run file for guide gaps"
6. "Is the guide missing empty-state / error paths the code actually renders?"
7. "Hand-off after review-product-flow — run the isolation map, don't drive yet"

## Should-not-fire `vet-product-flow` (prefer peer)

| Query | Prefer |
|---|---|
| "Produce a review-product-flow test guide for the notes feature" | `review-product-flow` (author) |
| "Build the cases YAML and render the HTML shell" | `review-product-flow` |
| "Drive every case in the guide against the local app with saw/server" | `run-product-walkthrough` |
| "Execute the walkthrough ledger and mark pass/fail" | `run-product-walkthrough` |
| "Write Playwright e2e specs for create-note and commit them" | `validate-ui` |
| "Set up Chromium e2e harness and cover NOTE-1.1 for CI" | `validate-ui` |
| "The delete endpoint returns 204 but list still shows the row" | `root-cause` |

## Recording results

| Query # | Expected | Observed model / choice | Pass? |
|---|---|---|---|
| (fill when run) | | | |
