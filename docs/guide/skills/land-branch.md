# `land-branch`

> Prepare completed work locally, then decide the crossing: merge, PR, keep,
> discard, or block. Agent-authored PR title and body are the reviewer truth.

|  |  |
|---|---|
| **Bucket** | ship |
| **Invocation** | model-invocable |
| **Reads** | `docs/agents/project.md`, `docs/agents/issue-tracker.md`, the base…head diff, worktree state |
| **Writes** | commits it creates itself; local merges; pushed branches and PRs; deleted branches; isolate-workspace cleanup |
| **Calls** | [`prove-claim`](prove-claim.md), [`validate-feature`](validate-feature.md) (when user-facing behavior is undriven), [`record-verdict`](record-verdict.md), [`realign-spec`](realign-spec.md) |
| **Called by** | [`execute-common`](execute-common.md) (close sequence) |

`package-change` is retired. This skill authors remaining commits and the PR
description itself. There is no `.skills/pr-packages/` tree and no
approve / request-edits / cancel loop.

## When it fires

When a feature branch is complete and an integration decision is needed — or
when finished work still needs reviewer-readable commits and a pull-request
description.

## The gate comes first

[`prove-claim`](prove-claim.md) runs every verify command from
`docs/agents/project.md` **fresh**, and confirms [`audit-trace`](audit-trace.md)
is clean. User-facing behavior that has not been driven through the running
system also runs [`validate-feature`](validate-feature.md) before Merge or PR
is offered.

This skill is the **one human station** after close: sample withhold,
optional `/record-debt` for this session's banked blocks, and the menu —
all in the same message. `/study-change` and `/brief-team` are still
named later when their predicates hold; they never withhold merge/PR.

After verify is green, a **sample withhold** also applies: if the diff hits
a B1 risk path, is more than 15 files, or the user asked for a sample, and
this session has no attention allocation and the user has not typed
`unsampled`, merge and PR stay withheld. Name [`/select-review-sample`](select-review-sample.md)
for the user — do not start it. That skill stays an aid; this skill is the
gate.

**Any failure (verify, acceptance, or sample withhold) = withhold merge and PR.**
Still offer discard / block.

## Prepare locally

Base is resolved from an explicit value, an existing PR, or `Default PR base:`
— never from `origin/HEAD` / `main` / topology. Residue commits are grouped
and created; pre-existing history is never rewritten. The PR title and body
are authored from the live diff. That text **is** the reviewer truth.

## The menu

Five options when the gate is green (merge / PR / keep / discard / block),
worded exactly as the skill lists them. Banked leftovers reprint in that
same message. A request to "just open a PR" is option 2 after the menu is
shown — not a skip of the gate or the menu.

## Executing a PR

After `record-verdict` publishes: push, then `gh pr create` from the
session title and body written to process-temp files (not
`.skills/pr-packages/`). The worktree is kept for review iteration.

## See also

- [Verification layers](../concepts/verification-layers.md) — human withhold vs computational gate
- [`prove-claim`](prove-claim.md) — the gate
- [`record-verdict`](record-verdict.md) — record-before-crossing
- [`cut-release`](cut-release.md) — version cut, not a branch merge
- [Retired `package-change`](package-change.md)
