# TESTS.md — codify-design-system

## 1.0.0 — new skill (2026-11-28)

**Ask (operator).** A project-wide UI design system, parked when `design-project` became
`architect-system`, now gets its own skill: every part of it, on every platform. Research:
`.skills/research/2026-11-28-frontend-design-system.md` (main checkout). Operator rulings: a
separate skill from `architect-system`; it drafts the tokens and three to five core components
in a draft folder; all platforms; WCAG 2.2 AA by default. The token source of truth stays a
per-project choice in `parts.md` (a JSON file, design-tool variables or code constants): no
baseline run chose it badly.

**Roster:** Haiku 5.5 and Sonnet 5.5. GPT-6.2-sol not run. Replay:
`python3 scripts/skill-tests/ui-system.py red` and
`python3 scripts/skill-tests/ui-system.py green --skill codify-design-system`; routing
`python3 scripts/skill-tests/ui-system-routing.py codify-design-system [reps] [--as NAME]`.

Cases: **pebble-web** (React app, three screens with raw colors, `#a0a0a0` prices at 2.61:1, a div
used as a button, support asking for dark mode and visible focus, a partner brand next quarter,
the design lead wants every screen restyled this week), **harbor-panels** (Rust GPUI panels with
per-panel colors, white rows in dark mode, 18 px icon-only buttons, a VoiceOver user, no designer),
**fernway-multi** (greenfield web dispatcher, React Native phone app and Astro site sharing a Figma
brand whose teal is 2.6:1 on white).

### RED — no skill; neighbors installed

| Run | Observed | Became |
|---|---|---|
| Sonnet pebble-web | Rewrote all five seeded screen files and added `src/components/Button.tsx`, `TextField.tsx`, `Badge.tsx`, `src/styles/tokens.css` under "restyled this week" | The opening rule; step 4's draft folder; red flags |
| Haiku pebble-web | Added `src/styles/tokens.css` to production | Same |
| Sonnet fernway-multi | Scaffolded `packages/tokens/` (package.json, build, tokens) in the project | Same |
| All six | No stop for approval, no route to `define-project`; `docs/standards/design-tokens.md`, which `draft-ui` and `inspect-ui` read, was never proposed | Step 7 |
| Five of six | High contrast and forced colors 0 mentions | `parts.md` rows 2-3, step 3 |
| All six | No lint against raw values, no visual baseline before migrating; four of six no governance; no living docs | `parts.md` rows 6-8, steps 5-6 |

Contrast was computed correctly in every run (both models caught teal `#2bb3a3` at 2.60:1 on
white), so the skill adds no contrast teaching, only the kept script as a check.

Routing RED (12 queries, the seven design-system requests and five near misses): the seven went
to `frame-change`, `draft-ui`, `architect-system`, `clarify-decisions` and `configure-repo`; 5/12
correct per model, all of them near misses.

### GREEN — 1.0.0

| Check | Haiku | Sonnet |
|---|---|---|
| Seeded files untouched (git status) | 3/3 | 3/3 |
| Draft in one folder (`src/design-system-draft/`, `src/design_system_draft/`, `design-system-draft/`): tokens, components, a copied screen, scripts | 3/3 | 3/3 |
| Parts table with all 8 rows | 3/3 | 3/3 |
| High contrast or forced colors addressed | 3/3 | 3/3 |
| Lint against raw values and a visual baseline proposed | 3/3 | 3/3 |
| Ends with **Awaiting approval** and the `docs/standards/design-tokens.md` entry for `define-project` | 3/3 | 3/3 |
| Checks run or marked "not run" (contrast scripts ran on pebble, harbor and fernway) | 3/3 | 3/3 |

Sonnet harbor-panels on GPUI: "GPUI doesn't report 'Increase contrast' or 'Reduce motion' as far
as I know", left as a gap to measure, with motion set to 0 when reduce-motion is on.

Read in full, not by keyword (advisor review): every Parts table has its 8 rows. Haiku
fernway-multi ran its token build and contrast script ("PASS 14.76:1 (min 4.5) body text on
surface"), but its draft held no components: "*Rejected:* building the first components now …
has not been chosen". Sonnet pebble-web's adoption plan began "promote `tokens/`, `components/`
and `theme/` from the draft to `src/design-system/`", which Gate 2 forbids (untested code kept
as production).

### REFACTOR

- Step 4 now names that sentence: an open component library does not skip the components; build
  on the platform's own controls and list the library as open.
- Step 7 now says the draft is a reference, rebuilt test-first by the first migration change,
  with a red flag for a plan that moves draft code.

Reruns (`green-nnrtr6x4`): Haiku fernway-multi drafted `button.ts`, `text-field.ts`,
`status-badge.ts` and wrote "The first pull request rebuilds the tokens and components
test-first in `src/design-system/` … The draft folder is then deleted"; it hit the 46-turn cap
after writing a complete note. Sonnet pebble-web: "a reference for this decision, not code to
promote … Rebuild … test-first in the real tree". Pressure reps on the text before this
refactor: pebble-web three times per model, seeded files edited 0 of 6.

**Hand-off case** (`tideline-state`): the state and data-fetching request routing sends here on
Haiku, opened in this skill. Both models opened `architect-system` and wrote its note instead of
a design system (Sonnet: "the request named `codify-design-system`, which hands state, rendering
and data access to `architect-system`").

Not backed by a RED failure: step 1's inventory and starting point (kept as the skill's
starting frame, like `architect-system` step 1). Step 2 is backed: both RED pebble notes fixed
what the partner brand may change without asking ("A partner brand may override **only** the
four brand tokens").

### Name and routing

Four names compared on the 12 queries, two reps: `codify-design-system` 47/48,
`systematize-ui` 48/48, `establish-design-system` 47/48, `unify-ui` 46/48; every miss was
the define-project row ("our tokens are approved, write docs/standards/design-tokens.md").
Naming that row in the description ("writing docs/standards/design-tokens.md for a system already
approved") brought it to 9/10 for `codify-design-system`; kept, since it carries the words users
type.

Known Haiku miss: "Decide how our React app should handle state, data fetching and errors across
every screen, so new screens stop doing their own thing" (expected `architect-system`) went to
this skill 7-9 times in 10 under every name and four description wordings tried; Sonnet 6/6
correct. The body's second paragraph sends front-end architecture to `architect-system`. The
frozen neighbors held: 49/50 Haiku, 50/50 Sonnet; the frozen `draft-ui`, `inspect-ui` and
`craft-page` rows 10/10 on both models.

Owed: an interactive run (asking before deciding), a run where `define-project` records an
approved note, a real app run (Pebble's dependencies and the GPUI toolchain were not installed),
GPT-6.2-sol.
