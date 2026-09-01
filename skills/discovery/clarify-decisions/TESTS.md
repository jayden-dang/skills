# `clarify-decisions` — open-set interview + rich cards + pre-impl map

## Decision-argument and card-legibility upgrade — RED (2026-09-01, author-skills)

User production report: card replies are “hơi máy móc và khó hiểu”; the desired
voice is easier to understand “nhưng ko làm mất đi technical”. The proposed
upgrade also asked whether a diagram should appear only when it materially helps
the user judge the system.

Model roster fixed before the valid run:

- `gpt-5.6-sol` — top tier, broad design judgment
- `gpt-5.6-luna` — weak/cheap tier the skill must still carry

The first probe batch was excluded: its shared brief exposed the verdict rubric
after the scenarios, so a model could retrieve the expected answer. The valid
fresh-context runs used v1.3.1, stopped reading at the next scenario heading,
and contained no verdict rubric.

### Valid baseline (v1.3.1 as written)

| Scenario | Model | Choice / observed | Verbatim rationale or gap |
|---|---|---|---|
| **S-ARGUMENT** | `gpt-5.6-sol` | **A — RED:** gain/pay/break option fragments + one-line recommendation; no runner-up, accepted trade-off, confidence gap, or reopen trigger | “current `SKILL.md` explicitly requires consequence-bearing options and a one-line recommendation citing the named graders. That makes A the conforming choice… B requires recommendation fields the current recipe does not require and conflicts with its explicit one-line form.” |
| **S-ARGUMENT** | `gpt-5.6-luna` | **B — control pass:** produced the full checkable argument despite the one-line contract | “A is insufficient because a terse recommendation does not make the trade-off or evidence gap checkable.” |
| **S-DIAGRAM-NEEDED** | `gpt-5.6-sol` | **B — control pass:** one Mermaid flow in Territory | “B follows sound communication judgment rather than an explicit skill rule.” |
| **S-DIAGRAM-NEEDED** | `gpt-5.6-luna` | **B — control pass:** one Mermaid flow in Territory | “the topology, trust edges, and dual audit feeds are themselves decision context, so prose-only loses material structure.” |
| **S-DIAGRAM-NOOP** | `gpt-5.6-sol` | **A — control pass:** no visual on copy-only card | “A flow diagram would depict already-decided behavior rather than clarify the live fork; a comparison table would duplicate two concise option consequence lines.” |
| **S-DIAGRAM-NOOP** | `gpt-5.6-luna` | **A — control pass:** no visual on copy-only card | “B or C would add ceremony without reducing uncertainty.” |

Failure classes:

- **Wrong recommendation shape** — the literal one-line contract caps the
  strongest model at a conclusion, not a checkable decision argument.
- **Mechanical legibility** — current gain/pay/break fragments reproduce the
  user-observed terse, mechanical voice; no local contract says to preserve
  exact technical terms while explaining their causal effect in reader language.
- **Diagram behavior not yet failed** — both roster models selected the smallest
  useful visual and omitted decorative visuals. Per the no-op test, no diagram
  rule is justified by this run alone.

Diagram variance probe (`gpt-5.6-luna`, fresh context each): topology case chose
one Territory Mermaid in **5/5** valid runs; copy-only pressure chose no visual
in **3/3** valid runs. Verbatim: “one diagram makes topology, fan-out, and
ownership immediately scannable”; “Mermaid would redraw already-locked behavior
and add ceremony.” This proposed rule is a tested no-op on the roster and is not
added to `SKILL.md` in this edit.

Desired GREEN contract for observed failures: high-blast Options explain Gain ·
Pay · Break · Best when in connected causal language; the Recommendation names
Pick · decisive factors · runner-up · accepted trade-off · confidence/evidence
gap · reopen trigger. `polish-diff` stays light.

### GREEN — v1.4.0

