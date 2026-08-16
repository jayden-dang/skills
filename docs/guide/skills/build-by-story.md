# `build-by-story`

> Drive an approved **story-unit** plan: derive review units from requirement stories, implement with subagents, stop for a human after each unit, resume from the unit ledger, finish with whole-branch review.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invocable |
| **Reads** | `tasks.md` (`Execution-mode: story-unit`), `requirements.md`, `.skills/<CODE>/progress.md` |
| **Writes** | implementation commits; task + unit review packages; ledger task and `Unit <k>: complete` lines |
| **Calls** | [`isolate-workspace`](isolate-workspace.md), implementer/reviewer templates under `build-in-waves/`, [`inspect-change`](inspect-change.md), `polish-diff`, [`validate-feature`](validate-feature.md), [`land-branch`](land-branch.md); mode-change write-handoff to [`build-in-waves`](build-in-waves.md) |
| **Called by** | [`plan-tasks`](plan-tasks.md) (story-unit route), [`build-in-waves`](build-in-waves.md) (mode gate redirect) |

## When it fires

An approved `tasks.md` has **`Execution-mode: story-unit`**. Continuous subagent runs use [`build-in-waves`](build-in-waves.md). Controller-only runs use [`build-inline`](build-inline.md) (no unit barriers there).

## Shape

1. **Derive** review units from live requirement story IDs (never PM "Human review order" lists).
2. For each unit: run the per-task subagent loop (brief → implementer → two-verdict review → ledger).
3. **Unit barrier:** unit agent review → STOP with a required summary contract → wait for human unlock.
4. Unlock: `continue` = next unit only; `stop stopping` / `just run it all` = write `Execution-mode: continuous` into `tasks.md`, then hand remaining work to `build-in-waves`.
5. After the last unit: whole-branch agent review still runs — human unit reviews are not a substitute.

## See also

- [`build-in-waves`](build-in-waves.md) · [`build-inline`](build-inline.md)
- [Phase 3 — Execution](../process/execution.md)
