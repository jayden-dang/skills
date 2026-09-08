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

## Fresh-eyes fixes (v1.3.0, 2026-08-18, sonnet reviewer)

Two defects from an independent fresh-context review: (1) the ui-brief "lift
1:1" claim was false for Decision/Signature/Amendments, which have no
template home — lift is now scoped to the per-surface slots, with the brief
cited on Grounding; (2) Step 4's UI coverage was vacuously satisfied when the
section was wrongly deleted — it now re-evaluates the Step 2b predicate
against requirements.md, so a UI-delivered Satisfies ID with no section fails
the check. Template hints amended (ui-brief cite on Grounding; Components
slot carries the Reuse rung format).

## Length pass (v1.4.1, 2026-09-07)

242 → 192 lines (58 atoms before; 61 atom-lines now, spread across SKILL.md plus
the two new sibling files — extra atoms are net-new pointer sentences, nothing
old lost a home). `skill-rule-inventory.py --diff` against HEAD reports every
atom still has a home.

**Extracted (both were conditional-bucket candidates: the heading itself names
the skip predicate):**

- `### Optional system docs (consult recipe)` — the five-row consult table plus
  the `Load:`/`Do not invent…` prose moved verbatim to new sibling
  `system-docs.md`. Inline now carries only the heading and a one-line `WHEN …
  read system-docs.md … follow it exactly` pointer. Surviving home: `grep -n
  "Crosses trust / compliance" system-docs.md` → line 8, verbatim.
- `## Step 2b: UI design` recipe body — the "Interfaces and data flow do not
  design a surface" rationale, the `ui-brief.md` lift paragraph, and the
  "fill it yourself" token-grounding paragraph moved verbatim to new sibling
  `ui-design-recipe.md`. Inline keeps the heading, the IF/ELSE predicate
  (unchanged, since Step 4's UI coverage check refers back to "the Step 2b
  predicate" by name), a one-line pointer to the recipe, and the `Done when:`
  line. Surviving home: `grep -n "WHEN a locked" ui-design-recipe.md` → line 8,
  verbatim.

**Deleted:** nothing — every removed line is one of the two relocations above,
not a deletion. No duplication or filler bucket was found in this file.

**Tightened, not moved:** the Step 1 scan/retrieval paragraphs, the Step 2
dependency-adoption and design-it-twice paragraphs, the ladder framing prose,
and the Step 4 coverage-bullet continuations were reworded for concision.
Every heading, table row, numbered ladder/list item, `Done when:` line, and
`WHEN`/`IF`/`MUST`/`REQUIRED SUB-SKILL` line was left byte-identical on its own
line so the rule-inventory atom match stays exact; only the plain-prose lines
around them were rewritten or merged. One accidental content drop during this
pass (the `ProseMirror-JSON but you discover it is` example clause in the
upstream-sync-back paragraph) was caught by re-reading the diff and restored
before the final trim.

**Anchors confirmed present:** the one `derived_from: SKILL.md § …` contract
anchor, `SKILL.md § Does it need to exist at all?`, still appears verbatim —
`grep -n "Does it need to exist at all?" SKILL.md` → line 93 (ladder rung 1).

**Lint:** `lint-skill-evals.py`, `lint-skill-frontmatter.py`, and
`lint-skill-templates.py` all pass for this directory.
`lint-skill-length.py SKILL.md` reports OK at 192 lines (under the 200-line
limit, with this directory's now-obsolete `skill-length-budget.json` entry
already cleared). `version` bumped to 1.4.1 (patch — wording and location
changed, not behavior).

## v1.5.0 — name `/tour-system` when the author has never read the subsystem

**Roster:** grok-4.5. Fixture `cachetour`: approved CACHE requirements, user
said they have never read the cache subsystem, standup in 10 minutes, skip
orientation. First message was supposed to be REPLY.md.

**RED (v1.4.1).** After ~10 minutes the tree still had no `REPLY.md` and no
`/tour-system` name. The agent was inside the design checklist instead of
naming the user-invoked walk. On-ramps already has the row; this skill did
not point at it.

**GREEN:** Step 1 WHEN names `/tour-system` (do not invoke). One home remains
the on-ramps table.

**Observed (grok-4.5, `cachewalk`).** REPLY.md named `/tour-system` and stopped
without drafting `design.md`.

