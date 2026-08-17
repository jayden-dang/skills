# On-ramps

**One home** for which skill starts a situation. `gate-session`,
`ask-me-bro`, `solve-problem`, and [START-HERE](../START-HERE.md) point
here — they do not restate this table.

Load this file when the entry point is unclear. Then invoke the named
model-invocable skill, or name the `/slash` for the user to run.

| Situation | Start here |
|---|---|
| Brand-new project, empty directory | `/bootstrap-repo` |
| Existing repo, adopting this skill set | `/configure-repo` |
| Ambiguous problem / requested fix without a clear gap or workflow | `solve-problem` |
| New feature, nothing spec'd yet | `frame-change` |
| Small change to an already-shipped, spec'd feature | `amend-feature` |
| Something is broken (clear unexpected behavior) | `root-cause` |
| Broken on a **deployed** environment (prod / staging / remote dev; traces, OpenObserve, request id) | `debug-remote` (then `root-cause` with the pack) |
| Is our tracing / OpenObserve / sampling complete enough? | `assess-observability` |
| Unit tests green, unsure it truly works | `validate-feature` |
| Want to try a finished feature by hand | `review-product-flow` |
| Have a review-product-flow guide and want the agent to run every case | `run-product-walkthrough` |
| A conversation, spec, or idea to capture as tracker issues | `/publish-issues` |
| Incoming issue or external PR you did not author | `/triage` |
| Codebase feels muddy, want a refactor target | `/scan-architecture` |
| Session ending with work unfinished | `/write-handoff` |
| Cutting a version | `/cut-release` |
| Spec has drifted from the code, or the audit-trace check comes back dirty | `realign-spec` |
| Mid-execution plan is wrong | `reroute-plan` |
| Multi-session destination still foggy | `/pathfind` |
| Unsure which row applies | `/ask-me-bro` |

Three rules of thumb:

> Never spec what you do not understand yet. Unknowns go to `research` or `run-spike` first.

> When even the *workflow* is unclear (bug vs product, investigate vs build), intake with `solve-problem` before opening a delivery chain.

> When two skills both seem to apply, the process skill wins. It will invoke the implementation skill itself.

`ask-me-bro` owns **how** to hand off (invoke a model skill vs name a
user-invoked one). This file owns **which** name to pick.
