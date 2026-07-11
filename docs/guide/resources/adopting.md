# Adopting the skill set

## Install

```bash
npx skills@latest add jayden-dang/skills
```

Or install it as a Claude Code plugin — this repo is a valid plugin, shipping the skills plus a `SessionStart` hook that keeps the skill-check gate alive across `/clear` and compaction.

**Dev mode**, so `git pull` updates the skills in place:

```bash
./scripts/link-skills.sh
```

This symlinks the skill directories into `~/.claude/skills`.

## Then configure the repo, once

Which entry point depends on what you are standing in.

| Situation | Run |
|---|---|
| An empty (or nearly empty) directory | `/scaffold-project` |
| An existing or mature repo | `/setup-repo` |

`scaffold-project` will detect that you are *not* in a greenfield directory and redirect you to `setup-repo` rather than scaffolding on top of a real project. It ends by handing off to `setup-repo` anyway, so the two compose.

Neither can be auto-invoked. Both carry `disable-model-invocation: true`; you run them.

## What `scaffold-project` does

Bootstraps a greenfield repo to a **verified baseline**: a skeleton where every quality tool is wired and demonstrably working, so the first feature starts from green.

Its step 0 is a gate. It resolves the target directory, inspects it itself (never asks you what is in it), and classifies:

| Target state | Action |
|---|---|
| Does not exist, or holds only `.git` / `README` / `LICENSE`, and no manifest | **Greenfield** — proceed |
| A new, empty subdirectory inside an existing repo | **Subpackage** — proceed, skipping the root-touching steps |
| Holds a manifest or many tracked files | **Not greenfield — stop and redirect** |

Then it grills the stack one decision at a time (language, framework, test runner, formatter, package manager, layout, license), scaffolds, and runs `verify` on the result. The deliverable is the harness, proven by **one passing example test** — nothing more.

Its completion criterion: from the repo root, one command installs dependencies and one command runs the verify suite green. It states both commands explicitly.

## What `setup-repo` does

A seven-step conversation, not a script. It explores first, presents what it found, then decides **one thing at a time** with you — each with a two-or-three-sentence explainer, a recommendation, and a one-line reason.

### The six decisions

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

**C. Verify commands.** typecheck, lint, unit, e2e — plus the **single-test-file pattern**, the command shape for running one test file. That is the tight loop `tdd` lives in.

**D. Test annotation conventions.** One per test layer, chosen to be greppable and to match the repo's frameworks. This is what lets `check-trace` find requirement IDs in tests.

**E. Release steps.** The ordered, project-specific commands `release` executes and refuses to improvise. An empty list is a valid answer for a library with no build.

**F. Docs layout.** Specs at `docs/specs/`, ADRs at `docs/adr/`, and a glossary that is either single-context (one root `CONTEXT.md`) or multi-context (a `CONTEXT-MAP.md` pointing at per-context files, typically a monorepo).

### What it writes

`docs/agents/project.md`, `issue-tracker.md`, and `triage-labels.md`; `docs/specs/INDEX.md` if missing; `CONTEXT.md` if missing; and an `## Agent skills` block into **exactly one canonical file** — `AGENTS.md` by default, with a short `CLAUDE.md` pointing at it, so Claude Code finds instructions by its native filename without duplicating them.

It also vendors the two linters via `vendor_linters.py`, and ensures `.skills/` and `.worktrees/` are git-ignored.

**The additive rule governs everything:** existing files are edited in place, never clobbered.

### The three opt-ins

Each is offered; each acts only on a yes.

1. **Session-start hook** — vendored into the repo at `.claude/hooks/session-start.sh` and referenced via `$CLAUDE_PROJECT_DIR`, never an absolute path (which would break on every other machine).
2. **Trace and graph checks in CI** — appended to an *existing* workflow. No CI workflow exists? It says so and skips; authoring one is out of scope.
3. **Git verify hooks** — `pre-commit` gets the fast gates, `pre-push` gets tests plus both linters. If you already run a hook manager, the commands go into that one.

### Step 6 is the step that matters

> Confirmed-with-the-user is not the same as works-in-this-project.

Commands were pre-filled from what the agent *detected*. A wrong manifest path, a missing script, or an uninstalled tool will otherwise surface as a mid-task failure in `tdd` or `release`, weeks from now.

So every configured command gets run, and the result classified:

| Result | Meaning | Blocks setup? |
|---|---|---|
| **Wiring failure** | the command could not run as written — exit 127, missing script, bad `--manifest-path`, uninstalled tool | **Yes.** Re-detect, correct `project.md`, re-run |
| **Content failure** | the tool ran correctly and reported problems — type errors, lint warnings, failing tests | No. The repo has pre-existing issues; they get recorded |
| **Pass** | wired and green | No |

It is cost-aware: typecheck and lint run in full; test runners are proven cheaply via the single-test-file pattern or a collect-only mode, never a full e2e run. `check-trace` must execute and exit 0 (zero requirements is a valid clean state). `check-graph --harvest` must write `GRAPH.md`, and `--verify` must exit 0 — because an unrunnable graph linter makes `brainstorm` and `code-review` skip their duplication checks forever, *which looks exactly like "no overlapping features"*. And a remote tracker gets one read-only call to prove it is reachable and authenticated.

You get a table: each command → wired? → passed / failed / pre-existing.

## Adopting incrementally

You do not have to spec the whole codebase. The skill set works on a per-feature basis, and `check-trace` treats zero requirements as a clean state.

**The fastest first pass.** You do not have to answer every question deeply or take every opt-in on day one. Accept each of `setup-repo`'s recommended defaults, choose the `local` markdown tracker if you have no strong preference, and decline the three opt-ins (session hook, CI, git hooks) for now. That gets you a working trace spine and detected verify commands with the fewest decisions — enough to take one feature through the chain. Re-run `/setup-repo` later to add the hook, CI, and git hooks once the workflow has earned its place; it is additive and never clobbers your earlier answers.

A reasonable path:

1. Run `/setup-repo`. Take the CI and hook opt-ins.
2. Take the **next** feature through the full chain — `brainstorm` → the triad → `execute-plan`. One feature code, one spec folder.
3. Take the next **bug** through `debug` and let it write its tier-1 mini-spec into `docs/specs/fixes.md`.
4. Leave the existing code alone. Untraced code is not an error; only an *implemented requirement without a covering test* is.

The spine grows from the edges inward. `check-graph --harvest` will pick up each new feature's surface as its spec lands, and the dedup check gets more useful with every one.

## Afterwards

`docs/agents/*.md` can be edited directly. Re-running `/setup-repo` is only needed to switch trackers or start over — and when you do, it checks the vendored linters for drift first and offers to update them.

## See also

- [When to use it](../methodology/when-to-use.md) — and when not to
- [`setup-repo`](../skills/setup-repo.md) — the full wizard
- [`scaffold-project`](../skills/scaffold-project.md) — the greenfield path
- [Troubleshooting](troubleshooting.md) — when something does not fire
