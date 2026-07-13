---
name: ask
description: Use when the user is unsure which skill or flow in this set fits their task,
  asks "how do I start", "what's the workflow", "which skill should I use", or
  "what comes next" — routes among the already-installed development skills
  (not for discovering or installing new ones).
disable-model-invocation: true
---

You are the router. Read the situation, name the entry point, and explain the
chain that follows. Do not start executing the chosen flow inside this skill.
If the entry point is model-invocable (`brainstorm`, `amend`, `debug`,
`acceptance-check`, `dogfood`), invoke it and let it take over. If it is a user-invoked skill
(`triage`, `file-issues`, `improve-architecture`, `setup-repo`,
`scaffold-project`, `establish-project`, `handoff`, `release`), you cannot invoke it — name it and
tell the user to run its command, e.g. `/triage`.

## The main flow: idea → ship

1. **`brainstorm`** — always the entry point for new behavior. It interviews
   the user, explores the codebase, detours to `research` / `prototype` when a
   question needs evidence, and ends by declaring a ceremony tier:
   - **Tier 0** (typo-level, no behavior change): skip specs — `tdd` + `verify`.
   - **Tier 1** (bugfix / ≤ half-day change): mini-spec — a fix requirement +
     a SHALL-CONTINUE-TO guard in the owning `requirements.md`, tagged
     regression test.
   - **Tier 2** (feature): full spec cycle, continue below.
2. **`write-requirements`** → **`write-design`** → **`write-plan`** — the spec
   triad in `docs/specs/<date>-<feature>/`. Approval gates between each.
3. **`worktrees`** → **`execute-plan`** — isolated workspace, then task-by-task
   execution (subagent-per-task, ledgered progress).
4. **`code-review`** → **`acceptance-check`** → **`finish-branch`** →
   (when shipping) **`release`** → **`sync-spec`**.

**Context hygiene:** keep steps 1–2 (discovery through plan) in one unbroken
context window. If the window is filling up before the plan is done, tell the
user to run `/handoff` to move to a fresh session. Execution sessions are
context-isolated per task by design.

## On-ramps

- Small in-scope change to an already-shipped, spec'd feature (a tweak, recolor,
  or follow-on) → **`amend`** (reads the existing spec, routes to the light lane;
  escalates to `brainstorm` only for genuinely new scope).
- A mid-execution discovery invalidated your already-approved plan (the plan is wrong, scope
  changed mid-flight, the design no longer holds) → **`correct-course`** (it classifies the
  lowest invalidated artifact and routes the re-entry; `execute-plan` also hands off to it).
- Unit tests green but unsure it truly works end-to-end → **`acceptance-check`**
  (drives the running system through the spec's behaviors as a real user).
- Want to try a finished feature by hand in the real app → **`dogfood`**
  (builds a checkable, app-grounded guide you tick off while testing).
- Something is broken → **`debug`** (it exits into the tier-1 mini-spec flow).
- A conversation/spec/idea to capture as tracker issues (the fast lane, skipping
  the full spec triad) → **`file-issues`** (tracer-bullet slices with blocking
  edges, published agent-ready).
- Incoming issues/PRs you didn't author → **`triage`**.
- Codebase feels muddy → **`improve-architecture`** (periodic; its output
  re-enters at `brainstorm`).
- New repo, no config → **`setup-repo`**. No repo at all → **`scaffold-project`**.
- Starting a large/long-lived project and want a product vision + architecture-invariant
  spine above the feature loop → **`establish-project`** (optional; the layer the feature
  skills consult when present, off by default).
- Session is ending mid-work → **`handoff`**.
- Cutting a version → **`release`**.

## Rules of thumb

- Never spec what you don't understand yet: unknowns go to `research` or
  `prototype` first. Specs are for execution, not discovery.
- When two skills both seem to apply, the process skill wins; it will invoke
  the implementation skill itself.
