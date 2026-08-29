# Adopting the skill set

## Install

**Claude Code / Grok** — plugin (slug `jdk`, picker label Engineer Pack). Do not also flatten Engineer Pack into `~/.claude/skills/` on the same machine.

```text
/plugin marketplace add jayden-dang/skills
/plugin install jdk@jayden-dang-skills
```

Grok: `grok plugin marketplace add jayden-dang/skills` then `grok plugin install jdk --trust`.

**Codex** — same GitHub marketplace, Codex CLI:

```bash
codex plugin marketplace add jayden-dang/skills
codex plugin add jdk@jayden-dang-skills
```

**Kimi Code CLI** — plugin (slug `jdk`). Skills invoke as `/skill:<name>` (not `/jdk:<name>`). Do not also flatten Engineer Pack into `~/.kimi-code/skills/` or `~/.agents/skills` on the same machine.

```text
/plugins install https://github.com/jayden-dang/skills
```

Then `/reload` or a new session. Optional catalog: `/plugins marketplace` with `.kimi-plugin/marketplace.json`.

**OpenCode** — this repo ships `opencode.json` that points at Engineer Pack category folders (not Personal Pack). Clone and open the repo, or copy those `skills` paths into `~/.config/opencode/opencode.json` against a local clone. Invoke via the `skill` tool (`frame-change`), not `/jdk:`. Do not flatten this tree into `~/.agents/skills/` if OpenCode would then see category folders as skill IDs.

**Cursor and other flatten agents** — skill folder names unchanged (`/frame-change`, not `/jdk:frame-change`):

```bash
npx skills@latest add jayden-dang/skills --copy
```

Update: plugin manager / `grok plugin update jdk` on Claude and Grok; reinstall the GitHub URL on Kimi; `npx skills@latest update` on flatten installs.

**Dev mode** — for working on this repo, so `git pull` updates the skills in place. Clone it and symlink the engineering skill folders into `~/.claude/skills` (flatten — do not combine with a `jdk` plugin install on the same Claude/Grok machine):

```bash
for cat in meta discovery spec execution review acceptance craft ship track project setup; do
  for d in skills/$cat/*/; do ln -sfn "$PWD/$d" ~/.claude/skills/$(basename "$d"); done
done
```

A blind `skills/*/*/` loop would also install Personal OS.

## Then configure the repo, once

Which entry point depends on what you are standing in.

| Situation | Run |
|---|---|
| An empty (or nearly empty) directory | `/bootstrap-repo` |
| An existing or mature repo | `/configure-repo` |

`bootstrap-repo` will detect that you are *not* in a greenfield directory and redirect you to `configure-repo` rather than scaffolding on top of a real project. It ends by handing off to `configure-repo` anyway, so the two compose.

Neither can be auto-invoked. Both carry `disable-model-invocation: true`; you run them.

## What `bootstrap-repo` does

Bootstraps a greenfield repo to a **verified baseline**: a skeleton where every quality tool is wired and demonstrably working, so the first feature starts from green.

Its step 0 is a gate. It resolves the target directory, inspects it itself (never asks you what is in it), and classifies:

| Target state | Action |
|---|---|
| Does not exist, or holds only `.git` / `README` / `LICENSE`, and no manifest | **Greenfield** — proceed |
| A new, empty subdirectory inside an existing repo | **Subpackage** — proceed, skipping the root-touching steps |
| Holds a manifest or many tracked files | **Not greenfield — stop and redirect** |

Then it grills the stack one decision at a time (language, framework, test runner, formatter, package manager, layout, license), scaffolds, and runs `prove-claim` on the result. The deliverable is the harness, proven by **one passing example test** — nothing more.

Its completion criterion: from the repo root, one command installs dependencies and one command runs the verify suite green. It states both commands explicitly.

## What `configure-repo` does

A seven-step conversation, not a script. It explores first, presents what it found, then decides **one thing at a time** with you — each with a two-or-three-sentence explainer, a recommendation, and a one-line reason.

### The decisions (A–I)

**A. Issue tracker.** `github` (via `gh`), `gitlab` (via `glab`), `linear` (via a connected MCP server or the GraphQL API), `local` (markdown under `.scratch/`), or `other` (freeform prose). It recommends from what it found — but Linear will never appear in `git remote`, so it offers Linear whenever you say the team lives there.

For GitHub and GitLab it asks a follow-up: **are external pull requests a request surface?** Open-source repos often receive feature requests as PRs. If yes, `triage` pulls them into the same queue.

**B. Triage label mapping.** Seven canonical roles — five states and two categories:

| Role | Meaning |
|---|---|
| `needs-triage` | awaiting evaluation |
| `needs-info` | waiting on the reporter |
| `ready-for-agent` | fully specified; an agent can pick it up cold |
| `ready-for-human` | needs human judgment or access |
| `wontfix` | will not be actioned |
| `bug` | something is broken |
| `enhancement` | new capability or improvement |

Each maps to the label string *this repo actually uses*, so `triage` never creates duplicates. Labels that do not exist yet are created only with your explicit consent.

**C. verify commands.** typecheck, lint, unit, e2e — plus the **single-test-file pattern**, the command shape for running one test file. That is the tight loop `test-first` lives in.

