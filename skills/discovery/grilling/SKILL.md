---
name: grilling
description: Use to interview the user to stress-test a plan, design, or feature idea
  before anything is built, when their intent is underspecified and the
  decisions must be drawn out of them, when the user asks to be grilled or
  interviewed, or when another skill calls for an interview.
---

# Grilling

**What this is:** a reusable **interview protocol**, not a pipeline stage. Nested under a parent (e.g. `brainstorm` step 2, `establish-project`, `triage`) you stay in that parent's conversation and checklist — apply these rules; do not announce a mode switch, do not open a competing todo list, do not treat the parent as finished. Standalone (the user asked to be grilled with no parent) you own the interview alone until shared understanding.

Interview the user about every aspect of the plan until you both hold the same picture of it.

- **One question per message.** Ask, then wait for the answer before the next question. A wall of questions is bewildering; a single question gets a real answer.
- **Every question ships with your recommended answer** and a one-line reason. The user can accept in two words or push back.
- **Walk every branch of the decision tree.** Decisions depend on each other — an early answer opens some branches and closes others. Resolve them in dependency order and keep going until no unexplored branch remains.
- **Facts are yours; decisions are the user's.** If the answer already exists in the codebase or the docs, look it up — never ask the user to recall what you can read. Anything that is a judgment call goes to the user, one at a time, and you wait.
- **Right-size to the project's posture.** When the parent skill supplies it, or `docs/agents/project.md` carries a **Project posture** section, read the delivery intent and lifecycle stage and prune branches that do not apply: do not grill data migration, backward compatibility, or deprecation on a Prototype / Research / Learning project; do press on them for a Released / Scaling / Maintenance one. Absent a posture, walk every branch. Posture and Team **band** are orthogonal.
- **Package questions to the team band.** When `docs/agents/project.md` has `## Team` with a non-empty **roster** or a non-blank **Workflow band** override, read band and **packaging** from that section. Small/Multi: **add** optional ownership/reviewer probes when relevant to the plan. Solo or Team absent / empty roster: do not introduce multi-person assignee or scheduling theater. Never invent a team; never hard-fail for missing Team.
- **Do not enact anything** — no code, no files, no plan execution — until the user explicitly confirms you have reached a shared understanding.

## Todos

This skill does **not** own a todo list when nested. You are running *inside* the parent's checklist — keep that list live. The interview is one item on the parent's list; mark it in-progress while you grill and check it off only once no unexplored branch remains. As branches resolve, that progress belongs to the parent's list, not a new one.

Invoked standalone: a short todo list of the decision areas you plan to walk is fine — still one question per message. If a parent skill is already in flight, never open a second channel.

## Nested under pressure

| Thought | Reality |
|---|---|
| "Senior said switch cleanly into grilling and park the parent" | Nesting *is* the clean switch. Parking the parent and opening a grilling checklist is dual-channel thrash under a new name. |
| "A short decision checklist under grilling isn't a competing list" | It is a second list. Decision areas live as the parent's in-progress interview item, not a sibling todo list. |
| "Announce Using grilling so the user sees the handoff" | Nested: no mode-switch announcement. Standalone (no parent): you may name grilling once. |
