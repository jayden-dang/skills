# `draft-ui`

> Deciding what a screen should look like is a workflow, not a one-shot render: divergent directions as real HTML the user clicks through, a review-and-amend loop, and a locked brief the build chain reads instead of re-deciding.

|  |  |
|---|---|
| **Bucket** | craft |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the user's direction; `docs/standards/design-tokens.md` or the repo's token/theme files; the component kit screens already build from; the feature's requirements when they exist |
| **Writes** | draft variants + switcher (deleted at the end); a `ui-brief.md` when the surface has no UI design yet, or an in-place promotion plus updated `## UI design` when it already ships |
| **Calls** | [`craft-page`](craft-page.md) (§2 plan discipline, once per variant) |
| **Called by** | [`run-spike`](run-spike.md) (its UI branch routes here) |

## When it fires

"What should this look like?", "show me a few design directions", "make variants and let me pick" — before a surface is specified or built. `run-spike` hands its UI branch here; logic/state spikes stay with `run-spike`.

## The workflow

1. **Plan N directions** (default 3, max 5) — each variant gets its own named Color/Type/Layout plan plus a Signature line, via `craft-page` §2. Directions diverge on **design, not only structure**: identical palette, type, and density across variants is one direction laid out three ways. For a screen people work in (a dashboard, queue, admin or tool view), three lines come first — the **Question** the person opening it must answer, the **Finding** in today's data that answers it, and the **Primary job** it calls for — and every variant shows the finding in words with the job's control beside it, on the object the finding names.
2. **Build real HTML** — embedded in the running app behind a `?variant=` switcher (real header, real data, real density), or standalone pages behind the same bar when no app exists. Real content, read-only, mutations stubbed. Controls the kit already ships are composed from it, never re-declared under a variant class — a rebuilt button silently drops the focus and disabled states the kit carried.
3. **Review loop** — URL + one-line pitch per variant; collect the pick (usually a hybrid) *and its amendments*; apply, show again; repeat. Lock only on the user's explicit go.
4. **Shipped surface** — when an owning `design.md` already has `## UI design` and the winner changes no spec'd behavior, promote the winner, update those lines, and do not write a ui-brief (added behavior goes through `amend-feature`). Otherwise **lock** — write `ui-brief.md` (feature spec dir, else `docs/design/`) whose slots mirror `design.md`'s `## UI design` 1:1, plus the Decision in the user's words, the Signature, the `Job:` line for a worked-in screen, and the amendments log. Keep one screenshot.
5. **Clean up** — on the unshipped path only: losing variants and switcher deleted; the winner is rewritten from the brief under `test-first`. A shipped surface already finished at step 4.

## Downstream

[`design-solution`](design-solution.md) Step 2b lifts `## UI design` from an existing ui-brief instead of re-deciding. A brief authored before any spec waits in `docs/design/` for the feature that adopts it.
