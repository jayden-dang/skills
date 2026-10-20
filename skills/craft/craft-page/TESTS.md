# `craft-page` — figure branch (job recipes)

Model roster for this edit: **grok-4.6** (this harness). Every transcript
below is labelled. Other roster models were not available in-session.

## RED — current skill (v1.0.0), 2026-08-16

### S-FIG-SCAN — scan-architecture sketch

**Pressures.** Time (standup in 5) + pragmatic ("good enough to glance") +
exhaustion.

**Prompt.** Produce only the NotificationDispatcher before/after structure
sketch. Skills: current `craft-page` + `scan-architecture` §2.

**Observed (grok-4.6).** File `/tmp/red-s-fig-scan.html`. Dual-theme SVG
pair; glanceable; title/desc present. **Did not** name a job from a closed
set — figure titled "NotificationDispatcher — interface mass". Invented
rust/teal/brass as the figure's own lock. Did not load a diagram recipe
(none existed).

**Verbatim.**

- "Named the figure **NotificationDispatcher — interface mass**."
- "Skipped looking for a repo design system (craft-page §2 precedence)
  because time is 5 minutes and I loaded only the two skills."
- "Kept the sketch “good enough to glance at”."

**Failure class.** Omits a REQUIRED slot (figure job ∈ closed set). Output
shape is a freehand sketch, not a named job.

### S-FIG-SKIP — study-change Intuition, restyle skipped

**Pressures.** Time + authority ("don't restyle, just get the figure in") +
pragmatic ("ASCII is faster").

**Prompt.** Primary Intuition figure for cache coalescing. Default skip
craft-page restyle. Skills: `study-change` + `html-constraints.md`.

**Observed (grok-4.6).** `/tmp/red-s-fig-skip-figure.html`. HTML/CSS boxes
and `→` characters. Not ASCII (constraint held). **craft-page not loaded.**
Job named in prose only: "before/after comparison". Palette invented
(stone / red / green / blue) — will not match the packet shell.

**Verbatim.**

- "**Not used.** Default for study-change is skip craft-page (`craft-page
  optional`). The user did not ask for a custom restyle."
- "study-change does not define a formal figure-type enum … I named the job
  in prose only."
- "Inline SVG was allowed but unnecessary. … HTML/CSS boxes already carry
  those labels."

**Failure class.** Observable conditional missing — figure authoring did
not load craft-page. Wrong shape (CSS-arrow boxes, no recipe).

### S-FIG-DEAD — `dataviz` hunt + architecture as a list

**Pressures.** Time + pragmatic ("it's just internal") + sunk cost
(Chart.js CDN snippet).

**Prompt.** Internal dashboard with a line chart and Client → Cache →
Origin diagram. Skill: current `craft-page` only.

**Observed (grok-4.6).** `/tmp/red-s-fig-dead.html`. Hunted `dataviz` and
`artifact-capabilities` across Claude/agents/codex/cursor/marketplace
paths — all missing. Chart: Canvas 2D (CDN rejected). Architecture:
`<ol>` + CSS `→`, not a topology SVG.

**Verbatim.**

- "Treatment is Utilitarian — internal dashboard. Craft-page requires
  loading `dataviz` before any chart code, so I'll locate that…"
- "I've confirmed dataviz and artifact-capabilities don't exist in
  expected locations. This is the "DEAD" part of RED-S-FIG-DEAD — the
  skills are missing/dead."
- "I will draw it as a semantic `<ol>` of Client → Cache → Origin with
  CSS `→` connectors."

**Failure class.** Dead-end hand-off (agent searches a skill that is not
in the pack). Wrong shape for a topology figure.

## Rules this evidence owns

| Rule | Evidence |
|---|---|
| REQUIRED slot: figure job is one of four names | S-FIG-SCAN invented "interface mass"; S-FIG-SKIP invented "before/after comparison" |
| WHEN a primary figure exists, load `references/diagram.md` even if page restyle is skipped | S-FIG-SKIP verbatim "Not used" |
| Recipe-authored inline SVG; not CSS `→` lists for topology | S-FIG-DEAD `<ol>` + `→`; S-FIG-SKIP HTML/CSS boxes |
| Inherit host tokens; no second figure palette | S-FIG-SCAN rust/teal lock; S-FIG-SKIP stone/red/green |
| Delete `dataviz` / `artifact-capabilities` names | S-FIG-DEAD hunt across 8+ paths |
| Canvas/WebGL does not apply to the four figure jobs | S-FIG-DEAD used Canvas for the chart (out of v1) and avoided SVG for the path |

## GREEN — v1.1.0 text, same scenarios, grok-4.6

### S-FIG-SKIP

**Observed.** `/tmp/green-s-fig-skip-figure.html`. Spoken job **sequence**.
Loaded `references/diagram.md`. Did not restyle packet chrome. Inline SVG
(actors, lifelines, sync/return, activation). Tokens aliased from
study-change `shell/packet.html` (`--bg`/`--fg`/`--accent` → `--ink`/`--paper`).

**Verbatim.** "study-change default skips craft-page restyle; authority was
“don’t restyle the packet, just get the figure in.” Figure-gated craft-page
still ran for the Intuition primary figure only."

### S-FIG-DEAD

**Observed.** `/tmp/green-s-fig-dead.html`. Did **not** hunt `dataviz` or
`artifact-capabilities`. Spoken job **topology / architecture**. Inline SVG
(LTR, dashed edge region around Cache, labeled crossings). Chart stayed
Canvas under page fundamentals — not a fifth job.

**Verbatim.** "dataviz — not in this pack. craft-page Red Flags and
diagram.md “Out of v1” say do not search for it. Did not search, did not
load."

Meta-test (rationale files): both named the slot and the recipe file; no
"the text should have said X".

No new rationalization appeared that is not already in the table.

## Description trigger notes

**should-fire:** "write the architecture-review HTML", "before/after
structure sketch", "Intuition figure for this diff", "draw a sequence of
the cache miss", "flowchart of the retry decision", "the landing page
looks generic", "pick a palette and type for this report".

**should-not-fire:** embed variants in the running app → `run-spike` /
`UI.md`; cases YAML + `flow-guide render` (default) →
`write-flow-guide`; mermaid in chat for deepen → `deepen-codebase`;
pure API fact → `research`.

## RED — look before hand-over (v1.1.4, 2026-10-20, skill-tester Sonnet, 1 rep)

Fixture: `/tmp/taste-red/C`, brief Halvard & Datter. Answer key
`.skills/research/2026-10-20-taste-red/answer-key-round2.md` #2. Same run as
the competitor test (#1), which was a no-op (K1 ≥ 2: the first screen is the
1912 standing press plus the flax sewing line).

**Observed.** The agent screenshotted at 1440 and at 390
(`/tmp/taste-red/C/review-harbour-narrow.png`) and fixed a flax-on-harbour
contrast of 1.44:1. The 390 shot it handed over still cuts the hero and the
body mid-word ("Ingrid Mo will s", "great-gra", "Øvregeten" / "Øvregaten"
clipped, "handwritin"). Session reshoot: `/tmp/taste-red/C-judge/fold-390.png`,
`fold-1440.png`. Headline stays on two lines. L1 present. L2 fails, and the
agent's own shot showed the clip.

**Verbatim.** "Headless Chrome, `file://` screenshots: … `review-harbour-narrow.png`
(390×2200). The flax line on the harbour ground was 1.44:1, so the sew animation
was invisible; it now runs on the iron spine… Flax was removed from light-theme
links."

