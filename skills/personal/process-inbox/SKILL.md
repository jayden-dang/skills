---
name: process-inbox
description: Use when unprocessed inbox notes need clarifying — produces a route decision per item and updates or files notes after confirm when moves are ambiguous.
---

# Process inbox

## Role

REQUIRED: read sibling `ROLE.md` (secretary default, grant rule, hybrid ban, config paths).


## Recipe

For each note with `processed: false`:

| If | Route |
|---|---|
| Trash | Delete or archive |
| ≤2 min action | User does it (unless grant); else schedule on daily |
| Reference only | `layout.resources_dir` |
| Next action on existing project | Propose `next_action` update |
| New outcome | `open-project` (WIP rules apply) |
| Area standard | `maintain-area` |
| Learning | track or `open-learning-track` |
| Someday | `horizon: someday` note or area park |

Then set `processed: true`, `routed_to`, move/delete per vault taste.

Ambiguous bulk moves → show table; wait confirm.

## Done when

No unprocessed inbox items remain, or leftovers are explicitly deferred with reason.
