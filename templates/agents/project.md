# Project configuration (agent-facing)

Written by `setup-repo`. Skills read this file for repo-specific commands.

## Verify commands

Run in this order; all must pass before any completion claim.

| Check | Command |
|---|---|
| Typecheck | `<command>` |
| Lint | `<command>` |
| Unit tests | `<command>` |
| E2E / smoke | `<command>` |

Single test file: `<command pattern, e.g. npx vitest run <path>>`

The traceability check is not a command here — the `trace` skill runs it as
`grep`/`git` over `docs/specs/` and the test globs. If this repo's tests live
outside the default globs (`tests test e2e src src-tauri crates app lib packages`),
record the real locations below so `trace` searches the right paths.

Test globs: `<override, or leave blank for defaults>`
Trace ignore (files whose IDs are fixtures, not coverage): `<optional>`

## Test annotation conventions

| Layer | Requirement-ID convention |
|---|---|
| <e2e framework> | <e.g. Playwright tag: { tag: ['@CODE-N.M'] }> |
| <unit framework> | <e.g. Vitest: annotate('CODE-N.M', 'requirement') or ID in test name> |
| <other> | <e.g. Rust: /// REQ: CODE-N.M doc comment> |

## Run locally (dev)

How to start the app for user-facing acceptance checks (read by `acceptance-api`
and `acceptance-ui`). Fill in once the app can be run locally; leave a row blank
if that surface does not exist.

| Surface | Start command | Ready signal |
|---|---|---|
| Backend / API | `<command>` | `<e.g. GET http://localhost:<port>/health → 200>` |
| Frontend | `<command>` | `<e.g. http://localhost:5173 serves the app>` |

Browser E2E (Playwright, Chromium): `<e.g. pnpm exec playwright test --project=chromium>`

## Release steps

<Ordered list of project-specific release steps (build commands, bundling,
signing), consumed by the release skill.>

## Paths

- Specs: `docs/specs/`
- ADRs: `docs/adr/`
- Glossary: `CONTEXT.md`
- Out-of-scope KB: `.out-of-scope/`
