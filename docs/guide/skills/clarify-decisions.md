# `clarify-decisions`

> The interview primitive. One full-context question card per message — including problem lock and criteria when they apply — until you and the user hold the same picture, sealed by a close package (decisions, constraints, high-tweak, **success**, **boundaries**, **spine touch**) and explicit confirmation.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the codebase and docs — to look up every fact before asking about it; parent Knowns / Blindspot digests when present |
| **Writes** | nothing production; it enacts no code, files, or plan execution (glossary side effects via `define-domain` only) |
| **Calls** | may **name** `/work-the-problem` for the user to run when Identify/Define is still open (never auto-invoke); may hand unknown-knowns to the parent's `run-spike` / `research` detour |
| **Called by** | [`frame-change`](frame-change.md) (its required interview step); any skill whose work calls for an interview |

## When it fires

Whenever intent is underspecified and the decisions must be drawn out of the user: to stress-test a plan, design, or feature idea before anything is built, when the user asks to be grilled or interviewed, or when another skill calls for an interview.

[`frame-change`](frame-change.md) invokes it as a required sub-skill for its whole interview step, and other design skills reach for it the same way. It is a primitive — it does one thing, holds no state of its own, and hands the picture it draws to whatever skill called it.

## Channel: inline chat only

Every question is ordinary chat with **full context**. The skill forbids `AskUserQuestion` and any harness MCQ UI that truncates labels, option text, or the "why this matters" line. A tap-friendly picker that strips consequences is a different, worse interview — not a speed optimization.

Open set has **no fixed round count** — stop only when high-blast judgment calls are empty.

## Problem lock (before preference cards)

**Fork:** if 2–4 alternate problem statements (each Observed · Desired · Non-goals) fit on one card → that card first; if symptoms and solution shapes are still tangled or those three lines cannot be written honestly per option → the agent **names** `/work-the-problem` for you to run (never auto-invokes it). No solution-shape menu in either case.

## The question card

Exactly one decision per message, in this shape:

1. **Radius** — `architecture` · `data` · `auth/security` · `UX flow` · `polish-diff`
2. **Thread** — Locked so far · This card · Still open after (names, never “3 of 5”)
3. **Territory** — grounded repo/parent facts (teach blindspots here)
4. **Question** — the decision in plain language
5. **Why it matters** — blast narrative only (what rewrites if wrong)
6. **Closes** — `known-unknown` · `unknown-known` · `blindspot-confirm`
7. **Criteria (graders)** — required on high-blast radii (omit only `polish-diff`): 1–2 named pass/fail graders **above** Options; not the close-package Success slot; Recommendation cites graders by name
8. **Options (2–4)** — each title **plus** a consequence line
9. **Recommendation** — marked pick + reason citing Criteria graders
10. **Stop** and wait

Blast-radius first — even when the user asks to start with polish. Facts are looked up; only judgment calls go to the user.

## Close package

When no high-blast branch remains, and **before** handing back or claiming alignment, the agent emits:

1. A **decisions table** (radius · topic · decision · unknown class)
2. A **constraints block** ready to paste into the next stage
3. **High-tweak surface**
4. **Success / done signal** — 1–3 observables
5. **Boundaries** — Off limits · Must keep working
6. **Spine touch** — `Respects: ARCH-N` · `none` · or `challenges` (when an architecture spine exists)
7. An ask for **explicit confirmation** on that package

"Any other questions?", "we're aligned — skip the table", and "just go write requirements" are not confirmation. Nothing is enacted until the yes lands on the package.

## Why it is written the way it is

Baseline failures (see `TESTS.md`) drove the text: truncated channels, thin cards, fixed-round quotas, skipped close packages — and the 2026-08-27 P0 set: solution menus before problem lock, recommendations without criteria, close packages without success/boundaries/spine, and Identify/Define without naming `/work-the-problem`.

The no-enactment rule keeps `clarify-decisions` a pure interview: it draws the picture, and another skill builds from it.

## See also

- [`frame-change`](frame-change.md) — the primary caller; clarify-decisions is its interview step
- [`work-the-problem`](work-the-problem.md) — user-run companion when the problem tree needs multi-round Identify/Define
- [`research`](research.md) — where a factual question too big to just look up gets sent
- [`run-spike`](run-spike.md) — where unknown knowns need a visible throwaway answer
- [`define-domain`](define-domain.md) — runs alongside clarify-decisions to settle terms mid-interview
- [The skill model](../concepts/skill-model.md) — how primitives like this compose
