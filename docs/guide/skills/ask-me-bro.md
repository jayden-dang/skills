# `ask-me-bro`

> The router. It names the entry point for a task and explains the chain that follows — without executing any of it.

|  |  |
|---|---|
| **Bucket** | meta |
| **Invocation** | user-invoked — run as `/ask-me-bro` (the frontmatter sets `disable-model-invocation: true`, so the agent can name it but cannot auto-invoke it) |
| **Reads** | the user's situation and what specs already exist |
| **Writes** | nothing — it produces a routing decision, not an artifact |
| **Calls** | invokes the model-invocable entry point it lands on ([`solve-problem`](solve-problem.md), [`frame-change`](frame-change.md), [`root-cause`](root-cause.md), [`validate-feature`](validate-feature.md), [`review-product-flow`](review-product-flow.md)); names user-invoked ones ([`triage`](triage.md), [`scan-architecture`](scan-architecture.md), [`configure-repo`](configure-repo.md), [`bootstrap-repo`](bootstrap-repo.md), [`write-handoff`](write-handoff.md), [`cut-release`](cut-release.md), [`pathfind`](pathfind.md)) for the user to run |
| **Called by** | [`gate-session`](gate-session.md) (names it when the right flow is unclear) |

## When it fires

The user runs `/ask-me-bro` when they are unsure which skill or flow fits — asking "how do I start", "what's the workflow", "which skill should I use", or "what comes next". It routes among the already-installed development skills; it is not for discovering or installing new ones. `gate-session` names it whenever the agent cannot tell which flow applies.

The skill's own rule for itself: read the situation, name the entry point, explain the chain, and then stop. It does not start executing the chosen flow inside itself. If the entry point it lands on is model-invocable, it invokes it and lets that skill take over; if the entry point is user-invoked, it can only name it and tell the user to run the command.

## Which skill, and how to hand off

**Which** skill to start is [on-ramps](../process/on-ramps.md) — one home.
This page does not keep a parallel table.

**How** to hand off: invoke a model-invocable entry point; name a
user-invoked one (`/triage`, `/pathfind`, …) for the user to run.

Context hygiene: keep discovery through plan in one unbroken window; if
it fills, name `/write-handoff`. Execution is isolated per task.

The idea-to-ship chain itself is in [START-HERE](../START-HERE.md) and
[the process](../process/README.md). Rules of thumb live on the on-ramps page.

## Worked examples

> **User:** `/ask-me-bro` I've got a bug report that the export button downloads an empty CSV. Where do I start?

`ask-me-bro` reads the situation — a reported defect with clear unexpected behavior — and routes rather than executes:

> Start with `root-cause`. It establishes the root cause before any fix is proposed, then exits into the tier-1 mini-spec flow: a fix requirement plus a SHALL-CONTINUE-TO guard in the owning `requirements.md`, and a regression test. From there it is `test-first` for the fix, `prove-claim` before you claim it works, then `inspect-change` and `land-branch`.

Because `root-cause` is model-invocable, `ask-me-bro` hands off by invoking it. Had the situation instead been "review the PR my teammate opened", it would have named `/triage` for the user to run.

> **User:** `/ask-me-bro` Checkout conversion feels off, tests are green, CEO wants the AI personalizer shipped — no gap analysis. Bug or product? Debug or build?

`ask-me-bro` does **not** guess `root-cause`, `frame-change`, or multi-session `/pathfind`. It names **`solve-problem`**: write a Problem Brief (observed vs desired, facts vs assumptions, success provenance, one route). That skill then hands off to `root-cause`, `frame-change`, `clarify-decisions`, or `STOP` from an observable predicate.

## Why it is written the way it is

`ask-me-bro` is a pure router, so per [`author-skills`](author-skills.md) it is a recipe skill, not a gate: its baseline failure is producing routing advice of the wrong shape, not breaking a rule under pressure. That is why it carries no iron law, no rationalization table, and no red flags — those forms measurably backfire on a skill whose job is to lay out a chain. Instead it is a positive contract: what a route IS, its steps in order. The `disable-model-invocation: true` frontmatter is itself doctrine — a router the agent could auto-invoke would fire on every ambiguous turn and pre-empt the actual entry skills; keeping it user-invoked means the human decides when routing help is wanted.

## See also

- [On-ramps](../process/on-ramps.md) — which skill starts a situation
- [Methodology overview](../methodology/overview.md) — the same idea-to-ship chain in full
- [Ceremony tiers](../methodology/ceremony-tiers.md) — the tier-0/1/2 split `ask-me-bro` routes on
- [`gate-session`](gate-session.md) — the gate that names `ask-me-bro` when the flow is unclear
- [`solve-problem`](solve-problem.md) — ambiguous problem intake before diagnosis or delivery
- [`frame-change`](frame-change.md) — the default entry point for clear new behavior
