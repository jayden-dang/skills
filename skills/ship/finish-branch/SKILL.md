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

### 4a. Ticket and content checkpoint (options 1 and 2 only)

Before `record-decision` runs, on options **1 (merge)** and **2 (PR)**: display
the resolved ticket set (the `[{ id, title, classification, linkage_syntax }]`
list `prepare-change`'s ticket resolution produced) and ask whether any
missing ticket should be created or supplemented. Ask this question even with
no tracker configured — an absent tracker does not skip it, the checkpoint
still asks the same missing-ticket question either way. If the user asks for
a ticket to be created, pause the crossing here and ask the user to run
`/file-issues` themselves: name it, never invoke it — `/file-issues` is
user-invoked and `finish-branch` is model-invoked (ARCH-5).

On option **2 (PR)** only, also display the exact package content read from
`.skills/pr-packages/<stable-id>/manifest.md` and `body.md` — title, base,
head, body, ticket linkage, commits, advisory commit map, convention
findings, validation results — and offer exactly three responses:
**approve**, **request edits**, or **cancel**. On request edits: re-author
the affected content, revalidate it, redisplay the full package, and require
a fresh approval — an edit never carries forward a prior approval; the loop
repeats until an explicit approve or a cancel. Carry the approved
`Content-digest:` forward as **inline** decision evidence for
`record-decision` below; never cite the `.skills/pr-packages/<stable-id>/`
path as its locator.

This checkpoint runs, and (on option 2) reaches approval, **before**
`record-decision` publishes and **before** the crossing itself — the order
is menu selection → this checkpoint → `record-decision` → the git/gh side
effect, never transposed.

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

**Option 2 — push + PR.** After a successful record: `git push -u origin
<feature-branch>`, then, **immediately before submission**, re-resolve the
base and head SHAs and recompute `Content-digest:` using
`package-contract.md`'s exact recipe, unparaphrased — the readability guard
runs first and aborts before the pipe:

```bash
test -r ".skills/pr-packages/<stable-id>/body.md" || {
  echo "Error: body.md missing or unreadable at .skills/pr-packages/<stable-id>/body.md" >&2
  exit 1
}
{ printf '%s\n' "<title>"; cat ".skills/pr-packages/<stable-id>/body.md"; } | git hash-object --stdin
```

If either resolved SHA or the recomputed digest differs from the approved
values, that mismatch invalidates the approval: do not submit — return to
the 4a checkpoint to re-author, revalidate, redisplay, and reapprove before
trying again. Because `record-decision` already published against the
now-invalidated digest, this reapproval requires a fresh `record-decision`
publish — carrying the reapproved values — before submission is retried, so
the published record always describes what actually crosses. Once both
SHAs and the digest still match, submit the approved title, base, head, and
body **without re-authoring** them:

```bash
gh pr create --base <base> --body-file .skills/pr-packages/<stable-id>/body.md
```

— using the package's own `Base:` rather than recomputing one. **Keep the
worktree** — the user needs it to iterate on review feedback. **Team
packaging:** when `docs/agents/project.md` has `## Team` with a non-empty
**roster** or band override, read **band**/**packaging** from that section —
Solo: no invented reviewer list in PR body language; Small/Multi: suggest
reviewers from roster/ownership notes in PR prose. No new menu item. Missing
Team → pre-feature default.

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

### 6a. Spec status

On merge or PR, remind the user (or run it when tasks are complete): REQUIRED
SUB-SKILL: use `sync-spec` to update the feature's `Status:` and trace state.

### 6b. Name optional human skills (risk = diff path)

**Leading word: risk glob** — match **actual diff paths** (not plan labels, not
task count) against the default B1 set in
`skills/review/allocate-attention/references/signals.md`, **extended** (never
replaced) by `Risk globs` in `docs/agents/project.md` when present.

**Recipe — run every close-loop (Merge, PR, Keep):**

1. Count tasks in the plan (or commits if no plan): `multi_task = (count > 1)`.
2. List paths in the branch diff vs base. `risk_hit = any path matches a risk glob`.
3. Note `architecture_affecting` when the change rewrites public contracts /
   persistence / auth boundaries (or the user/plan already said so).
4. **IF** `multi_task OR risk_hit` → **name** `/comprehend-change` (user-invoked —
   never auto-run, never soft-gate the menu).
5. **IF** `multi_task OR risk_hit OR architecture_affecting` → **name**
   `/explain-change` (user-invoked — never auto-run, never withhold merge/PR).
6. **IF** `.skills/implementation-notes.md` has deviations → mention that path once.

**Worked case:** one task, diff only `skills/auth/session.ts` → `risk_hit` true →
name **both**. **Keep** still runs steps 4–5 (names only; no merge/PR).

**Optional means the human may skip running the skill — you still name it.**

**Done when:** steps 1–6 executed; names appear in the close-out when predicates hold.

## Red flags

Never:

- Offer merge or PR while any verify command fails
- Remove a worktree before the merged result has passed tests
- Accept anything but the typed word `discard` for discard confirmation
- Remove a worktree outside `.worktrees/`/`worktrees/`, or from inside itself
- Force-push on your own initiative — it happens only on an explicit request from the user, never as your idea of a fix
- Execute merge/PR/discard before `record-decision` publishes successfully
- Emit a decision record for keep, pause/defer, or mechanical failure alone
- Omit `/comprehend-change` or `/explain-change` names because the branch is single-task, one-file, Keep-only, or a lead said "skip theater," while the diff still hits a risk glob
- Skip the missing-ticket question on option 1 or 2 because no tracker is configured
- Run `/file-issues` yourself instead of naming it and pausing for the user
- Submit a PR whose title or body was re-authored after approval instead of looping back through the 4a checkpoint
- Skip the immediately-before-submission SHA/digest recheck, or submit after it reveals a mismatch
- Retry submission on a stale record after a mismatch instead of publishing a fresh `record-decision` first
- Cite the `.skills/pr-packages/<stable-id>/` path as decision evidence instead of the inline digest

| Thought | Reality |
|---|---|
| "Tests were green an hour ago, skip the gate" | Stale evidence. Anything merged on old green is unverified. |
| "The user obviously wants a PR, skip the menu" | The decision is theirs. Five options when green; block/discard still available on red. |
| "Cleanup first, then merge — tidier" | A failed merge with the worktree gone loses the work. Merge, verify, then clean. |
| "Skip the record; merge is the real work" | Record-before-crossing: no merge/PR/discard without a published record. |
| "Senior said skip paperwork — just merge" | Authority is not a gate exemption; publish the record or withhold the crossing. |
| "Merge now, record tomorrow" | Deferred record is still an unrecorded crossing — same red flag. |
| "Single-task / one-file — skip optional skill names" | Risk is the **diff path**, not task count. Auth (or any risk glob) still names both |
| "Lead said skip the theater" | Authority is not a gate exemption. Name them; the human can ignore |
| "No tracker configured, so skip the ticket question" | The question is asked either way; an absent tracker is a normal state, not a skip |
| "The user clearly wants the ticket filed, just run /file-issues" | `/file-issues` is user-invoked; name it and pause, never invoke it (ARCH-5) |
| "One small edit to the body doesn't need a fresh approval" | Any edit re-authors content; the loop redisplays and requires approval again |
| "Digest matched at authoring time, no need to recheck at submit" | Re-resolve SHAs and recompute the digest immediately before submission every time |
| "Citing the .skills/ path is fine, it's where the evidence lives" | Storage location isn't a citable locator; carry the digest inline instead |
| "Risk prompts are only for multi-task plans" | False. Multi-task **or** risk glob **or** architecture-affecting |
| "Keep means no review prompts" | Keep still names optional self-check / explainer; it only skips merge/PR |
