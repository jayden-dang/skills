# `execute-common`

> Shared controller recipe for the execute family. Not an entry point — `build-in-waves`, `build-by-story`, and `build-inline` load it.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invocable (loaded by the execute family; do not start here) |
| **Reads** | `docs/agents/issue-tracker.md` when present; `.skills/<CODE>/progress.md` |
| **Writes** | Close-branch notes (`skip: no polish predicate` when the predicate is false) |
| **Calls** | [`inspect-change`](inspect-change.md), [`polish-diff`](polish-diff.md), [`validate-feature`](validate-feature.md), [`review-product-flow`](review-product-flow.md), [`package-change`](package-change.md), [`land-branch`](land-branch.md) |
| **Called by** | [`build-in-waves`](build-in-waves.md), [`build-by-story`](build-by-story.md), [`build-inline`](build-inline.md) |

## What it is

One home for session preflight, ledger check, the Close branch todo, the close sequence, and the polish / product-walk predicates. The three execute-family skills keep only their mode iron law and per-task / per-unit loop.

It is a registered Engineer Pack skill so `npx skills add` copies the folder beside those three. After install the load path is `../execute-common/SKILL.md`.

## See also

- [`build-in-waves`](build-in-waves.md) · [`build-by-story`](build-by-story.md) · [`build-inline`](build-inline.md)
- [Phase 3 — Execution](../process/execution.md)
