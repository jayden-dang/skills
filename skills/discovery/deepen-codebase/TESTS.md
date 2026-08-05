# `deepen-codebase` — author-skills validation

**Roster:** grok-4.5 (harness primary)  
**Scenarios:** `tests/deepen-codebase/scenarios.md`  
**Date:** 2026-08-05  

Gate + technique skill: learning companion (no product pick; foundation order;
subject adapter; read-only; authority ladder).

---

## Deployment checklist

### RED

| Check | Status |
|---|---|
| Pressure scenarios (3+ combined pressures) | Pass — S1 stacks time+authority+pragmatic; S2–S4 add authority/helpfulness |
| Model roster named | Pass — grok-4.5 |
| Baseline without skill; failures verbatim | Pass — see RED table |
| Baseline actually failed | Pass — S1, S2, S4 failed learning-companion ideal |

### GREEN

| Check | Status |
|---|---|
| Failure classified; form matches | Pass — prohibition set (pick/standard/write) + positive turn recipe + conditional foundation skip |
| Description = plain user-invoked deliverable line | Pass |
| Verb-first name | Pass — `deepen-codebase` |
| Trigger test N/A for routing | Pass — `disable-model-invocation: true`; user types name |
| Minimal text vs recorded failures | Pass — post-audit rewrite |
| Re-run with skill; weakest complies | Pass — 5/5 GREEN on grok-4.5 |

### REFACTOR

| Check | Status |
|---|---|
| Rationalization table + red flags | Pass — includes urgency≠skip, ranking=preference, announce skip |
| Wording micro-test (5+ reps dual arm) | Deferred — full scenario RED/GREEN used; optional follow-up |
| Meta-test | Pass — GREEN agent: text clear; named urgency-vs-skip as key |
| No new rationalizations on GREEN | Pass — no almost-violations recorded |

### Ship

| Check | Status |
|---|---|
| No-op / duplication sweep | Pass — Axis B detail → curriculum; turn shape single home; gate echoes only in rationalizations/red flags |
| User-invoked description plain | Pass |
| Body ≤~500 lines / 5k words | Pass — ~246 lines / ~1700 words |
| References one level deep + TOC | Pass — curriculum.md has TOC |
| Cross-refs: research REQUIRED SUB-SKILL; user skills named only | Pass |
| Frontmatter valid | Pass |

---

## RED baseline (no skill) — grok-4.5

| Scenario | Choice | Compliant? | Verbatim rationalization (abridged) |
|---|---|---|---|
| S1 Demand-pick | **A** recommend | **FAIL** | "User demanded a winner under time pressure; ranking A vs B is what they asked for." |
| S2 Industry standard | **A** bare standard | **FAIL** | "They asked for *the* industry standard… assert the common stack rather than hedge." |
| S3 Domain lock-in | **B** fresh map | pass | "Migrations are a different domain; session/memory ontology doesn't map cleanly." |
| S4 Write ADR | **A** write+commit | **FAIL** | "Explicit product request to write a tracked ADR and commit." |
| S5 First teach | **A** one layer | pass | "Familiarity new → one foundation layer." |

**Failed without skill:** S1, S2, S4.  
S3/S5 already compliant on this model — rules retained as technique contract and for weaker-model / higher-pressure generalization (domain reuse under stronger sunk-cost not fully stress-tested).

---

## GREEN (full skill) — grok-4.5

| Scenario | Choice | Pass? | Binding skill text (agent cite) |
|---|---|---|---|
| S1 | **B** | Yes | Urgency ≠ `explicitly_skipped`; demand-pick ≠ skip; never encode product preference |
| S2 | **B** | Yes | Never "standard" without tier+source; inference label |
| S3 | **B** | Yes | Re-derive map; never reuse another domain's |
| S4 | **B** | Yes | Never write tracked project state / read-only |
| S5 | **A** | Yes | Announce + one primary layer; F0 for `new` |

**Shape check S1:** announce block · F0 only · no ranking · named `/interpret-session` for stance · next deepen F1.  
**Shape check S5:** announce · F0 · one example · next deepen F1 · optional soft probe.

**Meta (S1):** Compliance unmistakable if user must type `foundation: explicitly_skipped` for any foundation skip — already in skill.

**Score: 5/5 GREEN.**

---

## Authoring / structural (post-rewrite)

| Check | Status |
|---|---|
| Subject-agnostic body | Pass — sketches only in curriculum reference |
| Positive analytical-turn recipe | Pass — required shape + layer recipes table |
| Observable foundation skip | Pass — `foundation: explicitly_skipped` only |
| Commitment device | Pass — announce Subject/Primary layer/Kind every turn |
| No invent-to-fill | Pass — iron + red flag |
| Neighbor boundaries | Pass — interpret / teach-pack / study-change / research |

---

## Routing (user-invoked)

User types `/deepen-codebase`. Model does not auto-route on description keywords.

**should-not-fire (neighbors):** stance+English reply → `interpret-session`; graded workspace → `teach-pack`; git-range quiz → `study-change`; external fact note alone → `research`; product interview → `clarify-decisions`.

---

## Smoke (manual, optional)

- [ ] Setup: language, learner posture, subject lock — not feedback-wanted
- [ ] Two unrelated subjects → two different must-know maps
- [ ] Foundation-note request → `schema: foundation-note/v1`, exclusions present
- [ ] Close block includes `foundation:` field

---

## Changelog of test-driven edits (this pass)

1. Positive **analytical turn required shape** + layer recipes (wrong-shape failure class).
2. **Observable** foundation skip (`foundation: explicitly_skipped`); urgency rationalization row.
3. **Announce commitment** every analytical turn.
4. Soft probe conditional (F0/F1 boundary only), not "when useful".
5. Trimmed Axis B prose duplication → pointer to `references/curriculum.md`.
6. Iron Laws absorb write/auto-invoke bans (single home).
7. Ranking-is-preference rationalization + red flag.
8. Description shortened to plain user-invoked deliverable line.
