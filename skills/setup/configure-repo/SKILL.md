---
name: configure-repo
version: 1.6.1
description: Sets up docs/agents config so this skill set can run in an existing repo.
disable-model-invocation: true
---

# Set Up the Repo

Configure a repository, once, so every other skill can read its answers instead of guessing. The output is a set of agent-facing config files under `docs/agents/`, seed spec files, and a pointer block in the repo's agent instructions.

This is a conversation, not a script: explore, present what you found, decide one thing at a time with the user, then write.

Template seeds live in this skill set's `templates/` directory. Resolve pack seeds in this order, first path that exists: (1) `templates/` beside this SKILL.md, (2) `${CLAUDE_PLUGIN_ROOT}/templates` when that variable is set, (3) `../../../templates` relative to this SKILL.md.

## Track progress

This skill has seven steps (decisions A–L inside step 2) and skipping one is the common failure — an unconfigured tracker, or the Step 6 verification gate never run. Before Step 1, create a todo for each numbered step below and complete them in order, checking each off only when its **Done when** is met. Step 6 (prove the configuration works) is not optional.

## 1. Read the setup state

This step does one thing: determine whether the repo is already configured for the skill set, and how completely. Read the repo's **own files only** — do not probe external services or their auth (no `gh auth`, `gh label list`, `glab`, no Linear MCP call) and do not read the user's shell environment (no `env`, no `*_API_KEY` probing). Detection is not the job here: the *user* drives what gets set up in Step 2, and any service or toolchain specifics are gathered later, in service of a choice the user has already made. Check the setup markers — all by reading files in the repo:

- `docs/agents/project.md`, `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md` — present and filled in, or missing?
- `## Team` section inside `docs/agents/project.md` — present and filled, or a gap?
- An `## Agent skills` section in `CLAUDE.md` / `AGENTS.md` (note which of the two files exists)
- Seed files the skill set expects: `docs/specs/INDEX.md` (domain router) + `docs/specs/catalog/<domain>.md`, a glossary (`CONTEXT.md` or `CONTEXT-MAP.md`)
- `.skills/` and `.worktrees/` present in `.gitignore`

Then branch on what you found:

- **Already configured (fully or partly)** — this is a *fill-the-gaps* run, not a rebuild. List exactly what exists and what is missing or stale, show the user that summary, and offer to fill only the gaps. Walk only the Step 2 sections whose output is missing or that the user explicitly asks to change; leave everything already written untouched (the additive rule, Step 4).
- **Not configured** — go straight to the user-driven flow in Step 2. Do **not** guess the tracker from the git remote or a connected MCP server, and do not auto-detect anything the user should choose. Ask the user how they want to set the repo up, one decision at a time.

You may still read the repo's own manifests (lockfiles, `package.json` scripts, `Cargo.toml`, `pyproject.toml`, `Makefile`, test configs) to *pre-fill suggestions* in later steps — but reading a file in the repo is not the same as probing a service, and a pre-filled suggestion is never a decision made on the user's behalf.

**Done when:** you have classified the repo as configured / partly-configured / not-configured, listed any gaps, and presented that summary to the user.

## 2. Decide, one section at a time

Walk the twelve decisions below (A–L; I is optional project-docs; K is optional remote environments; L is optional catalog sync) strictly one at a time: give a two-or-three-sentence explainer (what this is, which skills consume it, what changes with each choice), state your recommendation with a one-line reason, then wait for the user's answer before moving on. Never dump all sections at once. Assume the user has not seen these concepts before.

### A. Issue tracker

Explainer: skills that read or write issues (`triage`, `publish-issues`, `plan-tasks` when publishing a plan, `land-branch`, `cut-release`) need to know where issues live and which commands touch them. Options: **github**, **gitlab**, **linear**, **local**, **other**. Recommend only from the repo's local git remote — a GitHub remote → github, a GitLab remote → gitlab, no remote → local — and always let the user overrule it. Do not probe a service or its auth to guess the tracker. Linear is a separate service and will not appear in `git remote`, so present it as an option and pick it whenever the user says the team lives in Linear, even if the code host is GitHub/GitLab.

