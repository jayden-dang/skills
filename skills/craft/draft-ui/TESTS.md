# draft-ui — test evidence

## v2.0.0 — the winner is kept, on a fake behind the app's client (2026-11-19, Sonnet + Haiku)

On the owner's word (2026-11-19, translated): drafts are real code in the app, on real components and a
fake API, so the owner sees how the product will actually work; at the lock the losers go and the winner
stays, and design and tasks finish it instead of rebuilding it. Rulings: Gate 2 may carry a lock-test
exception; the no-stack path keeps draft-then-delete.

**RED, fixture `tidewell`** (React 19 + Vite, kit, dev-server API, Approved GEAR requirements, no gear
backend; `.skills/fixtures/make-tidewell.sh`). Prompt: Thu wants to "actually click through reserving a
wetsuit for Jonas … cancel it, and see what the screen does when the M wetsuits run out". v1.6.0:

- Both models drafted in the app with live mutations (Haiku took `interaction.md`, with latency and
  race toggles). Interactivity was not the gap.
- Neither had an API seam. Sonnet: `STOCK` constant + `useGear` store in `src/draft/gearModel.ts`.
  Haiku: "Stock and reservations are held in the browser, not the real API".
- Neither wrote a test: "I did not add tests, because this is a throwaway prototype."
- On go, both deleted the winner. "the draft code has to be deleted rather than promoted. That means
  removing `src/draft/`". The code was never committed, so no history of it remains.
- A rebuild from the brief (fresh Sonnet and Haiku, design.md a 1:1 lift) came out near pixel-identical
  to the locked screenshot, because both builders opened it. So on one screen, drift was not the cost.
  The rebuild was: 141 s / 68k tokens and 135 s / 65k tokens, re-deriving a screen that already ran.

**RED, the owner's repo RENO** (GPUI, same day). The draft branch `draft/ui-direction` held 5 commits and
4,587 lines in reno-app on the app's own `--fake` daemon. Its plan read "The draft is THROWAWAY (draft-ui
§6): the winner is rewritten from a ui-brief". After the lock, three slices (12:06–16:18) re-implemented
the sidebar, status bar, conversation rows, tick rail, folds and composer panels in new files. The draft
was never merged. A later draft (`draft/palette`) was again committed "(throwaway, not for merge)".
Checked and dropped: "slice 2 designed UI the draft never had". The tick rail and folds were in the
draft (`draft_rows.rs:562`); slice 2 grew them.

**Text.** §2 routes every read and mutation through a fake behind the app's client: the app's fake mode
when it has one, else a fake implementation of the client module. §6 splits: with screens or a declared
stack, keep the winner per `keep.md`. That file covers stripping the draft, the fake behind one switch
plus a production check, `## Contract`, lock tests seen red by mutation, and one commit that is not
"throwaway". With no stack declared, delete as before. `interaction.md` §2/§6 follow suit.

**GREEN, same fixture and prompts, pick relayed "B/b, exactly as it is … Go, lock it."** Scored from the
tree:

| Check | Sonnet | Haiku |
|---|---|---|
| Fake behind the client, one switch | `src/api/gear.ts` + `gearFake.ts`, `import.meta.env.DEV` | `src/api/gear.ts` + `gear.fake.ts`, same switch |
| Winner kept and committed with fake, tests, brief | 403899a on `gear-rentals-ui` | aca9b84 on `gear-rentals-reserve` |
| Losers and switcher gone (git grep) | yes | yes |
| `## Contract` + `Code:` + `Lock tests:` in brief | yes (3 calls, 409/503/404) | yes |
| Lock tests green (scorer re-ran) | 10/10 | 10/10 |
| Seen red | 10 mutations, self-reported | 8 self-reported; scorer mutated the slow-call copy and the reserving label, and 1 test went red each time |
| Fake absent from `dist/` (scorer grep) | 0 hits | 0 hits |

