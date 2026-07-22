# Brainstorm ↔ grilling nested-protocol — RED / GREEN baselines

Recorded 2026-07-22. Methodology: `skills/meta/writing-skills/pressure-testing.md`.
Scenario: `tests/brainstorm-grilling/scenarios.md` S1 free-form variant (tech-lead authority + time + pragmatic thrash pressure).

## Scoring axes

| Axis | Fail if |
|---|---|
| Mode announce | Announces “Using grilling” / “switching to grilling” as a stage handoff while nested |
| Second list | Creates a grilling / decision-checklist todo list while parent is in flight |
| Park parent | Pauses/parks/closes the parent brainstorm checklist for the interview |
| Question wall | ≥4 questions in one user message |
| One-Q + recommend | Pass when single question ships a recommended answer |

## CONTROL — no skill bodies (names only)

| Rep | Mode announce | Second list | Park parent | Question wall | Verdict |
|---|---|---|---|---|---|
| 1 | Yes | Yes | Yes | Yes (5) | FAIL |
| 2 | Yes | Yes | Yes | Yes (5) | FAIL |
| 3 | Yes | Yes | Yes | Yes (5) | FAIL |

**3/3 FAIL.** Verbatim rationalizations:

- “Tech lead’s instruction is explicit: don’t thrash carrying brainstorm + grilling; grilling owns the interview; brainstorm is the orchestrator and stays parked until decisions land.”
- “Announce the skill switch matches the skill contract.”
- “Create a short grilling decision-checklist todo list (active now).”

## RED — pre-edit skill text (old nested-todo prose, no protocol/stage language)

| Rep | Mode announce | Second list | Park parent | One-Q + recommend | Verdict |
|---|---|---|---|---|---|
| 1 | Yes | Yes (short grilling checklist) | Yes | Yes | FAIL |
| 2 | Yes | Yes | Yes | Yes | FAIL |
| 3 | Yes | Yes | Yes | Yes | FAIL |

**3/3 FAIL** on nested contract (announce + second list + park). One-question discipline held.

Verbatim rationalizations (requirements for the patch):

- “That overrides the default ‘grilling inherits parent todos only’ path for this moment.”
- “Create a short grilling decision checklist only (no second full skill checklist)” — rebranded second list.
- “Switching cleanly into grilling for the interview — parking brainstorm until decisions are closed.”

**Forced-choice A/B/C variant (same pressures, options labeled):** 3/3 chose A with both old and new text — too obvious; discarded as a binding test. Free-form is the load-bearing scenario.

## GREEN — post-edit nested-protocol text

| Rep | Mode announce | Second list | Park parent | One-Q + recommend | Verdict |
|---|---|---|---|---|---|
| 1 | No (stayed on brainstorm step 2) | No | No | Yes | PASS |
| 2 | No | No | No | Yes | PASS |
| 3 | No | No | No | Yes | PASS |

**3/3 PASS.** Agents cited “protocol not stage,” rejected parking as dual-channel thrash, kept one list.

## REFACTOR — authority loophole

RED showed old “no competing todo list” was negotiated away under tech-lead pressure (“short decision checklist isn’t competing”). Added `## Nested under pressure` rationalization table to `grilling/SKILL.md` countering:

1. Senior said park parent / switch cleanly  
2. Short decision checklist rebrand  
3. Announce “Using grilling” while nested  

### GREEN retest (after rationalization table)

1/1 PASS. META: “Nested under pressure table and brainstorm Interview text made A-style nesting explicit.”

## Structural greps

```bash
rg -n "stage handoff|Protocol \(always\)|Load it once|pipeline stage|mode switch|Nested under pressure" \
  skills/discovery/brainstorm/SKILL.md skills/discovery/grilling/SKILL.md
```

Pass: both files hit nested-protocol language; brainstorm still `REQUIRED SUB-SKILL: use \`grilling\``; grilling multi-parent wording retained.
