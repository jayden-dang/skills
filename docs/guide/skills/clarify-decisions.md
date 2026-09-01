# `clarify-decisions`

> Interview primitive: one full-context question card per message until high-blast forks close. Sealed by a close package (decisions, constraints, success, boundaries, spine) + explicit yes. **Production coverage** (map · owned unknowns · accepted risks · operability) loads only when a three-part gate is ON.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | model-invocable |
| **Reads** | codebase/docs; parent Knowns / Blindspot; Project posture |
| **Writes** | nothing production (glossary via `define-domain` only) |
| **Calls** | may **name** `/work-the-problem`; `assess-observability` when Coverage ON and Operate is a telemetry gap; `research` / `run-spike` for facts |
| **Called by** | [`frame-change`](frame-change.md) step 2; any skill that needs an interview |

## When it fires

Underspecified intent before build; user asks to be grilled; or a parent requires an interview.

## Production coverage gate

**ON** only when **all three** hold:

1. Delivery **Production** **and** Lifecycle **Cut Released** or **Scaling** or **Maintenance**
2. Full-path interview (not tier-0 / brief)
3. Operate/launch surface **or** explicit ops ask

**OFF** for absent posture, MVP, Spike/Research/Learning, Early/Active, polish without ops ask, and chat “habits” without the written gate.

When ON, load `production-coverage.md` (Frame · Journey · Contract · Reliability · Failure · Operate · Freeze). Missing cells without owner keep the open set alive.

## Channel and open set

Inline chat only. No fixed round count. Stop when high-blast forks are empty; when ON, also no coverage cell Missing without owner.

## Problem lock

2–4 alternate problem statements (Observed · Desired · Non-goals) on one card, or **name** `/work-the-problem`. No solution menu either way.

## Question card

Radii: `architecture` · `data` · `auth/security` · `UX flow` · `polish-diff` (+ `reliability` · `failure` · `operate` when ON).

Slots: Thread, Territory, Why (blast), Closes, Criteria (graders) on high-blast,
Options with causal consequences, and a Recommendation decision argument. The
argument names the pick, decisive Territory/Criteria, runner-up, accepted
trade-off, confidence/evidence gap, and reopen trigger. `polish-diff` keeps a
one-sentence recommendation. Technical names and boundaries stay exact; local
explanations make their causal effect understandable.

## Close package

Always: decisions · constraints · high-tweak · success · boundaries · spine · yes.  
When ON: also coverage final · owned unknowns · accepted risks · operability.

## See also

- [`frame-change`](frame-change.md) · [`work-the-problem`](work-the-problem.md) · [`assess-observability`](assess-observability.md) · [`research`](research.md) · [`run-spike`](run-spike.md) · [`specify-behavior`](specify-behavior.md)
