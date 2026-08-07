# `review-product-flow`

> A human driving the real app through every user-facing ability and judging what they see. The deliverable is a **cases catalog** (YAML) plus a **rendered HTML guide** from a checked-in shell — not a chat message and not a bespoke CSS page every time.

|  |  |
|---|---|
| **Bucket** | acceptance |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the spec triad — `requirements.md`, `design.md`, `tasks.md`; the source (theme tokens, CSS, keyword and label definitions); `docs/agents/project.md` (the `## Run locally (dev)` command) |
| **Writes** | `.skills/<slug>-review-product-flow.json` (one run file: cases + verdicts) and `.skills/<slug>-review-product-flow.html` (rendered human view) |
| **Calls** | `review-product-flow` CLI (`scripts/review-product-flow render`); **immediately** [`vet-product-flow`](vet-product-flow.md) after the run file exists; [`craft-page`](craft-page.md) **only** when the user asks for custom craft |
| **Called by** | [`validate-feature`](validate-feature.md), [`prove-claim`](prove-claim.md); hand-off path to [`run-product-walkthrough`](run-product-walkthrough.md) only after a clean vet report |

## When it fires

When you are manually exercising a finished feature in the real running app from the user's seat — a hands-on pass, case by case, over every user-facing ability, including the visuals, feel, and edge cases a human must eyeball rather than an automated test or a quick launch.

It complements [`validate-ui`](validate-ui.md), which automates flows into tests. `review-product-flow` is the manual, eyeball-it sibling. To **execute** an already-written guide in the browser (with backend probes and a fix loop), use [`run-product-walkthrough`](run-product-walkthrough.md).

## 1. Scope — coverage gate

Same taxonomy and coverage rules as before: every user-facing ID has ≥1 case; every ability area has `happy` **and** a non-happy kind (or a greppable *Coverage exception*); Out-of-Scope gets `nonbehavior` when attemptable; persistence claims get `persist`.

Kinds: `happy` | `edge` | `error` | `nonbehavior` | `persist` | `visual` | `journey`.

## 2–3. Ground + boot

Ground Expect in real source (labels, theme tokens). Boot via `## Run locally (dev)`. Honest observation points for behaviors with no UI yet.

## 4. Cases YAML + shell render

**Authoring SSOT** is `.skills/<slug>-review-product-flow.json` — not hand-rolled HTML. Run
state (`run`, `human`) is filled in for you; author the eight case slots.

Required per case: `id`, `req`, `kind`, `title`, `setup`, `try`, `expect`, `backend` (server assertion or `presentational`).

Render the human companion:

```bash
python3 <review-product-flow-skill-root>/scripts/review-product-flow render .skills/<slug>-review-product-flow.json \
  -o .skills/<slug>-review-product-flow.html
```

The shell (`shell/guide.html`) already carries theme-aware CSS, kind chips, progress, and optional human localStorage ticks. **Do not** invent a full custom page by default; `craft-page` is opt-in craft only.

Schema pointer: skill sibling `references/cases-schema.md`. Contract: `docs/specs/2026-07-27-review-product-flow-cli/contract.md`.

## Todos + 5. Hand over

Create one todo per section (1–4) **and** a terminal **Vet product flow** todo
(created now; check off only when the vet report exists).

After the run file + HTML are on disk: **IMMEDIATELY** run
[`vet-product-flow`](vet-product-flow.md). Give both artifact paths, the
30-second first pass, degraded-feature notes. Human ticks in HTML are optional.
Name [`run-product-walkthrough`](run-product-walkthrough.md) only after a clean
vet report (or named override).

## Worked sketch

Notes feature → three cases in the run file → `review-product-flow render` →
**immediately** `vet-product-flow` → report on disk → hand run file + HTML.
Offer `review-product-flow serve` when they will also be testing by hand.

## Why it is written this way

Rebuilding CSS/JS every review-product-flow pass wasted tokens and tempted agents to treat localStorage as progress. Cases + shell matches the `study-change` packet pattern: fixed shell, filled content. Agent progress for execution lives in the ledger CLI under `run-product-walkthrough`.

## See also

- [`run-product-walkthrough`](run-product-walkthrough.md) — execute cases with ledger + CLI
- [`validate-ui`](validate-ui.md) — automated sibling
- [`validate-feature`](validate-feature.md) — orchestrator
- [`prove-claim`](prove-claim.md) — names a manual review-product-flow pass for "the feature works"
