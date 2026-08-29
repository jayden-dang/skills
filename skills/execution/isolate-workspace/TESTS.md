# `isolate-workspace` — tests

## Edit — share `.worktrees/` instead of minting `.isolate-workspace/` (v1.1.0)

**Origin.** User request: isolation for skills / execute / check should live
under `.worktrees/`, the conventional project-local worktree parent, instead of
a parallel `.isolate-workspace/` directory and gitignore entry.

**RED (v1.0.0 text).** Git fallback priority:

1. explicit user instruction
2. existing `.isolate-workspace/`
3. existing `isolate-workspace/`
4. neither → **create `.isolate-workspace/`**

`configure-repo` and `land-branch` restated the same parent. A repo that already
ignored `.worktrees/` still got a second ignored path.

**GREEN (v1.1.0).** Default parent is `.worktrees/`. Reuse an existing
`.worktrees/` (or `worktrees/`) rather than minting another directory. Append
`.gitignore` only when `$DIR` is not already ignored. Reuse a legacy
`.isolate-workspace/` / `isolate-workspace/` if one is already on disk, so a
second parent is not created beside it.
