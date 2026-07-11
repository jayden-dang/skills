# `worktrees`

> Give feature work an isolated workspace with a verified-clean starting point, using the harness's own tools where it has them, before the first file is edited.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | `git rev-parse` output (git-dir vs common-dir, superproject), lockfiles and manifests, `docs/agents/project.md` (the test command) |
| **Writes** | a new git worktree and branch (fallback path), an **uncommitted** `.gitignore` entry, installed dependencies |
| **Calls** | the harness's native workspace tool when one exists (e.g. `EnterWorktree`); suggests `setup-repo` if `docs/agents/project.md` is missing |
| **Called by** | [`execute-plan`](execute-plan.md), [`write-plan`](write-plan.md), [`finish-branch`](finish-branch.md), [`setup-repo`](setup-repo.md) |

## When it fires

Starting feature work, executing a plan, or making any multi-commit change that should not touch the user's current checkout — it sets up the isolated workspace before the first file is edited.

The governing preference order is: **detect isolation that already exists → the harness's native workspace tool → a manual `git worktree` fallback**. The rule underneath all of it is *never fight the harness* — a manual worktree created alongside a native mechanism leaves phantom state the harness cannot see.

## Step 0 — detect and get consent

Compare the private git directory against the common one:

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" && pwd -P)
```

The two paths differ by what those two directories resolve to:

- **`GIT_DIR != GIT_COMMON`** → likely a linked worktree, **but guard against submodules first**: if `git rev-parse --show-superproject-working-tree` prints a path, this is a submodule, not a worktree — treat it as a normal checkout. Otherwise the workspace is already isolated: report the path and branch, skip creation, and go straight to Step 2.
- **`GIT_DIR == GIT_COMMON`** → a normal checkout. Honor a stated worktree preference silently; otherwise ask whether to set up an isolated worktree so the current branch stays untouched. Declined → work in place, go to Step 2.

The submodule guard matters because a submodule's private git dir also differs from its common dir, so without it a submodule reads as "already isolated" and the skill would skip the setup the user actually wanted.

Done when you know which of the three cases you are in, and have consent if creating.

## Step 1 — create the workspace

**1a. Native tool first.** If the harness provides a workspace or worktree mechanism (a tool named like `EnterWorktree`, a `/worktree` command, a `--worktree` flag), use it and go to Step 2. A native tool manages placement, branching, and cleanup itself. Only fall through when none exists.

**1b. Git fallback.** Pick the directory by priority, and use the chosen one in every command that follows — the list is real only if the commands honor it:

1. An explicit user instruction — always wins
2. An existing `.worktrees/` at the repo root
3. An existing `worktrees/` (if both exist, `.worktrees/` wins)
4. Neither → create `.worktrees/`

Before creating anything inside a project-local directory, confirm it is git-ignored. The ignore entry is deliberately **left as an uncommitted working-tree change** — git honors it immediately, and committing `.gitignore` here would write a commit to the user's *current* branch, the exact thing this skill promises not to touch:

```bash
git check-ignore -q "$DIR" || printf '%s/\n' "$DIR" >> .gitignore
git worktree add "$DIR/<branch-name>" -b "<branch-name>"
```

If creation fails on a sandbox or permission error, tell the user and work in place instead.

## Step 2 — install dependencies

Auto-detect the package manager from the lockfile or manifest that is present, then run its install:

- `pnpm-lock.yaml` → pnpm; `bun.lock*` → bun; `yarn.lock` → yarn; `package-lock.json` or a bare `package.json` → npm
- `Cargo.toml` → `cargo build`
- `uv.lock` → uv; `poetry.lock` → poetry; `requirements.txt` → pip
- `go.mod` → `go mod download`

No manifest at all → skip this step.

## Step 3 — clean baseline

Run the test suite using the command in `docs/agents/project.md` (missing → say so, suggest `setup-repo`, and use the ecosystem's default runner).

- **Baseline green** → proceed.
- **Baseline red** → **STOP and ask the user before proceeding.** Starting on a failing baseline makes it impossible to tell your own bugs from pre-existing ones.

The report at the end is three lines: the workspace path and branch, the baseline result (e.g. "N tests passing, 0 failures"), and the task that is ready to start. It exists so the caller — usually [`execute-plan`](execute-plan.md) — can confirm the promise was kept before it edits anything.

## Never

Four hard prohibitions, each the inverse of a step above:

- Create a worktree when Step 0 found you already in one.
- Use `git worktree add` when a native tool exists.
- Create a project-local worktree directory without the ignore check.
- Skip the baseline run, or continue past a red baseline without asking.

## Worked example

A plan is about to be executed on a normal checkout. **Step 0:** `git rev-parse --git-dir` and `--git-common-dir` resolve to the same path, so this is not a linked worktree; `--show-superproject-working-tree` prints nothing, so it is not a submodule either. The user has no stated preference, so the skill asks, and the user agrees to isolation. **Step 1:** the harness exposes no native worktree tool, so the git fallback runs; there is no existing `.worktrees/` or `worktrees/`, so `.worktrees/` is created. `git check-ignore -q .worktrees` fails, so `.worktrees/` is appended to `.gitignore` — and left uncommitted, because a commit here would land on the user's current branch. Then `git worktree add .worktrees/feat-login -b feat-login`. **Step 2:** a `pnpm-lock.yaml` is present, so `pnpm install` runs. **Step 3:** the suite runs green — 143 passing, 0 failures — so the report goes out and execution can begin. Had the baseline come back red, the skill would have stopped and asked rather than let pre-existing failures masquerade as new bugs.

## Why it is written the way it is

The skill exists to make one promise — the user's current checkout is not touched — and every rule serves it. Detecting existing isolation and preferring the native tool avoid creating redundant or phantom state; the submodule guard stops a false "already isolated" reading; and leaving `.gitignore` uncommitted is the subtle one, because the obvious tidy move (commit the ignore entry) would itself break the promise by writing to the current branch. The clean-baseline gate protects a different promise: that any failure discovered later is attributable to this work, not inherited noise.

## See also

- [`execute-plan`](execute-plan.md) — the main caller, which requires an isolated workspace before Task 1
- [`finish-branch`](finish-branch.md) — decides what becomes of the branch this skill created
- [`setup-repo`](setup-repo.md) — writes the `docs/agents/project.md` this skill reads for the test command
- [When to use](../methodology/when-to-use.md) — where workspace isolation sits in the flow
