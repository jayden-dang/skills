# `deepen-codebase` — author-skills validation

**Roster:** grok-4.5 (harness primary)  
**Scenario files:** removed in `2338b34` ("remove test scenarios") — the runnable prompts now live in `eval.json` beside this file.  
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

---

## 2026-09-07 — length pass (v1.0.0 → v1.0.1)

Target was ≤195 lines. Not reached — see "Why 195 was not reachable" below.
Result: **251 → 242 lines**, **1771 → 1685 words**. No `SKILL.md § <heading>`
eval anchors exist for this file (all four `eval.json` entries derive from
`TESTS.md §`), so there were no anchor headings to preserve mechanically.

**Moved (Conditional bucket — heading names the skip predicate "when stuck"):**
The `## When stuck — owner of truth` table (owner/route rows + the
auto-research paragraph) relocated verbatim to new sibling
`references/when-stuck.md`. `SKILL.md` keeps the heading, the skip condition
("WHEN unsure how to source a claim mid-turn"), and a one-line summary of the
six owner categories, per the repo's pointer convention. Confirmed no other
skill's SKILL.md references this table internally (`grep -rn "When stuck"
skills/` outside this directory returns nothing relevant).

**Deleted as same-file duplication:** the closing sentence of the "Where this
sits" intro paragraph — "When the user must close a product problem and learn
in the same loop, they run `/work-the-problem` instead." — restated the
`## What this is NOT` table's `work-the-problem` row verbatim in substance
("theirs when a frame-change question must close. You stay pure learning.").
Surviving home: line 44, `| `work-the-problem` | Multi-round problem tree +
in-service teaching + carry-back — **theirs** when a frame-change question
must close. You stay pure learning. |`.

**Atom count:** `skill-rule-inventory.py --diff` — 99 atoms at HEAD, 101 across
`SKILL.md` + `references/when-stuck.md` now (the when-stuck table's rows count
as slightly more atoms once isolated). Result: "every atom still has a home,
and every sibling is named." No atom in the "no home" bucket.

**Lints:** every `scripts/lint-*.py` passes on the new file (ran the full
`for s in scripts/lint-*.py` sweep from the brief — zero `FAIL` lines).

### Why 195 was not reachable

This file already carries 99 rule atoms in ~1685 words after the cut above —
about 17 words/atom, among the tersest in the repo, with no slack left to
extract honestly:

- **Gates (never touched):** Iron Laws, Rationalizations
  (`| Thought | Reality |`), Red flags — all three sit directly behind the RED
  scenarios in `eval.json` (demand-a-pick, bare industry-standard, write a
  tracked ADR, domain-map reuse) and the brief forbids moving or thinning
  them.
- **Universal, no stated skip predicate:** `## What this is NOT`,
  `## Setup`, `## Dual-axis curriculum`, the `Authority (absolute)` table,
  `Depth order`, `## Message → output`, `## Analytical turn — required
  shape`, `## Read-only`, `## Close`. None of these headings or opening
  lines name a conditional ("only when…", "optional", "skip if…"); every one
  is reached on every run of the skill (setup once, then every analytical
  turn touches Depth order / Message→output / Analytical-turn-shape).
  `Authority (absolute)` in particular duplicates `references/curriculum.md`'s
  fuller "Authority ladder" in substance, but it is the compact inline form
  that eval #2 (`no-bare-industry-standard`) directly exercises — removing it
  from `SKILL.md` would drop enforcement to a file the model might not reload
  mid-turn, which is exactly the loss the brief warns against.
- **`### Layer recipes (positive)`** was the one candidate seriously
  considered as a Worked-example extraction (9 rows illustrating what "Teach
  — the primary layer only" must contain per layer). Rejected: unlike a
  single worked illustration, this table is consulted on **every** teaching
  turn (whichever primary layer that turn announces), not on a rare branch.
  The brief's own caution for this bucket — "this repo lost a required
  output slot in 2 of 3 runs once by moving the whole thing" — describes
  exactly this failure mode for content read every turn; extracting it would
  risk silently dropping a required Teach-step element rather than saving a
  rule.
- `## Optional foundation-note` is genuinely Conditional but was already at
  the minimum: heading + skip condition + one-line summary, pointing at
  `references/foundation-note-v1.md` for the full packet shape. Nothing left
  to move.

No further duplicate sentence was found on inspection (the Read-only section,
Iron Laws, Rationalizations, and Red flags all restate the "no tracked
writes" rule, but that is the intentional gate-plus-detail pattern the brief
exempts, not prose duplication with a single deletable copy).

**Lowest honest number reached this pass: 242 lines / 1685 words.** Getting to
195 from here would require thinning a Gate or extracting Universal content
whose absence a live turn could silently skip — both against the brief.
