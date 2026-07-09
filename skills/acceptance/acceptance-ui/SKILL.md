---
name: acceptance-ui
description: Use to validate a frontend against its spec by driving it end-to-end (e2e)
  in a real browser the way a user would — automated Playwright specs on
  Chromium, asserting visible state and persistence across reload — before
  merging. Covers the happy-path and edge-case flows that component unit tests
  mock away. Also checks for and sets up a Playwright/Chromium harness, and
  persists the local run command, when the repo has none.
---

# Acceptance — UI

Drive the app in a real browser the way a user will: click, type, submit,
reload, and assert on what's actually on screen. Component tests mock the
network and prove the component's own logic; this proves the wired stack —
render, request, response, re-render, persistence.

Invoked by `acceptance-check` with a slice of the acceptance ledger, or run
directly against a frontend change. Work through the ledger in order.

## 1. Get the app running — and persist how

Read `docs/agents/project.md` for **Run locally (dev)**. Start the frontend (and
any backend it calls) with the recorded commands; if absent, discover them,
start the app, confirm it loads in a browser, then WRITE them into project.md
under `## Run locally (dev)`. *Done when: the app loads AND the commands are
recorded.*

## 2. Ensure a Playwright/Chromium harness

Check for one: `@playwright/test` installed and a `playwright.config.*` with a
Chromium project. If present, use it. If not, set it up: install
`@playwright/test`, add a config with a `chromium` project and the dev-server
`baseURL`, a test directory, and record the run command
(`… playwright test --project=chromium`) in project.md. *Done when: the
Playwright command runs against Chromium — even with zero specs — and is
recorded.*

## 3. Turn each checklist flow into a spec

For each UI item in the ledger, write a Playwright spec that acts as a user:
locate elements by role or label (`getByRole`, `getByLabel`), type and click,
and assert on visible outcomes — text on screen, the input cleared, list order,
an error message shown. Where the criterion says "persists", `page.reload()` and
assert the state survives. Tag each spec with its requirement ID per the
project.md conventions (e.g. `test('…', { tag: '@CODE-N.M' }, …)`).

## 4. Run on Chromium and fix what breaks

Run the specs headless on Chromium. Any failure is a real defect.
REQUIRED SUB-SKILL: use `debug` — the failing spec is your red-capable loop. Fix
the root cause, keep the spec as the regression, re-run. *Done when: every UI
flow passes in a fresh Chromium run.*

## 5. Commit the specs

The specs are the durable artifact — commit them, tagged, so they join the
verify suite and `finish-branch` re-runs them. Record any new run command in
project.md and note results in the ledger. *Done when: specs committed, tagged,
green.*
