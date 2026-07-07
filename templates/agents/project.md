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
| Trace | `node <path-to>/check-trace.mjs` |

Single test file: `<command pattern, e.g. npx vitest run <path>>`

## Test annotation conventions

| Layer | Requirement-ID convention |
|---|---|
| <e2e framework> | <e.g. Playwright tag: { tag: ['@CODE-N.M'] }> |
| <unit framework> | <e.g. Vitest: annotate('CODE-N.M', 'requirement') or ID in test name> |
| <other> | <e.g. Rust: /// REQ: CODE-N.M doc comment> |

## Release steps

<Ordered list of project-specific release steps (build commands, bundling,
signing), consumed by the release skill.>

## Paths

- Specs: `docs/specs/`
- ADRs: `docs/adr/`
- Glossary: `CONTEXT.md`
- Out-of-scope KB: `.out-of-scope/`
