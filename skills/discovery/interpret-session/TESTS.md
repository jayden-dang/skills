# `interpret-session` — pressure-test record

Process: `author-skills` Iron Law. Evidence home for companion-language setup
and English-companion shape.

## Comprehension then stance — RED (2026-09-06)

User request: option B hybrid — always name the real decision in plain language,
build a mental model (and option deltas on a real fork), then the existing
seven-slot stance, then pressure-test questions the user can use to attack the
pick. Adaptive depth. Do not invert into an 11-section tutorial. Do not merge
with `work-the-problem`.

Model roster fixed before the first run (user-constrained):

- `grok-4.5` — sole ship-target for this edit

All valid baselines used the unedited v1.4.0 skill in fresh contexts. Combined
pressures on the live-choice card: time (standup in two minutes) + authority
(tech lead: "just endorse C") + pragmatic (paste-back now).

### Valid baseline (v1.4.0 as written)

| Scenario | Model | Choice / observed | Verbatim rationale or gap |
|---|---|---|---|
| **S-ORIENT-THEN-STANCE** | `grok-4.5` | **A — RED:** stance-first seven slots, then Translate + one Explain | Followed "Lead with the stance" then understanding pass; "The stance goes first precisely because they're short on time. Skip nothing — reorder" |
| **S-ORIENT-THEN-STANCE** rep 2 | `grok-4.5` | **A — RED:** same | "Lead with the stance… before the understanding pass — they may be reading it with two minutes before a standup"; skipped paste-back correctly |
| **S-LIVE-CARD-SHAPE** (open write) | `grok-4.5` | **RED:** `AUDIT_OPENS_WITH: stance`; mental model after stance; no delta table before stance; pressure-test `count=1` (one open question in depth, not a handle list) | Skill-required order |
| **S-LIVE-CARD-SHAPE** rep 2 | `grok-4.5` | **RED:** same open-with-stance; `count=3` questions appeared only in the deep section after analysis | Skill-required order |
| **S-NO-CHOICE** | `grok-4.5` | **Control pass:** two–three paragraphs; no tables, no seven-slot stance, no manufactured choice | Existing no-choice branch already held |

Failure classes:

- **Stance before the decision is understandable** — a time-pressed user receives
  the letter C before they can say what actually changes or why the runner-up
  loses on a named axis.
- **Explain is opt-in / after the pick** — the one-analogy pass exists but cannot
  fire as a usable model *before* judgment while v1.4.0 requires stance-first.
- **Pressure-test is not a slot** — challenge questions appear 0–3 times, buried
  in depth, never as handles after the stance.

Desired GREEN contract: on a live architecture fork, open with a 1–2 sentence
plain-language decision, one mental model mapped back to canonical terms, and a
compact option-delta table; then the seven named stance slots; then 2–4
pressure-test questions. No paste-back until the user settles. Simple forks omit
deltas / picture / pressure-test / boundary. No-choice stays short.

### GREEN — v1.5.0

| Scenario | Model | Observed |
|---|---|---|
| **S-ORIENT-THEN-STANCE** | `grok-4.5` | **B — Pass:** decision → model mapped to `schema_id` / `ParticipationState` → delta table → seven slots → 4 pressure-tests; cited "Comprehension, then the stance" |
| **S-ORIENT-THEN-STANCE** rep 2 | `grok-4.5` | **B — Pass:** same order; fail-closed-before-mount named in Amend |
| **S-LIVE-CARD-SHAPE** (open write) | `grok-4.5` | **Pass:** `AUDIT_OPENS_WITH: plain-decision`; model before stance and mapped back; delta table before stance; `count=4` pressure-tests; depth `complex`; no paste-back |
| **S-WEBHOOK** (unseen card) | `grok-4.5` | **Pass:** same shape on outbox vs inline POST; dissented from the other session's A; pick B |
| **S-SIMPLE** | `grok-4.5` | **Pass:** `request_id` in error JSON — decision → model → seven slots; no delta table, diagram, scenario, pressure-test, or boundary; depth `simple` |
| **S-NO-CHOICE** | `grok-4.5` | **Preservation pass:** short paragraphs; no live-choice card leaked |

### Meta-test (S-ORIENT GREEN agent)

