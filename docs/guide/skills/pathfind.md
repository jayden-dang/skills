# `pathfind`

> Chart or advance a multi-session **decision map** until the route to a destination is clear. Optional Layer 0 — decisions, not deliverables.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | **user-invoked only** — `/pathfind`. `disable-model-invocation: true` |
| **Reads** | `docs/agents/issue-tracker.md` (Pathfind operations), optional territory scan / knowns under `.skills/pathfind/` |
| **Writes** | Map + decision tickets on tracker (or local `.skills/pathfind/`), knowns package |
| **Calls** | `clarify-decisions`, `research`, `run-spike`, `define-domain` (passive); **names** handoff skills only |
| **Called by** | nobody auto — user runs it; `route-task` may *name* it |

## When it fires

Effort is **larger than one agent session** and the route is still **foggy**. Not for tier-0 tweaks, clear single-session features, or bugs (`root-cause`).

## Modes

- **Chart** — name destination, surface sharp decision tickets, leave fog, fire research in parallel; do not resolve HITL tickets in the charting session.
- **Work** — claim one frontier ticket, resolve it, graduate fog, update knowns.

## Vocabulary

Ticket type **`clarify`** (not `grilling`); resolve via **`clarify-decisions`**. Labels `pathfind:*`.

## See also

- [`clarify-decisions`](clarify-decisions.md) — HITL interview protocol
- [`frame-change`](frame-change.md) — after fog clears
- [`publish-issues`](publish-issues.md) — implement tickets (strict separate graph)
- Design: `docs/design/pathfind-layer.md` · Spec: `docs/specs/2026-07-31-pathfind/`
