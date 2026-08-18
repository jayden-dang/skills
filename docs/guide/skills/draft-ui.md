# `draft-ui`

> Deciding what a screen should look like is a workflow, not a one-shot render: divergent directions as real HTML the user clicks through, a review-and-amend loop, and a locked brief the build chain reads instead of re-deciding.

|  |  |
|---|---|
| **Bucket** | craft |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the user's direction; `docs/standards/design-tokens.md` or the repo's token/theme files; the feature's requirements when they exist |
| **Writes** | draft variants + switcher (deleted at the end); the surviving `ui-brief.md` + one screenshot |
| **Calls** | [`craft-page`](craft-page.md) (§2 plan discipline, once per variant) |
| **Called by** | [`run-spike`](run-spike.md) (its UI branch routes here) |

## When it fires

"What should this look like?", "show me a few design directions", "make variants and let me pick" — before a surface is specified or built. `run-spike` hands its UI branch here; logic/state spikes stay with `run-spike`.

## The workflow

1. **Plan N directions** (default 3, max 5) — each variant gets its own named Color/Type/Layout plan plus a Signature line, via `craft-page` §2. Directions diverge on **design, not only structure**: identical palette, type, and density across variants is one direction laid out three ways.
2. **Build real HTML** — embedded in the running app behind a `?variant=` switcher (real header, real data, real density), or standalone pages behind the same bar when no app exists. Real content, read-only, mutations stubbed.
3. **Review loop** — URL + one-line pitch per variant; collect the pick (usually a hybrid) *and its amendments*; apply, show again; repeat. Lock only on the user's explicit go.
4. **Lock** — write `ui-brief.md` (feature spec dir, else `docs/design/`) whose slots mirror `design.md`'s `## UI design` 1:1, plus the Decision in the user's words, the Signature, and the amendments log. Keep one screenshot.
5. **Clean up** — losing variants and switcher deleted; the winner is rewritten from the brief under `test-first`, never promoted as-is.

## Downstream

[`design-solution`](design-solution.md) Step 2b lifts `## UI design` from an existing ui-brief instead of re-deciding. A brief authored before any spec waits in `docs/design/` for the feature that adopts it.
