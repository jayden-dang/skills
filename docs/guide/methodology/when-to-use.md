# When to use it

This skill set is opinionated and it costs something. Knowing when it earns its keep — and when it does not — matters more than adopting it everywhere.

## Use it when

**An AI agent writes a meaningful share of the code.** This is the design center. Every gate exists because an agent, unprompted, will skip it. If a human writes all the code and reviews all of it, most of the machinery is redundant with the discipline that human already has.

**Work outlives a context window.** The trace spine is a memory system. Its value shows up on the third session about a feature, when the original conversation is compacted and gone and the requirements file is the only surviving record of what was agreed.

**More than one person or agent touches the same code.** Requirement IDs give a shared, unambiguous vocabulary. "Does `SHELL-1.3` still hold?" is a question with an answer. "Did we break the module thing?" is not.

**Correctness is checkable and matters.** Traceability pays off exactly where you can write a test that proves a criterion. It pays off less on work whose success is a matter of taste.

**You ship releases.** [`release`](../skills/release.md) assembles the changelog by grouping commits under their requirement-ID trailers and looking up each requirement's text, so release notes read as shipped behavior rather than commit prose. That is free once the spine exists, and impossible without it.

## Do not use it when

**You are exploring, not building.** Specs are an execution tool, not a discovery tool. If you do not yet know what the thing should do, the answer is [`prototype`](../skills/prototype.md) or [`research`](../skills/research.md) — throwaway code and cited notes — not a requirements document. `brainstorm` will route you there itself when a question needs evidence rather than opinion.

**The change is genuinely trivial and you know it.** That is what tier 0 is for. State the tier, run `tdd`, run `verify`, move on. The system has an answer for small work; use it rather than abandoning the system.

**The repo is a throwaway.** A spike, a one-day demo, a scratch script. The trace spine's payoff is durability. There is nothing to be durable about.

**You cannot run a test.** The whole edifice rests on a runnable, red-capable signal. In an environment where nothing can be automatically verified, `verify` has nothing to verify with, `tdd` has no RED to observe, and `debug`'s Phase 1 gate cannot be passed. Fix that first; it is the highest-leverage thing you can do.

## Choosing your entry point

If you are unsure, run `/ask` — it is a router whose entire job is mapping a situation to the right entry point. Otherwise:

| Your situation | Start here |
|---|---|
| Brand-new project, empty directory | [`/scaffold-project`](../skills/scaffold-project.md) |
| Existing repo, adopting this skill set | [`/setup-repo`](../skills/setup-repo.md) |
| New feature, nothing spec'd yet | [`brainstorm`](../skills/brainstorm.md) |
| Small change to an already-shipped, spec'd feature | [`amend`](../skills/amend.md) |
| Something is broken | [`debug`](../skills/debug.md) |
| Unit tests green, unsure it truly works | [`acceptance-check`](../skills/acceptance-check.md) |
| Want to try a finished feature by hand | [`dogfood`](../skills/dogfood.md) |
| Incoming issue or external PR you did not author | [`/triage`](../skills/triage.md) |
| Codebase feels muddy, want a refactor target | [`/improve-architecture`](../skills/improve-architecture.md) |
| Session ending with work unfinished | [`/handoff`](../skills/handoff.md) |
| Cutting a version | [`/release`](../skills/release.md) |
| Spec has drifted from the code, or the trace check comes back dirty | [`sync-spec`](../skills/sync-spec.md) |

Two rules of thumb resolve most remaining ambiguity, and both come from `ask`:

> Never spec what you do not understand yet. Unknowns go to `research` or `prototype` first.

> When two skills both seem to apply, the process skill wins. It will invoke the implementation skill itself.

## The distinction people get wrong most often

**`brainstorm` versus `amend`.** They look similar and they are not.

`brainstorm` is for *new* behavior — a feature or component nothing has spec'd. It runs the full discovery interview and it will not let you write code until requirements are approved.

`amend` is for a small, in-scope change to a feature that *already shipped with a spec*. It reads the existing triad, classifies the change against it, and routes to the lightest lane that keeps the spec and the tests true. It is a fast lane, not a gate bypass: every path still exits through `tdd`.

The honest test for escalating from `amend` back to `brainstorm`: **does the existing spec's intent already cover this behavior?** If you are inventing what it should do, that is new scope, and it earns the full cycle.

## Context hygiene

One operational rule that is easy to miss and expensive to violate:

**Keep discovery through planning in one unbroken context window.** `brainstorm` → `write-requirements` → `write-design` → `write-plan` is a single continuous act of thinking. If the window is filling before the plan is done, do not push through — run `/handoff` and move to a fresh session with a document a successor can resume from.

Execution is different. `execute-plan` sessions are context-isolated **per task by design**: each task gets a fresh subagent whose world is a generated brief file. That is not a limitation being worked around; it is the mechanism.

## See also

- [Ceremony tiers](ceremony-tiers.md) — how the system scales down for small work
- [Philosophy](philosophy.md) — the principles behind these boundaries
- [`ask`](../skills/ask.md) — the router, when you are unsure
- [Adopting the skill set](../resources/adopting.md) — the practical install path
