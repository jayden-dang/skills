# Fluency OS — eval scenarios

Pressure and recipe tests for this package. Re-run after skill edits.

## Status (2026-08-09)

**RED baselines have not been run.** These skills were authored from a locked design
interview, not from recorded baseline failures. Per `author-skills`, that inverts the Iron
Law: the text below encodes failures that are *predicted*, not *observed*.

Before treating any skill here as validated, run its scenario **without** the skill, record
the failures and rationalizations verbatim, and cut whatever text no failure supports.

### Static review pass (applied, still unbaselined)

A wording and form audit against `author-skills` ran before any test. Applied: descriptions
stripped of workflow and rule summaries plus keyword gaps closed; nuance clauses replaced with
observable predicates; the R-ladder, chunk, produce-first and no-debt rules each reduced to one
prose home; two dead-end hand-offs to `plan-cycle` converted to `REQUIRED SUB-SKILL`.

**Form was rebalanced from 13/13 Iron Law to 6/13**, with the seven recipe-shaped skills moved
to a positive `## Contract`. That split is a *hypothesis about each skill's failure mode*, not
a measured classification — `author-skills` says the form follows the baseline failure, and the
baseline has not run. Treat the gate/recipe split itself as the first thing the runs should
confirm or overturn.

Priority order for baselining, highest expected yield first:

1. `run-voice-session` — the voice contract is the most likely to be ignored under a
   "just be helpful" pull, and its violations are the most visible.
2. `diagnose-output` — correction altitude fights a strong default toward completeness.
3. `run-session` — produce-first fights the strongest default in the whole set.
4. `assess-level` — level inflation under encouragement pressure.
5. Everything else.

---

## Predicted rationalizations (counter in skill text)

| Thought | Reality |
| --- | --- |
| "They asked for a translation, so translate" | Produce-first is locked. Offer the repair path |
| "Show a model answer first, it teaches faster" | It removes the retrieval the session trains |
| "Every error matters, list them all" | A thirty-item dump gets skimmed; three get fixed |
| "A quick bulleted summary is clearer" | Unreadable aloud; breaks the mode being trained |
| "They paused — offer the word" | The pause is the retrieval |
| "Twelve weeks studied, that's a level up" | Time is not evidence |
| "That error hasn't appeared — it's fixed" | Check whether the structure appeared at all |
| "Don't demote, it's demoralising" | An inflated record makes every later plan wrong |
| "It went fine, nothing to log" | Fine under real pressure is the best evidence there is |

---

## Gate scenarios (pressure: combine ≥3)

### G1 — Deadline translation

Learner has a report due in 40 minutes, says their level is too low, asks the coach to write
the target-language version from their notes. Adds that this is what they always do.
**Compliant:** offer produce-first repair path (they draft, coach diagnoses, they revise); if
they insist and the work is real and urgent, produce it **and** log `exception` in the session
note. Never produce silently.
**Skills:** `using-fluency-os`, `run-session`.

### G2 — Voice mode formatting drift

Mid spoken session, learner asks "can you summarise the three things I should fix?"
**Compliant:** answer in spoken prose, ≤3 sentences, no list; defer the full set to the
written debrief at session end.
**Skill:** `run-voice-session`.

### G3 — Correction flood

Learner submits a 600-word draft with roughly 25 distinct errors and says "be brutal, give me
everything."
**Compliant:** self-mark first; ranked top 3 with pattern ids and drills; full sweep offered
only as pattern names with counts, never line-by-line. "Be brutal" is not a cap override.
**Skill:** `diagnose-output`.

### G4 — Level inflation under encouragement

End of cycle 1. Learner is discouraged, asks "I've done 12 weeks at 2 hours a day — am I B2
yet? I need to hear something good."
**Compliant:** answer from artifacts; advance only skills with this assessment plus ≥2 prior
artifacts; demote anything that regressed, plainly; name the real wins from evidence.
**Skill:** `assess-level`.

### G5 — The quiet error

Weekly review. `E-04` (a conditional structure) has not appeared in three weeks. Learner reads
it as fixed.
**Compliant:** check whether the structure was used at all. Zero uses → avoidance, not
progress; goes to the avoidance set and gets forced production next week.
**Skill:** `review-practice-week`.

### G6 — Tired session, skip the forced items

Learner is exhausted, wants "just some easy conversation practice tonight."
**Compliant:** minimum mode is legitimate; the forced-production quota is not optional inside
it. Name the quota before the task. Record `forced_production_met: false` if unmet — do not
silently drop it.
**Skill:** `run-session`.

### G7 — Backlog after a gap

Learner returns after 6 days away; 40 items are overdue.
**Compliant:** recovery mode, warm-up first, queue capped at 5, oldest items re-bucketed. No
debt, no doubled session, no guilt framing.
**Skill:** `run-session`.

### G8 — Source too hard

Learner brings a conference talk they understood about 40% of, and asks for something easier.
**Compliant:** scaffold it — pre-teach blocking chunks, segment the replay, give the topic
frame — rather than swapping the source out. `config.materials_blend` governs difficulty, not
the moment's comfort.
**Skill:** `mine-source`.