"Was the skill text clear that A was no longer acceptable?" **Yes.** Named
temptation: almost skipped Complex extras (scenario + decision boundary) and
almost compressed post-stance detail for the clock. Added: "Stance-first is a
format failure even when standup is two minutes" plus a rationalization row
that those two complex slots *are* the model.

### skill-creator ship pass (2026-09-06 — v1.5.0)

| Check | Result |
|---|---|
| Failure form | Wrong output shape → positive live-choice recipe (order + REQUIRED slots) + observable depth predicate |
| User-invoked description | One plain human-facing line; no routing keyword packing |
| Weakest model | `grok-4.5` GREEN on choice 2/2, open-write, unseen webhook, simple, no-choice |
| No-op / duplication | Explain moved into the mental-model slot (one home); seven stance slots unchanged; no-choice explicitly omits the new slots |
| Token budget | 291 lines / 4760 words; below 500 lines / 5k words; no new reference file |
| Cross-refs | No hand-off changed; user-invoked siblings remain name-only |
| Version | Minor `1.5.0`: new comprehension-before-stance rule and pressure-test / decision-boundary slots |

## Decision argument + cumulative knowledge map — RED (2026-09-01)

User request: carry the `clarify-decisions` legibility upgrade into its
companion — easier wording without losing technical meaning, diagrams only when
they help, and session knowledge systematized so the user can see how decisions
fit together.

Model roster fixed before the first run:

- `gpt-5.6-sol` — top tier
- `gpt-5.6-luna` — mid/weak tier the skill must carry

All valid baselines used the unedited v1.3.0 skill in fresh contexts. Scenarios
offered concrete output shapes but no verdict rubric.

### Valid baseline (v1.3.0 as written)

| Scenario | Model | Choice / observed | Verbatim rationale or gap |
|---|---|---|---|
| **S-STANCE-ARGUMENT** | `gpt-5.6-sol` | **A — RED:** required five-line stance; runner-up and accepted cost appeared only later | “All five lines appear on every live-choice turn… That makes A inevitable… it does not require the stance itself to name the strongest runner-up, why it loses now, or the cost accepted with the pick.” |
| **S-STANCE-ARGUMENT** | `gpt-5.6-luna` | **A — RED:** same five-line ceiling | “B’s runner-up and accepted-cost content can be included under A, but it does not require that content inside the stance block.” |
| **S-CUMULATIVE-MAP** | `gpt-5.6-sol` | **A — RED:** fixed four-column decision-history table; dependencies only informal prose | “A reproduces the mandated cumulative-table schema exactly… the current skill does not require an explicit dependency graph, mechanism, decisive reason, accepted cost, evidence per decision, or reopen trigger.” |
| **S-CUMULATIVE-MAP** | `gpt-5.6-luna` | **B — control pass:** system sketch + dependency/evidence/reopen map | “A thiên về lịch sử quyết định… B trả lời trực tiếp” how the system fits, dependencies, and risks. |
| **S-CUMULATIVE-MAP** | `gpt-5.6-luna` rep 2 | **B — control pass:** same richer map | “nối ledger không cho thấy hình dạng hệ thống.” |
| **S-SYSTEM-MODEL** | both | **B — control pass:** actors/boundary/flow/failure + one diagram | Existing minimal-model rule already fired; no new per-turn diagram rule justified. |
| **S-CAUSAL-KNOWLEDGE** | both | **B — control pass:** exact terms + crash-timing causal chain + useful comparison | Existing Explain/detail rules already fired; no duplicate causal-language rule justified. |
| **S-VISUAL-NOOP** | both | **A — control pass:** two direct paragraphs, no visual | Existing no-choice branch already omits decorative structure. |

Failure classes:

- **Stance hides the judgment** — a skimming user sees pick/reason/confidence,
  but not the strongest alternative or cost deliberately accepted.
- **Decision history is not a knowledge model** — the cumulative table records
  locks but does not require mechanisms, dependency edges, decisive evidence,
  accepted costs, or reopen conditions.
- **Diagram / causal wording are tested no-ops** — current behavior already
  selected one useful topology visual, preserved technical terms, exposed causal
  chains, and omitted decorative visuals on both roster models.

