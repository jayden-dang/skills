---
name: trace
description: Use when checking that every requirement ID traces to a task and a
  covering test — the traceability / check-trace pass invoked by verify, release,
  sync-spec, and write-plan's coverage check, or whenever requirements, tasks, and
  tests may have drifted out of agreement. Produces a traceability finding set —
  IDs cited but never defined, Implemented/Shipped requirements with no covering
  test, duplicate definitions, and approved-but-uncited warnings.
---

# Trace

The vertical traceability check. It answers one question with evidence: **does
every requirement ID agree across where it is defined, cited, and tested?**

It is not a judgment call. Every input is gathered with `grep` and reads —
deterministic passes — and every finding follows a fixed rule. Two agents running
this on the same repo reach the same finding set.

## What it produces

A finding set, each item an ERROR or a WARNING:

| Code | Tier | Condition |
|---|---|---|
| **E1** | error | A task or test cites an ID that no requirements file defines |
| **E2** | error | An `Implemented` or `Shipped` requirement has no covering test |
| **E3** | error | The same ID is defined (bold) in more than one file |
| **W1** | warn | An `Approved` requirement is cited by no task |
| **W2** | warn | A `requirements.md` is missing its `Status:` or `Feature code:` line |

Errors mean the trace is broken. Warnings mean the trace is incomplete but not
wrong. `verify`/`release` treat any error as a failing gate; warnings are reported,
not fatal, unless the caller says otherwise.

## Inputs

- **Specs** live under `docs/specs/` (or the `specsDir` named in
  `docs/agents/project.md`). Definitions come from files ending `requirements.md`
  or `fixes.md`; task citations from files ending `tasks.md`.
- **Tests** live under the repo's test locations. Default roots to search:
  `tests test e2e src src-tauri crates app lib packages` (skip any that don't
  exist). Within them, a **test file** is one whose path matches:
  `\.(test|spec)\.[cm]?[jt]sx?$` · a `/tests?/` or `/e2e/` path segment ·
  `_test\.(rs|go|py)$` · or any `.rs` file (Rust cites IDs in doc comments).
- If `docs/agents/project.md` names different test globs or an ignore list, use
  those instead. If it is absent, say so and use the defaults.
- Skip `node_modules .git dist build target coverage .next .skills vendor` and any
  dotfile/dot-dir.

## The passes

Run these against the repo root. Read the full output of each — coverage depends on
gathering *every* matching file, not a sample.

**1. Definitions** — bold IDs in requirements/fixes files, minus retired ones.

```bash
# every bold **CODE-N.M** in a requirements/fixes file
grep -rnoE '\*\*[A-Z][A-Z0-9]{1,11}-[0-9]+\.[0-9]+\*\*' docs/specs \
  --include='*requirements.md' --include='fixes.md'
```

A bold ID inside a `~~ … ~~` strikethrough is **retired** — it is not a definition.
Strip strikethrough spans before counting a line's bold IDs. A plain (non-bold) ID
in a requirements file is prose, not a definition.

**2. Statuses and feature codes** — per requirements file.

```bash
grep -rnE '^(Status:|Feature code:)' docs/specs --include='*requirements.md'
```

`Status:` is one of `Draft | Approved | Implemented | Shipped` (first match wins).
`fixes.md` is exempt from W2 — it needs neither line.

**3. Task citations** — IDs on `_Requirements:` lines.

```bash
grep -rhoE '_Requirements:.*' docs/specs --include='*tasks.md' \
  | grep -oE '[A-Z][A-Z0-9]{1,11}-[0-9]+\.[0-9]+'
```

Only IDs on a line containing the literal `_Requirements:` are task citations.

**4. Test coverage** — every ID string appearing anywhere in a test file. Search
each existing test root; here is the JS/TS + Rust default:

```bash
grep -rhoE '[A-Z][A-Z0-9]{1,11}-[0-9]+\.[0-9]+' \
  $(printf '%s ' tests test e2e src src-tauri crates app lib packages) 2>/dev/null \
  --include='*.test.*' --include='*.spec.*' --include='*_test.rs' \
  --include='*_test.go' --include='*_test.py' --include='*.rs' \
  | sort -u
```

Adjust the roots/includes to the repo's actual layout. The ID grammar is
`[A-Z][A-Z0-9]{1,11}-<major>.<minor>`; a three-level ID like `CODE-1.2.3` is a
different token — do not let `CODE-1.2` match inside it.

## The rules

With the four sets in hand — `defined` (ID → {file, status}), `taskCited`,
`testCovered` — apply:

- **E1** — for each ID in `taskCited ∪ testCovered` not in `defined`: report it and
  the citing file(s).
- **E2** — for each `defined` ID whose status is `Implemented` or `Shipped` and is
  **not** in `testCovered`: report it. (A task citation does not satisfy E2 — only a
  test does.)
- **E3** — for each ID bold-defined in two or more distinct files: report the files.
  (Two bold occurrences in the *same* file are not a duplicate.)
- **W1** — for each `defined` ID whose status is exactly `Approved` and not in
  `taskCited`: report it.
- **W2** — for each `requirements.md` (never `fixes.md`) missing a `Status:` or a
  `Feature code:` line: report which line is missing.

Status obligations at a glance:

| Status | Needs a test (E2) | Needs a task (W1) |
|---|---|---|
| Draft | no | no |
| Approved | no | **yes** |
| Implemented / Shipped | **yes** | no |

## <NON-NEGOTIABLE> Coverage is textual presence — do not judge it

An ID is **covered** when its string appears in a test file. Full stop. Do not read
the test to decide whether it "really" exercises the requirement, whether the
assertion is meaningful, or whether a commented-out line should count. That judgment
is not part of this check, and adding it makes the result depend on the reader —
which is the one thing this check exists to prevent.

The only sanctioned exclusion is an **ignore list** in `docs/agents/project.md`:
files (e.g. a fixture or test-support file that carries IDs as data) named there are
dropped from the test search wholesale — never ID-by-ID by hand.

Likewise: gather **every** matching file. Missing one test file invents a false E2;
missing one requirements file invents a false E1. Grep the whole tree; do not
sample or reason about which files "probably" matter.

## Output

Report the counts, then the findings:

```
trace: 24 requirements · 24 task-cited · 22 tested · 18 test files
  ERROR E1 test cites unknown requirement SHELL-9.9 (src/shell.test.ts)
  ERROR E2 SHELL-1.4 (docs/specs/2026-07-01-shell/requirements.md, Implemented) has no covering test
  warn  W1 NOTES-2.1 (…/requirements.md, Approved) is not cited by any task
```

Exact wording and ordering are not contractual — the **finding set** is. If
`docs/specs/` does not exist, say there is nothing to check and stop. When a caller
(verify, release) needs a pass/fail, the gate is: zero errors.
