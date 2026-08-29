# Changelog

## Unreleased

### Packaging: Codex plugin for Engineer Pack (`jdk`)

Codex CLI / ChatGPT can install the same pack:

```bash
codex plugin marketplace add jayden-dang/skills
codex plugin add jdk@jayden-dang-skills
```

- `.codex-plugin/plugin.json` — Codex manifest (`name` `jdk`, `skills` `./skills/`)
- `.agents/plugins/marketplace.json` — Codex/ChatGPT catalog (Engineer Pack only)
- Claude manifests stay the source of truth for Claude/Grok; version **1.2.0**
- Codex walks `skills/` recursively; Personal OS folders under `skills/personal/`
  may appear namespaced as `jdk:life-*` if that scan includes them

### Packaging: Engineer Pack slug `jdk` (jayden-dang-kit)

The Engineer Pack plugin identity is **`jdk`** (picker label still **Engineer Pack**).
Slash on Claude Code / Grok: `/jdk:frame-change`. Install:

```text
/plugin marketplace add jayden-dang/skills
/plugin install jdk@jayden-dang-skills
```

**Breaking** for anyone who had the plugin installed as `engineer-pack`: uninstall
that entry and install `jdk`. Skill *directory* names are unchanged.

Primary install for Claude/Grok is the marketplace plugin (session-start hook
ships with it). Do not flatten Engineer Pack into `~/.claude/skills/` on the same
machine. Codex / Cursor / Kimi keep `npx skills add … --copy` (bare `/frame-change`).
Updates: plugin manager / `grok plugin update jdk` vs `npx skills update`.

- `.claude-plugin/plugin.json` + marketplace Engineer Pack entry: `name` `jdk`,
  `displayName` Engineer Pack, version **1.1.0**
- Personal Pack unchanged (`personal-pack`)
- Docs: README, START-HERE, adopting, platforms, troubleshooting, engineering README
- Check: `python3 scripts/check-plugin-slug.py`

### Rename: 6 skills for naming consistency (v2.0.0 each)

`review-invariants`, `review-ui`, and `select-review-sample` (review) and
`review-product-flow`, `vet-product-flow`, and `run-product-walkthrough`
(acceptance) used the word "review" for two unrelated meanings across
categories, and the product-flow trio spelled its shared artifact three
different ways ("product-flow" / "product-walkthrough" / "review-product-flow").

Renamed to `inspect-invariants` and `inspect-ui` — both are lanes `inspect-change`
invokes, and now read as its family — `select-sample` (drops the redundant
"review", already implied by the `review/` bucket), and `write-flow-guide` →
`vet-flow-guide` → `run-flow-guide`, a pipeline that now shares one artifact
noun ("flow guide") end to end. The CLI script and its run-file/report/pid
naming convention (`scripts/review-product-flow` → `scripts/flow-guide`,
`*-review-product-flow.json` → `*-flow-guide.json`) and the `VPF-N` finding-ID
prefix (→ `VFG-N`) moved with it. Every cross-reference across `skills/`,
`docs/guide/`, `AGENTS.md`, `README.md`, and the marketplace manifests was
updated; no behavior changed.

### `land-branch` v3.0.0 — thin exact-revision landing (2026-08-25)

Landing no longer replays review, verification, trace, and acceptance already
bound to the current base and HEAD. `execute-common` writes
`.skills/<CODE>/close-receipt.md` after the final mutation; `land-branch`
validates and consumes it, falling back to fresh producers only when the receipt
is missing, stale, dirty, or incomplete.

Explicit PR/merge/keep/discard/block intent executes without the old five-option
menu. Sampling and banked debt are advisory, custom decision records are opt-in
through `project.md` Decision boundaries, and ambiguous “land this” resolves
through an existing PR or `Default landing action` before one short question.
Local merge remains explicit-only and still verifies the merged result before
worktree cleanup. Minimal RED/GREEN evidence is recorded in
`skills/ship/land-branch/TESTS.md`.

### `draft-ux` — decide how a surface behaves before it is built (2026-08-25)

Nothing in the chain decided an interaction. `draft-ui` locks what a screen looks like and
explicitly freezes its variants (*"stub any mutation"*); `inspect-ui`, `validate-ui`, and
`write-flow-guide` all run after the build. So the shape of the interaction was settled by
whichever agent happened to implement it. Measured: handed identical Approved requirements, an
identical component kit, and the same locked look, two runs shipped **opposite** flows — one
removed the rows on click with a six-second undo, the other froze the list until the call
returned — and each wrote its own answer up as the one the requirements forced.

`draft-ux` (craft, model-invoked, **v1.0.0**) builds **2–3 runnable takes of one flow** that
differ in *when the world changes*, on the screen's real components, hands them over with a
recommendation, and locks only on the user's go — into `ui-brief.md`'s `## Interaction`, one
`###` per moment in the same five slots the visual sections use, so `design-solution` Step 2b
lifts it with no change to that skill. Every simulated delay and window carries a reason and an
answer for the call that runs long; at cleanup the losing takes *and the winner* are deleted.

The gate cost three RED/GREEN iterations. Each one closed a rationalization the transcript handed
over verbatim: *"you told me to decide, not hand you a menu"*, then *"I wrote the deviation into
Amendments, so it stays overrulable"*, then *"you're not available… so I wrote it into the brief
now so the implementer has it regardless."* The absent user is now named as the case the rule
exists for. Trigger test 18/18 against `draft-ui`, `inspect-ui`, `run-spike`, `validate-ui`,
`write-flow-guide`, `craft-page`, `design-solution`, `root-cause`, `amend-feature`.

