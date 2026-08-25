---
name: ask-me-bro
version: 1.1.0
description: Routes among the already-installed development skills to the one that fits the task at
  hand. Run it with /ask-me-bro.
disable-model-invocation: true
---

# Ask Me Bro

You are the router. Read the situation, name the entry point, and explain the
chain that follows. Do not start executing the chosen flow inside this skill.

**Which skill:** load `docs/guide/process/on-ramps.md` and pick the matching
row. That table is the one home — do not invent a parallel list here.

**How to hand off:** if the entry point is model-invocable (`frame-change`,
`frame-change`, `amend-feature`, `root-cause`, `validate-feature`,
`review-product-flow`, `reroute-plan`, `realign-spec`, `plan-milestones`),
invoke it and let it take over. If it is a user-invoked skill (`triage`,
`publish-issues`, `scan-architecture`, `configure-repo`, `bootstrap-repo`,
`define-project`, `refresh-roadmap-status`, `assess-milestone`,
`write-handoff`, `cut-release`, `pathfind`), you cannot invoke it — name it
and tell the user to run its command, e.g. `/triage` or `/pathfind`.

**Context hygiene:** keep discovery through plan in one unbroken context
window. If the window is filling before the plan is done, tell the user to
run `/write-handoff`. Execution sessions are context-isolated per task by
design.
