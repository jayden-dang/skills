# `setup-repo`

> Configure a repository once, so every other skill reads its answers instead of guessing.

|  |  |
|---|---|
| **Bucket** | setup |
| **Invocation** | user-invoked — run as `/setup-repo`; no skill may auto-invoke it, others only name it for the user to run |
| **Reads** | `git remote`, `CLAUDE.md` / `AGENTS.md`, existing lockfiles and CI, tracker labels, `docs/agents/` |
| **Writes** | `docs/agents/project.md`, `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, seed spec files, the `## Agent skills` block, the opt-in session-start hook |
| **Calls** | the discipline of [`verify`](verify.md) (Step 6 gate) |
| **Called by** | nothing — it is user-invoked; [`scaffold-project`](scaffold-project.md) redirects the user here when a directory is not greenfield |

## When it fires

Run it once against a repository that has not been configured for the skill set yet — no `docs/agents/` directory, verify commands unknown, triage labels unmapped. Run it again later only to change the tracker, labels, verify commands, or release steps. It is the entry point for adopting the set into an existing or mature repo, and it is where [`scaffold-project`](scaffold-project.md) sends the user when the target directory turns out to hold a real project.

Because `disable-model-invocation` is set, no other skill can start it automatically. Skills that depend on its output — [`triage`](triage.md), [`release`](release.md), [`tdd`](tdd.md), [`verify`](verify.md) — name it so the user runs it themselves.

It is a conversation, not a script: explore, present what you found, decide one thing at a time, then write. It has seven steps, and skipping one — an unconfigured tracker, or the Step 6 verification gate never run — is the common failure. The skill opens a todo per step and completes them in order, checking each off only when its **Done when** is met.

## The seven steps

### 1. Explore

Before asking anything, learn the repo's starting state: `git remote -v` (GitHub, GitLab, or none), whether a Linear MCP server is connected or `LINEAR_API_KEY` is set, which of `CLAUDE.md` / `AGENTS.md` exists and whether either already carries an `## Agent skills` section, whether `docs/agents/` has run here before, the spec and glossary directories, the package manager and toolchain, the test runners and CI, and existing tracker labels. Done when a short findings summary is presented — what exists, what is missing, what can be pre-filled.

### 2. Decide, one section at a time

Six decisions, walked strictly one at a time: a two-or-three-sentence explainer, a recommendation with a one-line reason, then a wait for the user's answer. The skill assumes the user has never seen these concepts and never dumps all sections at once.

- **A. Issue tracker.** Where issues live and which commands touch them, for `triage`, `write-plan` when publishing tasks, and `release`. Options are **github** (`gh`), **gitlab** (`glab`), **linear** (a connected MCP server, preferred, or the GraphQL API — for teams that track work in Linear rather than the code host), **local** (markdown files under `.scratch/<feature>/` each carrying a `Status:` line), and **other** (freeform prose describing the workflow). Linear will not appear in `git remote`, so it is offered whenever the user says the team lives there even if the host is GitHub or GitLab. A github/gitlab follow-up asks whether external pull requests are a request surface; if yes, `triage` pulls external PRs into the same queue. Skipped entirely for linear/local/other.
- **B. Triage label mapping.** `triage` moves issues through canonical roles but must apply this repo's actual label strings or it creates duplicates. The seven canonical roles are five states and two categories:

  | Role | Meaning |
  |---|---|
  | needs-triage | awaiting evaluation |
  | needs-info | waiting on the reporter |
  | ready-for-agent | fully specified; an agent can pick it up cold |
  | ready-for-human | needs human judgment or access |
  | wontfix | will not be actioned |
  | bug | something is broken |
  | enhancement | new capability or improvement |

  The repo's existing labels are shown next to the roles and a mapping proposed (default: each role's string equals its name). Missing labels are created only with explicit consent. For local trackers the role names are the vocabulary. For linear the team's existing workflow states and labels are listed first, then state roles are mapped to workflow states and category roles to Linear labels. Done when every role maps to a confirmed label string.
