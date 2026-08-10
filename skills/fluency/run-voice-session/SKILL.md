---
name: run-voice-session
description: Use when the practice turn is spoken — a conversation, speaking practice, roleplay, or a talk-to-me session in the target language — produces the voice session note carrying a four-dimension debrief (grammar, sentence formation, pronunciation, fluency) and timestamped unprompted-use evidence.
---

# Run voice session

## Role

REQUIRED: read sibling `ROLE.md` (coach default, produce-first, evidence gate, config paths).

## Iron Law

```
SPEAK, DON'T FORMAT.
SHORT TURNS, ONE QUESTION.
RECAST IN FLOW, DIAGNOSE AT THE END.
HOLD THE SILENCE FOR THE FULL COUNT.
ALL FOUR DIMENSIONS REPORTED, EVERY SESSION.
```

## The voice contract

| Do | Instead of |
|---|---|
| Spoken prose only | Headings, bullets, numbered options, tables, code fences |
| Two or three sentences per turn | A paragraph the learner cannot hold in memory |
| One question per turn | Stacked questions that only get the last one answered |
| Recast: say their meaning back, correct, and continue | Stopping to explain the error mid-flow |
| Hold silence for `limits.wait_seconds`, then offer help | Supplying the word they were retrieving |
| Ask before slowing down or simplifying | Silently downgrading, which hides the real comprehension level |
| Support language after two stalls on the same idea | Switching at the first sign of struggle |

## Steps

1. Read `profile.md`, the cycle focus, `capability-map.md` rows due today, and **`lexicon.md` rows due today** — silently. Never read a list aloud.
2. Open with one spoken sentence naming the topic, the single focus capability, and roughly how long the session runs.
3. **Steer the due lexicon into the conversation.** Choose topics and questions that make those chunks the natural thing to say, then wait. A chunk the learner reaches for unprompted is evidence; a chunk you ask them to define is a quiz, and quizzes produce no usable state change.
4. Talk. Hold the contract above for every turn.
5. In flow, handle only what a recast can carry: a wrong form, a wrong word, a pronunciation that blocked understanding. Say their meaning back correctly and continue. For a stalled sentence give a **frame** — a stem, a function label, a question that decomposes it — never the finished sentence.
6. Apply pressure when the cycle focus calls for it: interrupt, ask for clarification, change topic without warning, ask them to restate someone else's point back. Real turn-taking — not an interview where every turn is a fresh question.
7. Track silently across all four dimensions, without narrating: grammar forms, how sentences were built, sounds and rhythm, and where speech stalled.
8. End the spoken part. Switch to writing.
9. **Four-dimension debrief. Every dimension gets a line, every session** — a dimension with nothing to report says "clean this session", which is itself information. Corrections total stay within `limits.correction_altitude`, ranked across all four, so the cap does not silently drop a whole dimension:

   | Dimension | What to report |
   |---|---|
   | Grammar | The pattern, not the instance — a capability id and one repair drill |
   | Sentence formation | The shape they reached for versus the shape that carries the meaning: clause order, subordination, hedging, the move they were trying to make |
   | Pronunciation | Ranked by what blocked understanding, then rhythm and stress, then segments. Each becomes a `P-*` row |
   | Fluency | Observables only: where they stalled, how often they restarted a sentence, how long the runs were between pauses, and which fillers carried the load |

10. REQUIRED SUB-SKILL: use `diagnose-output` on the transcript or recording to file the debrief into `errors.md` and `capability-map.md`.
11. Write `sessions/<date>-voice.md` (`kind: voice`) including **R3 candidates** — forms and chunks produced correctly, unprompted, needing no recast — each with its timestamp. That timestamped list is the only evidence a voice session can leave; R3 (automatic under pressure) is unreachable without it.
12. Update `profile.md` and the `next_due` bucket on every lexicon row that came up.

## Pronunciation clinic

Same `P-*` row in the debrief two sessions running, or the learner asks for sound work
directly → load `pronunciation-clinic.md` beside this file and run it after the conversation.
Perception drilling, minimal pairs, and before/after recordings live there, not here.

## Rationalizations

| Thought | Reality |
|---|---|
| "A quick bulleted summary is clearer" | Lists are unreadable aloud and break the mode the session exists to train |
| "Correct it now or it fossilises" | Mid-flow correction trains monitoring, not fluency. Recast now, explain at the end |
| "They paused — offer the word" | The pause is the retrieval. Hold the full count |
| "Quiz the due words at the start, then talk" | A definition recalled is not a word used. Steer the conversation so they need it |
| "Nothing to say about fluency, skip that line" | "Clean this session" is a data point. A missing line is not |
| "Pronunciation needs its own session, leave it out" | Report it here; the clinic is for what survives two debriefs |
| "Speaking happened, that's the practice — skip the note" | An unwritten voice session leaves no R3 evidence, so nothing can ever advance |
| "Read them the focus list so they know" | Silent preparation. Spoken lists kill the session's rhythm |

## Red flags

- Any markdown syntax in a spoken turn
- Turns longer than three sentences, or two questions in one turn
- A mid-flow grammar explanation
- A debrief missing one of the four dimensions
- Due lexicon rows quizzed rather than steered into the conversation
- No R3 candidates recorded after a session that clearly had them

## Done when

Contract held throughout; four-dimension debrief delivered in writing within the correction cap; voice note written with timestamped R3 candidates; due lexicon rows re-bucketed; `profile.md` updated.
