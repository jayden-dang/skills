---
name: log-learning
description: Use after a practice session — appends a practice log and updates the track streak, last_practice, and next_action from the user's report.
---

# Log learning

## Role

REQUIRED: read sibling `ROLE.md` (secretary default, grant rule, hybrid ban, config paths).


## Recipe

1. Append log entry from **user-reported** practice (what, minutes, difficulty).
2. Update track: `last_practice`, `streak` (consecutive cadence hits — reset to 0 when the gap since `last_practice` exceeds the track's cadence), `next_action`.
3. Append the session's weak points to the track note's `weak_points` field — they are what step 2's `next_action` is drawn from.

Do not invent practice that did not happen.

## Done when

Track frontmatter matches the reported practice.