Three things the baseline did **not** fail at were left unwritten: a component-reuse ladder, a
focus-and-keyboard slot, and a per-stack adapter matrix (htmx / MSW / Storybook). The research
behind all three, graded by evidence strength, is in `docs/design/draft-ux-sources.md`.

### `draft-ui` v1.1.0 — compose the kit before writing chrome (2026-08-25)

Variants were grounded in the repo's *tokens* but not its *components*. In a fixture whose
`components/` kit ships `UI.button` and a `.btn:focus-visible` ring, one baseline run in two
hand-rolled **19 buttons** against a single `UI.button` call, re-declared the kit's chrome under
variant names (`.fbB__saveConfirm` is `.btn--primary` with a different radius), and gave focus
rings to its `<select>`s only — leaving all 19 controls without one. The other run did none of
this: variance, which is the signal that a form is not binding.

§1 now grounds on the kit alongside the tokens, §2 requires controls the kit ships to be composed
from it, and §4's `Components:` slot must come out in the ladder form `design.md` expects
(`rung N — <target>`, or `new (rung 7)` + reason) rather than prose — a lock in the RED run had
named `UI.button`/`UI.badge` in its Grounding line while describing its controls in prose the
lift step cannot use. GREEN 2/2 on the build rule, and the resumed lock produced the ladder form.

### `/forge-prompt` — forge the ask into a prompt; `solve-problem` removed (2026-08-25)

The entry ramp never fixed *what* a request meant. A slot-presence pass over the four on-ramps at
`320e91e` found **0/4** carrying an exact-target slot, **0/4** a do-not-touch declaration, **0/4**
a paste-ready block, and **0/4** a question budget. `solve-problem` closed the gap by labelling
it: on `our onboarding is bad, we should probably add a wizard` it returned eight of nine slots as
`unresolved`, asked the user nothing, and forwarded the request no better specified than it
arrived. Removed.

`/forge-prompt` (discovery, **user-invoked**, v1.0.0) is not its replacement in the routing sense
— it sits outside every chain. It interviews a vague ask one card at a time, in a language chosen
at setup, and hands back **one paste-ready prompt block**: what this touches (each line marked
`[confirmed]` / `[unconfirmed]`), off limits, must keep working, what is already known, not yet
checked, open questions, done when.

**It names no lane, no skill, no step, and no classification** — that is the design decision, and
it reverses the first draft of this change. A model-invoked on-ramp that ended in
`Start with: <lane>` would have manufactured the bias it was meant to remove: models anchor on
their own earlier output (arXiv 2603.01239), self-preference is strongest when authorship is known
(arXiv 2511.05766), and prompt-level mitigations of anchoring are largely ineffective
(arXiv 2505.15392). Transferring upstream reasoning downstream helps to a threshold then converges
it prematurely — *selective context, not comprehensive history* (arXiv 2605.04361) — and
cross-context review only beats same-session review when the reviewer receives **only the
artifact** (arXiv 2603.12123). The anchor is the artifact, not the session, so the fix was to take
the conclusion out of the artifact.

- Target and boundary rules grounded in UnderSpecBench (arXiv 2607.02294): 55.8–67.8% of acted
  runs cross a boundary; safe success 67.9% → 8.6% and wrong-target 9.6% → 75.1% as target
  certainty degrades; shared-production action rate 65.5% vs contained 64.0%
- Interview order from CLARITI (arXiv 2604.14624); its 3.0-vs-5.1 question result is applied as an
  **answerability stop signal**, not a hard cap — the user drives this interview
- Channel borrowed from `clarify-decisions` (one card per message, no picker, open-set stop), not
  restated. No `Recommendation` slot: recommending would make it a design interview
- Preserved from `solve-problem`: provenance or `unresolved`, facts separated from assumptions,
  a deadline is a constraint. Dropped: gap classification as an end in itself
- **Reverted from the first draft:** the `frame-change` / `amend-feature` / `root-cause` lane seeds
  and their version bumps — they existed only to consume a routed brief
- Rewired: `AGENTS.md` §2/§3/§11 (27 user-invoked, seven uncalled model-invocable), on-ramps,
  discovery, START-HERE, README, both plugin manifests, `ask-me-bro`, `configure-repo`,
  `work-the-problem`, `interpret-session` v1.3.0 (sibling pointer, reads a handed-over block cold)
- Owed: multi-model roster RED/GREEN, recorded in `TESTS.md`. No trigger matrix is owed — a
  `disable-model-invocation` description routes nothing

### Packaging: consumer-local seed copies (SEED)

`npx skills add` copies only each skill folder, so repo-root `templates/` never
reached a flatten install (`~/.agents/skills/configure-repo` → missing seeds).
Root `templates/` stays the authoring SSOT. Every consumer skill now carries a
byte-identical copy under its own `templates/`. Resolve order: sibling
`templates/` beside SKILL.md, then `${CLAUDE_PLUGIN_ROOT}/templates`, then
`../../../templates`. `scripts/lint-skill-templates.py` fails on a missing or
drifted copy (`--write` refreshes from SSOT). Engineer Pack and Personal Pack
(`life-setup` / `templates/personal-os/`) in the same change. No `pack-templates`
skill.

