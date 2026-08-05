# `solve-problem`

> Ambiguous problem-shaped request → one evidence-grounded **Problem Brief** and exactly one route. Intake router, not a delivery pipeline.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | model-invocable |
| **Reads** | whatever evidence the request supplies; may detour to `research` / `run-spike` / `load-subgraph` |
| **Writes** | a Problem Brief (chat is fine; optional note under `.skills/` if the session needs it) |
| **Calls** | `research`, `run-spike`, `load-subgraph` when a missing fact blocks classification; then re-classifies once |
| **Called by** | session routing when gap or workflow is unclear; hands off to `root-cause`, `frame-change`, `clarify-decisions`, or `STOP` |

## When it fires

Use when a **symptom, opportunity, requested solution, or “problem”** has **no trustworthy gap** or **clear workflow** yet.

Typical shapes:

- “Something is wrong / conversion dropped” without a diagnostic loop or agreed outcome
- “Add Redis / ship the AI personalizer” as a prescribed fix without a demonstrated gap
- “Is this even a problem?” / stuck between investigate and build

## When it does **not** fire

| Already clear | Go straight to |
|---|---|
| Unexpected behavior, failing test, crash, regression | `root-cause` |
| New feature / behavior, no requirements yet | `frame-change` |
| Small change to shipped, spec'd feature | `amend-feature` |
| Plan invalidated mid-execution | `reroute-plan` |
| Multi-session destination still foggy | user runs `/pathfind` |

## What it produces

A **Problem Brief** with every slot filled — observed state (with sources), desired state, gap verdict, facts vs assumptions, constraints, success/guards with provenance, risk, and **exactly one** class + route (or `STOP`).

Derivation rules that pressure tests own:

1. Evidence ≠ interpretation
2. Desired state is an outcome, not a prescribed operator
3. Deadlines are constraints, not evidence
4. Success numbers need provenance or stay `unresolved`
5. A baseline is not a threshold
6. Owner and risk need evidence
7. No meaningful gap → `STOP`
8. Delivery verified ≠ outcome solved

## Route table (summary)

| Class | Route |
|---|---|
| diagnostic | `root-cause` |
| discovery / improvement / adaptive | `frame-change` (with brief) |
| decision | `clarify-decisions` |
| no-problem | `STOP` |
| unresolved (need a fact first) | evidence skill, then classify once |

Stop after routing. The target skill owns the work.

## See also

- Skill body: [`skills/discovery/solve-problem/SKILL.md`](../../../skills/discovery/solve-problem/SKILL.md)
- Pressure evidence: [`skills/discovery/solve-problem/TESTS.md`](../../../skills/discovery/solve-problem/TESTS.md)
- [`root-cause`](root-cause.md) · [`frame-change`](frame-change.md) · [`clarify-decisions`](clarify-decisions.md) · [`research`](research.md)
