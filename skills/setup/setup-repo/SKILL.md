---
name: setup-repo
description: Use when a repository has not been configured for this skill set yet (no docs/agents/ directory, verify commands unknown, triage labels unmapped), or when the user wants to change the repo's tracker, labels, verify commands, or release steps.
disable-model-invocation: true
---

# Set Up the Repo

Configure a repository, once, so every other skill can read its answers instead of guessing. The output is a set of agent-facing config files under `docs/agents/`, seed spec files, and a pointer block in the repo's agent instructions.

This is a conversation, not a script: explore, present what you found, decide one thing at a time with the user, then write.

Template seeds live in this skill set's `templates/` directory — resolve it as `${CLAUDE_PLUGIN_ROOT}/templates` when installed as a plugin, otherwise `../../../templates` relative to this SKILL.md.

## 1. Explore

Before asking anything, learn the repo's starting state:

- `git remote -v` — GitHub? GitLab? No remote?
- `CLAUDE.md` and `AGENTS.md` at the root — which exists? Does either already contain an `## Agent skills` section?
- `docs/agents/` — has this skill already run here?
- `docs/specs/`, `docs/adr/`, `CONTEXT.md`, `CONTEXT-MAP.md`, `.scratch/`, `.out-of-scope/`
- Package manager and toolchain (lockfiles, `package.json` scripts, `Cargo.toml`, `pyproject.toml`, `Makefile`, …)
- Test runners and their configs; existing CI workflows
- Existing tracker labels (`gh label list` / `glab label list`) if a remote tracker is plausible

**Done when:** you have presented a short findings summary — what exists, what is missing, what you can pre-fill.

## 2. Decide, one section at a time

Walk the six decisions below strictly one at a time: give a two-or-three-sentence explainer (what this is, which skills consume it, what changes with each choice), state your recommendation with a one-line reason, then wait for the user's answer before moving on. Never dump all sections at once. Assume the user has not seen these concepts before.

### A. Issue tracker

Explainer: skills that read or write issues (`triage`, `write-plan` when publishing tasks, `release`) need to know where issues live and which commands touch them.

Options:

- **github** — repo issues via the `gh` CLI
- **gitlab** — repo issues via the `glab` CLI
- **local** — markdown files under `.scratch/<feature>/`, each carrying a `Status:` line; good for solo repos or repos without a remote
- **other** — the user describes their workflow in a paragraph; record it as freeform prose

Recommend based on the remote: GitHub remote → github, GitLab host → gitlab, no remote → local.

Follow-up (github/gitlab only): **are external pull requests a request surface?** Explainer: open-source repos often receive feature requests as PRs — a PR is an issue with attached code. If yes, `triage` pulls external PRs into the same queue and state machine. Default: no. Skip the question entirely for local/other.

**Done when:** tracker choice and the PR-surface answer are confirmed.

### B. Triage label mapping

Explainer: `triage` moves issues through canonical roles, but it must apply the label strings this repo actually uses, or it will create duplicates.

The canonical roles — five states and two categories:

| Role | Meaning |
|---|---|
| needs-triage | awaiting evaluation |
| needs-info | waiting on the reporter |
| ready-for-agent | fully specified; an agent can pick it up cold |
| ready-for-human | needs human judgment or access |
| wontfix | will not be actioned |
| bug | something is broken |
| enhancement | new capability or improvement |

Show the repo's existing labels next to the roles and propose a mapping (default: each role's string equals its name). For any mapped label that does not exist in the tracker yet, offer to create it — only with the user's explicit consent. For local trackers, the role names themselves are the vocabulary; defaults are fine.

**Done when:** every canonical role maps to a confirmed label string.

### C. Verify commands

Explainer: `tdd`, `verify`, `execute-plan`, and `release` all run this repo's proof commands; they must be exact, not guessed.

Confirm each, pre-filled from what you detected: typecheck, lint, unit tests, e2e/smoke, and the **single-test-file pattern** (the command shape for running one test file — the tight loop `tdd` lives in). Also confirm where `check-trace.mjs` will be invoked from.

**Done when:** each command has been confirmed by the user (or explicitly marked "none").

### D. Test annotation conventions

