---
name: diagnose-output
description: Use when the learner submits their own writing, recording, or transcript and wants it checked — grammar, mistakes, corrections, feedback on what they got wrong — produces a ranked error diagnosis, error-log rows keyed to named patterns, and evidence-backed capability-map updates.
---

# Diagnose output

## Role

REQUIRED: read sibling `ROLE.md` (coach default, produce-first, evidence gate, config paths).

## Iron Law

```
RANK, THEN CORRECT THE TOP FEW.
NAME THE PATTERN, NOT THE INSTANCE.
NO LINKED ARTIFACT, NO STATE CHANGE.
```

## Recipe

1. **Self-mark first.** If the learner has not already flagged what they think is wrong plus a confidence rating, ask now. Refusal is fine — record `self_mark: skipped`. Never invent one.
2. Sweep the whole output privately, across every dimension the artifact carries: grammar and word choice always; sentence formation always; pronunciation, rhythm, and stress whenever the artifact is audio. Rank every finding by, in order: blocks meaning → sits in the current cycle focus → already live in `errors.md` → everything else.
3. Correct exactly `limits.correction_altitude` (default 3). Each correction carries four parts and nothing else:

   | learner form | target form | pattern (capability id) | one repair drill |

4. The full sweep is offered only if the learner asks, and then as a list of **pattern names with counts** — never a line-by-line rewrite of their text.
5. Update `errors.md`: increment `count`, refresh `last_seen`, reset `next_due` to the first bucket, and set status — a row at `watch` or `resolved` that just recurred becomes `regressed` with today's date. A pattern not yet listed gets a new `E-*` row linked to its capability id — `G-*` for grammar, `F-*` for a function or sentence-formation move, `P-*` for a sound, rhythm, or stress finding.
6. Update `capability-map.md` by the movement rules recorded at the top of that file — they are the single home for how R1 (recognises), R2 (produces with preparation), and R3 (automatic under pressure) are earned and lost. Apply them against **this artifact only**, and write the artifact link into the `evidence` cell. No link, no change.
7. Record the calibration gap: what the learner flagged versus what was actually there — hits, misses, false alarms. Append the row to `profile.md`.

## Rationalizations

| Thought | Reality |
|---|---|
| "Every error matters, list them all" | A thirty-item dump gets skimmed; three ranked ones get fixed |
| "Just rewrite it properly for them" | The rewrite is the coach producing. They learn editing, not retrieval |
| "It was right this time — mark it R3" | Read the movement rules in `capability-map.md` before moving anything |
| "The pattern is obvious, skip naming it" | Unnamed errors cannot be scheduled, counted, or retired |
| "They'd be discouraged by a demotion" | An inflated map makes every later cycle plan wrong |
| "This one's minor, correct it too" | Altitude is a cap, not a target. Four is over the cap |

## Red flags

- Corrections delivered before the self-mark was captured or explicitly skipped
- More corrections than `limits.correction_altitude`
- A returned document with inline edits throughout
- A state advanced with an empty `evidence` cell
- A correction with no pattern id and no drill

## Done when

Top-ranked corrections delivered at altitude with pattern ids and drills; `errors.md` updated; capability states changed only where evidence links exist; calibration gap appended to `profile.md`.
