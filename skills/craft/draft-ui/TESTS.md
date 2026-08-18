# draft-ui — test evidence

## RED (2026-08-18, sonnet, 1 rep)

Fixture: static vanilla-JS board at pre-implementation `main` (approved FILT
requirements only). Baseline = run-spike's UI branch text alone, task: "show
me genuinely different design directions in the browser; after I pick the
decision must carry into our spec docs."

Mechanics held (3 structurally different variants — tabs / chip toolbar /
vertical rail — behind a working switcher on real data). The three target
gaps all reproduced:

- **One design direction laid out three ways:** a single shared `styles.css`
  for all variants; the only non-house font was the switcher's; zero
  per-variant plans — pitches were purely structural ("tab bar", "chips",
  "rail").
- **No review loop:** hand-over went straight to a post-pick plan.
- **No durable brief:** the decision carrier was "the commit message states
  which variant won and why" + a later design.md authored from memory — type,
  density, states, and signature of the chosen direction survive nowhere.

## GREEN (2026-08-18, sonnet, 1 rep, two-phase)

Same fixture, full draft-ui text (craft-page discipline inlined for the
sandbox).

**Phase 1 (build + show):** three named plans, each with its own Color / Type
/ Layout / Signature — solid-fill segmented capsule vs stat-block rail
(uppercase 12px caption over 20px numeral) vs pure-typographic middot
sentence — diverging on palette-spend AND type AND density while staying
inside the `:root` token sheet. Stopped at hand-over and **waited for the
pick without writing any brief** ("Waiting on your pick … before this gets
locked").

**Phase 2 (pick relayed: hybrid c+a, 3 amendments, "go"):** amendments
applied to the live variant and verified by screenshot before lock;
`ui-brief.md` written with Decision (user quoted), Grounding, Layout /
Components / States (including the composed overdue-and-selected state) /
Type & color / A11y, Signature, and the three Amendments as decided
constraints; one screenshot kept beside the brief; variants + switcher
deleted, `app.js` restored to committed baseline, cleanup commit references
the brief. The winner's draft code was deleted, not promoted.

## Trigger test (2026-08-18, sonnet)

12 routing queries against run-spike, craft-page, review-ui, design-solution,
frame-change: **12/12** — should-fire ("what should X look like", "variants
and let me pick", "mock both up for real", "explore design directions",
"clickable takes of the empty state") all reached draft-ui; traps landed
right (logic spike → run-spike; distinctive landing page and HTML report →
craft-page; design-review a branch and mobile breakage → review-ui; brand-new
feature → frame-change; design.md for approved reqs → design-solution).
