---
name: setup-repo
description: Use when a repository has not been configured for this skill set yet (no docs/agents/ directory, verify commands unknown, triage labels unmapped), or when the user wants to change the repo's tracker, labels, verify commands, or release steps. This is the entry point for adopting the skill set into an existing or mature repo — where `scaffold-project` redirects when the directory is not greenfield.
disable-model-invocation: true
---

# Set Up the Repo

Configure a repository, once, so every other skill can read its answers instead of guessing. The output is a set of agent-facing config files under `docs/agents/`, seed spec files, and a pointer block in the repo's agent instructions.

This is a conversation, not a script: explore, present what you found, decide one thing at a time with the user, then write.

Template seeds live in this skill set's `templates/` directory — resolve it as `${CLAUDE_PLUGIN_ROOT}/templates` when installed as a plugin, otherwise `../../../templates` relative to this SKILL.md.

## Track progress

This skill has seven steps and skipping one is the common failure — an unconfigured tracker, or the Step 6 verification gate never run. Before Step 1, create a todo for each numbered step below and complete them in order, checking each off only when its **Done when** is met. Step 6 (prove the configuration works) is not optional.

## 1. Explore

Before asking anything, learn the repo's starting state:

- `git remote -v` — GitHub? GitLab? No remote?
- Is a **Linear** MCP server connected, or a `LINEAR_API_KEY` set in the environment? Either signals a team that tracks work in Linear rather than the code host.
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
- **linear** — issues in Linear, via a connected Linear MCP server (preferred) or the Linear GraphQL API; for teams that track work in Linear rather than in the code host
- **local** — markdown files under `.scratch/<feature>/`, each carrying a `Status:` line; good for solo repos or repos without a remote
- **other** — the user describes their workflow in a paragraph; record it as freeform prose

Recommend based on what you found: GitHub remote → github, GitLab host → gitlab, a connected Linear MCP server or a `LINEAR_API_KEY` → linear, no remote and no tracker signal → local. Linear is a separate service and will not appear in `git remote`, so offer it whenever the user says the team lives in Linear even if the code host is GitHub/GitLab.

Follow-up (github/gitlab only): **are external pull requests a request surface?** Explainer: open-source repos often receive feature requests as PRs — a PR is an issue with attached code. If yes, `triage` pulls external PRs into the same queue and state machine. Default: no. Skip the question entirely for linear/local/other — for a Linear shop, requests arrive as Linear issues and any PRs stay in the linked code host, not the triage queue.

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

Show the repo's existing labels next to the roles and propose a mapping (default: each role's string equals its name). For any mapped label that does not exist in the tracker yet, offer to create it — only with the user's explicit consent. For local trackers, the role names themselves are the vocabulary; defaults are fine. For **linear**, list the team's existing workflow states and labels first (via the MCP server or API), then map the state roles to Linear workflow states where one fits (e.g. `ready-for-agent` → a "Todo"/"Ready" state, `wontfix` → a "Canceled" state) and the category roles (`bug`/`enhancement`) to Linear labels.

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
4. Add the `## Agent skills` block. It lives in exactly **one** canonical file; any second file is a thin pointer, never a copy of the block.
   - **Neither `CLAUDE.md` nor `AGENTS.md` exists** (the default): make `AGENTS.md` canonical (it holds the block) and write a short `CLAUDE.md` whose entire body points at `AGENTS.md` — so Claude Code finds instructions by its native filename without duplicating them. Do not ask which to create; this pattern serves both.
   - **Only one exists:** that file is canonical — add or update the block in it. If it is `AGENTS.md` and Claude Code is a target, also add the `CLAUDE.md` pointer. If it is `CLAUDE.md`, leave it canonical — do not demote it to a pointer or create a competing `AGENTS.md`.
   - **Both exist:** put the block in whichever already carries real agent instructions; make the other a pointer only if it is not already substantive. Never place the block in both.
   - If an `## Agent skills` section already exists in the canonical file, update it in place — never append a duplicate, never touch surrounding sections.

   The `CLAUDE.md` pointer, when you create one:

   ```markdown
   # CLAUDE.md

   The canonical agent instructions for this repo live in **[AGENTS.md](AGENTS.md)** —
   read it first. It applies to Claude too; this file exists only so Claude Code
   finds it by its native name.
   ```

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

