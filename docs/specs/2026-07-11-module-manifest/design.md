# Design: Module Manifest & Boundary Linting

Feature code: MODMAP
Status: Approved
Date: 2026-07-11
Requirements: ./requirements.md

## Context

M1 adds the boundary source of truth for the enterprise context layer: a small
authored manifest mapping source folders to modules, plus a linter that proves
the manifest covers the real source tree. Everything downstream (the sharded
graph M2, feature homing M3, the on-ramp M4, standards M5) reads this manifest;
M1 authors nothing itself and installs no semantics beyond coverage.

The whole feature lives in `scripts/check_graph.py` — a stdlib-only linter
(`json`, `os`, `re`, `sys`; no argparse, no fnmatch, no pathlib), self-stamped
`# @skills-linter: check-graph sha256:…` and vendored by `vendor_linters.py`,
with a hard invariant of **no top-level side effects on import**. Two facts from
the current code shape the design. First, `check_graph` **never walks the source
tree** — its only filesystem walk (`_walk`, scoped to `specsDir`) finds spec
files, and `sourceRoots`/`sourceExts` are used purely as string-matching config
against paths scraped from spec prose. Enumerating real source folders is
therefore net-new behavior. Second, `_run_verify` accumulates only an `errors`
list and returns `1 if errors else 0`; it has no notion of a non-failing
warning, which MODMAP-3.4 (stale-glob) requires.

The constraint that shapes everything: this must be **purely additive**. A repo
with no `modules` key must behave exactly as today (harvest, query, and the
existing `--verify` freshness + registration checks all unchanged), and the
module must still do nothing at import time.

## Decisions

1. **Manifest home = a `modules` key in `docs/agents/trace.json`.** `load_config`
   already shallow-merges unknown top-level keys through (`{**DEFAULTS, **user}`),
   so a `modules` list passes into `cfg["modules"]` untouched and its absence
   means `cfg.get("modules")` is `None` — zero-config degradation falls out for
   free. (MODMAP-4.1, 4.4)
