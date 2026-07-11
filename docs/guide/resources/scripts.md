# Scripts

Five scripts. Two are linters that enforce the spine, two support `execute-plan`'s subagent engine, and one distributes the linters into consuming repos.

All are zero-dependency and offline. `check-trace.mjs`, `check-graph.mjs`, and `vendor-linters.mjs` are Node ESM; `task-brief` and `review-package` are bash.

---

## `check-trace`

The requirements traceability linter. The vertical layer: one feature's requirements, tasks, and tests must agree.

```bash
node scripts/check-trace.mjs [--strict] [--json] [--root <repo-root>]
```

### Sources of truth

| Path | Role |
|---|---|
| `<specsDir>/<feature>/requirements.md` | **defines** requirement IDs (`**CODE-N.M**`) |
| `<specsDir>/fixes.md` | optional shared home for tier-1 fix and guard requirements |
| `<specsDir>/<feature>/tasks.md` | **references** them, via `_Requirements: CODE-N.M_` footers |
| test files (per `testGlobs` + `testFilePattern`) | **reference** them, via tags, annotations, names, or comments |

### Checks

| Code | Meaning |
|---|---|
| **E1** | a task or test cites an ID that is not defined in any requirements file |
| **E2** | a requirements file with `Status: Implemented` or `Shipped` has a requirement with zero test references |
| **E3** | the same ID is defined more than once |
| **W1** | a requirements file with `Status: Approved` has a requirement not cited by any task |
| **W2** | a requirements file is missing a `Status:` line or a `Feature code:` line |

**Exit code 1** on any error, and on warnings too under `--strict`. Otherwise 0. Zero requirements is a valid clean state.

### The ID grammar

```
/\b([A-Z][A-Z0-9]{1,11})-(\d+)\.(\d+)(?![.\d])/g
```

Two deliberate details. There is **no trailing `\b`**, because a markdown italics footer ends with `_` — a word character — which would silently drop the last ID on the line. And the negative lookahead `(?![.\d])` prevents matching a prefix of a longer number.

A struck-through ID (`~~**SHELL-1.2**~~`) counts as **undefined**, so retiring a requirement immediately surfaces every test and task still citing it as an E1.

### Config — `docs/agents/trace.json`

Optional. Every key falls back to a default.

```json
{
  "specsDir": "docs/specs",
  "testGlobs": ["tests", "test", "e2e", "src", "src-tauri", "crates", "app", "lib", "packages"],
  "testFilePattern": "(\\.(test|spec)\\.[cm]?[jt]sx?$)|([/\\\\]tests?[/\\\\])|…",
  "ignore": []
}
```

**`ignore`** is a list of repo-relative path *substrings* additionally excluded from the test-file scan. It exists for fixture-bearing files — a test file for `check-trace` itself contains ID-shaped example strings that no test asserts. Those are **fixture IDs**, not [citations](../concepts/traceability.md), and scanning them would produce phantom coverage.

Three constraints on `ignore`, from its own spec (`TRACE`): it is a plain path-substring list, not a glob or regex engine; it filters the **test-file walk only** and never excludes a requirements file from *defining* IDs; and it excludes a whole file rather than suppressing an individual error code. It is off by default and applied *on top of* `testGlobs`/`testFilePattern`, never in place of them.

### Who runs it

`verify` (before any "requirements met" claim), `write-plan` (coverage check), `finish-branch` (the merge gate), `release` (gate a), `sync-spec` (before and after pictures), the pre-push git hook, and CI.

---

## `check-graph`

The [feature graph](../concepts/feature-graph.md) linter. The horizontal layer: which features touch the same code.

```bash
node scripts/check-graph.mjs --harvest                              # write GRAPH.md
node scripts/check-graph.mjs --query --json --path P --keyword K    # overlaps as JSON
node scripts/check-graph.mjs --verify                               # lint
```

It harvests from each feature's **existing** `design.md` and `tasks.md` — it authors nothing new — producing a surface manifest (`owns` / `touches`), a reverse index, and summary cards.

### `--verify` checks two things

1. **Freshness** — the committed `<specsDir>/GRAPH.md` must be byte-identical to a fresh render. If it is not: `GRAPH.md is stale — run check-graph --harvest and commit the result.`
2. **Registration** — every harvested feature code must appear in `<specsDir>/INDEX.md`.

Exits 1 on either failure.

### Config

Shares `docs/agents/trace.json`, under an optional `graph` key:

