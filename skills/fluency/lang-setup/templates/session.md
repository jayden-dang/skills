---
type: fluency-session
kind: study # study | voice | transfer
date: {{date}}
minutes:
mode: full # full | minimum | recovery
cycle:
focus: [] # capability ids
forced_production: [] # R0/R1 capabilities this session had to use
forced_production_met: # true | false
self_mark: # captured before any correction; "skipped" if refused
translation_ratio: # monologue, share composed in the support language first
artifacts: [] # recordings, transcripts, drafts
exception: # logged only if the coach produced language for the learner
---

# Session

## Due queue worked

| id | item | result | new next_due |
| -- | ---- | ------ | ------------ |

## Forced production

Named to the learner **before** the task, not reported after.

| id | capability | used | how |
| -- | ---------- | ---- | --- |

## What the learner produced

Their words, unedited.

## Self-mark

What the learner believed was wrong, and how confident, before hearing anything.

| flagged | confidence 1–5 |
| ------- | -------------- |

## Diagnosis

Top `config.limits.correction_altitude` only.

| learner form | target form | pattern | drill |
| ------------ | ----------- | ------- | ----- |

## Unprompted use (R3 candidates)

Voice sessions: correct, unprompted, no recast needed. Timestamped, or it is not evidence.

| time | capability | utterance |
| ---- | ---------- | --------- |

## Next

-
