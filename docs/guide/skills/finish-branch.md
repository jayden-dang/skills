# `finish-branch`

> Decide what happens to completed work: gate on the verify suite, detect the environment, offer a fixed menu, execute the choice, clean up safely.

|  |  |
|---|---|
| **Bucket** | ship |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | `docs/agents/project.md` (verify commands), git worktree state (`--git-dir` vs `--git-common-dir`), `docs/specs/` (spec status) |
| **Writes** | local merges, pushed branches and PRs, deleted branches, removed worktrees |
| **Calls** | [`verify`](verify.md) (the gate), [`acceptance-check`](acceptance-check.md) (when user-facing behavior is undriven), [`sync-spec`](sync-spec.md) (to close the loop) |
| **Called by** | [`execute-plan`](execute-plan.md) (its final Finish step) |

## When it fires

When implementation on a branch is complete and committed and an integration decision is needed — you are done with a feature branch and choosing whether to merge it, open a PR, keep it as-is, or discard the work. It is the last step [`execute-plan`](execute-plan.md) runs, and it is distinct from [`release`](release.md): this skill integrates a single branch, it does not cut a version.

## The gate comes first

Before any option is offered, [`verify`](verify.md) runs every verify command from `docs/agents/project.md` — typecheck, lint, unit, e2e — **fresh**, and confirms the [`trace`](trace.md) check is clean. A branch must not merge with untraced requirements; this is the same gate [`release`](release.md) enforces. If no test command is discoverable, the skill asks the user for it and suggests [`setup-repo`](setup-repo.md).

If the branch has user-facing behavior that has not been driven through the running system, [`acceptance-check`](acceptance-check.md) runs before Merge or PR is even offered — green units prove assertions pass, not that the feature works.

**Any failure = STOP.** The skill shows the failures and states that no integration option is available until they pass. It does not present the menu.

## Detect the environment

The skill compares the branch's git directory against the common git directory to learn what kind of workspace it is standing in:

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" && pwd -P)
```

| State | Meaning |
|---|---|
| `GIT_DIR == GIT_COMMON` | normal checkout — no worktree cleanup |
| differ, named branch | linked worktree — provenance-checked cleanup applies |
| differ, detached HEAD | externally managed workspace — no merge option, no cleanup |

The base branch is found via `git symbolic-ref --quiet --short refs/remotes/origin/HEAD` (stripping the leading `origin/`), falling back to `git rev-parse --verify --quiet main || git rev-parse --verify --quiet master`, and confirmed with the user if still ambiguous. The skill carries an explicit warning: `git merge-base` returns a commit SHA, not a branch name — do not use it here.

## The menu

The skill presents exactly these four options, verbatim, with no added commentary:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

On a detached HEAD, option 1 is dropped — a merge is not possible — and the remaining three are renumbered (Push and create a Pull Request, Keep the branch as-is, Discard this work). The decision belongs to the user; the skill does not guess which one they want, and it adds no commentary steering them toward one.

## Executing the choice

**Option 1 — merge locally.** The merge runs from the main repo root, never from inside a worktree:

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git checkout <base-branch> && git pull && git merge <feature-branch>
```

The verify suite is re-run **on the merged result, before any worktree is removed**. Only after that passes does the skill clean up the worktree (see below) and then `git branch -d <feature-branch>`.

**Option 2 — push + PR.** `git push -u origin <feature-branch>`, then create the PR. The worktree is **kept** — the user needs it to iterate on review feedback.

**Option 3 — keep.** Report the branch name and worktree path. Touch nothing.

**Option 4 — discard.** List exactly what will be permanently deleted — branch, commits, worktree path — and require the user to literally type the word `discard`. Anything else, including "yes", "confirm", or "do it", is not confirmation. On confirmation, from the main repo root, clean up the worktree and then `git branch -D <feature-branch>`.

At a glance, the four options differ in what they touch:

| Option | Branch | Worktree | Re-verify |
|---|---|---|---|
| 1 Merge | deleted (`-d`) after merge | removed (if provenance matches) | yes, on the merged result |
| 2 PR | pushed, kept | **kept** for review iteration | no |
| 3 Keep | untouched | untouched | no |
| 4 Discard | deleted (`-D`) | removed (if provenance matches) | no |

## Worktree cleanup (options 1 and 4 only)

Cleanup happens only for a merge or a discard, and only for a worktree whose path sits under `.worktrees/` or `worktrees/` — that provenance means this skill set created it. Anything else, including harness-owned workspaces, is not yours to remove; leave it, or use the platform's own workspace-exit mechanism. The removal is never run from inside the worktree being removed — `cd` to the main repo root first. After removal, `git worktree prune` clears stale metadata.

## Close the loop

On a merge or PR, the skill reminds the user — or does it directly, if the spec's tasks are all complete — to run [`sync-spec`](sync-spec.md) to update the feature's `Status:` line and trace state.

## Red flags

Never:

- Present the menu while any verify command fails
- Remove a worktree before the merged result has passed tests
- Accept anything but the typed word `discard` for option 4
- Remove a worktree outside `.worktrees/`/`worktrees/`, or from inside itself
- Force-push, ever, unless the user explicitly asked

| Thought | Reality |
|---|---|
| "Tests were green an hour ago, skip the gate" | Stale evidence. Anything merged on old green is unverified. |
| "The user obviously wants a PR, skip the menu" | The decision is theirs. Four options, every time. |
| "Cleanup first, then merge — tidier" | A failed merge with the worktree gone loses the work. Merge, verify, then clean. |

## Worked example

A feature branch `feat/shell-module-persistence` is complete in a linked worktree at `.worktrees/shell-module-persistence`. The skill runs [`verify`](verify.md): typecheck, lint, and the unit suite pass fresh, and [`trace`](trace.md) reports every `SHELL` requirement covered. The feature is user-facing, so [`acceptance-check`](acceptance-check.md) drives module persistence through the running app — it passes and leaves committed tests behind.

The environment probe finds `GIT_DIR` differs from `GIT_COMMON` on a named branch: a linked worktree, provenance-checked cleanup applies. The base branch resolves to `main` via `refs/remotes/origin/HEAD`. The four-option menu is presented verbatim, and the user picks option 1.

The skill `cd`s to the main repo root, runs `git checkout main && git pull && git merge feat/shell-module-persistence`, and re-runs the verify suite on the merged result. It passes. Only now does the skill remove `.worktrees/shell-module-persistence` from the main root, `git worktree prune`, `git branch -d feat/shell-module-persistence`, and hand off to [`sync-spec`](sync-spec.md) to flip the feature's status.

Had the user picked option 2 instead, the worktree would have stayed in place so they could push follow-up commits from it in response to review feedback, and no branch would have been deleted. Had they picked option 4, the skill would have printed the branch, its commits, and the worktree path, and waited for the literal word `discard` before removing anything.

## Why it is written the way it is

`finish-branch` sits at the point of highest consequence — the moment work is integrated or destroyed — so it is written to remove every place an agent could act on a guess. The verbatim menu exists because inferring the user's intent here is exactly the failure it guards against: the integration decision is the user's, not the agent's. The typed-`discard` requirement exists because destructive actions must not fire on the same loose affirmatives that carry every other conversation. And the ordering rules — verify before offering, merge and re-verify before cleanup, cleanup only for known-provenance worktrees — all serve one invariant: never lose committed work to a shortcut.

## See also

- [`verify`](verify.md) — the gate that must pass before any option is offered
- [`release`](release.md) — the user-invoked sibling that cuts a version, not a branch merge
- [Traceability](../concepts/traceability.md) — why an untraced requirement blocks the merge
- [`worktrees`](worktrees.md) — how the `.worktrees/` provenance this skill checks gets created