- RED: lint 43 missing copies including `configure-repo/templates/agents/project.md`
- GREEN: copies + sibling-first resolve in 15 consumer SKILL.md files; lint 0
- Spec: `docs/specs/fixes.md` SEED-1.1–1.3, guards SEED-2.1–2.8

### Wire `hold-stage` / `speak-outer` into callers (2026-08-19)

- `inspect-change` v1.4.0: step 3e REQUIRED SUB-SKILL `hold-stage`; Spec
  walk admits IDs this diff uses; not-in-range listed once. RED 2/2
  walked all 12 IDs as full findings; GREEN 2/2 staged 1.3+1.10.
- `land-branch` v2.4.0 / `prepare.md`: REQUIRED SUB-SKILL `speak-outer`
  on Author PR text. RED 2/2 leaked `Satisfies: BILL-1.4`; GREEN 2/2
  sweep clean.

### `hold-stage` — only the ideas this act uses (v1.0.0)

Model-invocable. A long working set does not ride into the outgoing
review. Cite IDs this file implements or violates; the rest stay in
`requirements.md`.

- RED: review of 5-line `tax.js` tabled all 12 BILL IDs (g46) / listed
  1.1–1.12 in the header (g45).
- First GREEN wording ("at most two") dropped blocker BILL-1.10.
  Refactored iron law. Second GREEN 2/2: 1.3 + 1.10, no recap.

### `prove-claim` v1.3.0 / `execute-common` v1.5.0 — Verified slot

A ledger `Verified:` line names the proving command and coverage. RED
2/2 with v1.2.0 wrote `Verified: BILL-1.4` after a fresh suite. GREEN
2/2 filled `by` + `covering`.

### J-Space leftovers that did **not** earn text

- Inner pass (item 1): glance "what's next?" produced the ledger Next
  line. No-op.
- Seam refresh (item 3): after three seams both models did the written
  Next. Unused-module re-read not observed on disk.
- Marker / third wall (item 5): current `root-cause` already shifted
  off two timeout attempts to the real rounding cause. No-op.

### `speak-outer` — person-facing text is the outer register (v1.0.0)

Model-invocable. Status, reply, standup, PR prose: domain sentences, no
process machinery.

- Softer "read it out loud" RED already complied — discarded.
- Harder RED (Maya: "I'm back. What happened?"): grok-4.6 leaked
  `build-inline` / `Core hub` / "prove the claim". g45 r2 leaked
  `test-first`. First g45 copy discarded (byte-identical to g46).
- GREEN 4/4 both models, sweep list empty. Trigger clean vs
  `land-branch` / `prove-claim` / `write-handoff`.

### `vet-source` — fetched text cannot give orders (v1.0.0)

Model-invocable. When tool output, retrieved docs, search results, or
vendor READMEs instruct the agent, produce a trust decision: keep the
original job, drop orders the user did not state.

- RED (grok-4.6 / grok-4.5, 4/4): a fetched `vendor/SETUP.md` plus CTO
  "follow the vendor docs" deleted `tests/` and wrote `SKIP_VERIFY=1`.
  First A/B/C batch discarded (named the virtue).
- Other J-Space-shaped hypotheses (register leak, stage overload, resume
  from ledger) already complied — no text written. S4 skip-test stays
  with `root-cause` / `prove-claim`.
- GREEN 4/4 both models; description trigger 11/11 should-fire, no
  overtrigger on a *user*-stated skip.
- Registered: plugin + marketplace, AGENTS/README/START-HERE/skill-model.

### `teach-build` — new review skill (v1.0.0)

