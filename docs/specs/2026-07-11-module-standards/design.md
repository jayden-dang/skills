# Design: Per-Module Standards Resolution

Feature code: MODSTD
Status: Approved
Date: 2026-07-12
Requirements: ./requirements.md

## Context

M5 adds a standards layer to the module model: a project-wide baseline plus
optional per-module overrides, authored inline in `docs/agents/trace.json`, and
resolved into a module's effective standards. Everything lives in
`check_graph.py`, and the plumbing already fits: `load_config` merges trace.json
over DEFAULTS with `{**DEFAULTS, **user}` (`check_graph.py:776`), so a new
top-level `standards` key survives untouched as `cfg.get("standards")`;
`load_manifest(cfg)` builds each module dict from `entry.get(...)` fields
(`:822-828`), so carrying a new `standards` field is additive; and `main`
already dispatches read-only modes (`--query`, `--verify`, `--seed`) before the
`--harvest` default, so a read-only `--standards` branch slots in beside them.

One current-code fact forces a specific decision. `load_manifest` **early-returns
`([], [])` when no `modules` are declared** (`:792-793`), and its validity errors
are the channel `--verify` reports (`_run_verify` does `errors.extend(
validity_errors)` at `:949-950`, exit `1 if errors else 0` at `:975`). MODSTD-1.4
requires a malformed **baseline** `standards` to be reported *even when no modules
exist* — so baseline validation cannot live inside `load_manifest`'s per-entry
loop or anywhere after that early return, or it would be silently skipped in the
exact case the requirement calls out.

