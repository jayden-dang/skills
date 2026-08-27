# ResolvedRange (change-impact)

## Contents

- [Object](#object)
- [Inputs](#inputs)
- [Omitted-range cascade](#omitted-range-cascade)
- [Hard-stops](#hard-stops)
- [Dirty fingerprint](#dirty-fingerprint)

Resolve **once**, snapshot **once**, pass the same object to mapping, stops,
production, ledger, and export.

## Object

Minimum fields (names may be kebab or snake; keep one convention per run):

| Field | Meaning |
|---|---|
| `schema_version` | e.g. `1` |
| `base` / `head` | Tree-ish tips compared |
| `mode` | `commit` \| `dotdot` \| `dotdotdot` \| `uncommitted` \| … |
| `paths` | Rename-aware inventory rows |
| `fingerprint` | Hash of relevant dirty state when worktree involved |
| `scope_notice` | Optional human notice (e.g. dirty + branch commits) |

Inventory row: `status`, `similarity` (if rename), `old_path`, `new_path`.

## Inputs

| Input | Resolution |
|---|---|
| Single commit | Parent→commit; root commit → empty tree |
| `A..B` | Literal tree-to-tree |
| `A...B` | merge-base(A,B)→B |
| `uncommitted` | Staged + unstaged **tracked** |
| Path filters | Optional; empty after filter → hard-stop |
| Untracked | Only with `--include-untracked` or concrete path |

## Omitted-range cascade

First match wins:

1. Pure untracked → **hard-stop**
2. Tracked dirty → `HEAD → WORKTREE`
3. Clean → `merge-base(default_branch, HEAD) → HEAD`
4. Empty result → **hard-stop**

Default branch (local only): `origin/HEAD` → `main` → `master`; else require
explicit range (no network guess).

## Hard-stops

Ambiguous input, unresolved refs, invalid comparison, path-filtered empty,
cannot snapshot → hard-stop. Write **diagnostic attempt only** — no success
checkpoint, no `demonstrated`, no partial success export, no overwrite of prior
success ledger.

Binary/submodule-only: inventory allowed; semantic claims stay `unverified`
without a readable oracle.

## Dirty fingerprint

If fingerprint changes mid-run → `stale_during_run`: no `demonstrated`, no export.
