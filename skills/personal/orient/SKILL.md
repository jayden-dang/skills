---
name: orient
description: Use when the user needs a status snapshot — produces a WIP and focus briefing with exactly one recommended next focus.
---

# Orient

## Role

REQUIRED: read sibling `ROLE.md` (secretary default, grant rule, hybrid ban, config paths).


## Recipe

Emit a briefing with REQUIRED sections:

1. **Active projects** — id, priority, next_action, path_status  
2. **Today** — daily focus if a daily note exists  
3. **Blocked / missing / overdue**  
4. **Learning cold** — tracks with last_practice >7 days or unknown  
5. **One recommendation** — single next focus (optionally energy-matched)  

Read-only by default. Write only if user asks to append orientation to daily.

## Done when

Briefing complete with exactly one recommended focus; no project state changed unless asked.
