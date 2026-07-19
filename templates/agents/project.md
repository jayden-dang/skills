# Project configuration (agent-facing)

Written by `setup-repo`. Skills read this file for repo-specific **machine config** —
commands, globs, paths — and the project's **posture** (below). Human-facing engineering
guidelines (coding standards, naming, house rules) live in `docs/product/guidelines.md`
when the project-docs layer is enabled; `write-plan` sources them from there and falls
back to this file otherwise.

## Project posture

The project's standing intent and lifecycle phase. Skills read this instead of re-asking:
`brainstorm` and `grilling` right-size how much they weigh data migration, backward
compatibility, and deprecation against it; `interpret` reuses it as session context.
Edit these two lines directly whenever the project moves phase — no wizard needed.

- **Delivery intent:** `<Production | MVP | Prototype | Research | Learning>` — how robust and complete the output must be.
- **Lifecycle stage:** `<Idea | Early development | Active development | Released | Scaling | Maintenance>` — where the project is in its life.

These are distinct from the product **Goals** in `docs/product/vision.md` (what success
looks like): posture is *how carefully to build right now*, not *what to build*.

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
- Engineering guidelines (project-docs layer, optional): `docs/product/guidelines.md`
- Product vision / architecture spine (project-docs layer, optional): `docs/product/vision.md`, `docs/architecture/`
