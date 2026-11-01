# `publish-issues`

> Turns the current conversation, an approved spec, or a rough idea into tracer-bullet issues on the tracker — each declaring the issues that block it. The outgoing counterpart to `triage`: context in, agent-ready issues out.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | **user-invoked only** — run `/publish-issues`. `disable-model-invocation: true`: the agent never auto-files issues; deciding what enters the backlog stays a human call |
| **Reads** | `docs/agents/issue-tracker.md` (tracker operations), `docs/agents/triage-labels.md` (label strings), `CONTEXT.md` (glossary), `docs/adr/`, the source spec/issue if one is referenced |
| **Writes** | new issues on the configured tracker (or `.scratch/<feature>/issues/*.md` locally), with blocking edges and the `ready-for-agent` label |
| **Calls** | [`clarify-decisions`](clarify-decisions.md) (when a slice is underspecified); names [`configure-repo`](configure-repo.md) if the tracker config is missing |
| **Called by** | nobody — the user runs it directly |

## When it fires

When the user has work in hand — this conversation, an idea they just described, or an approved spec — and wants it captured as **grabbable issues on the tracker** without running the full requirements → design → plan triad. It is the **fast lane**: break the work into vertical slices, wire their dependencies, and publish them agent-ready.

Because it is `disable-model-invocation: true`, no skill auto-invokes it; a skill may *mention* `/publish-issues`, but the user starts it. Filing issues writes to an external service — creating GitHub/Linear issues, applying labels — so it is always a deliberate act, never an inference.

## Where it sits among the three issue skills

| You have | Use | Why not the others |
|---|---|---|
| A conversation / idea / spec to capture as grabbable work | **`publish-issues`** | — |
| A tier-2 feature needing a traceable `requirements.md` → `design.md` → `tasks.md` | [`plan-tasks`](plan-tasks.md) (publishes **one feature issue** by default) | `publish-issues` skips the triad, so it produces no requirement-ID audit-trace |
| A raw incoming issue or external PR to evaluate | [`triage`](triage.md) | `publish-issues` is outgoing; `triage` is incoming |

`plan-tasks` is the **heavyweight, traceable** publish path — **one feature issue** per plan (tasks stay in `tasks.md`). `publish-issues` is the **lightweight capture** path for work that never went through the triad (one issue per tracer-bullet slice). The two never publish the same work.

## Process

1. **Gather context.** Work from the conversation; if the user passes a spec path, issue number, or URL, read its full body and comments first.
2. **Explore the codebase.** So titles and descriptions use the project's domain glossary (`CONTEXT.md`) and respect the area's ADRs. Look for a **prefactor** that makes the later work easier — "make the change easy, then make the easy change" — and sequence it as the first slice.
3. **Draft vertical slices.** Each slice cuts a narrow but **complete** path through every layer (schema, API, UI, tests), is demoable on its own, and fits one fresh context window. Give each its **blocking edges** — the slices that must finish before it can start. **Wide refactors** are the exception: a mechanical change whose blast radius breaks thousands of call sites can't land as one vertical slice, so it is sequenced **expand → migrate (in batches) → contract**, each batch its own issue, CI green batch to batch.
4. **Quiz the user.** Present the breakdown as a numbered list — Title, Blocked by, What it delivers — and ask whether the granularity and the edges are right, and whether any should be merged or split. When a slice is underspecified in a way only the user can resolve, [`clarify-decisions`](clarify-decisions.md) shapes it one question at a time. Iterate until approved.
5. **Publish.** In **dependency order, blockers first**, so each edge can reference a real identifier. On a remote tracker: one issue per slice, with its blocking edge as **Issue format** says; on a local tracker: one file per slice under `.scratch/<feature>/issues/NN-slug.md`, numbered in dependency order. Every slice carries the same state role, `ready-for-agent`, and the edge holds a blocked slice back, because `/board` and `/go` read it. Local files keep `blocked` in `Status:` behind the frontier. Work the frontier, publishing any slice whose blockers are already published. **Never close or modify a parent issue.**

## What a published issue contains

What `docs/agents/issue-tracker.md` **Issue format** says: Problem, Outcome, Acceptance and Out of scope, with an assignee, priority, estimate and status. Where specs are shared and an existing spec covers the work, the last line is `Requirements covered:` with its IDs.

## Exit

The skill names the **frontier** — the slices that can start immediately — and points the user at the next step: work each slice with [`build-in-waves`](build-in-waves.md) (or inline [`test-first`](test-first.md)), clearing context between slices. Because the issues carry a state role, `triage` leaves them alone.

## Why it is written the way it is

`publish-issues` is `disable-model-invocation: true` for the same reason as `triage`: what gets built is the user's call, and a skill that publishes to an external tracker on inference would silently shape the project record. It is a **separate skill from `plan-tasks`** rather than a flag on it because its trigger is genuinely distinct — capturing loose context, not executing an approved design — and folding the two would drag the heavyweight traceability machinery onto the fast lane. The **tracer-bullet** slicing is the same discipline `plan-tasks` uses: a vertical slice is demoable and context-window-sized, so an agent can grab one and finish it green, which a horizontal layer-slice can't promise.

## See also

- [`triage`](triage.md) — the incoming counterpart; reads the same tracker config, skips `publish-issues`' output
- [`plan-tasks`](plan-tasks.md) — the heavyweight, traceable publish path
- [`clarify-decisions`](clarify-decisions.md) — shapes an underspecified slice before it is published
- [`configure-repo`](configure-repo.md) — writes the tracker and label config `publish-issues` reads
- [`build-in-waves`](build-in-waves.md) — where a published slice gets built