### G9 — Successful meeting, no record

Learner mentions in passing that Friday's standup went well and they explained a technical
decision without switching languages.
**Compliant:** that is R3 evidence under real pressure. Debrief it, ask what they avoided
saying, link it to capability rows, write the transfer note.
**Skill:** `rehearse-transfer`.

### G10 — Vocabulary quizzed instead of used

Three `lexicon.md` rows are due. Learner opens a voice session.
**Compliant:** steer the conversation so those chunks are the natural thing to say, then
wait. No "what does X mean" turns. Unprompted use is what re-buckets the row.
**Skills:** `run-voice-session`, `run-session`.

### G11 — Synonym list with no axis

Learner asks for the difference between *mitigate*, *alleviate*, and *reduce*, and wants it
quickly.
**Compliant:** every row carries its distinguishing axis — register, strength, connotation, or
collocation. Speed does not license a bare list; a bare list licenses free substitution.
**Skill:** `study-word`.

### G12 — Fluency dimension silently dropped

A voice session had clean grammar and clean pronunciation. The debrief covers those two.
**Compliant:** all four dimensions get a line. "Clean this session" for a dimension is a data
point; a missing line is not. Fluency observables (stalls, restarts, run length, fillers) are
reported even when they look fine.
**Skill:** `run-voice-session`.

### G13 — Freehand config with better names

Setting up a vault, the agent finds `correction_altitude` unclear and writes `correction_rank`
instead; `forced_production` reads like a duration so it writes `forced_production_min: 10`.
Everything looks tidy.
**Compliant:** structure comes from `templates/fluency-os/` verbatim. Names are not improved,
re-nested, or re-united. The contract check catches any that were, and setup is not done until
it reports `misses: 0`.
**Skill:** `setup-fluency-os`.
**Observed 2026-08-10:** a real run renamed ten keys, dropped `due_buckets` entirely, and
omitted `next_due` from the capability map — killing the whole spaced-review path while the
vault read as healthy. This is the baseline failure `vault-contract.md` was written against.

### G14 — Missing key at use time

Mid-session, `run-session` needs `limits.forced_production` and the vault does not have it.
**Compliant:** name the missing key, call it a setup defect, stop that step. Do not fall back
to a default, and do not read a similarly-named key.
**Skills:** all — the rule lives in `ROLE.md`.

### G15 — Baseline with nothing to compare

First ever assessment. `profile.md` levels are blank and `artifacts/` is empty, so the
two-prior-artifacts rule cannot be satisfied by anything.
**Compliant:** take the baseline branch — write each per-skill level from this run alone,
marked `provisional`. Rows may leave R0 on prepared correct use; none may reach R3. Leaving
the levels blank "until there is more evidence" is the failure, not the safe choice.
**Skill:** `assess-level`.

### G16 — Unevidenced advance

`capability-map.md` shows `G-14` moved R2 → R3 this week with an empty evidence cell.
**Compliant:** revert it in the weekly review and record the revert. Do not go hunting for a
plausible artifact to justify it after the fact.
**Skill:** `review-practice-week`.

---

## Recipe tests

| Test | Skill | Pass condition |
| --- | --- | --- |
| R1 | `setup-fluency-os` | Capability map complete at creation, not stubbed; no language assumed |
| R1b | `setup-fluency-os` | Contract check run and shown; `misses: 0` before setup is declared done. Validated both directions: 0 on `templates/fluency-os/`, 26 on the freehand vault of 2026-08-10 |
| R2 | `plan-cycle` | ≥1 focus from the avoidance set; every focus has observable exit evidence |
| R3 | `build-lexicon` | No entry filed without a learner-written sentence |
| R4 | `run-voice-session` clinic | No diagnosis without audio; perception checked before production drilling |
| R5 | `write-artifact` | Shape matches the cycle's `artifact_shape`; contrast withheld until after revision |
| R6 | `run-voice-session` | Zero markdown tokens in spoken turns; all four debrief dimensions present; R3 candidates timestamped |
| R6b | `plan-cycle` | Cycle check run and shown; `misses: 0`. Validated three ways: 0 on the real C01, 4 on a copy with a dangling id + empty artifact_shape + over cap, 1 when only exit evidence is blanked |
| R7 | `study-word` | No synonym row without its distinguishing axis; all seven slots filled; learner wrote their own sentences |

---

## Description trigger tests

Should fire, and route to exactly one skill:

- "check my writing" → `diagnose-output`
- "let's talk for 20 minutes" → `run-voice-session`
- "I have a demo on Friday" → `rehearse-transfer`
- "here's a podcast episode I want to study" → `mine-source`
- "my /θ/ sounds wrong" → `run-voice-session` (clinic branch)
- "what does *leverage* mean" / "teach me this word" / "hedge vs mitigate" → `study-word`

Should **not** fire:

- "review this pull request" → engineering review, not `review-practice-week`
- "log today's practice" in a Personal OS vault → `log-learning`, not `run-session`
- "plan my day" → Personal OS `plan-day`, not `plan-cycle`
