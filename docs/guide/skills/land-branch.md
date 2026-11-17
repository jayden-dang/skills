# `land-branch`

> Prepare completed work locally, then decide the crossing: merge, PR, keep,
> discard, or block. Agent-authored PR title and body are the reviewer truth.

|  |  |
|---|---|
| **Bucket** | ship |
| **Invocation** | model-invocable |
| **Reads** | `docs/agents/project.md`, `docs/agents/issue-tracker.md`, `.skills/<CODE>/close-receipt.md`, the base…head diff, worktree state |
| **Writes** | commits it creates itself; local merges; pushed branches and PRs; deleted branches; isolate-workspace cleanup |
| **Calls** | [`prove-claim`](prove-claim.md), [`validate-feature`](validate-feature.md) (when user-facing behavior is undriven), [`speak-outer`](speak-outer.md) (PR title and body), [`record-verdict`](record-verdict.md), [`realign-spec`](realign-spec.md), [`refresh-lanes`](refresh-lanes.md) (after the delivery record and the push) |
| **Called by** | [`build`](build.md) (close sequence) |

`package-change` is retired. This skill authors remaining commits and the PR
description itself. There is no `.skills/pr-packages/` tree and no
approve / request-edits / cancel loop.

## When it fires

When a feature branch is complete and an integration decision is needed — or
when finished work still needs reviewer-readable commits and a pull-request
description.

## Exact-revision evidence

A close receipt binds review, verification, trace, and acceptance to one base
and HEAD. A valid receipt is reused; missing, stale, dirty, or incomplete
evidence falls back to [`prove-claim`](prove-claim.md) and, when needed,
[`validate-feature`](validate-feature.md).

Sampling and banked debt are advisory. They may be named once and never
withhold merge or PR.

## Prepare locally

Base is resolved from an explicit value, an existing PR, or `Default PR base:`
— never from `origin/HEAD` / `main` / topology. Residue commits are grouped
and created; pre-existing history is never rewritten. The PR title and body
are authored from the live diff. That text **is** the reviewer truth.

## Ship guard and owner notice

Before a `pr` or `merge`, two read-only scripts in the skill's own folder check the branch. `ship-guard.sh` lists lockfiles changed without their manifest, generated files, files that are in neither the plan's file map nor a task's `Files` block, and how far the branch is behind its base. Lockfile and generated files are dropped from the branch, and out-of-plan files move to a `<branch>-extra` branch, unless you named them for this PR. Nothing is pushed while any of those rows stand. A behind-base count goes in the PR body as one line.

For a PR, `owner-notice.py` finds changed files that another team owns, using the Owner column in the feature catalog, the shard's `Owner:` line, or the Ownership notes in `project.md`. When it finds any, the PR body gets a "Changes outside this feature's ownership" section and each owner is requested as a reviewer. It never holds the branch. Files with no owner are never reported.

## Intent

Explicit PR, merge, keep, discard, or block intent executes without a second
menu. Ambiguous intent resolves through existing PR, project default, then one
short question. Discard and block are never inferred, and a local merge is inferred only from
`Default landing action: merge`.

## After merge or PR — spec status

Read `Status:`. Still `Approved` or `In-progress`, no `- [ ]` left in `tasks.md`, a clean trace and green verify → land-branch writes `Implemented` in `requirements.md` and the INDEX row itself, together with the delivery record. The execute family ticks each task as it closes (build 3.2.0), so the boxes can be trusted here. An open box or a trace finding → run [`realign-spec`](realign-spec.md) (forgot-net). Already `Implemented` and no drift → skip. This is not `/cut-release`.

## Recording the delivery

On a PR or a merge, land-branch writes `Delivered-by: PR #N` or `Delivered-by: <merge sha>` into the feature's `tasks.md` (inside the `## ROAD-N amendment` group for an amendment) and commits it as `docs(<CODE>): record delivery`. With `Delivery proof: required`, [`refresh-roadmap-status`](refresh-roadmap-status.md) counts an item done only when that line resolves to a commit on the integration ref. Without the step, both clean baseline runs merged and left the item in review.

## The ticket

The ticket set starts from `.skills/<CODE>/tickets.md` and the ticket you named, so the PR body carries `Closes #N` even when the branch name has no ID. When the PR opens, the ticket's state role moves to `in-review`. The merge is yours; `Closes #N` then closes the ticket. See [the workflow](../workflow.md).

## Executing a local merge

The merge is `--no-ff`, and its message carries the closing keyword of every ticket the diff completes. The merged result is verified, the worktree is removed, and the delivery record is committed.

When `Default landing action:` reads `merge`, or the request asks to push, `land-branch` then pushes the base and reads each ticket back. A completed ticket that is still open gets closed with `Landed in <merge sha> on <base>`, which is what covers a base that is not the default branch, where GitHub ignores the keyword. A completed ticket loses its state role either way. A partial ticket moves to `needs-info`, with a comment saying what landed, what is left, and asking whether to continue or close.

A rejected push, or no remote, stops there: the merge stays local, nothing is forced, and no ticket changes. In any other repo a local merge stays local, and the report names the commits ahead of the remote and each ticket still open.

## Executing a PR

Push, then create or update the PR from session title/body files. A custom
decision record is required only when `project.md` configures that boundary.
The worktree is kept for review iteration.

## Tending the PR to merge-ready (4.10.0, 2026-11-17)

The PR-tending skill is now part of this one, as `tend.md`. After a PR opens, `land-branch` tends it
until it is merge-ready or has a named blocker. It works in this order: conflicts, then
review threads, then CI on the head those pushes produced. It classifies each red check as a
stale base, a flake (one fresh build), or a real failure (`root-cause` and `test-first`), and
reads the forge's merge verdict rather than the check list. It never merges. The one
exception is a caller with more branches still to land, such as `/go` with tickets left to
build. There, `land-branch` returns the URL and the caller tends every PR it opened at the end,
so one slow CI does not stall the next ticket. Asking about a PR that is already open ("CI is
red on #41", "babysit my PR") goes straight to `tend.md`.

## See also

- [Verification layers](../concepts/verification-layers.md) — receipt-bound evidence layers
- [`prove-claim`](prove-claim.md) — stale/missing receipt fallback
- [`record-verdict`](record-verdict.md) — configured decision boundaries
- [`cut-release`](cut-release.md) — version cut, not a branch merge
- [Retired `package-change`](package-change.md)
