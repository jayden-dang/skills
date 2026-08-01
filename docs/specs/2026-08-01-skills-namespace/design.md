# Design: Skills ephemera namespace

Feature code: SKNS
Status: Approved
Date: 2026-08-01
Requirements: ./requirements.md

## Context

Today feature ephemera lives mostly at the bare `.skills/` root: `progress.md`,
`task-N-brief.md` / `task-N-report.md`, `review-<base>..<head>.diff`,
`implementation-notes.md`, plus many `<slug>-*` digests. Consumer repos that run
this skill set hard (mailgate ~95 root entries, bot ~166) show the failure mode:
one progress file (or ad-hoc `progress-pnot.md`), review diffs stacked by SHA
only, and implementation-notes mixing features. Parallel worktrees and concurrent
features collide on names and ledgers.

Some roots are already namespaced correctly and must stay: `.skills/pathfind/`,
`.skills/research/`, `.skills/decisions/`, `.skills/pr-packages/<stable-id>/`.
Discovery already uses optional `.skills/<slug>-knowns.md` / `-scan.md` — that
slug pattern becomes a directory prefix under Feature code (or `_pending-` /
`_adhoc-`) rather than a root file.

**Binding constraint:** ARCH-3 — no Python runtime or vendored path library in
the consumer repo. Path rules live as **prose contract** in skill bodies (and a
single shared reference markdown agents follow), verified by source-contract /
scenario tests in *this* skill-set repo only — same pattern as FSUB
`passes.md` + tests, not a runtime under `skills/`.

**Rejected alternative:** a materialised registry file listing CODE → path maps,
or auto-migrating consumer trees. That reintroduces staleness and violates
SKNS-4.3.

## Decisions

1. **Directory key = Feature code only** — e.g. `.skills/SPAY/`. No long slug in
   the path segment (SKNS-1.2).
2. **Canonical feature root** — `.skills/<CODE>/` for all feature-scoped ephemera
   listed in SKNS-1.1.
3. **Progress** — `.skills/<CODE>/progress.md` only; never a global multi-feature
   ledger (SKNS-1.4, SKNS-7.1).
4. **Shared roots unchanged** — pathfind, research, decisions, pr-packages
   (SKNS-2.x). Optional `Feature-code:` on PR package manifest only.
5. **Pre-CODE** — `.skills/_pending-<slug>/`; promote to `.skills/<CODE>/` on
   INDEX registration (SKNS-3.1–3.2).
6. **Ad-hoc** — `.skills/_adhoc/<short-slug>/` when no Feature code path applies
   (SKNS-3.3).
7. **Legacy** — read allowed once for resume; write only under CODE (SKNS-4.1–4.2);
   no auto-migrate (SKNS-4.3).
8. **SSOT for path grammar** — one reference file agents and authors open:
   `skills/execution/load-subgraph` style: e.g.
   `skills/meta/gate-session` is wrong home; put under a neutral path:
   **`docs/agents/` is consumer config** — so skill-set SSOT lives at
   `skills/execution/build-in-waves/references/skills-ephemera-paths.md`
   *or* better a shared place every category can cite:
   **`templates/skills-ephemera-paths.md`** (shipped with the pack; skills
   `REQUIRED` load via relative pointer / prose name "skills ephemera paths").
   Final choice: **`skills/meta/gate-session` no** —
   **`docs/guide` no (not agent contract)** —
   **Ship as `skills/execution/build-in-waves/references/…` is too narrow.**

   **Locked path for SSOT:**
   `skills/setup/configure-repo` is run-once.
   Use **`templates/skills-ephemera-paths.md`** copied nowhere — skills resolve
   pack root and read `templates/skills-ephemera-paths.md` the same way they
   resolve `templates/requirements.md`. Single grammar table: CODE / pending /
   adhoc / shared / basename list / resolve order / legacy read rule.

9. **CODE resolve order** (SKNS-1.3): (1) active plan/brief/session feature
   context, (2) feature `requirements.md` `Feature code:` line, (3) INDEX row
   for the active spec dir. Controller injects `CODE` into every task brief
   header so implementers never invent a path.

10. **No new user-invoked skill** — model skills update in place (ARCH-5
    composition unchanged).

## Architecture

### 1. Path grammar SSOT (`templates/skills-ephemera-paths.md`)

Satisfies: SKNS-1.1, SKNS-1.2, SKNS-1.3, SKNS-2.1, SKNS-2.2, SKNS-2.3, SKNS-2.4, SKNS-3.1, SKNS-3.2, SKNS-3.3, SKNS-4.1, SKNS-4.2
Reuse: rung 2 — same "templates + skill prose" pattern as triad seeds; no new runtime
Respects: ARCH-3, ARCH-1 (tests assert path strings via grep, not LLM judgment of "good layout")
Interface: Agents and skills know only: root forms, basename list, resolve order, legacy read/write rule
Depth: If deleted, skills fall back to contradictory hard-coded paths — one table must exist; callers only need the path forms, not migration history
Locality: create `templates/skills-ephemera-paths.md`; leave consumer apps; extend every skill body that cites flat paths

