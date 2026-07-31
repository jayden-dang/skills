# Design: Pathfind layer

Feature code: PFIND  
Status: Approved (design narrative SSOT: `docs/design/pathfind-layer.md`)  
Date: 2026-07-31  
Requirements: ./requirements.md  
Narrative SSOT: [`docs/design/pathfind-layer.md`](../../design/pathfind-layer.md)

This file is the **feature design bridge** for tasks and `Satisfies:` citations.
Full architecture (layers, fog, OD locks, handoff matrix) lives in the narrative
SSOT; do not fork that content here.

**Respects:** ARCH-2, ARCH-3, ARCH-5, ARCH-6

## 1. Skill surface

**Satisfies:** PFIND-1.1, PFIND-1.2, PFIND-1.3, PFIND-1.4, PFIND-1.5

User-invoked skill at `skills/discovery/pathfind/SKILL.md` with
`disable-model-invocation: true`. Modes Chart and Work. Description is one
plain human-facing line (outcome noun: decision map). Neighbors only **name**
`/pathfind`; optional layer no-ops when unused.

**Reuse:** existing — `clarify-decisions`, `research`, `run-spike`, `define-domain`
composition pattern from `frame-change` (rung 2).

## 2. Chart and Work workflows

**Satisfies:** PFIND-2.1–PFIND-2.10, PFIND-3.1–PFIND-3.9

Chart: brownfield scan gate → destination via nested `clarify-decisions` →
breadth-first tickets vs fog → map body slots → research parallel → knowns
skeleton; no HITL resolve in Chart.  
Work: low-res map → claim first → one HITL ticket → resolve → Decisions so far
(re-read before append) → graduate fog / out of scope.

**Reuse:** existing — `define-project/brownfield-scan.md` predicate and untrusted-candidate
rules (rung 2).

## 3. Decision tickets and vocabulary

**Satisfies:** PFIND-4.1–PFIND-4.8, PFIND-5.1–PFIND-5.5

Types: `clarify` | `research` | `prototype` | `task`. Labels `pathfind:*`. Never
`grilling` / `wayfinder`. Plan-don’t-do hard gate. Strict separation from
`publish-issues` graphs.

## 4. Tracker ops and knowns

**Satisfies:** PFIND-6.1–PFIND-6.4, PFIND-7.1–PFIND-7.7

Pathfind operations section in issue-tracker templates; local fallback under
`.skills/pathfind/<effort>/`. Knowns package + exit rules (complete / deferred fog /
early stop). Handoff names only. `frame-change` seeds knowns when pointed at package.

## 5. Lenses, routing, docs

**Satisfies:** PFIND-8.1–PFIND-8.2, PFIND-9.1–PFIND-9.3, PFIND-10.1–PFIND-10.3

Explore/Forge/Recon guidance-only. `route-task` on-ramp. Post-ship ADR +
workflows.md + skills.md. author-skills pressure before ship.

## Seams for testing

| Seam | What is asserted | IDs |
|---|---|---|
| Skill file + frontmatter | Exists, user-invoked, modes named, description shape | PFIND-1.1–1.3 |
| Skill body gates | Plan-don’t-do, types, no grilling, claim-first, one HITL | PFIND-3.2, 3.8, 4.*, 5.* |
| Chart/Work recipes | Required sections, fog test, research exception, exit | PFIND-2.*, 3.*, 7.* |
| Tracker seeds | Pathfind operations in templates | PFIND-6.3 |
| Neighbors | route-task names `/pathfind`; frame-change knowns seed | PFIND-7.6, 7.7, 9.1 |
| Registration | AGENTS/plugin/README inventory | PFIND-1.1, 9.2 |
| Scenarios markdown | Greppable ID layer for all criteria | all PFIND-* |
| author-skills RED | red-baselines + pressure scenarios before GREEN skill text | PFIND-10.3 |

## Out of scope (design)

Matches requirements Out of Scope. Narrative detail: pathfind-layer.md §2.2.
