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
9. **Run the check below** from the vault root and show its output. `misses: 0` and the cycle is open. Anything else means a later skill will read this note and find nothing — fix the named items and re-run.

## The check

A focus id that does not exist in `capability-map.md` costs a whole cycle silently: `run-session`
pulls nothing for it, and `review-practice-week` reports zero attempts on a row that was never
real. Nothing else in the pack catches that.

```bash
C=$(ls -1 cycles/C*.md | tail -1); miss=0
grep -q "^status: *active" "$C" || { echo "NO active status  $C"; miss=$((miss+1)); }
sed -n '/^artifact_shape:/,/^[a-z_]*:/p' "$C" | sed '1d;$d' | grep -qE '[a-z]+:.*[^[:space:]#]' \
  || grep -qE '^artifact_shape:[[:space:]]*[^[:space:]#]' "$C" \
  || { echo "EMPTY artifact_shape  $C"; miss=$((miss+1)); }
cap=$(grep -oE 'max_cycle_focus:[[:space:]]*[0-9]+' config.md | grep -oE '[0-9]+')
ids=$(grep -oE '\b[GFP]-[0-9]+\b' "$C" | sort -u); n=$(echo "$ids" | grep -c .)
[ "$n" -le "${cap:-8}" ] || { echo "OVER CAP  $n focuses > $cap"; miss=$((miss+1)); }
for id in $ids; do
  grep -qE "^\| ?$id ?\|" capability-map.md || { echo "DANGLING ID  $id not in capability-map.md"; miss=$((miss+1)); }
done
e=$(grep -E "^\| ?[GFP]-[0-9]+ ?\|" "$C" | awk -F'|' '{v=$(NF-1); gsub(/[[:space:]]/,"",v); if(v=="") c++} END{print c+0}')
[ "$e" -eq 0 ] || { echo "EMPTY exit evidence on $e focus row(s)"; miss=$((miss+1)); }
echo "checked status + artifact_shape + cap + $n ids + exit evidence -- misses: $miss"
```

**Rule on the output:** `misses: 0` or the cycle is not open. Never resolve a dangling id by
adding the row to `capability-map.md` after the fact — pick a focus that already exists, or
the map was not complete at setup and that is the real defect.

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
