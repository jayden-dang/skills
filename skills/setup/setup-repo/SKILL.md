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

## 1. Read the setup state

This step does one thing: determine whether the repo is already configured for the skill set, and how completely. Read the repo's **own files only** — do not probe external services or their auth (no `gh auth`, `gh label list`, `glab`, no Linear MCP call) and do not read the user's shell environment (no `env`, no `*_API_KEY` probing). Detection is not the job here: the *user* drives what gets set up in Step 2, and any service or toolchain specifics are gathered later, in service of a choice the user has already made.

Check the setup markers — all by reading files in the repo:

- `docs/agents/project.md`, `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md` — present and filled in, or missing?
- An `## Agent skills` section in `CLAUDE.md` / `AGENTS.md` (note which of the two files exists)
- Seed files the skill set expects: `docs/specs/INDEX.md`, a glossary (`CONTEXT.md` or `CONTEXT-MAP.md`)
- `.skills/` and `.worktrees/` present in `.gitignore`

Then branch on what you found:

- **Already configured (fully or partly)** — this is a *fill-the-gaps* run, not a rebuild. List exactly what exists and what is missing or stale, show the user that summary, and offer to fill only the gaps. Walk only the Step 2 sections whose output is missing or that the user explicitly asks to change; leave everything already written untouched (the additive rule, Step 4).
- **Not configured** — go straight to the user-driven flow in Step 2. Do **not** guess the tracker from the git remote or a connected MCP server, and do not auto-detect anything the user should choose. Ask the user how they want to set the repo up, one decision at a time.

You may still read the repo's own manifests (lockfiles, `package.json` scripts, `Cargo.toml`, `pyproject.toml`, `Makefile`, test configs) to *pre-fill suggestions* in later steps — but reading a file in the repo is not the same as probing a service, and a pre-filled suggestion is never a decision made on the user's behalf.

**Done when:** you have classified the repo as configured / partly-configured / not-configured, listed any gaps, and presented that summary to the user.

## 2. Decide, one section at a time

Walk the six decisions below strictly one at a time: give a two-or-three-sentence explainer (what this is, which skills consume it, what changes with each choice), state your recommendation with a one-line reason, then wait for the user's answer before moving on. Never dump all sections at once. Assume the user has not seen these concepts before.

### A. Issue tracker

Explainer: skills that read or write issues (`triage`, `file-issues`, `write-plan` when publishing tasks, `release`) need to know where issues live and which commands touch them.

Options:

- **github** — repo issues via the `gh` CLI
- **gitlab** — repo issues via the `glab` CLI
- **linear** — issues in Linear, via a connected Linear MCP server (preferred) or the Linear GraphQL API; for teams that track work in Linear rather than in the code host
- **local** — markdown files under `.scratch/<feature>/`, each carrying a `Status:` line; good for solo repos or repos without a remote
- **other** — the user describes their workflow in a paragraph; record it as freeform prose

Recommend only from the repo's local git remote — a GitHub remote → github, a GitLab remote → gitlab, no remote → local — and always let the user overrule it. Do not probe a service or its auth to guess the tracker. Linear is a separate service and will not appear in `git remote`, so present it as an option and pick it whenever the user says the team lives in Linear, even if the code host is GitHub/GitLab.

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

List the tracker's existing labels next to the roles and propose a mapping (default: each role's string equals its name); the user confirms it. For any mapped label the tracker does not have yet, offer to create it — only with the user's explicit consent. For local trackers, the role names themselves are the vocabulary; defaults are fine. For **linear**, list the team's existing workflow states and labels first (via the MCP server or API), then map the state roles to Linear workflow states where one fits (e.g. `ready-for-agent` → a "Todo"/"Ready" state, `wontfix` → a "Canceled" state) and the category roles (`bug`/`enhancement`) to Linear labels.

**Done when:** every canonical role maps to a confirmed label string.

### C. Verify commands

Explainer: `tdd`, `verify`, `execute-plan`, and `release` all run this repo's proof commands; they must be exact, not guessed.

Confirm each, pre-filled from what you detected: typecheck, lint, unit tests, e2e/smoke, and the **single-test-file pattern** (the command shape for running one test file — the tight loop `tdd` lives in).

**Done when:** each command has been confirmed by the user (or explicitly marked "none").

### D. Test annotation conventions

Explainer: every test carries the requirement ID it covers, and the `trace` check greps tests for those IDs — so the convention must be greppable and match the repo's frameworks.

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
- Capture a conversation/spec/idea into tracker issues: `/file-issues` (user-run)
- Incoming issues and PRs: `/triage` (user-run)
- Traceability check: the `trace` skill — run by `verify` and `release`;
  keep it clean

Repo config the skills read:

