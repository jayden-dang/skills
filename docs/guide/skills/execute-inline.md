# `execute-inline`

> Drive an approved plan **yourself**: sequential tasks, `tdd` every step, progress ledger, stop-on-blocker, whole-branch review — no implementer subagents.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invocable |
| **Reads** | `tasks.md`, `.skills/progress.md`, `docs/agents/project.md` |
| **Writes** | implementation commits; optional task reports; ledger lines with `inline, review self` |
| **Calls** | [`tdd`](tdd.md), [`worktrees`](worktrees.md), [`code-review`](code-review.md), `polish`, [`acceptance-check`](acceptance-check.md), [`prepare-change`](prepare-change.md), [`finish-branch`](finish-branch.md) |
| **Called by** | [`write-plan`](write-plan.md) (inline route), [`execute-plan`](execute-plan.md) (inline handoff) |

## When it fires

The user chose the inline route, the environment cannot (or must not) fan out implementers, or write-plan offered inline and they accepted. **Tool availability does not override the route.**

## Shape

- **Iron laws:** you are the implementer; no production code without `tdd`; never guess through a blocker.
- Build a brief for yourself, implement under `tdd`, commit with requirement trailers, self-check, ledger, next task.
- **No unit barriers** even if `Execution-mode: story-unit` — those belong to [`execute-story`](execute-story.md).
- **No parallel waves.** Serial only.
- End with whole-branch `code-review` (not a per-task reviewer subagent).

## See also

- [`execute-plan`](execute-plan.md) · [`execute-story`](execute-story.md)
- [Phase 3 — Execution](../process/execution.md)
