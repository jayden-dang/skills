---
name: finish-branch
description: Use when a feature branch is complete and committed and an integration
  decision is needed — merge, PR, keep, discard, or block at this boundary
  (publishes a decision record before crossings).
---

# Finish a Branch

Decide what happens to completed work: gate on verify, detect the environment,
offer a fixed menu, execute the choice, clean up safely. Terminal crossings use
**record-before-crossing** via `record-decision`.

## 1. Gate: verify, trace, and acceptance

REQUIRED SUB-SKILL: use `verify` to run every verify command from `docs/agents/project.md` (typecheck, lint, unit, e2e) fresh AND to confirm the `trace` check is clean — a branch must not merge with untraced requirements, the same gate `release` enforces. If no test command is discoverable, ask the user for it and suggest `setup-repo`.

If the branch has user-facing behavior that has not been driven through the running system, REQUIRED SUB-SKILL: use `acceptance-check` before offering Merge or PR — green units prove assertions pass, not that the feature works.

**On failure:** show the failures. While any verify, trace, or required acceptance
check fails: withhold **merge** and **PR**; still offer terminal **block** and
**discard** (emit a decision record against red evidence). Mechanical failure alone,
or pause/defer, without an explicit terminal block/discard → no decision record.

**Done when:** green path can offer the full menu, or red path has offered only
block/discard (or the user paused).

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

Present exactly these five options, verbatim, with no added commentary (when the gate is green):

```
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is (I'll handle it later)
4. Discard this work
5. Block: reject this work at this boundary (records a terminal block verdict)

Which option?
```

When the gate is red, present only options 4 and 5 (discard / block), renumbered, and state that merge and PR are withheld until checks pass.

On a detached HEAD with a green gate, drop option 1 (merge is not possible) and present the remaining four, renumbered. On detached HEAD with a red gate, still only discard/block.

**Done when:** the user has picked one menu option.

## 4. Execute

For options **1 (merge), 2 (PR), 4 (discard), and 5 (block)** — **before** any git/gh side effect — REQUIRED SUB-SKILL: use `record-decision` with:

| Option | Verdict | Boundary-Type |
|---|---|---|
| 1 merge | `merge` | `integration` |
| 2 PR | `pr` | `publication` |
| 4 discard | `discard` | `disposal` |
| 5 block | `block` | type of the crossing blocked (`integration` if merge was intended, else the blocked path) |

Hand off tier/predicate facts and durable evidence **inline as text**. Crossing executes only after `record-decision` publishes a validator-clean record. On publication failure: do **not** execute the crossing; report that the verdict was not enacted. For block, there is no crossing side effect, but a failed record is still an incomplete accountability workflow — never claim a recorded block.

**Option 1 — merge locally.** After a successful record: work from the main repo root, never from inside a worktree:

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git checkout <base-branch> && git pull && git merge <feature-branch>
```

Re-run the verify suite **on the merged result, before removing any worktree**. Only after it passes: clean up the worktree (step 5), then `git branch -d <feature-branch>`.

**Option 2 — push + PR.** After a successful record: `git push -u origin <feature-branch>`, then create the PR. **Keep the worktree** — the user needs it to iterate on review feedback. **Team packaging:** when `docs/agents/project.md` has `## Team` with a non-empty **roster** or band override, read **band**/**packaging** from that section — Solo: no invented reviewer list in PR body language; Small/Multi: suggest reviewers from roster/ownership notes in PR prose. No new menu item. Missing Team → pre-feature default.

**Option 3 — keep.** Report the branch name and worktree path. Touch nothing. **Do not** invoke `record-decision`.

**Option 4 — discard.** After a successful record: list exactly what will be permanently deleted (branch, commits, worktree path) and require the user to literally type `discard`. Anything else — including "yes", "confirm", "do it" — is not confirmation. On confirmation: from the main repo root, clean up the worktree (step 5), then `git branch -D <feature-branch>`.

**Option 5 — block.** After a successful record: report the terminal block; do not merge, PR, or discard. Leave the branch in place unless the user separately asks otherwise.

**Done when:** the chosen option has been executed (or withheld with an honest
publication-failure report), including any required `record-decision` publish.

## 5. Worktree cleanup (options 1 and 4 only)

- Only remove a worktree whose path sits under `.worktrees/` or `worktrees/` — that provenance means this skill set created it. Anything else (including harness-owned workspaces) is not yours to remove; leave it, or use the platform's own workspace-exit mechanism.
- Never run the removal from inside the worktree being removed — `cd` to the main repo root first.
- After removal, `git worktree prune` to clear stale metadata.

## 6. Close the loop

On merge or PR, remind the user (or do it, if the spec's tasks are all complete): REQUIRED SUB-SKILL: use `sync-spec` to update the feature's `Status:` line and trace state.

## Red flags

Never:

- Offer merge or PR while any verify command fails
- Remove a worktree before the merged result has passed tests
- Accept anything but the typed word `discard` for discard confirmation
- Remove a worktree outside `.worktrees/`/`worktrees/`, or from inside itself
- Force-push, ever, unless the user explicitly asked
- Execute merge/PR/discard before `record-decision` publishes successfully
- Emit a decision record for keep, pause/defer, or mechanical failure alone

| Thought | Reality |
|---|---|
| "Tests were green an hour ago, skip the gate" | Stale evidence. Anything merged on old green is unverified. |
| "The user obviously wants a PR, skip the menu" | The decision is theirs. Five options when green; block/discard still available on red. |
| "Cleanup first, then merge — tidier" | A failed merge with the worktree gone loses the work. Merge, verify, then clean. |
| "Skip the record; merge is the real work" | Record-before-crossing: no merge/PR/discard without a published record. |
