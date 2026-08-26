---
name: land-branch
version: 3.0.0
description: >
  Use when a finished feature branch needs integration or disposition —
  produces a local merge, pull request, kept branch, discard, or block with
  reviewer-readable commits and pull-request text. Not for reviewing an
  existing PR (inspect-change), cutting a version (cut-release), or allocating
  human attention over a range (select-review-sample).
---

# Finish a Branch

Resolve the requested outcome, prepare the branch, and perform that outcome.

## Invariants

```
REUSE EVIDENCE BOUND TO THE CURRENT REVISION.
FALL BACK TO VERIFICATION WHEN THAT EVIDENCE IS ABSENT OR STALE.
NEVER DELETE WORK WITHOUT LITERAL CONFIRMATION.
```

Agent-authored PR title and body remain reviewer truth. There is no package
approval loop and no `.skills/pr-packages/` tree.

## 1. Resolve intent

Walk this ladder and stop at the first rung that resolves:

1. explicit intent in the user's request: `pr`, `merge`, `keep`, `discard`, or
   `block` (ordinary equivalents such as “open the PR” count);
2. an existing PR for the head branch → `pr`;
3. `Default landing action:` in `docs/agents/project.md`, when its value is one
   of `pr`, `merge`, or `keep`;
4. ask one short question: “PR, local merge, or keep the branch?”

Never infer `discard` or `block`. An explicit action is already the user's
choice; do not show a second menu.

**Done when:** exactly one action is resolved.

## 2. Prepare locally

REQUIRED: load `prepare.md` and follow it through **Author commits**. Resolve
and memoize the base there. Author PR text only for `pr`.

If authoring a residue commit changes HEAD, any earlier close receipt is stale;
step 3 handles the fallback. Never rewrite a pre-existing commit.

**Done when:** base, conventions, context, tickets, and created commits are
resolved, with no unhandled in-scope tracked residue.

## 3. Establish crossing evidence

This step applies only to `pr` and `merge`. `keep`, `discard`, and `block` do
not claim the branch is verified.

REQUIRED: load `../../execution/execute-common/close-receipt.md` and run its
fixed validation recipe against `.skills/<CODE>/close-receipt.md`.

- **Valid receipt:** consume it. Do not rerun equivalent verification,
  traceability, review, or acceptance checks.
- **Missing or stale receipt:** REQUIRED SUB-SKILL: use `prove-claim` to run
  every verify command and `audit-trace` fresh. If user-facing behavior has not
  been driven on the current revision, REQUIRED SUB-SKILL: use
  `validate-feature`. A failure withholds only `pr` and `merge`; report the
  failing evidence and leave `keep`, `discard`, and `block` available.

The sample line is advisory. When the receipt says `Sample: required`, name
`/select-review-sample` once without invoking it and continue the crossing.
If this session holds paste-ready banked blocks, reprint them and name
`/record-debt`; they never withhold the crossing.

**Done when:** `pr`/`merge` has a valid current-revision receipt or fresh green
fallback evidence, or the crossing is honestly withheld.

## 4. Detect the environment

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" && pwd -P)
```

| State | Meaning |
|---|---|
| equal | normal checkout — no worktree cleanup |
| differ, named branch | linked worktree — provenance-checked cleanup applies |
| differ, detached HEAD | externally managed workspace — no local merge or cleanup |

Use the base memoized by `prepare.md`; never re-select it from topology.

## 5. Record only configured boundaries

Read `docs/agents/project.md` `## Decision boundaries` when present. A record is
required only when a non-placeholder row matches `land-branch:<action>` or
`land-branch:*`. No section or no matching row means no record.

For a matching row, before the side effect REQUIRED SUB-SKILL: use
`record-verdict` with the resolved verdict, boundary type, tier/predicate facts,
and durable evidence inline. A publication failure withholds that configured
crossing. Never emit a record for `keep`.

**Done when:** no record is configured, or the required record published.

## 6. Execute the resolved action

### PR

Load `prepare.md` **Author PR text** (REQUIRED SUB-SKILL: use `speak-outer`).
Push the feature branch, then create or update the PR for the memoized base.
Submit title/body bytes from process-temp files; never interpolate authored text
as executable shell input. Keep the worktree for review iteration.

### Local merge

Only explicit intent reaches this action. From the main repo root:

```bash
git checkout "<base>" && git pull && git merge "<feature-branch>"
```

The merged result is a new revision. Run the full verify suite on it before any
cleanup. On failure, keep the worktree and branch and report the failure. On
success, apply step 7 and delete the feature branch with `git branch -d`.

### Keep

Report branch name and worktree path. Change nothing.

### Discard

List the branch, commits, and worktree path that will be permanently deleted.
Require the user to type the literal word `discard`; “yes” and “confirm” do not
count. After confirmation, apply step 7 and delete with `git branch -D`.

### Block

Report the terminal block and leave the branch in place.

**Done when:** the resolved action completed or was withheld with its concrete
failure.

## 7. Worktree cleanup

Applies only after a green local merge or confirmed discard.

- Remove only a worktree below `.isolate-workspace/` or `isolate-workspace/`.
- Never remove a harness-owned or externally managed workspace.
- `cd` to the main repo root before removal, then run `git worktree prune`.

## 8. Close the loop

On PR or merge, inspect feature `Status:`:

| Status | Action |
|---|---|
| `Draft` | report missing approval; do not transition |
| `Approved` + every task checked + clean trace + crossing evidence | REQUIRED SUB-SKILL: use `realign-spec` |
| `Approved` + partial evidence | report the missing evidence |
| `Implemented` / `Shipped`, no drift | skip |
| `Implemented` / `Shipped`, drift | REQUIRED SUB-SKILL: use `realign-spec` |

For PR, merge, or keep: name `/study-change` when multi-task or risk paths are
present; name `/brief-team` when those conditions or architecture impact are
present. These are optional and never withhold the resolved action.

## Red Flags

- Rerunning checks already proven by a valid current-revision receipt
- Trusting a receipt whose base, HEAD, clean-tree state, or required slot fails
- Showing a choice menu after the user already gave explicit intent
- Withholding PR/merge for a sample, study packet, team brief, or debt record
- Publishing a decision record when no matching project boundary config exists
- Inferring local merge, discard, or block from “land this”
- Removing a worktree before the merged result passes verification
- Accepting anything except literal `discard` for destructive confirmation
- Rewriting, squashing, rebasing, or force-pushing pre-existing commits
- Writing `.skills/pr-packages/` or adding a PR-text approval loop

| Thought | Reality |
|---|---|
| “Fresh means rerun even though exact HEAD is unchanged” | The receipt binds the proof to that revision; validate the binding instead of replaying the work. |
| “Auth path means sampling must block” | Sampling allocates human attention; it is advisory after review and acceptance. |
| “Open the PR is only a menu preference” | It is explicit intent. Execute it after evidence resolves. |
| “Every crossing deserves a custom record” | Platform history is the default; custom records are opt-in project policy. |
| “Simpler means trust any receipt” | Simpler removes duplicate work, not revision checks. Stale or incomplete evidence takes the fallback. |
