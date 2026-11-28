---
name: codify-design-system
version: 1.0.0
description: "Use when a project needs one UI design system that every screen follows, on any platform (web, desktop such as GPUI or SwiftUI, mobile such as React Native): design tokens, theming and dark mode, color, type and spacing scales, the component library and its states, accessibility rules, docs and governance, or consolidating screens that each style themselves. Produces a design-system decision note, a runnable draft of the tokens and a few core components in a separate draft folder, and the rules with the checks that keep screens on the system, ready for approval. Not for one screen's look (draft-ui), judging a built diff (inspect-ui), front-end architecture such as state or rendering (architect-system) or writing docs/standards/design-tokens.md for a system already approved (define-project)."
---

# Codify Design System

Decide the visual system and component behavior every screen shares, try it in
a draft, and stop for approval. Production screens, components and styles stay
untouched: the draft lives in its own folder, the approved standard is recorded
by `define-project`, and screens move onto the system one change at a time
through the repo's normal workflow. Under "restyle all screens this week" a
baseline run rewrote all five screen files of a running shop and added its new
components to `src/`, with no review and no visual baseline to compare against.

The user owns the note's location; a filename alone means the checkout root.
One screen's look belongs to `draft-ui`, front-end architecture (state,
rendering, data access) to `architect-system`.

## 1. Establish the starting point

- **Platforms:** every client that will consume the system (web, desktop,
  mobile, a marketing site), its toolkit and its styling mechanism.
- **What exists:** token or theme files, a component folder, a brand file or
  design-tool library. For a running app, inventory the raw values in use with
  `grep` (distinct colors, font sizes, spacing, radii) with counts and files,
  and the duplicated components (three buttons, two text fields).
- **Who it must serve:** support reports and users' needs (low vision, a
  screen-reader user, dark-mode requests, gloves or bright sun).

**Done when:** the note names the platforms, the inventory with counts, and
the user needs it must meet, each with its source.

## 2. The user's calls

The brand, which themes ship (light, dark, high contrast, a partner brand),
the conformance target (WCAG 2.2 AA unless the user sets another) and the
design-tool workflow belong to the user. Ask each before the choice that
turns on it. REQUIRED SUB-SKILL: use `clarify-decisions`, one question at a
time. When nobody can answer in this session, pick a provisional default,
list it as the user's decision, and hold what depends on it.

**Done when:** every call is answered or listed as open with what it holds.

## 3. Cover every part

Read `parts.md` beside this file. The note carries a **Parts** table with one
row per part there, each with one status: **decided here**, **already
settled** (cite the file), **deferred** (with the trigger that reopens it) or
**not needed yet** (with why). Baseline notes covered what the request named:
high contrast and forced colors went unmentioned in five of six, a lint
against raw values and a visual baseline in all six, governance in four.

For each part decided here, write the options considered, the choice, and
what was rejected and why.

**Done when:** every row has a status.

## 4. Draft it and run it

Build the draft in one folder inside the app's source tree
(`src/design-system-draft/` on the web, a `design_system_draft` module in a
native crate or app), using the project's real stack:

1. The token file in the chosen source of truth, and the output each platform
   consumes (CSS custom properties, Rust or Swift constants, a JS theme).
2. Three to five core components (for example button, text field, status
   badge, surface) built only on semantic tokens, each with its full state
   matrix. An open choice of component library does not skip them: build on
   the platform's own controls (DOM elements, React Native core, the toolkit's
   primitives) and list the library choice as open. A baseline run wrote
   "Rejected: building the first components now" and drafted none.
3. A switch for each theme axis.
4. One existing screen copied into the draft and moved onto the system, so
   the user sees the change on real content. The original stays as it is.

Run what the checkout can run: render or test each component in each theme
and state, and compute the contrast of every text and component pair from the
token values with the WCAG formula, keeping the script. When the stack cannot
run here, say exactly what was not run.

**Done when:** the draft folder holds the tokens, the components and the
copied screen, and every check has an outcome or an explicit "not run".

## 5. Rules and their checks

Write each rule the screens must follow with the check that fails when a
screen breaks it: a lint against raw colors and sizes outside the token
output, the contrast script over token pairs, a story or test per component
state, a visual baseline of every screen captured before migration starts,
accessibility checks (automated rules plus a manual pass for what they miss).

**Done when:** every rule has a check and the place it runs.

## 6. Plan the adoption

For a running app: tokens first, then the core components, then screens by
traffic or pain, one change per screen through the normal workflow, the
visual baseline before the first one, the lint warning first and failing once
a screen is migrated, and the date the old styles go. For greenfield: the
first feature builds on the approved system.

**Done when:** the order, the first screen and the removal date (or "open")
are named.

## 7. Stop for approval, then hand off

End the note with **Awaiting approval** and the exact list to record: the
`docs/standards/design-tokens.md` entry (and `ui.md` or `accessibility.md`
when a rule belongs there) and the rules with their checks. Stop there. Once
the user approves, REQUIRED SUB-SKILL: use `define-project` to record what
they approved; `draft-ui` and `inspect-ui` read that entry. The draft is a
reference for the decision, not code to promote: the first migration change
rebuilds the tokens and components test-first in the real source tree and
deletes the draft folder. A baseline plan's step 1 was "promote `tokens/`,
`components/` and `theme/` from the draft to `src/design-system/`".

## Red Flags

- A production screen, component or style file changed before approval.
- New components added outside the draft folder.
- A plan that moves draft code into production instead of rebuilding it test-first.
- A Parts table missing a row from `parts.md`.
- A rule with no check, or a contrast number nobody computed.
- A theme, brand or conformance target chosen without listing it as the user's call.

**No-op:** one screen's look, a review of a built diff, or recording a system
the user already approved goes to its owner.
