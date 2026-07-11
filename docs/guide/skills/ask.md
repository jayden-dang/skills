# `ask`

> The router. It names the entry point for a task and explains the chain that follows — without executing any of it.

|  |  |
|---|---|
| **Bucket** | meta |
| **Invocation** | user-invoked — run as `/ask` (the frontmatter sets `disable-model-invocation: true`, so the agent can name it but cannot auto-invoke it) |
| **Reads** | the user's situation and what specs already exist |
| **Writes** | nothing — it produces a routing decision, not an artifact |
| **Calls** | invokes the model-invocable entry point it lands on ([`brainstorm`](brainstorm.md), [`debug`](debug.md), [`acceptance-check`](acceptance-check.md), [`dogfood`](dogfood.md)); names user-invoked ones ([`triage`](triage.md), [`improve-architecture`](improve-architecture.md), [`setup-repo`](setup-repo.md), [`scaffold-project`](scaffold-project.md), [`handoff`](handoff.md), [`release`](release.md)) for the user to run |
| **Called by** | [`using-skills`](using-skills.md) (names it when the right flow is unclear) |

## When it fires

The user runs `/ask` when they are unsure which skill or flow fits — asking "how do I start", "what's the workflow", "which skill should I use", or "what comes next". It routes among the already-installed development skills; it is not for discovering or installing new ones. `using-skills` names it whenever the agent cannot tell which flow applies.

The skill's own rule for itself: read the situation, name the entry point, explain the chain, and then stop. It does not start executing the chosen flow inside itself. If the entry point it lands on is model-invocable, it invokes it and lets that skill take over; if the entry point is user-invoked, it can only name it and tell the user to run the command.

## The main flow: idea → ship

The heart of the skill is a map of the standard chain, which it walks the user through:

1. **[`brainstorm`](brainstorm.md)** — always the entry point for new behavior. It interviews the user, explores the codebase, detours to [`research`](research.md) or [`prototype`](prototype.md) when a question needs evidence, and ends by declaring a ceremony tier:
   - **Tier 0** (typo-level, no behavior change): skip specs — [`tdd`](tdd.md) plus [`verify`](verify.md).
   - **Tier 1** (bugfix or ≤ half-day change): a mini-spec — a fix requirement plus a SHALL-CONTINUE-TO guard in the owning `requirements.md`, and a tagged regression test.
   - **Tier 2** (feature): the full spec cycle, continuing below.
2. **[`write-requirements`](write-requirements.md)** → **[`write-design`](write-design.md)** → **[`write-plan`](write-plan.md)** — the spec triad under `docs/specs/<date>-<feature>/`, with approval gates between each.
3. **[`worktrees`](worktrees.md)** → **[`execute-plan`](execute-plan.md)** — an isolated workspace, then task-by-task execution with ledgered progress.
4. **[`code-review`](code-review.md)** → **[`acceptance-check`](acceptance-check.md)** → **[`finish-branch`](finish-branch.md)** → (when shipping) **[`release`](release.md)** → **[`sync-spec`](sync-spec.md)**.

It also carries a context-hygiene rule: keep discovery through plan (steps 1–2) in one unbroken context window, and if the window fills before the plan is done, run `/handoff` to move to a fresh session. Execution sessions are context-isolated per task by design.

## On-ramps

For the tasks that do not start at `brainstorm`, the skill lists direct entry points:

- A small in-scope change to an already-shipped, spec'd feature routes to [`amend`](amend.md), which reads the existing spec and routes to the light lane, escalating to `brainstorm` only for genuinely new scope.
- Unit tests green but unsure it truly works end-to-end routes to [`acceptance-check`](acceptance-check.md).
- Wanting to try a finished feature by hand in the real app routes to [`dogfood`](dogfood.md).
- Something broken routes to [`debug`](debug.md), which exits into the tier-1 mini-spec flow.
- Incoming issues or PRs you did not author route to [`triage`](triage.md).
- A codebase that feels muddy routes to [`improve-architecture`](improve-architecture.md), whose output re-enters at `brainstorm`.
- A new repo with no config routes to [`setup-repo`](setup-repo.md); no repo at all routes to [`scaffold-project`](scaffold-project.md).
- A session ending mid-work routes to [`handoff`](handoff.md); cutting a version routes to [`release`](release.md).

## Rules of thumb

Two governing heuristics close the skill. Never spec what you do not understand yet — unknowns go to `research` or `prototype` first, because specs are for execution, not discovery. And when two skills both seem to apply, the process skill wins; it will invoke the implementation skill itself.

## Worked example

> **User:** `/ask` I've got a bug report that the export button downloads an empty CSV. Where do I start?

`ask` reads the situation — a reported defect, not new behavior — and routes rather than executes. It names the entry point and the chain:

> Start with `debug`. It establishes the root cause before any fix is proposed, then exits into the tier-1 mini-spec flow: a fix requirement plus a SHALL-CONTINUE-TO guard in the owning `requirements.md`, and a regression test tagged with the requirement ID. From there it is `tdd` for the fix, `verify` before you claim it works, then `code-review` and `finish-branch`.

Because `debug` is model-invocable, `ask` hands off by invoking it and letting it take over. Had the situation instead been "review the PR my teammate opened", `ask` would have named `/triage` and told the user to run it, since a user-invoked skill cannot be auto-invoked.

## Why it is written the way it is

`ask` is a pure router, so per [`writing-skills`](writing-skills.md) it is a recipe skill, not a gate: its baseline failure is producing routing advice of the wrong shape, not breaking a rule under pressure. That is why it carries no iron law, no rationalization table, and no red flags — those forms measurably backfire on a skill whose job is to lay out a chain. Instead it is a positive contract: what a route IS, its steps in order. The `disable-model-invocation: true` frontmatter is itself doctrine — a router the agent could auto-invoke would fire on every ambiguous turn and pre-empt the actual entry skills; keeping it user-invoked means the human decides when routing help is wanted.

## See also

- [Methodology overview](../methodology/overview.md) — the same idea-to-ship chain in full
- [Ceremony tiers](../methodology/ceremony-tiers.md) — the tier-0/1/2 split `ask` routes on
- [`using-skills`](using-skills.md) — the gate that names `ask` when the flow is unclear
- [`brainstorm`](brainstorm.md) — the default entry point `ask` points most tasks to
