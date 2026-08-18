# `design-solution` — the `Surface:` slot (affected-reader disposition)

Model roster: Sonnet. Fixture: a TypeScript billing service where
`calculateTotal` has four in-repo callers, a persisted `orders.total_cents`
row, and an `order.settled` webhook consumed by two external partners.
Task: design tiered pricing (Steps 1–2 only), release cut on Friday.

## RED — S-SURF (omission)

**Observed (1/1).** Found all four callers and chose a sound design. Then
dismissed the external contract in prose, verbatim:

> "Order.totalCents and the order.settled webhook payload keep their current
> shape. Orders with a qualifying line item will simply carry a different
> (correctly discounted) number — a value change the two external partners
> already expect a 'total' field to reflect, not a contract change.
> **No coordination with those partners is triggered by this design.**"

Also: `Locality: leave` on every neighbor, and "callers need zero edits — they
get correct tiered totals for free". Two external partners silently begin
receiving different money and the design records it as zero-impact.

**Failure class.** Omits an element from something it already produces — the
readers were *found*, never *classified*. Per `author-skills`' failure table
the form is a REQUIRED slot, not a prohibition.

## GREEN — same fixture, `Surface:` slot added

**Observed (run 1).** Six-row `Surface:` table, one disposition each; the two
webhook partners raised as a flagged coordination risk instead of a non-event.

**Meta-test found a real gap** (diagnostic class "it should have said X"): the
tested agent could not place the webhook. `frozen` read as "must not alter",
which contradicts a requirement that *mandates* the value change, so it
composed a fourth category — `replace — with a flagged coordination risk`.
The rationalization row ("frozen until their owner agrees") and the `frozen`
definition disagreed with each other.

**REFACTOR.** `frozen` sharpened to "may not alter *unilaterally*", discharged
two ways — build around it, or gate shipping on the owner's agreement, with
the row naming which.

**Observed (run 2, post-refactor).** All rows resolved inside the three-word
vocabulary; agent confirmed no invented category was needed. The design itself
changed: it split out `calculateTieredTotal` and left the invoice/webhook path
on the untouched `calculateTotal`, because the `frozen` row forced the external
contract to be a design constraint rather than a footnote.

## Rules this evidence owns

| Rule | Evidence |
|---|---|
| `Surface:` REQUIRED when a section changes behavior/**value**/shape/signature of something with readers | RED classified nothing; GREEN produced a per-reader table |
| "value" listed coordinate with shape/signature | Meta-test: agent quoted "value" as the phrase that denied a same-shape pass |
| `frozen` = may not alter **unilaterally**, discharged by workaround **or** named consent gate | Run-1 meta-test invented a 4th category; run 2 needed none |
| `Locality:` ≠ `Surface:` (edit location vs affected reader) | RED wrote `leave` on readers whose returned value changed |
| Rationalization row: "same shape, different number — not a contract change" | Verbatim from the RED transcript |

## UI design fork (v1.1.0, 2026-08-18, sonnet)

**RED** — 2 reps (des-a, des-b), fixture: static vanilla-JS board with a real
token sheet (`--accent`/`--danger`/`--space-*` etc.), approved FILT
requirements (filter bar + counts + selected state + empty state + overdue
emphasis). Both reps produced structurally complete designs (Satisfies /
Reuse / Interface / Depth / Locality all filled) with **zero visual
dimension**: no layout composition, no interaction states (hover / focus /
selected styling), no type or spacing decisions, no empty-state presentation,
no a11y. Token names appeared only where a requirement's own wording forced
them ("same emphasis treatment as the existing overdue badge"). Grep for
gap/space/align/font/focus/hover/keyboard/aria/pill/layout: des-a 3 hits,
des-b 2 hits — all false positives (addEventListener, "handful of lines").
Failure class: **output has the wrong shape** → positive recipe / REQUIRED
template slots gated on an observable predicate, not a prohibition.

**GREEN** — 2 reps, updated template + Step 2b:

| Rep | Scenario | Result |
|---|---|---|
| des-c | FILT (should-fire) | `## UI design` present: Grounding cites styles.css precedence; per-surface Layout (flex child + gap tokens + wrap), Components with ladder rungs, States incl. composed selected-and-overdue and counts-visible, Type & color at token level (14px matching `.topbar-sub`), A11y (`aria-pressed`, `role="group"`, contrast inherited from shipped pairing) |
| des-d | LVAL console-only validation (should-not-fire) | section deleted per predicate; note in coverage check |

No new rationalizations; no REFACTOR round needed.

**Ship:** `templates/design.md` `## UI design` section (Grounding + five slots
per surface); SKILL.md Step 2b observable conditional + Step 4 UI coverage
line + todo list includes 2b.

## ui-brief lift (v1.2.0, 2026-08-18)

Step 2b gains the lift conditional: a locked `ui-brief.md` (spec dir or
docs/design/) is lifted 1:1 into `## UI design` and cited; nothing it locked
is re-decided. Evidence: draft-ui RED showed the locked direction's type /
density / states dying in a commit message and being re-decided at design
time — see `skills/craft/draft-ui/TESTS.md`.
