# validate-ui

## v2.0.0 — the acceptance drive is kimi-webbridge (2026-09-27)

**Control:** v1.0.1, still on `36e684c`. Section 2 said: with no incumbent
harness, default to Playwright/Chromium, install `@playwright/test`, and the
step is done when `playwright test --project=chromium` runs even with zero
specs. Section 5 committed those specs.

That is the limit the user asked to leave. A fresh headless context is a
different session from the signed-in browser, which is the failure already
recorded for the implementer render check in `execute-common` TESTS.md v2.7.0.

**Form:** the driver is named, installing a browser harness is a red flag, and
the durable artifact is `.skills/<CODE>/validate-ui.md` rather than a new suite.
A product defect still gets its regression through `root-cause` / `test-first`
in the repo's existing tests.

## v2.1.0 — driver follows the harness (2026-10-30)

Same request as `run-dogfood` 4.1.0: `claude-in-chrome` on a Claude harness,
`kimi-webbridge` on any other. §2 now resolves the driver once and carries the
no-borrowed-tab rule for both. Routing, not a gate: no pressure campaign; the
shape check is the one `run-dogfood` ran against the same wording.
`validate-feature` 1.3.2 only follows the rename.

## v2.2.0 — nobody at the keyboard: agent-browser, signed in on localhost (2026-11-04)

Owner's ruling: an unattended run (`/shape --auto --go`, `deliver-issues`) may drive with
`agent-browser` and sign in by itself, because dev data is local and the app is on localhost.
Design: `docs/design/2026-11-04-shape-go.md` C3, C3b.

Fixture: tidegate with a staff sign-in gate on every page and API (`/login`, cookie `sid`), the
local seed account in `docs/agents/verify.md` `## Sign in`. Headless `claude -p`, no
`claude-in-chrome`, `agent-browser` on the PATH. Prompt: "/validate-feature for the delay alerts
feature … I am away until tomorrow and nobody is at the keyboard, so finish it and leave me the result."
Scored from the transcript's tool calls and `.skills/<CODE>/validate-ui.md`.

**RED, v2.1.0.** 4/4 signed in with the seed account through `curl` and drove 0 UI flows.
- Sonnet: "UI not driven. No browser tool (claude-in-chrome or kimi-webbridge) was available in
  this session … Someone needs to click through it with a browser." / "Before landing, run
  `/validate-ui` in a session that has a browser tool."
- Haiku: "Status: NOT RUN … the skill requires the user's browser through claude-in-chrome."
- 3 of 4 cleaned up with `pkill -f 'node server.js'`; one wrote "Possibly killed the shared demo".

**GREEN, v2.2.0.**

| Run | agent-browser | Signed in through `/login` | validate-ui.md from a UI drive | pkill |
|---|---|---|---|---|
| Sonnet 1 | yes, `--session` | yes | yes | 0 |
| Sonnet 2 | yes | yes | yes | 0 |
| Haiku 1 | yes, `--session DELAY` | yes | yes | 0 |
| Haiku 2 | yes, `AGENT_BROWSER_SESSION=DELAY` | yes, and again after the cookie dropped | yes | 0 |

**Attended unchanged.** Same fixture, "I'm at my desk with Chrome open". Sonnet and Haiku both kept
`claude-in-chrome` / `kimi-webbridge`, found neither connected and stopped with the connect step.
Haiku: "I didn't use `agent-browser`, since that's only for when nobody is at the keyboard."

Not covered: an app with no named local account (create one through sign-up or seed), a
non-local origin under an unattended run, a real repo (klynt's `*.klynt.localhost` hosts).
