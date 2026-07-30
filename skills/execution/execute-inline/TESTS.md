# `execute-inline` — test evidence

**Protocol:** `writing-skills` / `pressure-testing.md`  
**Scenarios:** `tests/pressure/execute-family/scenarios.md` (S-INLINE-*)  
**Design:** `tests/pressure/execute-family/DESIGN.md`

## RED (2026-07-30, grok-4.5) — before skill existed

| Scenario | Observed | Failure for new skill |
|---|---|---|
| S-INLINE-1 tools exist, user chose inline | **A** via execute-plan Inline Fallback | Gate text works when loaded; **no first-class trigger** |
| Routing "no subagents, implement yourself" | **execute-plan** (fallback buried) | Distinct-trigger miss — description cannot fire |
| Plan gap + demo pressure | **A** stop and ask | Keep in iron law |
| One-line + skip TDD pressure | **A** still tdd | Keep REQUIRED SUB-SKILL tdd |

**Authoring target:** elevate fallback to its own skill (routing) + full recipe
(setup, ledger, stop conditions, no unit barriers, no reviewer subagent).

## GREEN retest log (2026-07-30, grok-4.5)

| Scenario | CHOICE / result | Cite? |
|---|---|---|
| S-INLINE-1 tools exist + user inline | **A** self + tdd | yes — Iron Law |
| Routing 7 queries | plan/story/inline/debug correct split | yes |
| story-unit header + inline route | **A** no unit barrier | yes — sequential only |
| Plan gap + demo | **A** stop ask | yes |
| One-line TDD pressure | **A** tdd first | yes |
| execute-plan opened + user inline | **A** hand off execute-inline | yes — execute-plan Inline route |

## Ship gate

- [x] First-class skill + description for inline route
- [x] No implementer subagent under tool pressure
- [x] No unit barriers even if header is story-unit
- [x] Stop-on-blocker + tdd iron laws hold
- [x] execute-plan redirects to execute-inline (Inline Fallback removed)
- [ ] write-plan / AGENTS / templates family wire (downstream)
