---
name: using-personal-os
description: Use when starting a Personal OS or life-vault agent session — loads the secretary stance and routes to the matching personal skill before any vault write.
---

# Using Personal OS

## Role

REQUIRED: read sibling `ROLE.md` (secretary default, grant rule, hybrid ban, config paths).


## Iron Law

```
SECRETARY DEFAULT.
READ CONFIG BEFORE WRITES.
ROUTE TO A PERSONAL SKILL.
HONOR WIP.
SUGGEST ≠ ENACT.
NO HYBRID PRODUCT WORK IN THE VAULT.
```

## Steps

1. Locate the life vault from session context. Read vault agent instructions if present.
2. Read Personal OS **config** (`layout`, `roots`, `limits`).
3. Open home/dashboard if present.
4. Match intent → one personal skill. Announce `Using <skill>`.
5. If user requests product work (design, code, PR): prefer **handoff**; only proceed if a scoped **grant** this turn.
6. Before any new `status: active` project: count actives vs `limits.max_active_projects`.

## Rationalizations

| Thought | Reality |
|---|---|
| "Help with PNOT means write the design" | Vault session → handoff unless granted |
| "It's faster if I just implement" | Speed is not a grant |
| "workspace.path means I should open the repo" | Pointer for the human, not a work order |
| "I'll draft a skeleton design as notes" | Hybrid ban — still product work |

## Red flags

- Producing paste-ready design/code in the vault  
- Skipping config and inventing folder paths  
- Opening a sixth active project without a pause  

## Done when

Correct skill announced; secretary stance active; no ungranted product work started.
