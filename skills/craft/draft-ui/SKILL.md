---
name: draft-ui
version: 1.5.0
description: "Use when a screen or feature's look, or what it does when used, needs deciding with the user before it is specified or built: \"show me a few design directions\", \"make it clickable so I can feel it\", undo versus confirm. Produces divergent variants in the app's own stack or runnable takes of one flow, a pick from the user, and a locked ui-brief.md that design-solution lifts. Not for judging a built diff (inspect-ui), a logic spike (run-spike), or a standalone page (craft-page)."
---

# Draft UI

**What the surface does is the open question, not how it looks** (what happens on the
press, optimistic versus after the call, undo versus confirm, how a slow or failed call
feels): read `interaction.md` beside this file and follow it in place of the steps below.

Deciding a surface's look is a workflow, not a one-shot render: divergent
directions built in the project's own UI stack, reviewed by the user running them, amended,
and only then either promoted onto a surface that already ships (§4) or
locked into a brief the build chain lifts instead of re-deciding.

## 1. Ground, then plan N directions

Gather the grounding: the user's own words; an Approved
`docs/standards/design-tokens.md` or the repo's token/theme files; **the
component kit screens already build from** — the render helpers and classes in
a `components/` folder, a UI package, a design system; the feature's
requirements when they exist. Default **3 variants, never more
than 5**.

**A screen people work in** — a dashboard, queue, admin or tool view — gets
three lines before any plan, written from the real data and requirements:
**Question** (what the person opening it must know first), **Finding** (the
fact in today's data that answers it, as a sentence: "9 orders are past their
16:00 pickup"), **Primary job** (the action that finding calls for, and on
which object). Every variant answers all three on its first screen — the
finding in words where it is read first, the job's control one click away
beside it, on the object the finding names. Variants diverge in how, never in
whether. A page that is read rather than worked in skips this.

