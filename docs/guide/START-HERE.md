# Start here

How the skill set works end to end: the A–Z workflow, the steps to use it in a new
repo, and what every skill does. For the architecture behind it, see
`docs/architecture/INDEX.md`; for one page per skill, see
[the skill reference](skills/README.md).

The whole set is script-free for consumers. A consuming repo installs nothing
executable beyond the optional session-start hook — traceability is the
[`audit-trace`](skills/audit-trace.md) skill (deterministic `grep`/`git` passes),
and feature overlap is **ask-time derivation** via
[`load-subgraph`](skills/load-subgraph.md) over live `docs/specs/` (neighbors
schema 1.1, **`cluster(focus)`**, no generated graph file).

**Human tutorial (setup + feature loop + variants):** this page.  
**Agent constitution (laws, 1% rule, DoD):** [`AGENTS.md`](../../AGENTS.md).

## 1. The A–Z workflow

```
                        gate-session  ── session gate: 1% rule before every response
                             │
        ┌────────────────────┴─────────────────────────────────────────────┐
        ▼                                                                    │
  /ask-me-bro  ── "I'm lost" ── routes to an entry point below               │
  /forge-prompt ── "my ask is vague" ── hands back one prompt to paste       │
        │                                                                    │
 SETUP (once)                                                                 │
  /bootstrap-repo (greenfield)  or  /configure-repo (existing code)           │
  optional: /define-project · plan-milestones · /map-features (brownfield)    │
        │                                                                    │
 IDEATION → SPEC                          BUILD                    SHIP
 ─────────────────                        ─────                    ────
 frame-change ─► specify-behavior ─► design-solution ─► plan-tasks
 [GATE: no code]  (EARS + IDs)     (Satisfies:)      (_Requirements:_ + audit-trace)
 + load-subgraph (neighbors 1.1)   + fresh load-subgraph   + blast_radius + cluster
        │                                                 │
        │ tier 0/1 shortcuts     isolate-workspace ─► build-in-waves | build-by-story | build-inline
        ▼                                                 │
  root-cause / debug-remote / assess-observability / test-first / prove-claim / audit-trace │
  (+ load-subgraph after Phase 2 only)                    ▼
         inspect-change ─► [polish-diff if predicate] ─► validate-feature
         (+ load-subgraph)     [product-walk if predicate]   (api/ui)
                    ─► land-branch ─► /cut-release ─► realign-spec

 MAINTENANCE: amend-feature · /publish-issues · /triage · /scan-architecture
              · /map-features · /tour-system · /pathfind · /write-handoff · realign-spec
```

**Ceremony tiers** decide how much of the chain you run (see
[ceremony tiers](methodology/ceremony-tiers.md)):

- **Tier 0 (trivial):** `test-first` + `prove-claim` only — no specs.
- **Tier 1 (bugfix):** `root-cause` (or `debug-remote` then `root-cause` if the failure is on a deployed env) → a mini-spec (fix requirement + a `SHALL CONTINUE TO`
  guard) → tagged regression test → `prove-claim` → `inspect-change` → `land-branch`.
- **Tier 2 (feature):** the full triad + execute family (`build-in-waves` /
  `build-by-story` / `build-inline`).

