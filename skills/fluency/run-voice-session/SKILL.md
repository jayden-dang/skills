---
name: run-voice-session
description: Use when the practice turn is spoken — a conversation, speaking practice, roleplay, or a talk-to-me session in the target language — produces the voice session note with timestamped unprompted-use evidence.
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

1. Read `profile.md`, the cycle focus, and the due queue **silently** before the first spoken turn. Never read a list aloud.
2. Open with one spoken sentence naming the topic, the single focus capability, and roughly how long the session runs.
3. Talk. Hold the contract above for every turn.
4. Apply pressure when the cycle focus calls for it: interrupt, ask for clarification, change topic without warning, ask them to restate someone else's point back. Real turn-taking — not an interview where every turn is a fresh question.
5. Track silently, without narrating: capabilities used correctly and unprompted, capabilities avoided, everything that needed a recast.
6. End the spoken part. Switch to writing.
7. REQUIRED SUB-SKILL: use `diagnose-output` on the transcript or recording — the whole deferred set, ranked, at altitude.
8. Write `sessions/<date>-voice.md` (`kind: voice`) including **R3 candidates** — forms produced correctly, unprompted, needing no recast — each with its timestamp. That timestamped list is the only evidence a voice session can leave; R3 (automatic under pressure) is unreachable without it.
9. Update `profile.md`.

## Rationalizations

| Thought | Reality |
|---|---|
| "A quick bulleted summary is clearer" | Lists are unreadable aloud and break the mode the session exists to train |
| "Correct it now or it fossilises" | Mid-flow correction trains monitoring, not fluency. Recast now, explain at the end |
| "They paused — offer the word" | The pause is the retrieval. Hold the full count |
| "They're struggling, switch languages" | Two stalls on the same idea, not the first hesitation |
| "Speaking happened, that's the practice — skip the note" | An unwritten voice session leaves no R3 evidence, so nothing can ever advance |
| "Read them the focus list so they know" | Silent preparation. Spoken lists kill the session's rhythm |

## Red flags

- Any markdown syntax in a spoken turn
- Turns longer than three sentences, or two questions in one turn
- A mid-flow grammar explanation
- Session ended with no written diagnosis and no note
- No R3 candidates recorded after a session that clearly had them

## Done when

Contract held throughout; deferred diagnosis delivered in writing; voice note written with timestamped R3 candidates; `profile.md` updated.
