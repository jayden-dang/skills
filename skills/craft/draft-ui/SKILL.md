---
name: draft-ui
version: 1.0.1
description: Use when a screen or feature's look and feel needs deciding with
  the user before it is specified or built — "what should this look like",
  "show me a few design directions", "make some variants and let me pick", a
  UI mockup exploration clicked through in the real browser. Produces 2–5
  divergent real-HTML variants behind a floating switcher (embedded in the
  running app, or standalone pages when no app exists), a review-and-amend
  loop with the user, and a locked ui-brief.md that design-solution's UI
  design section lifts instead of re-deciding. Not for judging an already
  built diff (review-ui), logic or state spikes (run-spike), or a standalone
  document page (craft-page).
---

# Draft UI

Deciding a surface's look is a workflow, not a one-shot render: divergent
directions built as real HTML, reviewed by the user in the browser, amended,
and only then locked into a brief the build chain lifts instead of
re-deciding.

## 1. Ground, then plan N directions

Gather the grounding: the user's own words; an Approved
`docs/standards/design-tokens.md` or the repo's token/theme files; the
feature's requirements when they exist. Default **3 variants, never more
than 5**.

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
design spend.*

## 2. Build real HTML

App exists → embed in the real page: route, params, and data stay; only the
rendered subtree swaps on a `?variant=` param, so every direction is judged
against real header, real data, real density. Floating switcher bottom-center
— prev arrow, `key — name` label, next arrow, wrap-around, arrow-key cycling
(not while an input has focus), styled to obviously not belong to any design
under evaluation, hidden in production builds. No app yet → a `draft-ui/`
folder of standalone real-HTML pages sharing one token sheet, switched by the
same bar on a hash param, served statically. Real content throughout, never
lorem. Variants stay read-only — stub any mutation.

Every choice in a variant's CSS traces to its plan; a variant sharing every
choice with its neighbor betrays step 1.

*Done when: the switcher serves all variants on real content.*

## 3. Show, then the review loop — before lock

Hand over the URL plus a one-line pitch per variant naming its signature.
Then loop:

1. Collect the pick — a winner or a hybrid ("A's layout with C's density";
   the hybrid is the common real answer) — **and the amendments** that come
   with it.
2. Apply amendments to the live variants; show again.
3. Repeat until the user gives an explicit go. Silence, "interesting", or
   your own reading of their tone is not a go. No pick offered → recommend
   one with a stated reason and ask.

*Done when: the user has said lock/go on a specific variant or hybrid.*

## 4. Lock — write the ui-brief

Write `docs/specs/<date>-<feature>/ui-brief.md` when the feature's spec dir
exists; else `docs/design/<YYYY-MM-DD>-<slug>-ui-brief.md`. The per-surface
slots mirror `design.md`'s `## UI design` so the design lifts them 1:1;
Decision, Signature, and Amendments live only in the brief, which the design
cites:

- **Decision:** winner or hybrid in one line, plus why in the user's words
- **Grounding:** token source of record
- Per surface: **Layout / Components / States / Type & color / A11y**
- **Signature:** the kept move
- **Amendments:** what the user changed during review, as decided constraints

Keep one screenshot of the locked direction beside the brief. *Done when: the
brief exists with every slot filled and the user-visible decision quoted.*

## 5. Clean up

Delete the losing variants, the switcher, and all scaffolding. The winner's
code was written under draft constraints — the production build **rewrites it
from the brief** under `test-first`, never promotes it as-is. What survives:
the brief, its screenshot, and a cleanup commit referencing the brief path.

## Hand-off

The chain consumes the lock: `design-solution` Step 2b lifts `## UI design`
from an existing ui-brief instead of re-deciding. When no spec exists yet,
the brief waits in `docs/design/` for the feature that adopts it.

## Rationalizations

| Thought | Reality |
|---|---|
| "Three layouts on the house palette are three directions" | Identical palette, type, and density is one direction laid out three ways. Each plan names its own spends |
| "The commit message records the decision" | A commit carries the pick; the direction's type, density, states, and signature die there. The brief is what the build reads |
| "User picked — skip the amendments round" | The pick usually arrives with amendments. Apply, show once more, lock on their word |
| "No app yet, so describe the options in chat" | Real HTML is the medium. No app → standalone pages behind the same switcher |
| "The winning variant works — promote its code" | Draft code. The build rewrites from the brief under test-first |

## Red Flags

- A variant without its own named plan (Color / Type / Layout / Signature)
- All variants sharing every palette, type, and density choice
- A lock without the user's explicit go
- The decision surviving only in a commit message or ADR — no ui-brief
- Losing variants or the switcher left in the tree
