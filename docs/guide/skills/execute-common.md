# `execute-common`

> Shared controller recipe for the execute family. Not an entry point — `build-in-waves`, `build-by-story`, and `build-inline` load it.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invocable (loaded by the execute family; do not start here) |
| **Reads** | `docs/agents/issue-tracker.md` when present; `.skills/<CODE>/progress.md` |
| **Writes** | Close-branch notes (`skip: no polish predicate` / `skip: no sample predicate` / `sample: required`) |
| **Calls** | [`inspect-change`](inspect-change.md), [`polish-diff`](polish-diff.md), [`validate-feature`](validate-feature.md), [`review-product-flow`](review-product-flow.md), [`land-branch`](land-branch.md) |
| **Called by** | [`build-in-waves`](build-in-waves.md), [`build-by-story`](build-by-story.md), [`build-inline`](build-inline.md) |

## What it is

One home for session preflight, ledger check, the Close branch todo, the close sequence, and the polish / sample / product-walk predicates. After acceptance, the sample predicate writes `sample: required` or `skip: no sample predicate`. It does not name `/select-review-sample` — `land-branch` is the one human station. The three execute-family skills keep only their mode iron law and per-task / per-unit loop.

It is a registered Engineer Pack skill so `npx skills add` copies the folder beside those three. After install the load path is `../execute-common/SKILL.md`.

## See also

- [Verification layers](../concepts/verification-layers.md) — map of methods; this skill does not load that file
- [`build-in-waves`](build-in-waves.md) · [`build-by-story`](build-by-story.md) · [`build-inline`](build-inline.md)
- [Phase 3 — Execution](../process/execution.md)
