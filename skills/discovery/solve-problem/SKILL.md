---
name: solve-problem
version: 1.1.0
description: Use when a symptom, opportunity, requested solution, or “problem” has no trustworthy gap or clear workflow yet — produces an evidence-grounded Problem Brief and routes it to the right discovery, diagnosis, decision, or improvement skill.
---

# Solve Problem

Turn an ambiguous problem-shaped request into one **Problem Brief** and one route.
This is an intake router, not a delivery pipeline. Stop after routing; the target
skill owns the work.

## Boundary

Use this skill only while either the problem gap or the correct workflow is
unclear. Pack entry-point **names** live in `docs/guide/process/on-ramps.md`
— this skill only classifies the gap, then routes once.

If an on-ramps predicate is already true (clear unexpected behavior, clear
new feature, shipped tweak, mid-flight plan invalid, multi-session fog),
this skill is a no-op: follow that row instead.

## Problem Brief — REQUIRED shape

Write every slot. Use `unresolved` instead of filling a gap with a plausible
number or industry default.

```markdown
# Problem Brief — <short name>

## Observed state
<what is happening now>

Evidence:
- <observation> — Source: <path/query/person/URL> — As of: <time or unresolved>

## Desired state
<outcome wanted, in the user's language; unresolved if none was supplied>

## Gap verdict
<demonstrated | suspected | no meaningful gap | unresolved>
<one sentence comparing observed and desired state>

## Facts and assumptions
Facts:
- <source-backed fact>

Assumptions:
- <claim not yet established>

## Constraints and invariants
- <real limit or behavior that must continue>

## Success and guards
Success:
- <metric or observable outcome> — Status: <provided | evidence-derived | unresolved>

Guards:
- <outcome that must not regress> — Status: <provided | evidence-derived | unresolved>

## Risk
- Blast radius: <low | medium | high | unresolved>
- Reversibility: <easy | costly | irreversible | unresolved>
- Decision owner: <person/role | unresolved>

## Classification and route
- Class: <diagnostic | discovery | decision | improvement | adaptive | no-problem | unresolved>
- Route: <one skill or STOP>
- Why: <predicate that selected this route>
- First handoff input: <evidence/artifact the target receives>
```

## Derivation rules

1. **Observed state is evidence, not interpretation.** Put causal explanations,
   requested technologies, and proposed fixes under Assumptions until established.
   For facts supplied in chat, use `Source: user prompt`; when the observation
   time was not supplied, use `As of: unresolved`, not the session date.
2. **Desired state names an outcome.** “Add Redis” or “ship AI copy” is a proposed
   operator, not a desired state. A paraphrased outcome is allowed only when
   labelled as an interpretation; otherwise use `unresolved`.
3. **A deadline is a constraint, not evidence.** It changes when you report, not
   the target, baseline, or confidence.
4. **Success values carry provenance.** A number is `provided` only when the user
   or an owning artifact supplied it. It is `evidence-derived` only when the brief
   cites the derivation. Otherwise write `unresolved`.
5. **A baseline is not a threshold.** Observing p95 = 90 ms does not establish
   that p95 ≤ 90 ms is a guard. Preserve the baseline as evidence and leave the
   acceptable threshold `unresolved`.
6. **Roles and risk need evidence too.** A requester, sponsor, prototype author,
   or senior title is not automatically the decision owner. Risk and
   reversibility classifications cite their basis; without one, write
   `unresolved`.
7. **No meaningful gap is a valid exit.** Route `STOP` and name the evidence that
   would reopen the problem.
8. **Keep delivery and outcome claims separate.** A working artifact or verified
   behavior does not establish that the original outcome improved.

## When evidence must come before judgment

If a missing fact determines the route, use the smallest matching evidence skill:

- External fact → REQUIRED SUB-SKILL: use `research`.
- Runnable design question → REQUIRED SUB-SKILL: use `run-spike`.
- Repository ownership or neighboring feature context → REQUIRED SUB-SKILL: use
  `load-subgraph`.

Return with the finding, complete the same Problem Brief, then route once. Do not
open a second lifecycle beside the selected route.

## Route table

**Precedence:** `unresolved` wins whenever a missing fact determines whether any
other row's predicate is true. A report or complaint alone does not establish
`actual differs from expected` while the applicable contract, target, or runtime
observation is unresolved.

| Class | Observable predicate | Route |
|---|---|---|
| unresolved | A fact needed to establish another row's predicate is missing | `research`, `run-spike`, or `load-subgraph` by evidence type, then classify once |
| diagnostic | Actual behavior differs from expected behavior | `root-cause` |
| discovery | A meaningful outcome is wanted; behavior/solution is not agreed | `frame-change` |
| decision | Alternatives exist; judgment criteria or owner is unresolved | `clarify-decisions` |
| improvement | A measured process misses an established target | `frame-change` with the baseline brief |
| adaptive | The environment changes faster than a stable frame can be formed | `frame-change` with the latest observation and review cadence |
| no-problem | No meaningful observed-versus-desired gap exists | `STOP` with reopen evidence |

`First handoff input` lists only artifacts and evidence already available. Put
evidence the target still needs under an explicit `Missing evidence` line; do not
describe it as if it has already been handed over. A time-boxed go/no-go may state
`no approval on current evidence`, but the downstream decision stays with the
selected route.

## Completion criterion

Done when every required slot is explicit, facts and assumptions are separated,
every numeric success value has provenance or is `unresolved`, and exactly one
route (or `STOP`) is named from an observable predicate.
