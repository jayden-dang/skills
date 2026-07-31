# `dogfood`

> A human driving the real app through every user-facing ability and judging what they see. The deliverable is a **cases catalog** (YAML) plus a **rendered HTML guide** from a checked-in shell — not a chat message and not a bespoke CSS page every time.

|  |  |
|---|---|
| **Bucket** | acceptance |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the spec triad — `requirements.md`, `design.md`, `tasks.md`; the source (theme tokens, CSS, keyword and label definitions); `docs/agents/project.md` (the `## Run locally (dev)` command) |
| **Writes** | `.skills/<slug>-dogfood.json` (one run file: cases + verdicts) and `.skills/<slug>-dogfood.html` (rendered human view) |
| **Calls** | `dogfood` CLI (`scripts/dogfood render`); [`design-page`](design-page.md) **only** when the user asks for custom craft |
| **Called by** | [`acceptance-check`](acceptance-check.md), [`verify`](verify.md); hand-off path to [`drive-dogfood`](drive-dogfood.md) when the agent should run the guide |

## When it fires

When you are manually exercising a finished feature in the real running app from the user's seat — a hands-on pass, case by case, over every user-facing ability, including the visuals, feel, and edge cases a human must eyeball rather than an automated test or a quick launch.

It complements [`acceptance-ui`](acceptance-ui.md), which automates flows into tests. `dogfood` is the manual, eyeball-it sibling. To **execute** an already-written guide in the browser (with backend probes and a fix loop), use [`drive-dogfood`](drive-dogfood.md).

## 1. Scope — coverage gate

Same taxonomy and coverage rules as before: every user-facing ID has ≥1 case; every ability area has `happy` **and** a non-happy kind (or a greppable *Coverage exception*); Out-of-Scope gets `nonbehavior` when attemptable; persistence claims get `persist`.

Kinds: `happy` | `edge` | `error` | `nonbehavior` | `persist` | `visual` | `journey`.

## 2–3. Ground + boot

Ground Expect in real source (labels, theme tokens). Boot via `## Run locally (dev)`. Honest observation points for behaviors with no UI yet.

## 4. Cases YAML + shell render

**Authoring SSOT** is `.skills/<slug>-dogfood.json` — not hand-rolled HTML. Run
state (`run`, `human`) is filled in for you; author the eight case slots.

Required per case: `id`, `req`, `kind`, `title`, `setup`, `try`, `expect`, `backend` (server assertion or `presentational`).

Render the human companion:

```bash
python3 <dogfood-skill-root>/scripts/dogfood render .skills/<slug>-dogfood.json \
  -o .skills/<slug>-dogfood.html
```

The shell (`shell/guide.html`) already carries theme-aware CSS, kind chips, progress, and optional human localStorage ticks. **Do not** invent a full custom page by default; `design-page` is opt-in craft only.

Schema pointer: skill sibling `references/cases-schema.md`. Contract: `docs/specs/2026-07-27-dogfood-cli/contract.md`.

## 5. Hand over

Give **both** paths (YAML + HTML), the 30-second first pass, degraded-feature notes. Human ticks in HTML are optional. Agent runs go through [`drive-dogfood`](drive-dogfood.md) + CLI ledger — not Chrome ticks on the guide.

## Worked sketch

Notes feature → three cases in the run file (happy create, error empty title, persist reload) → `dogfood render` → hand `.skills/notes-dogfood.json` and `.skills/notes-dogfood.html`. Offer `dogfood serve` when they will also be testing by hand.

## Why it is written this way

Rebuilding CSS/JS every dogfood pass wasted tokens and tempted agents to treat localStorage as progress. Cases + shell matches the `comprehend-change` packet pattern: fixed shell, filled content. Agent progress for execution lives in the ledger CLI under `drive-dogfood`.

## See also

- [`drive-dogfood`](drive-dogfood.md) — execute cases with ledger + CLI
- [`acceptance-ui`](acceptance-ui.md) — automated sibling
- [`acceptance-check`](acceptance-check.md) — orchestrator
- [`verify`](verify.md) — names a manual dogfood pass for "the feature works"
