# Project configuration (agent-facing)

Written by `configure-repo`. Skills read this file for repo-specific **machine config** —
commands, globs, paths — plus **posture** and **team** (below). Human-facing engineering
guidelines (coding standards, naming, house rules) live in `docs/product/guidelines.md`
when the project-docs layer is enabled; `plan-tasks` sources them from there and falls
back to this file otherwise.

## Project posture

The project's standing intent and lifecycle phase. Skills read this instead of re-asking:
`frame-change` and `clarify-decisions` right-size how much they weigh data migration, backward
compatibility, and deprecation against it; `interpret-session` reuses it as session context.
Edit these two lines directly whenever the project moves phase — no wizard needed.

- **Delivery intent:** `Production` — how robust and complete the output must be.
- **Lifecycle stage:** `Active development` — where the project is in its life.
- **Default PR base:** `main` — the branch `package-change` reads as the third rung of its base-resolution ladder and `land-branch` uses without recomputing.

These are distinct from the product **Goals** in `docs/product/vision.md` (what success
looks like): posture is *how carefully to build right now*, not *what to build*.

## Team

Who works on this repo and how skills should package collaboration.
Skills that plan, review, or hand off read this section when present and
right-size **packaging** only (Solo / Small / Multi) — Iron Law gates never
change. Edit freely; re-run `/configure-repo` to re-draft from git/CODEOWNERS.
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
| **Multi** | CODEOWNERS-aware review language when ownership notes exist; explicit review responsibilities as prose; write-handoff/docs emphasis |
| **(no band)** | Team absent, or empty roster with blank override — pre-feature default; do not invent a team; do not hard-fail |

## Decision boundaries

Optional. When present, `record-verdict` reads this table. Pins may raise a
floor or bind an action to a boundary type. An entry that would lower a core
floor is ignored with a one-line notice. Absent section → core table only.

| Action | Boundary-Type | Floor |
|---|---|---|
| *(none pinned — core table only)* | | |

## Attention signals

Read by `select-review-sample`'s binding pass. Optional — absent, the built-in
defaults in `skills/review/select-review-sample/references/signals.md` apply.

Declared here because this repo's risk does not look like an application's. The
default globs watch auth, migrations, and payments; **this repo ships skill
bodies**, so a change to `skills/` is the thing that most needs human eyes, and
without these lines the feature under-samples its own product surface.

- **Partition depth:** 2
- **Risk globs:** `skills/**`, `hooks/**`, `scripts/**`, `templates/**`, `AGENTS.md`

## verify commands

Run in this order; all must pass before any completion claim.

| Check | Command |
|---|---|
| Typecheck | *(none)* |
| Lint | `python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-write-handoffs.py && python3 scripts/lint-context7.py` |
| Unit tests | `python3 -m unittest discover -s tests` |
| E2E / smoke | *(none)* |

Single test file: `python3 -m unittest tests.<module>`  
(e.g. `python3 -m unittest tests.test_lint_handoffs`)

The traceability check is not a command here — the `audit-trace` skill runs it as
`grep`/`git` over `docs/specs/` (and optional `docs/architecture/`). It is
**docs-only**: it does not grep application or pack test trees for requirement IDs.

Pack product fixtures under `tests/**` may still embed greppable `CODE-N.M` tokens
when testing this skill set itself (DOSP-2.5). That is not a consumer convention.

## Pack fixture note (this repo only)

Unit/scenario tests for skills may use greppable `CODE-N.M` in method names or
scenario markdown as product fixtures. Consumer apps must not be taught to do the same.

## Run locally (dev)

How to start the app for user-facing acceptance checks (read by `validate-api`
and `validate-ui`). Fill in once the app can be run locally; leave a row blank
if that surface does not exist.

| Surface | Start command | Ready signal |
|---|---|---|
| Backend / API | *(none — not an app)* | |
| Frontend | *(none — not an app)* | |

Browser E2E (Playwright, Chromium): *(none)* — the review-product-flow guide shell is covered by
source-contract tests in `tests/test_walk_product_guide_contract.py`; its runtime browser
behavior (a click firing a POST, a poll repainting) is deliberately deferred to
`validate-ui`, which owns harness setup. See DFSYNC tasks.md, "Browser coverage".

## release steps

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
