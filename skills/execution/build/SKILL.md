---
name: build
version: 1.4.0
description: Use when an approved tasks.md is to be executed. Produces the built feature task by task, with a progress ledger, a two-verdict review of each task and a revision-bound close receipt, run as continuous subagent waves, as human-gated story units, or inline without subagents, as the plan's Execution-mode line and the environment say.
---

# Build

One approved plan, three ways to run it. Read the `Execution-mode:` line of `tasks.md` and look
at the environment, then read **exactly one** mode file beside this one and follow it:

Check the rows in order and take the first that holds:

| What holds | Read |
|---|---|
| this harness cannot dispatch subagents, or the operator chose to watch the controller implement | `inline.md` |
| `Execution-mode: story-unit`, or the operator asked to review after each story | `story.md` |
| `Execution-mode: continuous` | `waves.md` |

A caller that names a mode ("`build` (story mode)") has chosen it. No `Execution-mode:` line,
no named mode and no word from the operator: `waves.md` where subagents exist,
else `inline.md`. Each mode file says when to hand over to another.

All three share one controller recipe, `common.md`: session preflight, the ledger check, the
todos gate, runtime binding and the close sequence. Its parts are `task-lifecycle.md`,
`ledger-check.md`, `runtime-binding.md`, `tracker-sync.md`, `decision-trail.md`,
`implementer-prompt.md`, `task-reviewer-prompt.md` and `close-receipt.md`. Each mode file names
the moment to load them.

*Done when: you have said which mode is running and why, and opened that one file.*