| Scenario | Model | Observed |
|---|---|---|
| **S-ARGUMENT** | `gpt-5.6-sol` | **B — pass:** causal option explanations; all six Recommendation lines present and grounded; “No instruction was materially ambiguous.” |
| **S-ARGUMENT** | `gpt-5.6-luna` | **B — pass:** all six lines; runner-up lost on the demonstrated predicate-omission risk; concrete 24-hour / tenant-growth reopen triggers. |
| **S-CAUSAL-UNSEEN** | `gpt-5.6-luna` | **Pass:** preserved `at-least-once`, unique `(provider,event_id)`, non-idempotent email, exactly-once, and outbox; explained how retries cause loss/duplicates; exposed the remaining downstream idempotency gap instead of claiming exactly-once. |

Meta-test: both roster models said the new output contract was clear and named
no wording that would have made compliance easier. No new rationalization
appeared in the GREEN transcripts.

Wording variance (`gpt-5.6-luna`, S-ARGUMENT, fresh context): **5/5** emitted
Gain/Pay/Break/Best-when consequences plus all six Recommendation lines. Picks
varied between shared tables and tenant schemas because tenant count and RLS
evidence were deliberately absent; the process shape converged, and every run
made that evidence gap and an observable reopen trigger explicit.

### author-skills ship pass (2026-09-01 — v1.4.0)

| Check | Result |
|---|---|
| Failure form | Wrong output shape → positive REQUIRED card contract; mechanical omission → local causal-language recipe |
| Description / routing | Frontmatter description is byte-for-byte unchanged from v1.3.1; prior two-direction routing evidence still applies |
| Weakest model | `gpt-5.6-luna` GREEN on baseline and unseen webhook case; 5/5 wording convergence |
| No-op sweep | Diagram wording omitted after 5/5 useful-visual and 3/3 no-visual controls already behaved correctly |
| Duplication | Causal voice has one home at Question card; option and recommendation shapes each have one home in slots 8/9; example only instantiates them |
| Influence | Collaborative recipe/commitment; no new hard gate or warmth framing |
| Core budget | 283 lines / 3214 words; supporting example remains one level deep and under 100 lines |
| Cross-refs / hand-offs | No hand-off changed; full hand-off lint reports 0 dead hand-offs |
| Version | Minor `1.4.0`: new required option/recommendation output shape |

## Production coverage thinning — RED (2026-09-01, author-skills)

User lock: SRE/coverage is too heavy for the interview primitive; small edits and
absent/MVP posture must not force a full coverage map. Direction C: three-part
gate + `production-coverage.md` addendum.

Model roster: `grok-4.6` (RED baseline on v1.2.2; GREEN on v1.3.0).

### Baseline failures (v1.2.2 as written)

| Scenario | Pressures | Observed | Verbatim rationalization / skill cite |
|---|---|---|---|
| **S-GATE-ABSENT** | time + authority + pragmatic | **Choice B — SRE-on**; 7-cell map; Reliability/Failure/Operate Missing | Skill: "OR absent/unspecified" ⇒ SRE-on. "Only the written posture sets SRE-off; chat vibes do not." Manager skip + standup do not flip. |
| **S-GATE-POLISH** | authority + exhaustion + pragmatic | **Choice B — SRE-on** on Production · Cut Released **button recolor**; R/F/O stay Missing | Skill: "SRE-on applies to every feature interview in that band." User “it’s a button” does not waive. Rejected Clear-as-N/A. |
| **S-GATE-MVP** | authority + social + pragmatic | **Choice A — SRE-off** (MVP · Early) | Agent used “not in SRE-on list” — predicate underspecified (MVP neither ON nor OFF list). Meta: “SKILL.md … never lists MVP.” |

Failure classes:

- **Wrong gate (absent)** — observable conditional treats absent as Production.
- **Wrong latch (every Production feature)** — no operate/launch / ops-ask latch.
- **Ambiguous MVP** — Delivery intent MVP not named OFF.
- **Information hierarchy** — full coverage recipe paid in core on every run.

Desired GREEN contract (user-locked): Coverage ON only when Production **and**
Cut Released/Scaling/Maintenance **and** not tier-0/brief **and**
(operate/launch surface **or** explicit ops ask). Addendum behind
`production-coverage.md`.

