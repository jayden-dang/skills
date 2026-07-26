---
name: replan
description: Use when a plan is invalidated mid-flight — classifies blast radius and records the decision on the project note after user confirm.
---

# Replan

## Role

REQUIRED: read sibling `ROLE.md` (secretary default, grant rule, hybrid ban, config paths).


## Recipe

1. State what invalidated the plan (user words).
2. Classify blast radius: **next_action** | **milestone** | **outcome** | **kill project**.
3. Propose patch; apply after confirm.
4. `done_when` changes → write the log line first, then apply the change.
5. Append decision to project log.

## Done when

Decision logged; `next_action` non-empty and inside the new blast radius;
done_when change (if any) confirmed.
