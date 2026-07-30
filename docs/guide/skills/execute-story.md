# `execute-story`

> Drive an approved **story-unit** plan: derive review units from requirement stories, implement with subagents, stop for a human after each unit, resume from the unit ledger, finish with whole-branch review.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invocable |
| **Reads** | `tasks.md` (`Execution-mode: story-unit`), `requirements.md`, `.skills/progress.md` |
| **Writes** | implementation commits; task + unit review packages; ledger task and `Unit <k>: complete` lines |
| **Calls** | [`worktrees`](worktrees.md), implementer/reviewer templates under `execute-plan/`, [`code-review`](code-review.md), `polish`, [`acceptance-check`](acceptance-check.md), [`prepare-change`](prepare-change.md), [`finish-branch`](finish-branch.md); mode-change handoff to [`execute-plan`](execute-plan.md) |
| **Called by** | [`write-plan`](write-plan.md) (story-unit route), [`execute-plan`](execute-plan.md) (mode gate redirect) |

## When it fires

An approved `tasks.md` has **`Execution-mode: story-unit`**. Continuous subagent runs use [`execute-plan`](execute-plan.md). Controller-only runs use [`execute-inline`](execute-inline.md) (no unit barriers there).

## Shape

1. **Derive** review units from live requirement story IDs (never PM "Human review order" lists).
2. For each unit: run the per-task subagent loop (brief → implementer → two-verdict review → ledger).
3. **Unit barrier:** unit agent review → STOP with a required summary contract → wait for human unlock.
4. Unlock: `continue` = next unit only; `stop stopping` / `just run it all` = write `Execution-mode: continuous` into `tasks.md`, then hand remaining work to `execute-plan`.
5. After the last unit: whole-branch agent review still runs — human unit reviews are not a substitute.

## See also

- [`execute-plan`](execute-plan.md) · [`execute-inline`](execute-inline.md)
- [Phase 3 — Execution](../process/execution.md)