- Verify commands, test annotations, release steps: `docs/agents/project.md`
- Issue tracker operations: `docs/agents/issue-tracker.md`
- Triage label mapping: `docs/agents/triage-labels.md`
```

5. Ensure the local working dirs are git-ignored: the skills' scratch artifacts — `execute-plan`'s ledger and briefs, and the scan/review digests the spec skills write — live under `.skills/`, and isolated workspaces under `.worktrees/`; neither belongs in version control. Idempotently, for each pattern: `grep -qxF '.skills/' .gitignore 2>/dev/null || printf '.skills/\n' >> .gitignore` (same for `.worktrees/`), then stage `.gitignore`. (A line-presence check, not `git check-ignore` — a trailing-slash pattern only matches an *existing* directory, so `check-ignore` would re-append before the dir exists.)

**Done when:** all files are written, `.skills/` and `.worktrees/` are git-ignored, and `git status` shows only the expected additions/edits.

## 5. Offer the session-start hook

The skill set installs nothing else into the repo — no linters, no CI steps, no git hooks. The one optional install keeps the skill-usage gate alive:

**Session-start hook.** If this skill set was installed without plugin hook support, offer to add a `SessionStart` hook (matcher `startup|clear|compact`) so the gate survives `/clear` and compaction. **Vendor the hook into the repo — never reference a path outside it.** An absolute path (e.g. to the skill set's own working copy) is committed into `.claude/settings.json` and breaks on any other machine, in CI, or if that copy moves. Instead:
   - Copy `templates/session-start.sh` to `.claude/hooks/session-start.sh` in the repo and `chmod +x` it. It is dependency-free (plain `cat`), so it runs in any project regardless of toolchain.
   - Reference it in `.claude/settings.json` via the project-dir variable, not an absolute path:
     ```json
     { "hooks": { "SessionStart": [ { "matcher": "startup|clear|compact",
       "hooks": [ { "type": "command",
         "command": "\"$CLAUDE_PROJECT_DIR/.claude/hooks/session-start.sh\"" } ] } ] } }
     ```
   - Merge into any existing `SessionStart` block additively; do not clobber other hooks.

**Done when:** the hook offer has an explicit yes/no, and a yes is implemented.

## 6. Prove the configuration actually works — GATE

Confirmed-with-the-user is not the same as works-in-this-project. Commands were pre-filled from what you detected; a wrong manifest path, a missing script, or a tool that is not installed will surface as a mid-task failure in `tdd`, `verify`, or `release` weeks from now. Prove them now, while you own the context. This is the discipline of the `verify` skill applied to the config you just wrote: run the command, read the output, believe the output — not the config.

Run each configured verify command fresh and classify the result. The distinction that matters is **wiring vs content**:

- **Wiring failure** — the command could not run as written: "command not found" / exit 127, "missing script", "no such file or directory", a bad `--manifest-path` or unknown flag, an uninstalled tool. **This is a config bug you must fix**: re-detect, correct `docs/agents/project.md`, and re-run until it is gone. Setup is not done while any command is mis-wired.
- **Content failure** — the tool ran correctly but reported problems (type errors, lint warnings, failing tests). The command is wired right; the repo has pre-existing issues. Record these for the user; they do **not** block setup.
- **Pass** — wired and green.

Be cost-aware — do not run the whole suite to prove wiring:

- Typecheck and lint: run in full (bounded).
- Unit/e2e runners: prove the runner resolves its config cheaply — run the **single-test-file pattern** from `project.md` against one existing test file, or the runner's collect-only/list mode. Never trigger a full e2e run during setup; state that the full run is the user's to do later.
- Trace check: run it (REQUIRED SUB-SKILL: use `trace`) and confirm it reports a clean finding set — zero requirements is a valid clean state. The check is `grep`/`git` over `docs/specs/` and the test globs, so there is nothing to install; if the test globs it searches don't match this repo's layout, record the right ones in `docs/agents/project.md` now.
- If you installed the session-start hook, execute `.claude/hooks/session-start.sh` and confirm it prints one line of valid JSON.
- If the tracker is a remote service (`github` / `gitlab` / `linear`), prove it is reachable and authenticated with **one read-only call** — `gh issue list` / `glab issue list`, or for Linear a single MCP list call (or a minimal `issues` GraphQL query). This verifies the tracker the *user already chose*; it is not the setup-time detection Step 1 forbids — the choice is made, and this call only proves it works. A missing CLI, an unauthenticated session, or a disconnected or unauthenticated MCP server is a wiring failure; it would otherwise stay hidden until `triage` fails weeks later. `local` and `other` need no reachability check.

Report a small table: each command → wired? → passed / failed / pre-existing.

**Done when:** every configured command is proven **wired** (no wiring failures remain), the trace check runs clean, the hook (if installed) fires, the configured tracker answers a read-only call, and any content failures are listed for the user.

## 7. Finish

Tell the user setup is complete, which skills now read the config, that the verify table shows what is wired vs pre-existing, and that `docs/agents/*.md` can be edited directly later — re-running this wizard is only needed to switch trackers or start over.
