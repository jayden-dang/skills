---
name: validate-ui
version: 2.1.0
description: Use to validate a frontend against its spec by driving it in the user's
  browser through claude-in-chrome on a Claude harness or kimi-webbridge elsewhere — click, type, reload — and asserting visible
  state and persistence, before merging. Not a Playwright harness. Covers the
  flows component tests mock away. Also persists the local run command when
  the repo has none.
---

# Acceptance — UI

Drive the running app in the user's Chrome or Edge through the harness's browser driver (`claude-in-chrome` or `kimi-webbridge`, §2).
Click, type, submit, reload, and assert on what is actually on screen.
Component tests mock the network; this proves the wired stack. A fresh
headless browser is a different session — it is not this drive, and this
skill does not install one.

Invoked by `validate-feature` with a slice of the acceptance ledger, or run
directly against a frontend change. Work through the ledger in order.

## 1. Get the app running — and persist how

Read `docs/agents/project.md` for **Run locally (dev)**. Start the frontend (and
any backend it calls) with the recorded commands; if absent, discover them,
start the app, confirm it loads in a browser, then WRITE them into project.md
under `## Run locally (dev)`. *Done when: the app loads AND the commands are
recorded.*

**Preconditions — auth, data, environment.** If the flows need a logged-in
session, a seeded account, or environment configuration, discover how the repo
provides them and record it in project.md. The signed-in browser is the
session. Do not mint a `storageState` file for a headless runner. A run that
stalls on a login wall stops for the user to sign in once in the drive's tab,
then continues. An empty screen is not a pass.

### UI / accessibility standards (optional)

**Load:** `skills/project/define-system-doc/consult-recipe.md`.  
**Paths:** `docs/standards/ui.md`, `docs/standards/accessibility.md`.  
Consult when Approved; no-op when absent; suggest once
`/define-system-doc standards/ui|accessibility` if material; never auto-invoke.

## 2. The driver follows the harness

Resolve the driver once and name it. On a Claude harness (Claude Code, Claude
desktop) with the `claude-in-chrome` tools connected, it is `claude-in-chrome`.
On any other harness, or a Claude harness without that extension, it is
`kimi-webbridge`. Step names below are `kimi-webbridge`'s; `claude-in-chrome`
uses its equivalents (`read_page`, `find`, `computer`, `form_input`,
`read_network_requests`).

- **`claude-in-chrome`:** `tabs_context_mcp` first, then `tabs_create_mcp` for
  this feature's tab. Never reuse an id from another session or the user's tab.
- **`kimi-webbridge`:** follow its skill. One session name for this feature, on
  every command. First `navigate` uses `newTab:true`. `find_tab` with
  `active:true` borrows the user's tab — do not. If the daemon is down, start it.

If the chosen driver is not connected, relay its connect instructions and stop.
Do not install `@playwright/test`, Cypress, or any other browser harness for
this pass, and do not drive the flow in a fresh headless browser because one
is already in the repo. *Done when: the drive tab is open on the app through
the resolved driver, or the not-connected stop is on the record.*

## 3. Drive each checklist flow

For each UI item in the ledger, act as a user. `snapshot` to find the control
by role or name, then `click` or `fill`. Assert visible outcomes — text on
screen, the input cleared, list order, an error message shown — and quote
that text into the ledger. Where the criterion says "persists", `navigate` to
the same URL again and assert the state survived. Where the check is what the
server stored, `network` `start` before the action and `detail` before `stop`,
and record status plus the response fact. Map requirement IDs in the ledger,
not in application source.

## 4. Triage what breaks

No failure is waved away. Re-drive the failing flow once:

- **Deterministic failure on a user-visible outcome** — wrong text, wrong
  status, a missing element that should render — is a **product defect**.
  REQUIRED SUB-SKILL: use `root-cause`. The red loop is this same browser
  drive, not a new browser suite. A regression for the fix lands in the repo's
  existing test stack via `test-first`.
- **Non-deterministic** (passes on re-drive) or a **drive fault** — a ref that
  no longer matches, a missing wait, absent seed state — is fixed in the
  drive, not by standing up another harness.

Only a deterministic failure on a real outcome goes to `root-cause`.
*Done when: every UI flow passes on a fresh browser drive.*

## 5. Record the drive

Write `.skills/<CODE>/validate-ui.md`: one block per flow, the quoted screen
text, the reload result, and pass or fail. That file is the acceptance
evidence. Note results in the ledger. Do not commit a browser-harness suite
from this pass. *Done when: the record is on disk and every flow in it passed.*

## Rationalizations

| Thought | Reality |
|---|---|
| "No Playwright, so I'll install it and CI can re-run" | This pass is the user's browser. Do not create that harness here |
| "Headless is more reliable" | It is a different session. Flows that need the signed-in browser never run there |
| "The repo already has a browser suite, so drive that" | Leave it. This acceptance drive is still the user's browser through the resolved driver |
| "A login wall means the feature failed" | Stop for one sign-in in the drive tab, then continue |

## Red Flags

- Adding a browser test dependency or config for this pass
- A pass recorded from a fresh headless browser
- Borrowing the user's open tab (`find_tab` with `active:true`, or reusing their tab id)
- A login-wall screenshot treated as the flow's result
