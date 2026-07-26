---
name: sync-workspaces
description: Use when reconciling disk folders under configured roots with the project registry — produces an advisory orphan/missing report without auto-creating projects.
---

# Sync workspaces

## Role

REQUIRED: read sibling `ROLE.md` (secretary default, grant rule, hybrid ban, config paths).


## Iron Law

```
REPORT ONLY.
NO AUTO-CREATE.
NO AUTO-DELETE.
```

## Steps

1. Read `roots`, ignore globs, max_depth from config.
2. Read registry + each project's `workspace.path`.
3. Scan roots (skip sandbox root by default).
4. Emit three lists: **orphan disk** | **missing path** | **still missing (info)**.
5. Suggest actions; **wait for per-item confirm** before any registry/project write.
6. Never promote sandbox paths to active WIP.

## Rationalizations

| Thought | Reality |
|---|---|
| "Register everything for completeness" | Completeness is the report, not mass active projects |
| "Orphans are obviously projects" | User confirms membership |
| "I'll create then they can delete" | Creates WIP debt and ghosts |

## Done when

User has the three lists; any writes were explicitly confirmed.
