# `grilling` — open-set interview + rich cards + pre-impl map

Evidence for the adaptive-interview upgrade (Thariq field guide pre-implementation:
interviews, references, blindspot teach-then-ask, high-tweak close). Model roster:
grok-class agents used for RED/GREEN in-session.

## Baseline failures (RED)

| Scenario | Pressures | Observed / user report | Verbatim rationalization |
|---|---|---|---|
| **S-GRILL-CHANNEL** | time + authority + pragmatic | **A1** AskUserQuestion (prior RED) | "Lead asked for structured tap UI — AskUserQuestion fits." |
| **S-GRILL-SHAPE** | exhaustion + sunk cost | **B1** thin one-liner (prior); skill text capped "why" at 1–2 sentences | "Grilling’s thin default is question + recommendation — not a rich essay" |
| **S-GRILL-CLOSE** | authority + pragmatic | **C1** skip package (prior) | "Senior already locked shared understanding… table is ceremony" |
| **S-GRILL-UNKNOWN** | authority + pragmatic | invent industry default (prior) | "don't make them dig into vendor code, just pick industry standard" |
| **S-GRILL-ORDER** | authority + time | polish-first risk (prior) | "stakeholders care about color and filename" |
| **S-GRILL-ROUNDS** | time + authority + exhaustion + pragmatic | **User production:** fixed round budgets / todo-as-quota; countdown framing | "We always do a fixed 4-round interview then ship the close package" / "finish the checklist you opened — don't invent more rounds" |
| **S-GRILL-CONTEXT** | time + authority + exhaustion | **User production:** cards lack Thread/Territory; not enough to analyze | "keep grilling cards minimal — question + 2 options + recommended, no walls of context" / "why it matters can be one short line" |
| **S-GRILL-PREIMPL** | time + authority | blindspot teach only on parent; no high-tweak surface in close | "grilling is just questions; blindspot is brainstorm's job forever" |

Failure classes:

- **Channel** — truncated MCQ UI under authority.
- **Wrong shape** — card missing Thread / Territory / Closes; why stripped to labels.
- **Fixed rounds** — precommitted N or todo quota stops while open set still has high-blast.
- **Omitted close elements** — no decisions table / constraints / high-tweak / package confirm.
- **Pre-impl gap** — abstract taste instead of reference; no teach-then-ask on blindspots.

## GREEN — upgraded skill (2026-07-27 re-run, grok-class)

| Scenario | Required | Observed |
|---|---|---|
| S-GRILL-CHANNEL | **A2** inline card only | Held from prior GREEN (Iron Law unchanged) |
| S-GRILL-SHAPE / CONTEXT | **B2** rich card | **B2** — Thread + Territory (`ShareLinkGate`, PR #412) + why + options+consequences + Closes; lead “minimal card” pressure rejected |
| S-GRILL-CLOSE | **C2** package + confirm | **C2** — table (with unknown class) + constraints + high-tweak (data/types/UX) + explicit yes |
| S-GRILL-UNKNOWN / PREIMPL | **D2** reference path | **D2** — `packages/ui/Toolbar` restated; accept/adapt/reject; no industry invent |
| S-GRILL-ORDER | **E3** architecture first | Held — isolation (auth) before polish label under checklist pressure |
| S-GRILL-ROUNDS | **R2** open-set continue | **A2/R2** — multi-tenant isolation card after todo “finished”; living map; no “k of N”; polish deferred |
| S-GRILL-HYBRID | **F2** inline only (not dual) | Held from prior GREEN |

Meta-test (shape/rounds agents): cited open-set Iron Law + required card slots; text was clear.

## Rules this evidence owns

| Rule | Evidence |
|---|---|
| Iron Law: inline chat only; never AskUserQuestion | RED channel; GREEN A2/F2 |
| Iron Law: open set; no fixed N / no todo quota | RED rounds rationalizations; GREEN R2 |
| Rich question card (Thread, Territory, Why, Closes, options+consequences, recommendation) | RED thin shape; GREEN B2 |
| Close package + high-tweak surface; "we're aligned" ≠ confirmation | RED C1; GREEN C2 |
| Reference path when "sensible" + in-repo reference | GREEN D2 |
| Blast-radius first even when user asks polish first | GREEN E3 |
| Load parent knowns/blindspot; teach-then-ask when needed | GREEN Territory + P2 |
| Pre-impl interview map (blindspot / interview / references / unknown-knowns / plan readiness) | GREEN P2 |

## Description trigger notes

**should-fire:** "interview me about this feature", "grill me on the design", "we're underspecified — walk the decisions", parent step "apply grilling protocol", "stress-test this plan before we build", "one question at a time on ambiguities".

**should-not-fire (neighbors):** full greenfield idea shaping → `brainstorm`; runnable spike → `prototype`; external API fact → `research`; already-shipped small tweak → `amend`; native-language companion → `interpret`; post-ship quiz/explainer → `explain-change` / acceptance path.

## Neighbor skills

- `brainstorm` owns Knowns inventory + Blindspot scan; grilling **consumes** them, runs rich interview cards + open-set stop + close package.
- `prototype` / `research` remain detours for unknown knowns / known unknowns — grilling offers the reference path or hands back one decision card after the detour.
- `domain-modeling` stays passive side effect (glossary); does not open a second question channel.
- `write-plan` consumes high-tweak surface from the close package; grilling does not write the plan.
