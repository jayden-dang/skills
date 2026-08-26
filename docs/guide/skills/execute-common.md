# `execute-common`

> Shared controller recipe for the execute family. Not an entry point — `build-in-waves`, `build-by-story`, and `build-inline` load it.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invocable (loaded by the execute family; do not start here) |
| **Reads** | `docs/agents/issue-tracker.md` when present; `.skills/<CODE>/progress.md` |
| **Writes** | Close-branch notes and `.skills/<CODE>/close-receipt.md` |
| **Calls** | [`inspect-change`](inspect-change.md), [`polish-diff`](polish-diff.md), [`validate-feature`](validate-feature.md), [`review-product-flow`](review-product-flow.md), [`land-branch`](land-branch.md) |
| **Called by** | [`build-in-waves`](build-in-waves.md), [`build-by-story`](build-by-story.md), [`build-inline`](build-inline.md) |

## What it is

One home for session preflight, ledger check, the Close branch todo, and the
close sequence. After the final mutation it writes a receipt binding review,
verification, trace, acceptance, product-walk, and advisory sample state to the
exact base and HEAD. `land-branch` consumes that receipt instead of replaying
equivalent checks.

It is a registered Engineer Pack skill so `npx skills add` copies the folder beside those three. After install the load path is `../execute-common/SKILL.md`.

## See also

- [Verification layers](../concepts/verification-layers.md) — map of methods; this skill does not load that file
- [`build-in-waves`](build-in-waves.md) · [`build-by-story`](build-by-story.md) · [`build-inline`](build-inline.md)
- [Phase 3 — Execution](../process/execution.md)
