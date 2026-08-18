# `review-ui`

> A style diff read carefully still only yields hypotheses — "these classes may collide", "this might overflow on a phone". This skill settles every visual claim the only way it can be settled: by rendering the change in the real app and looking.

|  |  |
|---|---|
| **Bucket** | review |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the diff range; `design.md` `## UI design` (when present); the repo's token/theme files; `docs/agents/project.md` **Run locally (dev)** |
| **Writes** | screenshots under `.skills/<CODE>/review-ui/` — never the working tree |
| **Calls** | nobody |
| **Called by** | [`inspect-change`](inspect-change.md) (UI lane, step 3d) |

## When it fires

When a diff or branch touches anything a browser renders — HTML, CSS/styling, components, templates — and its visual and interaction quality must be judged before merge. `inspect-change` invokes it automatically whenever the reviewed range includes such files; the user can also ask for it directly ("design-review this branch", "does this break on mobile?").

## What it does

1. **Scopes** the changed rendered surfaces and maps each to a screen.
2. **Starts the app** (same run-command contract as `validate-ui`). Can't run → the whole review is labeled `unverified (static)`, loudly.
3. **Floor passes**, deterministic: grep the changed styles for raw hex/rgb outside the token system and for `outline: none` with no visible focus replacement.
4. **Drives and captures**: three viewports (1440×900 / 768 / 375) with a horizontal-overflow check at each; every reachable and composed interaction state (hover, Tab-focus, selected, empty, error); a walk of the design contract's `States:` lines; WCAG contrast ratios computed from actual rendered values.
5. **Reports** findings with severity + `file:line` + screenshot path, a `needs-human-eyes` list of genuine taste calls (which feeds `execute-common`'s product-walk predicate), and a `UI: clean | findings | cannot drive` verdict line.

## Severity stance

Broken layout at a common viewport width is **Important** even when no requirement says the word "responsive" — the rest of the page reflows, so a surface that doesn't is broken, not out of scope. Text under 1.5:1 contrast is effectively invisible: **Critical**.

## Boundaries

- Asserting spec'd behavior end-to-end with committed Playwright tests is [`validate-ui`](validate-ui.md).
- Authoring a human eyeball walkthrough is [`review-product-flow`](review-product-flow.md) — `review-ui` is the agent's eyes, not the human's.
- Designing a page's look in the first place is [`craft-page`](craft-page.md); this skill judges what got built.
