# Attention signals — glob sets and repo config

Loaded from `SKILL.md`'s **Binding pass** when you need the risk-glob set, the
manifest globs, the test globs, or the repo config grammar.

## Default risk-glob set (B1)

Used when the repo declares none. Case-insensitive, matched against the
repo-relative path of every file in `RANGE`.

```
**/auth/**            **/*auth*            **/*login*         **/*session*
**/*password*         **/*secret*          **/*token*         **/*credential*
**/*crypt*            **/security/**
**/migrations/**      **/migrate/**        **/*schema*        **/*.sql
**/payment/**         **/billing/**
**/.github/workflows/**   **/Dockerfile*   **/*.tf
```

## Manifest globs (B2)

```
package.json   Cargo.toml   pyproject.toml   go.mod
requirements*.txt   Gemfile   pom.xml   .claude-plugin/plugin.json
```

## Test globs (B3)

Read the `Test globs` line in `docs/agents/project.md`. When it is absent or
records `(defaults)`, use the same default set `trace` uses:

```
tests test e2e src src-tauri crates app lib packages
```

## Repo config grammar

Optional. A repo may add this section to `docs/agents/project.md`:

```markdown
## Attention signals

- **Partition depth:** 2
- **Risk globs:** `**/auth/**`, `src/payments/**`
```

Rules:

- The section is **optional**. When it is absent, the defaults above apply with
  no warning and no failure.
- `Risk globs` **extend** the defaults — they never replace them. A repo adds
  the paths its own risk lives behind; it does not switch the built-in set off.
- `Partition depth` accepts an integer ≥ 1. Anything else → use 2 and say so once.
- Nothing here can disable the binding pass: B2–B5 stay live regardless.
