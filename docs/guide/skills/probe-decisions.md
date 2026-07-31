# `probe-decisions`

> The interview primitive. One full-context question card per message — radius, why it matters, options with consequences, and a recommendation — until you and the user hold the same picture, sealed by a decisions table and explicit confirmation.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the codebase and docs — to look up every fact before asking about it; parent Knowns / Blindspot digests when present |
| **Writes** | nothing production; it enacts no code, files, or plan execution (glossary side effects via `define-domain` only) |
| **Calls** | — (a pure interview primitive; may hand unknown-knowns to the parent's `run-spike` / `research` detour) |
| **Called by** | [`frame-change`](frame-change.md) (its required interview step); any skill whose work calls for an interview |

## When it fires

Whenever intent is underspecified and the decisions must be drawn out of the user: to stress-test a plan, design, or feature idea before anything is built, when the user asks to be grilled or interviewed, or when another skill calls for an interview.

[`frame-change`](frame-change.md) invokes it as a required sub-skill for its whole interview step, and other design skills reach for it the same way. It is a primitive — it does one thing, holds no state of its own, and hands the picture it draws to whatever skill called it.

## Channel: inline chat only

Every question is ordinary chat with **full context**. The skill forbids `AskUserQuestion` and any harness MCQ UI that truncates labels, option text, or the "why this matters" line. A tap-friendly picker that strips consequences is a different, worse interview — not a speed optimization.

## The question card

Exactly one decision per message, in this shape:

1. **Radius** — `architecture` · `data` · `auth/security` · `UX flow` · `polish-diff`
2. **Question** — the decision in plain language
3. **Why it matters** — what changes in the system if the answer flips (queue vs sync, schema, permission boundary, scope), grounded in this repo when possible
4. **Options (2–4)** — each title **plus** a consequence line (gain, cost, what breaks)
5. **Recommendation** — marked pick + one-line reason (accept in two words or push back)
6. **Stop** and wait

Blast-radius first — even when the user asks to start with polish. Facts are looked up; only judgment calls go to the user. Project posture and team band right-size which branches are walked (same rules as before).

## Unknowns the interview closes

The map (prompts, plans) is not the territory (codebase, runtime, users, history). Probe Decisions shrinks that gap before wrong guesses get expensive:

- Load the parent's Knowns inventory and Blindspot list when they exist; turn high-blast landmines into cards or confirmed locks
- Prefer territory-grounded forks (share-link egress, dual-write traps, flag skew, historical reverts) over generic taste questions
- When the user can only "know it when they see it," offer a **reference path** (point at a module and restate its semantics) or hand off to `run-spike` / `research`, then resume with one card
- "Just make something sensible" is not a decision while an in-repo reference exists

## Close package

When no branch remains, and **before** handing back to a parent or claiming alignment, the agent emits:

1. A **decisions table** (radius · topic · decision)
2. A **constraints block** ready to paste into the next stage
3. An ask for **explicit confirmation** on that package

"Any other questions?", "we're aligned — skip the table", and "just go write requirements" are not confirmation. Nothing is enacted until the yes lands on the package.

## Worked example

The user wants annotation export. Rather than a truncated picker or a questionnaire dump, `probe-decisions` walks architecture first:

> **architecture** · Question 1
>
> Where should export generation run?
>
> ↳ This decides whether we need a job queue, a ready-notification path, and an artifacts bucket — or none of those. Large reviews will blow a 30s gateway timeout on the request thread.
>
> - **Sync in the API request** — simplest; a 400-comment export times out.
> - **Background job on the existing queue** (Recommended) — reuses transcode worker patterns; needs a "ready" notification.
> - **Client-side only** — zero backend; caps formats and helps support less.
>
> Recommended: background job — export size is unpredictable with drawings.

Later, after every branch is closed, a decisions table and constraints block are confirmed before `frame-change` continues.

## Why it is written the way it is

Three baseline failures drove the current text:

1. **Truncated channel** — under time or "house style" pressure, agents reach for structured MCQ tools that drop consequences; users cannot push back on merits.
2. **Thin questions** — "Recommended: X — safer" without option consequences trains rubber-stamp answers and leaves architecture debt unexamined.
3. **Ceremony skip at the close** — "we're aligned" without a decisions package lets silent assumptions leak into requirements.

The no-enactment rule keeps `probe-decisions` a pure interview: it draws the picture, and another skill builds from it.

## See also

- [`frame-change`](frame-change.md) — the primary caller; probe-decisions is its interview step
- [`research`](research.md) — where a factual question too big to just look up gets sent
- [`run-spike`](run-spike.md) — where unknown knowns need a visible throwaway answer
- [`define-domain`](define-domain.md) — runs alongside probe-decisions to settle terms mid-interview
- [The skill model](../concepts/skill-model.md) — how primitives like this compose