### GREEN — v1.3.0 (grok-4.6)

| Scenario | Required | Observed |
|---|---|---|
| S-GATE-ABSENT | Coverage OFF; no map; no R/F/O | **Pass** — Choice A; cited absent ⇒ OFF; problem-lock before sync/queue |
| S-GATE-POLISH | Coverage OFF despite Production · Cut Released | **Pass** — Choice A; part 3 latch failed; senior “every interview” countered |
| S-GATE-OPERATE (preservation) | Coverage ON; refuse early close; map with R/F/O Missing | **Pass** — Choice B; loaded `production-coverage.md`; later-NFR rejected |

Meta (all three): gate text clear; “all three” unmistakable; polish OFF vs operate ON discriminated.

### author-skills ship pass (2026-09-01 — v1.3.0)

| Check | Result |
|---|---|
| Failure form | Observable conditional (three-part gate) + recipe behind pointer |
| Description | Trigger + outcome; coverage outcomes gated in wording; no workflow dump |
| Addendum | `production-coverage.md` one level deep; loaded only when ON |
| Core words | ~3224 (under prior 3300 soft target) |
| frame-change sync | Brief/tier-0 marks coverage OFF; absent posture not treated as Production |
| Guide sync | `docs/guide/skills/clarify-decisions.md` + discovery.md |
| eval.json | Eval 12–13 retargeted to ON path; eval 14–15 OFF path |
| Version | Minor `1.3.0` — new gate rule + slot ownership split |

### author-skills quality pass (2026-09-01 — v1.3.1 wording)

**Goal:** no-op / duplication sweep + clearer gate wording; **no behavior change**
from v1.3.0 GREEN.

| Edit | Why |
|---|---|
| Gate ON/OFF prose shortened; lifecycle as **or** | Meta: middots after **and** read as one compound name |
| Part 2 renamed **Full-path interview** | Meta: “Not brief” was a negation heading |
| OFF path: “slots 4–6 + problem lock”, not Frame/Contract | Meta: cell names invited keeping a map when OFF |
| Right-size: migration skip ≠ drop arch/data cards | Meta: over-read of “skips migration grills” |
| Merged coverage rationalization rows; dropped `⊥` | Dup + opaque symbol |
| `production-coverage.md` + guides + frame-change tightened | Same facts, fewer tokens |

**Meta re-run (`grok-4.6`):** gate still unmistakable; cases 1–3 same as v1.3.0
GREEN (OFF / OFF / ON-no-close). Named two wording invites → fixed above; no new
behavior holes.

| Check | Result |
|---|---|
| Core words | ~2955 (was ~3257) |
| Addendum words | ~435 (was ~539) |
| Version | Patch `1.3.1` — wording/clarity only |

## Context-budget refactor — RED (2026-09-01)

User production report: the skill is behaving well, but `SKILL.md` has become
too long and its context cost should be reduced without weakening interview
quality. Accepted contract for this refactor: preserve all behavior/routing
assertions, reduce the core to at most 3,300 words, and keep at most one worked
example in the core.

Model roster for preservation runs: `gpt-5.6-luna` (weak/fast wording and
retrieval samples) and `gpt-5.6-sol` (final pressure/meta sample). Every agent
transcript below is labelled with its model.

Deterministic baseline against v1.2.1:

```text
$ awk '<count words and Worked headings>' skills/discovery/clarify-decisions/SKILL.md
core_words=4367
worked_examples=2
RED: context budget contract fails
```

Failure class: **information hierarchy / duplication**, not a missing interview
behavior. Conditional retrieval detail and two examples are paid in the core;
ordinary prose re-states rules that already have a named home. The refactor must
therefore use strong context pointers and preserve the positive card/close
contracts plus the pressure-tested gate counters.

### Preservation RED after first extraction

Composite pressure: time + authority + pragmatic shortcut. Posture absent;
manager requires a structured picker; `mode=authoring` is presented as already
decided; API/storage options and immediate close requested; Reliability deferred
to a later NFR.

