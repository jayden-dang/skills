# When to use it

This skill set is opinionated and it costs something. Knowing when it earns its keep — and when it does not — matters more than adopting it everywhere.

## Use it when

**An AI agent writes a meaningful share of the code.** This is the design center. Every gate exists because an agent, unprompted, will skip it. If a human writes all the code and reviews all of it, most of the machinery is redundant with the discipline that human already has.

**Work outlives a context window.** The trace spine is a memory system. Its value shows up on the third session about a feature, when the original conversation is compacted and gone and the requirements file is the only surviving record of what was agreed.

**More than one person or agent touches the same code.** Requirement IDs give a shared, unambiguous vocabulary. "Does `SHELL-1.3` still hold?" is a question with an answer. "Did we break the module thing?" is not.

**Correctness is checkable and matters.** Traceability pays off exactly where you can write a test that proves a criterion. It pays off less on work whose success is a matter of taste.

**You ship releases.** [`cut-release`](../skills/cut-release.md) assembles the changelog by grouping commits under their requirement-ID trailers and looking up each requirement's text, so release notes read as shipped behavior rather than commit prose. That is free once the spine exists, and impossible without it.

## Do not use it when

**You are exploring, not building.** Specs are an execution tool, not a discovery tool. If you do not yet know what the thing should do, the answer is [`run-spike`](../skills/run-spike.md) or [`research`](../skills/research.md) — throwaway code and cited notes — not a requirements document. `frame-change` will route you there itself when a question needs evidence rather than opinion.

**The change is genuinely trivial and you know it.** That is what tier 0 is for. State the tier, run `test-first`, run `prove-claim`, move on. The system has an answer for small work; use it rather than abandoning the system.

**The repo is a throwaway.** A spike, a one-day demo, a scratch script. The trace spine's payoff is durability. There is nothing to be durable about.

**You cannot run a test.** The whole edifice rests on a runnable, red-capable signal. In an environment where nothing can be automatically verified, `prove-claim` has nothing to prove-claim with, `test-first` has no RED to observe, and `root-cause`'s Phase 1 gate cannot be passed. Fix that first; it is the highest-leverage thing you can do.

## Choosing your entry point

If you are unsure, run `/route-task` — it is a router whose entire job is mapping a situation to the right entry point. Otherwise:

| Your situation | Start here |
|---|---|
| Brand-new project, empty directory | [`/bootstrap-repo`](../skills/bootstrap-repo.md) |
| Existing repo, adopting this skill set | [`/configure-repo`](../skills/configure-repo.md) |
| New feature, nothing spec'd yet | [`frame-change`](../skills/frame-change.md) |
| Small change to an already-shipped, spec'd feature | [`amend-feature`](../skills/amend-feature.md) |
| Something is broken | [`root-cause`](../skills/root-cause.md) |
| Unit tests green, unsure it truly works | [`validate-feature`](../skills/validate-feature.md) |
| Want to try a finished feature by hand | [`review-product-flow`](../skills/review-product-flow.md) |
| Have a review-product-flow guide and want the agent to run every case | [`run-product-walkthrough`](../skills/run-product-walkthrough.md) |
| A conversation, spec, or idea to capture as tracker issues | [`/publish-issues`](../skills/publish-issues.md) |
| Incoming issue or external PR you did not author | [`/triage`](../skills/triage.md) |
| Codebase feels muddy, want a refactor target | [`/scan-architecture`](../skills/scan-architecture.md) |
| Session ending with work unfinished | [`/write-handoff`](../skills/write-handoff.md) |
| Cutting a version | [`/cut-release`](../skills/cut-release.md) |
| Spec has drifted from the code, or the audit-trace check comes back dirty | [`realign-spec`](../skills/realign-spec.md) |

Two rules of thumb resolve most remaining ambiguity, and both come from `route-task`:

> Never spec what you do not understand yet. Unknowns go to `research` or `run-spike` first.

> When two skills both seem to apply, the process skill wins. It will invoke the implementation skill itself.

## The distinction people get wrong most often

**`frame-change` versus `amend-feature`.** They look similar and they are not.

`frame-change` is for *new* behavior — a feature or component nothing has spec'd. It runs the full discovery interview and it will not let you write code until requirements are approved.

`amend-feature` is for a small, in-scope change to a feature that *already shipped with a spec*. It reads the existing triad, classifies the change against it, and routes to the lightest lane that keeps the spec and the tests true. It is a fast lane, not a gate bypass: every path still exits through `test-first`.

The honest test for escalating from `amend-feature` back to `frame-change`: **does the existing spec's intent already cover this behavior?** If you are inventing what it should do, that is new scope, and it earns the full cycle.

## Context hygiene

One operational rule that is easy to miss and expensive to violate:

**Keep discovery through planning in one unbroken context window.** `frame-change` → `specify-behavior` → `design-solution` → `plan-tasks` is a single continuous act of thinking. If the window is filling before the plan is done, do not push through — run `/write-handoff` and move to a fresh session with a document a successor can resume from.

Execution is different. `build-in-waves` sessions are context-isolated **per task by design**: each task gets a fresh subagent whose world is a generated brief file. That is not a limitation being worked around; it is the mechanism.

## See also

- [Ceremony tiers](ceremony-tiers.md) — how the system scales down for small work
- [Philosophy](philosophy.md) — the principles behind these boundaries
- [`route-task`](../skills/route-task.md) — the router, when you are unsure
- [Adopting the skill set](../resources/adopting.md) — the practical install path
