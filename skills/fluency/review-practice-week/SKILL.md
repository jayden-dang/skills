---
name: review-practice-week
description: Use in the weekly review slot of a fluency vault — produces the weekly review note carrying session counts, error trends split from avoidance, capability movement with evidence, metric trends, and next week's focus ids.
---

# Review practice week

## Role

REQUIRED: read sibling `ROLE.md` (coach default, produce-first, evidence gate, config paths).

## Contract

Every number in the note comes from a file that was opened this run: session counts from
`sessions/`, error movement from `errors.md`, state changes from `capability-map.md`, metric
trends from `profile.md`. Next week's focuses are ids, capped at `limits.max_weekly_focus`.

## Steps

1. Open this week's `sessions/`, the weekly artifact, `errors.md`, `capability-map.md`, and `profile.md` before writing anything.
2. Session tally from those files: sessions run, minutes, minimum-session days, recovery days, missed days. Report the real number.
3. Weekly artifact present? If not, that is a finding — name why, and whether the shape held.
4. **Error trends**: which `E-*` rows grew, which went quiet, which are new. For every quiet row, check the sessions for whether the structure was *used at all*. Quiet with use = improving. Quiet with no use = **avoidance**, and it goes to the next cycle's avoidance set.
5. **Capability movement**: every row whose state changed this week, with its evidence link. A row that changed with an empty evidence cell is reverted here, and the revert is recorded.
6. Metrics: calibration-gap and translation-ratio trends from `profile.md`. Trend across weeks, not this week's number alone.
7. Cycle-focus check: any focus capability with zero attempts this week is being routed around — schedule forced production for it next week rather than restating it as a goal.
8. Next week: ≤ `limits.max_weekly_focus` focuses, each naming a specific capability id or error id. Not a skill name, not a theme.
9. Write `reviews/<year>-W<NN>.md`. Update `profile.md`. Retire `errors.md` rows whose capability sits at R3 (automatic under pressure) with two clean weeks.

## Rationalizations

| Thought | Reality |
|---|---|
| "It felt like a good week" | Count the sessions and read the error log |
| "That error hasn't appeared — it's fixed" | Check whether the structure appeared at all. Silence is usually avoidance |
| "Roll the untouched focus over to next week" | Untouched twice means it is blocked or wrong. Say which, then change something |
| "Don't record the missed days" | Missed days are the input to the recovery rule; hidden, the rule never fires |
| "The state change is obviously right, leave it" | Evidence or revert |
| "Set next week's focus by what feels weakest" | The error log and the map already know |

## Red flags

- Session counts stated without opening the session notes
- Quiet error rows marked improving with no usage check
- A state change left standing with an empty evidence cell
- More than `limits.max_weekly_focus` focuses, or a focus naming a skill instead of an id

## Done when

Weekly note written with counted sessions, artifact status, error trends split from avoidance, capability movement each carrying evidence or reverted, metric trends, and ≤3 next-week focuses each naming an id; `profile.md` updated.