2. **Two folder sets from one walk.** The walk yields every repo-relative
   directory under a `sourceRoot` (a *repo folder*), and marks the subset that
   directly contains ≥1 file whose extension is in `sourceExts` (a *source
   folder*). The **coverage** checks (orphan / double-map) range only over
   *source folders* — this avoids false orphans on pure-container directories
   (`src/` holding only subfolders) and empty/asset-only directories, which no
   module should be forced to claim. The **stale-glob** check ranges over all
   *repo folders*, so a pattern that legitimately owns a container/asset folder
   is not falsely called stale (aligning with MODMAP-3.4's "no folder in the
   repo").
3. **New walk `enumerate_folders(root, cfg)` parallels `_walk`** — same dotfile
   and `_SKIP_DIRS` exclusions (`node_modules`, `.git`, `dist`, `build`,
   `target`, `coverage`, `.next`, `.skills`, `vendor`) — but targets each
   existing `sourceRoot` and returns `(repo_folders, source_folders)` per
   decision 2. This is the first time the module reads the source tree; it stays
   scoped to `sourceRoots` and skip-listed, and remains import-inert (a function,
   never called at module load).
4. **Owns glob dialect: hand-rolled `_glob_to_re`, supporting `**` and `*`.**
   `**` matches any descendant path including empty (crosses `/`); `*` matches a
   single path segment (never `/`); everything else is literal. So
   `src/auth/**` owns `src/auth` and every folder beneath it, while `src/auth`
   owns exactly that folder. Rejected stdlib `fnmatch`: its `*` crosses `/`, giving
   wrong directory semantics, and hand-rolled `re` matches the module's existing
   style (`_ext_re`, `is_source_path`).
5. **Resolution stays neutral; verification escalates.**
   `resolve_module(path, modules)` returns the **sorted list of matching module
   codes**: `[]` = orphan, `[code]` = home, `[a, b, …]` = ambiguous
   (double-mapped). The list encoding carries the same three cases without a
   sentinel and is what M3 (feature homing) will consume. The resolve API is
   deliberately non-judging; only `_verify_boundaries` turns an empty/multi list
   *on a source folder* into an error. It normalizes the path **minimally**
   (strip a leading `./` and trailing `/`) — deliberately NOT via `normalize_path`,
   whose locator-stripping rules would corrupt a digit-suffixed folder segment
   (`src/store2` → `src/store`). (MODMAP-2.3 vs 3.2/3.3)
6. **A distinct `warnings` channel in `_run_verify`.** Add a `warnings` list
   beside `errors`; the exit code stays `1 if errors else 0`, so warnings print
   but never fail the gate. Stale-glob is the sole warning. (MODMAP-3.4, 3.6, 3.7)
7. **Boundary checks run inside `--verify` when a manifest is present — no new
   flag.** Validity errors (missing fields, dup/malformed codes) short-circuit
   the coverage pass, since coverage over an invalid manifest is meaningless. The
   existing freshness + registration checks always run first, whether or not a
   manifest exists. (MODMAP-1.3, 4.3)

No decision here is hard-to-reverse *and* surprising *and* a real trade-off, so
no ADR is warranted — all are internal, test-covered, and cheaply changed.

## Architecture

### Config integration & manifest loader

Satisfies: MODMAP-1.1, MODMAP-1.2, MODMAP-1.3, MODMAP-1.4, MODMAP-1.5, MODMAP-4.1, MODMAP-4.4

`load_config` is unchanged — it keeps resolving `specsDir` and the deep-merged
`graph` config, and now simply carries a `modules` list through when present
(4.4). A new `load_manifest(cfg)` reads `cfg.get("modules")`:

- Absent → returns `([], [])` and the caller treats the layer as disabled (4.1).
- Present → parses each entry into `{code, name, owns:[str], layer?, owner?}`
  (1.1), preserving optional `layer`/`owner` verbatim (1.2), and collects
  **validity errors** without raising: an entry missing `code`/`name`/non-empty
  `owns` (1.3), a duplicate `code` across entries (1.4), or a `code` failing the
  full-string shape `^[A-Z][A-Z0-9]{1,11}$` (1.5). Returns
  `(modules, validity_errors)`.

That shape is the **uppercase** feature-code namespace the codebase already uses
(the harvest extractor `check_graph.py:322` and `check_trace.py:52` both anchor
`[A-Z][A-Z0-9]{1,11}`); MODMAP-1.5's "A–Z0–9, starting with a letter" is the
same shape as a full-string validator, so module codes and feature codes stay in
one namespace. (Those existing regexes are extraction-anchored, so a
full-string validator is authored fresh — just with the same character class,
not a widened one.)

### Glob dialect & path→module resolution

Satisfies: MODMAP-2.1, MODMAP-2.2, MODMAP-2.3

`_glob_to_re(pattern)` compiles one `owns` glob to a regex per decision 4,
cached per pattern. `resolve_module(path, modules)` minimally normalizes the
path (strip leading `./` and trailing `/`; not `normalize_path`) and tests it
against every module's compiled `owns` patterns, returning the sorted list of
matching codes:

- exactly one module matches → `[code]` (2.1);
- two or more match → `[a, b, …]` (2.2);
- none match → `[]` (2.3).

The function is pure over `(path, modules)` and holds no verification opinion,
so M3 can call it to home features without inheriting boundary-error behavior.

### Folder enumeration

Satisfies: MODMAP-3.1

`enumerate_folders(root, cfg)` walks each existing `sourceRoot` under `root` with
the same `os.scandir` recursion and skip rules as `_walk`, returning
`(repo_folders, source_folders)` — the sorted, de-duplicated repo-relative
directories, and the subset directly containing a `sourceExts` file (decision 2).
A `sourceRoot` that does not exist on disk is skipped silently (a repo need not
have every default root).

### Boundary verification sub-check

Satisfies: MODMAP-3.2, MODMAP-3.3, MODMAP-3.4, MODMAP-3.5

`_verify_boundaries(root, cfg, modules) → (errors, warnings)`:

1. For each **source folder**, call `resolve_module`:
   `None` → append an **orphan-folder error** naming the folder (3.2);
   `Ambiguous(codes)` → append a **double-mapped-folder error** naming the
   folder and the competing codes (3.3).
2. For each module `owns` pattern, test it against every **repo folder** (every
   directory under a `sourceRoot`, source-bearing or not); a pattern matching
   none → append a **stale-glob warning** naming the module and pattern (3.4).
   Ranging over all source-rooted folders (not just source-bearing ones) avoids
   false staleness on a glob that owns a container/asset folder.
3. When the source-folder set is non-empty, every source folder resolved to
   exactly one module, and there are no errors, the pass contributes nothing —
   leaving `_run_verify` to report OK (3.5).

Error strings use the existing `E:` convention; warnings use a `W:` prefix.

### `--verify` integration, exit model & degradation guards

Satisfies: MODMAP-3.6, MODMAP-3.7, MODMAP-4.2, MODMAP-4.3, MODMAP-4.5

`_run_verify(root, cfg, specs_dir, as_json)` keeps its two existing checks
(GRAPH.md freshness, INDEX.md registration) exactly as they are (4.3), then:

- `modules, validity_errors = load_manifest(cfg)`.
- No manifest (`modules == []` and nothing declared) → skip the boundary pass
  entirely; harvest/query paths are never touched by this feature (4.2).
- `validity_errors` present → extend `errors` with them and **skip** the
  coverage pass (decision 7).
- Otherwise → `berrors, warnings = _verify_boundaries(...)`; extend `errors`
  with `berrors` and collect `warnings`.

Exit stays `return 1 if errors else 0`, so warnings never flip it (3.6, 3.7).
Output gains an additive `warnings` channel: JSON mode emits
`{"errors": [...], "warnings": [...]}`; text mode prints a `warnings:` section
after the errors. All new logic lives in functions invoked only from
`_run_verify`; the module adds no top-level statements, preserving import
inertness (4.5). After editing, re-stamp with `vendor_linters.py --stamp`.

## Seams for testing

All seams are unit/integration entry points inside the existing
`scripts/check_graph_test.py` module-test surface — no new public seam is
introduced, only new functions tested the same way `harvest`/`query`/`_run_verify`
already are.

| Seam | Kind | Covers |
|---|---|---|
| `load_manifest(cfg)` | unit | MODMAP-1.1, 1.2, 1.3, 1.4, 1.5, 4.1, 4.4 |
| `_glob_to_re` + `resolve_module(path, modules)` | unit | MODMAP-2.1, 2.2, 2.3 |
| `enumerate_folders(root, cfg)` over a tmp source tree | unit | MODMAP-3.1 |
| `_verify_boundaries(root, cfg, modules)` over a tmp tree | unit | MODMAP-3.2, 3.3, 3.4, 3.5 |
| `_run_verify(...)` / `main(argv)` return code over a tmp repo | integration | MODMAP-3.6, 3.7, 4.2, 4.3, 4.5 |

## Coverage check

All 20 requirement IDs map to exactly one Satisfies line:

- Story 1 — 1.1, 1.2, 1.3, 1.4, 1.5 → Config integration & manifest loader.
- Story 2 — 2.1, 2.2, 2.3 → Glob dialect & path→module resolution.
- Story 3 — 3.1 → Source-folder enumeration; 3.2, 3.3, 3.4, 3.5 → Boundary
  verification sub-check; 3.6, 3.7 → `--verify` integration & exit model.
- Story 4 — 4.1, 4.4 → Config integration & manifest loader; 4.2, 4.3, 4.5 →
  `--verify` integration & degradation guards.

No IDs are deliberately unmapped.
