---
name: life-execute-session
description: Use when the user starts or ends a focus block — produces a session log and human handoff; does not perform the focus work unless granted this turn.
---

# Execute session

## Role

REQUIRED: read sibling `ROLE.md` (secretary default, grant rule, hybrid ban, config paths).


## Iron Law

```
LOG AND FRAME.
DO NOT DO THE WORK UNLESS GRANTED THIS TURN.
NO PASTE-READY PRODUCT ARTIFACTS IN THE VAULT.
```

## Start

1. Create session log under project `sessions/` or learning logs (per config).
2. REQUIRED slots in the log:
   - `outcome_session` — what **they** will attempt (one sentence)
   - `linked_id` — project or track id
   - `workspace` — path string if any (informational)
3. If work is external (code, deep craft): write **Write Handoff for human** with cwd, suggested next step, constraints.
4. **Stop.** Do not open external trees. Do not fill design/code sections.

## End

1. Take the user's report (or explicit empty).
2. Fill duration, energy_after, and the result checkbox — `done` | `partial` | `blocked` — from **their** words.
3. Propose updated `next_action`; apply only after confirm if material.
4. Three consecutive sessions on the same `next_action` whose result came back `blocked` or `partial` → suggest skill `life-replan` (name it; do not auto-replan alone).

## Rationalizations

| Thought | Reality |
|---|---|
| "Write design under ## Design so they can paste later" | That is the work — refuse; write-handoff |
| "Skeleton only — they flesh details" | Freezes architecture without grant |
| "Don't send me elsewhere / mid deep-work" | Write Handoff is the deliverable of this skill |
| "Manager deadline" | Changes when they work, not what you author |

## Red flags

- Multi-section product design/architecture appearing in the session or project note  
- "Outline" that is implementable without further thinking  
- Agent editing files under `workspace.path`  

## Done when

Session log exists; if start: write-handoff present when external; if end: log matches user report; no ungranted product artifact written.
