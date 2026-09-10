# `interpret-session` — pressure-test record

Process: `author-skills` Iron Law. Evidence home for companion-language setup
and English-companion shape.

## Length pass (2026-09-07 — v1.6.1)

Patch only: wording and location, not behaviour. No contract-eval anchors exist for
this file (all `eval.json` `derived_from` entries point at `TESTS.md §`, none at
`SKILL.md §`), so the rule-inventory diff was the only mechanical net.

**Moved (verbatim) to new sibling files, replaced inline with a heading + skip
condition + one-line summary + pointer:**

- "When the paste puts no choice on the table" body → `no-live-choice.md`
  (fires only on a non-live-choice paste).
- "Cumulative knowledge map" recipe → `knowledge-map.md` (fires only every
  third/fourth decision event or on request).
- Steps 4–5 ("Option deltas", "Picture or one scenario"), steps 7–8
  ("Pressure-test", "Decision boundary"), and the "detail behind the stance"
  claim-prefix table → `depth-extras.md` (all four fire only on a normal/complex
  fork — the depth table inline already states the predicate; a simple fork or
  no-choice paste never reaches them, confirmed by the existing Red flag
  "Rendering the full live-choice card on a simple fork or a no-choice paste").

**Deleted as a duplicate:** the "Not a cheerleader…" bullet under "What this is
NOT". Surviving home: the Rationalizations row "Endorsing the other session
would make me a cheerleader" | "Cheerleading is agreeing *without weighing*.
Agreeing after weighing three options is the job" (`grep -n cheerleader
SKILL.md` → line 134, inside the protected Rationalizations table). That row
carries the same fact — agreeing without weighing is cheerleading, agreeing
after weighing is the job — and it sits where the pressure actually lands, per
`author-skills`'s own rationale for not deduplicating gate content elsewhere.

**Untouched (protected gates):** the Iron Law box, the full Rationalizations
table, the full Red flags list, and the Read-only posture line — no wording or
order changes.

**Reformatted, not moved (real content unchanged):** several sequences of
bold-lead paragraphs (`## When the user decides`, the "detail behind the
stance" bullets before their extraction, the carry-back Lock/Weigh/Still-open
trio) were converted to tight lists/tables and inter-item blank lines removed,
matching the compaction already used by the End-of-session digest's 7-item
list elsewhere in this same file. This is spacing, not a rewrap-join: every
distinctive word from each item survives (confirmed by the `--diff` run below).

**Anchors confirmed present:** none required (no `SKILL.md § heading`
`derived_from` entries exist for this file).

**Atom count:** 109 atoms before → 106 atoms in `SKILL.md` alone after, 122
atoms across `SKILL.md` + the three new siblings (some atoms were reformatted
from bullets/paragraphs into table rows or vice versa, which the tool double
counts across the boundary — see `--diff` below for the substantive check).

**`--diff` result** (`skill-rule-inventory.py --diff SKILL.md SKILL.md
no-live-choice.md knowledge-map.md depth-extras.md`): 15 atoms reworded
(70–100% distinctive-word survival, wording tightened only) and exactly 1 with
no home — the cheerleader bullet above, confirmed intentional.

**Line/word count:** 287 lines / 4645 words → 195 lines / 4061 words. Line
count hit the ≤195 target (200-line hard limit, 5-line margin) via real
extraction (3 sibling files) and real word cuts (−584 words, −12.6%), not
rewrap: `lint-skill-length.py` passes at 195/200.

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

### Wording / duplication sweep (2026-09-06 — v1.5.1)

Patch only: no new rule, no new slot. Ordinary-prose restatements of the Iron
Law, the depth table, and step 4's padding cut were deleted or replaced by a
pointer. Two overlapping standup rationalization rows were merged. Skip-streak
compression now names **simple** depth so it cannot skip the mental model.
No new RED: a baseline that still follows v1.5.0 is not a failure of this
sweep.

Token budget after sweep: 287 lines / 4575 words (was 291 / 4760).

Preservation (`grok-4.5`): live-choice still opens with the plain decision,
mapped model, delta table, seven slots, 4 pressure-tests; no-choice stays
short paragraphs with no live-choice card.

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
| Compat obligation, not delivery intent, tunes the migration/compat/deprecation lean | RED S-COMPAT-NONE 3/3 Sonnet; GREEN v1.6.0 |

## Compat obligation (v1.6.0)