**WHEN the tracker is chosen, read `issue-tracker-followups.md` beside this file and follow it exactly** — what each option means, the PR-surface, Publish unit, and Program sync follow-up questions, the write-scope table, and the IC-default rule all live there.

**Done when:** tracker choice, PR-surface (if applicable), Publish unit, Program sync, and Program write role are confirmed (or declined to defaults: feature + local + ic).

### B. Triage label mapping

**WHEN this decision runs, read `triage-label-mapping.md` beside this file and follow it exactly** — the canonical-roles table, the mapping proposal, label creation consent, and the linear-specific branch.

**Done when:** every canonical role maps to a confirmed label string.

### C. verify commands

Explainer: `test-first`, `prove-claim`, `build-in-waves`, and `cut-release` all run this repo's proof commands; they must be exact, not guessed. Confirm each, pre-filled from what you detected: typecheck, lint, unit tests, e2e/smoke, and the **single-test-file pattern** (the command shape for running one test file — the tight loop `test-first` lives in). **Done when:** each command has been confirmed by the user (or explicitly marked "none").

### D. Traceability (docs-only)

Explainer: requirement IDs live in `docs/specs/**`. The `audit-trace` check is **docs-only** — it greps requirements and task footers, not application tests. Do **not** require `/// REQ:`, `@CODE-N.M`, or IDs in test titles for consumer apps. Optional note in project.md: legacy annotations are ignored; do not add new ones. Confirm the specs directory path if non-default; skip inventing test-annotation tables. **Done when:** docs-only trace posture is confirmed (specs path; no mandatory consumer ID-in-test convention).

### E. release steps

Explainer: the `cut-release` skill executes an ordered list of project-specific commands — build, bundle, sign, publish — and it refuses to improvise them. Draft the ordered list from what you found (build scripts, packaging config) and confirm. Include the smoke-check command if one exists. **Done when:** the ordered release steps are confirmed (an empty list is a valid answer for libraries with no build).

### F. Docs layout

Explainer: spec and discovery skills read `docs/specs/`, `docs/adr/`, and the domain glossary; they need to know the shape. Confirm specs at `docs/specs/`, ADRs at `docs/adr/` (create the directories if missing), and glossary layout — **single-context** (one root `CONTEXT.md` — most repos) or **multi-context** (a root `CONTEXT-MAP.md` pointing at per-context `CONTEXT.md` files — typically monorepos). **Done when:** layout is confirmed.

### G. Project posture

Explainer: three standing facts about the project — its **delivery intent** (the quality bar the output must meet), its **lifecycle stage** (where it is in its life), and its **compat obligation** (who is already committed to the current schemas, endpoints, and formats). `frame-change` and `clarify-decisions` read them to right-size ceremony — compat obligation alone decides the migration / backward-compat / deprecation lens — and `interpret-session` / `deepen-codebase` reuse them so they never re-ask. They live in `docs/agents/project.md` and the user edits those lines directly as the project moves phase. Confirm these, pre-filled from repo signals — never invented:

- **Delivery intent** — Production / MVP / Run Spike / Research / Learning. The quality bar, not a release state: **Production** never means the project has shipped. Recommend from what the repo shows (a published package or cut-release workflow → Production; a bare greenfield spike → Run Spike); default **MVP** when unclear.
- **Lifecycle stage** — Idea / Early development / Active development / Cut Released / Scaling / Maintenance. Recommend from git signals (tags or a cut-release history → Cut Released; a young repo with few commits → Early development); default **Early development** when unclear.
- **Compat obligation** — None / Internal / External. Ask only when the repo contradicts the derivation the template's Project posture section gives from Lifecycle stage (pre-release → None, released → External): a published package, a versioned public API, or a deployed database under a pre-release lifecycle argues for a written override. Otherwise leave the line out and let the derivation stand — an unwritten line is the working default, not a gap.

