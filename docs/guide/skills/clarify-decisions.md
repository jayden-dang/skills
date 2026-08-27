# `clarify-decisions`

> The interview primitive. One full-context question card per message — problem lock, criteria graders, and (on Production) an SRE **coverage map** — until high-blast cells are Clear or owned. Sealed by a close package (decisions, constraints, success, boundaries, spine, **owned unknowns**, **accepted risks**, operability touch) plus explicit confirmation.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | model-invocable |
| **Reads** | codebase/docs; parent Knowns / Blindspot; Project posture |
| **Writes** | nothing production (glossary via `define-domain` only) |
| **Calls** | may **name** `/work-the-problem`; may run `assess-observability` when Operate is a telemetry gap; may hand facts to `research` / `run-spike` |
| **Called by** | [`frame-change`](frame-change.md) interview step; any skill that needs an interview |

## When it fires

Underspecified intent that must be drawn out before build; user asks to be grilled; or a parent skill requires an interview.

## Production SRE coverage

**SRE-on** when posture is Production · Scaling · Maintenance · Cut Released, **or posture is absent** (treated as Production).  
**SRE-off** only when posture is **written** as Run Spike · Research · Learning — chat “spike vibe” does not flip the band.

When SRE-on, the starting map includes a **coverage map** (Frame · Journey · Contract · Reliability · Failure · Operate · Freeze). Journey closes via `UX flow` / `architecture` CUJ cards (no Journey radius). Freeze is not a radius — it clears when Owned unknowns + Accepted risks are ready to list. Missing cells without an owner keep the open set alive.

## Channel and open set

Inline chat only — no truncated MCQ pickers. **No fixed round count.** Stop when high-blast forks (including reliability / failure / operate under SRE-on) are empty **and** no coverage cell is Missing without owner.

## Problem lock

If 2–4 alternate problem statements fit on one card → problem-lock card (Observed · Desired · Non-goals). If symptoms and solutions stay tangled → **name** `/work-the-problem`. No solution menu either way.

## Question card

Radius: `architecture` · `data` · `auth/security` · `UX flow` · `reliability` · `failure` · `operate` · `polish-diff` (last three only when SRE-on).

Required slots include Thread, Territory, Why (**blast only**), Closes, **Criteria (graders)** on high-blast radii, Options with consequences, Recommendation citing graders.

## Close package

Always: decisions table · constraints · high-tweak · success · boundaries · spine · explicit yes.  
When SRE-on, also: **coverage final** · **owned unknowns** (undecided TBD: owner · date · forbid-guess) · **accepted risks** (decided keep-the-risk + signer) · **operability touch** (rollback + who is paged) — three distinct slots.

## See also

- [`frame-change`](frame-change.md) · [`work-the-problem`](work-the-problem.md) · [`assess-observability`](assess-observability.md) · [`research`](research.md) · [`run-spike`](run-spike.md) · [`specify-behavior`](specify-behavior.md)