1. **Session-start hook.** If this skill set was installed without plugin hook support, offer to add a `SessionStart` hook (matcher `startup|clear|compact`) so the skill-usage gate survives `/clear` and compaction. **Vendor the hook into the repo — never reference a path outside it.** An absolute path (e.g. to the skill set's own working copy) is committed into `.claude/settings.json` and breaks on any other machine, in CI, or if that copy moves. Instead:
   - Copy `templates/session-start.sh` to `.claude/hooks/session-start.sh` in the repo and `chmod +x` it. It is dependency-free (plain `cat`), so it runs in any project regardless of toolchain.
   - Reference it in `.claude/settings.json` via the project-dir variable, not an absolute path:
     ```json
     { "hooks": { "SessionStart": [ { "matcher": "startup|clear|compact",
       "hooks": [ { "type": "command",
         "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh\"" } ] } ] } }
     ```
   - Merge into any existing `SessionStart` block additively; do not clobber other hooks.
2. **Trace check in CI.** Offer to append a step to the existing CI workflow that runs `check-trace.mjs` (with `--strict` if the user wants warnings to fail too). Edit the existing workflow additively; do not author a new pipeline.

**Done when:** each offer has an explicit yes/no, and any yes is implemented.

## 6. Prove the configuration actually works — GATE

Confirmed-with-the-user is not the same as works-in-this-project. Commands were pre-filled from what you detected; a wrong manifest path, a missing script, or a tool that is not installed will surface as a mid-task failure in `tdd`, `verify`, or `release` weeks from now. Prove them now, while you own the context. This is the discipline of the `verify` skill applied to the config you just wrote: run the command, read the output, believe the output — not the config.

Run each configured verify command fresh and classify the result. The distinction that matters is **wiring vs content**:

- **Wiring failure** — the command could not run as written: "command not found" / exit 127, "missing script", "no such file or directory", a bad `--manifest-path` or unknown flag, an uninstalled tool. **This is a config bug you must fix**: re-detect, correct `docs/agents/project.md`, and re-run until it is gone. Setup is not done while any command is mis-wired.
- **Content failure** — the tool ran correctly but reported problems (type errors, lint warnings, failing tests). The command is wired right; the repo has pre-existing issues. Record these for the user; they do **not** block setup.
- **Pass** — wired and green.

Be cost-aware — do not run the whole suite to prove wiring:

- Typecheck and lint: run in full (bounded).
- Unit/e2e runners: prove the runner resolves its config cheaply — run the **single-test-file pattern** from `project.md` against one existing test file, or the runner's collect-only/list mode. Never trigger a full e2e run during setup; state that the full run is the user's to do later.
- `check-trace.mjs`: run it — it must execute and exit 0 (zero requirements is a valid clean state). If it fails to run at all (e.g. no `node`), that is a wiring failure worth flagging: this repo needs that runtime for the trace lint, or the lint must be adapted.
- If you installed the session-start hook, execute `.claude/hooks/session-start.sh` and confirm it prints one line of valid JSON.
- If the tracker is a remote service (`github` / `gitlab` / `linear`), prove it is reachable and authenticated with **one read-only call** — `gh issue list` / `glab issue list`, or for Linear a single MCP list call (or a minimal `issues` GraphQL query). A missing CLI, an unauthenticated session, a bad `LINEAR_API_KEY`, or a disconnected MCP server is a wiring failure; it would otherwise stay hidden until `triage` fails weeks later. `local` and `other` need no reachability check.

Report a small table: each command → wired? → passed / failed / pre-existing.

**Done when:** every configured command is proven **wired** (no wiring failures remain), `check-trace` runs clean, the hook (if installed) fires, the configured tracker answers a read-only call, and any content failures are listed for the user.

## 7. Finish

Tell the user setup is complete, which skills now read the config, that the verify table shows what is wired vs pre-existing, and that `docs/agents/*.md` can be edited directly later — re-running this wizard is only needed to switch trackers or start over.
