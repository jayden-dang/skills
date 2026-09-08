# Templates

Seed files the skills copy into a consuming repo. They live in [`templates/`](../../../templates/) at the repo root — that tree is the **authoring SSOT**. Each skill that reads a seed also carries a byte-identical copy under its own `templates/` so `npx skills add` (which copies only the skill folder) still has the file after flatten.

Resolve order, first path that exists: (1) `templates/` beside this SKILL.md, (2) `${CLAUDE_PLUGIN_ROOT}/templates` when that variable is set, (3) `../../../templates` relative to the SKILL.md. `scripts/lint-skill-templates.py` fails if a cite has no copy or the copy drifted from SSOT; `python3 scripts/lint-skill-templates.py --write` refreshes the copies.

## The spec triad

| Template | Copied by | Becomes |
|---|---|---|
| [`requirements.md`](../../../templates/requirements.md) | [`specify-behavior`](../skills/specify-behavior.md) | `docs/specs/<date>-<feature>/requirements.md` |
| [`design.md`](../../../templates/design.md) | [`design-solution`](../skills/design-solution.md) | `docs/specs/<date>-<feature>/design.md` |
| [`tasks.md`](../../../templates/tasks.md) | [`plan-tasks`](../skills/plan-tasks.md) | `docs/specs/<date>-<feature>/tasks.md` |

Each carries its rules as an HTML comment at the top, so the rules travel with the file rather than living only in the skill.

### `requirements.md`

Header block (`Feature code:`, `Status:`, `Date:`), then one `## N. <title>` section per story with a `**Story:** As a <actor>, I want <capability>, so that <benefit>.` line and [EARS](ears.md) criteria beneath it. Then `## Out of Scope` and `## Open Questions` — the latter deleted when empty, and always before `Status: Approved`.

### `design.md`

`## Context` (2–4 paragraphs), `## Decisions` (numbered, 1–2 sentences each), `## Architecture` with one `###` section per component — **each carrying a `Satisfies: <CODE>-N.M` line** — then the `## Seams for testing` table and a `## Coverage check`.

The seam table is a REQUIRED slot rather than a suggestion, because [`test-first`](../skills/test-first.md) refuses to write a test at a seam it does not name:

```markdown
| Seam | Kind | Covers |
|---|---|---|
| <module/interface> | unit / integration / e2e | <CODE>-1.x |
```

### `tasks.md`

Opens with a pointer that makes the file self-executing:

```markdown
> **For agentic workers:** REQUIRED SUB-SKILL: use `build-in-waves` to implement
> this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
```

Then the header, `## Global Constraints`, `## File Structure`, and the tasks. Each task is a REQUIRED-slot structure — **Files**, **Interfaces** (Consumes / Produces), checkbox **Steps** with complete code and exact commands, and a `_Requirements: <CODE>-N.M_` footer.

The template says out loud what a plan bug looks like:

> *complete code block — no placeholders, no "add appropriate error handling", no "similar to Task N"*

## Repo config

Written once by [`configure-repo`](../skills/configure-repo.md) into `docs/agents/`.

| Template | Becomes | Read by |
|---|---|---|
| [`agents/project.md`](../../../templates/agents/project.md) | `docs/agents/project.md` | `test-first`, `prove-claim`, `build-in-waves`, `isolate-workspace`, `cut-release`, the acceptance skills, `write-flow-guide`, `run-spike`, `debug-remote`, `assess-observability` |
| [`agents/issue-tracker.md`](../../../templates/agents/issue-tracker.md) | `docs/agents/issue-tracker.md` | `triage`, `plan-tasks`, `cut-release` |
| [`agents/triage-labels.md`](../../../templates/agents/triage-labels.md) | `docs/agents/triage-labels.md` | `triage` |

`configure-repo` keeps only the chosen tracker's operations section in `issue-tracker.md`.

**`project.md` grows after setup.** The acceptance skills write a `## Run locally (dev)` section into it the first time they have to discover how to start the app — so the next run is cheap.

## Other seeds

| Template | Becomes | Notes |
|---|---|---|
| [`CONTEXT.md`](../../../templates/CONTEXT.md) | root `CONTEXT.md` | The domain glossary. Created *lazily* by [`define-domain`](../skills/define-domain.md) when the first term settles, if `configure-repo` did not already seed it |
| [`specs-INDEX.md`](../../../templates/specs-INDEX.md) | `docs/specs/INDEX.md` | The feature-code registry `frame-change` and `inspect-change` search for overlap |

This is the whole seed set. Nothing executable lands in a consuming repo — no linters, no CI, no git hooks, no session-start hook.

## The additive rule

Every template application obeys one rule, stated in `configure-repo`:

> **Existing files are edited in place, never clobbered.** If a target file already exists, merge your content into it and preserve everything the user wrote.

This applies to `.gitignore` (idempotent line-presence checks) and to `CLAUDE.md` / `AGENTS.md` (the `## Agent skills` block lives in exactly one canonical file; any second file is a thin pointer, never a copy).

## See also

- [The artifact model](../concepts/artifacts.md) — where each of these lands
- [EARS reference](ears.md) — the criterion grammar `requirements.md` uses
- [`configure-repo`](../skills/configure-repo.md) — the wizard that applies most of these
- [Traceability — the spine](../concepts/traceability.md) — the audit-trace check `prove-claim` and `cut-release` run
