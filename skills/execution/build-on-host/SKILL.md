---
name: build-on-host
version: 1.0.0
description: Use when an approved tasks.md should run somewhere other than this
  machine — offload the build to a remote host, build server, or second machine
  over ssh, unattended, under whichever agent CLI that host runs (grok, codex,
  claude, cursor-agent, kimi, gemini, qwen, opencode). Produces the finished
  run's branch back on this machine and a close report naming the agent and the
  base commit it built. Wraps the execute route the user already picked —
  build-in-waves, build-by-story, or build-inline — and never replaces it.
---

Ephemera paths: resolve `FEATURE_CODE` / `<CODE>` then follow `templates/skills-ephemera-paths.md` (feature root `.skills/<CODE>/`). Resolve pack seeds in this order, first path that exists: (1) `templates/` beside this SKILL.md, (2) `${CLAUDE_PLUGIN_ROOT}/templates` when that variable is set, (3) `../../../templates` relative to this SKILL.md.

# Build On Host

Run an approved plan on a **remote build host**, under **whichever agent CLI**
that host runs. This skill owns the host, the base commit, and the return path.

**Two-layer rule.** Every step below is agent-neutral: git over SSH, one tmux
session, one log, one exit sentinel. Everything CLI-specific — headless flag,
working-directory flag, autonomy flag, auth check, log shape — lives in
`runner-drivers.md` and nowhere else; a new agent CLI is a new row there, never
an edit to these steps. Runs are **full-autonomy**: each driver's
`autonomy_full` flag, in a run directory of its own. No allowlist profile here.

## What this skill does not own

| Question | Owner |
|---|---|
| Which tasks run, in what order, with what review | the picked execute route, on the host |
| Whether a success sentence is true | `prove-claim`, before you say it here |
| How the returned branch merges | `land-branch`, after the return |

## Phase 1 — Preflight

Run every check before touching the host's git state. Report all failures at
once with the exact one-time fix beside each; do not fix them silently.

1. **Alias.** Try the manifest's alias, then its fallbacks, in order:
   `ssh -o BatchMode=yes -o ConnectTimeout=8 <alias> true`. Record the winner.
2. **Toolchain.** `git`, `tmux`, the driver's `bin`, and anything the repo's
   install and verify commands need, all resolving **with the PATH the manifest
   declares** — a non-interactive `ssh` shell reads neither `.zshrc` nor
   `.zprofile`. It precedes the tmux check because without that PATH,
   `ssh <alias> 'tmux ls'` answers `command not found` on a host running tmux,
   which the next check reads as "no server". Docker and per-language toolchains
   hide here too: installed, running, and invisible to a bare `ssh`.
3. **tmux server.** `ssh <alias> '<manifest PATH>; tmux ls'`. A server started
   from the host's **GUI login** must already exist — panes forked from it
   inherit an unlocked login keychain, and keychain-backed CLIs fail without it.
   No server → STOP and ask the user to start one on the host console.
4. **Driver.** Read the agent's row in `runner-drivers.md`. Row absent → STOP,
   and follow that file's probe recipe to add one. `status: probed` is
   dispatchable; say so in the report.
5. **Auth — GATE.** Run the driver's `auth_check` **inside the tmux server**,
   not over plain SSH. Failure → STOP with that driver's login command.

   <HARD-GATE>
   NO DISPATCH ON A FAILED OR SKIPPED AUTH CHECK. A run that starts unauthenticated
   burns the lease and returns nothing. Neither a user instruction to "just try it"
   nor a previously green check on another agent overrides this.
   </HARD-GATE>
6. **Skills reachable.** Use the driver's `skills_check` to confirm the picked
   route plus `execute-common`, `prove-claim`, `test-first`,
   `isolate-workspace`, `inspect-change`. Unreachable → the kickoff falls back
   to explicit `SKILL.md` paths, and the run record says so.

*Done when: every check has a verdict, failures carry their fix command, and no
gate is open.*

## Phase 2 — Provision

The manifest is `docs/agents/host-build.md`, committed, never holding a secret
value; per-run state is `.skills/<CODE>/host-run.json`, local-only. Missing
manifest, or anything below unbuilt → read `host-provisioning.md` beside this
file and follow it exactly — run root,
bare repo, warm clone, the `hostbuild` remote, install, and env-file transfer in
their idempotent form. Two of its rules do not bend. The warm clone is the point:
never wipe and re-clone to "start clean" unless the user asked. And for env files,
a value is transferred only on explicit confirmation, for the files the manifest
names — record names, never values.

WHEN `max_concurrency` is above 1, also read `run-isolation.md` and follow it
exactly. It owns slots, the per-run worktree, and the port and container
namespacing that keeps concurrent runs off each other — including the two
measured traps, `git worktree add --force` and a compose `ports:` override
without `!override`.

*Done when: the clone is warm, every declared env name is present on the host,
and under concurrency the run holds a slot with its worktree, port block, and
compose project derived from it.*

## Phase 3 — Bind the base commit

The plan was approved against one revision. That revision, and no other, is what
the host builds.

1. `BASE` = the revision the plan was approved at — the local feature branch tip
   carrying the approved `tasks.md`. Record it.