**Grammar (normative summary; full table in the template file):**

| Kind | Root | Examples |
|---|---|---|
| Feature | `.skills/<CODE>/` | `progress.md`, `task-N-brief.md`, `task-N-report.md`, `review-<base7>..<head7>.diff`, `implementation-notes.md`, `global-constraints.md`, `knowns.md`, `scan.md`, `req-review.md`, `design-review.md`, `plan-review.md`, `acceptance.md`, `<slug>-review-product-flow.json` (basename may keep slug suffix under CODE dir) |
| Pending | `.skills/_pending-<slug>/` | same basenames before CODE exists |
| Adhoc | `.skills/_adhoc/<short-slug>/` | tier-0 / one-off |
| Shared | `.skills/pathfind/`, `.skills/research/`, `.skills/decisions/`, `.skills/pr-packages/` | unchanged |

**Resolve CODE:** brief/plan context → `Feature code:` → INDEX.

**Legacy:** IF `.skills/<CODE>/` missing AND legacy root has clear single-feature state → read once; all writes go to `.skills/<CODE>/` (create dir). NEVER write new progress/task/review/notes/knowns/scan/acceptance loose at bare `.skills/`.

**Promote pending:** On INDEX registration of CODE, if `_pending-<slug>/` was used for this work: `mv` or rewrite so subsequent writes use `.skills/<CODE>/`. Prefer `mv .skills/_pending-<slug> .skills/<CODE>` when CODE dir absent.

### 2. Execute family path rewrite

Satisfies: SKNS-1.4, SKNS-5.1, SKNS-6.2, SKNS-7.1
Reuse: rung 2 — extend build-in-waves / build-by-story / build-inline / implementer-prompt / task-reviewer-prompt
Respects: ARCH-3
Interface: Controller sets `FEATURE_CODE=<CODE>`; all ledger and handoff paths are `.skills/<CODE>/…`
Depth: n/a — extends execute family
Locality: extend those skill packages; leave isolate-workspace (worktree root still has its own `.skills/`)

| Old | New |
|---|---|
| `.skills/progress.md` | `.skills/<CODE>/progress.md` |
| `.skills/task-N-brief.md` | `.skills/<CODE>/task-N-brief.md` |
| `.skills/task-N-report.md` | `.skills/<CODE>/task-N-report.md` |
| `.skills/review-<b>..<h>.diff` | `.skills/<CODE>/review-<b>..<h>.diff` |
| `.skills/implementation-notes.md` | `.skills/<CODE>/implementation-notes.md` |
| (optional) global constraints copy | `.skills/<CODE>/global-constraints.md` |

Ledger line format unchanged (`Task N: complete (commits …)`). Preflight: create
`.skills/<CODE>/` if missing. Resume: read only that feature's ledger.

### 3. Discovery / spec path rewrite

Satisfies: SKNS-3.1, SKNS-3.2, SKNS-5.2
Reuse: rung 2 — extend frame-change, design-solution, specify-behavior, plan-tasks, clarify-decisions (load parent knowns)
Respects: ARCH-2 (pending/adhoc no-op inventing CODE)
Interface: Writers use pending root until CODE exists; then CODE root
Depth: n/a — extends discovery/spec
Locality: extend skill bodies; leave pathfind shared root (SKNS-2.1)

| Artifact | Before CODE | After CODE |
|---|---|---|
| scan digest | `_pending-<slug>/scan.md` | `<CODE>/scan.md` |
| knowns | `_pending-<slug>/knowns.md` | `<CODE>/knowns.md` |
| req / design / plan review | under pending or CODE | `<CODE>/*-review.md` or fixed basenames `req-review.md`, etc. |

Prefer **fixed basenames** under CODE (`knowns.md`, `scan.md`, `req-review.md`,
`design-review.md`, `plan-review.md`) to kill root slug sprawl. Accept legacy
read of `.skills/<old-slug>-scan.md` only under SKNS-4.1 when migrating mid-flight.

`specify-behavior` Step 1 (register CODE): after INDEX row, promote pending dir
(SKNS-3.2) — one explicit step in skill body.

### 4. Acceptance / product-flow path rewrite

Satisfies: SKNS-5.3
Reuse: rung 2 — extend validate-feature, review-product-flow, vet-product-flow, run-product-walkthrough
Interface: Run files live under `.skills/<CODE>/` with stable basenames
Depth: n/a — extends acceptance
Locality: extend acceptance skills + their reference schemas that hardcode `.skills/<slug>-…`

| Old pattern | New |
|---|---|
| `.skills/<slug>-acceptance.md` | `.skills/<CODE>/acceptance.md` |
| `.skills/<slug>-review-product-flow.json` | `.skills/<CODE>/review-product-flow.json` (same for `.html`, report, vet md) |
| walkthrough override → `.skills/progress.md` | `.skills/<CODE>/progress.md` |

CLI examples in references update to `$SKILLS_FEAT=.skills/<CODE>` style.