```json
{
  "graph": {
    "sourceRoots": ["src", "src-tauri", "tests", "test", "e2e", "crates", "app", "lib", "packages"],
    "sourceExts": ["ts", "tsx", "js", "jsx", "mjs", "cjs", "rs", "css", "scss", "go", "py"],
    "cardCap": 12
  }
}
```

### Who runs it

`brainstorm` step 1 (`--query`, the dedup check), `code-review` step 3a (`--query`, the reuse-miss check), `sync-spec` (`--harvest`, staged into the sync commit), `verify` (`--verify`, required before "requirements met"), the pre-push hook, and CI.

**Both consuming skills degrade gracefully.** If `check-graph` is absent, the graph is not installed: say so, name `setup-repo` as the remedy, and say it **at most once per session**. If it errors, note that the overlap check was unavailable. Either way, continue — it never blocks a gate.

---

## `vendor-linters`

Installs the two linters into a consuming repo, and detects drift between the two copies.

```bash
node scripts/vendor-linters.mjs --install --to <repo> --scripts-dir <path>
node scripts/vendor-linters.mjs --check   --to <repo> --scripts-dir <path>
node scripts/vendor-linters.mjs --stamp
```

The skill set's own `scripts/` is the **single canonical copy** — deliberately not mirrored into `templates/` — so there is exactly one axis of drift to police.

Each linter carries a stamp of its own body, excluding the stamp line itself, which makes re-stamping idempotent:

```js
// @skills-linter: check-graph sha256:8897837c7133
```

`--check` reports each linter as one of four states, and exits 1 on any drift:

| State | Meaning | `setup-repo`'s response |
|---|---|---|
| `ok` | current | nothing |
| `missing` | never installed | install it |
| `outdated` | the skill set moved on | offer to update |
| `modified` | someone edited the repo's copy | **offer**, never overwrite without an explicit yes — that copy may carry a local fix worth upstreaming |

### Why it exists

The skills read `check-trace.mjs` and `check-graph.mjs` **from the consuming repo**, not from the skill set. A repo that lacks them silently loses the trace spine and the feature graph — and an uninstalled `check-graph` makes `brainstorm` and `code-review` skip their duplication checks forever, which *looks exactly like "no overlapping features"*.

That is why `setup-repo`'s step 6 treats a `check-graph` that prints nothing, exits non-zero, or never writes its file as a **wiring failure** that must be fixed before setup can complete.

---

## `task-brief`

```bash
task-brief <tasks.md> <N>     # writes .skills/task-N-brief.md, prints the path
```

Extracts Task N plus the `## Global Constraints` section into a single file. The implementer subagent reads *this*, never the whole plan.

The brief opens with a line that is doing real work:

```markdown
# Task Brief

This brief is your requirements. Read it fully before starting.
```

Exits 1 if the plan file is missing or Task N is not found.

---

## `review-package`

```bash
review-package <base-sha> <head-sha>    # writes .skills/review-<b7>..<h7>.diff, prints the path
```

Bundles everything a task reviewer needs into one file: the commit list, a diffstat, and the full diff with generous context.

The script's own header carries the warning that `execute-plan` repeats as a red flag:

> **BASE must be the commit recorded BEFORE dispatching the implementer — never `HEAD~1`, which silently drops all but the last commit.**

A reviewer handed a `HEAD~1` package sees a fraction of a multi-commit task and approves it.

---

## Wiring them up

`setup-repo` offers to install both linters into the repo's configured scripts directory, then to wire them into:

- **CI** — appended to an existing workflow, additively. It does not author a pipeline.
- **Git hooks** — `pre-commit` gets the *fast* gates (format staged, lint, typecheck) so commits stay quick; `pre-push` gets the fuller suite plus `check-trace.mjs` and `check-graph.mjs --verify`.

The split matters: *a hook slow enough to be routinely `--no-verify`'d is worse than none.*

If the repo already runs a hook manager (`.husky/`, `lefthook.yml`, `.pre-commit-config.yaml`, `simple-git-hooks`), the commands go into **that** — never a competing mechanism.

## See also

- [Traceability](../concepts/traceability.md) — what `check-trace` is enforcing and why
- [The feature graph](../concepts/feature-graph.md) — what `check-graph` harvests
- [`setup-repo`](../skills/setup-repo.md) — the wizard that installs and proves all of this
- [Troubleshooting](troubleshooting.md) — when a check fails
