---
name: run-session
description: Use when running a typed study session, lesson, or practice drill in the target language — produces the session note carrying due-queue work, a forced-production quota, the learner's self-marking, and the diagnosis.
---

# Run session

## Role

REQUIRED: read sibling `ROLE.md` (coach default, produce-first, evidence gate, config paths).

## Iron Law

```
LEARNER PRODUCES FIRST.
FORCED PRODUCTION BEFORE FREE PRODUCTION.
SELF-MARK BEFORE CORRECTION.
NO DEBT.
```

## Steps

1. Read `profile.md`, the active cycle's focus, live rows in `errors.md`, and every row where `next_due <= today` in **both** `capability-map.md` and `lexicon.md`. The lexicon queue is part of the session, not an extra.
2. Pick the mode. This is the home of the recovery and no-debt rules:
   - **full** — `config.schedule.session_shape`;
   - **minimum** — learner says the day is short: `config.schedule.minimum_session_minutes` covering the due queue plus one production task;
   - **recovery** — gap since `profile.last_session` exceeds `config.schedule.recovery_gap_days`: warm-up first, due queue capped at 5.
   Overdue items never stack. Re-bucket the oldest and move on — `config.schedule.study_debt` is false.
3. **Name the forced-production quota out loud before the task**: `limits.forced_production` capabilities at R0 (understands) or R1 (recognises) from the cycle focus that this session's output must contain. Naming them after the task turns the quota into a report instead of a constraint.
4. Set the task. The learner produces. Do not model the answer, supply the vocabulary, or write a first line. If they stall twice on the same idea, give a **frame** — a sentence stem, a function label, a question that decomposes it — never a finished sentence.
   **Due lexicon rows are reviewed by being required, not recited**: build the task so those chunks are the natural way to say it. Asking what a word means tests memory and moves no state; using it unprompted is what promotes the row.
5. **Self-mark**: before saying anything about accuracy, ask the learner to flag what they believe is wrong and rate confidence 1–5. Their marks go in the note verbatim, whether right or wrong.
6. REQUIRED SUB-SKILL: use `diagnose-output` on what they produced.
7. Close with a 60-second unscripted monologue on any theme from the cycle. The learner reports `translation_ratio` — roughly what share they composed in the support language first. Record the number; do not argue with it.
8. Write `sessions/<date>-s<N>.md` (`kind: study`). The coach fills the note; the learner types nothing they did not already say.
9. Update `profile.md`: `last_session`, `streak`, calibration gap, translation ratio. Re-bucket `next_due` on every lexicon and capability row that came up.

## Rationalizations

| Thought | Reality |
|---|---|
| "Show a model answer first, it teaches faster" | It removes exactly the retrieval the session exists to train |
| "They're tired — skip the forced items" | Avoided structures generate no errors, so error-driven practice never reaches them |
| "Self-marking is a formality" | The calibration gap is the only progress signal available without a diagnostic test |
| "Three days missed — run the whole backlog" | Recovery mode, capped queue, oldest re-bucketed |
| "They asked me to just write it" | Offer the repair path. If they decline it in words, produce it and write `exception:` in the note |
| "Quiz the due words first, then practise" | A definition recalled is not a word used. Build the task so the chunk is needed |
| "The note can wait until later" | An unwritten session leaves no evidence, so nothing in the map can move |

## Red flags

- A target-language sentence produced by the coach before the learner attempted one
- Forced-production capabilities named only in the note, never to the learner
- Correction delivered before the self-mark was captured
- Session note missing, or written from memory a day later

## Done when

Session note written with mode, forced quota (used or explicitly recorded unmet), self-mark, diagnosis, and translation ratio; `profile.md` updated.