### 5. Ship / track path rewrite

Satisfies: SKNS-5.1, SKNS-2.4, SKNS-6.1
Reuse: rung 2 — package-change, land-branch, brief-team, write-handoff, reroute-plan, refresh-roadmap-status
Interface: Notes/progress under CODE; pr-packages/decisions unchanged
Depth: n/a — extends ship/track
Locality: extend path strings only; leave package-contract stable-id tree

- `implementation-notes` → `.skills/<CODE>/implementation-notes.md`
- `reroute-plan` corrections: **feature-scoped** → `.skills/<CODE>/corrections.md` (was root `.skills/corrections.md`; aligns with per-feature plan flight)
- `refresh-roadmap-status` advisory progress: scan `.skills/*/progress.md` or named CODE if known — **not** only root `progress.md`
- Optional: package manifest `Feature-code: <CODE>` when known (SKNS-2.4)

### 6. Constitution and human docs

Satisfies: SKNS-5.4, SKNS-6.3, SKNS-6.4
Reuse: rung 2 — AGENTS.md §8/§6, docs/guide/concepts/artifacts.md, process/execution, examples, troubleshooting, architecture/artifacts.md
Respects: ARCH-6 (skill-mediated paths only)
Interface: Humans and agents see one layout diagram
Depth: n/a — docs
Locality: extend docs; leave Personal OS docs

Also: `configure-repo` / gitignore already ignore `.skills/` — CONTINUE (SKNS-6.3).
audit-trace / load-subgraph: **no path logic change** (SKNS-6.4) — only ensure
docs do not claim flat progress is required.

### 7. Verification (this repo)

Satisfies: SKNS-4.3, SKNS-5.1–5.4, SKNS-7.1 (verification method)
Reuse: rung 2 — unittest source contracts like FSUB / PCHG
Interface: Tests grep skill bodies for forbidden bare paths and required CODE forms
Depth: n/a — test-side only under `tests/skills-namespace/`
Locality: new tests; leave consumer repos alone (SKNS-4.3)

**Forbidden** (must not appear as the *prescribed* path in skill bodies after ship):

- bare `` `.skills/progress.md` `` as the execute ledger (except legacy-read prose)
- bare `` `.skills/task-N-brief.md` `` / `task-N-report.md` / `implementation-notes.md` as write targets
- bare `` `.skills/review-` `` write targets without `<CODE>/`

**Required:** mention of `.skills/<CODE>/` (or equivalent token) in execute family SKILL.md files.

Scenario pressure (markdown, optional RED/GREEN author-skills style): two CODEs → two progress paths; write never to root for feature ephemera.

## Seams for testing

| Seam | Kind | Covers |
|---|---|---|
| Source contract: `templates/skills-ephemera-paths.md` exists + tables CODE/pending/adhoc/shared | unit | SKNS-1.1, 1.2, 2.1–2.4, 3.1, 3.3 |
| Source contract: execute family SKILL/prompts cite `.skills/<CODE>/` for progress/brief/report/review/notes | unit | SKNS-1.4, 5.1, 6.2, 7.1 |
| Source contract: discovery/spec/acceptance cite CODE or pending roots for feature digests | unit | SKNS-3.1–3.2, 5.2, 5.3 |
| Source contract: AGENTS.md + guide artifacts describe per-CODE layout | unit | SKNS-5.4 |
| Source contract: no auto-migrate mandate in skill bodies | unit | SKNS-4.3 |
| Source contract: pathfind/research/decisions/pr-packages still prescribed as shared | unit | SKNS-2.x, 6.1, 6.4 |
| Scenario pressure: dual-CODE ledger isolation (prose scenario + assert path forms) | scenario | SKNS-7.1, 1.4 |
| Scenario pressure: legacy read / write-only CODE | scenario | SKNS-4.1, 4.2 |
| specify-behavior registration promotes pending (skill body step present) | unit | SKNS-3.2 |
| gitignore / `.skills/` ignore rule unchanged language | unit | SKNS-6.3 |

No runtime e2e against mailgate/bot trees.

## Coverage check

| ID | Satisfies section |
|---|---|
| SKNS-1.1, 1.2, 1.3 | §1 Path grammar |
| SKNS-1.4 | §2 Execute |
| SKNS-2.1–2.4 | §1 Shared table + §5 pr-packages |
| SKNS-3.1–3.3 | §1 + §3 Discovery |
| SKNS-4.1–4.3 | §1 Legacy + §7 Verification |
| SKNS-5.1 | §2 Execute |
| SKNS-5.2 | §3 Discovery/spec |
| SKNS-5.3 | §4 Acceptance |
| SKNS-5.4 | §6 Docs |
| SKNS-6.1 | §5 Ship/track + §1 shared |
| SKNS-6.2 | §2 Execute |
| SKNS-6.3 | §6 Docs |
| SKNS-6.4 | §6 + §7 (no audit/FSUB change) |
| SKNS-7.1 | §2 + §7 seams |

All IDs mapped once. No placeholders.