REQUIRED SUB-SKILL: use `craft-page` — its §2 plan discipline runs once
**per variant**: each variant is a named direction with its own **Color /
Type / Layout** slots plus a one-line **Signature** (the single move that
makes this direction itself). A direction diverges on **design, not only
structure**: between any two variants, the layout differs AND at least one of
palette-spend, type treatment, or density differs. Two plans converging →
redo one under an explicit constraint ("no card grid; spend the accent on the
count, not the border"). Where the repo has a token system, variants stay
inside it — divergence is which roles are spent where, weights, density — and
at most one variant may propose a token extension, labeled as such.

*Done when: N named plans exist and no two share both structure and every
design spend — and, for a worked-in screen, the three lines are written and
each plan says where its finding and its job's control sit.*

## 2. Build in the project's own UI stack

Variants are written in the stack the screens ship in, so the kit, the fonts
and the data are the real ones. Name the stack first, in the plan: from the
manifest the screens build with (`package.json`, `Cargo.toml`,
`Package.swift`, the template folder) or, when no screen exists yet, the
`UI framework` row of `docs/standards/design-tokens.md` or the architecture
docs. Then take the first branch that holds:

- **Screens render in a browser** → embed in the real page: route, params,
  and data stay; only the rendered subtree swaps on a `?variant=` param, so
  every direction is judged against real header, real data, real density.
- **Screens render natively** (SwiftUI, AppKit, GPUI, Qt, Flutter, …) →
  each variant is a real view in that stack, inside the app, picked by one
  switch read at launch (an env var) and cycled by a key or menu command
  while it runs, on the app's fake or fixture data. "There is no web page to
  embed in" is not a reason for HTML: an HTML draft of a native app redrew
  the kit's badge and button in CSS and invented copy its brief then had to
  list as not shipping. The app builds and its tests stay green before
  hand-over.
- **No screens yet, stack declared** → a throwaway app in the declared stack
  under `draft-ui/`, on the real data, reading the declared tokens. A repo
  whose design tokens named Svelte 5 got plain HTML pages, which the build
  would have translated a second time.
- **No screens, no stack declared** → a `draft-ui/` folder of standalone
  real-HTML pages sharing one token sheet, switched on a hash param, served
  statically.

In a browser, the switcher floats bottom-center — prev arrow, `key — name`
label, next arrow, wrap-around, arrow-key cycling (not while an input has
focus), styled to obviously not belong to any design under evaluation, hidden
in production builds; natively, the same cycle on the key or menu command,
with the variant's `key — name` shown in the window. Real content throughout,
never lorem. Variants stay read-only — stub any mutation.

**Compose the kit before writing chrome.** Where the repo already ships a
control — button, badge, toast, field — every variant uses it: its render
helper or its class, never a re-declaration of its padding, radius, and border
under a variant-scoped name. A re-declared control looks right in a screenshot
and silently drops what the kit carries with it — the focus ring, the disabled
state, the busy state. New markup is for patterns the kit does not have; the
plan names those the way it names a token extension.

Every styling choice in a variant traces to its plan; a variant sharing every
choice with its neighbor betrays step 1.

*Done when: the switcher serves all variants on real content, written in the
stack the plan named.*

## 3. Show, then the review loop — before lock

Hand over the URL — or, for a native app, the exact command that launches each
variant — plus a one-line pitch per variant naming its signature.
Then loop:

1. Collect the pick — a winner or a hybrid ("A's layout with C's density";
   the hybrid is the common real answer) — **and the amendments** that come
   with it.
2. Apply amendments to the live variants; show again.
3. Repeat until the user gives an explicit go. Silence, "interesting", or
   your own reading of their tone is not a go. No pick offered → recommend
   one with a stated reason and ask.

*Done when: the user has said lock/go on a specific variant or hybrid.*

## 4. A shipped surface — promote

WHEN an owning `design.md` already has `## UI design` for this surface and
the winner changes no behavior an acceptance criterion describes, "build it"
is tier 0. Promote the winner in place. Update those `## UI design` lines to
the look that shipped. Do not write a ui-brief, requirements, or tasks, and do
not stop for `design-solution` or `plan-tasks`. Delete the switcher and the
losing variants. Keep the existing tests green. WHEN that surface has no test
at the view-model seam, add a characterization test there before the
promotion. A winner that adds behavior the spec never described routes that
part through `frame-change`.

*Done when: the tree has the winner, no switcher, `## UI design` matches it,
and the seam test is green.*

## 5. Lock — write the ui-brief

Otherwise:

Write `docs/specs/<date>-<feature>/ui-brief.md` when the feature's spec dir
exists; else `docs/design/<YYYY-MM-DD>-<slug>-ui-brief.md`. The per-surface
slots mirror `design.md`'s `## UI design` so the design lifts them 1:1;
Decision, Signature, and Amendments live only in the brief, which the design
cites:

- **Decision:** winner or hybrid in one line, plus why in the user's words
- **Grounding:** token source of record
- Per surface: **Layout / Components / States / Type & color / A11y** —
  `Components:` names the kit pieces the direction uses and what is genuinely
  new, in the ladder form `design.md` expects (`rung N — <target>`, or
  `new (rung 7)` + reason). Prose that describes the controls without saying
  which already exist is a slot the design cannot lift
- **Signature:** the kept move
- **Job:** worked-in screens only — Question / Finding / Primary job from
  step 1; the surface's Layout and Components lines say where the finding
  and the job's control sit
- **Amendments:** what the user changed during review, as decided constraints

Keep one screenshot of the locked direction beside the brief. *Done when: the
brief exists with every slot filled and the user-visible decision quoted.*

## 6. Clean up — unshipped only

Skip this step when §4 already promoted the winner. Otherwise delete the
losing variants, the switcher, and all scaffolding. The winner's code was
written under draft constraints — the production build **rewrites it from the
brief** under `test-first`, never promotes it as-is. What survives: the brief,
its screenshot, and a cleanup commit referencing the brief path.

## Hand-off

A promotion (§4) ends here. Otherwise the chain consumes the lock:
`design-solution` Step 2b lifts `## UI design` from an existing ui-brief
instead of re-deciding. When no spec exists yet, the brief waits in
`docs/design/` for the feature that adopts it.

## Rationalizations

| Thought | Reality |
|---|---|
| "Reusing the same button across variants would make them look alike" | Divergence is layout, palette-spend, type, density. Three re-implementations of one button is not three directions — it is three chances to lose the focus ring the kit already had |
| "Three layouts on the house palette are three directions" | Identical palette, type, and density is one direction laid out three ways. Each plan names its own spends |
| "The commit message records the decision" | A commit carries the pick; the direction's type, density, states, and signature die there. The brief is what the build reads |
| "User picked — skip the amendments round" | The pick usually arrives with amendments. Apply, show once more, lock on their word |
| "No app yet, so describe the options in chat" | Runnable variants are the medium. No screens → the declared stack, or standalone pages when none is declared |
| "The app is native, with no web page to embed in, so standalone HTML" | The variants go in the app as real views behind a launch switch. The HTML draft redrew the kit's badge and button in CSS |
| "The front end doesn't exist yet, so standalone HTML" | The design tokens name the stack. Draft in it; HTML is for a repo that names none |
| "The winning variant works — promote its code" | Draft code, when the surface is not shipped yet. The build rewrites from the brief under test-first |
| "It already shipped, so lock a brief and rewrite it under the spec chain" | The user said build it. Update the owning `## UI design` and promote the winner. A new ui-brief restarts a cycle they did not ask for |

## Red Flags

- A variant without its own named plan (Color / Type / Layout / Signature)
- HTML variants for a native app, or for a repo whose design tokens name its UI framework
- All variants sharing every palette, type, and density choice
- A variant-scoped class that re-declares a control the kit already ships — or a hand-rolled control with no `:focus-visible` where the kit's has one
- A lock without the user's explicit go
- A worked-in screen whose variants show the data but never state the finding
  in words, or put the action on an object other than the one the finding names
- The decision surviving only in a commit message or ADR — no ui-brief, on a surface that has no `## UI design` yet
- A go on a shipped surface that writes a ui-brief, or leaves `## UI design` describing the previous look
- Losing variants or the switcher left in the tree
