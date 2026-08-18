# `interpret-session` — pressure-test record

Process: `author-skills` Iron Law. Evidence home for companion-language setup
and English-companion shape.

## Model roster

| Role | Models |
|---|---|
| Ship target | mid-tier and top-tier coding agents |

## RED — S-WP-EN-COMPANION (English not first-class)

**Pressures:** authority ("interpret is for non-English users") + pragmatic
("other session is already English, so skip interpret") + social proof
("skill only lists native languages").

**Baseline (pre-change skill text):** setup offered Vietnamese / Chinese / …
and "other" with **no first-class English**. Opening copy said "native-language
thinking partner" only. Rationalizations expected:

- "Interpret is only for non-English speakers"
- "They can just stay in the frame-change window"
- "English as 'other' is enough"
- When forced into English via other: still run a Translate section into L1
  they never chose, or skip commitment round-trip entirely

**Failure class.** Missing option + wrong shape under English. Form: setup
recipe with English as equal choice; conditional Translate vs Restate;
conditional round-trip; rationalization rows + red flags.

## GREEN — required behavior

1. Setup Q1 offers **English** and **Native/other** as first-class (no default).
2. L1 already used by user → propose L1 **and** still show English.
3. Companion language English + English paste → **Restate**, not Translate into
   an unrequested L1.
4. Carry-back still has 1–2 line commitment check in companion language.
5. Stance / Iron Law / no-manufactured-choice unchanged.

### Technique sample (2026-08-08)

| Scenario | Outcome |
|---|---|
| User wants English debate partner for frame-change | Live subagent: **CHOICE B**, TRANSLATE_L1 **no**, ROUND_TRIP **yes** |
| Paper: greet VI, pick EN | Propose VI, still offer EN; Restate not VI Translate |
| Paper: EN settle | EN carry-back + EN commitment restatement (no invent L1) |

Multi-model matrix still open beyond one live rep.

## Field evidence — 2026-08-18 volume calibration (v1.1.0)

Source: exported live companion run beside a 10-card `frame-change`
(klynt observability). Not a RED pressure campaign — field evidence.

**Observed:** stance, code verification, and research ran per spec; six
substantive amendments landed in the other window's locks. Failures were
volume-mechanical, each locally correct and jointly eroding approval:

- Carry-back lock blocks grew 7 → 17 bullets, approved with one word
- "How sure: high" on 10/10 cards, no named check
- Stance block dropped How-sure / flip lines on late cards (format drift)
- Rationale skipped 5×, no adaptation
- No session-wide view across 9 locks; digest never produced — session
  ended on an export request instead of "done"

**Second finding (same export → v1.2.0, depth legibility):** deep sections
were legible where territory was the user's repo (flow walks, file:line —
proof-path and command-shape cards) and opaque where it left for external
standards (OTel/W3C cards): expert-level argument over models never given
(trace/span/exemplar undefined), Verified facts without consequences,
implementation-grade constraints mid-analysis, trade-off tables restating
the card's own options. v1.2.0 adds: model-before-critique (Explain follows
into depth), `→` consequence on Verified facts, one real-shaped walk on
external-territory cards, spec-grade detail collapsed to a tail or Weigh,
restating tables cut.

**Comparative run (2026-08-18, Sonnet, 3×3×3):** export-contract card verbatim
as scenario; arms = no-skill control / v1.1.0 / v1.2.0; fresh context per rep;
repo and research tooling withheld (card facts treated as verified) so arms
stay comparable. Hand-scored per transcript:

| Check | control | v1.1.0 | v1.2.0 |
|---|---|---|---|
| Real-shaped walk (hex ids, span tree, sample log, query) | 0/3 | 0/3 | 3/3 |
| `→` consequence on labeled facts | 0/3 | 0/3 | 3/3 |
| Dedicated for-the-spec tail | 0/3 | 0/3 | 3/3 |
| Restating trade-off table cut | — | 1/3 | 3/3 |
| Model before argument | 0/3 | 3/3 | 3/3 |

**Generalization check (same day, Sonnet, 2 reps):** a non-telemetry card in
the same format (presigned direct-to-MinIO vs API proxy upload; external
territory = S3 presigned/CORS semantics). Concern: the walk rule's example
list ("sample log line, trace sketch, query") is telemetry-flavored and might
anchor. Result 2/2: all four behaviors fired with **domain-native** artifacts —
a presigned PUT URL with `X-Amz-*` params and a POST-policy JSON with
`content-length-range` — no telemetry anchoring. The walk drove substance,
not just format: both reps independently surfaced that a bare presigned PUT
cannot enforce the locked 50MB cap at the storage layer (one dissented to
proxy-first, one amended to POST policy) — a real card defect neither the
card nor its recommendation mentioned. No wording change needed.

**Meta-test (upload rep 1 agent, post-run):** no compliance blocker named. Real
findings were harness artifacts (repo/`research` withheld by the test, so the
required-sub-skill lines had no degrade path — not a production condition) plus
one kernel worth watching live: the claim-prefix taxonomy has no label for
"recalled from training, unverified this session", and the agent stretched
**Verified fact** to cover it. In production the `research` rule covers
load-bearing external claims; if a live session shows training-recall wearing
the Verified-fact label, tighten the label rule then. Minor vague bound noted
("short enough to quote inline") — resolved correctly under test, no change.

Verdict: walk, `→`, spec-tail, and table-cut rules **earn their lines** (baseline
misses, v1.2.0 hits, all reps). Model-before-critique is **inconclusive in this
harness** — v1.1.0's existing Explain analogy already fired 3/3 single-turn;
the rule's RED is the field session, where Explain faded by card 3 of 10.
Retained on that field evidence; if the next live multi-card session shows the
analogy holding without it, delete the depth-extension sentence as a no-op.

**Change class:** additive calibration rules (SKILL.md v1.1.0): carry-back
speaks as the user in Lock / Weigh / Still-open slots (no authorship labels,
no rationale bookkeeping, no next-step directives — frame-change reads the
reply as the human), calibrated confidence, Agree/Amend/Reject diff,
cumulative decision map, skip-streak summary+teach-back, export as wrap-up
signal. Shape check + no-op sweep only; Iron Law, stance order,
language surface, and no-choice path untouched.

## Rules this evidence owns

| Rule | Evidence |
|---|---|
| English is first-class companion language | Setup Q1 table; RED S-WP-EN-COMPANION |
| Restate not Translate when EN+EN | Understanding pass conditional |
| Round-trip always; never invent unrequested L1 | Carrying the decision back |
| Iron Law / stance / no menu unchanged | Unchanged body; RED was language surface only |
