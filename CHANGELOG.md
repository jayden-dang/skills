# Changelog

## Unreleased

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
  (`build-in-waves` / `build-by-story` / `build-inline` + review-product-flow path)

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

- **review-product-flow** run file v2 + serve/guide sync (DFSYNC) and coverage taxonomy
- **`run-product-walkthrough`** — agent-driven guide execution with FE+BE evidence
- **`vet-product-flow`** — isolation judgment / missing-situation map before dogfood
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

### Feature: one review-product-flow run file, plus an optional live guide (`DFSYNC`)

A review-product-flow run used to be three files that did not know about each other — the
cases YAML, a rendered HTML snapshot of it, and a markdown ledger where the
verdicts actually lived. A person holding the guide could not see what the agent
had proven, and a person testing by hand had nowhere to put what they found.

**Breaking.** `.skills/<slug>-review-product-flow.cases.yaml` and
`.skills/<slug>-review-product-flow-run.md` are replaced by a single
`.skills/<slug>-review-product-flow.json` (`version: 2`). There is no migration path and no
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
  the other, `review-product-flow next` ignores `human` entirely, and the HTTP surface
  rejects any attempt to write a verdict. See ADR 0006.
- **`review-product-flow serve`** binds `127.0.0.1:8787` and serves a guide that follows the
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
for the run file; `run-product-walkthrough` now ends a run by asking whether to stop a
server it started.

Contract: `docs/specs/2026-07-30-review-product-flow-sync/`.

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

### `review-product-flow` / `run-product-walkthrough` — cases YAML + CLI ledger (no guide ticks for agents)

Stops agent progress living in HTML `localStorage` (Chrome ticks burned tokens)
and stops re-authoring full CSS per review-product-flow pass.

- **Cases SSOT:** `.skills/<slug>-review-product-flow.cases.yaml` with required slots
  (`id`, `req`, `kind`, `title`, `setup`, `try`, `expect`, `backend`)
- **Shell:** `skills/acceptance/review-product-flow/shell/guide.html` — theme-aware, kind
  chips, human-only localStorage ticks
- **CLI:** `skills/acceptance/review-product-flow/scripts/review-product-flow` —
  `list` / `show` / `init` / `status` / `next` / `mark` / `render` / `report`
- **`review-product-flow` skill:** write cases → `render`; `craft-page` opt-in only
- **`run-product-walkthrough` skill:** Iron Law adds *progress lives in the ledger*; browser
  only for the product under test; `mark` enforces `saw` + `server`
- **Contract:** `docs/specs/2026-07-27-review-product-flow-cli/contract.md`
- **Tests:** `tests/test_dogfood_cli.py`; scenarios in
  `tests/run-product-walkthrough/scenarios-cli.md`

### Packaging

- Engineer Pack version **0.2.4** (skill/docs + scripts; plugin path list
  unchanged — scripts ship inside the review-product-flow skill folder)

## 0.2.3 — 2026-07-26

### `review-product-flow` coverage gate + case taxonomy

Stops happy-only review-product-flow guides: each ability area needs non-happy cases (edge /
error / nonbehavior / persist) or a greppable coverage exception.

- **Taxonomy** on every row: `data-kind` = `happy` \| `edge` \| `error` \|
  `nonbehavior` \| `persist` \| `visual` \| `journey`
- **Coverage rules** replace "≥1 case per requirement ID" as the sole bar
- **Self-check** before hand-off: count kinds per section
- **`run-product-walkthrough`**: ledger carries `kind`; no demo-only happy-path subset
- Guide + review-and-acceptance docs updated

### Packaging

- Engineer Pack version **0.2.3** (skill/docs only; plugin path list unchanged)

## 0.2.2 — 2026-07-26

### New: `run-product-walkthrough` + machine-drivable review-product-flow guides

Agent-driven execution of an existing review-product-flow HTML guide in a real browser, with
paired front-end and backend evidence, a resumable run ledger, and a fix loop
through `root-cause`.

- **New skill** `skills/acceptance/run-product-walkthrough/` — model-invocable; outcome is
  an evidence-backed run ledger (pass / fail / blocked per case), not committed
  e2e specs (`validate-ui`) and not guide authoring (`review-product-flow`)
- **`review-product-flow` upgrade** — every case row carries `data-case`, `data-req`,
  `data-backend`, `data-setup`; guide always written to a known file path;
  descriptions disambiguate author vs drive
- **RED/GREEN** recorded under `tests/run-product-walkthrough/` (baselines on `grok-4.5`)
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