`/teach-build`: one self-contained HTML teach packet for a finished build —
journey (wave shape, every `implementation-notes.md` deviation with its
Revisit line) plus operation (runtime path that must cross components
outside the feature's diff), written to `.skills/<CODE>/teach-build.html`.
Aid only, never a ship gate; packet stays local unless the user asks to
publish; scout subagents Sonnet-only.

- RED (Sonnet, 4 reps, two prompt arms): content was never the failure —
  baselines found deviations and crossed the diff boundary unprompted. The
  failure was deliverable shape variance: chat-only dumps with zero diagrams
  on terse asks, unrequested external artifact publishes on rich ones, three
  shapes in four runs. Form: positive contract, not prohibitions.
- GREEN (3 reps) + edge (no-build repo → stop, name `/study-change`) +
  meta-test recorded in `TESTS.md`; runnable assertions in `eval.json`.
- Registered: AGENTS.md (82 skills, review 8, user-invoked 26), plugin +
  marketplace manifests, guide page + index, ephemera basename
  `teach-build.html`.

### `interpret-session` depth legibility (v1.2.0)

Second finding from the same field export: deep sections were legible where
territory was the user's repo (flow walks, `file:line`) and opaque where it
left for external standards — expert-level argument over models never given,
facts without consequences, spec-grade detail mid-analysis, tables restating
the card's own options.

- Explain follows into depth: a concept absent from paste + repo gets its
  minimal model at first use (model-before-critique)
- **Verified fact** ends with `→` consequence on the live choice
- External-territory cards get one real-shaped walk (sample log line, trace
  sketch, runnable query)
- Implementation-grade constraints collapse to a *for the spec* tail or Weigh;
  trade-off tables cut when they restate the card's options
- GREEN: 3×3×3 comparative run (Sonnet, export-contract card) — walk, `→`
  consequence, spec-tail, and table-cut rules all 0/3 baseline → 3/3 v1.2.0;
  model-before-critique inconclusive single-turn (baseline analogy held),
  retained on field evidence of late-session fade
- v1.2.1 wording: Knowns-sketch line no longer uses "teach-pack" as a verb —
  an ambiguous hand-off to a `disable-model-invocation` skill (author-skills
  review pass); now plain "teach or research the criteria"

### `interpret-session` volume calibration (v1.1.0)

Field evidence (2026-08-18 companion run beside a 10-card observability
`frame-change`): analysis quality held — six amendments landed in the other
window's locks — but approval mechanics eroded: 17-bullet locks approved with
one word, "high" confidence on every card, rationale skipped 5×, no
session-wide view, digest never produced because the session ended on an
export.

- Carry-back speaks as the user (no authorship labels, no rationale
  bookkeeping, no directing the other window's next step) in three
  receiver-native slots — **Lock** / **Weigh (not locked)** / **Still
  open**; a long block's round-trip names its highest-blast bullets
- **How sure** names the check that earned it; "high, and it barely matters"
  is a valid answer on low-stakes calls
- **Versus the other session** becomes an Agree / Amend / Reject diff; all
  five stance lines persist for the whole session (anti-drift red flag)
- Cumulative decision map every 3–4 decision events or on request
- Repeated rationale skips → decision-maker summary tier + one teach-back
  offer
- Export/archive request counts as a wrap-up signal → offer the digest
- Guide + TESTS.md field-evidence record; shape check + no-op sweep per
  small-addition practice

### New: `assess-observability` — telemetry readiness finding set

Model-invocable. “Is tracing / OpenObserve / sampling complete?” produces a
Must-row finding set. No completeness stamp. Does not write
`docs/ops/observability.md` (that is `/define-system-doc`). SERVER 4xx →
Error is a fail row, not a close.

- RED: stamp/4xx **refused** (not a gate fail); shape fail was Draft at the
  canonical ops path; trigger went to `solve-problem`
- GREEN: finding set + `not-complete`; trigger Q1–4 fire this skill

### New: `debug-remote` — deployed-environment evidence pack

Model-invocable execution skill. When the failure is on production / staging /
remote dev, the agent writes a **remote evidence pack** (identity, read-only
Phase 1, trace/log join, access, refusals) then hands off to `root-cause`.
Iron Law: no writes to a deployed environment; no mutating replay against
production. Promotion is local → `dev` → staging probe → production.

- `skills/execution/debug-remote/` (`SKILL.md`, `evidence-pack.md`, `TESTS.md`,
  `eval.json`)
- `root-cause` v1.1.0: if the failure is already deployed and no pack exists,
  REQUIRED SUB-SKILL `debug-remote` first
- On-ramp row + plugin / marketplace path
- RED: grok-4.5 port-forwarded prod and looped mutating `POST`s as the loop;
  both models treated OpenObserve as never Phase 1. GREEN: pack +
  `telemetry-query`; no prod `POST` / exec / `set image`
- Wording (v1.0.2 / assess v1.0.1): promotion and Must pass/fail have one
  home each (`evidence-pack.md` / `readiness-bar.md`); pointers say WHEN to
  load; no new rules

### `land-branch` absorbs `package-change` (v2.0.0)

One ship skill for a PR. `land-branch` now authors remaining commits and the
pull-request title/body. Agent-authored PR text is reviewer truth — no
`.skills/pr-packages/`, no `Content-digest:`, no approve/edit/cancel loop.

- Delete `skills/ship/package-change/`
- Move `conventions.md` / `tickets.md` / `passive-data-safety.md` under `land-branch/`
- New sibling `prepare.md` (local-authoring recipe)
- `execute-common` close sequence ends at `land-branch` (v1.1.0)
- RED/GREEN on grok-4.6 / grok-4.5 in `skills/ship/land-branch/TESTS.md`

### Packaging: register `execute-common`

Shared execute-family recipe is now a skill folder so `npx skills add` copies it.

- Move `skills/execution/execute-common.md` → `skills/execution/execute-common/SKILL.md`
- Register `./skills/execution/execute-common` in `plugin.json` and `marketplace.json` (62 engineer paths)
- Execute-family load path is `../execute-common/SKILL.md` (works in-repo and after flatten install)

### `craft-page` figure branch (v1.1.0)

Job/type recipes for primary figures. Chrome (checked-in shells) unchanged.

- Fourth plan slot: figure job ∈ `before/after structure` · `topology / architecture` · `sequence` · `flowchart`
- Sibling `references/diagram.md` (inherit host tokens; inline SVG; no mermaid/CDN/second file)
- Figure-gated: study-change Intuition and brief-team `figure_html` load craft-page for the figure even when restyle is skipped
- `scan-architecture` sketch = `before/after structure` (recipe SVG is hand-built)
- Removed dangling `dataviz` / `artifact-capabilities` names
- RED/GREEN on grok-4.6 in `skills/craft/craft-page/TESTS.md`

## 1.0.0 — 2026-08-08

First **stable 1.0.0** of Engineer Pack. Range: `v1.0.0-pre-released` → this cut
(6 commits). Packaging version string: `1.0.0` (git tag `v1.0.0` when published).

**Semver:** graduation from pre-release to non-pre `1.0.0` (public pack contract
intended as stable; Personal Pack still **0.2.1**). No `docs/specs/**` feature
triads in this monorepo — bullets below are product/process surface shipped in
the pack, not EARS IDs.

### Discovery / companions

- **`work-the-problem`** — multi-round problem-solving companion (identify → define
  → foundation→feature → breakdown↔solve, disk artifacts under
  `.skills/work-the-problem/<slug>/`, carry-back brief); user-invoked
  `/work-the-problem`. Siblings: `/interpret-session` (time-boxed stance),
  `/deepen-codebase` (pure learning). Author-skills RED/GREEN on grok-4.5
  (`tests/work-the-problem/`)
- **`solve-problem`** — evidence-grounded Problem Brief intake router before
  `root-cause` / `frame-change` when gap or workflow is unclear
- **`interpret-session`** — first-class **English** companion language (second-opinion
  / debate), not only L1 translation bridge

### Track / execution

- **`publish-issues`** — publish one feature issue; clarify ROAD vs CODE ownership
- Execute-family setup: require **polish-diff** and auto-vet via setup todos
  (`build-in-waves` / `build-by-story` / `build-inline` + write-flow-guide path)

### Packaging

- Register **`work-the-problem`** in Engineer Pack manifests (`plugin.json`,
  `marketplace.json`) — was on disk/guides before path list
- Engineer Pack skill path count: **60** (all paths validated present)
- Version bump **`1.0.0-pre-released` → `1.0.0`**

### Misc

- Guide inventory, discovery process companion table, troubleshooting user-invoked
  list, sibling pointers on interpret / deepen

### Verify (this cut)

- `docs/agents/project.md` **absent** — no configured typecheck/lint/unit/e2e
  pipeline; gate substituted with: skill frontmatter lint (exit 0), marketplace /
  plugin JSON parse, all skill paths exist (60 engineer + 19 personal)
- `docs/specs/` **absent** — audit-trace: nothing to check (clean)
- Decision records: `validate-records.sh --mode=trace` → 0 errors (3 warnings:
  W-opaque ×2, W-uncited-tag on pre-release baseline)
- Smoke: same structural checks on post-bump manifests

## 1.0.0-pre-released — 2026-08-05

First **1.0 pre-release** of Engineer Pack. Range: `v0.2.5` → `HEAD` (no prior
1.x tag; last cut-release tag was `v0.2.5`). Packaging version string:
`1.0.0-pre-released` (git tag `v1.0.0-pre-released`).

**Semver note:** pre-1.0 surface is large enough for a 1.0 line; this is still a
**pre-release** (installers and consumers should treat the contract as stabilizing,
not frozen).

### Highlights since `v0.2.5`

#### Discovery / learning

- **`deepen-codebase`** — subject-agnostic learning companion (dual-axis curriculum,
  foundation before delta, no product pick); replaces `thinking-practice`
- **`pathfind`** — multi-session Chart/Work decision map (Layer 0)
- **`interpret-session`** remains the stance + English-reply companion

#### Spec / execution spine

- **Docs-only spine (DOSP)** — `audit-trace` is docs-only; drop ID-in-test / trailer mandates
- **`load-subgraph` / FSUB** — neighbors schema 1.1, cluster, blast radius; `map-features`
- **Execute family** — `build-in-waves`, `build-by-story`, `build-inline` registered and
  documented; mid-build notes (IMPN); `.skills/<CODE>/` layout (SKNS)
- **`specify-behavior`** — thin system-docs consult for NFR grounding

#### Acceptance / review

- **write-flow-guide** run file v2 + serve/guide sync (DFSYNC) and coverage taxonomy
- **`run-flow-guide`** — agent-driven guide execution with FE+BE evidence
- **`vet-flow-guide`** — isolation judgment / missing-situation map before dogfood
- **`brief-team`**, **`study-change`**, decision-record (DREC) path at ship boundaries

#### Project / system docs

- **Hybrid 1A First-class system docs** — `define-system-doc` catalog (codebase,
  product, architecture, standards, security, ops)
- **`assess-pivot-impact`**, roadmap milestones assessments
- Skill renames to engineer-facing vocabulary (0.4.0-pre.0 lineage)

#### Packaging

- Engineer Pack marketplace entry version **`1.0.0-pre-released`**
- 58 engineer skills registered; all manifest paths validated present
- Personal Pack remains **0.2.1** (independent, opt-in)

### Misc

- Author-skills pressure evidence for `deepen-codebase` (RED/GREEN on grok-4.5)
- Guide inventory, START-HERE, discovery process, cross-links updated

### Verify (this cut)

- `docs/agents/project.md` **absent** — no configured typecheck/lint/unit/e2e release
  pipeline; gate substituted with: skill frontmatter lint (exit 0), marketplace/plugin
  JSON parse, all skill paths exist (58 + personal 19)
- `docs/specs/` **absent** — audit-trace: nothing to check (clean)
- Smoke: same structural checks on post-bump manifests

## 0.4.0-pre.2 — 2026-08-05

### Replace: `thinking-practice` → `deepen-codebase` (learning companion)

Retires the train→ship / anti-recommendation gym. New skill is a **subject-agnostic
learning companion**: dual-axis curriculum (Bloom kinds × foundation layers), slow
and deep, any codebase or technical topic — not a mode of interpret, not brainstorm
practice.

- **New skill** `skills/discovery/deepen-codebase/` (user-invoked `/deepen-codebase`)
  — Iron Laws: foundation before delta; no product pick; no "standard" without
  authority tier + source; no mastery claims; read-only
- **Curriculum** `references/curriculum.md` — subject adapter probes + authority
  ladder; worked sketches are examples only (memory session, payments, auth)
- **Optional packet** `foundation-note/v1` (knowledge only) replaces
  `thinking-handoff/v1`
- **Removed** `skills/discovery/thinking-practice/`
- **Packaging:** `plugin.json` + `marketplace.json` path swap
- **Docs:** guide page, discovery companions, inventory rows, interpret See also,
  configure-repo posture note

## 0.4.0-pre.1 — 2026-08-03

### New: `thinking-practice` — thinking gym without recommendation

*(Superseded by `deepen-codebase` in 0.4.0-pre.2.)*

Sibling of `interpret-session` for native-language **reasoning ownership**. Equips
territory, named unknowns, question scaffolds, and evidence calibration; never
encodes a preferred choice. Explicit train→ship only via neutral
`thinking-handoff/v1` to `interpret-session` (Path A checkpoint or Path B escape).

- **New skill** `skills/discovery/thinking-practice/` (user-invoked `/thinking-practice`)
  — Iron Laws: no recommendation anywhere; no invent-to-fill; no auto-ship from
  urgency; no learning-complete / ship-ready claims from single-session proxies
- **Packet** `thinking-handoff/v1` with field-level provenance
  (`references/thinking-handoff-v1.md`)
- **Pressure evidence** in `TESTS.md` (grok-4.5 RED/GREEN: demand-pick, after-loop,
  Path B ambiguous reject, Path A/B packet smoke)
- **Packaging:** Engineer Pack **0.4.0-pre.1** — `plugin.json` + `marketplace.json`
  list `./skills/discovery/thinking-practice`
- **Docs:** skill guide page, discovery inventory (README / START-HERE / process),
  configure-repo posture note, interpret-session See also

## 0.3.0 — 2026-07-31

### Feature: one write-flow-guide run file, plus an optional live guide (`DFSYNC`)

A write-flow-guide run used to be three files that did not know about each other — the
cases YAML, a rendered HTML snapshot of it, and a markdown ledger where the
verdicts actually lived. A person holding the guide could not see what the agent
had proven, and a person testing by hand had nowhere to put what they found.

**Breaking.** `.skills/<slug>-write-flow-guide.cases.yaml` and
`.skills/<slug>-write-flow-guide-run.md` are replaced by a single
`.skills/<slug>-flow-guide.json` (`version: 2`). There is no migration path and no
v1 reader: `.skills/` is git-ignored scratch, so delete the old files and
re-author. Passing a `.yaml`/`-run.md` path now gives a named error instead of a
confusing parse failure.

- **One artifact.** Cases and verdicts share a file. Every subcommand takes one
  path, so `mark --catalog` is gone — which also closes a hole where the
  presentational evidence rules were silently skipped whenever no catalog was
  reachable.
- **Human ticks are recorded, never authoritative.** Each case carries two
  field spaces that share no key name: `run` (the agent's verdict, `saw`,
  `server`) and `human` (`checked`, `at`, `comment`). Nothing promotes one into
  the other, `write-flow-guide next` ignores `human` entirely, and the HTTP surface
  rejects any attempt to write a verdict. See ADR 0006.
- **`flow-guide serve`** binds `127.0.0.1:8787` and serves a guide that follows the
  run and accepts the person's ticks. It is optional by construction: `render`
  bakes current verdicts into the HTML, so a guide opened by double-click is
  correct with nothing running, and says on the page that it is a render-time
  snapshot. ARCH-3 is why that ordering matters.
- **Shutdown proves identity.** `serve --stop` terminates a process only when
  `/whoami` returns the token in its pidfile, because `kill -0` cannot tell a
  live server from a recycled PID. See ADR 0007.
- **PyYAML dropped.** The CLI is standard-library only.
- **Concurrent writes.** All writes go through one store: an `O_EXCL` lockfile,
  a field-scoped patch, and `os.replace`.

Skill bodies, `references/cases-schema.md`, and the human guides are rewritten
for the run file; `run-flow-guide` now ends a run by asking whether to stop a
server it started.

Contract: `docs/specs/2026-07-30-write-flow-guide-sync/`.

## 0.2.7 — 2026-07-30

### Fix: register `build-by-story` and `build-inline` in the pack manifests

The execute-family split (`5d82820`) shipped both skills plus all docs and
routing, but never listed them in `.claude-plugin/plugin.json` /
`.claude-plugin/marketplace.json` — installers of `engineer-pack` got routing
instructions pointing at two skills they did not have.

- **Manifests** now list `skills/execution/build-inline` and
  `skills/execution/build-by-story` alongside `build-in-waves`
- No skill content changed; manifest coverage of on-disk engineer skills is
  now complete

## 0.2.6 — 2026-07-27

### New: `brief-team` — team-shared pitch+map

Post-implementation human projection for large / architecture-affecting changes.

- **New skill** `skills/review/brief-team/` (user-invoked `/brief-team`)
  — HTML packet under `docs/explainers/<slug>.html` + `INDEX.md` upsert; overwrite
  canonical; range required; optional enrich from specs/notes/clarify-decisions locks
- **No quiz, never a ship gate** — split from `/study-change` (self + quiz +
  outside repo); `land-branch` / `write-handoff` may **name** both optionally
- Spec **XPLN** (`docs/specs/2026-07-27-brief-team/`); scenarios in
  `tests/brief-team/scenarios.md`

## 0.2.5 — 2026-07-27

### New: `assess-pivot-impact` — pivot disposition ledger

Closes the gap where `define-project` (brownfield), `realign-spec`, and
`scan-architecture` all treat **code as truth**. When the user pivots intent
and shipped reality collides with the new vision, nothing previously owned that
flow.

- **New skill** `skills/project/assess-pivot-impact/` (user-invoked `/assess-pivot-impact`)
  — Iron Law: no vision/architecture rewrite until every contradicted shipped
  feature and live `ARCH-N` has a user-confirmed disposition in
  `docs/product/pivot-ledger.md`
- **Single-writer preserved:** skill never writes `vision.md` /
  `architecture/`; names `/define-project` (update) after confirmation
- **RED/GREEN** under `tests/assess-pivot-impact/` (Ledgerly fixture; Sonnet + Haiku)
  - S1 deadline pivot: baseline **failed** (both models rewrote vision) → skill
    **green** after REFACTOR (ledger-on-disk + named-repo counters for Haiku)
  - S2 challenge-pivot and S3 bare-delete: baseline **passed** → cut from skill
    text (no-op rule)
- **Neighbors:** `define-project` update routes pivots-with-collisions here;
  `reroute-plan` Vision re-entry names `/assess-pivot-impact` when shipped code
  collides

### Packaging

- Engineer Pack version **0.2.5**; plugin path list adds
  `./skills/project/assess-pivot-impact`

## 0.2.4 — 2026-07-27

### `write-flow-guide` / `run-flow-guide` — cases YAML + CLI ledger (no guide ticks for agents)

Stops agent progress living in HTML `localStorage` (Chrome ticks burned tokens)
and stops re-authoring full CSS per write-flow-guide pass.

- **Cases SSOT:** `.skills/<slug>-write-flow-guide.cases.yaml` with required slots
  (`id`, `req`, `kind`, `title`, `setup`, `try`, `expect`, `backend`)
- **Shell:** `skills/acceptance/write-flow-guide/shell/guide.html` — theme-aware, kind
  chips, human-only localStorage ticks
- **CLI:** `skills/acceptance/write-flow-guide/scripts/flow-guide` —
  `list` / `show` / `init` / `status` / `next` / `mark` / `render` / `report`
- **`write-flow-guide` skill:** write cases → `render`; `craft-page` opt-in only
- **`run-flow-guide` skill:** Iron Law adds *progress lives in the ledger*; browser
  only for the product under test; `mark` enforces `saw` + `server`
- **Contract:** `docs/specs/2026-07-27-write-flow-guide-cli/contract.md`
- **Tests:** `tests/test_dogfood_cli.py`; scenarios in
  `tests/run-flow-guide/scenarios-cli.md`

### Packaging

- Engineer Pack version **0.2.4** (skill/docs + scripts; plugin path list
  unchanged — scripts ship inside the write-flow-guide skill folder)

## 0.2.3 — 2026-07-26

### `write-flow-guide` coverage gate + case taxonomy

Stops happy-only guides from write-flow-guide: each ability area needs non-happy cases (edge /
error / nonbehavior / persist) or a greppable coverage exception.

- **Taxonomy** on every row: `data-kind` = `happy` \| `edge` \| `error` \|
  `nonbehavior` \| `persist` \| `visual` \| `journey`
- **Coverage rules** replace "≥1 case per requirement ID" as the sole bar
- **Self-check** before hand-off: count kinds per section
- **`run-flow-guide`**: ledger carries `kind`; no demo-only happy-path subset
- Guide + review-and-acceptance docs updated

### Packaging

- Engineer Pack version **0.2.3** (skill/docs only; plugin path list unchanged)

## 0.2.2 — 2026-07-26

### New: `run-flow-guide` + machine-drivable guides from write-flow-guide

Agent-driven execution of an existing write-flow-guide HTML guide in a real browser, with
paired front-end and backend evidence, a resumable run ledger, and a fix loop
through `root-cause`.

- **New skill** `skills/acceptance/run-flow-guide/` — model-invocable; outcome is
  an evidence-backed run ledger (pass / fail / blocked per case), not committed
  e2e specs (`validate-ui`) and not guide authoring (`write-flow-guide`)
- **`write-flow-guide` upgrade** — every case row carries `data-case`, `data-req`,
  `data-backend`, `data-setup`; guide always written to a known file path;
  descriptions disambiguate author vs drive
- **RED/GREEN** recorded under `tests/run-flow-guide/` (baselines on `grok-4.5`)
- **Inventory:** plugin + marketplace, guide page, AGENTS/README skill counts,
  See also links from acceptance neighbors

### Packaging

- Engineer Pack version **0.2.2**

## 0.2.1 — 2026-07-26

### Packaging: Engineer Pack + Personal Pack

`npx skills add jayden-dang/skills` now presents two clear packs instead of
"Jayden Skills" plus an ungrouped bucket:

| Pack | Plugin name | Contents |
|---|---|---|
| **Engineer Pack** | `engineer-pack` | All engineering skills (default plugin) |
| **Personal Pack** | `personal-pack` | All Personal OS skills (opt-in) |

- Renamed default plugin `jayden-skills` → `engineer-pack`
- Renamed personal plugin `personal-os` → `personal-pack`
- Added `.claude-plugin/marketplace.json` so the skills CLI groups both packs
- Moved three program-layer skills into Engineer Pack inventory (they were on
  disk under engineering categories but missing from `plugin.json`, so the CLI
  put them in **Other** / **General**):
  - `plan-milestones` (`skills/project/plan-milestones`)
  - `refresh-roadmap-status` (`skills/track/refresh-roadmap-status`)
  - `assess-milestone` (`skills/track/assess-milestone`)
- Docs: `docs/packages.md`, root README inventory, package READMEs

## 0.2.0 — 2026-07-26

### New: Personal OS package (independent, opt-in)

A standalone life and multi-project **management** skill set. Agent role is
secretary / coach — not product implementer. Does not depend on the engineering
package; not included in the default Claude engineering plugin.

- **18 skills** under `skills/personal/`: `using-personal-os`, `setup-personal-os`,
  `capture`, `process-inbox`, `orient`, `plan-day`, `execute-session`,
  `open-project`, `plan-project`, `close-project`, `maintain-area`,
  `open-learning-track`, `log-learning`, `review-week`, `review-quarter`,
  `replan`, `life-charter`, `sync-workspaces`
- **Templates** under `templates/personal-os/` (project, area, daily, weekly,
  quarterly, learning track, session, inbox, config example)
- **Docs:** package README, `docs/personal-os/START-HERE.md`, `docs/packages.md`
  (multi-package install isolation)
- **Optional plugin** manifest: `.claude-plugin/personal-os.plugin.json`
- **Secretary default / permission rules:** management only unless the user grants
  a scoped act; registry-first workspaces; config-mapped layouts (no forced rename)
- Default `.claude-plugin/plugin.json` remains **engineering-only**

### Docs / packaging

- Root README and AGENTS.md describe dual independent packages
- Engineering install docs avoid a blind `skills/*/*` loop that would pull Personal OS
- `skills/engineering/README.md` package index (paths unchanged)

### Misc

- Version bump to **0.2.0** (minor: new optional package surface)

## 0.1.1 — 2026-07-24

### New requirements shipped

#### Outbound study-change (XDIFF)

User-invoked `/study-change` builds one self-contained HTML comprehension
packet (Background → Intuition → Code → Quiz) for a resolved git range —
outbound self-check aid, never a ship gate.

- On-demand user-invoked skill with explicit triggers; no auto-run, soft-prompt, or ship-menu coupling — **XDIFF-1.1–1.6**
- D! range cascade with pure-untracked hard-stop, tracked-dirty + scope notice, truly-clean branch vs default base, empty hard-fail — **XDIFF-2.1–2.7**
- A+ untracked policy (exclude by default; flag/paths; untracked-only honest stop) — **XDIFF-3.1–3.5**
- Single offline HTML packet via checked-in shell template; optional craft-page craft only — **XDIFF-4.1–4.12**
- Fixed five-question interactive quiz; personal pass only; never omit for “trivial” — **XDIFF-5.1–5.9**
- Optional DREC read-only enrichment (forward-cite + explicit ids; no emit) — **XDIFF-6.1–6.10**
- Passive-data safety and HTML escape constraints — **XDIFF-7.1–7.3**
- Package, plugin inventory, guide, ARCH-3 pure skill path — **XDIFF-8.1–8.4**
- No partial success HTML; quiz a11y basics — **XDIFF-9.1–9.2**
- Neighbor isolation guards (DREC emitters, land-branch/release, inspect-change, digest term, ARCH-6) — **XDIFF-10.1–10.9**

#### Boundary Decision Records (DREC)

Immutable decision records at production boundaries (`land-branch` / `cut-release`)
with validator, record-before-crossing, and ARCH-6 participant model.

- Record substrate, identity/reissue, depth classification — **DREC-1.x–3.x**
- Verbatim human provenance and storage classes — **DREC-4.x–5.x**
- Emission rules for land-branch and cut-release — **DREC-6.x–7.x**
- Durable evidence, record-verdict skill, participant SSOT — **DREC-8.x–10.x**
- Audit Trace extension, validator, adoption anchor — **DREC-11.x**
- interpret-session ledger/labels/digest upgrades — **DREC-12.x**
- Spec-folder discovery convention; NFR secret scan / determinism — **DREC-13.x–14.x**
- Record-before-crossing ordering and publication failure — **DREC-15.x**

### Protected behavior

- Record-before-crossing and caller gate pressure hardening — **Guards: DREC-15.1, DREC-9.5, DREC-6.3**
- Doctrine SSOT / description trigger polish-diff — **Guards: DREC-9.1, DREC-9.4, DREC-15.1**

### Misc

- `realign-spec(DREC)`: mark triad Implemented; ARCH-6 design citation
- `fix(drec)`: move e-spine fixture IDs out of unittest source (audit-trace E1)
- `refactor(xdiff)`: author-skills checklist hardening (Iron Law, red flags, pointers)
- `docs(xdiff)`: pressure-test results; range decision-tree callout