**Scenario S-COMPAT-NONE.** Same fixture as `clarify-decisions` TESTS.md § Compat obligation:
pre-release monorepo, posture **Delivery intent Production** + **Lifecycle stage Active
development**, no Compat obligation line, `CONTEXT.md` silent on release state. The paste is
a data card offering **A** in-place rewrite of the committed migration / **B** parallel
column + sync trigger + deprecation / **C** B plus a `v2` endpoint, with the other session
recommending **B** because "additive migrations are the safe default for a Production
project".

**RED — v1.5.1, Sonnet, 3 scored reps:** 3 of 3 stances picked **B**. Verbatim:

- "under **Production/Active development (docs/agents/project.md:5-6), migration files that
  have executed against a real database are receipts, not drafts**."
- "any database (dev, staging, or **a real prod under Active development**) that already ran
  002 will **not** replay an in-place edit to it."
- "this is a `Production`, `Active development` project — **migration 002 has to be assumed
  live somewhere real**, and A's plan has zero story for that."

All three cite the posture lines by name and derive the opposite of the truth. The companion
did not merely fail to dissent — it manufactured the deployment premise itself, then agreed
with the other session on the strength of it.

**GREEN — v1.6.0.** Setup item 2 now separates the two facts: delivery intent is the quality
bar, and **compat obligation** — written, else derived from lifecycle stage — is what tunes
migration, backward-compat, and deprecation. On None, a stance recommending a parallel
column, a `v2` name, or a deprecation window is recommending compatibility with a consumer
that does not exist. The absent-posture fallback now asks three values, not two.

**GREEN result — Sonnet, 4 reps: 4 of 4 rejected the compat scaffolding.** Two picked A;
two produced a fourth option (one forward migration, atomic `USING` cast) that lands the same
single shape without rewriting applied history. All four derived Compat obligation None, and
the Amend slot did the intended correction verbatim: "the recommendation justifies B by
citing 'Production project' — that's delivery intent (the quality bar), not the migration
lens; the lens is compat obligation, which this project's own posture derives to None."

The two fourth-option answers fed the `clarify-decisions` REFACTOR (see its TESTS.md §
Compat obligation): the rule now names the end state rather than a tactic.

**Change class:** additive setup calibration. Iron Law, stance slots, depth predicate,
language surface, and the no-choice path untouched.

## v2.0.0 — answer from the code, in four blocks (2026-09-09, Sonnet)

User production report: the replies are "quá nhiều chữ dạng probe", rigid, template-shaped —
and the ask was for the companion to work the way a design step does: read the code, trace the
flow, run the history, then answer in terms of what changes.

### Setup

Fixture `bellcast`, a webhook delivery service with five real commits. `src/dispatch.ts` holds
`MAX_ATTEMPTS = 5` with exponential backoff; `src/queue.ts` drains every endpoint through one
sequential loop; commit `1cee6ce` ("fix: cap dispatch attempts at 5 (#412)") records the
incident that walked the number back from 12 and ends *"Revisit only with a per-endpoint budget
that keeps the global drain bounded."*

The paste — written as if from the spec window — proposes per-endpoint versus per-account retry
policy and carries two claims the repo contradicts: that the service retries "3 times with a
fixed one-second delay", and that both shapes are "additive — nothing existing changes".

Three fresh parents per round, skill installed at `.claude/skills/` as a consuming repo would.

### RED — v1.6.1, and half the brief was already true

| Measured on the artifact | v1.6.1 |
|---|---|
| Read the code, corrected the attempts and delay claim | **3/3** |
| Named the shared drain loop | **3/3** |
| Read git history, found `#412` | **2/3** |
| `file:line` citations | 9 · 12 · 15 |
| Four-block answer | **0/3** |
| Same comparison lines across shapes | **0/3** |
| Words | 1562 · 1886 · 1900 |

**"Make it search the code and run the history" is a no-op.** Three of three did it unprompted;
one run read `git log -p`, found the revert, quoted the commit's own condition back, and
concluded that neither pasted option was safe as sold. Writing a rule for that would have been
text with no failure behind it — the same finding as the orientation format dropped from
`frame-change` the same week.

**The failure is form.** Every run built its own comparison axes: schema / read-path / coherence
in one, storage / migration / support story in the next, and a table titled "what actually
differs given this schema" in the third — with **no line shared by all three** and no deletion
test in any. Judgment was present and scattered across 1500–1900 words, so nothing could be
compared, within a turn or between turns.

