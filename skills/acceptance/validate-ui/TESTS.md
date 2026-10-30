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
