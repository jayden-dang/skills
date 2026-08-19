# Requirements: pack seed shipping (tier-1)

Feature code: SEED
Status: Approved
Date: 2026-08-19

<!--
Tier-1 mini-spec for the missing-templates install bug.
Root `templates/` stays the authoring SSOT. Consumer skills carry
byte-identical copies so `npx skills add` (flatten) ships the seeds.
-->

## 1. Consumer-local seed copies

**Story:** As someone who installed the pack with `npx skills add`, I want `/configure-repo` (and every other seed-reading skill) to find its seed files without a checkout of this repo, so setup does not report missing templates.

- **SEED-1.1** WHEN engineer-pack or personal-pack is installed via `npx skills` THE SYSTEM SHALL include, inside each consumer skill directory, a copy of every repo-root `templates/` file that skill's `SKILL.md` cites — at the same relative path under that skill's `templates/` (example: `skills/setup/configure-repo/templates/agents/project.md`).
- **SEED-1.2** WHEN a consumer `SKILL.md` cites a repo-root `templates/<path>` and that skill directory has no copy at `templates/<path>`, or the copy's bytes differ from the SSOT file THE SYSTEM SHALL fail `scripts/lint-skill-templates.py` with a non-zero exit.
- **SEED-1.3** WHEN a consumer skill resolves a pack seed THE SYSTEM SHALL try, in this order, the first path that exists: (1) `templates/` beside its `SKILL.md`, (2) `${CLAUDE_PLUGIN_ROOT}/templates` when that variable is set, (3) `../../../templates` relative to its `SKILL.md`.

A **cite** is a greppable `templates/<relpath>` in that skill's `SKILL.md` whose `<relpath>` names a file under repo-root `templates/`. It does **not** include a skill's private tree (for example `define-system-doc/templates/`).

### Consumer map (install-time copies)

| Skill | SSOT files to copy |
|---|---|
| `configure-repo` | `agents/project.md`, `agents/issue-tracker.md`, `agents/triage-labels.md`, `specs-INDEX.md`, `CONTEXT.md`, `product-vision.md`, `architecture-INDEX.md`, `product-guidelines.md`, `session-start.sh` |
| `bootstrap-repo` | `CONTEXT.md`, `specs-INDEX.md`, `product-vision.md`, `architecture-INDEX.md`, `product-guidelines.md` |
| `specify-behavior` | `requirements.md`, `roadmap-findings.md`, `skills-ephemera-paths.md` |
| `design-solution` | `design.md` |
| `plan-tasks` | `tasks.md` |
| `define-domain` | `CONTEXT.md` |
| `define-project` | `product-vision.md`, `architecture-INDEX.md`, `product-guidelines.md` |
| `plan-milestones` | `roadmap-INDEX.md`, `milestone-assessment.md` |
| `record-debt` | `quality-debt.md` |
| `assess-milestone` | `roadmap-findings.md`, `milestone-assessment.md` |
| `refresh-roadmap-status` | `roadmap-findings.md`, `roadmap-INDEX.md`, `skills-ephemera-paths.md` |
| `build-in-waves` | `skills-ephemera-paths.md` |
| `build-by-story` | `skills-ephemera-paths.md` |
| `build-inline` | `skills-ephemera-paths.md` |
| `life-setup` | every file under `templates/personal-os/` |

## 2. Guards

Touched files and existing behavior:

| File / surface | Guard |
|---|---|
| `templates/**` (repo root) | **SEED-2.1** (guard) WHEN a seed is authored or edited THE SYSTEM SHALL CONTINUE TO treat repo-root `templates/` as the single authoring original. |
| Plugin install (`${CLAUDE_PLUGIN_ROOT}/templates`) | **SEED-2.2** (guard) WHEN the pack is installed as a Claude plugin THE SYSTEM SHALL CONTINUE TO resolve `${CLAUDE_PLUGIN_ROOT}/templates` as a valid seed directory. |
| Source-tree relative path | **SEED-2.3** (guard) WHEN a skill runs from `skills/<category>/<name>/` in this repo THE SYSTEM SHALL CONTINUE TO resolve `../../../templates` to the repo-root SSOT. |
| `lefthook.yml` | **SEED-2.4** (guard) WHEN `lefthook` runs pre-commit or pre-push THE SYSTEM SHALL CONTINUE TO run `lint-skill-frontmatter.py`, `lint-skill-evals.py`, `lint-write-handoffs.py`, and `lint-context7.py`. |
| `skills/personal/life-setup/SKILL.md` | **SEED-2.5** (guard) WHEN `life-setup` cannot find `templates/personal-os/` THE SYSTEM SHALL CONTINUE TO create minimal stubs and not invent a second layout system. |
| `.claude-plugin/plugin.json`, `marketplace.json`, `personal-os.plugin.json` | **SEED-2.6** (guard) WHEN the pack manifests are read THE SYSTEM SHALL CONTINUE TO list only skill folders that already exist — no `pack-templates` (or other asset-only) skill. |
| `skills/setup/configure-repo/SKILL.md` Step 4 | **SEED-2.7** (guard) WHEN `configure-repo` writes seeds into a consuming repo THE SYSTEM SHALL CONTINUE TO edit existing target files in place and never clobber user-written content. |
| `skills/project/define-system-doc/templates/` | no behavior to guard — private catalog templates, not pack SSOT. |
| `scripts/lint-skill-templates.py` (new) | no behavior to guard. |
| Consumer `templates/` copies (new) | no behavior to guard. |
| `docs/guide/resources/templates.md` | **SEED-2.8** (guard) WHEN the human guide names seed locations THE SYSTEM SHALL CONTINUE TO point at repo-root `templates/` as the authoring home. |
