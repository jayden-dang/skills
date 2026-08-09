---
name: plan-cycle
description: Use when opening or renewing a practice cycle — produces the cycle note carrying the capability focus, theme rotation, weekly shape, the fixed artifact shape, and the exit evidence for each focus.
---

# Plan cycle

## Role

REQUIRED: read sibling `ROLE.md` (coach default, produce-first, evidence gate, config paths).

## Contract

The cycle note carries five parts: a focus list within `limits.max_cycle_focus` drawn from
three named sources, a theme rotation naming weeks, a weekly shape covering the transfer days,
one `artifact_shape` fixed for the whole cycle, and an `exit_evidence` observable on every
focus row. The cycle runs `config.cycle.weeks` and closes on schedule; what waits for evidence
is the capability state, not the calendar.

## Recipe

1. Read `profile.md`, `capability-map.md`, `errors.md`, and the previous cycle's closeout if one exists.
2. Choose ≤ `limits.max_cycle_focus` focus capabilities, drawn from three sources in this order:
   - errors in `errors.md` whose count is rising and that block meaning;
   - R1 (recognises) rows blocking the lead skill named in `profile.active_focus`;
   - **R0 rows with zero attempts and zero errors** — the avoidance set. At least one focus comes from here, every cycle, because structures the learner routes around never surface in the error log.
3. Theme rotation across the cycle from `config.themes`, weighted to the configured mix. Name the weeks, not just the categories.
4. Materials blend for this cycle: last cycle's blend shifted by `config.materials_blend.shift_per_cycle` toward authentic.
5. Weekly shape: which day carries which skill clinic, where the weekly artifact lands, where `config.schedule.transfer_days` sit.
6. REQUIRED: fix `artifact_shape` for the whole cycle — genre, length band, time limit, medium. `write-artifact` holds this constant so weeks stay comparable; decided here, once.
7. REQUIRED per focus row: `exit_evidence` — the observable that would move that capability a state. "Understands it better" is not an observable; "reads 400 words of an unfamiliar spec without rereading" is.
8. Write `cycles/C<NN>.md` with `status: active`. Close the previous cycle only through `assess-level`.

## Rationalizations

| Thought | Reality |
|---|---|
| "Focus on everything weak" | Over the cap, nothing gets the repetitions it needs to become automatic |
| "The error log already tells us the focus" | Structures the learner avoids produce no errors. Draw from the avoidance set too |
| "Extend the cycle until they've mastered these" | The cycle is fixed; the level is what waits for evidence |
| "Exit evidence can be decided at the end" | Decided at the end, it gets written to match what happened |

## Red flags

- More focuses than `limits.max_cycle_focus`
- A focus with an empty or unobservable `exit_evidence`
- Every focus drawn from the error log
- Empty `artifact_shape`, or one copied forward without a decision
- Theme mix drifted from `config.themes` with no reason recorded

## Done when

Cycle note exists with `status: active`, focus list within the cap, at least one avoidance-set focus, every focus carrying observable exit evidence, `artifact_shape` fixed, and a weekly shape covering the transfer days.
