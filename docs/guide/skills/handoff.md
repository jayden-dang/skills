# `handoff`

> Compact the conversation into a document a fresh agent can resume from — written to temp, never the workspace, because a handoff is session ephemera, not a project artifact.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | **user-invoked only** — run `/handoff`. `disable-model-invocation: true`: no skill may auto-invoke it; other skills only name it for the user to run |
| **Reads** | the current conversation, git branch/worktree state, the specs/plans/ADRs/issues it will cite |
| **Writes** | a single `handoff-<topic>-<timestamp>.md` in the OS temp directory — never in the repo |
| **Calls** | nothing required; optionally launches a background successor agent, only if the user asks |
| **Called by** | nobody — the user runs it directly |

## When it fires

When the current conversation must continue elsewhere. Three situations trigger it:

- Context is filling up or nearing compaction.
- The user is ending a session with work unfinished.
- Another agent must pick the work up.

Because it is `disable-model-invocation: true`, no skill triggers it automatically; a skill may *name* `/handoff`, but the user starts it.

The document is written to the **OS temp directory** (`$TMPDIR`, falling back to `/tmp`; `%TEMP%` on Windows), **never into the workspace** — a handoff is session ephemera, not a project artifact. It is named `handoff-<topic>-<timestamp>.md`, and the skill tells the user the absolute path.

If the user passes an argument, it is treated as what the next session will focus on: the whole document is oriented around that focus, trimming anything the focus makes irrelevant.

## The five sections

| Section | What it holds |
|---|---|
| **Goal** | what the work is ultimately for, in the user's terms |
| **Current state** | what is done, what is in flight, the **exact branch/worktree**, and whether the working tree is dirty |
| **Tried and rejected** | every approach attempted or considered and dropped, each with **why** |
| **Next actions** | concrete, ordered, starting with the very next command or edit |
| **Suggested skills** | which skills of this set the successor should invoke, and at which step |

**Tried and rejected** is the section the skill singles out: it saves the successor from re-walking dead ends, and it is usually the most valuable one in the document. **Suggested skills** is specific, not vague — "resume [`execute-plan`](execute-plan.md) at task 4", "run [`verify`](verify.md) before claiming task 3 done" — naming both the skill and the step.

Laid out, the document has the shape:

```markdown
# Handoff: <topic>

## Goal
<what the work is ultimately for, in the user's terms>

## Current state
- Branch / worktree: <exact ref and path>
- Working tree: <clean | dirty, with what is uncommitted>
- Done: <what is finished>
- In flight: <what is mid-change>

## Tried and rejected
- <approach> — dropped because <why>
- <approach> — considered, not taken because <why>

## Next actions
1. <the very next command or edit>
2. <then …>

## Suggested skills
- <skill> at <step> — <why>
```

## Rules

- **Reference, never duplicate.** Specs, plans, ADRs, issues, commits, diffs are cited by path, URL, or hash — not pasted. Copying their content bloats the handoff and **forks the truth**; the artifact on disk stays authoritative.
- **Redact secrets.** API keys, tokens, passwords, personal data are replaced with a placeholder naming where the real value lives — the doc may become another agent's prompt.
- **Decisions the user already made are recorded as settled**, with their rationale. The successor must not re-open them or re-ask.

The three rules pull in one direction: keep the handoff small, safe to pass around, and non-authoritative. It is a map to the work, not a second copy of it.

## Optional: launch the successor

Only if the user asks, the skill starts a background agent seeded with the handoff document as its prompt, with a descriptive display name, running in the current working directory. It confirms the mechanism the harness provides before promising it; otherwise it just hands over the file path.

## Completion criterion

Read the finished document **as a skeptic**: could a fresh agent, given only this file plus the artifacts it references, resume the work without asking the user anything already answered in this conversation? If any question survives that test, the answer belongs in the doc — add it before finishing. This is the one test that matters; a handoff that passes it has done its job, and one that fails it has quietly pushed the cost onto the successor.

## Worked example

A session has spent an afternoon on a caching feature and context is nearly full. The user runs `/handoff caching`. The skill writes `handoff-caching-1720579200.md` to `$TMPDIR` and fills the five sections:

- **Goal** — "cut report-page load time by caching the aggregation query; in the user's words, 'reports should feel instant on repeat views'."
- **Current state** — on branch `feat/report-cache` in the worktree `.worktrees/report-cache`, tree dirty with an uncommitted spike in `src/cache/`.
- **Tried and rejected** — an in-memory LRU was dropped because the app runs multi-process and the caches diverged; a blanket HTTP cache-control header was dropped because the data must invalidate on write. Each carries its *why*, so the successor does not retry either.
- **Next actions** — starting with the literal next command: "run the failing test in `src/cache/aggregate.test.ts`, then implement Redis-backed memoization behind the `AggregateCache` seam."
- **Suggested skills** — "resume under [`tdd`](tdd.md) — a RED test already exists; run [`verify`](verify.md) before any done claim."

Three rules bite here:

- The Redis connection string is **redacted** to a placeholder naming the secrets manager, because the file might be pasted into another agent's prompt.
- The `design.md` that owns the cache requirements is **referenced by path**, not copied — its content stays authoritative on disk rather than being forked into the handoff.
- The decision to use Redis rather than a local cache is recorded as **settled**, with its rationale, so the successor does not reopen it.

Reading it back as a skeptic: a fresh agent could pick up the branch, see why LRU and HTTP caching were abandoned, run the next command, and finish — without asking the user anything already settled. The completion criterion passes, so the handoff is done.

## Why it is written the way it is

A handoff fails in exactly one way: the successor has to come back and ask the user something this conversation already answered — so the whole skill is organized to close every such gap, which is what the skeptic's read at the end tests for. "Tried and rejected" is elevated because the most expensive thing a successor can do is cheerfully re-walk a dead end the previous agent already ruled out; recording the *why* is what makes that impossible. Reference-never-duplicate exists because two copies of a spec immediately disagree, and a handoff that forks the truth is worse than one that just points at it. Writing to temp rather than the repo keeps the codebase clean of session detritus — the handoff is scaffolding for a conversation, not a document the project keeps. And redaction is not optional politeness but a safety rule, because the file is explicitly intended to be readable as another agent's prompt.

## See also

- [`execute-plan`](execute-plan.md) — the most common work a handoff resumes, cited by task number
- [`verify`](verify.md) — the kind of gate a Suggested-skills line points the successor at
- [Artifacts](../concepts/artifacts.md) — the durable specs/plans a handoff references rather than copies
- [`worktrees`](worktrees.md) — the branch/worktree state Current state records exactly
- [`using-skills`](using-skills.md) — the successor's entry point for picking up the suggested skills