Explainer: every test carries the requirement ID it covers, and `check-trace` greps tests for those IDs — so the convention must be greppable and match the repo's frameworks.

Per test layer, recommend a convention based on the detected frameworks (for example: an e2e tag like `{ tag: ['@CODE-N.M'] }`, a unit-test annotation or the ID in the test name, a `/// REQ: CODE-N.M` doc comment for compiled languages). Confirm one convention per layer.

**Done when:** every test layer in the repo has a confirmed ID convention.

### E. Release steps

Explainer: the `release` skill executes an ordered list of project-specific commands — build, bundle, sign, publish — and it refuses to improvise them.

Draft the ordered list from what you found (build scripts, packaging config) and confirm. Include the smoke-check command if one exists.

**Done when:** the ordered release steps are confirmed (an empty list is a valid answer for libraries with no build).

### F. Docs layout

Explainer: spec and discovery skills read `docs/specs/`, `docs/adr/`, and the domain glossary; they need to know the shape.

Confirm:

- Specs at `docs/specs/`, ADRs at `docs/adr/` (create the directories if missing)
- Glossary layout: **single-context** (one root `CONTEXT.md` — most repos) or **multi-context** (a root `CONTEXT-MAP.md` pointing at per-context `CONTEXT.md` files — typically monorepos)

**Done when:** layout is confirmed.

## 3. Draft and confirm

Show the user, before writing anything:

- the three `docs/agents/*.md` files' contents
- the `## Agent skills` block destined for CLAUDE.md/AGENTS.md

Let them edit. **Done when:** the user approves the drafts.

## 4. Write

**The additive rule: existing files are edited in place, never clobbered.** If a target file already exists, merge your content into it and preserve everything the user wrote.

1. Write `docs/agents/project.md`, `docs/agents/issue-tracker.md`, and `docs/agents/triage-labels.md`, seeded from `templates/agents/project.md`, `templates/agents/issue-tracker.md`, and `templates/agents/triage-labels.md`. In the issue-tracker file keep only the chosen tracker's operations section, and record the PR-surface answer.
2. If `docs/specs/INDEX.md` is missing, create it from `templates/specs-INDEX.md`.
3. If the glossary is missing, create `CONTEXT.md` from `templates/CONTEXT.md` (or a `CONTEXT-MAP.md` for multi-context, per the user's answer).
4. Add the `## Agent skills` block:
   - If `CLAUDE.md` exists, edit it. Else if `AGENTS.md` exists, edit that. **Never create `AGENTS.md` when `CLAUDE.md` exists** (or vice versa). If neither exists, ask the user which to create — do not pick for them.
   - If an `## Agent skills` section already exists, update it in place — never append a duplicate, never touch the surrounding sections.

The block:

```markdown
## Agent skills

This repo is configured for a spec-driven skill set.

- Feature flow: `brainstorm` → `write-requirements` → `write-design` →
  `write-plan` → `execute-plan`
- Bug on-ramp: `debug` (root cause first, then a guarded fix)
- Incoming issues and PRs: `triage`
- Traceability lint: `node <configured path>/check-trace.mjs` — run by
  `verify` and `release`; keep it green

Repo config the skills read:

- Verify commands, test annotations, release steps: `docs/agents/project.md`
- Issue tracker operations: `docs/agents/issue-tracker.md`
- Triage label mapping: `docs/agents/triage-labels.md`
```

**Done when:** all files are written and `git status` shows only the expected additions/edits.

## 5. Offer the opt-ins

Two optional installs — offer each, act only on a yes:

1. **Session-start hook.** If this skill set was installed without plugin hook support, offer to add a `SessionStart` hook (matcher `startup|clear|compact`) to the project's `.claude/settings.json` invoking the skill set's `hooks/session-start.sh`, so the skill-usage gate survives `/clear` and compaction.
2. **Trace check in CI.** Offer to append a step to the existing CI workflow that runs `check-trace.mjs` (with `--strict` if the user wants warnings to fail too). Edit the existing workflow additively; do not author a new pipeline.

**Done when:** each offer has an explicit yes/no, and any yes is implemented.

## 6. Finish

Tell the user setup is complete, which skills now read the config, and that `docs/agents/*.md` can be edited directly later — re-running this wizard is only needed to switch trackers or start over.
