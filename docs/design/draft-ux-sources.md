# `draft-ux` — design source register

**Date:** 2026-08-25 · **Status:** pre-build research · **Decision taken:** a
separate `skills/craft/draft-ux`, not an expansion of `draft-ui` ·
**Companions:** the future `draft-ux/SKILL.md` + `TESTS.md`, a Step-0 amendment
to `skills/craft/draft-ui`, and a Step-2b lift in `skills/spec/design-solution`

`TESTS.md` will record *what was measured and what rule it produced*. This file
records *where each claim came from and how far it was actually read* — because
the two load-bearing external claims behind this design (what Storybook's MCP
gives an agent, and what a static mockup cannot reveal) were taken from
search-result summaries rather than source text, and a reader deciding whether
to trust a rule needs to know which.

## Evidence strength

| Tier | Meaning |
|---|---|
| **A — read** | Source text retrieved and read during the research session |
| **A′ — read through a summariser** | Page fetched, but the content reached this file as a model-written summary; wording is not quotable verbatim |
| **B — unverified** | Carried on a search-result summary **or** on unretrieved background knowledge. **Not verified against the source.** |
| **C — background** | Surfaced during search, informed framing, produced no rule |
| **D — unavailable** | Retrieval failed; contributed nothing beyond what a summary already carried |

---

## The gap this research was run against

Read directly from the repo (tier A, in-repo):

- `skills/craft/draft-ui/SKILL.md` §2 — *"Variants stay read-only — stub any
  mutation."* The prototype is deliberately dead, so no interaction decision can
  be made in it.
- `skills/craft/draft-ui/SKILL.md` §4 — the locked `ui-brief` slots are
  **Layout / Components / States / Type & color / A11y**. `States:` is a *list of
  static states*; nothing carries what triggers a transition, how long it takes,
  where feedback lands, how a mistake is recovered, or what a multi-step flow is.
- `skills/spec/design-solution/SKILL.md` §Step 2b — lifts exactly those five
  slots 1:1 and re-decides nothing. Any UX decision without a slot there dies in
  the branch.
- `skills/spec/design-solution/templates/design.md:60` — `Components:` already
  carries **ladder discipline** (`rung N — <target>`, or `new (rung 7)` + reason),
  but the ladder is only applied *after* the draft has already emitted new HTML.
- `review-ui`, `validate-ui`, `review-product-flow`, `run-product-walkthrough`
  all run **after** the build. Nothing in the chain decides UX before it.

Two gaps, therefore: **interaction is never decided**, and **existing components
are never inventoried before the draft invents markup**.

---

## A — read, and what each produced

### htmx · [/bigskysoftware/htmx](https://github.com/bigskysoftware/htmx) (v2.0.4; docs read via Context7)

Retrieved as documentation snippets from `www/content/`, not as full pages.

