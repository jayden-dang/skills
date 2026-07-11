# Design: Brownfield On-Ramp — Manifest Seed

Feature code: MODSEED
Status: Approved
Date: 2026-07-11
Requirements: ./requirements.md

## Context

M4 adds a `check-graph --seed` mode that drafts a module manifest from a repo's
directory structure and prints it for a human to paste into `trace.json`. Every
piece it needs already exists in `check_graph.py`: `enumerate_folders(root, cfg)`
(`check_graph.py:391`) walks each existing `graph.sourceRoots` directory and
returns `(repo_folders, source_folders)` — sorted repo-relative dir paths, with
the bare root included and each immediate child stored as `<root>/<name>`;
`_MODULE_CODE_RE = ^[A-Z][A-Z0-9]{1,11}$` (`:781`) defines a valid code;
`load_manifest(cfg)` (`:784`) is the validator the draft must round-trip through
cleanly; and `main(argv)` (`:931`) already dispatches `--query`/`--verify` before
the `--harvest` default and returns an int without calling `sys.exit`, so a new
read-only branch slots in beside them. The seed writes nothing and reuses the
harvest machinery downstream: once its output is pasted in, M2's `--harvest`
renders the map and M1's `--verify` checks boundaries.

Two constraints shape the design. First, **round-trip validity is the load-
bearing property** (MODSEED-3.1): every drafted code must satisfy
`_MODULE_CODE_RE`, whose quantifier `{1,11}` after the leading letter means a
code is **2–12 characters** — so a single-character directory (`a` → `A`) is
*invalid* and the normalizer must guarantee a ≥2-char, letter-first, uppercase-
alnum result for *every* possible directory name, or the whole draft fails to
load. Second, the mode must be **purely read-only** (MODSEED-4.1): it may walk
the tree but must create, modify, or delete nothing, and must ignore any existing
`cfg["modules"]` (MODSEED-4.2) — it is a suggestion tool, not a config editor.

## Decisions

1. **Reuse `enumerate_folders`; do not add a second tree walk.** `seed` calls
   `enumerate_folders(root, cfg)`, takes `repo_folders`, and filters to the
   immediate children of each existing source root — an entry `f` is an immediate
   child of root `r` iff `f.startswith(r + "/")` and `f[len(r)+1:]` contains no
   `/`. This inherits the exact dotfile/`_SKIP_DIRS` exclusions the boundary
   linter already applies, so the seed and `--verify` agree on what a "folder"
   is. A dedicated `os.scandir` helper was rejected: it would duplicate the
   exclusion logic and could drift from `enumerate_folders`.
2. **One normalizer, `_seed_code(name)`, that always returns a valid code.**
   Keep `[A-Z0-9]` of the uppercased name; if the result is empty or does not
   start with a letter, prefix `M`; truncate to 12; if still shorter than 2,
   append `0`. This yields a 2–12-char, letter-first code for every input
   (`auth`→`AUTH`, `2024`→`M2024`, `a`→`A0`, `___`→`M0`, a 14-char name → its
   first 12). The `+"0"` tail is the guarantee that closes the min-length-2 edge.
3. **Deterministic collision suffixing (MODSEED-1.6).** After normalization,
   process drafts in sorted order; the first claimant of a code keeps it, and any
   later collision takes the smallest integer `n ≥ 2` whose suffix, appended to a
   base truncated to `12 - len(str(n))`, is unused and still matches
   `_MODULE_CODE_RE`. Truncating the base before appending keeps the result ≤ 12;
   the base's first char is a letter, so `base + digits` always matches the regex.
4. **A pure `seed(root, cfg) → {"modules": [...]}` builder, a thin CLI branch.**
   `seed` does all the work and is unit-testable without the CLI; the `--seed`
   branch in `main` is two lines: `print(json.dumps(seed(root, cfg), indent=2,
   ensure_ascii=False))` then `return 0`. This mirrors how `--query` is a thin
   wrapper over `query`.
5. **Total ordering for byte-identical output (MODSEED-2.2).** `seed` sorts the
   drafted modules by `code` and each module's `owns` list, so a re-run over an
   unchanged tree prints identical bytes.
6. **Directories only; ignore existing manifest.** Only immediate child
   *directories* become modules (loose root files are out of scope, per the
   approved requirements); `seed` never reads `cfg["modules"]` (MODSEED-4.2).

No decision here is hard-to-reverse AND surprising AND a real trade-off, so no
ADR. `seed` is a single-shape read-only mode reusing an existing walk, not a new
boundary — so no parallel design exploration.

## Architecture

### `_seed_code` — directory name → valid module code