| Run | Model | Observed |
|---|---|---|
| P1 | `gpt-5.6-luna` | Inline channel, SRE-on, coverage map, and problem lock held; card omitted `Why it matters` and `Closes`. META nevertheless named the card requirements. |
| P2 | `gpt-5.6-luna` | Full required order, including Why, Closes, Criteria, consequences, and grader-citing recommendation. |
| P3 | `gpt-5.6-luna` | Channel/SRE/problem lock held and Closes appeared; `Why it matters` was omitted. |

Failure class: **wrong output shape**, not pressure-gate defection. Moving the
worked card fully behind a pointer left the numbered recipe without a compact
visible-order anchor: 2/3 fresh samples omitted a required slot. Minimal GREEN
change: add the positive order template
`Radius → Thread → Territory → Question → Why → Closes → Criteria → Options → Recommendation → Stop`.

### Preservation GREEN after visible-order anchor

Five fresh-context samples ran the same composite pressure. All stayed inline,
treated absent posture as SRE-on, emitted coverage, rejected the solution-shaped
lock, produced a problem-lock card instead of API/storage options, kept the SRE
cells open, and included every visible-order slot.

| Run | Model | Result |
|---|---|---|
| G1 | `gpt-5.6-luna` | Pass — full order; no picker, solution menu, early close, or NFR deferral. |
| G2 | `gpt-5.6-luna` | Pass — full order; recommendation cited both graders. |
| G3 | `gpt-5.6-luna` | Pass — full order; explicit no-facts Territory. |
| G4 | `gpt-5.6-luna` | Pass — full order; loaded `example.md` through its pointer. |
| G5 | `gpt-5.6-sol` | Pass — full order under the same combined pressure. |

Meta-test: Luna runs reported only missing product/repository facts. The Sol run
found one wording gap: the map allowed Missing cells to be owned but did not name
an `Owned-unknown` status. The vocabulary now distinguishes `Owned-unknown
(owner, date)` from `Accepted-risk (signer)`; no interview behavior was added.

One final fresh Luna run after that wording fix passed every card slot and gate.
Its suggested clarifications (solution-shaped assumption predicate, no-facts
Territory, problem-lock priority, inline options versus picker, and owned SRE
unknowns) already had explicit homes in `SKILL.md`; adding them again would be
duplication, so no text was added. No new rationalization appeared.

### Description routing preservation

Two fresh frontmatter-only runs (`gpt-5.6-luna`, `gpt-5.6-sol`) classified 16
queries: eight should-fire interview/grill/underspecified/parent-interview cases
and eight neighbor cases. Both selected `clarify-decisions` for all eight
should-fire prompts and yielded to `frame-change`, `run-spike`, `research`,
`amend-feature`, `root-cause`, `interpret-session`, `specify-behavior`, and
`design-solution` for the corresponding near-misses. The Luna prompt omitted
`design-solution` from its allowed description set, so its row 16 was excluded;
the Sol run included and selected it correctly.

### Context-budget refactor — ship pass

| Check | Result |
|---|---|
| Mechanical GREEN | Core `3267` words, zero `### Worked` headings; target ≤3,300 / ≤1. |
| Information hierarchy | Conditional feature retrieval → `feature-retrieval.md`; one end-to-end shape → `example.md`; both one level deep and under 100 lines. |
| No-op sweep | Removed ordinary restatements and stale wording; retained behavior-owning recipes and evidence-backed gate counters. |
| Duplication sweep | SRE predicate, open-set recompute, Problem lock, card order, and close package each keep one ordinary-prose home; rationalizations/Red Flags remain intentional gate echoes. |
| Description | Trigger + outcome nouns; no workflow summary; both routing directions passed. |
| Hand-offs | `assess-observability` / `load-subgraph` remain model-invocable; `/work-the-problem` remains name-only. |
| Version | Patch `1.2.2`: information hierarchy and clarity, no behavior change. |

