# `clarify-decisions`

> Interview primitive: one full-context question card per message until high-blast forks close. Sealed by a close package (decisions, constraints, success, boundaries, spine) + explicit yes. **Production coverage** (map · owned unknowns · accepted risks · operability) loads only when a three-part gate is ON.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | model-invocable |
| **Reads** | codebase/docs; parent Knowns / Blindspot; Project posture |
| **Writes** | nothing production (glossary via `define-domain` only) |
| **Calls** | `assess-observability` when Coverage ON and Operate is a telemetry gap; `research` / `run-spike` for facts, and `research` for how a shipped product does the feature on the card |
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

## Compat obligation

Separate from the coverage gate, and read on every interview. `docs/agents/project.md`
**Project posture** carries a **Compat obligation** — `None` / `Internal` / `External` —
written, or derived from lifecycle stage when the line is absent (pre-release → None,
released → External). It, not delivery intent, decides the migration lens.

On **None**, options and the Recommendation on an `architecture` or `data` card change the
shape in place: rewrite the committed migration, rename the column, change the endpoint,
delete the dead path. A parallel column, a sync trigger, a `v2` name, or a deprecation
window on a None repo buys compatibility with a consumer the posture says does not exist —
a defect in the card, not caution. On **Internal** / **External** those costs are
first-class. Absent posture: no compat lens either way.

## Channel and open set

Inline chat only. No fixed round count. Stop when high-blast forks are empty; when ON, also no coverage cell Missing without owner.

## Problem lock

2–4 alternate problem statements (Observed · Desired · Non-goals) on one card. No solution menu.

## Question card

Radii: `architecture` · `data` · `auth/security` · `UX flow` · `polish-diff` (+ `reliability` · `failure` · `operate` when ON).

Slots: Thread, Territory, Why (blast), Closes, Criteria (graders) on high-blast,
Options with causal consequences, and a Recommendation decision argument. The
argument names the pick, decisive Territory/Criteria, runner-up, accepted
trade-off, confidence/evidence gap, and reopen trigger. `polish-diff` keeps a
one-sentence recommendation. Technical names and boundaries stay exact; local
explanations make their causal effect understandable.

When the card decides a feature that shipped products already have (undo on
delete, sharing and access, invites, retries, notifications, search), one option
is **the proven reference, cut to fit**. The card names the product and why it is
known to work, confirmed through `research` or marked recalled and unverified. It
lists every piece the product ships, in the order a user meets them, and cuts
each piece this repo does not need, one reason each. What is left is judged by
the same Criteria as any other option. Two baseline interviews drew every option
from scratch. One recommended a single `editor_id` column for sharing, a hard
limit of one collaborator that no note app people share in has.

## Close package

Always: decisions · constraints · high-tweak · success · boundaries · spine · yes.  
When ON: also coverage final · owned unknowns · accepted risks · operability.

## Card or default (v1.9.0)

Measured over six interviews, one run spent a card on what another read from the code, and two runs cut a date picker because a nearby filter existed, leaving a bookkeeper's own period with no control. So each open item is now tested first. A changed meaning, a new state, or who pays, holds or loses is always a card, even when no column is added. Otherwise a point the repo settles, or a pick that builds nothing and leaves nobody worse off, becomes a `default` row in the close package, where the user still confirms it. A reference piece cut as already on the screen must name the control that does that part of the task, or it is a gap. On an unseen fixture the old text ran past six answers without closing, and the new text closed in five or six with the money and hold cards intact. This is not evidence of less overbuild, and a few weak defaults remain.

## See also

- [`frame-change`](frame-change.md) · [`assess-observability`](assess-observability.md) · [`research`](research.md) · [`run-spike`](run-spike.md) · [`specify-behavior`](specify-behavior.md)
