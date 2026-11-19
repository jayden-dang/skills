# `draft-ui`

> Deciding what a screen should look like is a workflow, not a one-shot render: divergent directions built in the project's own UI stack on a fake API that the user clicks through, a review-and-amend loop, and a locked brief, with the winner kept as the code the build finishes.

|  |  |
|---|---|
| **Bucket** | craft |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the user's direction; `docs/standards/design-tokens.md` or the repo's token/theme files; the component kit screens already build from; the feature's requirements when they exist |
| **Writes** | draft variants + switcher + a fake behind the app's client; at the lock the losers go and the winner stays with lock tests (standalone pages: all deleted); a `ui-brief.md` with `## Contract` when the surface has no UI design yet, or an in-place promotion plus updated `## UI design` when it already ships |
| **Calls** | [`craft-page`](craft-page.md) (§2 plan discipline, once per variant) |
| **Called by** | [`run-spike`](run-spike.md) (its UI branch routes here) |

## When it fires

"What should this look like?", "show me a few design directions", "make variants and let me pick" — before a surface is specified or built. `run-spike` hands its UI branch here; logic/state spikes stay with `run-spike`.

## The workflow

1. **Plan N directions** (default 3, max 5) — each variant gets its own named Color/Type/Layout plan plus a Signature line, via `craft-page` §2. Directions diverge on **design, not only structure**: identical palette, type, and density across variants is one direction laid out three ways. For a screen people work in (a dashboard, queue, admin or tool view), three lines come first — the **Question** the person opening it must answer, the **Finding** in today's data that answers it, and the **Primary job** it calls for — and every variant shows the finding in words with the job's control beside it, on the object the finding names.
2. **Build in the project's own UI stack** — named first from the manifest or the design tokens' `UI framework` row. A browser app gets the variants embedded behind a `?variant=` switcher (real header, real data, real density); a native app (SwiftUI, GPUI, …) gets them as real views behind a launch switch on its fake data; a repo with no screens but a declared stack gets a throwaway app in that stack; only a repo that declares nothing gets standalone HTML pages. Real content; every read and mutation goes through a fake behind the app's own client (its fake mode when it has one), so the user clicks real flows and the fake's calls become the backend's contract. Controls the kit already ships are composed from it, never re-declared under a variant class — a rebuilt button silently drops the focus and disabled states the kit carried.
3. **Look, then review loop** — before showing anything, the agent runs each variant, captures its own page or window (`capture.md`: headless Chrome, or the native window by ID — never a screen region), opens every capture and fixes what fails against the plan: clipped text, a hidden finding, a kit control out of state. A variant it could not capture is named unseen. Then URL or launch command + one-line pitch + capture path per variant; collect the pick (usually a hybrid) *and its amendments*; apply, show again; repeat. Lock only on the user's explicit go.
4. **Shipped surface** — when an owning `design.md` already has `## UI design` and the winner changes no spec'd behavior, promote the winner, update those lines, and do not write a ui-brief (added behavior goes through `frame-change`). Otherwise **lock** — write `ui-brief.md` (feature spec dir, else `docs/design/`) whose slots mirror `design.md`'s `## UI design` 1:1, plus the Decision in the user's words, the Signature, the `Job:` line for a worked-in screen, and the amendments log. Keep one screenshot.
5. **Keep or clean up** — with screens or a declared stack, `keep.md`: losers and switcher deleted, the winner moved to its real route, the fake behind one switch and absent from the production build, lock tests written and each seen red by mutation, all committed together. With no stack declared, everything is deleted and the build writes the surface from the brief. A shipped surface already finished at step 4.

## Downstream

[`design-solution`](design-solution.md) Step 2b lifts `## UI design` (and `## Contract`) from an existing ui-brief instead of re-deciding; the tasks finish the kept code — polish, real endpoints to the contract, the fake out of the production path — rather than rebuild it. A brief authored before any spec waits in `docs/design/` for the feature that adopts it.

## Modes folded in (2026-11-15)

Each is a file beside `SKILL.md`, opened on the condition `SKILL.md` names.

- `interaction.md` — what a surface does when used: two or three runnable takes of one flow and a locked Interaction section.
- `keep.md` — the lock on the keep path: strip, fake check, contract, lock tests, one commit.
