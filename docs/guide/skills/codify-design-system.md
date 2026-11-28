# `codify-design-system`

Use this when a project needs one UI design system that every screen follows,
on any platform: a web app, a desktop app (GPUI, SwiftUI), a mobile app
(React Native), or several at once. It covers greenfield work and a running app
whose screens each style themselves.

It decides and drafts, and does not change production code. The draft lives in
its own folder; once you approve, `define-project` records the standard in
`docs/standards/design-tokens.md`, which `draft-ui` and `inspect-ui` read, and
screens move onto the system one change at a time.

## What you get

- The starting point: every platform that consumes the system, an inventory of
  the raw colors, sizes and duplicated components in use, and the user needs it
  must meet.
- Your calls asked before the choices that depend on them: brand, which themes
  ship, the conformance target (WCAG 2.2 AA by default), the design-tool workflow.
- A **Parts** table covering tokens, theming, foundations, components, content
  patterns, docs and tooling, governance and adoption. Each part is decided,
  already settled, deferred with a trigger, or not needed yet.
- A runnable draft: the token file and each platform's output, three to five
  core components with their states, a theme switch, and one existing screen
  copied onto the system. It comes with the contrast script and whatever else
  could run here.
- The rules every screen follows, each with the check that fails when a screen
  breaks it (lint against raw values, contrast script, visual baseline).
- An adoption order and the list `define-project` records once you approve.

Try: "Every screen in our app styles itself and dark mode is requested. Set up
the design system every screen follows."

[Architect System](architect-system.md) decides the front end's architecture
(state, rendering, data access). [Draft UI](draft-ui.md) explores one screen's
look on top of the system. [Inspect UI](inspect-ui.md) judges a built diff
against it.
