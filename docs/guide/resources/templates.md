# Templates

Seed files the skills copy into a consuming repo. They live in [`templates/`](../../../templates/) at the repo root.

When the skill set is installed as a plugin, skills resolve the directory as `${CLAUDE_PLUGIN_ROOT}/templates`; otherwise as a path relative to the SKILL.md.

## The spec triad

| Template | Copied by | Becomes |
|---|---|---|
| [`requirements.md`](../../../templates/requirements.md) | [`write-requirements`](../skills/write-requirements.md) | `docs/specs/<date>-<feature>/requirements.md` |
| [`design.md`](../../../templates/design.md) | [`write-design`](../skills/write-design.md) | `docs/specs/<date>-<feature>/design.md` |
| [`tasks.md`](../../../templates/tasks.md) | [`write-plan`](../skills/write-plan.md) | `docs/specs/<date>-<feature>/tasks.md` |

Each carries its rules as an HTML comment at the top, so the rules travel with the file rather than living only in the skill.

### `requirements.md`

Header block (`Feature code:`, `Status:`, `Date:`), then one `## N. <title>` section per story with a `**Story:** As a <actor>, I want <capability>, so that <benefit>.` line and [EARS](ears.md) criteria beneath it. Then `## Out of Scope` and `## Open Questions` — the latter deleted when empty, and always before `Status: Approved`.

### `design.md`

`## Context` (2–4 paragraphs), `## Decisions` (numbered, 1–2 sentences each), `## Architecture` with one `###` section per component — **each carrying a `Satisfies: <CODE>-N.M` line** — then the `## Seams for testing` table and a `## Coverage check`.

The seam table is a REQUIRED slot rather than a suggestion, because [`tdd`](../skills/tdd.md) refuses to write a test at a seam it does not name:

```markdown
| Seam | Kind | Covers |
|---|---|---|
| <module/interface> | unit / integration / e2e | <CODE>-1.x |
```

### `tasks.md`

Opens with a pointer that makes the file self-executing:

```markdown
> **For agentic workers:** REQUIRED SUB-SKILL: use `execute-plan` to implement
> this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.
```

Then the header, `## Global Constraints`, `## File Structure`, and the tasks. Each task is a REQUIRED-slot structure — **Files**, **Interfaces** (Consumes / Produces), checkbox **Steps** with complete code and exact commands, and a `_Requirements: <CODE>-N.M_` footer.

The template says out loud what a plan bug looks like:

> *complete code block — no placeholders, no "add appropriate error handling", no "similar to Task N"*

## Repo config

Written once by [`setup-repo`](../skills/setup-repo.md) into `docs/agents/`.

| Template | Becomes | Read by |
|---|---|---|
| [`agents/project.md`](../../../templates/agents/project.md) | `docs/agents/project.md` | `tdd`, `verify`, `execute-plan`, `worktrees`, `release`, the acceptance skills, `dogfood`, `prototype` |
| [`agents/issue-tracker.md`](../../../templates/agents/issue-tracker.md) | `docs/agents/issue-tracker.md` | `triage`, `write-plan`, `release` |
| [`agents/triage-labels.md`](../../../templates/agents/triage-labels.md) | `docs/agents/triage-labels.md` | `triage` |

`setup-repo` keeps only the chosen tracker's operations section in `issue-tracker.md`.

**`project.md` grows after setup.** The acceptance skills write a `## Run locally (dev)` section into it the first time they have to discover how to start the app — so the next run is cheap.

## Other seeds

| Template | Becomes | Notes |
|---|---|---|
| [`CONTEXT.md`](../../../templates/CONTEXT.md) | root `CONTEXT.md` | The domain glossary. Created *lazily* by [`domain-modeling`](../skills/domain-modeling.md) when the first term settles, if `setup-repo` did not already seed it |
| [`specs-INDEX.md`](../../../templates/specs-INDEX.md) | `docs/specs/INDEX.md` | The feature-code registry |
| [`session-start.sh`](../../../templates/session-start.sh) | `.claude/hooks/session-start.sh` | Vendored **into the repo**, never referenced by absolute path |
| [`githooks/pre-commit`](../../../templates/githooks/pre-commit) | `.githooks/pre-commit` | The *fast* gates: format staged, lint, typecheck |
| [`githooks/pre-push`](../../../templates/githooks/pre-push) | `.githooks/pre-push` | The fuller suite, plus `check-trace` and `check-graph --verify` |

### Why the session hook is vendored

An absolute path to the skill set's own working copy would be committed into `.claude/settings.json` and break on every other machine, in CI, and if that copy ever moves. So `setup-repo` copies the script into the repo and references it through the project-dir variable:

```json
{ "hooks": { "SessionStart": [ { "matcher": "startup|clear|compact",
  "hooks": [ { "type": "command",
    "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh\"" } ] } ] } }
```

The script is dependency-free, so it runs in any project regardless of toolchain.

### Why the git hooks are split

`pre-commit` gets only the fast gates. `pre-push` gets the tests and both linters.

> A hook slow enough to be routinely `--no-verify`'d is worse than none.

If a typecheck drags, move it to pre-push. And if the repo already runs a hook manager — `.husky/`, `lefthook.yml`, `.pre-commit-config.yaml`, or `simple-git-hooks` — the verify commands go into **that**, never into a competing mechanism.

Because `core.hooksPath` is local config and is not carried by a clone, a JS repo also gets a `"prepare": "git config core.hooksPath .githooks"` script so fresh clones apply it on install.

## The additive rule

Every template application obeys one rule, stated in `setup-repo`:

> **Existing files are edited in place, never clobbered.** If a target file already exists, merge your content into it and preserve everything the user wrote.

This applies to `.gitignore` (idempotent line-presence checks), to `CLAUDE.md` / `AGENTS.md` (the `## Agent skills` block lives in exactly one canonical file; any second file is a thin pointer, never a copy), to CI workflows (append steps, do not author a pipeline), and to hook configs (merge into an existing `SessionStart` block).

## See also

- [The artifact model](../concepts/artifacts.md) — where each of these lands
- [EARS reference](ears.md) — the criterion grammar `requirements.md` uses
- [`setup-repo`](../skills/setup-repo.md) — the wizard that applies most of these
- [Scripts](scripts.md) — the linters the hooks and CI run
