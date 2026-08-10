# Vault contract

Load this file at step 2 of `setup-fluency-os`, and run its check at the last step.

Contents: [Rule](#rule) · [Required config keys](#required-config-keys) ·
[Required columns and slots](#required-columns-and-slots) · [Value ranges](#value-ranges) ·
[The check](#the-check)

Every other skill in this pack reads the vault **by exact key path and exact column name**.
A key that is renamed — however sensibly — is a key no skill can find, and the skill then
does nothing rather than failing loudly. This file is the list those readers depend on.

## Rule

Copy the structure from the `templates/` folder beside `SKILL.md`. Fill in values; do not rename, re-nest,
re-unit, or drop keys. Adding keys is safe. Changing one is not.

Two failures seen in the field, both from writing the config freehand and reverse-engineering
names out of skill prose:

- `correction_rank` for `correction_altitude` — the cap became unreadable, so nothing enforced it.
- `forced_production_min: 10` for `forced_production: 3` — the reader wants a **count of
  capabilities**, not minutes. Interpreted literally it names ten structures per session.

## Required config keys

| key path | unit / shape |
| --- | --- |
| `languages.target` | name |
| `languages.support` | name |
| `schedule.session_shape` | string, e.g. `"2x60"` |
| `schedule.minimum_session_minutes` | minutes |
| `schedule.study_debt` | boolean |
| `schedule.recovery_gap_days` | days |
| `schedule.transfer_days` | list of weekdays |
| `pronunciation.accent_anchor` | name |
| `pronunciation.listening_accents` | list |
| `pronunciation.accent_erasure` | boolean |
| `themes` | map totalling 100 |
| `materials_blend.structured` / `.authentic` / `.shift_per_cycle` | points |
| `language_policy.practice` / `.explanation` / `.support_use` / `.support_drops_at` | enum / level label |
| `ai_policy.learner_produces_first` | boolean |
| `cycle.weeks` | weeks |
| `cycle.benchmarks` | list, may be empty |
| `due_buckets` | list of days, e.g. `[1, 3, 7, 21, 60]` |
| `limits.max_cycle_focus` | **count** of capabilities |
| `limits.max_weekly_focus` | **count** of focuses |
| `limits.forced_production` | **count** of capabilities per session — not minutes |
| `limits.correction_altitude` | **count** of corrections per diagnosis |
| `limits.chunks_per_source` | **count** |
| `limits.lexicon_live` | **count** of live rows |
| `limits.errors_live` | **count** of open rows |
| `limits.wait_seconds` | seconds of silence held in voice |

## Required columns and slots

| file | must contain |
| --- | --- |
| `capability-map.md` | the movement-rules block, and columns `state`, `evidence`, `next_due` |
| `lexicon.md` | columns `function`, `state`, `study note`, `my sentence`, `next_due` |
| `errors.md` | columns `count`, `last_seen`, `next_due`, `status` |
| `profile.md` | `last_session`, `streak`, `active_focus`, and tables for `calibration_gap` and `translation_ratio` |

`profile.md`'s two metric tables are not optional decoration: `diagnose-output` appends the
calibration row and `run-session` appends the translation ratio every session. Without them
the pack's only two evidence-free progress signals have nowhere to go.

Every ledger carries YAML frontmatter. The skills address fields such as
`profile.last_session` and `profile.active_focus` as fields, not as prose.

## Value ranges

A correct name holding a wrong number is the failure the name check cannot see, and it is the
same mistake one step later: `forced_production_min: 10` was a rename *and* a unit error. The
rename is caught above. These bounds catch the unit.

| key | must be | why this bound |
| --- | --- | --- |
| `languages.target` ≠ `languages.support` | different | identical languages make the whole support policy a no-op |
| `themes` | children sum to 100 | a theme mix that does not total 100 silently reweights every cycle |
| `materials_blend.structured` + `.authentic` | 100 | same |
| `due_buckets` | ascending, all > 0 | a descending ladder reviews backwards |
| `cycle.weeks` | 4–26 | shorter cannot show a state change; longer stops being a cycle |
| `limits.forced_production` | 1–6 | a **count** of capabilities. Past six it is a checklist, not a session |
| `limits.correction_altitude` | 1–10 | above this it is a dump, which is the thing the cap exists to prevent |
| `limits.max_weekly_focus` | 1–5 | |
| `limits.max_cycle_focus` | 1–12 | |
| `limits.chunks_per_source` | 1–20 | |
| `limits.wait_seconds` | 3–30 | 0 removes the retrieval pause the voice contract is built on |
| `limits.lexicon_live` | 10–500 | |
| `limits.errors_live` | 10–200 | |
| `capability-map.md` | ≥100 rows, ≥20 in each of G/F/P | a floor that catches a stubbed map without dictating granularity |

The map floor is deliberately low. It is there to fail a map of twelve example rows, not to
set a target — completeness is judged against the learner's ceiling, not against a number.

## The check

Run this from the vault root before declaring setup finished. It is the completion criterion,
not a formality.

```bash
miss=0
val() { k=${1##*.}; grep -m1 -E "^[[:space:]]*${k}[[:space:]]*:" config.md | sed 's/[^:]*://; s/#.*//; s/["'"'"']//g; s/[[:space:]]//g'; }
rng() { v=$(val "$1"); case "$v" in ''|*[!0-9]*) echo "BAD VALUE     $1 = '$v' (want integer $2-$3)"; miss=$((miss+1)); return;; esac
  { [ "$v" -ge "$2" ] && [ "$v" -le "$3" ]; } || { echo "OUT OF RANGE  $1 = $v (want $2-$3)"; miss=$((miss+1)); }; }

# 1. config keys exist
for k in languages.target languages.support schedule.session_shape \
  schedule.minimum_session_minutes schedule.study_debt schedule.recovery_gap_days \
  schedule.transfer_days pronunciation.accent_anchor pronunciation.listening_accents \
  pronunciation.accent_erasure materials_blend language_policy ai_policy cycle.weeks \
  cycle.benchmarks due_buckets limits.max_cycle_focus limits.max_weekly_focus \
  limits.forced_production limits.correction_altitude limits.chunks_per_source \
  limits.lexicon_live limits.errors_live limits.wait_seconds themes; do
  grep -qE "^[[:space:]]*${k##*.}[[:space:]]*:" config.md || { echo "MISSING KEY   $k"; miss=$((miss+1)); }
done

# 2. table columns — must appear in a table row, not merely in prose
for pair in "capability-map.md:state" "capability-map.md:evidence" "capability-map.md:next_due" \
  "lexicon.md:function" "lexicon.md:state" "lexicon.md:study note" "lexicon.md:my sentence" \
  "lexicon.md:next_due" "errors.md:count" "errors.md:last_seen" "errors.md:next_due" \
  "errors.md:status"; do
  f=${pair%%:*}; c=${pair#*:}
  grep -qiE "^\|.*${c}" "$f" || { echo "MISSING COL   $f -> $c"; miss=$((miss+1)); }
done

# 3. profile fields
for c in last_session streak active_focus calibration_gap translation_ratio; do
  grep -qi -- "$c" profile.md || { echo "MISSING FIELD profile.md -> $c"; miss=$((miss+1)); }
done

# 4. frontmatter
for f in config.md profile.md errors.md lexicon.md capability-map.md; do
  head -1 "$f" | grep -q '^---' || { echo "NO FRONTMATTER $f"; miss=$((miss+1)); }
done

# 5. values
[ "$(val languages.target)" != "$(val languages.support)" ] \
  || { echo "SAME LANGUAGE target and support are both '$(val languages.target)'"; miss=$((miss+1)); }
ts=$(awk '/^[[:space:]]*themes:/{f=1;next} f&&/^[a-z_]+:/{f=0} f{gsub(/#.*/,"");if(match($0,/:[[:space:]]*[0-9]+/))
  {split($0,a,":");s+=a[2]}} END{print s+0}' config.md)
[ "$ts" -eq 100 ] || { echo "THEMES SUM    $ts (want 100)"; miss=$((miss+1)); }
ms=$(( $(val structured) + $(val authentic) ))
[ "$ms" -eq 100 ] || { echo "BLEND SUM     $ms (want 100)"; miss=$((miss+1)); }
grep -m1 -E "^[[:space:]]*due_buckets[[:space:]]*:" config.md | sed 's/.*\[//; s/\].*//' | tr ',' '\n' \
  | tr -d ' ' | awk 'NF{if($1+0<=0||(NR>1&&$1+0<=p))bad=1; p=$1+0} END{exit bad?1:0}' \
  || { echo "DUE BUCKETS   not ascending or not all > 0"; miss=$((miss+1)); }
rng cycle.weeks 4 26;            rng forced_production 1 6
rng correction_altitude 1 10;    rng max_weekly_focus 1 5
rng max_cycle_focus 1 12;        rng chunks_per_source 1 20
rng wait_seconds 3 30;           rng lexicon_live 10 500
rng errors_live 10 200

# 6. capability-map floor
tot=$(grep -cE '^\| [GFP]-' capability-map.md)
[ "$tot" -ge 100 ] || { echo "MAP TOO SMALL $tot rows (want >= 100)"; miss=$((miss+1)); }
for g in G F P; do
  n=$(grep -cE "^\| $g-" capability-map.md)
  [ "$n" -ge 20 ] || { echo "MAP THIN      $g has $n rows (want >= 20)"; miss=$((miss+1)); }
done

echo "checked 25 keys + 12 columns + 5 fields + 5 frontmatter + 13 values + map floor -- misses: $miss"
```

**Rule on the output:** `misses: 0` and setup is done. Any other number means the vault is
wired wrong; fix the named items and re-run. Do not report the vault as ready on a partial
pass, and do not resolve a miss by editing this contract.