**Optional project layer** (large projects, off by default): before feature work,
`/define-project` writes a repo-level product vision and an IDed
architecture-invariant spine (`docs/architecture/`, each rule an `**ARCH-N**`). The
discovery, spec, execution, and review skills consult it when present — a `design.md`
cites `Respects: ARCH-N`, and `audit-trace` checks those citations — and ignore it cleanly when
absent. See [the artifact model](concepts/artifacts.md#docsproduct-and-docsarchitecture--the-optional-project-layer).

**The gates** — hard prohibitions written to survive an agent under pressure (see
[the gates](concepts/gates.md)):

| Gate | Iron law |
|---|---|
| `frame-change` | No code, scaffold nothing, until the tier is stated out loud |
| `test-first` | No production code without a failing test first |
| `root-cause` | No fixes without root-cause investigation first |
| `debug-remote` | Deployed-env failure: read-only evidence pack, then `root-cause` |
| `assess-observability` | Readiness finding set for tracing/OTLP/sampling |
| `prove-claim` | No completion claims without fresh verification evidence |

## 2. Using it in a new repo — step by step

**Mental model:** you drive with **slash commands** (`/…`) and plain-English
requests; most skills are **model-invoked** and fire when their trigger matches.
The session gate ([`gate-session`](skills/gate-session.md)), re-injected by the
session-start hook after `/clear` and compaction, keeps the 1% rule alive.
Full skill index: [Skill reference](skills/README.md) · laws: [`AGENTS.md`](../../AGENTS.md).

### One-time setup

1. **Install** — Claude Code / Grok: `/plugin marketplace add jayden-dang/skills`
   then `/plugin install jdk@jayden-dang-skills` (slash prefix `/jdk:`). Codex,
   Cursor, Kimi: `npx skills@latest add jayden-dang/skills --copy` (bare skill
   names). Do not flatten Engineer Pack onto Claude/Grok if the plugin is
   installed. Nothing is installed *into* your app repo beyond optional markdown + hook.
2. **Wire the repo**
   - **Greenfield / empty:** **`/bootstrap-repo`** → stack + harness + one green test → then configure.
   - **Existing codebase:** **`/configure-repo` only** (do not bootstrap).
3. **`/configure-repo`** — tracker, labels, verify commands, release steps, team,
   posture, optional Remote environments; writes `docs/agents/*.md`, seeds
   `docs/specs/INDEX.md` / glossary as needed, `## Agent skills` in
   `AGENTS.md`/`CLAUDE.md`; offers session-start hook.
   Proves commands are *wired* (content failures on an old repo are listed, not
   blocking). Installs **no** consumer linters/CI by default.
4. **Optional**
   - **`/define-project`** — vision + `ARCH-N` spine + guidelines (large projects).
   - **`plan-milestones`** — `docs/roadmap/INDEX.md` (`MILE-N` / `ROAD-N`).
   - **`/map-features`** — catalog ops: dispose OBS/OWNS gaps; with
     `Catalog sync: index-only`, also **export** (triad→INDEX) / **materialize**
     (INDEX→Draft local stubs). Brownfield: Feature code, ROAD binds, OWNS gaps,
     DEPENDS_ON *candidates* (propose → confirm only).

### Building a feature (tier 2)

You mostly describe the idea and **approve files**; the rest chains:

1. Describe the idea → **`frame-change`** (HARD GATE: no code). Explores context,
   runs **`load-subgraph`** (terms + paths → neighbors schema 1.1 + OWNS coverage),
   interviews you (`clarify-decisions` reuses the package when valid, else rederives),
   states the **tier**, hands off only when ready.
2. **`specify-behavior`** → `requirements.md` (EARS + `CODE-N.M`) → **you approve**.
3. **`design-solution`** → fresh **`load-subgraph`** at Step 1, then `design.md`
   (`Satisfies:`) → **you approve**.
4. **`plan-tasks`** → after the file map, **`load-subgraph`** once for
   `blast_radius` **and** `cluster(feature CODE)`; then task bodies;
   **`audit-trace`** coverage check; **you approve** and pick execute route.
5. **`isolate-workspace`** (recommended) unless you explicitly consent to main.
6. **Execute family** (exactly one):
   - **`build-in-waves`** — continuous subagent waves
   - **`build-by-story`** — human-gated story units
   - **`build-inline`** — controller implements with `test-first` (no implementers)
7. Per task: **`test-first`** · **`prove-claim`** (and **`audit-trace`** when claiming
   requirements met).
8. **`inspect-change`** — Standards + Spec; neighbors again via **`load-subgraph`**.
9. **Close sequence** (one home: `skills/execution/execute-common/SKILL.md`):
   **`polish-diff`** only when a polish predicate holds; **`validate-feature`**
   (`validate-api` / `validate-ui`); product-walk only when a walk predicate holds.
10. **`land-branch`** — validate close evidence, commit residue, then perform the resolved merge / PR / keep / discard / block action
    (agent-authored PR title and body are reviewer truth).
11. **`/cut-release`** when shipping a version.
12. **`realign-spec`** — triad + INDEX status (Implemented / Shipped).

### Other entry points

The table lives in [on-ramps](process/on-ramps.md) — one home. Unsure → **`/ask-me-bro`**.

## 3. Skill index (engineering package)

Full tables: [Skill reference](skills/README.md) (69 engineering skills).  
Personal OS is a **separate** package — [personal-os START-HERE](../personal-os/START-HERE.md).

`U` = you run `/name` · `m` = model-invoked · `si` = session-injected

| Category | Skills (see also [AGENTS.md §11](../../AGENTS.md#11-quick-reference-every-skill)) |
|---|---|
| **meta** | `gate-session` (m, si), `/ask-me-bro`, `/author-skills`, `/teach-pack` |
| **setup** | `/configure-repo`, `/bootstrap-repo` |
| **discovery** | `frame-change`, `clarify-decisions`, `research`, `run-spike`, `define-domain`, `/forge-prompt`, `/pathfind`, `/interpret-session`, `/deepen-codebase`, `/tour-system`, `/work-the-problem` |
| **spec** | `specify-behavior`, `design-solution`, `plan-tasks` |
| **execution** | `build-in-waves`, `build-by-story`, `build-inline`, `execute-common`, `test-first`, `root-cause`, `debug-remote`, `assess-observability`, `prove-claim`, `audit-trace`, **`load-subgraph`**, **`reconcile-features`**, `isolate-workspace`, `hold-stage` |
| **review** | `inspect-change`, `polish-diff`, `vet-feedback`, `vet-source`, `speak-outer`, `inspect-invariants`, `/study-change`, `/brief-team`, `/select-sample` |
| **acceptance** | `validate-feature`, `validate-api`, `validate-ui`, `write-flow-guide`, `vet-flow-guide`, `run-flow-guide` |
| **craft** | `craft-page` |
| **ship** | `land-branch`, `record-verdict`, `/cut-release` |
| **track** | `amend-feature`, `reroute-plan`, `realign-spec`, `/triage`, `/publish-issues`, `/scan-architecture`, **`/map-features`**, `/write-handoff`, `/refresh-roadmap-status`, `/assess-milestone` |
| **project** | `/define-project`, `/assess-pivot-impact`, `plan-milestones` |

## Where to go next

- [`AGENTS.md`](../../AGENTS.md) — agent constitution (Iron Laws, 1% rule, DoD)
- [Methodology overview](methodology/overview.md)
- [Feature overlap / load-subgraph](concepts/feature-graph.md) — neighbors 1.1, cluster, callers
- [Traceability](concepts/traceability.md)
- [Process by phase](process/README.md)
- [Examples](examples/tier-2-feature.md)
- `docs/architecture/INDEX.md`
