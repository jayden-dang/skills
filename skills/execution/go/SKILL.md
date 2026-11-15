---
name: go
version: 1.3.0
description: Use when the operator sends /go, or asks in other words for every ready ticket on the board, or named tickets, to be built, reviewed and opened as pull requests in one unattended run. Produces a pull request for each ticket and one message at the end for whatever needs the operator.
---

# Go

The third of the five commands. It takes Ready tickets to In review. The states are the roles in
`docs/agents/triage-labels.md`.

**Todos first.** Before anything else, put on the harness's todo tool (`TaskCreate` in Claude Code; load it with `ToolSearch` when it is deferred), else a checklist in your first reply one item per ticket in the frontier, in build
order, and a last item for the one message. Tick a ticket when its PR is open or its row is final. A baseline
`/go #4` ran eight tool calls into the build with no list.

REQUIRED: read `deliver.md` beside this file and follow it. When the operator named tickets
(`/go #23 #31`), its frontier is those tickets only. Every other ticket keeps its state. With no IDs, the
frontier is every ready ticket.

End with the one message `deliver.md` describes.
