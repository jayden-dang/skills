# UI prototype

Several structurally different takes on one screen, all mounted on a single route and flipped between with a floating switcher. The user browses them in the running app, picks a winner (or a hybrid), and the rest gets deleted. If the question is about logic or state rather than looks, wrong branch: see [LOGIC.md](LOGIC.md).

## Embed in an existing page — the default

A variant judged in a vacuum always looks fine. Against the real header, real sidebar, real data, and real density, the weak ones expose themselves. So:

- **Default: host the variants inside an existing page.** The route, data fetching, params, and auth all stay; only the rendered subtree swaps per variant. This also covers new sections that would naturally live inside an existing page — mount the variants there.
- **Last resort: a new throwaway route**, only when there is genuinely no page to embed in (an entirely new top-level surface). Follow the project's routing conventions, put `prototype` in the path or filename, and sanity-check first: is there really nowhere to embed this?

## Process

### 1. State the plan and pick N

Default **3 variants; never more than 5** — beyond that they stop being different and start being noise. Record the plan in one line at the prototype's location, e.g. "Three variants of the billing screen on the existing `/billing` route, switched by `?variant=`."

### 2. Draft structurally different variants

Every variant must respect the page's purpose, the data it actually has, and the project's existing component library and styling system. Export each under a clear name (`VariantA`, `VariantB`, ...).

**Structurally different means different layout, different information hierarchy, different primary affordance** — not the same layout in new colors or copy. If two drafts converge, redo one under an explicit structural constraint ("no card grid this time"). Variants may share small leaf components; sharing the layout defeats the exercise.

### 3. Wire the switcher route

One route reads a `?variant=` query param (defaulting to the first variant) and renders the matching component, with the shared floating switcher rendered alongside. Data fetching stays above the switch so all variants get identical real data. Variants stay read-only — if one needs a mutation, stub it; "does the backend work" is not the question.

### 4. Build the floating switcher

A small fixed bar, bottom-center: previous arrow, current variant label (key plus name, e.g. `B — split view`), next arrow, cycling with wrap-around.

- Arrows update the URL query param through the framework's router, so a variant is shareable and survives reload.
- Left/right arrow keys also cycle — but not while an input, textarea, or contenteditable element has focus.
- Style it to obviously not belong to the design under evaluation (high-contrast pill, shadow).
- **Hidden in production builds** — gate it on the project's dev/prod check so an accidental merge can never show users the switcher.
- Build it once as a shared component wherever the project keeps shared UI.

### 5. Hand it over

Give the user the URL and the variant keys. The best feedback is usually a hybrid — "A's layout with C's detail panel" — and that hybrid is the real answer.

### 6. Capture the answer and clean up

Record which variant (or hybrid) won and why — ADR, requirement, or the commit message that does the cleanup (see SKILL.md). Then delete the losing variants and the switcher, and fold the winner in properly: variant code was written under prototype constraints, so rewrite it to production standard rather than promoting it as-is. Leave nothing behind.