| Attribute | Source | What it settles |
|---|---|---|
| `hx-indicator="#spinner"` + `.htmx-request` | [`attributes/hx-indicator.md`](https://github.com/bigskysoftware/htmx/blob/master/www/content/attributes/hx-indicator.md) | Where the pending state lives |
| `hx-disabled-elt="inherit, find button"` | [`attributes/hx-disabled-elt.md`](https://github.com/bigskysoftware/htmx/blob/master/www/content/attributes/hx-disabled-elt.md) | Double-submit protection, inheritable down a form |
| `hx-confirm="…"` | [`migration-guide-intercooler.md`](https://github.com/bigskysoftware/htmx/blob/master/www/content/migration-guide-intercooler.md) | The destructive-action confirm |
| `hx-swap="innerHTML swap:100ms settle:50ms"` | [`attributes/hx-swap.md`](https://github.com/bigskysoftware/htmx/blob/master/www/content/attributes/hx-swap.md), [`docs.md`](https://github.com/bigskysoftware/htmx/blob/master/www/content/docs.md) | **Latency and animation timing simulated with no backend** |
| `hx-swap-oob` | [`attributes/hx-swap-oob.md`](https://github.com/bigskysoftware/htmx/blob/master/www/content/attributes/hx-swap-oob.md) | Feedback that lands somewhere other than the target — toast, badge count. Nested OOB is on by default (`htmx.config.allowNestedOobSwaps`); `tr`/`li`/SVG children need `<template>` wrappers |
| `hx-swap="innerHTML transition:true"` | [`essays/view-transitions.md`](https://github.com/bigskysoftware/htmx/blob/master/www/content/essays/view-transitions.md) | View Transitions on a swap |
| `hx-trigger="keyup changed delay:300ms"` | **not retrieved this session (tier B)** — asserted from background knowledge | Explicit vs implicit trigger, debounce |

→ **Rule produced:** htmx is adopted as the *interaction engine* for the
no-app and server-rendered lanes — the seven rows above are close to the whole
question set a UX draft has to answer, and they are answerable in attributes,
with no state management and no backend (fragments can be static `.html` files
behind any static server).

### htmx and component mounting · [`essays/webcomponents-work-great.md`](https://github.com/bigskysoftware/htmx/blob/master/www/content/essays/webcomponents-work-great.md)

htmx's model is: every interaction is an HTTP request returning an **HTML
fragment** that gets swapped into the DOM. The essay's own framing — htmx "is not
a traditional JavaScript framework", and its fetch-and-insert approach "aligns
perfectly with the DOM-based lifecycles of custom elements" — is also the boundary
of what it can mount.

→ **Rule produced:** htmx mounts an existing component **only where that component
already exists as server-rendered HTML** (Django, Rails, Laravel, Go templates,
Phoenix, Razor) or as a Web Component. On a compiled SPA component (React, Vue,
Svelte) there is no HTML endpoint to `hx-get`, so htmx would force a hand-written
copy of the component's markup — reproducing the exact defect this work exists to
remove, and adding a second source of truth. **htmx is rejected as the general
component-reuse mechanism and accepted as the interaction engine.**

### MSW · [/mswjs/mswjs.io](https://github.com/mswjs/mswjs.io) (docs read via Context7)

- [`http/mocking-responses/response-timing.mdx`](https://github.com/mswjs/mswjs.io/blob/main/websites/mswjs.io/src/content/docs/http/mocking-responses/response-timing.mdx)
  — `await delay(500)` inside a handler delays one response.
- [`http/mocking-responses/error-responses.mdx`](https://github.com/mswjs/mswjs.io/blob/main/websites/mswjs.io/src/content/docs/http/mocking-responses/error-responses.mdx)
  — `new HttpResponse(null, { status: 404 })` / `500` returns a real error to the
  real client code.
- [`best-practices/structuring-handlers.mdx`](https://github.com/mswjs/mswjs.io/blob/main/websites/mswjs.io/src/content/docs/best-practices/structuring-handlers.mdx)
  — happy paths live in `handlers.js`; error scenarios arrive as runtime overrides
  (`server.use(...)`), keeping the base set clean.

→ **Rule produced:** in the SPA lane, pending / error / empty are made
*experienceable* by intercepting the network, not by faking component props.
`draft-ui` §2 already embeds variants in the real running app with real data;
MSW is what makes that embedded surface answer UX questions without touching
app code. The delay values are a **decision**, recorded in the brief — not a
per-variant whim.

---

## A′ — read through a summariser

### [Best practices for using Storybook with AI](https://storybook.js.org/docs/ai/best-practices) · Storybook docs

Fetched; content reached this file as a summary. What it carries:

- The AI features are **React-only at present**, with API changes expected.
- Agents read a **manifest**; `tags: ['!manifest']` excludes stories from what an
  agent sees.
- Prop extraction quality depends on `react-docgen-typescript`; JSDoc on the
  component explains *when to use it and what the alternatives are*.
- Values that are only rendered dynamically (the page's example is colour tokens)
  do **not** reach the manifest — the agent sees source, not runtime.

→ **Rule produced:** Storybook is an *adapter* in the React lane, not the
foundation of the skill. A skill that assumed it would exclude every non-React
repo, and would inherit a manifest whose completeness depends on repo hygiene the
skill does not control.

---

## B — unverified: carried on a summary or on background knowledge

| Claim | Where it entered | What it gates |
|---|---|---|
| Storybook 10.3 ships an **MCP server for React** letting an agent query design-system components, reuse them, write stories, and run focused component + a11y tests, with failures tied to specific stories | Search-result summary of [storybook.js.org/blog/storybook-10-3](https://storybook.js.org/blog/storybook-10-3/) — **the page fetch failed** (see tier D) | The React-lane adapter row of the matrix. If it is weaker than summarised, that lane falls back to the app-embedded route, which is already proven |
| A microinteraction decomposes into **trigger / rules / feedback / loops & modes** (Dan Saffer), still the working frame in 2025 | Search-result summary; [structure of microinteractions](https://cieden.com/book/sub-atomic/microinteractions/structure-of-microinteractions), [UXPin](https://www.uxpin.com/studio/blog/microinteractions-for-protypes/) | The *shape of the `ux-brief` slots*. Not retrieved from Saffer's text |
| Static mockups cannot expose feedback loops, transition timing, or response patterns; higher-fidelity interaction prototypes surface usability failures static testing misses | Search-result summary, same query | The premise that the prototype must be **runnable**, not described. Plausible and consistent with `draft-ui`'s own "real HTML is the medium" stance, but unverified as stated |
| Response-time budgets ≈ **0.1 s** feels instant, **1 s** keeps the flow of thought, **10 s** is the attention limit (Nielsen / Miller / Card) | **Recalled, not retrieved this session** | The numeric defaults in the `Timing:` slot. Verify before writing specific numbers into the skill |

The first row is the load-bearing one: it is the only reason the React lane
gets a component-aware adapter at all rather than defaulting to the
already-working app-embedded path.

---

## C — background

Surfaced during search, shaped framing, produced no rule: the UX Design
Institute and Brand Vision microinteraction overviews; the several
"AI + Storybook" workflow posts (Zencity, Open Self Service, UXPin's
Cursor + Storybook piece) — all describing the same reuse-first stance the
repo's own ladder already encodes.

---

## D — retrieval failed

- [storybook.js.org/blog/storybook-10-3](https://storybook.js.org/blog/storybook-10-3/)
  — WebFetch returned an empty error. Everything attributed to Storybook 10.3 in
  this file is therefore **tier B**, from the search summary.

---

## What the evidence constrains in the skill

### 1. There is no single mount mechanism — the skill must pick an adapter

| Context | Mount the real component with | Make it live with |
|---|---|---|
| SPA already running | The path `draft-ui` §2 already defines: real route, real data, subtree swap on `?variant=` — importing the real components | MSW (`delay`, error overrides) |
| React + a design system | Storybook manifest / MCP *(tier B)*, `play` functions as runnable interaction scenarios | The story itself |
| Server-rendered | The real partial | htmx attributes |
| No app / no component library | Standalone pages, as `draft-ui` does today | htmx + static HTML fragments |

### 2. A UI reuse ladder belongs *before* the draft, not after it

`design-solution` already speaks `rung N — <target>` / `new (rung 7)` + reason for
`Components:`. The same discipline moves earlier: a Step 0 in `draft-ui`
inventories existing components and tokens, and new markup becomes rung 7 with a
stated reason. This is the amendment to `draft-ui`; it is small and does not make
that skill own interaction.

### 3. The decision must land in a slot `design-solution` lifts

Proposed `ux-brief` slots, per surface: **Flow** (steps, entry, exit, abandon
point) · **Trigger → Feedback** (per action: trigger, immediate response, pending
state, result, where it lands) · **Timing** (deliberate ms budget per transition)
· **Recovery** (error path; optimistic + undo vs confirm dialog) · **Focus &
keyboard** (where focus goes *after each swap*, ESC, Enter) · **Modes** (sticky
states: edit mode, selection mode). Step 2b lifts them 1:1, exactly as it lifts
the five visual slots.

The focus slot is not decoration: focus loss after a DOM swap is the failure both
htmx and SPA lanes share, and today it is only caught by `review-ui`, after build.

### 4. Throwaway discipline has to survive mounting real components

`draft-ui` §5 deletes the variants and rewrites from the brief under
`test-first`. Mounting real components blurs that line, so the rule must be
explicit: **fragments, mocks, the switcher, and htmx itself are scaffolding and
are deleted; what survives is the brief plus the chosen-component list (rung +
target).** htmx and MSW must not reach a production build, and neither is
proposed as a dependency of the app in the SPA lane.

### 5. Why a separate skill rather than a bigger `draft-ui`

When a project already has reusable components, the *look* question is largely
pre-decided — which is precisely the case that motivated this research. A UX lane
that can only run as the tail of a look-exploration would be unreachable in its
main use case. `draft-ux` therefore consumes a locked `ui-brief` **or** runs
standalone against an existing design system. Cost accepted: a second lock/review
loop that duplicates machinery `draft-ui` already has, and one more hand-off in
the chain.

---

## Open verification work

1. Read the Storybook 10.3 release post directly (fetch failed here) and confirm
   what the MCP server actually exposes, and whether the React-only limitation
   still holds. This gates the React adapter row.
2. Retrieve the response-time budgets from a primary source before any specific
   ms number is written into the `Timing:` slot.
3. Confirm the microinteraction decomposition against Saffer's text, or attribute
   the slot shape to this design instead of to him.
4. None of the three blocks building the skill; all three change how firmly its
   rationale can be stated.

## Search queries run

```
interaction prototype fidelity "microinteractions" trigger rules feedback loops modes spec 2025
Storybook stories as prototype existing components reuse design review AI agent 2026
ctx7 library: htmx — how htmx swaps HTML fragments and whether it can mount existing framework components
ctx7 docs: hx-indicator loading states, hx-confirm, hx-disabled-elt, hx-swap transitions for prototyping interaction feedback
ctx7 docs: hx-swap timing modifiers swap settle delay, out of band swaps, htmx.process for dynamically added content, using htmx with web components and existing JS frameworks
ctx7 library + docs: Mock Service Worker — simulate latency with delay() and return error responses in browser handlers for prototyping loading and error states
```