- **C. Verify commands.** The proof commands `tdd`, `verify`, `execute-plan`, and `release` run — exact, not guessed. Confirm typecheck, lint, unit tests, e2e/smoke, and the **single-test-file pattern** (the tight loop `tdd` lives in), plus the test locations and any ignore list the [`trace`](trace.md) check reads. Done when each is confirmed or explicitly marked "none".
- **D. Test annotation conventions.** Every test carries the requirement ID it covers, and the [`trace`](trace.md) check greps for those IDs, so the convention must be greppable and match the repo's frameworks — an e2e tag like `{ tag: ['@CODE-N.M'] }`, a unit annotation or the ID in the test name, a `/// REQ: CODE-N.M` doc comment for compiled languages. Done when every test layer has a confirmed convention.
- **E. Release steps.** `release` executes an ordered list of project-specific commands — build, bundle, sign, publish — and refuses to improvise them. Draft the list from the build scripts and packaging config found, including any smoke-check command. Done when the ordered steps are confirmed; an empty list is valid for a library with no build.
- **F. Docs layout.** Confirm specs at `docs/specs/` and ADRs at `docs/adr/` (creating the directories if missing), and the glossary layout: **single-context** (one root `CONTEXT.md`, most repos) or **multi-context** (a root `CONTEXT-MAP.md` pointing at per-context `CONTEXT.md` files, typically monorepos). Done when the layout is confirmed.

### 3. Draft and confirm

Before writing anything, show the user the three `docs/agents/*.md` files' contents and the `## Agent skills` block destined for `CLAUDE.md` / `AGENTS.md`, and let them edit. Done when the drafts are approved.

### 4. Write

**The additive rule: existing files are edited in place, never clobbered** — if a target already exists, content is merged and everything the user wrote is preserved. The step writes `docs/agents/project.md`, `docs/agents/issue-tracker.md`, and `docs/agents/triage-labels.md` from the matching `templates/agents/*` seeds, keeping only the chosen tracker's operations section and recording the PR-surface answer; creates `docs/specs/INDEX.md` if missing; and creates the glossary (`CONTEXT.md` or `CONTEXT-MAP.md`) if missing.

The `## Agent skills` block lives in exactly **one** canonical file; any second file is a thin pointer, never a copy. When neither `CLAUDE.md` nor `AGENTS.md` exists (the default), `AGENTS.md` becomes canonical and a short `CLAUDE.md` points at it. When only one exists it is canonical. When both exist the block goes in whichever already carries real agent instructions, and never in both; an existing `## Agent skills` section is updated in place, never duplicated. Finally the step git-ignores `.skills/` (the `execute-plan` ledger and scan digests) and `.worktrees/` idempotently by line-presence check. Done when all files are written, both dirs are ignored, and `git status` shows only expected changes.

### 5. Offer the session-start hook

One optional install — offered, acted on only with a yes:

**Session-start hook.** If the set was installed without plugin hook support, a `SessionStart` hook (matcher `startup|clear|compact`) keeps the skill-usage gate alive across `/clear` and compaction. The hook is copied into the repo — `templates/session-start.sh` to `.claude/hooks/` and `chmod +x`'d, then referenced in `.claude/settings.json` via `$CLAUDE_PROJECT_DIR`, never an absolute path (which would break on any other machine). Merged additively into any existing `SessionStart` block.

The set installs nothing else — no scripts, no CI steps, no git hooks. The [`trace`](trace.md) check is a set of `grep`/`git` passes an agent runs directly, so there is nothing to install and nothing to wire; `verify` and `release` run it inline when they need it. A repo that wants a hard headless gate can add its own CI step, but authoring one is out of scope here.

Done when the offer has an explicit yes/no and a yes is implemented.

### 6. Prove the configuration actually works — GATE

This is the step most likely to be skipped, and it is not optional. Confirmed-with-the-user is not the same as works-in-this-project: commands were pre-filled from detection, so a wrong manifest path, a missing script, or an uninstalled tool would otherwise surface as a mid-task failure in `tdd`, `verify`, or `release` weeks later. The gate applies the discipline of [`verify`](verify.md) to the config just written — run the command, read the output, believe the output, not the config.

Each configured verify command is run fresh and classified. The distinction that carries the whole step is **wiring versus content**:

- **Wiring failure** — the command could not run as written: command-not-found / exit 127, a missing script, no-such-file, a bad `--manifest-path` or unknown flag, an uninstalled tool. **This is a config bug that must be fixed** — re-detect, correct `docs/agents/project.md`, re-run until gone. Setup is not done while any command is mis-wired.
- **Content failure** — the tool ran correctly but reported problems: type errors, lint warnings, failing tests. The command is wired right; the repo has pre-existing issues. These are recorded for the user and do **not** block setup.
- **Pass** — wired and green.

