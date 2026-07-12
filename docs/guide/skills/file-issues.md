# `file-issues`

> Turns the current conversation, an approved spec, or a rough idea into tracer-bullet issues on the tracker — each declaring the issues that block it. The outgoing counterpart to `triage`: context in, agent-ready issues out.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | **user-invoked only** — run `/file-issues`. `disable-model-invocation: true`: the agent never auto-files issues; deciding what enters the backlog stays a human call |
| **Reads** | `docs/agents/issue-tracker.md` (tracker operations), `docs/agents/triage-labels.md` (label strings), `CONTEXT.md` (glossary), `docs/adr/`, the source spec/issue if one is referenced |
| **Writes** | new issues on the configured tracker (or `.scratch/<feature>/issues/*.md` locally), with blocking edges and the `ready-for-agent` label |
| **Calls** | [`grilling`](grilling.md) (when a slice is underspecified); names [`setup-repo`](setup-repo.md) if the tracker config is missing |
| **Called by** | nobody — the user runs it directly |

## When it fires

When the user has work in hand — this conversation, an idea they just described, or an approved spec — and wants it captured as **grabbable issues on the tracker** without running the full requirements → design → plan triad. It is the **fast lane**: break the work into vertical slices, wire their dependencies, and publish them agent-ready.

Because it is `disable-model-invocation: true`, no skill auto-invokes it; a skill may *mention* `/file-issues`, but the user starts it. Filing issues writes to an external service — creating GitHub/Linear issues, applying labels — so it is always a deliberate act, never an inference.

## Where it sits among the three issue skills

| You have | Use | Why not the others |
|---|---|---|
| A conversation / idea / spec to capture as grabbable work | **`file-issues`** | — |
| A tier-2 feature needing a traceable `requirements.md` → `design.md` → `tasks.md` | [`write-plan`](write-plan.md) (publishes its own tasks) | `file-issues` skips the triad, so it produces no requirement-ID trace |
| A raw incoming issue or external PR to evaluate | [`triage`](triage.md) | `file-issues` is outgoing; `triage` is incoming |

`write-plan` is the **heavyweight, traceable** publish path — every issue carries its `Requirements covered:` IDs. `file-issues` is the **lightweight capture** path for work that never went through the triad. The two never publish the same work.

## The AI marker

Every issue `file-issues` publishes opens its body with this exact line:

```
> *This issue was drafted by AI with `file-issues`.*
```

That line does double duty. It discloses AI authorship, and it is the **marker `triage` reads to skip these issues** — they are born agent-ready, so re-triaging them would stack a second, weaker spec on a real one. It is the outgoing mirror of `write-plan`'s `Requirements covered:` marker, which `triage` skips for the same reason.

## Process

1. **Gather context.** Work from the conversation; if the user passes a spec path, issue number, or URL, read its full body and comments first.
2. **Explore the codebase.** So titles and descriptions use the project's domain glossary (`CONTEXT.md`) and respect the area's ADRs. Look for a **prefactor** that makes the later work easier — "make the change easy, then make the easy change" — and sequence it as the first slice.
3. **Draft vertical slices.** Each slice cuts a narrow but **complete** path through every layer (schema, API, UI, tests), is demoable on its own, and fits one fresh context window. Give each its **blocking edges** — the slices that must finish before it can start. **Wide refactors** are the exception: a mechanical change whose blast radius breaks thousands of call sites can't land as one vertical slice, so it is sequenced **expand → migrate (in batches) → contract**, each batch its own issue, CI green batch to batch.
4. **Quiz the user.** Present the breakdown as a numbered list — Title, Blocked by, What it delivers — and ask whether the granularity and the edges are right, and whether any should be merged or split. When a slice is underspecified in a way only the user can resolve, [`grilling`](grilling.md) shapes it one question at a time. Iterate until approved.
5. **Publish.** In **dependency order, blockers first**, so each edge can reference a real identifier. On a remote tracker: one issue per slice, native sub-issue/blocking links where the platform has them; on a local tracker: one file per slice under `.scratch/<feature>/issues/NN-slug.md`, numbered in dependency order. The `ready-for-agent` label is applied **only to what is actually grabbable**: where the tracker *enforces* the blocking edge (native dependency links, Linear `blocks` relations) every slice gets it; where "Blocked by" is only text (GitHub Issues, local files) only the **frontier** — slices with no open blocker — gets it, and the user promotes each slice as its blockers close. Otherwise an autonomous agent grabs a labeled-but-blocked issue it cannot finish. Work the frontier, publishing any slice whose blockers are already published. **Never close or modify a parent issue.**

## What a published issue contains

Behavior and interfaces, **never file paths or line numbers** — they go stale while the issue waits. The body carries what to build (end-to-end behavior, from the user's view), independently verifiable acceptance criteria, and the Blocked-by list. When the work is covered by an existing spec, the relevant criteria cite the requirement IDs (`CODE-N.M`) so the trace stays intact. A prototype's decision-pinning snippet (a state machine, reducer, schema, or type shape) may be inlined; a working demo may not.

## Exit

The skill names the **frontier** — the slices that can start immediately — and points the user at the next step: work each slice with [`execute-plan`](execute-plan.md) (or inline [`tdd`](tdd.md)), clearing context between slices. Because the issues carry the AI marker, `triage` leaves them alone.

## Why it is written the way it is

`file-issues` is `disable-model-invocation: true` for the same reason as `triage`: what gets built is the user's call, and a skill that publishes to an external tracker on inference would silently shape the project record. It is a **separate skill from `write-plan`** rather than a flag on it because its trigger is genuinely distinct — capturing loose context, not executing an approved design — and folding the two would drag the heavyweight traceability machinery onto the fast lane. The **tracer-bullet** slicing is the same discipline `write-plan` uses: a vertical slice is demoable and context-window-sized, so an agent can grab one and finish it green, which a horizontal layer-slice can't promise.

## See also

- [`triage`](triage.md) — the incoming counterpart; reads the same tracker config, skips `file-issues`' output
- [`write-plan`](write-plan.md) — the heavyweight, traceable publish path
- [`grilling`](grilling.md) — shapes an underspecified slice before it is published
- [`setup-repo`](setup-repo.md) — writes the tracker and label config `file-issues` reads
- [`execute-plan`](execute-plan.md) — where a published slice gets built
