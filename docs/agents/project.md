# Project configuration (agent-facing)

Written by `setup-repo`. Skills read this file for repo-specific **machine config** —
commands, globs, paths — plus **posture** and **team** (below). Human-facing engineering
guidelines (coding standards, naming, house rules) live in `docs/product/guidelines.md`
when the project-docs layer is enabled; `write-plan` sources them from there and falls
back to this file otherwise.

## Project posture

The project's standing intent and lifecycle phase. Skills read this instead of re-asking:
`brainstorm` and `grilling` right-size how much they weigh data migration, backward
compatibility, and deprecation against it; `interpret` reuses it as session context.
Edit these two lines directly whenever the project moves phase — no wizard needed.

- **Delivery intent:** `Production` — how robust and complete the output must be.
- **Lifecycle stage:** `Active development` — where the project is in its life.

These are distinct from the product **Goals** in `docs/product/vision.md` (what success
looks like): posture is *how carefully to build right now*, not *what to build*.

## Team

Who works on this repo and how skills should package collaboration.
Skills that plan, review, or hand off read this section when present and
right-size **packaging** only (Solo / Small / Multi) — Iron Law gates never
change. Edit freely; re-run `/setup-repo` to re-draft from git/CODEOWNERS.
If this section is absent, skills do not invent a team.

**SSOT:** **band** derivation and the **packaging** matrix live only here.
Consumers **read** this section; they do not re-copy these rules into skill bodies.

### Roster

- Contributor — Jayden Đặng

Suggested roles (freeform allowed): Tech Lead, Backend Engineer, Frontend Engineer, Full-stack Engineer, Designer, Product Manager, QA, DevOps/SRE, Docs.

### Ownership notes (optional)

*(none)*

### Workflow band

- **Override (optional):** *(blank — derive)*
- **Derive (when override blank):**
  1. Headcount from **Roster only**: each `Role — Name` = 1; each `N × Role` / `N Role(s)` adds N.
     Ignore Ownership notes and placeholders (`<…>`).
  2. Buckets: empty roster → **no band** (same packaging as Team absent); 1 → **Solo**;
     2–4 → **Small**; ≥5 → **Multi**.
  3. Specialty upgrade only: if **Small** and ≥3 distinct role titles (case-insensitive, trimmed),
     upgrade to **Multi**. Never downgrade Multi→Small.

*(Derived: Solo — headcount 1)*

### Packaging matrix

| Band | Packaging |
|---|---|
| **Solo** | Lean multi-person ritual language; no invented peer reviewers/assignees; agent-as-pair; full gates |
| **Small** | Design-review checkpoints; ownership boundaries via optional freeform notes; name people when roster has names |
| **Multi** | CODEOWNERS-aware review language when ownership notes exist; explicit review responsibilities as prose; handoff/docs emphasis |
| **(no band)** | Team absent, or empty roster with blank override — pre-feature default; do not invent a team; do not hard-fail |

## Decision boundaries

Optional. When present, `record-decision` reads this table. Pins may raise a
floor or bind an action to a boundary type. An entry that would lower a core
floor is ignored with a one-line notice. Absent section → core table only.

| Action | Boundary-Type | Floor |
|---|---|---|
| *(none pinned — core table only)* | | |

## Verify commands

Run in this order; all must pass before any completion claim.

| Check | Command |
|---|---|
| Typecheck | *(none)* |
| Lint | `python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-handoffs.py && python3 scripts/lint-context7.py` |
| Unit tests | `python3 -m unittest discover -s tests` |
| E2E / smoke | *(none)* |

Single test file: `python3 -m unittest tests.<module>`  
(e.g. `python3 -m unittest tests.test_lint_handoffs`)

The traceability check is not a command here — the `trace` skill runs it as
`grep`/`git` over `docs/specs/` and the test globs. If this repo's tests live
outside the default globs (`tests test e2e src src-tauri crates app lib packages`),
record the real locations below so `trace` searches the right paths.

Test globs: *(defaults — `tests` covers this repo)*
Trace ignore (files whose IDs are fixtures, not coverage): `tests/team-structure/red-baselines.md`, `tests/decision-records/red-baselines.md`, `tests/decision-records/fixtures/`, `tests/comprehend-change/red-baselines.md`

## Test annotation conventions

| Layer | Requirement-ID convention |
|---|---|
| Unit (`unittest` under `tests/`) | Requirement ID in the test method name (e.g. `test_TEAM_1_2_…`) or first-line docstring as greppable `CODE-N.M` |
| Scenario / acceptance markdown | Greppable bare `CODE-N.M` tokens in the scenario file (e.g. `tests/team-structure/scenarios.md`) |

## Run locally (dev)

How to start the app for user-facing acceptance checks (read by `acceptance-api`
and `acceptance-ui`). Fill in once the app can be run locally; leave a row blank
if that surface does not exist.

| Surface | Start command | Ready signal |
|---|---|---|
| Backend / API | *(none — not an app)* | |
| Frontend | *(none — not an app)* | |

Browser E2E (Playwright, Chromium): *(none)*

## Release steps

*(empty — pure SKILL.md + plugin manifest; no build artifact)*

Smoke-check: `python3 -m unittest discover -s tests`

Version file: `.claude-plugin/plugin.json` (`version` field)

## Paths

- Specs: `docs/specs/`
- ADRs: `docs/adr/`
- Glossary: `CONTEXT.md`
- Out-of-scope KB: `.out-of-scope/`
- Engineering guidelines (project-docs layer, optional): `docs/product/guidelines.md`
- Product vision / architecture spine (project-docs layer, optional): `docs/product/vision.md`, `docs/architecture/`
