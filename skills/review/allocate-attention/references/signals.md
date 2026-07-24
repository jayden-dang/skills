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
- **Risk globs mode:** replace | extend
```

Rules:

- The section is **optional**. When it is absent, the defaults above apply with
  no warning and no failure.
- `Risk globs mode: extend` (the default when the key is missing) unions the
  repo's globs with the defaults; `replace` uses only the repo's.
- `Partition depth` accepts an integer ≥ 1. Anything else → use 2 and say so once.
- A repo may narrow the risk set. It may not disable the binding pass: an empty
  risk set still leaves B2–B5 live.
