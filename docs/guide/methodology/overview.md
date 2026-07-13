# Overview

This is an A-to-Z agentic development skill set: one system that carries a project from a raw idea to a tagged release, with **requirements traceability as the spine**.

It is built for a specific situation — a human directing an AI coding agent (or a fleet of them) through real work on a real codebase — and it exists because that situation has a failure mode that ordinary process documentation does not address.

## The problem it solves

An LLM is a stochastic system. Ask it the same question twice and you get two different answers, both plausible. That is a feature when you want ideas and a catastrophe when you want a codebase.

The specific failures compound:

- **Intent evaporates.** The user explains what they want. Three hundred turns later the context is compacted, the explanation is gone, and the agent is building something adjacent to what was asked. Nothing recorded the intent in a form that survives.
- **The agent rationalizes past its own rules.** "This is too small for process." "I'll add tests right after." "It's obviously X, let me just fix it." Each is locally reasonable and globally corrosive.
- **Completion is claimed, not proven.** "Done!" after a build that was never run. "Fixed!" after a change that was never re-tested. "Tests pass" from memory of a run ten minutes and four edits ago.
- **Verification checks the wrong thing.** Unit tests go green. The feature is broken, because green units prove the assertions someone wrote pass — not that the thing works when a real client calls it.
- **Nobody knows if the work is finished.** Was every acceptance criterion implemented? Which ones have tests? Which requirement does this commit even serve? A human audit answers this once and then rots.

Each failure has a corresponding defense in this system, and the defenses are the point.

## The shape of the answer

Every feature gets a **spec triad** in `docs/specs/<date>-<feature>/`:

- `requirements.md` — WHAT, as [EARS](../resources/ears.md) acceptance criteria, each carrying a [hierarchical ID](../concepts/requirement-ids.md) like `SHELL-1.2`
- `design.md` — HOW, where every architecture section names the requirement IDs it `Satisfies:`
- `tasks.md` — the PLAN, where every task ends with a `_Requirements: SHELL-1.2_` footer

That ID then flows outward into everything downstream: the test that verifies the behavior carries it as a tag, the commit that implements it carries it as a trailer, the issue that tracks it carries it in a `Requirements covered:` section, and the changelog entry that announces it is assembled from those trailers.

And then — this is the part that makes it real rather than aspirational — a **deterministic check**, not human diligence, keeps the chain honest. The [`trace`](../resources/scripts.md#the-trace-check) skill runs a fixed sequence of `grep` and `git` passes — invoked by `verify`, `release`, and `sync-spec` — and reports it when a task cites a requirement that does not exist, when a shipped requirement has no covering test, or when an ID is defined twice. Unchecked trace matrices rot; this one is machine-checked from primitives every repo already has.

Around that spine sit **36 skills** in ten buckets, each one a piece of process the agent is required to follow, and four **hard gates** that cannot be talked past. One of those buckets, `project/`, is an **optional layer above the feature loop**: on a large project, [`establish-project`](../skills/establish-project.md) maintains a repo-level product vision and an IDed architecture-invariant spine that the feature skills consult when present and ignore when absent.

## The four gates

| Gate | Skill | Law |
|---|---|---|
| No code before an approved spec | [`brainstorm`](../skills/brainstorm.md) | Write no code, scaffold nothing, until the ceremony tier is stated out loud |
| No production code before a failing test | [`tdd`](../skills/tdd.md) | `NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST` |
| No fix before a root cause | [`debug`](../skills/debug.md) | `NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST` |
| No completion claim without fresh evidence | [`verify`](../skills/verify.md) | `NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE` |

These are written as hard prohibitions with explicit rationalization tables, because that is the form that survives an agent under pressure. See [The gates](../concepts/gates.md).

## Ceremony scales with the task

The obvious objection to spec-driven development is that it drowns a two-line change in paperwork. The answer is a three-tier system, and the tier decision is itself the first design step:

| Tier | When | Artifacts |
|---|---|---|
| **0 — trivial** | typo-level, no behavior change | none; `tdd` and `verify` only |
| **1 — bugfix / small change** | behavior change, ≤ ~half a day | a mini-spec: one fix requirement plus a `SHALL CONTINUE TO` guard, and a tagged regression test |
| **2 — feature** | multi-task work | the full triad, then `execute-plan` |

`brainstorm` and `amend` decide the tier explicitly and say so out loud. Deciding a change is tier 0 *is* the design step. Skipping the decision is the overhead, not performing it.

See [Ceremony tiers](ceremony-tiers.md).

## The main chain

```
brainstorm ──► write-requirements ──► write-design ──► write-plan
  (gate: no code)   (EARS + IDs)        (Satisfies:)    (_Requirements:_)
       │                                                        │
       │ tier 0/1 shortcuts                                     ▼
       │                                       worktrees ──► execute-plan
       ▼                                                        │
 debug / tdd / verify ◄── discipline skills govern ─────────────┘
                                                                │
       code-review ──► acceptance-check ──► finish-branch ──► release ──► sync-spec
                   (drive the running system as a real user)
```

Each arrow is a hand-off written into the skill body as a `REQUIRED SUB-SKILL:` line. The chain is not a diagram someone drew after the fact; it is how the skills actually reach each other.

## What makes it different from generic spec-driven development

Plenty of methodologies say "write requirements first." Three things here are unusual:

1. **The requirement ID is a first-class runtime object.** It is not a heading in a document. It is a string that appears in a test tag, a commit trailer, an issue body, and a changelog line, and the trace check surfaces it the moment those uses disagree with the definition.

2. **The process is written for an agent, not a human.** Skill bodies are shaped by their observed failure mode: a skill that guards a rule the agent breaks under pressure gets a prohibition and a rationalization table; a skill whose output has the wrong shape gets a positive recipe instead, because in head-to-head tests prohibitions produced *more* of the unwanted content than no guidance at all. This doctrine is itself a skill — [`writing-skills`](../skills/writing-skills.md) — and every skill in the set was pressure-tested against it.

3. **Context is treated as a scarce, hostile resource.** [`execute-plan`](../skills/execute-plan.md) hands each task to a fresh subagent whose entire world is a generated brief file; bulk artifacts travel as file paths, never pasted text. Progress is appended to a ledger on disk because conversation memory does not survive compaction — and controllers that trusted memory have re-dispatched entire completed task sequences.

## Where to go next

- New to the ideas → [Philosophy](philosophy.md), then [When to use it](when-to-use.md)
- Adopting it on a repo today → [Adopting the skill set](../resources/adopting.md)
- Want the mechanics → [Traceability](../concepts/traceability.md) and [Requirement IDs](../concepts/requirement-ids.md)
- Want to see it run → [Examples](../examples/tier-2-feature.md)
- Looking for one skill → [Skill reference](../skills/README.md)