**Done when:** delivery intent and lifecycle stage are confirmed by the user, and compat obligation is either confirmed as an override or deliberately left to the derivation.

### H. Team

**WHEN Decision H runs, read `team-inference.md` beside this file and follow it exactly** — why band packaging matters, the explainer for the user, the recommend defaults, local git / CODEOWNERS / AUTHORS / CONTRIBUTORS / package manifests only, **infer-then-confirm**.

| Thought | Reality |
|---|---|
| "I'll pull collaborators from `gh api`" | Local metadata only — no collaborator APIs |
| "Commit volume proves who the tech lead is" | Never invent titles; default `Contributor` until the user re-roles |
| "Empty git history — invent a solo developer" | Empty draft + ask; never invent names |
| "Write the draft and fix it later" | Confirm gate: no Team write without explicit confirm in this run |

**Done when:** the user has confirmed the roster (named and/or count form), optional ownership notes, and optional band override — or explicitly deferred Team (remain a gap).

### I. Project-docs layer (optional — default No)

**WHEN this decision is offered, read `project-docs-layer.md` beside this file and follow it exactly** — what the layer is, which skills consult it, and the migration offer when guidelines already exist elsewhere.

Recommendation: **No** unless this is a large, multi-feature project.

**Done when:** the layer is opted in or declined.

### J. Default PR base

Explainer: `land-branch` reads `Default PR base:` from `docs/agents/project.md` as the third rung of its base-resolution ladder — after an explicit invocation base and a base already recorded on an existing PR — so it stops asking once a trunk is on record. Offer `dev`, `staging`, `main`, and the repo's own local branch list as suggestions only; no value is pre-selected — the user always names the branch themselves. Recommendation: the repo's actual trunk branch (commonly `main`) — it is the branch `land-branch` already assumes unless told otherwise. Declining: if the user declines to choose, write no value at all and skip the Step 4 item for this field — `land-branch` then asks for the base on every invocation, which is what keeps the field genuinely optional under ARCH-2.

**Done when:** the user has confirmed a value, or has explicitly declined and no value will be written.

### K. Remote environments (optional — default skip if nothing is deployed)

**WHEN this decision is offered, read `remote-environments.md` beside this file and follow it exactly** — what to confirm per environment, the token rule, and the matching write step.

**Done when:** the table is confirmed, or explicitly skipped (`None — not deployed` / declined).

### L. Catalog sync (optional — default unset / full-triad behavior)

**WHEN this decision is offered, read `catalog-sync-choice.md` beside this file and follow it exactly** — what thin-catalog sync means, the three option definitions, and the write step (Step 4, item 11). Guide for the user: `docs/guide/skills/catalog-sync.md`.

| Thought | Reality |
|---|---|
| "Everyone should be index-only now" | Opt-in only; default unset preserves current repos |
| "I'll add the gitignore without saying index-only" | Snippet only when L=`index-only` and user confirmed |

**Done when:** catalog sync value confirmed, or explicitly left unset.

## 3. Draft and confirm

Show the user, before writing anything:

- the three `docs/agents/*.md` files' contents (including confirmed `## Team` when Decision H was confirmed)
- the `## Agent skills` block destined for CLAUDE.md/AGENTS.md

Let them edit. **Done when:** the user approves the drafts.

## 4. Write

**The additive rule: existing files are edited in place, never clobbered.** If a target file already exists, merge your content into it and preserve everything the user wrote.