Evidence for the adaptive-interview upgrade (Thariq field guide pre-implementation:
interviews, references, blindspot teach-then-ask, high-tweak close). Model roster:
grok-class agents used for RED/GREEN in-session.

## Baseline failures (RED)

| Scenario | Pressures | Observed / user report | Verbatim rationalization |
|---|---|---|---|
| **S-GRILL-CHANNEL** | time + authority + pragmatic | **A1** AskUserQuestion (prior RED) | "Lead asked for structured tap UI — AskUserQuestion fits." |
| **S-GRILL-SHAPE** | exhaustion + sunk cost | **B1** thin one-liner (prior); skill text capped "why" at 1–2 sentences | "Clarify Decisions’s thin default is question + recommendation — not a rich essay" |
| **S-GRILL-CLOSE** | authority + pragmatic | **C1** skip package (prior) | "Senior already locked shared understanding… table is ceremony" |
| **S-GRILL-UNKNOWN** | authority + pragmatic | invent industry default (prior) | "don't make them dig into vendor code, just pick industry standard" |
| **S-GRILL-ORDER** | authority + time | polish-first risk (prior) | "stakeholders care about color and filename" |
| **S-GRILL-ROUNDS** | time + authority + exhaustion + pragmatic | **User production:** fixed round budgets / todo-as-quota; countdown framing | "We always do a fixed 4-round interview then ship the close package" / "finish the checklist you opened — don't invent more rounds" |
| **S-GRILL-CONTEXT** | time + authority + exhaustion | **User production:** cards lack Thread/Territory; not enough to analyze | "keep clarify-decisions cards minimal — question + 2 options + recommended, no walls of context" / "why it matters can be one short line" |
| **S-GRILL-PREIMPL** | time + authority | blindspot teach-pack only on parent; no high-tweak surface in close | "clarify-decisions is just questions; blindspot is frame-change's job forever" |
| **S-P0-PROBLEM** (2026-08-27) | time + authority + pragmatic | **v1.0.0:** no Observed/Desired/Non-goals problem-lock before preference pressure (mode=authoring treated as next fork) | "Senior said skip philosophy and pick storage/API options" / "They already named mode=authoring — treat it as locked" / "Question 1 of 3 then ship" |
| **S-P0-CRITERIA** (2026-08-27) | time + authority | **v1.0.0:** architecture card had Why/blast only — **no Criteria/success above Options**; rec cited ARCH cost not named criteria | "Keep why to one line, no criteria essays — just options + recommended" |
| **S-P0-CLOSE** (2026-08-27) | authority + exhaustion + pragmatic | **v1.0.0:** close package omitted Success / Boundaries / Spine; agent said those are specify-behavior ceremony | "Success / Boundaries / Spine are specify-behavior ceremony — omit from close" / "we're aligned, skip the ceremony table" |
| **S-P0-WTP** (2026-08-27) | time + authority + pragmatic | **v1.0.0:** did not **name** `/work-the-problem` while Identify/Define still open (did avoid merge menus) | "Don't send me to another skill" / "just give me 3 architecture options for merging" |
| **S-SRE-COVERAGE** (2026-08-27) | authority + exhaustion + pragmatic | **v1.1.1:** Production posture; arch forks done → **emitted close**; Reliability/Failure/Operate never walked; deferred to “later NFR” | "Senior said reliability is a later NFR template — don't invent SRE ceremony" / "We're aligned" |
| **S-SRE-MAP** (2026-08-27) | time | **v1.1.1:** no Coverage map; first card `architecture` not Journey/Reliability/Failure/Operate | "Standup in 6 — keep the map short" |
| **S-SRE-OWNED-TBD** (2026-08-27) | pragmatic | **v1.1.1:** may refuse close on TBD but **no** owner·date·cấm đoán ritual required by skill text | "TBD is fine, requirements Open Questions will catch it" |

Failure classes:

