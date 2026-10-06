# `validate-ui`

> Drive the app in the user's browser the way a user will: click, type, submit, reload, and assert on what is actually on screen. Component tests mock the network; this proves the wired stack — render, request, response, re-render, persistence.

|  |  |
|---|---|
| **Bucket** | acceptance |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | `docs/agents/project.md` (the `## Run locally (dev)` entry); a slice of the acceptance ledger; the spec when run directly |
| **Writes** | `.skills/<CODE>/validate-ui.md` (the drive record); the `## Run locally (dev)` entry when missing; results into the ledger |
| **Calls** | [`root-cause`](root-cause.md) when a visible outcome fails |
| **Called by** | [`validate-feature`](validate-feature.md) |

## When it fires

To validate a frontend against its spec by driving it in the user's Chrome or Edge through kimi-webbridge — click, type, reload — and asserting visible state and persistence, before merging. It covers the flows component tests mock away. It also fires when the repo has no documented local run command, because it records that command first.

It does not install Playwright, Cypress, or any other browser harness. A fresh headless browser is a different session from the one the user is signed into.

Usually [`validate-feature`](validate-feature.md) invokes it with a slice of the acceptance ledger. It can also run directly against a frontend change.

## 1. Get the app running — and persist how

Read `docs/agents/project.md` for `## Run locally (dev)` and start the frontend, and any backend it calls, with the recorded commands. If they are absent, discover them, start the app, confirm it loads, then **write** them into `project.md`. The step is done when the app loads and the commands are recorded.

If a flow needs a signed-in session, the browser's existing login is that session. A login wall stops for the user to sign in once in the drive's tab. An empty screen is not a pass.

## 2. The driver is kimi-webbridge

One session name for the feature. The first navigation opens a new tab. Do not borrow the tab the user is already viewing. If the daemon is down, start it. If the extension is not connected, relay its help page and stop. Do not substitute a headless browser because the repo already has one.

## 3. Drive each checklist flow

Act as a user. Find the control by its role or name, type and click, and assert on visible outcomes: text on screen, the input cleared, list order, an error shown. Quote that text into the ledger. Where the criterion says "persists", open the same URL again and assert the state survived. Where the check is what the server stored, capture the request the action just made.

## 4. Triage what breaks

Re-drive a failing flow once. A deterministic miss on a visible outcome is a product defect: [`root-cause`](root-cause.md), with this same drive as the red loop. The regression for that fix goes into the repo's existing test stack. A flake or a bad ref is fixed in the drive, not by standing up another harness.

## 5. Record the drive

Write `.skills/<CODE>/validate-ui.md` with one block per flow, the quoted screen text, the reload result, and pass or fail. That file is the acceptance evidence. Do not commit a browser-harness suite from this pass.

## See also

- [`validate-feature`](validate-feature.md) — the orchestrator that hands it a ledger slice
- [`validate-api`](validate-api.md) — the same contract for a backend surface
- [`write-dogfood`](write-dogfood.md) — the manual sibling, for judgment a drive does not settle
- [`run-dogfood`](run-dogfood.md) — agent-run an existing guide, same browser driver
- [`root-cause`](root-cause.md) — the red loop a failing flow drops into
