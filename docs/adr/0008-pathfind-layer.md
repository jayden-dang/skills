# 0008 — Optional Pathfind layer (decision maps)

**Status:** Accepted  
**Date:** 2026-07-31  

## Context

Multi-session discovery of *decisions* (not build slices) had no durable home: chat and
`.skills/` ephemera die on compact; forcing fog into `frame-change` or
`plan-milestones` freezes unverified shape. Matt Pocock wayfinder and BMAD Analysis
informed the shape without forking either.

## Decision

Ship user-invoked skill **`pathfind`** as optional Layer 0:

- Tracker-backed (or local `.skills/pathfind/`) **decision map** + decision tickets
- Types: `clarify` | `research` | `prototype` | `task` (vocabulary: **not** `grilling`)
- Plan-don't-do; strict graph separation from `publish-issues`
- Knowns package under `.skills/pathfind/<effort>/knowns.md`
- Agents **name** `/pathfind`; never auto-invoke (ARCH-5)
- No new ARCH-N until pressure proves plan-don't-do needs an invariant ID

## Consequences

- Greenfield and brownfield share one skill; brownfield requires territory scan before destination
- `frame-change` seeds knowns when pointed at a pathfind package
- `route-task` on-ramps multi-session fog → `/pathfind`
- Ordinary tier-0/1 work unchanged when no map exists (ARCH-2)
