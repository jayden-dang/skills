# `execute-common`

> Shared controller recipe for the execute family. Not an entry point — `build-in-waves`, `build-by-story`, and `build-inline` load it.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invocable (loaded by the execute family; do not start here) |
| **Reads** | `docs/agents/issue-tracker.md` when present; `.skills/<CODE>/progress.md` |
| **Writes** | `Approved` → `In-progress` on `requirements.md` + INDEX (before worktrees); Close-branch notes and `.skills/<CODE>/close-receipt.md` |
| **Calls** | [`inspect-change`](inspect-change.md), [`polish-diff`](polish-diff.md), [`validate-feature`](validate-feature.md), [`write-dogfood`](write-dogfood.md), [`land-branch`](land-branch.md) |
| **Called by** | [`build-in-waves`](build-in-waves.md), [`build-by-story`](build-by-story.md), [`build-inline`](build-inline.md) |

## What it is

One home for session preflight (tracker, In-progress stamp, workspace), ledger check, the Close branch todo, and the
close sequence. After the final mutation it writes a receipt binding review,
verification, trace, acceptance, product-walk, and advisory sample state to the
exact base and HEAD. `land-branch` consumes that receipt instead of replaying
equivalent checks.

At preflight it claims the ticket: it sets the assignee and swaps the state role to `building`. When the ticket is already resolved from your request or the plan, tracker sync no longer asks; it records the ticket set in `.skills/<CODE>/tickets.md`, which [`land-branch`](land-branch.md) reads to link `Closes #N` and move the ticket to `in-review`. The close receipt has a `Cost:` slot (Receipt-Version 2), and a branch that touches only a library gets no product walk. See [the workflow](../workflow.md).

It is a registered Engineer Pack skill so `npx skills add` copies the folder beside those three. After install the load path is `../execute-common/SKILL.md`.

## See also

- [Verification layers](../concepts/verification-layers.md) — map of methods; this skill does not load that file
- [`build-in-waves`](build-in-waves.md) · [`build-by-story`](build-by-story.md) · [`build-inline`](build-inline.md)
- [Phase 3 — Execution](../process/execution.md)
