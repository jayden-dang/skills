# `draft-ux` — design source register

**Date:** 2026-08-25 · **Status:** pre-build research · **Decision taken:** a
separate `skills/craft/draft-ux`, not an expansion of `draft-ui` ·
**Companions:** the future `draft-ux/SKILL.md` + `TESTS.md`, a Step-0 amendment
to `skills/craft/draft-ui`, and a Step-2b lift in `skills/spec/design-solution`

`TESTS.md` will record *what was measured and what rule it produced*. This file
records *where each claim came from and how far it was actually read* — because
several claims behind this design shipped on search-result summaries rather than
source text, and a reader deciding whether to trust a rule needs to know which.
A **second pass on 2026-08-25** (§ *Verified on a second pass*) closed most of
those and corrected one attribution outright; the tiers below say where each
claim now stands.

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
| `hx-trigger="keyup changed delay:500ms"` | [`attributes/hx-trigger.md`](https://github.com/bigskysoftware/htmx/blob/master/www/content/attributes/hx-trigger.md), [`docs.md`](https://github.com/bigskysoftware/htmx/blob/master/www/content/docs.md) — retrieved on the second pass | Explicit vs implicit trigger; `changed` + `delay` debounce (`hx-sync` cancels the in-flight request the debounce still lets through) |

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

## B — unverified when the skill was written, re-checked on a second pass

Three of the four rows below were verified on 2026-08-25 after the skill shipped;
see the next section for what each check returned. Only the Saffer row still
carries a caveat, and one row's **attribution turned out to be wrong**.

| Claim | Where it entered | Status after re-check |
|---|---|---|
| Storybook 10.3 ships an **MCP server for React** letting an agent query design-system components, reuse them, write stories, and run focused component + a11y tests, with failures tied to specific stories | Search-result summary; the page fetch failed | **Confirmed, tier A** — every sub-claim quoted from primary text, plus a caveat the note had missed |
| A microinteraction decomposes into **trigger / rules / feedback / loops & modes** (Dan Saffer) | Search-result summary | **Partly confirmed** — naming and order corroborated by convergent book-specific sources; the book's own text remains unread |
| Static mockups cannot expose feedback loops, transition timing, or response patterns | Search-result summary | **Still tier B.** Not re-checked; it states the premise this skill's RED evidence independently demonstrated, so nothing rests on it |
| Response-time budgets ≈ **0.1 s / 1 s / 10 s**, attributed to Miller, Card et al., and Nielsen | Recalled, not retrieved | **Numbers confirmed, tier A — attribution corrected.** The triad is Nielsen's synthesis, not Miller's |

## Verified on a second pass (2026-08-25)

Three checks, each run against primary sources with instructions to quote the
page and to say whether the page itself or only a snippet was read.

### Storybook MCP — confirmed, and one caveat added

[Storybook 10.3 release post](https://storybook.js.org/blog/storybook-10-3/)
(6 Apr 2026) fetched successfully this time, and re-fetched as raw HTML to get
verbatim text: *"Storybook 10.3 adds MCP for React so AI agents can reuse real
components, write stories, and run focused component and accessibility tests."*
The [/ai page](https://storybook.js.org/ai) carries the rest verbatim —
*"Force agents to reuse existing components instead of inventing new ones or
hallucinating"*, and *"Failures are tied to specific stories and assertions so
agents know what to fix."*

Detail the first pass never had: three toolsets (Dev / Docs / Test) exposing
`list-all-documentation`, `get-documentation`, `get-storybook-story-instructions`,
and `run-story-tests`; installed with `npx storybook add @storybook/addon-mcp`,
served at `http://localhost:6006/mcp`.

**The caveat this note was missing**, from
[the docs page](https://storybook.js.org/docs/ai/) — current at v10.5, so the
status has outlived the 10.3 release: *"🧪 Storybook's AI capabilities are
currently in preview and only supported for React projects. The API may change
in future releases."* The React-only limit therefore still holds, and the
adapter row it gates should be read as preview-grade.

### Response-time budgets — numbers confirmed, attribution corrected

[Response Times: The 3 Important Limits](https://www.nngroup.com/articles/response-times-3-important-limits/)
(Nielsen, 1993, excerpted from *Usability Engineering* ch. 5) read directly:
0.1 s is *"about the limit for having the user feel that the system is reacting
instantaneously"*; 1.0 s is *"about the limit for the user's flow of thought to
stay uninterrupted, even though the user will notice the delay"*; 10 s is
*"about the limit for keeping the user's attention focused on the dialogue"*.
Prescriptive: *"For delays of more than 1 second, indicate to the user that the
computer is working on the problem"*, while a percent-done indicator plus a
signposted way to interrupt is what ~10 s demands.
[Website Response Times](https://www.nngroup.com/articles/website-response-times/)
(2010) reaffirms all three.

**The correction:** Miller (1968) was read as the actual AFIPS PDF, and it does
**not** state the triad. Miller's own thresholds are a **two-second rule** for
thought continuity and **15 seconds** — not 10 — for the point past which
conversational interaction is ruled out; his 0.1 s is keystroke feedback. The
clean 0.1 / 1 / 10 packaging is **Nielsen's synthesis**, citing Miller and Card
et al. as background. Attribute it to Nielsen 1993. Card, Robertson & Mackinlay
(1991) was not retrieved and stays unverified.

→ `draft-ux` §3's sentence — *"work that finishes in about a tenth of a second
reads as instant; past about a second of silence the user needs a pending
state"* — is a faithful compression of the prescriptive text and needs no edit.

### Saffer's four parts — attribution stands, the book does not

Every route to the book's own prose returned HTTP 403 (O'Reilly, Amazon,
archive.org, a full-text mirror). What was read in full:
[Interaction Design Foundation](https://ixdf.org/literature/article/micro-interactions-ux)
— *"Dan Saffer, in his book Microinteractions: Designing with Details, breaks
down the key components of micro-interactions into four essential parts: the
trigger, the rules, feedback and loops/modes"* — corroborated independently by
[Cieden](https://cieden.com/book/sub-atomic/microinteractions/structure-of-microinteractions),
and consistent with the book's chapter titles (2 Triggers, 3 Rules, 4 Feedback,
5 Loops and Modes). No source anywhere proposes a different decomposition.

One wrinkle worth carrying: the publisher's jacket copy lists *five* topics —
"triggers, rules, feedback, modes, and loops" — so "loops and modes" as a single
named unit may be explainers' phrasing rather than Saffer's own. Keep the
attribution; say it rests on book-specific secondary sources, not on the text.

## C — background

Surfaced during search, shaped framing, produced no rule: the UX Design
Institute and Brand Vision microinteraction overviews; the several
"AI + Storybook" workflow posts (Zencity, Open Self Service, UXPin's
Cursor + Storybook piece) — all describing the same reuse-first stance the
repo's own ladder already encodes.

---

## D — retrieval failed

- [storybook.js.org/blog/storybook-10-3](https://storybook.js.org/blog/storybook-10-3/)
  — WebFetch returned an empty error **on the first pass**. It fetched cleanly on
  the second pass (see above), so nothing in this file rests on that failure any
  more. Kept as a record of why the claim shipped at tier B.

---

## What the evidence constrains in the skill

### 1. There is no single mount mechanism — the skill must pick an adapter

| Context | Mount the real component with | Make it live with |
|---|---|---|
| SPA already running | The path `draft-ui` §2 already defines: real route, real data, subtree swap on `?variant=` — importing the real components | MSW (`delay`, error overrides) |
| React + a design system | Storybook manifest / MCP *(confirmed; preview, React-only)*, `play` functions as runnable interaction scenarios | The story itself |
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

## What RED did to this plan (2026-08-25, after the fact)

The skill shipped as `skills/craft/draft-ux` v1.0.0. Baseline runs cut three of
the five constraints above — recorded here because a plan that survives its own
test unchanged usually was not tested:

- **§2's reuse ladder became a no-op.** Both baseline reps already built from
  the existing kit and one explicitly refused to add a toast variant "so the
  locked look isn't reopened for one state". No rule was written for it, and the
  Step-0 amendment to `draft-ui` was **not made** — it has no observed failure
  behind it yet.
- **The `Focus & keyboard` slot became a no-op.** Both reps moved focus to the
  toast action unprompted.
- **The adapter matrix did not ship.** The fixture is a static app, so nothing in
  it exercised the React / server-rendered / Storybook lanes. Untested text does
  not go in a skill; the matrix stays here, as research.
- **What survived, because it failed:** the divergence requirement (two reps,
  opposite flows, each certain the requirements forced it), the no-lock-without-a-go
  gate (three iterations to close), the single home for the decision (one rep
  filed a sibling `interaction-brief.md` Step 2b cannot reach, then edited an
  Approved `requirements.md` to compensate), numbers carrying reasons, and the
  cleanup boundary.
- **A slot shape the plan did not predict:** the winning form was not the six
  slots proposed above but one `###` per moment filling the *same five slots* the
  visual sections use — which is what makes Step 2b lift it with no change to
  `design-solution`.

## Open verification work

Closed on the second pass: the Storybook MCP capabilities (confirmed, with the
preview/React-only caveat added), and the response-time budgets (numbers
confirmed, attribution corrected to Nielsen 1993). Neither forced a change to
the skill text; the second cost this note a wrong attribution.

Still open:

1. **Card, Robertson & Mackinlay (1991)** — cited by NN/g as background for the
   response-time advice, never retrieved here. Nothing rests on it now that the
   triad is attributed to Nielsen.
2. **Saffer's own text** — the four-part decomposition is corroborated only by
   sources describing the book; every route to the book returned 403. If this
   attribution ever needs to survive a footnote, read the book, and settle the
   four-versus-five wrinkle in the jacket copy.
3. **The adapter matrix is still untested** — the React, server-rendered, and
   Storybook lanes have never been exercised by a RED run. It remains research,
   not skill text, until a fixture on one of those stacks says otherwise.

## Search queries run

```
interaction prototype fidelity "microinteractions" trigger rules feedback loops modes spec 2025
Storybook stories as prototype existing components reuse design review AI agent 2026
ctx7 library: htmx — how htmx swaps HTML fragments and whether it can mount existing framework components
ctx7 docs: hx-indicator loading states, hx-confirm, hx-disabled-elt, hx-swap transitions for prototyping interaction feedback
ctx7 docs: hx-swap timing modifiers swap settle delay, out of band swaps, htmx.process for dynamically added content, using htmx with web components and existing JS frameworks
ctx7 library + docs: Mock Service Worker — simulate latency with delay() and return error responses in browser handlers for prototyping loading and error states
```