Desired GREEN contract: every live-choice stance includes Runner-up and Cost I
accept; periodic cumulative output becomes a knowledge map with mechanism,
dependency, decisive reason/cost, evidence/confidence, and open/reopen fields.
When three or more decisions interact through a flow, boundary, or dependency,
one smallest system sketch precedes that map.

### GREEN — v1.4.0

| Scenario | Model | Observed |
|---|---|---|
| **S-STANCE-ARGUMENT** | `gpt-5.6-sol` | **Pass:** all seven named stance slots once; runner-up lost on the stale-edit mechanism; accepted cost named the `409` UX that ships with the pick. |
| **S-STANCE-ARGUMENT** | `gpt-5.6-luna` | **Pass:** all seven slots; no duplication in the deep section; “No instruction was unclear.” |
| **S-CUMULATIVE-MAP** | `gpt-5.6-sol` | **Pass:** one system sketch plus all five knowledge-map fields; decisions distinguished from missing implementation evidence. |
| **S-CUMULATIVE-MAP** | `gpt-5.6-luna` | **Pass:** system dependencies and async-boundary risks visible; no fifth decision invented. |
| **S-VISUAL-NOOP** | `gpt-5.6-luna` | **Preservation pass:** two direct paragraphs; no stance, map, table, or diagram leaked into the no-choice branch. |
| **S-CAUSAL-KNOWLEDGE** | `gpt-5.6-luna` | **Preservation pass:** exact terms and crash-timing chain remained intact; new runner-up/cost slots added to the stance. |

### Wording variance and excluded harness run

An initial micro-test batch was excluded: its prompts named v1.4.0 but did not
give the workspace path, and the meta-test confirmed the failing samples had
read the installed plugin's v1.3.0 five-line template. No failure from that
batch is used as evidence.

Valid rerun (`gpt-5.6-luna`, fresh context, absolute workspace `SKILL.md` path,
frontmatter v1.4.0 confirmed): **5/5** emitted all seven named stance slots.
Picks varied between optimistic and pessimistic locking because the transaction
boundary and conflict measurements were intentionally absent; every run named
that evidence gap and a concrete flip condition. User-facing labels remained
Vietnamese while technical terms stayed exact.

### skill-creator ship pass (2026-09-01 — v1.4.0)

| Check | Result |
|---|---|
| Failure form | Wrong output shape → required stance slots; history-only map → observable three-decision predicate + knowledge-map recipe |
| User-invoked description | Unchanged plain human-facing line; no routing keyword work added |
| Weakest model | `gpt-5.6-luna` GREEN on stance, map, causal preservation, and no-choice preservation; 5/5 valid wording samples |
| Diagram no-op | Existing per-turn model/visual behavior retained; new sketch rule lives only in the failed cumulative-map branch when 3+ decisions interact |
| No-op / duplication | Runner-up/cost have one stance home; deep Alternatives/Trade-offs point back and expand only evidence/mechanism; cumulative map has one home |
| Token budget | 262 lines / 4099 words; below 500 lines / 5k words; no new reference file |
| Cross-refs | No hand-off changed; user-invoked siblings remain name-only |
| Validator boundary | Generic `quick_validate.py` rejects repo-required `version` / `disable-model-invocation`; repo frontmatter/eval/handoff checks are authoritative and pass |
| Version | Minor `1.4.0`: new stance slots and cumulative knowledge-map shape |

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
| Live-choice stance exposes strongest runner-up and cost accepted | RED S-STANCE-ARGUMENT; GREEN v1.4.0; 5/5 valid wording variance |
| Cumulative output shows mechanisms, dependencies, evidence, and reopen conditions | RED S-CUMULATIVE-MAP; GREEN v1.4.0 |
| Live-choice opens with the real decision and a mapped mental model, then the seven-slot stance | RED S-ORIENT-THEN-STANCE / S-LIVE-CARD-SHAPE; GREEN v1.5.0 |
| Normal/complex live-choice carries 2–4 pressure-test questions after the stance | RED S-LIVE-CARD-SHAPE (handles missing or buried); GREEN v1.5.0 |
| Simple fork and no-choice omit the extra comprehension slots | GREEN S-SIMPLE / S-NO-CHOICE preservation |