**D. Test annotation conventions.** One per test layer, chosen to be greppable and to match the repo's frameworks. This is what lets the audit-trace check find requirement IDs in tests.

**E. release steps.** The ordered, project-specific commands `cut-release` executes and refuses to improvise. An empty list is a valid answer for a library with no build.

**F. Docs layout.** Specs at `docs/specs/`, ADRs at `docs/adr/`, and a glossary that is either single-context (one root `CONTEXT.md`) or multi-context (a `CONTEXT-MAP.md` pointing at per-context files, typically a monorepo).

**G. Project posture.** Delivery intent and lifecycle stage in `docs/agents/project.md` — how carefully to build right now.

**H. Team composition.** Roster and optional ownership notes in `docs/agents/project.md` `## Team`, drafted from local git/CODEOWNERS/manifests then confirmed. Skills package collaboration by Solo/Small/Multi **band** without changing process gates.

**I. Project-docs layer (optional).** Product vision, architecture invariants, engineering guidelines — default No.

### What it writes

`docs/agents/project.md` (including posture and Team), `issue-tracker.md`, and `triage-labels.md`; `docs/specs/INDEX.md` if missing; `CONTEXT.md` if missing; and an `## Agent skills` block into **exactly one canonical file** — `AGENTS.md` by default, with a short `CLAUDE.md` pointing at it, so Claude Code finds instructions by its native filename without duplicating them.

It writes markdown only — no scripts, no linters, no CI, no git hooks land in the repo. It also ensures `.skills/` and `.worktrees/` are git-ignored.

**The additive rule governs everything:** existing files are edited in place, never clobbered.

### The one opt-in

Offered, and applied only on a yes: the **session-start hook** — copied into the repo at `.claude/hooks/session-start.sh` and referenced via `$CLAUDE_PROJECT_DIR`, never an absolute path (which would break on every other machine). It is dependency-free and re-injects the [`gate-session`](../skills/gate-session.md) gate on `startup | clear | compact`.

A hard headless gate — running the audit-trace check in CI, or a git pre-push hook — is optional and team-specific. It lives outside the default path, so `configure-repo` does not wire one; the audit-trace check runs inside `prove-claim` and `cut-release` regardless.

### Step 6 is the step that matters

> Confirmed-with-the-user is not the same as works-in-this-project.

Commands were pre-filled from what the agent *detected*. A wrong manifest path, a missing script, or an uninstalled tool will otherwise surface as a mid-task failure in `test-first` or `cut-release`, weeks from now.

So every configured command gets run, and the result classified:

| Result | Meaning | Blocks setup? |
|---|---|---|
| **Wiring failure** | the command could not run as written — exit 127, missing script, bad `--manifest-path`, uninstalled tool | **Yes.** Re-detect, correct `project.md`, re-run |
| **Content failure** | the tool ran correctly and reported problems — type errors, lint warnings, failing tests | No. The repo has pre-existing issues; they get recorded |
| **Pass** | wired and green | No |

It is cost-aware: typecheck and lint run in full; test runners are proven cheaply via the single-test-file pattern or a collect-only mode, never a full e2e run. And a remote tracker gets one read-only call to prove it is reachable and authenticated. The audit-trace check needs nothing wired — the agent drives it with `grep`/`git` — so there is no command to prove; zero requirements is already a valid clean state.

You get a table: each command → wired? → passed / failed / pre-existing.

## Adopting incrementally

You do not have to spec the whole codebase. The skill set works on a per-feature basis, and the audit-trace check treats zero requirements as a clean state.

**The fastest first pass.** You do not have to answer every question deeply on day one. Accept each of `configure-repo`'s recommended defaults, choose the `local` markdown tracker if you have no strong preference, and decline the session-start hook for now. That gets you a working trace spine and detected verify commands with the fewest decisions — enough to take one feature through the chain. Re-run `/configure-repo` later to add the hook once the workflow has earned its place; it is additive and never clobbers your earlier answers.

A reasonable path:

1. Run `/configure-repo`. Take the session-start hook opt-in.
2. Take the **next** feature through the full chain — `frame-change` → the triad → `build-in-waves`. One feature code, one spec folder.
3. Take the next **bug** through `root-cause` and let it write its tier-1 mini-spec into `docs/specs/fixes.md`.
4. Leave the existing code alone. Untraced code is not an error; only an *implemented requirement without a covering test* is.

The spine grows from the edges inward. Each new feature registers its code in `docs/specs/INDEX.md` (and ideally a `**Files:**` block) as its spec lands, so `frame-change` + **`load-subgraph`** find more prior art with every one. On a brownfield repo with thin OWNS coverage, run [`/map-features`](../skills/map-features.md) to backfill.

## Afterwards

`docs/agents/*.md` can be edited directly. Re-running `/configure-repo` is only needed to switch trackers or start over.

## See also

- [When to use it](../methodology/when-to-use.md) — and when not to
- [`configure-repo`](../skills/configure-repo.md) — the full wizard
- [`bootstrap-repo`](../skills/bootstrap-repo.md) — the greenfield path
- [Troubleshooting](troubleshooting.md) — when something does not fire