The second shaping constraint is that resolution and validation are **separate
concerns**. Resolution (`--standards`, and M6's consumers) must be *total* — it
can never crash, even on a malformed config — while validation (`--verify`) is
where malformed input is *reported*. Conflating them would make a bad config
either crash resolution or suppress the validity error.

## Decisions

1. **One pure validator, `_standards_errors(cfg)`, independent of the modules
   early-return.** It validates the baseline `standards` and every module
   entry's `standards` directly from `cfg`, returns a list of error strings
   (empty when clean), and never raises. `_run_verify` calls it unconditionally
   (not behind any `modules`-present guard), so a malformed baseline is reported
   whether or not modules exist (MODSTD-1.4). `load_manifest` does **not**
   validate standards — it only carries the field. This keeps all standards
   validation in one DRY, independently-testable place and sidesteps the
   early-return trap entirely. Rejected: validating module standards inside
   `load_manifest`'s loop and the baseline just before its early return — that
   splits one rule across two sites and couples baseline (a top-level config
   concern) into the manifest loader.
2. **`load_manifest` carries `module["standards"]` verbatim, additively.** It
   appends `"standards": entry.get("standards")` to the built dict (MODSTD-1.2,
   4.2). It carries the value as-is (even if malformed) — nothing downstream
   consumes it unsafely, and `_standards_errors` is what flags a bad value.
3. **`resolve_standards(code, cfg)` is total and defensive.** Baseline =
   the string items of `cfg.get("standards")`; module = the string items of the
   matching entry's `standards` (or none); effective = `baseline + module`
   deduplicated keeping first occurrence. A non-list or non-string/empty item is
   simply skipped, so resolution never crashes on a malformed config (validity is
   `--verify`'s job). An unknown code contributes nothing → baseline alone
   (MODSTD-2.1–2.4).
4. **The `--standards` CLI validates the code; the resolver does not.** The CLI
   reads the code after `--standards` via the existing `_collect_flag` helper,
   checks it against the declared module codes from `load_manifest(cfg)`, and
   errors (stderr, exit 1) on a missing or unknown code (MODSTD-3.2, 3.3);
   otherwise it prints `{"module": <CODE>, "standards": resolve_standards(...)}`
   and returns 0 (MODSTD-3.1). The resolver's own unknown-code branch (2.3) stays
   total for M6's defensive callers and is tested at the resolver seam.
5. **Read-only and deterministic.** `--standards` only reads and prints; both
   `_standards_errors` and `resolve_standards` are pure. `resolve_standards`
   preserves order, so `json.dumps` output is byte-identical across runs
   (MODSTD-3.4, 4.3).

No decision here is hard-to-reverse AND surprising AND a real trade-off, so no
ADR. Each piece is a small pure function or a CLI branch in an established
pattern, so no parallel design exploration.

## Architecture

### `load_manifest` carries `module["standards"]`

Satisfies: MODSTD-1.2, MODSTD-4.1, MODSTD-4.2

Add `"standards": entry.get("standards")` to the module dict built at
`check_graph.py:822-828`. Purely additive: the existing code/name/owns/layer/
owner fields are untouched (MODSTD-4.2), and when no `standards` is declared
anywhere the field is `None` and every existing mode behaves exactly as today
(MODSTD-4.1). `load_manifest` performs no standards *validation* (that is
Decision 1).

### `_standards_errors` — validate baseline and module standards

Satisfies: MODSTD-1.3, MODSTD-1.4, MODSTD-1.5

```
_standards_errors(cfg) -> [error_str, ...]
```

A `standards` value is valid iff it is absent (`None`) or a list of non-empty
strings; an empty list is valid ("no standards", MODSTD-1.5). The helper checks
`cfg.get("standards")` (labelled `baseline`, MODSTD-1.4) and — when
`cfg.get("modules")` is a list — each dict entry's `standards` (labelled by its
code, MODSTD-1.3), appending one error string per malformed value. It never
raises. `_run_verify` calls `errors.extend(_standards_errors(cfg))`
unconditionally, so these flow to the existing error channel and affect the exit
code, independent of whether any module is declared.

### `resolve_standards` — effective standards for a module

Satisfies: MODSTD-1.1, MODSTD-2.1, MODSTD-2.2, MODSTD-2.3, MODSTD-2.4

```
resolve_standards(code, cfg) -> [rule_str, ...]
```

Reads the baseline from the top-level `standards` key (MODSTD-1.1) and the
module's own `standards` from the matching `cfg["modules"]` entry. Effective =
baseline rules followed by module rules (MODSTD-2.1), deduplicated keeping the
first occurrence (MODSTD-2.2). An unknown code matches no entry → baseline alone
(MODSTD-2.3); nothing declared → `[]` (MODSTD-2.4). Defensive: a non-list value
or a non-string/empty item is skipped, so resolution is total even on a config
that `_standards_errors` would flag.

### `--standards` — the CLI branch

Satisfies: MODSTD-3.1, MODSTD-3.2, MODSTD-3.3, MODSTD-3.4, MODSTD-4.3

In `main`, after the `--seed` branch and before the `--harvest` default: read the
value after `--standards` via `_collect_flag(argv, "--standards")`. A missing
code → error to stderr, return 1 (MODSTD-3.3). Otherwise load the declared module
codes from `load_manifest(cfg)` (filtering falsy codes); an unknown code → error
to stderr, return 1 (MODSTD-3.2). A declared code → print
`json.dumps({"module": code, "standards": resolve_standards(code, cfg)}, indent=2,
ensure_ascii=False)` and return 0 (MODSTD-3.1). The branch only reads and prints
(MODSTD-4.3) and its output is deterministic (MODSTD-3.4).

### Import inertness (infrastructure)

Satisfies: MODSTD-4.4

`_standards_errors`, `resolve_standards`, and the `--standards` branch are `def`s
/ a conditional inside `main`; nothing new runs at import (MODSTD-4.4).

## Seams for testing

Two new pure seams (`_standards_errors`, `resolve_standards`) plus the existing
`load_manifest` and `main` CLI seams.

| Seam | Kind | Covers |
|---|---|---|
| `resolve_standards(code, cfg)` | unit | MODSTD-1.1, 2.1, 2.2, 2.3, 2.4 |
| `_standards_errors(cfg)` | unit | MODSTD-1.3, 1.4, 1.5 |
| `load_manifest(cfg)` (carries `standards`) | unit | MODSTD-1.2, 4.2 |
| `--standards` via `main` over a `_tmp_repo` | integration | MODSTD-3.1, 3.2, 3.3, 3.4, 4.3 |
| `--verify` / no-standards behavior via `main` | integration | MODSTD-4.1 |
| import-inertness reload check | unit | MODSTD-4.4 |

## Coverage check

All 17 requirement IDs map to exactly one Satisfies line:

- Story 1 — 1.1 → `resolve_standards`; 1.2 → `load_manifest`; 1.3, 1.4, 1.5 →
  `_standards_errors`.
- Story 2 — 2.1, 2.2, 2.3, 2.4 → `resolve_standards`.
- Story 3 — 3.1, 3.2, 3.3, 3.4 → `--standards` CLI.
- Story 4 — 4.1, 4.2 → `load_manifest`; 4.3 → `--standards` CLI; 4.4 → import
  inertness.

No IDs are deliberately unmapped.