2. `git push hostbuild "${BASE}:refs/heads/${BRANCH}"`. The base commit does
   **not** need to exist on GitHub. Keep the braces: under zsh, `$BASE:refs/...`
   applies the `:r` history modifier and silently pushes a mangled refspec.
3. On the host: fetch, then `git checkout -B <branch> <BASE>`.
4. **Compare `git rev-parse HEAD` on the host against `BASE` as strings.**

   <HARD-GATE>
   NO DISPATCH WHILE THE TWO SHAs DIFFER. A host that is "on the right branch" is
   not the same claim as a host on the right commit, and a stale checkout produces
   a diff nobody can trace to the approved plan.
   </HARD-GATE>

*Done when: both sides print the same SHA, and both are in the run record.*

## Phase 4 — Dispatch

1. Write `.skills/<CODE>/host-kickoff.md`: name the execute route and the plan
   path, state the branch and base SHA, and state that the run is unattended.
   Pass it by **file** where the driver has a `prompt_file` — a long prompt
   through a shell argument is a quoting bug waiting to happen.
2. Render the command from the driver row. Never hand-write a CLI's flags here.
3. Dispatch detached, against the **existing** tmux server:

   ```
   tmux new-session -d -s bh-<CODE> \
     '<PATH exports>; cd <RUNDIR> && <driver command> > <LOG> 2>&1; echo $? > <SENTINEL>'
   ```

   The sentinel is written by the shell, not the agent, so a crashed CLI still
   produces an exit code.
4. Write the run record. *Done when: `tmux has-session -t bh-<CODE>` is true and
   the record names the session, log, and sentinel.*

## Phase 5 — Watch and close

Poll — never hold the SSH connection open for the length of a build. The signal
table lives in `reclaim.md` § Status, which answers the same question mid-run as
it does afterwards; read it and follow it. The one trap worth naming here: a
driver whose `log_format` emits a single object at the end leaves the log at
**0 bytes** for the whole run, so the session and the driver's `progress` field
are the liveness signals and a silent log is what working looks like.

On finish, read `return-leg.md` beside this file and follow it exactly — it owns
the order the work travels in, both return modes, and the token wiring `pr`
needs. Do not improvise a return: the agent commits in the host's **working
clone**, which the bare repo `hostbuild` points at has never seen, so a fetch run
straight after the build returns the commit you pushed *out*, exits 0, and reads
as success.

Report: route, agent and model, base SHA, commits returned, the driver's own
usage/cost fields when it emits them, and every check that was skipped. Any
sentence claiming the work succeeded goes through REQUIRED SUB-SKILL: use
`prove-claim` first — a zero exit code is the CLI's verdict on itself.

*Done when: the returned tip differs from `BASE`, the return mode is applied,
and no success sentence is unproven.*

## Phase 6 — Reclaim

A finished run keeps holding the host until something takes it back. Read
`reclaim.md` beside this file and follow it exactly — it owns the status read,
the reclaimable-vs-quarantined verdict, the enumerate-then-delete order, and the
merged trigger. Two rules from it: reclaim fires on a pull request that is
actually `MERGED` with a merge commit, never on one merely closed; and an age
policy may stop processes and containers but **may never delete a worktree** —
that is a user's call, made against the status view.

*Done when: the run's compute is released and its slot is free, or the run is
quarantined and visible in status with a reason.*

| Thought | Reality |
|---|---|
| "Remote is unreachable over SSH, so the agent can't be logged in" | Plain SSH cannot open the login keychain. Check inside the tmux server before concluding anything about auth |
| "tmux isn't running — I'll start one over SSH" | A server started from SSH has no keychain. Ask for one from the console |
| "The host is on the feature branch, so it's on the right commit" | Compare SHAs as strings. Branch names drift; SHAs do not |
| "Two runs, so two clones — safer" | Measured safe: six parallel worktrees and commits, `git fsck` clean. Isolate per run, share the store |
| "The CLI exited 0, so the feature is done" | That is the CLI's verdict on itself. `prove-claim` decides what you may say |
| "Copy the whole .env across — it's faster than listing names" | The manifest names what travels. Unlisted secrets do not leave this machine |

### Red Flags

- Dispatching after a failed, skipped, or plain-SSH auth check
- Dispatching while the host SHA and `BASE` differ, or without comparing them
- Starting the tmux server from SSH and calling that check passed
- Writing a CLI's flags into these steps instead of into `runner-drivers.md`
- Closing on a fetch whose tip still equals `BASE`
- Opening a second pull request for a head that already has an open one
- Falling back to `fetch` when `GH_TOKEN` is missing instead of stopping
- Reporting success from a zero exit code without `prove-claim`
- Sending env values the manifest does not name, or recording a value anywhere
- Re-cloning a warm run root to "start clean" unasked
- Reaching for `--force` on a worktree, or an override without `!override`
- Deleting a worktree whose commits are not provably somewhere else

**Done when:** the host ran the picked route at the approved base SHA under full
autonomy, the branch is back on this machine, the return mode is applied, and
the report names the agent, the SHA, and everything skipped.
