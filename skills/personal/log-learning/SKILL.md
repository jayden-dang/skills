---
name: log-learning
description: Use after a practice session — appends a practice log and updates the track streak, last_practice, and next_action from the user's report.
---

# Log learning

## Role

REQUIRED: read sibling `ROLE.md` (secretary default, grant rule, hybrid ban, config paths).


## Recipe

1. Append log entry from **user-reported** practice (what, minutes, difficulty).
2. Update track: `last_practice`, `streak` rule (consecutive cadence hits; reset on miss if you track it), `next_action`.
3. Note weak points for next session.

Do not invent practice that did not happen.

## Done when

Track frontmatter matches the reported practice.