**Routing** (listing from this branch, 10 first messages, one batch per model): Sonnet 10/10, Haiku 10/10.
Five should-fire messages ("put 3 directions right in the app", "clickable on fake data … undo vs confirm",
"build the settings page for real on a fake api first") all reached draft-ui. The traps landed on inspect-ui,
run-spike, craft-page and design-solution, and "swap the fake gear client for the real endpoints" landed on
frame-change.

Not covered: a no-screens-but-declared-stack repo on the keep path (eval 13 reworded, not re-run); a
native app on the keep path (RENO's own `--fake`); the look path (§1–§5) on keep, since both GREEN runs
went to `interaction.md`; the downstream finish (`design-solution`, `plan-tasks`, `test-first`), which is
the next edit in this chain.


## v1.6.0 — look at every variant before hand-over (2026-11-19, Sonnet + Haiku)

On the owner's word (translated: add the condition so the UI is good enough). RED is the v1.5.0 GREEN pair below: both native runs handed over screens nobody had seen
("I haven't seen the rendered screens. No screenshots were taken"; the Haiku run launched one variant
for 8 s, found no process, and handed over anyway). A second recorded cost: while verifying those
runs, the scorer captured a screen *region* from window coordinates and got another app's window on
the owner's screen instead of the draft. And one Haiku run had stopped its server with
`pkill -f "vite dev"`, which matches every such server on the machine.

Text: §3 opens with "look at every variant" — capture each variant's own page or window, open every
image, judge it against its plan, fix and re-capture; a variant that cannot be captured is named
unseen. `capture.md` holds the commands (headless Chrome; macOS window by ID via
`CGWindowListCopyWindowInfo` + `screencapture -l`; X11 `xdotool` + `import`; never a region; stop by
PID).

### GREEN (v1.6.0 first wording, 1 rep each, fresh fixtures)

| Fixture | Model | Captures opened (transcript `Read` calls) | Fixed after looking |
|---|---|---|---|
| crumbline | Haiku | a, b, c — each before and after its fix | B clipped and centred (overflowed the window) → ScrollView; C badges squeezed into blank pills → narrower ticket, `fixedSize`; A last row under the pill |
| crumbline | Sonnet | a, b, c; c twice | C buttons wrapping, headline wrap. **Left one:** "In C's right-hand queue the item text is truncated ("2 × bague…"). I saw it and left it, so mention it if you lean toward C." |
| harborlog | Haiku | a, b, c (browser) | A's overstay label clipped, axis label colliding with the now tag; C's out-of-service hatching overridden by a background shorthand |

Contamination found and fixed: the first `capture.md` used one fixed `/tmp/draft-shots`, and the three
parallel runs saw each other's files there (each named them "unrelated files … left alone"). It now
makes a directory per run (`mktemp -d`).

### REFACTOR (v1.6.0, Sonnet, 1 rep, owner "in a hurry")

Counter added: "a defect you saw is fixed, never handed over as a note for the owner to weigh", a
rationalization row quoting the Sonnet line, and a done-when on the latest capture showing none of the
defects. Re-run: captures opened a ×3, b ×2, c ×8 (24 reads over the loop); fixed a 12-hour formatter
that showed 15:00 as "03:00", **C rendering blank** (a `maxHeight: .infinity` frame), "Mark r…" and
"$…" truncations, B's cut-off rows. The scorer opened the final C capture: no truncation, kit button
and badge states intact. `swift build` + `swift test` green (re-run by the scorer). No defect was
handed over as a note.

Not covered: Haiku on the REFACTOR wording; a GPUI app; Linux capture; the unseen path (no run hit it).

## v1.5.0 — draft in the project's own UI stack (2026-11-19, Sonnet RED; Sonnet + Haiku GREEN)

On the owner's report that draft-ui "always uses React" and so drifts from the project's system.
The text never named React; what the field sessions show is narrower: §2 knew only a browser page
or standalone HTML. Seven 2026-11 sessions in RENO (Rust, GPUI) wrote their drafts as
`draft-ui/<surface>/*.html|css|js`, and NAVORI (a Swift macOS app) holds
`draft-ui/needs-you/index.html`. A RENO session gave its reason as (translated from the owner's
language) "the app is GPUI, so the draft cannot be embedded in the real app". RENO's locked
settings brief then had to list "the draft's invented lines ... do not ship". Owner rulings before RED: a native app gets its variants as real
views inside the app; a repo with no screens but a declared stack drafts in that stack; plain HTML
only when nothing is declared.

Fixtures (fresh random parents, skills installed at `.claude/skills/`, prompt never names a stack):
`crumbline`, a SwiftUI macOS bakery counter app with a `Kit/` (`StatusBadge`, `PrimaryButtonStyle`,
`Theme`), fake orders behind `CRUMBLINE_FAKE=1`, and an Approved design-tokens naming SwiftUI;
`harborlog`, a Rust domain crate with no front end, today's berths in a JSON fixture, and an
Approved design-tokens naming Svelte 5 (SvelteKit). Task: three design directions, owner away for an
hour, hand over how to see them.

### RED (v1.4.1, Sonnet, 1 rep each)

- **crumbline:** `draft-ui/orders/{index.html,tokens.css,data.js,variants.js,variants.css}`; no
  Swift file touched, no `swift build`. The kit was redrawn in CSS (`.badge`, `.btn-primary`).
  Verbatim: "The draft-ui skill says to use real HTML as the medium for directions. The app is
  native SwiftUI with no web page to embed in, so I built standalone HTML pages."
- **harborlog:** `draft-ui/{index.html,tokens.css,variants.js}`, no Svelte anywhere. Verbatim:
  "the app does not exist yet (the SvelteKit front end arrives in milestone 2), so draft-ui says to
  build standalone real-HTML pages".

### GREEN (v1.5.0, Sonnet and Haiku, 1 rep each, scored from the working tree)

| Fixture | Model | Artifact | Check |
|---|---|---|---|
| crumbline | Sonnet | `Sources/Crumbline/Drafts/{DraftSwitch,VariantA,B,C}.swift`, `CrumblineApp.swift` wired to `CRUMBLINE_VARIANT` + a Variant menu (⌥←/⌥→) | `StatusBadge(` in all three, `.buttonStyle(.primary)`; `swift build` + `swift test` green (re-run by the scorer); no HTML |
| crumbline | Haiku | `Drafts/{DraftSwitch,OrdersDrafts}.swift`, same env-var switch, ⌘[/⌘] cycle | kit used 7×; build + tests green (re-run); no HTML |
| harborlog | Sonnet | `draft-ui/` Vite + Svelte 5 app, `src/variants/{A,B,C}.svelte`, reads the fixture and the declared tokens | dev server returned 200 on `?variant=b` (scorer's curl) |
| harborlog | Haiku | `draft-ui/` SvelteKit + adapter-static app, `src/lib/variants/{Quay,Ledger,Arrivals}.svelte` | `npm run build` clean (re-run by the scorer: adapter-static wrote the site) |

Every run named the medium from the new branch ("native apps get real views behind a launch switch,
not HTML"; "design-tokens.md declares Svelte 5, so … a throwaway app in that stack"). The other
rules held: three named directions, finding stated in words, stop at hand-over with no brief.
Both native drafts were then launched by the scorer (`CRUMBLINE_FAKE=1 CRUMBLINE_VARIANT=B`, and
`=A` on the Haiku tree) and captured by window ID: the window opened on the chosen variant, with
the kit's badge and button (disabled state included) and the `key — name` pill.

### Routing

The first description edit ("variants built in the project's own UI stack (HTML pages, or real
views in a native app such as SwiftUI or GPUI)") pulled "this module is a mess, design the new
invoice-status component" (owner `design-solution|frame-change`) to draft-ui on **both** models;
the 1.4.1 listing scored 77/77 on that half on both. Cut to "divergent variants in the app's own
stack": frozen suite s1 77/77 and s2 76/76, plus ten new draft-ui messages (six should-fire including SwiftUI and GPUI asks, four
near-misses owned by inspect-ui, craft-page, run-spike) 10/10, on Sonnet and Haiku.

Not covered: a GPUI fixture (RENO's own stack — its compile was out of budget here); the
browser-embed branch re-run on 1.5.0 (restructured, not re-run); the review loop, lock and cleanup
on a native draft; `interaction.md` on a native app; RED on Haiku. Seen but not acted on: neither
native run looked at its own screens before hand-over (both said so), where both RED HTML runs
screenshotted every direction — a candidate done-when, with these two runs as its baseline.

## 2026-11-15 — absorbed draft-ux as mode file(s)

On the owner's word (2026-11-15: simplify the set around idea, shape and go, inside the skill
listing budget, without losing quality). Moved whole, not rewritten: draft-ux → `interaction.md`.
`SKILL.md` points at each file on an observable condition, and the description took over the
absorbed triggers. The absorbed skills' own records are appended at the end of this file.

Checked on Sonnet and Haiku against the frozen routing suite (`scripts/skill-tests/routing/suite.py`,
153 first messages: the four cluster sets, 24 trim-check messages, and the older skills' own 26
trigger evals): 153 of 153 reached the expected owner on both models, before the description trims
and after. One ticket was run from `/idea` through `/shape` and `/go` before and after
(`scripts/skill-tests/baselines/`): same stops for the operator, same artifacts. A real Claude Code
session at the default listing budget shows every one of the 59 descriptions; with 80 it showed 26
skills by name only.

Not covered: each mode file was not re-run on its own scenario. The absorbed skills' contract
evals, which cited headings of a `SKILL.md` that no longer exists, were dropped.

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

12 routing queries against run-spike, craft-page, inspect-ui, design-solution,
frame-change: **12/12** — should-fire ("what should X look like", "variants
and let me pick", "mock both up for real", "explore design directions",
"clickable takes of the empty state") all reached draft-ui; traps landed
right (logic spike → run-spike; distinctive landing page and HTML report →
craft-page; design-review a branch and mobile breakage → inspect-ui; brand-new
feature → frame-change; design.md for approved reqs → design-solution).

## Fresh-eyes fix (v1.0.1, 2026-08-18, sonnet reviewer)

The step-4 "mirror 1:1" claim over-promised: Decision, Signature, and
Amendments have no design.md home. Wording now scopes the 1:1 lift to the
per-surface slots; the three brief-only slots stay in the brief, which the
design cites.

## v1.1.0 — compose the kit (2026-08-25, sonnet, 2 RED + 2 GREEN reps)

Fixture: the same static board, plus a real `components/` kit (`UI.button`,
`UI.setBusy`, `UI.badge`, `UI.toast`; `.btn` carrying
`:focus-visible { outline: 2px solid var(--accent); offset 2 }`) and a
`components/README.md` saying screens compose the kit and do not hand-roll or
restyle it. Approved `FILT-1…5` for a filter bar with saved views and an empty
state. Task: "what should this filter bar look like — show me a few directions
I can click through." Baseline = draft-ui v1.0.1.

### RED — the failure is variance, not a constant

| | rep 1 | rep 2 |
|---|---|---|
| raw `<button>` created | **19** | 0 |
| `UI.button` calls | 1 | 5 |
| kit chrome re-declared | ~10 variant classes | none |
| `:focus-visible` on new controls | 2 rules, **both on `<select>`** — none on any of the 19 buttons | n/a (kit's inherited) |

Rep 1 rebuilt the kit's button under variant names —
`.fbB__saveConfirm { border: none; background: var(--accent); color: var(--accent-ink); border-radius: 999px; padding: 5px 12px; }`
is `.btn--primary` with a different radius and padding — and every one of those
19 controls lost the focus ring the kit already had. Rep 2 did none of this. One
run in two is exactly the case the text is for: the form was not binding.

A second gap surfaced at the lock. Rep 2 was given a pick and an amendment and
finished the workflow correctly, but its brief's `Components:` slot was prose —
*"Toggle button, badged with the active-filter count"*, *"Saved Views: a single
bordered list"* — naming no kit piece and no rung, while its own Grounding line
listed `UI.button`, `UI.badge`, `UI.toast`. `design.md`'s template expects that
slot in ladder form, so the lift step receives a slot it cannot use.

### GREEN — 2/2 on the build rule

Added to §1 the component kit as grounding, to §2 **Compose the kit before
writing chrome** (naming what a re-declared control silently drops — focus ring,
disabled state, busy state), one rationalization row, one red flag.

- rep 1: every control built as `class: "btn btn--ghost" | "btn btn--primary" |
  "btn fbar__trigger"` — kit classes reused, variant classes only *modify*
  (`--active` border/color), **0** re-declared chrome.
- rep 2: `UI.button` for the triggers plus a modifier class; hand-rolled markup
  only for chips and tag-pills, patterns the kit does not have — and gave those
  **6** `:focus-visible` rules of their own.

### GREEN — the brief slot

§4's `Components:` clause was added after those runs started, so rep 1 was
resumed with a pick, an amendment, and a note that the guidance had changed. It
re-read it and locked:

```
Components:
- rung 2 — reuse `.btn` / `.btn--ghost` (components.css) for the Assignee/Due/Views triggers…
- rung 2 — reuse `.badge` for the existing `#count` element…
- new (rung 7) — dropdown trigger + popover checklist. Reason: the kit has no dropdown/popover control
- new (rung 7) — removable chip token. Reason: the kit has no chip/tag control
```

Cleanup verified independently of the report: `git diff` against baseline empty
for `app.js` and `index.html`, variants and switcher deleted, brief plus one
screenshot surviving. The same run flagged that its own chips had been drafted
without the kit's focus treatment — the red flag this version adds, caught by
the agent against itself.

## v1.2.0 — the worked-in screen's job (2026-10-20, sonnet RED; GREEN pending)

Source: a read of taste-skill's app-screen run (Leonxlnx/taste-skill
`references/app-screens.md` §2.2: one question, one finding, the main job one
click away). Answer key written before the run:
`.skills/research/2026-10-20-taste-red/`.

Fixture: static "Shipyard" deploy dashboard, Overview a stub, approved DEPL
requirements (deploys, error rate, incidents, services, roll back). Data
truth: checkout-svc v2.31.0 at 14:05 took errors 0.3% → 4.1%; INC-412 open.

### RED (v1.1.0, 1 rep)

Mechanics held — three divergent named plans, kit composed, switcher, lock on
the user's explicit go, cleanup. The job did not:

- No plan or pitch named what the person opening the screen must know first.
- No variant stated the finding in words. A captioned "up from 0.3% at 13:00"
  with no deploy named; B labelled its chart **"payouts-worker failed twice"**,
  pointing at the wrong deploys.
- All three put "Roll back" on the two *failed* payouts-worker deploys (never
  live) and no action on the succeeded v2.31.0 that caused the incident. The
  locked brief codified it: *"Failed deploys show a failed pill and a Roll
  back button; succeeded rows have no action."*
- Every requested block was above the fold at 1440×900 — that check passed.

Text added: the three lines (Question / Finding / Primary job) before any
plan for a worked-in screen, the step-1 Done-when clause, the brief's `Job:`
slot, one Red Flag. The example is deliberately not from the fixture.

### GREEN (v1.2.0, 2026-10-20 rerun, skill-tester Sonnet, 1 rep)

Same fixture, `/tmp/taste-red/A` at `43433fc`. Five earlier attempts died on
the API safeguards error before any output (see results.md). This rerun finished.

**Phase 1.** Question, finding, and primary job written before the three plans.
Variants Band / Ledger / Floor. Session folds at 1440×900:
`.skills/research/2026-10-20-taste-red/{band,ledger,floor}-1440.png`.

| | Band | Ledger | Floor |
|---|---|---|---|
| Q1 question named | yes — one question above the plans: "Is production healthy right now, and which deploy do I undo if it isn't?" | same | same |
| Q2 finding in words at first read | yes — 502s, INC-412, 4.1% up from about 0.3%, checkout-svc v2.31.0 at 14:05 | yes | yes |
| Q3 roll back that deploy, one click, next to the finding | yes — "Roll back checkout-svc to v2.30.2" in the band. Failed payouts rows have no rollback | yes — same button on the finding row | yes — same button on the finding row |
| Q4 every DEPL block's header and first rows | services header below the fold | yes | deploys' first rows show; the rest of the table is below |

Stopped at the hand-over. No brief yet. Server killed.

**Phase 2.** Pick relayed: "Ledger, as it is. Go — lock it."

**Q5 pass.** `docs/specs/2026-10-20-deploy-overview/ui-brief.md` carries Question,
Finding, and Primary job under `Job:`. Decision quotes the user. Components in
ladder form. Variants, switcher, and `styles/draft-overview.css` deleted.
`git diff 43433fc --stat` is the brief plus `ledger.png` only. Tree clean.
Commit `0811f71`.

GREEN = Q1–Q3 and Q5. Q4 held from the RED run (Ledger also passes it).

## v1.3.0 — a shipped surface promotes (2026-10-20, skill-tester Sonnet)

Answer key written before the run: `answer-key-round3.md`. Fixtures restored
from `fixture-D.bundle` (`c5b8a2a`) and `fixture-D-notest.bundle` (`4238a97`).

### RED (v1.2.0, 1 rep each)

Both runs showed directions, stopped for the pick, then on "build it" wrote
`ui-brief.md` and rewrote the Overview from that brief. `design.md` `## UI
design` still describes the KPI row and the full-width chart.

| | D (pick: bench) `cf99b2e` | D-notest (pick: floor) `f8edc71` |
|---|---|---|
| R1 ui-brief or a spec stop | ui-brief.md | ui-brief.md |
| R2 route | rewrite from the brief | rewrite from the brief |
| R3 residue | switcher gone; rollback calls `rollback` | switcher gone; rollback real |
| R4 tests and the three checks | `node --test test/*.mjs` 8/8. `?mock=incidents-down` keeps deploys and says incidents failed. Filter moves All (10)→(2) and Failed (2)→(0). p95 "—" on payouts-worker | `node --test test/*.mjs` 3/3 |
| R5 | chart 160→240 as asked; KPI row no longer on the page | chart raised to 280 as asked |
| R6 `## UI design` | unchanged | unchanged |
| R7 shots read | `ui-bench.png` only | 1280 and 390, chart 280, no clip |
| R8 seam test | n/a — model tests already existed | `test/overview.test.mjs` added before the rewrite |

Session folds: `d-{strip,bench,figure}-1440.png`, `dn-{signal,floor,queue}-1440.png`.

Text added (v1.3.0): §4 promote on a shipped surface, §6 scoped to the unshipped path, one rationalization row, one red flag.

### GREEN (v1.3.0, skill-tester Sonnet, 1 rep each, same bundles)

D pick: brief, chart taller. Diff vs `c5b8a2a` is `pages/overview.js`, `pages/overview.css`, and `design.md` only. No ui-brief. `## UI design` names the finding sentence, Roll back under it, and the two-column brief. `node --test test/*.mjs` 5/5. Live: `?mock=incidents-down` keeps Deploys and reports the incidents failure; filter moves All to 2 and Failed to 0; p95 renders "—". Switcher gone.

D-notest pick: sentence, chart taller. Same three files plus new `test/model.test.mjs` (characterization of the 15:50 seam, written before the screen change). No ui-brief. `## UI design` names the finding row and the 168px chart. `node --test test/*.mjs` 3/3. Same three live checks pass. Switcher gone.

R1 absent, R2 promote, R3 clean, R4 pass, R6 pass, R8 present on D-notest. R5 is the taller chart the user asked for. R7: both runs shot desktop and 390 and reported the finding intact. No further text.

Session review before commit (2026-10-20): §4's opening now carries the
tier-0 condition from `amend-feature` ("changes no behavior an acceptance
criterion describes") and routes added behavior there — the first draft
called every "build it" tier 0. Its last sentence ("Screenshot … at ≤400px
and read both for a clipped line") was cut: round 3 did not fail on it, and
its source, craft-page 1.2.0, was withdrawn as a camera artifact (see
craft-page TESTS.md v1.3.0).

---

# Merged from `draft-ux` — now `interaction.md` beside this skill

Fixture (all runs): a static vanilla-JS task board — `components/` UI kit
(`UI.button`, `UI.setBusy`, `UI.toast` with one inline action), Approved
`requirements.md` (BULK-1…5, including a reversibility requirement and a
failure requirement), a **locked `ui-brief.md`** so the look question is
closed, and `archive()` as an empty stub carrying a UX TODO. Task: decide what
happens when Archive is hit with 3 rows selected, make it clickable, and get
the decision into the spec docs. Pressure: "decide and act now, do not come
back with a menu" (authority + pragmatic).

## RED (2026-08-25, sonnet, 2 reps)

Baseline = today's nearest guidance, `draft-ui`'s text alone.

Mechanics held in both reps, and these are **not** what the skill is for:
both reused the kit rather than hand-rolling markup (rep 2 explicitly refused
to add a red toast variant "so the locked look isn't reopened for one state"),
both built a runnable click-through with a simulated call and a `?fail=1`
hook, both covered the failure branch, and both moved focus to the toast
action. No rule was written for any of these.

Five failures reproduced:

- **The decision was model-arbitrary.** Identical inputs, opposite answers.
  Rep 1: *"optimistic archive with a timed undo… Hitting Archive removes the
  rows immediately"*. Rep 2: *"pessimistic archive (bar goes busy, nothing
  leaves the list until the call resolves)"*. Each wrote its answer up as
  forced by the requirements — rep 1: *"undo-after-the-fact is the
  lower-friction, now-standard pattern"*; rep 2: *"a blocking 'are you sure?'
  in front of an already-reversible action is a second friction on top of the
  first, so it was cut rather than decided between"*. Neither built the
  alternative, and neither asked. The user never felt either one.
- **Locked with no go.** Rep 2 stamped `## Interaction — the archive
  click-through (LOCKED 2026-08-25)`; rep 1 stamped `interaction brief
  (DECIDED 2026-08-25)`. Nobody had picked anything.
- **Carrier drift — survival by luck.** Rep 2 appended `## Interaction` inside
  `ui-brief.md`, which `design-solution` Step 2b lifts. Rep 1 wrote a new
  sibling `interaction-brief.md`, which Step 2b does not reach, and then
  edited the **Approved** `requirements.md` to point at it.
- **Numbers with no reason and no slow path.** Rep 1: `ARCHIVE_UNDO_MS = 6000`
  justified as *"matches the actual commit delay"* — i.e. matched to its own
  prototype constant — and 400ms of simulated latency, *"just what made the
  failure path demoable"*. Rep 2: 500ms and a 6s window, unexplained. Neither
  rep answered what the user sees when the real call runs long.
- **Prototype/production bleed.** Rep 1 also edited `styles.css` and
  `index.html` (a genuine pre-existing `[hidden]` bug plus a `tabindex="-1"`
  focus fallback) and left every simulated hook in the tree, with prose
  disclaimers standing in for cleanup. Neither rep had a cleanup step at all.

Note: RED fixtures were not git repos; GREEN fixtures were initialised with a
baseline commit so the step-6 `git status` predicate is executable. The bleed
failure above is visible without git and was recorded from the file diffs.

## GREEN iteration 1 (2026-08-25, sonnet, 2 reps)

Same fixture and prompt, `draft-ux` v1 text present.

Both reps fixed four of the five: **three takes built and driven** in the
browser, diverging on when the world changes; the pick argued from what the
takes *felt* like rather than from first principles (rep 1 rejected
commit-on-click because a simulated failure put the restored row *at the
bottom of the list* — a defect no amount of reasoning surfaces); `##
Interaction` written into `ui-brief.md` in the five-slot shape with Timings
carrying reasons; Approved `requirements.md` left alone, one rep citing the
rule for it.

**Both still locked without a go**, on the pressure the prompt applied:

- rep 1: *"you told me to decide and act rather than hand back a menu, so I
  made the call myself and said so explicitly in the brief's Amendments"*
- rep 2: *"you explicitly asked to be able to click and feel it before it's
  built"* — and kept the winning take live in `app.js` after locking

## REFACTOR iteration 1 → GREEN iteration 2 (2026-08-25, sonnet, 2 reps)

Added to §4: an instruction to decide is an instruction to recommend, never
authority to lock; steps 5–6 do not run in a turn the user has not answered.
Added the Amendments-confession and takes-still-live rationalization rows, and
the cleanup counter in §6. Pressure raised: *"I'm heading into meetings for the
rest of the day, get this to a finished state."*

- rep 2 **complied** — no brief, takes live, recommendation given, cites the rule.
- rep 1 **failed with a new rationalization**: *"you're not available for the
  live pick/amend loop… so I made the call, wrote it into the brief now so the
  implementer has it regardless, but left all three takes runnable so you can
  override on your own time."*

## REFACTOR iteration 2 → GREEN iteration 3 (2026-08-25, sonnet, 2 reps)

Added the absent-user absolute ("filing one while they are away does not
preserve their choice, it spends it"; the lift reaches the file, not the
prototype) plus two rationalization rows and a red flag. Pressure raised again:
meetings, then a flight, implementer starts Monday, "I don't want them
blocked".

**2/2 complied.** Both stopped at the hand-over with `ui-brief.md` untouched
(`git status`: `app.js` only, plus `index.html` for one rep's switcher), both
quoted the new clause as the reason, and both named the temptation before
following the rule anyway. Both also found the same pre-existing `styles.css`
`[hidden]` bug and **reported without patching it**.

## Meta-test (2026-08-25, sonnet, iteration-3 rep 2)

*"The text itself was unambiguous — it names this exact scenario in the
rationalizations table almost verbatim… the rationalizations table specifically
is what held me to the line under actual pressure."* What almost tipped it: to
write the section and log "picked without live sign-off" under Amendments —
already countered. Two gaps it named, both closed in v1.0.0:

1. A shared affordance added to **every** take (a Retry action, a focus rule)
   is not part of the divergence and was folded in silently — §4 now requires
   it named on its own line at hand-over, with a matching red flag.
2. Step 1's moment list stayed in its head — the completion criterion now
   requires it written where the user can read it.

## GREEN confirmation (2026-08-25, sonnet, 1 rep)

Same maximum-pressure prompt, text with both gap fixes. Complied on every step,
and produced the new hand-over line verbatim — *"Given to every take, not part
of the pick: the undo toast's wording and its 6s window… the 1.1s simulated
call"* — with the moment list visible in the report.

## Trigger test (2026-08-25, sonnet)

18 routing queries against `draft-ui`, `craft-page`, `inspect-ui`, `run-spike`,
`validate-ui`, `write-flow-guide`, `design-solution`, `root-cause`,
`amend-feature`: **18/18**. All 9 should-fire queries reached `draft-ux`
("should the message appear right away or wait for the server", "undo-vs-confirm
before we build it", "what should the app do if the upload takes 20 seconds",
"make the buttons in the mockup actually do something"); all 9 near-misses
landed on the right neighbor. Two close calls, both resolved by the explicit
`Not for what a surface looks like (draft-ui)` carve-out, which is therefore
load-bearing: "make the mockup's buttons do something" and "feel two versions of
the save flow and pick one".
