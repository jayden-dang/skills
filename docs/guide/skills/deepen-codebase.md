# `deepen-codebase`

> Native-language **learning companion** for deep foundational knowledge of any
> codebase topic or technical subject. Dual-axis curriculum (what kind of knowing ×
> which layer of the system), slow and deep, diagrams and failure modes — **without**
> shipping a product decision. Optional third session beside real work.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | user-invoked (`/deepen-codebase`) — a session mode you turn on, not auto-fired |
| **Reads** | the topic anchor (paste, path, symptom, question); codebase for as-is; optional `research` notes |
| **Writes** | nothing tracked; may disclose git-ignored `.skills/research/` notes only via `research` |
| **Calls** | [`research`](research.md) when a named external claim needs an owning source |
| **Called by** | — (run directly; may run parallel to any work session) |
| **Optional packet** | `foundation-note/v1` — knowledge only, on request |

## When it fires

You want to **understand** a subject deeply enough that later decisions are yours:
a module you are about to change, a design fork in another window, a bug class,
onboarding a subsystem, greenfield literacy before you design, debt you keep
tripping over. **Any subject** — the skill re-derives a must-know map each time;
it is not a fixed course in one domain.

Typical three-session layout (optional):

1. Main work — `frame-change`, implement, debug, …  
2. [`interpret-session`](interpret-session.md) — stance + English reply  
3. **`deepen-codebase`** — foundation, mechanisms, as-is, gaps, failure modes  

Session 3 does not require sessions 1–2. It does not replace interpret or teach-pack.

## What it builds

**Axis A — kind of knowledge:** factual · conceptual · procedural · metacognitive  

**Axis B — layers:** problem fundamentals (F0) → ontology (F1) → reference
architectures (F2, cited) → mechanisms (F3) → platform conventions (F4) → this-repo
as-is (F5) → evaluated practice (F6) → gap → unranked delta → fail/eval → ops  

The four comparison layers (as-is · reference · gap · delta) are the **change
lens** when an option is live. They sit **on top of** foundation, not instead of it.

**"Standard" is laddered:** fundamental (F0–F1) · named reference with source
(F2–F3) · platform docs (F4) · this repo (F5). No source → inference, never
"industry standard."

## Setup (once)

Target language · learner familiarity/goal/pace · reused project posture (risk
language only) · **subject lock** (name + anchor).

## Philosophy

Slow and deep. Every teaching turn **announces** subject + primary layer + kind,
then teaches **only** that layer. Soft probe only when a new F0/F1 boundary
appeared. Delta/options require F0+F1 first, or user-recorded
`foundation: explicitly_skipped` (urgency alone is not a skip). When the same gap
needs two re-explains, the skill **names** [`/teach-pack`](teach-pack.md) for
graded stickiness. Read-only toward the repo. Close with foundation cards, open
gaps, and `foundation:` status — never "learning complete" or "you are senior now."

## Validation

Pressure RED/GREEN on grok-4.5: demand-pick, bare "industry standard", ADR write,
domain lock-in, first-layer shape — **5/5 GREEN** after wording pass. Evidence:
`skills/discovery/deepen-codebase/TESTS.md`, `tests/deepen-codebase/`.

## Retired

Replaces **`thinking-practice`** (reasoning gym + train→ship hand-off to
interpret). Product stance and English replies stay on interpret-session only.

## See also

- [`interpret-session`](interpret-session.md) — decide + paste-back reply  
- [`teach-pack`](teach-pack.md) — graded multi-lesson workspace  
- [`research`](research.md) · [`study-change`](study-change.md)  
- [Discovery phase](../process/discovery.md) — companion sessions in the chain  
