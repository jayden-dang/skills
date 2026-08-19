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

