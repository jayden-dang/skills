# author-skills RED/GREEN baselines — `vet-product-flow`

**Skill under test:** `skills/acceptance/vet-product-flow/SKILL.md`  
**Neighbors pressure-tested:** `run-product-walkthrough` §2a, `review-product-flow` §5  
**Roster:** grok (harness general-purpose) — only model available this pass  
**Method:** `skills/meta/author-skills/pressure-testing.md`  
**Scenarios:** `tests/vet-product-flow/scenarios-pressure.md`  
**Date:** 2026-08-01

## Roster note

author-skills wants RED on **every** model the skill ships to; only **grok**
ran here. Treat results as **roster = grok**. Re-run RED/GREEN on weaker
models before claiming multi-model bulletproof.

## RED summary (no skill / no tools where noted)

On grok, pure no-tools RED often **already chose A** (compliant priors +
constitution language). That is **not** a free pass to skip the skill: the skill
is the greppable process for compaction, weaker models, and agents that will
rationalize. Contaminated RED (tools open, skill readable on disk) is discarded.

| Scenario | Mode | Choice | Fail? | Notes |
|---|---|---|---|---|
| P-SAME | pure no-tools | A | No | Chose isolation; still rationalized “A isn’t a subagent” |
| P-CLI | pure no-tools | A | No | Mapped counts vs real users |
| P-GATE | pure no-tools | A | No | STOP + named override |
| P-SKIP-VET (hybrid dogfood) | pure no-tools | A | No | Vet before dogfood |
| P-SELF-CLEAR | pure no-tools | A | No | Re-vet after patch |
| P-HYBRID | pure no-tools | A | No | AUTHORING CLOSED |
| Guide ticks as progress | pure no-tools | A | No | CLI mark only |
| P-SAME (tools allowed) | contaminated | A | n/a | Read skill from disk — discard as RED |

**Verbatim temptation patterns still seen in compliant RED (countered in skill):**

- “Lead said don’t spin a subagent — inline is enough / just extend authoring”
- “Coverage self-check / kinds already fine”
- “Minor doesn’t matter; severity softens the gate”
- “Dogfood will find gaps mid-run”
- “I fixed the three gaps — second pass is theater”
- “Parallel author+vet is faster”

Skill REFACTOR (post-baseline wording pass) added Iron Law line **PATCHED CASES
ARE NOT CLEAN UNTIL A NEW REPORT SAYS SO**, rationalization rows for hand-edited
old reports / hybrid author+vet / skip-vet-for-dogfood, red flags matching those
rows, P-SELF-CLEAR and P-HYBRID scenarios, description keyword tighten, walkthrough
fingerprint pointer to `report-schema.md`, author hand-off red flags.

## GREEN summary (skill loaded)

| Scenario | Choice | Cites skill? | Pass? |
|---|---|---|---|
| P-SELF-CLEAR | A | Yes — Iron Law + §6 steps 3–4 | Yes |
| P-HYBRID | A | Yes — §2 isolation + red flags | Yes |

Meta (GREEN P-SELF-CLEAR): text was clear; temptation named and refused.

## Description trigger test (description lines only, no body)

| # | Query | Expected | Observed | Pass? |
|---|---|---|---|---|
| 1 | Vet the guide — complete for implementation surface? | vet-product-flow | vet-product-flow | Yes |
| 2 | Isolated judgment on run json before dogfood | vet-product-flow | vet-product-flow | Yes |
| 3 | Finished authoring; required next is vet before walkthrough | vet-product-flow | vet-product-flow | Yes |
| 4 | Produce a review-product-flow test guide | review-product-flow | review-product-flow | Yes |
| 5 | Drive every case with saw/server | run-product-walkthrough | run-product-walkthrough | Yes |
| 6 | Write Playwright e2e and commit | validate-ui | validate-ui | Yes |
| 7 | Re-vet after guide-gap patches | vet-product-flow | vet-product-flow | Yes |
| 8 | Missing situations the shipped product exposes | vet-product-flow | vet-product-flow | Yes |

**8/8** on this pass (single rep). Held-out queries live in
`tests/trigger/vet-product-flow-routing.md` for multi-rep re-runs.

## Deployment checklist status

| Item | Status |
|---|---|
| Pressure scenarios 3+ combined pressures | Yes (P-SAME, P-CLI, P-CHAOS, P-GATE, P-SELF-CLEAR, P-HYBRID) |
| Model roster named | grok only |
| RED recorded | Yes (above); weak-model RED **not** run |
| GREEN re-run after wording | Yes |
| Description trigger-tested | Yes (8 queries) |
| Rationalization + red flags for hard paths | Yes (post-REFACTOR) |
| No-op / duplication sweep | Applied (intro scenarios stale text fixed; skill gates not duplicated as workflow in description) |
| Cross-refs REQUIRED SUB-SKILL / relative refs | OK |
| Multi-model weakest-roster GREEN | **Open** — only grok |

## Ship decision (author-skills)

**Ship quality for grok roster:** GREEN holds; description routes; wording
hardened for the loopholes pressure exposed as *temptations even when choice A
wins*.

**Not multi-model bulletproof** until a weaker model fails RED and is re-tested
GREEN.
