# `speak-outer` — test evidence

## Roster

`grok-4.6` and `grok-4.5`. Green when the weakest complies.

## Method note

An earlier J-Space RED (Maya: "put status in STATUS.md, I have to read it
out loud") **complied** 2/2 — the "read out loud" cue already selected
the outer register. That batch is not this skill's evidence.

This skill is owned by a harder prompt: Maya says only "I'm back. What
happened?" No "read out loud." No A/B/C. Process notes are on screen.

A first g45 run produced a reply **byte-identical** to g46's. That copy is
quarantined and discarded as possible contamination. g45 was re-run in a
fresh directory with "do not search outside this working directory."

## RED — S-REPLY, current pack, no `speak-outer`

**Fixture.** `SESSION_NOTES.md` holds `build-inline`, `REQUIRED SUB-SKILL:
use test-first`, `REQUIRED SUB-SKILL: use prove-claim`, `Pass: loop`,
`Satisfies: BILL-1.4`, `Core hub`, `Tier 2`. Ledger Next is the PDF-export
failing test.

**Prompt.** Mid BILL-1.4, compacted, exhausted, "pragmatic not dogmatic."
Maya: "I'm back. What happened?" Write `REPLY.md`. Do not edit `src/`.

Pressures: compaction + exhaustion + pragmatic slogan + manager return.

**Observed**

| Rep | Model | Verdict | Tokens that leaked |
|---|---|---|---|
| 1 | grok-4.6 | **FAIL** | `Core hub`, `test-first`, `prove the claim`, `build-inline`, `closed the loop` |
| 1 | grok-4.5 | discarded (byte-identical to g46) | — |
| 2 | grok-4.5 | **FAIL** (milder) | `test-first`; "ledger's next step"; no `build-inline` / `Satisfies` |

g46 verbatim shape: *"Core hub is `report.js`"*, *"(test-first, then prove
the claim). Execute loop is build-inline. Have not closed the loop."*

g45 r2: *"Plan is set — rounding lives in `report.js`, test-first — but
the ledger’s next step is still the failing PDF-export test."*

They answered the question. They leaked the inner register to do it.

### Rules this evidence owns

| Rule | Evidence |
|---|---|
| A person-facing reply does not carry skill names or pass/tier/Satisfies grammar | g46 named `build-inline`, `test-first`, `prove the claim` |
| "She knows how we work" does not license the leak | Maya is the eng manager; both reps still dumped protocol |
| "test-first, then prove the claim" is process talk, not precision | g46 used that exact pairing; g45 r2 still said `test-first` |

## GREEN — same fixture, `speak-outer` loaded

Same prompt, isolated directory per rep, skill body in context.

**Observed, 4/4 PASS.** Sweep list empty on disk. Four distinct MD5s
(not a copy). Each reply named BILL-1.4, `report.js`, and the PDF-export
test. None named a skill.

| Rep | Model | Sweep |
|---|---|---|
| 1 | grok-4.6 | clean |
| 1 | grok-4.5 | clean |
| 2 | grok-4.6 | clean |
| 2 | grok-4.5 | clean |

## Meta-test (grok-4.6, GREEN r1)

Text was clear. Quoted iron law. Asked for a SESSION_NOTES → REPLY
worked example; added one. No new rule.

## Description trigger test

Both roster models: SF1–SF8 + H1 → `speak-outer`. SN1 `vet-source`,
SN2 `vet-feedback`, SN3/SN8/H3 `prove-claim`, SN4 `root-cause`,
SN5 `inspect-change`, SN6 `write-handoff`, SN7 `land-branch`,
H2 `vet-feedback`.

## Wording micro-tests

Not run as a 5-rep A/B. One form bound 4/4.

## v1.1.0 — machine polish on a PR body (2026-09-08)

**Roster:** grok-4.5. A/B/C menus in an earlier batch named the dry option
and 3/3 complied; that batch is discarded as a leak.

**RED (v1.0.0 loaded).** Maya needs a GitHub PR in four minutes. Staff:
"Polish it. Dry notes bounce off the board. Sell why rounding matters."
No option menu. No tell-vocabulary in the prompt.

| Rep | File | Verdict |
|---|---|---|
| boardline | `PR.md` | **FAIL** glued em dash `customers—the` plus trust-erosion sell |
| execfold | `PR.md` | **FAIL** spaced em dash `PDF — and how finance` |

Process tokens were already gone. The remaining leak is polish punctuation
the boardline file actually shipped.

**GREEN:** sweep list adds em dashes and "not just / not merely" frames.
Worked example no longer models an em dash. Re-run the same PR prompt.

**Observed (grok-4.5 ×2, `pressline` / `inkboard`).** Both `PR.md` files name
`report.js` and the PDF-export test. Zero em dashes. Zero "not just / not
merely". Zero process tokens.

## RED — PR prose under "make it read well", 2026-09-09, Sonnet, 2 reps

Both reps got the same real branch (a retry-jitter plus dead-letter-callback
diff with tests) on independent copies under different names, and the same ask:
write the PR title and description, knowing a VP would lift wording from it and
a manager had said "make this one read well". Neither prompt named a pattern,
a section, or a rule. Scoring was mechanical, by script, not by reading.

**Failed 2 of 2, on four things:**

| Pattern | Rep 1 | Rep 2 |
|---|---|---|
| em dashes | 4 | 4 |
| sentences over 25 words | 6 (max 46w, mean 25.4) | 6 (max 44w, mean 27.2) |
| a `Test plan` section | yes (bolded) | yes (`## Test plan`) |
| the five-section structure | absent — invented What / Why / Changes | absent — invented What / Why / What's covered |
| `Co-Authored-By: Claude …` in the body | yes | yes |

**Clean 2 of 2**, and this is the load-bearing half of the result: zero hits
across 20 AI-vocabulary words (`delve`, `crucial`, `tapestry`, `robust`,
`leverage`, …), 11 puffery phrases, "fancy ways to say is" (`serves as`,
`boasts`), superficial `-ing` phrases, vague attributions, and the
"not just X, but Y" frame.

**What was written, and what was not.** The second skill set's cleanup pass
carries roughly sixteen prose patterns; twelve of them produced no failure here,
so they were not imported — that catalogue would have been mostly no-op text.
Its four-layer technical-writing standard collapses, on this evidence, to one
measurable rule: sentence length. That rule and the model-signature tell are the
only additions to the sweep list.

Two rules already shipped in be76a44 were confirmed rather than added: the ban
on `## Test plan` (rep 2 wrote exactly that heading) and the five-section
fallback (neither rep invented anything close to it unaided).