The gate is cost-aware. Typecheck and lint run in full. Test runners are proven cheaply — the single-test-file pattern against one existing file, or collect-only mode — never a full e2e run during setup. The [`trace`](trace.md) check needs no wiring proof — it is a set of `grep`/`git` passes, not an installed tool — so the gate instead confirms its inputs: the specs directory exists and the test globs and ignore list from Decision C are recorded (with zero requirements the check is trivially clean). An installed session-start hook is executed and must print one line of valid JSON. A remote tracker (github / gitlab / linear) is proven reachable and authenticated with one read-only call; local and other need no check. The step reports a small table: each command → wired? → passed / failed / pre-existing. Done when every command is proven wired, the trace inputs are recorded, any installed hook fires, the tracker answers, and content failures are listed.

### 7. Finish

Tell the user setup is complete, which skills now read the config, that the verify table shows what is wired versus pre-existing, and that `docs/agents/*.md` can be edited directly later — re-running the wizard is only needed to switch trackers or start over.

## Worked example

Adopting the set into an existing TypeScript + Vitest library with a GitHub remote and no prior `docs/agents/`.

**Explore.** `git remote -v` shows a GitHub origin; no Linear signal. `AGENTS.md` is absent, `CLAUDE.md` absent. `pnpm-lock.yaml` and a `package.json` with `test`, `lint`, `typecheck` scripts. A `.github/workflows/ci.yml` exists. `gh label list` returns the default GitHub label set.

**Decide.** A is **github**; external PRs are a request surface, so `triage` will pull them in. B maps the five state roles to new labels (offered for creation with consent) and `bug`/`enhancement` to the existing GitHub defaults. C confirms `pnpm exec tsc -b`, `pnpm lint`, `pnpm test`, no e2e, single-file pattern `pnpm exec vitest run <path>`. D records a single Vitest layer using `annotate('CODE-N.M', 'requirement')`. E is an empty release list — a library with no bundling. F is single-context `CONTEXT.md`.

**Write.** The three `docs/agents/*.md` files land, the issue-tracker file keeps only the github section, `AGENTS.md` is created canonical with the `## Agent skills` block and a thin `CLAUDE.md` pointer, and `.skills/` and `.worktrees/` are added to `.gitignore`. Nothing is copied into the repo but markdown config.

**Opt-in.** The user accepts the session-start hook — `templates/session-start.sh` copied into `.claude/hooks/` and referenced in `.claude/settings.json` via `$CLAUDE_PROJECT_DIR`.

**Prove — GATE.** `pnpm exec tsc -b` and `pnpm lint` run in full: lint reports three pre-existing warnings — a **content** failure, recorded not blocking. `pnpm exec vitest run` against one existing spec resolves the config: pass. The [`trace`](trace.md) check needs no wiring — its inputs are recorded (specs at `docs/specs/`, the Vitest test glob), and with zero requirements it is trivially clean. `gh issue list` returns cleanly, proving the tracker is authenticated. The table shows every command wired, the three lint warnings flagged as pre-existing.

## Why it is written the way it is

The whole skill is built around a single failure mode: a config that reads plausible but does not run. Everything downstream — `tdd`'s tight loop, `verify`'s completion claims, `release`'s ordered steps, `triage`'s label writes — trusts these files blindly, so a wrong path stays invisible until it fails far from the context that could fix it. Hence the one-decision-at-a-time conversation (a dumped questionnaire gets rubber-stamped), the additive write rule (never clobber the user's own instructions), and above all the Step 6 gate, which refuses to call setup done on the strength of what was confirmed rather than what was proven to run. The wiring-versus-content split is the load-bearing idea: it lets the gate be strict about the one thing setup controls (wiring) without demanding the user fix a pre-existing lint backlog before they can start.

## See also

- [Adopting the skill set](../resources/adopting.md) — the wider story of bringing an existing repo under the set
- [`scaffold-project`](scaffold-project.md) — the greenfield sibling that hands off here
- [Templates](../resources/templates.md) — the `docs/agents/*` and session-start seeds this skill writes from
- [`trace`](trace.md) — the traceability check the configured specs directory and test globs feed
