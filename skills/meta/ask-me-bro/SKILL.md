---
name: ask-me-bro
description: Routes among the already-installed development skills to the one that fits the task at
  hand. Run it with /ask-me-bro.
disable-model-invocation: true
---

You are the router. Read the situation, name the entry point, and explain the
chain that follows. Do not start executing the chosen flow inside this skill.
If the entry point is model-invocable (`frame-change`, `amend-feature`, `root-cause`,
`validate-feature`, `review-product-flow`), invoke it and let it take over. If it is a user-invoked skill
(`triage`, `publish-issues`, `scan-architecture`, `configure-repo`,
`bootstrap-repo`, `define-project`, `refresh-roadmap-status`, `assess-milestone`, `write-handoff`, `cut-release`, `pathfind`), you cannot invoke it — name it and
tell the user to run its command, e.g. `/triage` or `/pathfind`.

## The main flow: idea → ship

1. **`frame-change`** — always the entry point for new behavior. It interviews
   the user, explores the codebase, detours to `research` / `run-spike` when a
   question needs evidence, and ends by declaring a ceremony tier:
   - **Tier 0** (typo-level, no behavior change): skip specs — `test-first` + `prove-claim`.
   - **Tier 1** (bugfix / ≤ half-day change): mini-spec — a fix requirement +
     a SHALL-CONTINUE-TO guard in the owning `requirements.md`, tagged
     regression test.
   - **Tier 2** (feature): full spec cycle, continue below.
2. **`specify-behavior`** → **`design-solution`** → **`plan-tasks`** — the spec
   triad in `docs/specs/<date>-<feature>/`. Approval gates between each.
3. **`isolate-workspace`** → **`build-in-waves`** — isolated workspace, then task-by-task
   execution (subagent-per-task, ledgered progress).
4. **`inspect-change`** → **`validate-feature`** → **`land-branch`** →
   (when shipping) **`cut-release`** → **`realign-spec`**.

**Context hygiene:** keep steps 1–2 (discovery through plan) in one unbroken
context window. If the window is filling up before the plan is done, tell the
user to run `/write-handoff` to move to a fresh session. Execution sessions are
context-isolated per task by design.

## On-ramps

- Effort too large for one agent session and the route is still foggy (multi-session
  decision pathfinding) → **name `/pathfind`** for the user (user-invoked; never
  auto-start a map). Not required for ordinary tier-0/1 work.
- Small in-scope change to an already-shipped, spec'd feature (a tweak, recolor,
  or follow-on) → **`amend-feature`** (reads the existing spec, routes to the light lane;
  escalates to `frame-change` only for genuinely new scope).
- A mid-execution discovery invalidated your already-approved plan (the plan is wrong, scope
  changed mid-flight, the design no longer holds) → **`reroute-plan`** (it classifies the
  lowest invalidated artifact and routes the re-entry; `build-in-waves` also hands off to it).
- Unit tests green but unsure it truly works end-to-end → **`validate-feature`**
  (drives the running system through the spec's behaviors as a real user).
- Want to try a finished feature by hand in the real app → **`review-product-flow`**
  (builds a checkable, app-grounded guide you tick off while testing).
- Something is broken → **`root-cause`** (it exits into the tier-1 mini-spec flow).
- A conversation/spec/idea to capture as tracker issues (the fast lane, skipping
  the full spec triad) → **`publish-issues`** (tracer-bullet slices with blocking
  edges, published agent-ready).
- Incoming issues/PRs you didn't author → **`triage`**.
- Codebase feels muddy → **`scan-architecture`** (periodic; its output
  re-enters at `frame-change`).
- New repo, no config → **`configure-repo`**. No repo at all → **`bootstrap-repo`**.
- Starting a large/long-lived project and want a product vision + architecture-invariant
  spine above the feature loop → **`define-project`** (optional; the layer the feature
  skills consult when present, off by default).
- Several milestones in flight and unsure where the plan stands or what to do next →
  **`refresh-roadmap-status`** (read-only; derives progress from the roadmap, the specs, and git, then
  names one next action). Planning or changing the milestones themselves → **`plan-milestones`**.
- A milestone looks finished and you want to close it → **`assess-milestone`** (judges whether
  its outcome was achieved, records the judgment, and gates the close on your disposition).
- Session is ending mid-work → **`write-handoff`**.
- Cutting a version → **`cut-release`**.

## Rules of thumb

- Never spec what you don't understand yet — specs are for execution, not
  discovery; the unknowns detour is part of `frame-change` above.
- When two skills both seem to apply, the process skill wins; it will invoke
  the implementation skill itself.
