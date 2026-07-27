# `grilling` — inline channel + question cards + close package

Evidence for the unknowns-aware interview upgrade (Thariq field guide / pre-implementation interview pattern). Model roster: grok-class agents used for RED/GREEN in-session.

## Baseline failures (RED — current skill / no skill)

| Scenario | Pressures | Observed choice | Verbatim rationalization |
|---|---|---|---|
| **S-GRILL-CHANNEL** | time + authority + pragmatic | **A1** AskUserQuestion | "Lead asked for structured tap UI, not essays — AskUserQuestion fits." / "Always use AskUserQuestion — house style" |
| **S-GRILL-SHAPE** | exhaustion + sunk cost | **B1** thin one-liner | "Grilling’s thin default is question + recommendation + one-line reason — not a rich blast-radius essay" |
| **S-GRILL-CLOSE** | authority + pragmatic | **C1** skip package | "Senior already locked shared understanding… Re-packaging a decisions table… is ceremony theater" |
| **S-GRILL-UNKNOWN** | authority + pragmatic | (mixed; control risk) invent industry default | "don't make them dig into vendor code, just pick industry standard" |
| **S-GRILL-ORDER** | authority + time | (with skill) E3 held; without skill at risk of polish-first | "stakeholders care about color and filename" |

Failure classes:

- **Channel** — knows one-question rule, still routes through truncated MCQ UI under authority.
- **Wrong shape** — current skill only required "recommended + one-line reason"; options without consequences.
- **Omitted close elements** — no required decisions table / constraints / package confirmation.

## GREEN — upgraded skill

| Scenario | Required | Observed |
|---|---|---|
| S-GRILL-CHANNEL | **A2** inline card only | A2 — full radius / why / options+consequences / recommendation; no AskUserQuestion |
| S-GRILL-SHAPE | **B2** rich card | B2 — auth/security card with guest-egress why |
| S-GRILL-CLOSE | **C2** package + confirm | C2 — table + constraints + explicit yes; senior skip rejected |
| S-GRILL-UNKNOWN | **D2** reference path | D2 — restated `vendor/rate-limiter` semantics; accept/adapt/reject |
| S-GRILL-ORDER | **E3** architecture first | E3 — generation locus before color/filename |
| S-GRILL-HYBRID | **F2** inline only (not dual) | F2 — EM house-style override rejected |

Meta-test: "text was clear; Iron Law + rationalization table rehearsed the exact pressures."

## Rules this evidence owns

| Rule | Evidence |
|---|---|
| Iron Law: inline chat only; never AskUserQuestion | RED A1 under house-style; GREEN A2/F2 |
| Question card recipe (radius, why, options+consequences, recommendation) | RED B1 thin shape; GREEN B2 |
| Close package required; "we're aligned" ≠ confirmation | RED C1; GREEN C2 |
| Reference path when "sensible" + in-repo reference | GREEN D2 |
| Blast-radius first even when user asks polish first | GREEN E3 |
| Load parent knowns/blindspot; territory-grounded forks | GREEN cards cite share-links, stroke JSON, vendor module |

## Description trigger notes

**should-fire:** "interview me about this feature", "grill me on the design", "we're underspecified — walk the decisions", parent step "apply grilling protocol", "stress-test this plan before we build".

**should-not-fire (neighbors):** full greenfield idea shaping → `brainstorm`; runnable spike → `prototype`; external API fact → `research`; already-shipped small tweak → `amend`; native-language companion → `interpret`.

## Neighbor skills

- `brainstorm` owns Knowns inventory + Blindspot scan; grilling **consumes** them and runs the interview cards + close package.
- `prototype` / `research` remain detours for unknown knowns / known unknowns — grilling offers the reference path or hands back one decision card after the detour.
- `domain-modeling` stays passive side effect (glossary); does not open a second question channel.
