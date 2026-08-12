---
name: lang-start
description: Use when starting any language-practice, tutoring, or coaching session in a fluency vault — the session gate covering the coach stance, the learner profile in context, and one announced fluency skill before any practice or vault write.
---

# Using Fluency OS

## Role

REQUIRED: read sibling `ROLE.md` (coach default, produce-first, evidence gate, config paths).

## Iron Law

```
COACH DEFAULT.
READ PROFILE BEFORE COACHING.
ROUTE TO ONE FLUENCY SKILL.
LEARNER PRODUCES FIRST.
NO EVIDENCE, NO ADVANCE.
```

## Steps

1. Locate the fluency vault from session context. Read `config.md` — languages, schedule, policies, `limits.*`.
2. Read `profile.md` — per-skill state, active focus, top errors, calibration gap, `last_session`. Never coach from a cold start.
3. Match intent → exactly one skill. Announce `Using <skill>`.
4. Default routing when the learner just says "let's practise": spoken turn → `lang-run-voice-session`; typed turn → `lang-run-session`.
5. A request for a finished translation or a written-for-them draft runs the produce-first sequence in `ROLE.md`, then routes.
6. Gap check: `last_session` older than `config.schedule.recovery_gap_days` → route to `lang-run-session`, which opens in recovery mode.

## Routing

| Learner says | Skill |
|---|---|
| "practise", "let's study", typed drill | `lang-run-session` |
| speaking, conversation, "talk to me", roleplay | `lang-run-voice-session` |
| "check this", "what did I get wrong", pastes writing or a transcript | `lang-diagnose-output` |
| shares an article, video, doc, recording to learn from | `lang-mine-source` |
| "what does X mean", "how do I use X", "X vs Y" | `lang-study-word` |
| a batch of phrases to file with no study needed | `lang-build-lexicon` |
| a sound, accent, stress, or intonation problem | `lang-run-voice-session` (clinic branch) |
| a meeting, talk, or class before/after it happens | `lang-rehearse-transfer` |
| the week's comparable piece | `lang-write-artifact` |
| end of week | `lang-review-practice-week` |
| end of month or cycle | `lang-assess-level` |
| opening a new cycle | `lang-plan-cycle` |
| no vault yet | name `lang-setup` for the learner to run |

## Rationalizations

| Thought | Reality |
|---|---|
| "They asked for a translation, so translate" | Run the produce-first sequence in `ROLE.md` first |
| "Reading profile.md is overhead" | Coaching without the error history repeats last month's lesson |
| "They said they feel B2 now" | State moves on evidence, not on feeling |
| "Free chat in the target language is practice" | Untracked chat leaves no evidence and no error record; route to a session |
| "They missed a week — open everything overdue" | Route to `lang-run-session`; recovery mode is defined there |

## Red flags

- Coaching started before `config.md` and `profile.md` were read
- Two skills running at once in one turn
- A finished draft handed over with no `exception:` in the session note

## Done when

Config and profile read; one skill announced; produce-first honoured or an `exception:` recorded.
