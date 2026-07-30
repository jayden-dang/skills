# `execute-story` — test evidence

**Protocol:** `writing-skills` / `pressure-testing.md`  
**Scenarios:** `tests/pressure/execute-family/scenarios.md`  
**Design:** `tests/pressure/execute-family/DESIGN.md`  
**RED log:** `tests/pressure/execute-family/RED-BASELINE.md`

## RED summary (2026-07-30, grok-4.5)

| Failure | Class | Owns this text |
|---|---|---|
| All plan-execution intents route only to `execute-plan` | Distinct trigger (split case 1) | description + opening "not continuous / not inline" |
| Unit STOP message variance (mode-change write-back sometimes omitted) | Wrong/unstable shape → REQUIRED slots | `story-unit-mode.md` Unit summary contract |
| Quiz gates S-STORY-1..6 already A with dual-mode skill | No new iron laws | Extracted existing laws/rationalizations verbatim |

## GREEN — authoring targets

1. Skill exists and is discoverable for story-unit intent.
2. Unit summary contract binds all REQUIRED slots (technique re-test).
3. Iron laws / mode-change / derive-not-authored preserved from dual-mode text.

## GREEN retest log (2026-07-30, grok-4.5)

### Technique — bare unit summary (with skill)

| Rep | Model | Mode-change write-back? | All core slots? | Notes |
|---|---|---|---|---|
| 1 | grok-4.5 | yes | yes | Full contract; minors + unlock semantics |
| 2 | grok-4.5 | yes | yes* | *Stories set `{N}` omitted when prompt gave title only — title present |

**Vs RED bare:** mode-change write-back was Partial/missing under dual-mode freeform; both GREEN reps include `write Execution-mode: continuous into tasks.md` + handoff to execute-plan.

### Quiz S-STORY-1, S-STORY-2 (with skill)

| Scenario | Model | CHOICE | Cite skill? |
|---|---|---|---|
| S-STORY-1 | grok-4.5 | A | yes — iron law + EOD rationalization |
| S-STORY-2 | grok-4.5 | A | yes — mode change + execute-plan handoff |

### Description routing

| Query | Expected | Result |
|---|---|---|
| continuous + subagents | execute-plan | execute-plan |
| story-unit + review after each story | execute-story | execute-story |
| no subagents | execute-inline (future) | execute-inline named (not shipped) |
| suite failing mid-run | debug | debug |
| continuous just run it | execute-plan | execute-plan |
| story-unit unit barriers | execute-story | execute-story |

## Ship gate

- [x] Technique bare summary binds mode-change write-back (B2 fix)
- [x] Quiz gates remain A with skill citation
- [x] Description routes story-unit vs continuous (B1 fix)
- [x] No-op + duplication: per-task loop inlined intentionally until execute-plan narrow extracts shared home; templates pointer to `../execute-plan/*-prompt.md`
- [ ] execute-plan still dual-mode until its own RED/GREEN narrow pass
- [ ] execute-inline not shipped
- [ ] write-plan / AGENTS / templates cross-refs after family complete