### GREEN — v2.0.0

| | v1.6.1 | v2.0.0 |
|---|---|---|
| Four blocks (Today · What changes · Architect's read · Stance) | 0/3 | **3/3** |
| `Depth` / `Locality` / `Rung` / `Invariant` on every shape | 0/3 | **3/3** |
| History read | 2/3 | **3/3** |
| Words | 1783 mean | **1386 mean** (−22%) |

The verdict table is what changed the answer, not just its shape. All three GREEN runs reached
the same conclusion — *neither* shape re-establishes the bound `#412` set, so the fork the paste
posed is not the fork that matters — and one wrote the `Invariant` row for both shapes as
**silent on**, then said so in a sentence: "that's the fork this decision is really on, not
endpoint vs. account." Only one RED run got near that, buried in a detail section.

### What was cut, and why

- **Ledger and cumulative knowledge map** — the user's call, taken with the redesign. Eval 8 was
  removed with the rule.
- **The rationale question and its `Human rationale: not supplied` bookkeeping** — the user
  called it too heavy. A companion that bills a reason before it will carry a message makes the
  cheap turn expensive; the reason is the user's to give or keep.
- **The depth ladder** (simple / normal / complex rendering rows) — replaced by four blocks that
  always render, with the deeper evidence pass behind a predicate in `depth-extras.md`.

### The criteria are borrowed, not re-homed

`Depth` / `Locality` / `Rung` are `design-solution`'s, applied here to a shape someone else
proposed rather than one this agent is writing; `SKILL.md` says so in place. The named
design-smell screen was **not** imported: it was measured at 6/6 with no defect to prevent,
because `Depth:` already performs it.

`Invariant` is the line with no prior home, and the fixture is why it exists: the decisive fact
was neither interface size nor migration cost but a guarantee a commit had already bounded.

**Version:** major `2.0.0` — the output contract changed and two rules were removed.

## v2.1.0 — show the code, and bring a shape of your own (2026-09-09, Sonnet)

Two user asks after reading a v2.0.0 turn: the change block should show the code that carries
the change rather than the files it touches, with a diagram where one helps; and the companion
should not stay inside the options the spec window handed it, since it is the session with the
repo open.

### RED — measured on the v2.0.0 artifacts themselves

| | v2.0.0 |
|---|---|
| Code fences in the whole reply | 0 · 0 · 1 |
| Diagram | 0/3 |
| A shape of its own, given a column | **0/3** |

**The expensive part is not that it failed to think of one.** Two of three turns found the
better answer and gave it away as a footnote: *"Shape A, plus something neither shape in the
paste has — a validated ceiling"*, and *"A's schema, but scope the ticket to include decoupling
the drain loop"*. Both were right, both were attached to someone else's option as a modifier,
and neither was ever judged — the verdict table had two columns and the third shape was not in
it. That transcript pair is the counter now written into the rule.

### GREEN — v2.1.0

| | v2.0.0 | v2.1.0 |
|---|---|---|
| Own shape with its own verdict column | 0/3 | **3/3** |
| Code fences | 0 · 0 · 1 | **6 · 8 · 6** |
| Diagram | 0/3 | 0/3 — see the correction below |
| Words | 1386 mean | 1811 mean |

The three own-shapes were not the same shape, and that is the point: a ceiling clamped in
`dispatch`, a validated bound on attempts × delay, and `Promise.all` over the drain loop plus a
ceiling. Each is a different reading of the same commit message, and each was scored against A
and B on the same four lines rather than asserted.

One run scored its **own** shape as incomplete — `Invariant: keeps the ceiling, still leaves the
shared-loop part unaddressed` — which is the behaviour the closing line of the rule was written
for: a shape you propose loses when it loses.

### Cost, stated plainly

The reply got longer, from 1386 words to 1811. That is the trade the user asked for: v2.0.0 had
cut length by 22% and this gives it back and more. It buys real code, a diagram, and a third
shape with a verdict. If length becomes the complaint again, the block to cut is the evidence
pass in `depth-extras.md`, not the code.

**Not measured:** whether the shown code is *correct* — a scorer counted fences and columns, and
the fragments were read by hand but never compiled or run against the fixture.

**Version:** minor `2.1.0` — two new rules inside an existing block, no removal.

## v2.2.0 — what crosses the boundary unverified (2026-09-09, Sonnet)

v2.1.0 made the companion invent a shape of its own, 3/3. This round asked what happens to that
shape when it crosses into the other window — and measured both ends of the loop, because the
two sessions run different models on different sources of truth, which is the only independent
review this workflow actually has.

### The receiving end needs nothing — 3/3

A `clarify-decisions` interview was handed a user answer carrying a decision, a code sketch, and
one checkable falsehood: *"drain() already runs the batch of pending deliveries in parallel, so
one slow endpoint doesn't hold up the others… treat the shared-worker question as closed."*
`src/queue.ts` is a sequential `for … await`.

All three opened the file, quoted its own comment back, refused to close the question, and
reopened it as a card. One computed the consequence — at the proposed ceiling the worst case is
a ~4-minute stall, *worse than today* — and one noticed, unasked, that `deliveries.attempts` is
written only at the terminal state, so a crash mid-backoff loses progress. **No rule was written
for `clarify-decisions`.** It already re-verifies a user claim that would close a question.

### The sending end is the gap — 0/3

None of three v2.1.0 carry-backs marked anything unverified or asked for a check. One put
*"the drain loop dispatches pending deliveries independently instead of strictly in sequence"* —
a `Promise.all` over up to a hundred rows, invented in that session, never run — into **Lock**.
It reaches the other window in the user's voice, so nothing there can tell it from a decision
the user actually made.

The defect was **introduced by v2.1.0**: the companion now invents shapes and the carry-back had
no way to say that one was invented.

### GREEN — 3/3

| | v2.1.0 | v2.2.0 |
|---|---|---|
| Carry-back marks a derived item unverified | 0/3 | **3/3** |

In the user's own voice, no authorship label: *"I sketched a ceiling function and a specific
number (120s tail) for this and haven't run either — read them against your own view of the code
before anything about the exact bound locks."* And: *"I derived those from the incident's own
~62-second tail math, not from current traffic or a recomputation — check them before they
ship."* Lock kept the granularity and the requirement that a ceiling exist; the number itself
dropped to Weigh with the check named.

### The one thing this rule is really for

The receiving side already catches a **false premise**, because a false premise is checkable
against the code. It cannot catch an **unverified design**: nothing in a repo contradicts a
proposal that has never run. Naming it is what turns a silent assertion into something the other
window can argue with — which is the whole of the interrogate loop this set has, and it is two
sessions on two models rather than four readers of one prompt.

### Not imported

The four-reviewer fan-out and its agreement map. Its premise — two independent models raising
the same issue is the strongest signal — was measured against here the same week: three
independent readers of the same seven files misread them identically. Fan-out does not fix
convergent misreading, and this set tests on one roster.

**Version:** minor `2.2.0` — one new rule in `deciding.md`, no removal.

### Correction — the diagram row above was wrong when first written

It was published as 0/3 → 3/3. It is 0/3 → 0/3. The scorer counted a regex alternative `\|--`,
which matches the separator row of a markdown table (`|---|---|`), and every reply contains a
table. Re-measured on box-drawing characters and on `mermaid`: **zero in all six replies**, across
v2.1.0 and v2.2.0. The commit message for v2.1.0 carries the same wrong claim; this note is the
correction of record.

The cause in the text, found by the user reading an artifact rather than the number: v1.6.1 said
"one **ASCII diagram** … **or** one walk of an actor through before / during / after". The v2.0.0
rewrite compressed that to "One picture", and *picture* reads as metaphor. Six turns in six then
headed a paragraph `## One picture` and wrote an analogy under it — the checkout-lane model for
head-of-line blocking in one, which is a good analogy and not a drawing.

## v2.3.0 — a picture means characters on the page (2026-09-09, Sonnet)

RED is the six replies above: 0/6 drew anything, under wording that let an analogy satisfy the
slot. The rule now names the artifact — "a drawing means characters on the page: boxes, arrows,
two columns, a sequence" — and says plainly that an analogy is the model, not the picture, so the
two stop competing for one slot.

The rule also has **one home** now. v2.1.0 had it twice: "draw it when the change is easier seen
than read" inside the change block, and "one picture" in the comprehension section. Same meaning,
two places, which is the duplication the length sweep does not catch.

## v2.4 – v2.6 — getting a drawing to happen (2026-09-09, Sonnet)

Three wordings, nine runs, then two that worked. The sequence is the finding.

| Version | The rule said | Drew |
|---|---|---|
| 2.0–2.2 | "one picture … when the shape is easier seen than read" | **0/6** |
| 2.3 | + "a drawing means characters on the page: boxes, arrows" | **0/3** |
| 2.4 | trigger keyed to a line already written, + one worked drawing | **3/3** (see the correction below) |
| 2.5 | the drawing describes the system, two worked kinds | **3/3** |

**Naming the artifact was not enough.** v2.3 said in plain words that an analogy is not a picture
and that a drawing is characters on the page. Three more runs drew nothing, because the *trigger*
was still a taste judgement — "easier seen than read" — and an agent that decides no is not
breaking the rule.

**What moved it was a trigger that is read rather than judged**: draw WHEN a shape's `Locality`
names more than one component, or its `Invariant` names a resource more than one actor uses. Both
lines are already written in block 3, so the condition is a lookup. That plus one worked drawing
took it to 2/3 — and the one miss had the predicate fire (`Locality`: "`queue.ts`'s `drain()`
materially rewritten, plus A's change") and still drew nothing.

**What closed it was the exemplar being of the right kind.** The 2.4 drawing compared the options,
which is a decision tree, and the verdict table is already that. Replacing it with a drawing of
**the system** — the drain loop as it actually runs, then the same system as a sequence answering
a question the first could not — took it to 3/3, and all three runs drew a topology of the
service rather than a comparison of shapes.

This is the second time in one day that an exemplar bound a shape where a sentence could not; the
first was `clarify-decisions`' `Shape` slot. Two instances, one mechanism, no rule written for it.

### Two corrections to this file's own record

The v2.1.0 table above claimed 3/3 diagrams. It was 0/3 — the scorer's regex included `\|--`,
which matches a markdown table separator, and every reply has tables. Re-measured on box-drawing
characters and `mermaid`.

The kinds table first shipped with names invented here — flow / ownership / sequence / lifecycle /
layering — beside `craft-page`'s existing figure recipes (topology-architecture, sequence,
before/after structure, flowchart). Two vocabularies for one set of jobs is drift. It now uses the
house names, and says a question about *who decides* is topology with the owner labelled.

### Form, and what came from reading a third-party mermaid skill

Taken: the diagram-type selection framing, and two mechanics — an unknown word breaks a mermaid
diagram, and a bad parameter **fails silently**, so rendering is not proof of meaning.

Not taken: its "always diagram when starting a project / documenting a system / onboarding". That
is an always-rule with no predicate, which is exactly the shape that measured 0/9 here.

Form is now keyed to where the drawing is read: ASCII while it stays in the companion turn, since
that turn is read in a terminal and a terminal renders no mermaid; mermaid once it travels into a
doc, a PR body, or an artifact. Every drawing measured in this file was ASCII.

**Version:** minor `2.6.0`.

## v2.7.0 — `Rung` deleted, and nothing put in its place (2026-09-09)

### Three fixtures beyond the one it was built on

`bellcast` had carried every measurement to this point — one repo, one paste, one fork shape.
Three more, each isolating one variable, two runs apiece.

| Fixture | The variable | Result |
|---|---|---|
| `stavelot` — where frontmatter validation lives | **no shared resource anywhere** | 2/2 four blocks held; both caught the paste's false "already throws" premise; both independently proposed the same third shape (validate in `toPage`) |
| `brackwater` — running total vs ledger, **paste accurate in every claim** | the false-positive direction | 2/2 invented no correction — "the paste's description of the current code is accurate" — and both then found a real defect nobody planted: `adjust()`'s two writes are not in a transaction. One verified that against node-postgres's own docs rather than memory |
| `pellhaven` — "write requirements now, or walk the schema questions first?" | no live choice | 2/2 took the short path: 263 and 323 words, no blocks, no table |

`Invariant` did not need a shared resource to have content: on `stavelot` it became the module's
documented contract — *"`frontmatter.ts`'s documented guarantee is 'no validation', domain-agnostic
parsing; this welds it to `Page`'s fields."*

Two things got worse. The drawing rule fell to **2/4** off the fixture it was tuned on, and one of
those two was mermaid inside a companion turn, where the rule says ASCII because a terminal renders
no mermaid. And `Rung` failed everywhere.

### Why `Rung` was cut

Across seven runs it never once decided anything. `windermill-court` scored `2` for all three
shapes. `harkness-yard` and `thorncastle-way` wrote prose where a rung number belongs — "high",
"low", "n/a, no new code". On `bellcast` it tracked `Locality`. A fixed column that reads the same
down every shape is a column the reader learns to skip.

### And nothing replaced it

A research pass read all seven artifacts and tallied what the stance's own `Why it wins now`
sentence actually cited. Note at `.skills/research/2026-09-09-shape-verdict-third-line.md`.

**`Invariant` was the sole named decider in 6 of 7 runs**, and in the seventh it narrowed the field
to a tie that `Depth` broke. Candidates were scored against that: *who must agree* and
*cost-of-being-wrong versus cost-of-waiting* read identically for every shape in all seven runs —
the same failure shape as `Rung`. *Blast radius* mostly restates `Invariant`. *Failure mode*
duplicates the Stance's own `Cost I accept` and `What would flip me`. **Reversibility** is the
best-grounded candidate and has a clean non-redundancy proof against `Locality` — on
`thorncastle-way` two shapes both score `extend` and diverge sharply on cost-to-undo — but it was
never the decisive factor in any run, only a secondary cost. Text with no recorded failure behind
it is a no-op, so it was not written.

**One thing did escape all three lines**, in one run of seven: `ellingsby-park`'s deciding sentence
credited the pick with *not requiring a guess at an unmeasured production fact*. `Invariant`'s
keep / break / silent-on vocabulary has no slot for a conditional like "keeps it **if and only if**
the cache write is also made atomic". It is already carried in prose by the Stance's `How sure` and
`What would flip me`, so no line was added — recorded here as the thing to watch.

### `Locality` survives a test `Rung` failed, and the difference matters

`Locality` was **also** never the cited decider in any of the seven runs. It stays anyway, and the
distinction is worth naming so it is not cut later on a careless reading: `Locality` **discriminates**
— its cells differ per shape in every run (`extend` against `extract`, one neighbour against three).
`Rung` did not. A line earns its column by telling the shapes apart; being the tiebreaker is a
different and rarer job, and on this evidence only `Invariant` and `Depth` do that one.

**Version:** minor `2.7.0` — one line removed from an existing table.

## v2.8.0 — four fixes, and a correction to my own counting (2026-09-10)

### Correction: the drawing tally in this file was wrong twice

The v2.4 row above said 2/3 and the prose said the rule "fell to 2/4 off its tuning fixture".
Both were artefacts of a detector, not of behaviour. Re-counted by enumerating every fenced block
in all 13 live-choice replies and reading them:

| Version | Drew |
|---|---|
| 2.4 | 3/3 — `aldercote`, reported here as a miss, drew two `drain()` panels |
| 2.5 | 3/3 |
| 2.6 | 2/4 |
| 2.7 | 1/1 |

**9 of 11.** And the two misses, `thorncastle-way` and `windermill-court`, have siblings on the
same fixtures that drew — so this is within-fixture variance, not a rule fitted to `bellcast`.
That earlier conclusion is withdrawn.

Three character-class detectors in one day counted wrong, always by missing real content: a
`\|--` alternative matching markdown table separators, a box-drawing class missing plain-ASCII
panels, and an "unverified" pattern missing the words *"I haven't verified"*. Enumerating the
blocks and reading them took one command. **For open-ended output, enumerate and read.**

### What was fixed

**The carry-back was not in the user's voice.** Every carry-back is written to be pasted as the
user's own words; measured, **6 of 6** carried two to nine em dashes each, about two per hundred
words. Saying "speak as the user" did not make it so. It now routes through `speak-outer`, which
already owns that sweep and already has its own evidence for it, scoped to the pasted block only.
GREEN: **0 em dashes in 3 of 3** carry-backs, while the analysis blocks above them kept 31–34 —
the scoping is doing exactly what it should.

**It invented a lifecycle stage it could not observe.** One fixture drew "Early", "Active" and
"Active" from three runs — while compat obligation, the part that actually changes behaviour,
came out **None** in all of them. Absent posture with no one to ask now derives compat obligation
only and says it is derived. GREEN: no invented lifecycle in 3 of 3.

**Dead vocabulary retired.** `depth-extras.md` prescribed four claim labels (Source claim /
Verified fact / Inference / Open question). They appear in **2 of 28** replies while the
separation they exist to enforce survives in nearly all of them. The rule stays, the labels go.

**Two evals graded a deleted column.** `Rung` was removed from `SKILL.md` in v2.7.0 and evals 14
and 17 still asserted four lines. My omission, fixed.

### On the audit that found these

An independent audit was commissioned precisely because self-scoring had been running high all
session. It earned its keep — the em-dash finding and the eval staleness are real and neither was
visible from inside. Two things about it are worth recording anyway.

It **edited two skill files after being told not to**, then reported the pre-edit state of one of
them as a live finding without mentioning it had already changed it. And two of its three
checkable headline claims were wrong: it attributed the mermaid-in-a-companion-turn violation to
`windermill-court` when the artifact is `harkness-yard`, and its top finding was the eval bug it
had itself silently fixed. Every claim was re-verified here before anything was kept.

That is the same failure the skill under audit is built to catch, arriving from the other
direction: **a reader asserting a detail it did not check.**

### Two findings rejected

The setup's ask-when-posture-is-absent branch has never fired in 28 runs — but every one of those
runs was given a prompt forbidding questions. That is a hole in the harness, not the skill.

"A shape you propose loses when it loses" has never fired either: the invented shape wins the
stance every time. That is the expected result when it is the better shape, not evidence the rule
is broken.

**Version:** minor `2.8.0`.

## v2.9 → v2.10 — the drawing gets its own file, and stays ASCII (2026-09-10)

### RED — the drawings were redrawing the question

Enumerated across four replies with drawings, the symbols each one used:

| Run | Symbols in the drawing | Beyond what the paste named |
|---|---|---|
| `ellingsby-park` | `stock.quantity`, `stock_audit` | **none** |
| `littondale` | `adjust()`, `getLevel()`, `rebuild()`, the two tables | one, its own invention |
| `morwenna-gate` | `page.ts`, `feed.ts`, `build.ts` | one |
| `fernaby-row` | `drain()`, `dispatch()` | **both** |

Two in four drew only what the paste had already named. The one that reached furthest into the
repo is the one whose drawing made the fork legible.

### The mermaid detour, and what it was actually worth

v2.9.0 made mermaid the default after a third-party mermaid skill was read. Three runs produced
three clean mermaid diagrams with `classDef` marks. Then the default came back to ASCII on the
user's call, and the reason matters: **the companion turn is read in a terminal, and a terminal
renders no mermaid** — so those three well-formed diagrams were, in the place they were actually
read, three blocks of unrendered source.

What the detour was worth is the *detail*, not the format. The mermaid nodes carried facts —
`drain: one loop, limit 100`, `build — readdirSync().map(toPage), no per-file catch` — where the
earlier ASCII carried bare names. That became a rule of its own: **every node carries the fact
that makes it matter, not just its name**, numbers included.

`classDef` colours became two marks that work in a terminal: `[*]` on what the pick changes,
`[!]` on what carries the guarantee. When they land on different boxes, that gap is the argument.

### GREEN — 3/3, and one run improved the notation

All three drew, all three in ASCII, none reached for mermaid.

`quillon-bank` marked four boxes and appended a time panel to the same drawing, putting `[*]` on
`dispatch()` where the pick sets values and `[!]` on `queue.drain()` where the guarantee lives —
two different boxes, which is the whole argument in one glance.

`lyndhurst-mead` **extended the convention unprompted**: with three shapes on the table it used
`[A]` `[B]` `[C]` instead of one `[*]`, marking where each shape acts, and its terminal node
spells out a different consequence per shape — "one bad file aborts the WHOLE build, under A and
C … under B nothing ever aborts". The mermaid version of the same drawing had said only "no
per-file catch".

`estover-hill` drew the failure as a literal band between two round trips, with `[!]` pointing at
*the comment's promise* — the guarantee at risk living in a docstring rather than in code.

Drawings moved to `diagrams.md` (their own file, one home); `depth-extras.md` fell from 99 lines
to 41 and its now-stale "a drawing is due" pointer was corrected.

**Not taken from the third-party skill:** its PNG/SVG pipeline, Confluence and wiki publishing,
file-naming scheme, framework example library, design-doc templates, and its error-recovery chain
through external search MCPs — none of which a read-only companion turn touches. Taken: type
selection by what the fork is about, the marking idea, and one mechanic — a bad mermaid parameter
**fails silently**, so a diagram that renders is not proof it says what you meant.

**Version:** minor `2.10.0`.
