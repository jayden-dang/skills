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

## Test files (B3)

B3 asks whether the range added any **test file**. A test file is identified by
its own path, matching `trace`'s recognition rules:

```
\.(test|spec)\.[cm]?[jt]sx?$      foo.test.ts, bar.spec.jsx
a /tests?/ or /e2e/ path segment  tests/…, test/…, e2e/…
_test\.(rs|go|py)$                handler_test.go, thing_test.py
any .rs file                       Rust cites IDs in doc comments
```

**Do not use `trace`'s root list** (`tests test e2e src src-tauri crates app lib
packages`) for this. Those are the directories `trace` *searches*; `src/`,
`app/`, `lib/`, and `packages/` hold production code. Keying B3 off them turns
the rule into "the range added nothing under `src/`", which is false as soon as
any production file changes — B3 would then never fire in an ordinary app repo.

If `docs/agents/project.md` names different test globs or an ignore list, prefer
those.

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
