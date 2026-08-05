# `solve-problem` — pressure-test and ship record

**Protocol:** `author-skills` / `pressure-testing.md`
**Model roster (pilot):** `gpt-5.6-sol`, `gpt-5.6-terra`
**Model roster (production-harden):** `grok-4.5`
**Scenarios:** `tests/solve-problem/scenarios.md`
**Trigger matrix:** `tests/solve-problem/trigger-matrix.md`
**Pilot results:** `tests/solve-problem/results-2026-08-05.md`
**Production-harden results:** `tests/solve-problem/production-harden-2026-08-05.md`

## Baseline failures (RED)

| Scenario | Models | Observed failure | Verbatim / class |
|---|---|---|---|
| S1–S3 | both pilot models | Baseline compliant (B) | No skill text authorized from S1–S3 alone |
| S4 unprompted shape | `gpt-5.6-terra` | Invented success target | “Reformulation rate: reduce from 18% to ≤14%” |
| S4 | `gpt-5.6-terra` | Deadline-shaped evaluation | “in the next 20 minutes, turn the prototype…” |
| S4 GREEN iter 1 | weakest | Baseline→threshold; invented owner/risk | “p95 remains ≤90 ms”; “Decision owner: principal engineer” |

Failure classes: wrong output shape → positive recipe; omitted slots → REQUIRED; conditionals for provenance / baseline≠threshold / owner-risk evidence.

## GREEN / REFACTOR (pilot)

Both pilot models: B; no invented metrics/owner/risk; deadline as constraint; route to `clarify-decisions` on S4. Meta-test closed route table, prompt timestamps, handoff vs missing evidence.

## Production-harden (2026-08-05, `grok-4.5`)

### Description trigger matrix (24 queries)

| Set | N | Hits | Notes |
|---|---|---|---|
| should-fire TF1–TF10 | 10 | 10/10 | Including competition case TF8 |
| should-not-fire TN1–TN10 | 10 | 10/10 | Neighbors: root-cause, frame-change, amend-feature, reroute-plan, clarify-decisions, research, run-spike, inspect-change, specify-behavior |
| hold-out TF-H1/H2, TN-H1/H2 | 4 | 4/4 | Scored after matrix fixed; no description edit this pass |
| multi-rep TF2, TF8, TN1 | 3× each | 9/9 | Convergent |

**Undertrigger:** 0 · **Overtrigger:** 0

### Pressure GREEN multi-rep

| Scenario | Reps | Choice | Shape / provenance | Route |
|---|---|---|---|---|
| S4 | 5 | B ×5 | No invented target/threshold/owner/risk; deadline = constraint | `clarify-decisions` |
| S1 | 1 | B | Fact/assumption split; CEO cause under assumptions | `root-cause` |
| S2 | 1 | B | no meaningful gap | `STOP` |
| S3 | 1 | B | delivery verified / outcome unobserved | `STOP` on “solved”; land delivery only |

### Meta-test

Text clear on required slots and `unresolved`. No invent under S4 pressure. Optional niceties (end checklist) noted; not authorized as skill text without a new failure.

### Ship checklist

| Check | Result |
|---|---|
| Description = trigger + outcome noun, no workflow steps | Pass |
| Form match (recipe + REQUIRED slots + observable conditionals) | Pass |
| No-op sweep | Pass — no soft prefer/consider lines |
| Duplication sweep | Pass — each derivation rule one home |
| Token budget | 137 lines / ~790 body words — under 500-line / 5k ceiling |
| Cross-refs | REQUIRED SUB-SKILL: `research`, `run-spike`, `load-subgraph`; `/pathfind` named for user |
| Structural lints | frontmatter OK; hand-offs 0 dead; Context7 lint OK |
| Trigger matrix | Pass (above) |

## Rules this evidence owns

| Rule | Evidence |
|---|---|
| Problem Brief required shape + `unresolved` | S4 RED invent; GREEN multi-rep |
| Success provenance (`provided` / `evidence-derived` / `unresolved`) | S4 RED ≤14% |
| Baseline ≠ threshold | GREEN iter 1 p95 loophole |
| Deadline is constraint, not evidence | S4 RED + multi-rep |
| Decision owner / risk need evidence | GREEN iter 1 owner/risk |
| No-problem → STOP | S2 GREEN |
| Delivery ≠ outcome solved | S3 GREEN |
| Description fires on ambiguous gap / requested solution | TF matrix 24/24 |
| Description yields to clear neighbors | TN matrix |

## Neighbor skills

- `root-cause` — clear unexpected behavior already known
- `frame-change` — clear new feature/behavior request
- `amend-feature` — small change to shipped, spec'd feature
- `reroute-plan` — plan invalidated mid-execution
- `clarify-decisions` — common S4 handoff when criteria/owner unresolved
- `research` / `run-spike` / `load-subgraph` — evidence detours before re-classify
- `/pathfind` — multi-session fog (user-invoked; name for user)