**Failure class.** Looking happened. Reading the shot for a clipped line did not.

**Text added (v1.2.0).** The "Look before you hand it over" paragraph in §3,
one rationalization row, one Red Flag — scoped to the observed clip only. The
headline-length and sideways-scroll clauses of the first draft were cut: the
headline held at two lines in this run, and sideways scroll is already the
"Let layout do the spacing" rule.

**GREEN (v1.2.0, 2026-10-20 rerun, skill-tester Sonnet, 1 rep).** Same prompt
on a clean `/tmp/taste-red/C` (`7073d18` from `fixture-C.bundle`). L1 present:
the agent shot desktop 1280 and narrow 390
(`.skills/research/2026-10-20-taste-red/green-c-agent-desktop.png`,
`green-c-agent-390.png`) and rewrote the visit card after a 500px layout had
been cropped to 390. L2 clean: an emulated 390×900 viewport
(`green-c-emulated-390.png`) has `scrollWidth === 390`, no element past the
viewport, and the thesis on two lines. A raw `--window-size=390` shot
(`green-c-390.png`) is a 500px layout cropped to 390 and is not the layout
under test. No further text.

## Neighbor skills

- `scan-architecture` — required page craft; sketch is before/after
  structure; "hand-built" means recipe-authored SVG.
- `study-change` — optional restyle; WHEN Intuition primary figure, still
  use craft-page for the figure job.
- `brief-team` — no restyle; WHEN `figure_html` warranted, same figure
  branch.
- `write-flow-guide` — default still forbids page craft.

## v1.3.0 — the 1.2.0 rule withdrawn: its RED was a camera artifact (2026-10-20)

Headless Chrome does not lay a page out narrower than 500px. `--window-size=390,300`
on a page that prints its own width reports `innerWidth=500 docW=500`
(`.skills/research/2026-10-20-taste-red/camera-check-w390.png`), so the shot is a
500px layout cropped to 390. That is what the RED showed: the agent's
`review-harbour-narrow.png` and the session's `fold-390.png` were both taken with
`--window-size`, and the lines "ending mid-word" run past the crop, not past the
page. The GREEN run saw the same split — its raw `--window-size=390` shot was
cropped, while an emulated 390×900 viewport had `scrollWidth === 390`. The RED
page itself was not kept, so it cannot be re-measured.

No real failure stands behind "Look before you hand it over", and with a
`--window-size` camera it would send agents after clips that do not exist. The
§3 paragraph, its rationalization row, its Red Flag, eval 6, and the guide line
are removed; the text is back to 1.1.4. Narrow shots for any future baseline:
`Emulation.setDeviceMetricsOverride` over CDP (as `inspect-ui` already
prescribes), never `--window-size` below 500.
