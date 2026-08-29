# `land-branch`

> Prepare completed work locally, then decide the crossing: merge, PR, keep,
> discard, or block. Agent-authored PR title and body are the reviewer truth.

|  |  |
|---|---|
| **Bucket** | ship |
| **Invocation** | model-invocable |
| **Reads** | `docs/agents/project.md`, `docs/agents/issue-tracker.md`, `.skills/<CODE>/close-receipt.md`, the base…head diff, worktree state |
| **Writes** | commits it creates itself; local merges; pushed branches and PRs; deleted branches; isolate-workspace cleanup |
| **Calls** | [`prove-claim`](prove-claim.md), [`validate-feature`](validate-feature.md) (when user-facing behavior is undriven), [`speak-outer`](speak-outer.md) (PR title and body), [`record-verdict`](record-verdict.md), [`realign-spec`](realign-spec.md) |
| **Called by** | [`execute-common`](execute-common.md) (close sequence) |

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

## Intent

Explicit PR, merge, keep, discard, or block intent executes without a second
menu. Ambiguous intent resolves through existing PR, project default, then one
short question. Local merge, discard, and block are never inferred.

## After merge or PR — spec status

Read `Status:`. Still `Approved` or `In-progress` with every task checked and verify green →
run [`realign-spec`](realign-spec.md) (forgot-net). Already `Implemented`
and no drift → skip. This is not `/cut-release`.

## Executing a PR

Push, then create or update the PR from session title/body files. A custom
decision record is required only when `project.md` configures that boundary.
The worktree is kept for review iteration.

## See also

- [Verification layers](../concepts/verification-layers.md) — receipt-bound evidence layers
- [`prove-claim`](prove-claim.md) — stale/missing receipt fallback
- [`record-verdict`](record-verdict.md) — configured decision boundaries
- [`cut-release`](cut-release.md) — version cut, not a branch merge
- [Retired `package-change`](package-change.md)
