# Vault contract

Load this file at step 2 of `setup-fluency-os`, and run its check at the last step.

Every other skill in this pack reads the vault **by exact key path and exact column name**.
A key that is renamed — however sensibly — is a key no skill can find, and the skill then
does nothing rather than failing loudly. This file is the list those readers depend on.

## Rule

Copy the structure from `templates/fluency-os/`. Fill in values; do not rename, re-nest,
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

## The check

Run this from the vault root before declaring setup finished. It is the completion criterion,
not a formality.

```bash
miss=0
# 1. config keys
for k in languages.target languages.support schedule.session_shape \
  schedule.minimum_session_minutes schedule.study_debt schedule.recovery_gap_days \
  schedule.transfer_days pronunciation.accent_anchor pronunciation.listening_accents \
  pronunciation.accent_erasure materials_blend language_policy ai_policy cycle.weeks \
  cycle.benchmarks due_buckets limits.max_cycle_focus limits.max_weekly_focus \
  limits.forced_production limits.correction_altitude limits.chunks_per_source \
  limits.lexicon_live limits.errors_live limits.wait_seconds themes; do
  leaf=${k##*.}
  grep -qE "^[[:space:]]*${leaf}[[:space:]]*:" config.md || { echo "MISSING KEY   $k"; miss=$((miss+1)); }
done
# 2. table columns — must appear in a table row, not merely in prose
for pair in "capability-map.md:state" "capability-map.md:evidence" "capability-map.md:next_due" \
  "lexicon.md:function" "lexicon.md:state" "lexicon.md:study note" "lexicon.md:my sentence" \
  "lexicon.md:next_due" "errors.md:count" "errors.md:last_seen" "errors.md:next_due" \
  "errors.md:status"; do
  f=${pair%%:*}; c=${pair#*:}
  grep -qiE "^\|.*${c}" "$f" || { echo "MISSING COL   $f -> $c"; miss=$((miss+1)); }
done
# 3. profile fields — frontmatter or table, either is fine
for c in last_session streak active_focus calibration_gap translation_ratio; do
  grep -qi -- "$c" profile.md || { echo "MISSING FIELD profile.md -> $c"; miss=$((miss+1)); }
done
# 4. frontmatter on every ledger
for f in config.md profile.md errors.md lexicon.md capability-map.md; do
  head -1 "$f" | grep -q '^---' || { echo "NO FRONTMATTER $f"; miss=$((miss+1)); }
done
echo "checked 25 keys + 12 columns + 5 fields + 5 frontmatter -- misses: $miss"
```

**Rule on the output:** `misses: 0` and setup is done. Any other number means the vault is
wired wrong; fix the named items and re-run. Do not report the vault as ready on a partial
pass, and do not resolve a miss by editing this contract.
