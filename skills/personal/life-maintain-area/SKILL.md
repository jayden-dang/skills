---
name: life-maintain-area
version: 1.0.0
description: Use on an area's review cadence or yellow/red health — updates the area note health and next_action, proposing a project only when a gap needs an outcome.
---

# Maintain area

## Role

REQUIRED: read sibling `ROLE.md` (secretary default, grant rule, hybrid ban, config paths).


## Recipe

1. Open area note; walk standards checkboxes with user, marking each pass or fail.
2. Set `health`: green | yellow | red (confirm red).
3. If gap needs an end-state → propose `life-open-project` (WIP rules). Else set area `next_action` only.
4. Set `next_review`.

## Done when

Health and next_review written; every standard in the area note marked pass or fail.