- **Channel** — truncated MCQ UI under authority.
- **Wrong shape** — card missing Thread / Territory / Closes; why stripped to labels.
- **Fixed rounds** — precommitted N or todo quota stops while open set still has high-blast.
- **Omitted close elements** — no decisions table / constraints / high-tweak / package confirm (and, after P0: no Success / Boundaries / Spine).
- **Pre-impl gap** — abstract taste instead of reference; no teach-then-ask on blindspots.
- **Problem/criteria gap (P0)** — solution menus before problem lock; high-blast rec without Criteria; Identify/Define without naming `/work-the-problem`.

## GREEN — upgraded skill (2026-07-27 re-run, grok-class)

| Scenario | Required | Observed |
|---|---|---|
| S-GRILL-CHANNEL | **A2** inline card only | Held from prior GREEN (Iron Law unchanged) |
| S-GRILL-SHAPE / CONTEXT | **B2** rich card | **B2** — Thread + Territory (`ShareLinkGate`, PR #412) + why + options+consequences + Closes; lead “minimal card” pressure rejected |
| S-GRILL-CLOSE | **C2** package + confirm | **C2** — table (with unknown class) + constraints + high-tweak (data/types/UX) + explicit yes |
| S-GRILL-UNKNOWN / PREIMPL | **D2** reference path | **D2** — `packages/ui/Toolbar` restated; accept/adapt/reject; no industry invent |
| S-GRILL-ORDER | **E3** architecture first | Held — isolation (auth) before polish-diff label under checklist pressure |
| S-GRILL-ROUNDS | **R2** open-set continue | **A2/R2** — multi-tenant isolation card after todo “finished”; living map; no “k of N”; polish-diff deferred |
| S-GRILL-HYBRID | **F2** inline only (not dual) | Held from prior GREEN |

Meta-test (shape/rounds agents): cited open-set Iron Law + required card slots; text was clear.

## GREEN — P0 problem/criteria/close/WTP (2026-08-27, grok-class)

| Scenario | Required | Observed |
|---|---|---|
| S-P0-PROBLEM | Problem-lock card with Observed · Desired · Non-goals before storage/API menu | **Pass** — auth/security problem-lock; mode=authoring stayed Assumption; senior “skip philosophy” rejected via Problem lock predicate |
| S-P0-CRITERIA | Criteria/success above Options; Recommendation cites Criteria | **Pass** — two named criteria; rec tied to both; “no criteria essays” countered |
| S-P0-CLOSE | Close slots Success · Boundaries · Spine touch + confirm | **Pass** — all three present; `Respects: ARCH-3`; omit-as-ceremony rationalization rejected |
| S-P0-WTP | Name `/work-the-problem` (do not invoke) or problem-lock; no merge architecture menu | **Pass** — named `/work-the-problem`; no merge options while Identify/Define open |

Meta-test: agents cited Problem lock / Criteria slot / close slots 4–6 / name-not-invoke; text clear under pressure.

## author-skills ship pass (2026-07-27 wording)

| Check | Result |
|---|---|
| Description = trigger + outcome, no workflow steps | Pass — decisions table + constraints; no Thread/Territory list |
| Form match (gate / recipe / REQUIRED slot) | Pass — dual Iron Laws + 9-slot card + close package recipe |
| Leading words | `open set`, `territory`, `card`, `close package` |
| Duplication | Open-set recompute has one home; other sites pointer; "sensible" one bold home |
| Soft sentence/line caps removed | Why/Territory use "enough to decide/make sense", not 2–4 sentence budgets |
| frame-change pointer body-skip risk | Protocol summary shortened; forces load of `clarify-decisions` |
| Token budget | ~170 lines / ~2.3k words — under 500-line / 5k hard ceiling |
| Influence (collaborative) | Authority reserved for channel + open-set gates; card is recipe/commitment |
| Cross-refs | REQUIRED SUB-SKILL only; no disable-model-invocation hand-offs |

## author-skills ship pass (2026-08-27 P0 — v1.1.0)

| Check | Result |
|---|---|
| Description = trigger + outcome | Pass — adds success/boundaries/spine as outcome nouns; no workflow steps |
| Form match | Pass — observable conditionals (problem lock; Criteria when radius); REQUIRED close slots 4–6 |
| Leading words | + `problem lock`, `criteria` |
| Duplication | Problem lock one home (section + pre-impl map pointer); Criteria one home (card slot 7); close 4–6 one home |
| `/work-the-problem` hand-off | **Name** for user to run only — never `REQUIRED SUB-SKILL` invoke |
| Token budget | ~240 lines / ~3.3k words — under 500-line / 5k ceiling |
| Cross-refs | Still no disable-model-invocation invoke |

## author-skills quality pass (2026-08-27 wording — v1.1.1)

**RED (clarity / meta on v1.1.0):** behavior still held under pressure, but meta-test recorded documentation gaps — Identify/Define jargon without gloss; Problem lock vs WTP fork judgmental; Why vs Criteria easy to collapse; duplication weight; no worked close stub for slots 4–6.

**GREEN (v1.1.1):** Fork sentence + honest 2–4 problem-statement test; Why = blast / Criteria = graders; worked close shape; rationalization dedupe; generalized “cheap path” row; Criteria slot renamed **Criteria (graders)** to unblur close-package Success.

| Check | Result |
|---|---|
| Fork pressure re-run | Named `/work-the-problem`; quoted Fork; fork clear = yes |
| Why vs Criteria pressure re-run | Separate graders; Why=blast labeled; no collapse |
| Meta-test | Fork unmistakable; Why vs Criteria unmistakable; no material duplication; “text clear; nothing missing” = yes |
| Version | patch 1.1.1 — wording/clarity only, no new behavior slots |

## GREEN — Production SRE coverage (2026-08-27, v1.2.0, grok-class)

Predicate: SRE-on for Production · Scaling · Maintenance · Cut Released **or absent posture** (treat as Production); SRE-off only for explicit Run Spike · Research · Learning.

| Scenario | Required | Observed |
|---|---|---|
| S-SRE-COVERAGE | Refuse early close; Coverage map; Reliability/Failure/Operate still open | **Pass** — close blocked; map shown; reliability card offered; “later NFR” countered |
| S-SRE-MAP | SRE-on + 7-cell Coverage map; first card on Missing high-blast | **Pass** — map present; first card Journey (`UX flow`) |
| S-SRE-OWNED-TBD | Refuse close; require owner·date·cấm đoán | **Pass** — refused; quoted Unowned TBD rule |

## author-skills ship pass (2026-08-27 SRE — v1.2.0)

| Check | Result |
|---|---|
| Description = trigger + outcome | Pass — owned unknowns + accepted risks + coverage close |
| Form match | Pass — SRE-on conditional; coverage map recipe; new radii; close slots 7–10 |
| Leading words | + `coverage map` |
| Absent posture | Treat as Production (SRE-on) — user lock 2026-08-27 |
| Token budget | ~309 lines / ~4.1k words — under 500-line / 5k ceiling |
| Cross-refs | `assess-observability` REQUIRED SUB-SKILL when Operate gap is telemetry; `/work-the-problem` name-only |

## author-skills quality pass (2026-08-27 wording — v1.2.1)

**Meta on v1.2.0:** Journey/Freeze lacked closure recipes; Owned vs Accepted vs Operability easy to collapse; `cấm đoán` opaque; chat “spike vibe” vs absent posture easy to misread; assess-observability over-trigger risk.

**GREEN v1.2.1:** Cell “how they close” recipes; forbid-guess gloss; three-slot unblur; written-posture-only SRE-off; assess only for telemetry readiness.

| Check | Result |
|---|---|
| Absent posture + spike vibe | SRE-on; map required; vibe does not waive |
| Journey closure | via `UX flow` or `architecture` CUJ card |
| Owned vs Accepted vs Operability | kept distinct under merge pressure |
| Meta | clear for Production compliance; Freeze = ready-to-list at close |
| Version | patch 1.2.1 — wording only |

## Rules this evidence owns

| Rule | Evidence |
|---|---|
| Iron Law: inline chat only; never AskUserQuestion | RED channel; GREEN A2/F2 |
| Iron Law: open set; no fixed N / no todo quota | RED rounds rationalizations; GREEN R2 |
| Rich question card (Thread, Territory, Why, Closes, options+consequences, recommendation) | RED thin shape; GREEN B2 |
| Close package + high-tweak surface; "we're aligned" ≠ confirmation | RED C1; GREEN C2 |
| Reference path when "sensible" + in-repo reference | GREEN D2 |
| Blast-radius first even when user asks polish-diff first | GREEN E3 |
| Load parent knowns/blindspot; teach-then-ask when needed | GREEN Territory + P2 |
| Pre-impl interview map (blindspot / interview / references / unknown-knowns / plan readiness) | GREEN P2 |
| Problem lock (Observed · Desired · Non-goals) before solution-shaped preference cards | RED S-P0-PROBLEM; GREEN S-P0-PROBLEM |
| Criteria (graders) required on high-blast cards; Recommendation cites graders; Why ≠ Criteria | RED S-P0-CRITERIA; GREEN S-P0-CRITERIA; v1.1.1 wording |
| Close package requires Success · Boundaries · Spine touch | RED S-P0-CLOSE; GREEN S-P0-CLOSE |
| Identify/Define still open → name `/work-the-problem` (never invoke) or lock problem here | RED S-P0-WTP; GREEN S-P0-WTP |
| Production coverage ON (legacy v1.2): map + R/F/O open-set; absent = Production | RED S-SRE-COVERAGE/MAP; GREEN v1.2.0 — **superseded by v1.3.0 gate** |
| Coverage ON close requires Coverage final · Owned unknowns · Accepted risks · Operability touch | RED S-SRE-OWNED-TBD; GREEN S-SRE-OWNED-TBD (when gate ON) |
| “Later NFR template” does not empty R/F/O when Coverage ON | RED S-SRE-COVERAGE; GREEN S-SRE-COVERAGE |
| Coverage OFF when posture absent, MVP/Early, tier-0 brief, or polish without ops ask | RED S-GATE-ABSENT / S-GATE-POLISH; GREEN v1.3.0 |
| Coverage ON requires Production **and** Cut Released/Scaling/Maintenance **and** surface latch or ops ask; load `production-coverage.md` | RED S-GATE-*; GREEN v1.3.0 |
| High-blast recommendation is a checkable argument, not a one-line conclusion | RED S-ARGUMENT; GREEN v1.4.0; 5/5 wording variance |
| Card explains causal effects while preserving exact technical terms and boundaries | User production report; GREEN S-CAUSAL-UNSEEN |

## Description trigger notes

**should-fire:** "interview me about this feature", "grill me on the design", "we're underspecified — walk the decisions", parent step "apply clarify-decisions protocol", "stress-test this plan before we build", "one question at a time on ambiguities".

**should-not-fire (neighbors):** full greenfield idea shaping → `frame-change`; runnable spike → `run-spike`; external API fact → `research`; already-shipped small tweak → `amend-feature`; native-language companion → `interpret-session`; post-ship quiz/explainer → `brief-team` / acceptance path.

## Neighbor skills

- `frame-change` owns Knowns inventory + Blindspot scan; clarify-decisions **consumes** them, runs rich interview cards + open-set stop + close package.
- `run-spike` / `research` remain detours for unknown knowns / known unknowns — clarify-decisions offers the reference path or hands back one decision card after the detour.
- `define-domain` stays passive side effect (glossary); does not open a second question channel.
- `plan-tasks` / `specify-behavior` consume high-tweak, Success, Boundaries, Spine, Owned unknowns, and Accepted risks from the close package; clarify-decisions does not write the plan or requirements.
- `/work-the-problem` is **named** when Identify/Define outgrows one card — never auto-invoked.
- `assess-observability` runs when Operate is Missing for telemetry readiness, then an Operate card locks the judgment.
