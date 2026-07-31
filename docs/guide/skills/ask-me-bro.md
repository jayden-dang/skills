# `ask-me-bro`

> The router. It names the entry point for a task and explains the chain that follows — without executing any of it.

|  |  |
|---|---|
| **Bucket** | meta |
| **Invocation** | user-invoked — run as `/ask-me-bro` (the frontmatter sets `disable-model-invocation: true`, so the agent can name it but cannot auto-invoke it) |
| **Reads** | the user's situation and what specs already exist |
| **Writes** | nothing — it produces a routing decision, not an artifact |
| **Calls** | invokes the model-invocable entry point it lands on ([`frame-change`](frame-change.md), [`root-cause`](root-cause.md), [`validate-feature`](validate-feature.md), [`review-product-flow`](review-product-flow.md)); names user-invoked ones ([`triage`](triage.md), [`scan-architecture`](scan-architecture.md), [`configure-repo`](configure-repo.md), [`bootstrap-repo`](bootstrap-repo.md), [`write-handoff`](write-handoff.md), [`cut-release`](cut-release.md)) for the user to run |
| **Called by** | [`gate-session`](gate-session.md) (names it when the right flow is unclear) |

## When it fires

The user runs `/ask-me-bro` when they are unsure which skill or flow fits — asking "how do I start", "what's the workflow", "which skill should I use", or "what comes next". It routes among the already-installed development skills; it is not for discovering or installing new ones. `gate-session` names it whenever the agent cannot tell which flow applies.

The skill's own rule for itself: read the situation, name the entry point, explain the chain, and then stop. It does not start executing the chosen flow inside itself. If the entry point it lands on is model-invocable, it invokes it and lets that skill take over; if the entry point is user-invoked, it can only name it and tell the user to run the command.

## The main flow: idea → ship

The heart of the skill is a map of the standard chain, which it walks the user through:

1. **[`frame-change`](frame-change.md)** — always the entry point for new behavior. It interviews the user, explores the codebase, detours to [`research`](research.md) or [`run-spike`](run-spike.md) when a question needs evidence, and ends by declaring a ceremony tier:
   - **Tier 0** (typo-level, no behavior change): skip specs — [`test-first`](test-first.md) plus [`prove-claim`](prove-claim.md).
   - **Tier 1** (bugfix or ≤ half-day change): a mini-spec — a fix requirement plus a SHALL-CONTINUE-TO guard in the owning `requirements.md`, and a tagged regression test.
   - **Tier 2** (feature): the full spec cycle, continuing below.
2. **[`specify-behavior`](specify-behavior.md)** → **[`design-solution`](design-solution.md)** → **[`plan-tasks`](plan-tasks.md)** — the spec triad under `docs/specs/<date>-<feature>/`, with approval gates between each.
3. **[`isolate-workspace`](isolate-workspace.md)** → **[`build-in-waves`](build-in-waves.md)** — an isolated workspace, then task-by-task execution with ledgered progress.
4. **[`inspect-change`](inspect-change.md)** → **[`validate-feature`](validate-feature.md)** → **[`land-branch`](land-branch.md)** → (when shipping) **[`cut-release`](cut-release.md)** → **[`realign-spec`](realign-spec.md)**.

It also carries a context-hygiene rule: keep discovery through plan (steps 1–2) in one unbroken context window, and if the window fills before the plan is done, run `/write-handoff` to move to a fresh session. Execution sessions are context-isolated per task by design.

## On-ramps

For the tasks that do not start at `frame-change`, the skill lists direct entry points:

- A small in-scope change to an already-shipped, spec'd feature routes to [`amend-feature`](amend-feature.md), which reads the existing spec and routes to the light lane, escalating to `frame-change` only for genuinely new scope.
- Unit tests green but unsure it truly works end-to-end routes to [`validate-feature`](validate-feature.md).
- Wanting to try a finished feature by hand in the real app routes to [`review-product-flow`](review-product-flow.md).
- Something broken routes to [`root-cause`](root-cause.md), which exits into the tier-1 mini-spec flow.
- Incoming issues or PRs you did not author route to [`triage`](triage.md).
- A codebase that feels muddy routes to [`scan-architecture`](scan-architecture.md), whose output re-enters at `frame-change`.
- A new repo with no config routes to [`configure-repo`](configure-repo.md); no repo at all routes to [`bootstrap-repo`](bootstrap-repo.md).
- A session ending mid-work routes to [`write-handoff`](write-handoff.md); cutting a version routes to [`cut-release`](cut-release.md).

## Rules of thumb

Two governing heuristics close the skill. Never spec what you do not understand yet — unknowns go to `research` or `run-spike` first, because specs are for execution, not discovery. And when two skills both seem to apply, the process skill wins; it will invoke the implementation skill itself.

## Worked example

> **User:** `/ask-me-bro` I've got a bug report that the export button downloads an empty CSV. Where do I start?

`ask-me-bro` reads the situation — a reported defect, not new behavior — and routes rather than executes. It names the entry point and the chain:

> Start with `root-cause`. It establishes the root cause before any fix is proposed, then exits into the tier-1 mini-spec flow: a fix requirement plus a SHALL-CONTINUE-TO guard in the owning `requirements.md`, and a regression test tagged with the requirement ID. From there it is `test-first` for the fix, `prove-claim` before you claim it works, then `inspect-change` and `land-branch`.

Because `root-cause` is model-invocable, `ask-me-bro` hands off by invoking it and letting it take over. Had the situation instead been "review the PR my teammate opened", `ask-me-bro` would have named `/triage` and told the user to run it, since a user-invoked skill cannot be auto-invoked.

## Why it is written the way it is

`ask-me-bro` is a pure router, so per [`author-skills`](author-skills.md) it is a recipe skill, not a gate: its baseline failure is producing routing advice of the wrong shape, not breaking a rule under pressure. That is why it carries no iron law, no rationalization table, and no red flags — those forms measurably backfire on a skill whose job is to lay out a chain. Instead it is a positive contract: what a route IS, its steps in order. The `disable-model-invocation: true` frontmatter is itself doctrine — a router the agent could auto-invoke would fire on every ambiguous turn and pre-empt the actual entry skills; keeping it user-invoked means the human decides when routing help is wanted.

## See also

- [Methodology overview](../methodology/overview.md) — the same idea-to-ship chain in full
- [Ceremony tiers](../methodology/ceremony-tiers.md) — the tier-0/1/2 split `ask-me-bro` routes on
- [`gate-session`](gate-session.md) — the gate that names `ask-me-bro` when the flow is unclear
- [`frame-change`](frame-change.md) — the default entry point `ask-me-bro` points most tasks to
