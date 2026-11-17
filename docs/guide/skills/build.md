# `build`

> One approved plan, executed task by task, in one of three modes.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invoked when an approved `tasks.md` is to be executed; `plan-tasks` and `go` hand off to it |
| **Reads** | the approved `tasks.md` and its `Execution-mode:` line, the design and requirements it cites, `docs/agents/project.md` |
| **Writes** | the feature's commits, `.skills/<CODE>/progress.md` (the ledger), task briefs and review packages, and the close receipt |
| **Calls** | [`isolate-workspace`](isolate-workspace.md), [`test-first`](test-first.md), [`inspect-change`](inspect-change.md), [`polish-diff`](polish-diff.md), [`validate-feature`](validate-feature.md), [`write-dogfood`](write-dogfood.md), [`land-branch`](land-branch.md), [`reroute-plan`](reroute-plan.md) |
| **Called by** | [`plan-tasks`](plan-tasks.md), [`go`](go.md) |

## The three modes

Until 2026-11-15 these were three skills sharing a fourth. They are now one skill whose
`SKILL.md` reads the plan and the environment and opens exactly one mode file.

| Mode | File | When |
|---|---|---|
| wave | `waves.md` | `Execution-mode: continuous`: dependency-aware subagent waves, serial or parallel lanes, no human pause between tasks |
| story | `story.md` | `Execution-mode: story-unit`: human-gated review units derived from the stories |
| inline | `inline.md` | no subagents in this harness, or the operator watches the controller implement |

All three share `common.md`: the session preflight, the ledger check, the todos gate, the
runtime binding and the close sequence that ends in a revision-bound close receipt. In that sequence, when step 4b's product walk will run (inside `go` or with nobody at the keyboard, on a branch with a browser file), step 4 tells `validate-feature` so, and acceptance leaves the page to the walk. If the walk stops before any case gets a verdict, step 4b sends the UI back through `validate-feature` before the receipt.

## What the tests showed

Each mode keeps the evidence it had as its own skill; it is in
`skills/execution/build/TESTS.md`, below the note on the merge. The merge itself was checked by
running one ticket from `/idea` through `/shape` and `/go` before and after.

## See also

- [`plan-tasks`](plan-tasks.md) — writes the plan and offers the three modes
- [`go`](go.md) — builds every ready ticket through this skill
- [The process: execution](../process/execution.md)
