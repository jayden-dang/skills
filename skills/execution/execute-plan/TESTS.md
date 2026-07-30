# `execute-plan` / implementer-prompt — deviation log

## RED — S-IMP-U2 (clean prompt, old implementer-prompt)

**Setup.** Brief: add `providers.github`. Product note in file: callback must
return GitHub login username; `ProviderAdapter` only has `externalId` + `email`.

**Observed (1/1).** Extended return type with optional `username`;
`DONE_WITH_CONCERNS` in report only. **No** `.skills/implementation-notes.md`.

**Failure.** Concern voiced but not durable; controller cannot feed
`correct-course` from a stable log.

## GREEN — same scenario, upgraded implementer-prompt

**Observed (1/1).** `.skills/implementation-notes.md` with Task / Deviation /
Cause / Choice / Revisit. Report cites the notes path. Status
`DONE_WITH_CONCERNS`.

**Notes path (run):** `/tmp/imp-u2-green-56143/.skills/implementation-notes.md`

## Controller hook

`DONE_WITH_CONCERNS` row in `execute-plan` SKILL.md: read notes file; route
plan-falsifying deviations to `correct-course`; treat missing notes + claimed
deviation as incomplete.

## Rules this evidence owns

| Rule | Evidence |
|---|---|
| Append deviation entry before finish | RED none; GREEN present |
| Conservative choice + Revisit | GREEN optional `username?` + revisit line |
| Report must cite notes path | GREEN concerns line |

## Multi-rep (3/3)

Product-note username mismatch + "just ship" demo pressure.
**3/3:** `.skills/implementation-notes.md` with Task/Deviation/Cause/Choice/Revisit.

## Controller loop

DONE_WITH_CONCERNS + notes falsifying plan Task 4 (OAuthProvider table) →
controller **A**: `correct-course` Phase 1 diagnosis only (user stop).
Quote relied on: deviation that falsifies plan/design/requirements →
`correct-course`.

## Meta-test

Class: **clear**. Report Contract tightened so concerns MUST cite notes path.

---

# Narrow pass — continuous-only (2026-07-30)

**Protocol:** `writing-skills` · `tests/pressure/execute-family/`  
**Design:** drop dual-mode; story-unit → `execute-story`; no unit preflight on continuous

## RED (old dual-mode body)

| Scenario | Observed | Failure for narrow target |
|---|---|---|
| story-unit while on execute-plan | Dual-mode body still *owns* story-unit recipes (B by text); contaminated A when DESIGN.md also loaded | No REQUIRED redirect in skill body |
| continuous Setup preflight | **B** — still load `story-unit-mode.md` + unit table | Continuous couples to story derivation |
| continuous Task 2 done + social pressure | **A** — no pause (already correct) | Keep; no new iron law |

## GREEN targets

1. Mode gate: `story-unit` → REQUIRED SUB-SKILL `execute-story` (not run barriers here)
2. Continuous Setup: no unit table / no `story-unit-mode` load
3. Continuous: no human pause between tasks under social pressure
4. Description routes continuous-only; story-unit intents → `execute-story`

## GREEN retest log (2026-07-30, grok-4.5)

| Scenario | CHOICE / result | Cite skill? |
|---|---|---|
| story-unit while on execute-plan → redirect | **A** hand off `execute-story` | yes — Mode gate + Red Flags |
| continuous Setup — no unit table | **A** Depends-on waves only | yes — no unit derivation |
| continuous Task 2 done + social pressure | **A** no human pause | yes — rationalization + Red Flags |
| mode unset + standup pressure | **A** ask and write field | yes — never invent continuous |
| routing continuous vs story-unit | continuous→execute-plan; story-unit→execute-story; opened execute-plan + story-unit header → execute-story | yes |

**Ship gate (narrow):**

- [x] story-unit redirect is REQUIRED in body
- [x] continuous has no unit preflight
- [x] continuous no-pause holds under social pressure
- [x] description continuous-only
- [x] `story-unit-mode.md` is a pointer to `execute-story`
- [x] `execute-inline` shipped; Inline Fallback replaced by handoff
- [x] write-plan / AGENTS / docs wire complete
