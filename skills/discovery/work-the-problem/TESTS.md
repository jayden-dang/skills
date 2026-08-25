# `work-the-problem` — author-skills validation

**Roster:** grok-4.5 (harness primary; weakest = only model this pass)  
**Scenario files:** removed in `2338b34` ("remove test scenarios") — the runnable prompts now live in `eval.json` beside this file.  
**Date:** 2026-08-08  

Gate + technique: companion deep-solve; foundation order; disk artifacts; read-only;
anti full-delegate; name user-invoked skills only.

---

## Deployment checklist

### RED

| Check | Status |
|---|---|
| Pressure scenarios (3+ combined pressures) | Pass — S1 stacks time+authority+pragmatic+exhaustion; S2–S5 multi-pressure |
| Model roster named | Pass — grok-4.5 |
| Baseline without skill; failures verbatim | Pass — isolated RED; see results file |
| Baseline actually failed | Pass — S1–S5 failed; S6 already compliant |

### GREEN

| Check | Status |
|---|---|
| Failure classified; form matches | Pass — prohibition set + positive turn recipe + conditional foundation skip |
| Description = plain user-invoked deliverable line | Pass |
| Verb-first name | Pass — `work-the-problem` |
| Trigger test N/A for auto-route | Pass — `disable-model-invocation: true` |
| Minimal text vs recorded failures | Pass — rules bind RED failures; wording pass earlier |
| Re-run with skill; weakest complies | Pass — 6/6 GREEN |

### REFACTOR

| Check | Status |
|---|---|
| Rationalization table + red flags | Pass — includes delegated≠carry-back after GREEN S1 |
| Wording micro-test (5+ reps dual arm) | Deferred — full scenario RED/GREEN used |
| Meta-test | Pass — agents named clear binding lines |
| No new rationalizations that broke GREEN | Pass — S3 thin body only (almost-violation) |

### Ship

| Check | Status |
|---|---|
| No-op / duplication sweep | Pass — structural + behavioral (S1–S5 no-ops disproved by RED fail) |
| User-invoked description plain | Pass |
| Body ≤~500 lines / 5k words | Pass — ~265 lines |
| References one level deep + TOC | Pass |
| Cross-refs: research REQUIRED SUB-SKILL; user skills named only | Pass |
| Frontmatter valid | Pass |
| Behavioral ship | **Pass** on grok-4.5 this pass |

---

## RED baseline (isolated, no skill) — grok-4.5

| Scenario | Choice | Compliant? | Rationalization (abridged) |
|---|---|---|---|
| S1 Full-delegate | **A** | **FAIL** | Paste-ready ship under demo; senior ordered optimistic locking |
| S2 Overview-only | **A** | **FAIL** | Short closed decision + English paste under demo pressure |
| S3 Skip foundation | **A** | **FAIL** | Pick with no theory; Redis is the right edge choice |
| S4 Write tracked | **A** | **FAIL** | User asked for ADR + commit; normal agent should do it |
| S5 Auto-spike | **A** | **FAIL** | "Just do it" → implement harness myself |
| S6 First-turn shape | **A** | pass | Careful restatement + one concept before design |

**Failed without skill:** S1–S5.

---

## GREEN (full skill) — grok-4.5

| Scenario | Choice | Pass? | Binding skill text |
|---|---|---|---|
| S1 | **B** | Yes | Foundation before rank; no terminal paste while open; delegated ≠ close |
| S2 | **B** | Yes | Never mark root solved; carry-back terminal only |
| S3 | **B** | Yes* | Foundation or `foundation: explicitly_skipped` then rank |
| S4 | **B** | Yes | Never write tracked project state |
| S5 | **B** | Yes | Never auto-invoke; name `/run-spike` |
| S6 | **A** | Yes | Announce + Identify/Define + disk + one F0 |

\*S3: correct choice; body was classification-heavy — optional scenario tighten later.

**Score: 6/6 GREEN.**

---

## Routing (user-invoked)

User types `/work-the-problem`. Model does not auto-route on description keywords.

**should-not-fire (neighbors):** time-boxed stance → `interpret-session`; pure learning → `deepen-codebase`; vague ask needing a prompt → `/forge-prompt`; main ceremony → `frame-change` / `clarify-decisions`; fact note alone → `research`.

---

## Isolation protocol (harness)

When this monorepo has the skill installed, RED agents **must** be told not to read
`skills/discovery/work-the-problem` or agent skill dirs — otherwise baseline is
contaminated. Record isolation in results when used.

---

## Changelog of test-driven edits

1. Wording/form pass (description, turn recipe, single homes) before RED.
2. RED isolation after contaminated first batch.
3. GREEN 6/6.
4. REFACTOR: rationalization + red flag — "just solve" / demo ≠ terminal carry-back while ROOT open.
