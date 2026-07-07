---
name: ask
description: Use when the user is unsure which skill or flow fits their situation, or asks "how do I start", "what's the workflow", or "which skill should I use"
disable-model-invocation: true
---

You are the router. Read the situation, name the entry point, and explain the
chain that follows. Do not start executing the chosen flow inside this skill —
invoke its first skill and let it take over.

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
4. **`code-review`** → **`finish-branch`** → (when shipping) **`release`** →
   **`sync-spec`**.

**Context hygiene:** keep steps 1–2 (discovery through plan) in one unbroken
context window. If the window is filling up before the plan is done, `handoff`
to a fresh session. Execution sessions are context-isolated per task by design.

## On-ramps

- Something is broken → **`debug`** (it exits into the tier-1 mini-spec flow).
- Incoming issues/PRs you didn't author → **`triage`**.
- Codebase feels muddy → **`improve-architecture`** (periodic; its output
  re-enters at `brainstorm`).
- New repo, no config → **`setup-repo`**. No repo at all → **`scaffold-project`**.
- Session is ending mid-work → **`handoff`**.
- Cutting a version → **`release`**.

## Rules of thumb

- Never spec what you don't understand yet: unknowns go to `research` or
  `prototype` first. Specs are for execution, not discovery.
- When two skills both seem to apply, the process skill wins; it will invoke
  the implementation skill itself.
