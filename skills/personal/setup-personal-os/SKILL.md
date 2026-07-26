---
name: setup-personal-os
description: Use when installing Personal OS into a notes vault or remapping folders — produces a vault config mapping layout roles to the user's paths without forced renames.
disable-model-invocation: true
---

# Setup Personal OS

User-invoked. Do not auto-start bulk moves.

## Role

REQUIRED: read sibling `ROLE.md` (secretary default, grant rule, hybrid ban, config paths).


## Goal

A working **config** file that maps logical roles → this vault's real folders, plus optional template seeds.

## Templates

From package `templates/personal-os/` (or install path). If missing, create minimal stubs — do not invent a second layout system.

## Steps

1. Detect top-level dirs (any PARA/journal/inbox style).
2. Propose `layout:` table: role → **their** path.
3. Show recommended tree as **suggestion only** (package README).
4. One decision: keep names vs adopt recommended.
5. Write config **only after explicit OK**.
6. Create dirs / migrate **only** with confirmation.
7. Seed empty registry + optional templates.
8. Optional `roots.*` — only paths the user states.
9. Do not auto-register disk repos as projects.

## Never

- Bulk rename without consent  
- Delete notes  
- Invent machine-specific paths  

## Done when

Config validates; home note usable; user knows next skill to run (`life-charter` or `open-project`).
