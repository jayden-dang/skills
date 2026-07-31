# `build-inline`

> Drive an approved plan **yourself**: sequential tasks, `test-first` every step, progress ledger, stop-on-blocker, whole-branch review — no implementer subagents.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invocable |
| **Reads** | `tasks.md`, `.skills/progress.md`, `docs/agents/project.md` |
| **Writes** | implementation commits; optional task reports; ledger lines with `inline, review self` |
| **Calls** | [`test-first`](test-first.md), [`isolate-workspace`](isolate-workspace.md), [`inspect-change`](inspect-change.md), `polish-diff`, [`validate-feature`](validate-feature.md), [`package-change`](package-change.md), [`land-branch`](land-branch.md) |
| **Called by** | [`plan-tasks`](plan-tasks.md) (inline route), [`build-continuous`](build-continuous.md) (inline write-handoff) |

## When it fires

The user chose the inline route, the environment cannot (or must not) fan out implementers, or plan-tasks offered inline and they accepted. **Tool availability does not override the route.**

## Shape

- **Iron laws:** you are the implementer; no production code without `test-first`; never guess through a blocker.
- Build a brief for yourself, implement under `test-first`, commit with requirement trailers, self-check, ledger, next task.
- **No unit barriers** even if `Execution-mode: story-unit` — those belong to [`build-story-units`](build-story-units.md).
- **No parallel waves.** Serial only.
- End with whole-branch `inspect-change` (not a per-task reviewer subagent).

## See also

- [`build-continuous`](build-continuous.md) · [`build-story-units`](build-story-units.md)
- [Phase 3 — Execution](../process/execution.md)
