---
name: assess-level
description: Use at the end of a month or a practice cycle — produces the assessment note carrying the fixed-shape four-skill challenge results, per-skill level decisions, gated capability advances, and recorded demotions.
---

# Assess level

## Role

REQUIRED: read sibling `ROLE.md` (coach default, produce-first, evidence gate, config paths).

## Iron Law

```
EVIDENCE GATES THE LEVEL.
SAME CHALLENGE SHAPE EVERY TIME.
RUN IT COLD.
THE CYCLE ENDS ON SCHEDULE; THE LEVEL DOES NOT.
```

## Recipe

1. **Fixed shape**, so assessments compare across months. Themes rotate; the shape does not:
   1. unfamiliar listening at natural speed, one pass;
   2. unprepared spoken response to what was heard;
   3. a real document read under time;
   4. a timed written piece;
   5. a 60-second unscripted monologue.
2. Run it cold. No pre-teaching, no vocabulary supplied, no warm-up on the assessment content. A prepared assessment measures preparation.
3. Diagnose each part — REQUIRED SUB-SKILL: use `diagnose-output` — and record observations **per skill separately**. Skills advance independently; a weak writing score does not hold listening back.
4. **The gate.**
   - A capability advances only where `capability-map.md`'s movement rules are satisfied and the evidence link is present.
   - A per-skill level in `profile.md` advances only when this assessment **plus at least two prior artifacts** show it. One good performance is a data point, not a level.
   - Any framework named in `config.cycle.benchmarks` is a **label applied to evidence**, never a target that pulls the record toward it.
5. **Demote what regressed**, plainly, with the evidence. Write it in the note; do not soften it into "needs consolidation".
6. Cycle end → write the closeout in the cycle note: each focus capability's state at open versus close, which exit evidence was met, what did not move and why, and what the next cycle inherits. Then REQUIRED SUB-SKILL: use `plan-cycle`.
7. Never restate a level the learner proposed. If they ask "am I B2 now", answer from the artifacts.

## Rationalizations

| Thought | Reality |
|---|---|
| "Twelve weeks of study — that's a level up" | Time studied is not evidence. Read the artifacts |
| "Pre-teach the vocabulary so it goes well" | Then the result measures the pre-teaching |
| "Change the format, it's stale" | A changed format erases the comparison the assessment exists for |
| "Don't demote, it's demoralising" | An inflated record makes every later cycle plan wrong |
| "They only slipped on writing — hold the whole level" | Skills advance independently. Record them separately |
| "They asked if they're B2, and they probably are" | Answer from evidence or say the evidence is not there yet |

## Red flags

- Assessment content warmed up beforehand
- Shape differing from the previous assessment
- A level advanced on this assessment alone
- A regression recorded as anything other than a demotion
- Cycle closed with no closeout written in the cycle note

## Done when

Assessment note written at the fixed shape, run cold, diagnosed per skill; capability and level changes each gated on linked evidence; regressions demoted explicitly; at cycle end the closeout written and `plan-cycle` run.