1. Write `docs/agents/project.md`, `docs/agents/issue-tracker.md`, and `docs/agents/triage-labels.md`, seeded from `templates/agents/project.md`, `templates/agents/issue-tracker.md`, and `templates/agents/triage-labels.md`. In the issue-tracker file keep only the chosen tracker's operations section, record the PR-surface answer, and fill **Publish unit**, **Program sync**, **Program write role**, and **Close linkage** from Decision A (defaults: `feature` / `local` / `ic` / tracker-native close syntax).
2. If `docs/specs/INDEX.md` is missing, create it from `templates/specs-INDEX.md` **and** seed `docs/specs/catalog/app.md` from `templates/specs-catalog-domain.md` (replace `<Domain>` with `App`). If INDEX exists but is a flat Code table, name `/map-features` Domain boundary migrate — do not invent shards silently.

3. If the glossary is missing, create `CONTEXT.md` from `templates/CONTEXT.md` (or a `CONTEXT-MAP.md` for multi-context, per the user's answer).
4. Fill the **Project posture** section of `docs/agents/project.md` with the confirmed delivery intent and lifecycle stage (decision G), replacing the template placeholders. Write a `- **Compat obligation:** \`<value>\`` line only when decision G confirmed an override; when it left the derivation standing, delete the placeholder line so the derivation applies. (Additive: if the section already carries real values, update only what the user changed.) If decision L confirmed **index-only** or **full-triad**, set `- **Catalog sync:** \`<value>\`` in the same section (additive). If L left unset, write no Catalog sync line.
5. Fill **`## Team`** from the confirmed Decision H content (roster, ownership notes, optional band override), merging into the template shape from `templates/agents/project.md`. Replace only the Team section's confirmed fields; do not clobber other sections. If the user deferred Team, leave the section as template placeholders or omit until a fill-the-gaps run.
6. **If the project-docs layer was opted in (decision I):** seed `docs/product/vision.md`, `docs/architecture/INDEX.md`, and `docs/product/guidelines.md` from `templates/product-vision.md`, `templates/architecture-INDEX.md`, and `templates/product-guidelines.md` (additive, per the rule above). If migrating, move the existing engineering rules into `docs/product/guidelines.md` and leave a pointer in `docs/agents/project.md`. If the layer was declined, skip this — write none of these files.
7. Add the `## Agent skills` block. It lives in exactly **one** canonical file; any second file is a thin pointer, never a copy of the block.
   - **Neither `CLAUDE.md` nor `AGENTS.md` exists** (the default): make `AGENTS.md` canonical (it holds the block) and write a short `CLAUDE.md` whose entire body points at `AGENTS.md` — so Claude Code finds instructions by its native filename without duplicating them. Do not ask which to create; this pattern serves both.
   - **Only one exists:** that file is canonical — add or update the block in it. If it is `AGENTS.md` and Claude Code is a target, also add the `CLAUDE.md` pointer. If it is `CLAUDE.md`, leave it canonical — do not demote it to a pointer or create a competing `AGENTS.md`.
   - **Both exist:** put the block in whichever already carries real agent instructions; make the other a pointer only if it is not already substantive. Never place the block in both.
   - If an `## Agent skills` section already exists in the canonical file, update it in place — never append a duplicate, never touch surrounding sections.

   The `CLAUDE.md` pointer, when you create one, is seeded verbatim from `templates/claude-md-pointer.md`.

The block (include the project-docs bullet only if decision I was Yes) is seeded verbatim from `templates/agent-skills-block.md`.

8. Ensure the local working dirs are git-ignored: the skills' scratch artifacts — `build-in-waves`'s ledger and briefs, and the scan/review digests the spec skills write — live under `.skills/`, and isolated workspaces under `.worktrees/` (the same parent `isolate-workspace` uses); neither belongs in version control. Idempotently, for each pattern: `grep -qxF '.skills/' .gitignore 2>/dev/null || printf '.skills/\n' >> .gitignore` (same for `.worktrees/`), then stage `.gitignore`. Do not add a `.isolate-workspace/` line — that was the old parallel parent. Leave an existing `.isolate-workspace/` ignore in place (additive). (A line-presence check, not `git check-ignore` — a trailing-slash pattern only matches an *existing* directory, so `check-ignore` would re-append before the dir exists.)
9. If decision J (Default PR base) was confirmed, add `- **Default PR base:** \`<branch>\`` to the **Project posture** section of `docs/agents/project.md`, under the additive rule above — merge in, never clobber a value the user already set. If the user declined decision J, write nothing: leave the field absent so `land-branch` asks per invocation.
10. Follow the write step in `remote-environments.md` for decision K.
11. Follow the write step in `catalog-sync-choice.md` for decision L (index-only gitignore append).

**Done when:** all files are written, `.skills/` and `.worktrees/` are git-ignored, index-only gitignore applied only when L=`index-only`, and `git status` shows only the expected additions/edits.

## 5. Offer the session-start hook

**WHEN this step runs, read `optional-offers.md` beside this file and follow it exactly** — the vendored (never absolute-path) session-start hook install and the Context7 MCP recommendation.

**Done when:** both offers — the session-start hook and the Context7 MCP recommendation — have an explicit yes/no, and any yes is implemented (the hook installed, or the Context7 note written to `docs/agents/project.md`).

## 6. Prove the configuration actually works — GATE

Confirmed-with-the-user is not the same as works-in-this-project. Commands were pre-filled from what you detected; a wrong manifest path, a missing script, or a tool that is not installed will surface as a mid-task failure in `test-first`, `prove-claim`, or `cut-release` weeks from now. Prove them now, while you own the context. This is the discipline of the `prove-claim` skill applied to the config you just wrote: run the command, read the output, believe the output — not the config.

Run each configured verify command fresh and classify the result. The distinction that matters is **wiring vs content**:

- **Wiring failure** — the command could not run as written: "command not found" / exit 127, "missing script", "no such file or directory", a bad `--manifest-path` or unknown flag, an uninstalled tool. **This is a config bug you must fix**: re-detect, correct `docs/agents/project.md`, and re-run until it is gone. Setup is not done while any command is mis-wired.
- **Content failure** — the tool ran correctly but reported problems (type errors, lint warnings, failing tests). The command is wired right; the repo has pre-existing issues. Record these for the user; they do **not** block setup.
- **Pass** — wired and green.

Be cost-aware — do not run the whole suite to prove wiring:

- Typecheck and lint: run in full (bounded).
- Unit/e2e runners: prove the runner resolves its config cheaply — run the **single-test-file pattern** from `project.md` against one existing test file, or the runner's collect-only/list mode. Never trigger a full e2e run during setup; state that the full run is the user's to do later.
- Audit Trace check: run it (REQUIRED SUB-SKILL: use `audit-trace`) and confirm it reports a clean finding set — zero requirements is a valid clean state. The check is `grep`/`git` over `docs/specs/` (and optional architecture), not application test trees.
- If you installed the session-start hook, execute `.claude/hooks/session-start.sh` and confirm it prints one line of valid JSON.
- If the tracker is a remote service (`github` / `gitlab` / `linear`), prove it is reachable and authenticated with **one read-only call** — `gh issue list` / `glab issue list`, or for Linear a single MCP list call (or a minimal `issues` GraphQL query). This verifies the tracker the *user already chose*; it is not the setup-time detection Step 1 forbids — the choice is made, and this call only proves it works. A missing CLI, an unauthenticated session, or a disconnected or unauthenticated MCP server is a wiring failure; it would otherwise stay hidden until `triage` fails weeks later. `local` and `other` need no reachability check.

Report a small table: each command → wired? → passed / failed / pre-existing.

**Done when:** every configured command is proven **wired** (no wiring failures remain), the audit-trace check runs clean, the hook (if installed) fires, the configured tracker answers a read-only call, and any content failures are listed for the user.

## 7. Finish

Tell the user setup is complete, which skills now read the config, that the prove-claim table shows what is wired vs pre-existing, and that `docs/agents/*.md` can be edited directly later — re-running this wizard is only needed to switch trackers or start over.
