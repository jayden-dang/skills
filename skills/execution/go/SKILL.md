---
name: go
version: 1.1.0
description: Builds the named tickets, or every ready one, through review to an open pull request each, and ends with one message. Run it with /go or /go #N.
disable-model-invocation: true
---

# Go

The third of the five commands. It takes Ready tickets to In review. The states are the roles in
`docs/agents/triage-labels.md`.

**Todos first.** Before anything else, put on the harness's todo tool (`TaskCreate` in Claude Code; load it with `ToolSearch` when it is deferred), else a checklist in your first reply one item per ticket in the frontier, in build
order, and a last item for the one message. Tick a ticket when its PR is open or its row is final. A baseline
`/go #4` ran eight tool calls into the build with no list.

REQUIRED SUB-SKILL: use `deliver-issues`. When the operator named tickets (`/go #23 #31`),
its frontier is those tickets only. Every other ticket keeps its state. With no IDs, the
frontier is every ready ticket.

End with `deliver-issues`' one message.
