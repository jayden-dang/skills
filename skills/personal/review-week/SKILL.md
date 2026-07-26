---
name: review-week
description: Use in the weekly review slot — produces a weekly review note with audits and at most N P0s marked PROPOSED until the user confirms.
---

# Review week

## Role

REQUIRED: read sibling `ROLE.md` (secretary default, grant rule, hybrid ban, config paths).


## Iron Law

```
REVIEW FEEDS PLAN.
P0s ARE PROPOSED UNTIL CONFIRMED.
NO UNILATERAL PRIORITY REWRITES.
```

## Steps

1. Inbox: run clarify flow or confirm zero (`process-inbox` if items remain).
2. Wins / misses — user-led; short.
3. Every **active** project: still want? `next_action` valid? `path_status`?
4. Learning tracks: cold >7 days?
5. Areas: health skim.
6. Draft kill/pause list if over WIP — **confirm** before status changes.
7. Draft ≤ `limits.max_weekly_p0` **P0s** with one-line why each.
8. Write weekly review file. Mark P0s **PROPOSED** until user confirms.
9. On confirm only: apply priority/focus seeds; else leave project state unchanged.
10. Optional: name `sync-workspaces` for an advisory disk report.

## Rationalizations

| Thought | Reality |
|---|---|
| "They're exhausted — just set P0s" | Write PROPOSED; do not apply cold |
| "No questions means no consent" | Yes/no on a draft still required to apply |
| "Chat list is enough" | Durable review file is the artifact |
| "I'll fix wrong P0s next week" | Applied wrong priorities poison the week |

## Done when

Weekly file exists; every active project audited; P0s either confirmed-and-applied or clearly PROPOSED; ghosts flagged or fixed with user OK.
