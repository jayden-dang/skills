---
name: finish-branch
description: Use when implementation on a branch is complete and committed and an
  integration decision is needed — done with a feature branch and choosing
  whether to merge it, open a PR, keep it as-is, or discard the work.
---

# Finish a Branch

Decide what happens to completed work: gate on the verify suite, detect the environment, offer a fixed menu, execute the choice, clean up safely.

## 1. Gate: verify, trace, and acceptance

REQUIRED SUB-SKILL: use `verify` to run every verify command from `docs/agents/project.md` (typecheck, lint, unit, e2e) fresh AND to confirm the `trace` check is clean — a branch must not merge with untraced requirements, the same gate `release` enforces. If no test command is discoverable, ask the user for it and suggest `setup-repo`.

If the branch has user-facing behavior that has not been driven through the running system, REQUIRED SUB-SKILL: use `acceptance-check` before offering Merge or PR — green units prove assertions pass, not that the feature works.

**Any failure = STOP.** Show the failures and state that no integration option is available until they pass. Do not present the menu.

## 2. Detect the environment

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" && pwd -P)
```

| State | Meaning |
|---|---|
| `GIT_DIR == GIT_COMMON` | normal checkout — no worktree cleanup |
| differ, named branch | linked worktree — provenance-checked cleanup applies |
| differ, detached HEAD | externally managed workspace — no merge option, no cleanup |

Determine the base branch — `git symbolic-ref --quiet --short refs/remotes/origin/HEAD` (strip the leading `origin/`), falling back to `git rev-parse --verify --quiet main || git rev-parse --verify --quiet master`. Confirm with the user if still ambiguous. (`git merge-base` returns a commit SHA, not a branch name — do not use it here.)

## 3. Present the menu

Present exactly these four options, verbatim, with no added commentary:

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work

Which option?
```

On a detached HEAD, drop option 1 (merge is not possible) and present the remaining three, renumbered.

## 4. Execute

**Option 1 — merge locally.** Work from the main repo root, never from inside a worktree:

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git checkout <base-branch> && git pull && git merge <feature-branch>
```

Re-run the verify suite **on the merged result, before removing any worktree**. Only after it passes: clean up the worktree (step 5), then `git branch -d <feature-branch>`.

**Option 2 — push + PR.** `git push -u origin <feature-branch>`, then create the PR. **Keep the worktree** — the user needs it to iterate on review feedback.

**Option 3 — keep.** Report the branch name and worktree path. Touch nothing.

**Option 4 — discard.** List exactly what will be permanently deleted (branch, commits, worktree path) and require the user to literally type `discard`. Anything else — including "yes", "confirm", "do it" — is not confirmation. On confirmation: from the main repo root, clean up the worktree (step 5), then `git branch -D <feature-branch>`.

## 5. Worktree cleanup (options 1 and 4 only)

- Only remove a worktree whose path sits under `.worktrees/` or `worktrees/` — that provenance means this skill set created it. Anything else (including harness-owned workspaces) is not yours to remove; leave it, or use the platform's own workspace-exit mechanism.
- Never run the removal from inside the worktree being removed — `cd` to the main repo root first.
- After removal, `git worktree prune` to clear stale metadata.

## 6. Close the loop

On merge or PR, remind the user (or do it, if the spec's tasks are all complete): REQUIRED SUB-SKILL: use `sync-spec` to update the feature's `Status:` line and trace state.

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
