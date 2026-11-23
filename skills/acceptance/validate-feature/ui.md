# Acceptance — UI

Drive the running app in a real browser through the driver §2 resolves. Step names below
(`snapshot`, `click`, `fill`, `network`) are generic; the driver's own tool for each is in
`../build/browser-driver.md` §3.
Click, type, submit, reload, and assert on what is actually on screen.
Component tests mock the network; this proves the wired stack. This skill
installs no browser harness.

Invoked by `validate-feature` with a slice of the acceptance ledger, or run
directly against a frontend change. Work through the ledger in order.

## 1. Get the app running — and persist how

Read `docs/agents/project.md` for **Run locally (dev)**. Start the frontend (and
any backend it calls) with the recorded commands; if absent, discover them,
start the app, confirm it loads in a browser, then WRITE them into project.md
under `## Run locally (dev)`. Record the PID of each process you start, and at
the end stop those PIDs and nothing else: one baseline run cleaned up with
`pkill -f 'node server.js'`, which matches every Node server on the machine,
the team's shared demo included. *Done when: the app loads AND the commands are
recorded.*

**Preconditions — auth, data, environment.** If the flows need a logged-in
session, a seeded account, or environment configuration, discover how the repo
provides them and record it in project.md. The drive's browser is the
session. Do not mint a `storageState` file for a headless runner. A run that
stalls on a login wall stops for the user to sign in once in the drive's tab,
then continues. An empty screen is not a pass.

### UI / accessibility standards (optional)

**Load:** `skills/project/define-project/consult-recipe.md`.  
**Paths:** `docs/standards/ui.md`, `docs/standards/accessibility.md`.  
Consult when Approved; no-op when absent; suggest once
`/define-project standards/ui|accessibility` if material; never auto-invoke.

## 2. The driver follows who is at the keyboard

Read `../build/browser-driver.md` and resolve the driver once; name it and its class in the
record. Two baseline runs left alone signed in with the seed account through `curl`, then
stopped at "No browser tool (claude-in-chrome or kimi-webbridge) was available" with
`agent-browser` on the PATH, and the UI was never driven. Do not install `@playwright/test`,
Cypress, or any other browser harness for this pass, and do not drive the flow through a
browser suite because one is already in the repo. *Done when: the drive tab is open on the app
through the resolved driver, or the not-connected stop is on the record.*

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

Write `.skills/<CODE>/validate-feature.md`: one block per flow, the quoted screen
text, the reload result, and pass or fail. That file is the acceptance
evidence. Note results in the ledger. Do not commit a browser-harness suite
from this pass. *Done when: the record is on disk and every flow in it passed.*

## Rationalizations

| Thought | Reality |
|---|---|
| "No Playwright, so I'll install it and CI can re-run" | This pass is the user's browser. Do not create that harness here |
| "Headless is more reliable" | With an own-browser driver connected and someone at the keyboard, a separate profile is a different session from their signed-in browser. Use it when nobody is there, or when no own-browser driver is connected |
| "No claude-in-chrome or kimi, so the UI stays undriven" | Read the tool list: a harness-native browser tool, `chrome-devtools` or `agent-browser` drives it, signed in with the local account |
| "The repo already has a browser suite, so drive that" | Leave it. This acceptance drive is still the user's browser through the resolved driver |
| "A login wall means the feature failed" | Stop for one sign-in in the drive tab, then continue |

## Red Flags

- Adding a browser test dependency or config for this pass
- A pass recorded from a separate-profile driver while an own-browser driver is connected and someone is at the keyboard
- A UI item recorded as passed from `curl`
- `pkill` or `killall` on the app: stop only the PID you started
- Borrowing the user's open tab (`find_tab` with `active:true`, or reusing their tab id)
- Stopping at "not connected" with a browser tool in the tool list that `browser-driver.md` §2 names
- A login-wall screenshot treated as the flow's result