Satisfies: MODSEED-1.3, MODSEED-1.4

```
_seed_code(name: str) -> str
```

Steps: `s = "".join(c for c in name.upper() if "A" <= c <= "Z" or "0" <= c <=
"9")`; if `not s or not s[0].isalpha()` then `s = "M" + s` (MODSEED-1.4);
`s = s[:12]` (MODSEED-1.3 upper bound); if `len(s) < 2` then `s = s + "0"`
(closes the min-length-2 edge so the result always matches `_MODULE_CODE_RE`).
Pure, total, deterministic — defined for every string.

### `seed` — draft the manifest from the tree

Satisfies: MODSEED-1.1, MODSEED-1.2, MODSEED-1.5, MODSEED-1.6, MODSEED-2.2, MODSEED-3.1, MODSEED-3.2, MODSEED-4.2

```
seed(root, cfg) -> {"modules": [ {"code","name","owns"}, ... ]}
```

- `repo_folders, _ = enumerate_folders(root, cfg)`; `existing_roots = [r for r in
  cfg["graph"]["sourceRoots"] if r in repo_folders]` (the bare root is in
  `repo_folders` only when it exists on disk).
- **Immediate children** (MODSEED-1.1): each `f in repo_folders` that is one
  segment below some `existing_root` becomes a candidate; its `owns` is
  `[f + "/**"]` (MODSEED-1.2) and its `name` is `f.rsplit("/", 1)[-1]`, the child
  directory's own last segment, unmodified (MODSEED-1.5).
- **Codes + collisions**: `code = _seed_code(name)`; drafts are sorted by
  `(code, owns)` and passed through the suffixing rule (Decision 3) so every code
  is unique (MODSEED-1.6).
- **Determinism**: sort each module's `owns`, then sort modules by `code`
  (MODSEED-2.2).
- Every module carries a valid non-empty `code`, a non-empty `name` (a real
  directory segment is never empty), and a one-element `owns` list (MODSEED-3.2),
  and no code repeats — so the returned `modules` load through `load_manifest`
  with zero validity errors (MODSEED-3.1). `seed` never reads `cfg["modules"]`
  (MODSEED-4.2). Read-only: it only walks and builds.

### `--seed` — the CLI branch

Satisfies: MODSEED-2.1, MODSEED-2.3, MODSEED-2.4, MODSEED-4.1, MODSEED-4.3

In `main`, after the `--verify` branch and before the `--harvest` default: if
`"--seed" in argv`, print `json.dumps(seed(root, cfg), indent=2,
ensure_ascii=False)` (one `{"modules": [...]}` object, MODSEED-2.1) and
`return 0` (MODSEED-2.3). When no source root exists on disk, `enumerate_folders`
returns `([], [])`, so `seed` returns `{"modules": []}` and the branch prints it
and returns 0 (MODSEED-2.4). The branch writes nothing (MODSEED-4.1) and leaves
`--harvest`/`--verify`/`--query` dispatch untouched (MODSEED-4.3). `main`'s
existing `ConfigError` handling still applies before any branch runs.

### Import inertness (infrastructure)

Satisfies: MODSEED-4.4

`seed`, `_seed_code`, and the `--seed` branch are `def`s / a conditional inside
`main`; nothing new runs at import (MODSEED-4.4).

## Seams for testing

Two new pure seams (`_seed_code`, `seed`) plus the existing `main` CLI seam.

| Seam | Kind | Covers |
|---|---|---|
| `_seed_code(name)` over tricky names | unit | MODSEED-1.3, 1.4 |
| `seed(root, cfg)` over a `_tmp_repo` tree | unit | MODSEED-1.1, 1.2, 1.5, 1.6, 2.2, 3.1, 3.2, 4.2 |
| `--seed` via `main` over a `_tmp_repo` | integration | MODSEED-2.1, 2.3, 2.4, 4.1, 4.3 |
| import-inertness reload check | unit | MODSEED-4.4 |

The round-trip (MODSEED-3.1) is tested at the `seed` seam by feeding
`seed(...)["modules"]` back into `load_manifest` and asserting zero errors.

## Coverage check

All 16 requirement IDs map to exactly one Satisfies line:

- Story 1 — 1.3, 1.4 → `_seed_code`; 1.1, 1.2, 1.5, 1.6 → `seed`.
- Story 2 — 2.2 → `seed`; 2.1, 2.3, 2.4 → `--seed` CLI.
- Story 3 — 3.1, 3.2 → `seed`.
- Story 4 — 4.1, 4.3 → `--seed` CLI; 4.2 → `seed`; 4.4 → import inertness.

No IDs are deliberately unmapped.
