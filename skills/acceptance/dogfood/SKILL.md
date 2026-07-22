---
name: dogfood
description: Use when manually exercising a finished feature in the real running app from
  the user's seat — a hands-on dogfooding pass, case by case, over every
  user-facing ability, including the visuals, feel, and edge cases a human
  must eyeball rather than an automated test or a quick launch. Reach for it
  to try a feature for real, walk the whole user-facing surface, or produce a
  checkable, resumable HTML test guide kept open beside the app and ticked off
  as you go — not a one-off run.
---

# Dogfood

A dogfooding pass is a human driving the real app through every user-facing
ability and judging what they see. The deliverable is a **persistent, checkable
HTML artifact** — grounded in the app's own rendering, one row per ability, each
tagged with the requirement ID it exercises — that the user keeps open beside
the app and ticks off as they go. Build the artifact; a chat message is not the
deliverable.

## 1. Scope every ability from the spec

Read the feature's `requirements.md`, `design.md`, `tasks.md`. List every
user-observable ability keyed to its requirement ID — the happy path, the edge
cases, AND the deliberate non-behaviors (what should NOT happen; the
Out-of-Scope decisions). Include the adjacent capabilities in the same user
workflow, not only the new feature — the user exercises the whole surface.
*Done when: every user-facing requirement ID has at least one case.*

## 2. Ground each case in the real code

For each case, read the code to get what the user will ACTUALLY see: the exact
vocabulary (keywords, command names, labels), keyboard shortcuts, and the real
rendering — badge colors, chip styles, icons — pulled from the source (theme
tokens, CSS), never guessed. The artifact's "Expect" mirrors that rendering so
the user checks against a true picture. Where the code reveals an honest caveat
(a delimiter dimmed not removed, a status with no UI yet), the case says so.

## 3. Boot the real app and find the honest observation point

Start the app with the `Run locally (dev)` command from `docs/agents/project.md`
(discover and record it if missing — see `acceptance-ui`). Surface any degraded
area up front: a feature needing a key, a sub-feature not built yet. A behavior
with no UI surface still gets a case — with a real way to observe it (a devtools
`invoke(...)`, a read-only DB peek), never a pretend screen. *Done when: the app
is running and every not-yet-visible behavior has an observation method.*

## 4. Build the checkable artifact

REQUIRED SUB-SKILL: load `design-page` before building the page, then build a
self-contained HTML page and publish it with the Artifact tool. Contract:

- Sectioned by ability area; **one row per case**, each carrying its requirement
  ID so a failing box routes straight back to the spec.
- Each row: **Try** (what to type or click, copy-pasteable) → **Expect** (shown
  in the app's real rendering, not described in prose).
- **Interactive checkboxes that persist** (localStorage) plus a progress
  counter, so the user closes and resumes.
- Theme-aware, fully self-contained: inline CSS/JS, no external assets.

No artifact tooling in your environment? Write the same page to an `.html` file
and hand over its path.

## 5. Hand over

Give the fastest way in — a ~30-second first pass that lights the feature up —
then the degraded-feature notes and how to enable them, and that ticks save.
*Done when: the artifact is published, grounded, resumable, and every ability
and non-behavior is a checkable, ID-tagged case.*

## Rationalizations

| Thought | Reality |
|---|---|
| "A markdown checklist in chat is enough" | It saves no tick, cannot show the real badge being checked against, and scrolls away. The deliverable is the persistent artifact. |
| "They're in a native desktop app, not a browser, so an artifact doesn't fit" | The artifact is a companion reference kept open beside the app; the app being native is no reason to inline the guide into chat. |
| "I'll describe the badge in words" | The user checks against what they SEE. Mirror the real rendering, or the Expect is unverifiable. |
