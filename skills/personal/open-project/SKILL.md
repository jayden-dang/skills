---
name: open-project
description: Use when the user commits to a new outcome — creates a project note and registry row under the WIP limit with non-empty done_when and next_action.
---

# Open project

## Role

REQUIRED: read sibling `ROLE.md` (secretary default, grant rule, hybrid ban, config paths).


## Iron Law

```
NO ACTIVE PROJECT WITHOUT done_when AND next_action.
NO ACTIVE ABOVE WIP LIMIT.
```

## Steps

1. Count projects with `status: active`. If at `limits.max_active_projects`, **stop**: propose pause/close one (user picks). Do not create a sixth active.
2. Require non-empty **outcome** and **done_when** (user words). Reject `TBD` / empty / "figure out later" while active.
3. Create note under `layout.projects_active` from project template.
4. Optional `workspace.path` — record `path_status` if probed; never invent remotes.
5. Add registry row.
6. Set one concrete `next_action`; `phase: intake` or `roadmap`.
7. Offer `plan-project` for milestones (do not invent a 3-month task tree).

If they only have a name: REQUIRED SUB-SKILL path is user runs `capture` — park in inbox, not active.

## Rationalizations

| Thought | Reality |
|---|---|
| "I'm the boss, skip WIP" | Authority reorders; does not repeal WIP |
| "Just register quickly" | Active slots are scarce — use capture if unready |
| "done_when TBD is fine" | Ghost project — illegal while active |
| "Exception note in the file" | Soft compliance still breaks the cap |

## Done when

Legal frontmatter; registry row; WIP still ≤ limit; no product work performed.
