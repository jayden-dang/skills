# `forge-prompt` — source register

**Date:** 2026-08-25 · **Skill:** `skills/discovery/forge-prompt` (v1.0.0) ·
**Companion to:** that skill's `TESTS.md`, which cites these by arXiv ID only

`TESTS.md` records *what was measured and what rule it produced*. This file records
*where each measurement came from and how far it was actually read* — because several
load-bearing claims in that design record were taken from search-result summaries
rather than from the source text, and a reader deciding whether to trust a rule needs
to know which.

## Evidence strength

| Tier | Meaning |
|---|---|
| **A — read** | Source retrieved and read in full during the design session |
| **A′ — read, no magnitudes** | Source retrieved, but only the qualitative finding could be extracted; the paper's effect sizes were not obtained |
| **B — summary only** | Cited in `TESTS.md` / `CHANGELOG.md` on the strength of a search-result summary. **Not verified against the source.** |
| **C — background** | Surfaced during search, informed framing, produced no rule |
| **D — unavailable** | Retrieval failed; contributed nothing |

---

## A — read in full, and what each produced

### [Coding Agents Are Guessing: Measuring Action-Boundary Violations in Underspecified DevOps Instructions](https://arxiv.org/html/2607.02294) · arXiv 2607.02294

The decisive source. Five agent×model configurations across OpenCode, Claude Code, and
Codex: **55.8–67.8%** of acted runs violated at least one action boundary. Varying three
orthogonal axes, **target certainty dominates** — safe success collapses **67.9% → 8.6%**
and wrong-target rises **9.6% → 75.1%** — ahead of intent clarity, which has only a
moderate effect on over-scoping. Action rates on shared production surfaces (**65.5%**)
are indistinguishable from contained ones (**64.0%**).

→ `What this touches` as a REQUIRED slot; the `[confirmed] / [unconfirmed]` mark; the
rule that `named` means *resolves to exactly one object*; `Off limits` and
`Must keep working` as declarations rather than an inferred risk label.

### [Asking What Matters: Reward-Driven Clarification for Software Engineering Tasks](https://arxiv.org/html/2604.14624v1) · arXiv 2604.14624

CLARITI. **36.8%** task success at **3.0** questions average versus GPT-5's 5.1 — and the
*answerable* proportion falls as the clarification set grows, with success plateauing
first. Shapley analysis over 700 underspecified issues ranks what to ask: **error
information > implementation details > environment configuration**. Four-stage reward:
non-redundancy, diversity, answerability, task relevance.

→ The interview ordering. Applied as an **answerability stop signal**, deliberately not
as a hard question cap — the measurement is about an agent filling gaps for autonomous
execution, whereas this skill's user is actively driving the interview.

### [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) · Anthropic

"Right altitude"; "the minimal set of information that fully outlines your expected
behavior"; distinct sections via XML tags or Markdown headers; just-in-time retrieval
holding "lightweight identifiers (file paths, stored queries, web links)" instead of
pre-loaded data.

→ The *pointers, not paste* block rule; the ~40-line ceiling.

### [Every AI Prompting Technique That Works on Reasoning Models (2026)](https://karozieminski.substack.com/p/ai-prompting-techniques-reasoning-models-2026)

Names five techniques that now degrade reasoning models — chain-of-thought,
few-shot, self-consistency, least-to-most, skeleton-of-thought — against ten that
still work. Core claim: *"Prescribing reasoning paths hurts performance. Defining goals
and constraints improves it."*

→ The block rule forbidding a step plan, a reasoning instruction, or a role preamble.
Also the resolution of the few-shot tension with Anthropic's guidance above: examples of
**outcome shape** belong in evidence; examples of **reasoning steps** do not.

### [What Makes a Good AI Coding Agent Prompt?](https://www.verdent.ai/guides/answers/good-prompt-ai-coding-agent) · Verdent

Seven industry slots: Context · Goal · Scope · Constraints · Evidence · Acceptance ·
Non-goals.

→ The starting point for the block — superseded in ordering once UnderSpecBench showed
that "Scope: the export module" reads well and is still an unresolved target.

---

## A′ — read, but the magnitudes were not obtained

Both justify removing routing from the artifact. Both were retrieved as PDFs and
summarised; neither summary carried the paper's effect sizes. **Re-read before relying
on either quantitatively.**

### [Cross-Context Review: Improving LLM Output Quality by Separating Production and Review Sessions](https://arxiv.org/pdf/2603.12123) · arXiv 2603.12123

Cross-context review (a fresh session receiving *only the artifact*) beats same-session
review. The stated recommendation is that the reviewing session receive neither the
original prompt, nor intermediate traces, nor task context — familiarity with initial
assumptions blinds a reviewer to fundamental errors.

→ Validates handing `/interpret-session` the finished block and nothing else.

### [When Context Hurts: The Crossover Effect of Knowledge Transfer on Multi-Agent Design Exploration](https://arxiv.org/pdf/2605.04361) · arXiv 2605.04361

Passing upstream reasoning to a downstream agent improves it up to a threshold, then
degrades exploration by over-anchoring it on upstream assumptions. Derived rule:
**selective context, not comprehensive history**.

→ The reason a same-session on-ramp was rejected: it leaks the whole interview trail,
not the artifact.

---

## B — cited on a search summary, not verified against the source

These four appear in `TESTS.md § RED-4` and in the `CHANGELOG` entry. Each was taken
from a search-result summary. **Verify before quoting them onward.**

| Source | Claim it carries in the design record |
|---|---|
| [Self-Anchoring Calibration Drift in Large Language Models](https://www.alphaxiv.org/overview/2603.01239) · arXiv 2603.01239 | Confidence drifts systematically when a model builds iteratively on its own prior outputs across turns |
| [Anchors in the Machine: Behavioral and Attributional Evidence of Anchoring Bias in LLMs](https://arxiv.org/html/2511.05766) · arXiv 2511.05766 | Self-preference in self-evaluation nearly disappears when authorship of the evaluated text is unknown |
| [Understanding the Anchoring Effect of LLM with Synthetic Data](https://arxiv.org/html/2505.15392v2) · arXiv 2505.15392 | *"Simple prompt-level mitigation strategies are largely ineffective"* — anchoring is a robust feature of model behavior |
| [Context Rot: How Increasing Input Tokens Impacts LLM Performance](https://www.trychroma.com/research/context-rot) · Chroma | All 18 frontier models tested degrade as input length grows; accuracy is highest at the beginning and end of the context and degrades >30% in the middle |

The third row is the load-bearing one: it is why the fix was to remove the conclusion
from the artifact rather than to write "do not over-trust the brief" into a downstream
skill. If that claim does not survive checking, the design decision is worth re-opening.

---

## C — background

Surfaced during search, shaped framing, produced no rule.

**Underspecification and clarification**
- [Ask or Assume? Uncertainty-Aware Clarification-Seeking in Coding Agents](https://arxiv.org/html/2603.26233v1) · arXiv 2603.26233
- [Ambig-SWE: Interactive Agents to Overcome Ambiguity in Software Engineering](https://arxiv.org/html/2502.13069v1) · arXiv 2502.13069 · [OpenReview](https://openreview.net/forum?id=X2yzXtH4wp)
- [Uncertainty-Aware Clarification in LLM Agents with Information Gain](https://arxiv.org/pdf/2606.03135) · arXiv 2606.03135

**Context engineering**
- [Context Engineering: A Practical Guide for AI Agents (2026)](https://sourcegraph.com/blog/context-engineering) · Sourcegraph
- [Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents) · Anthropic
- [Context engineering: memory, compaction, and tool clearing](https://platform.claude.com/cookbook/tool-use-context-engineering-context-engineering-tools) · Claude Cookbook
- [Context Engineering 2.0: The Context of Context Engineering](https://arxiv.org/pdf/2510.26493) · arXiv 2510.26493
- [Firecrawl](https://www.firecrawl.dev/blog/context-engineering) · [Elastic Search Labs](https://www.elastic.co/search-labs/blog/context-engineering-vs-prompt-engineering) · [Atlan](https://atlan.com/know/context-engineering-vs-prompt-engineering/) · [An Illustrated Guide to Context Engineering](https://karozieminski.substack.com/p/context-engineering-product-builders-guide-2026)

**Context rot and isolation**
- [Context isolation in coding agent loops](https://depot.dev/blog/context-isolation-in-coding-agent-loops) · Depot
- [Diagnosing and Mitigating Context Rot in Long-horizon Search](https://arxiv.org/pdf/2606.29718) · arXiv 2606.29718
- [Morph](https://www.morphllm.com/context-rot) · [Redis](https://redis.io/blog/context-rot/)

**Prompting overviews**
- [Prompt Engineering 2026: The Frameworks That Actually Work](https://pasqualepillitteri.it/en/news/1090/prompt-engineering-2026-frameworks-complete-guide)
- [Chain of Thought Prompting in 2026](https://futureagi.com/blog/chain-of-thought-prompting-ai-2025/)

---

## D — retrieval failed

- [Prompting v2026 — Release Notes: 3 breaking changes, 5 deprecations](https://medium.com/@AshJai/prompting-v2026-release-notes-3c453754add3) — WebFetch returned an empty error. **Nothing from it entered the design.**

---

## In-repo documents that shaped the form

Content came from the sources above; *form* came from these.

- `skills/meta/author-skills/SKILL.md` — the failure→form table, the no-op test, the
  duplication sweep, the token budget, the description rules for a
  `disable-model-invocation` skill
- `skills/meta/author-skills/influence-principles.md` — the skill-type → technique
  mapping behind the wording calibration recorded in `TESTS.md § REFACTOR`
- `skills/meta/author-skills/pressure-testing.md` — the RED/GREEN protocol and roster
  discipline this skill still owes
- `skills/discovery/clarify-decisions/SKILL.md` — the channel Iron Law and card recipe
  `forge-prompt` borrows rather than restates
- `skills/discovery/solve-problem/SKILL.md` and `TESTS.md` — the removed skill, whose
  provenance rules were kept. Read at `git show 320e91e:skills/discovery/solve-problem/SKILL.md`

---

## Search queries run

```
context engineering vs prompt engineering 2026 best practices agents
Anthropic effective context engineering for AI agents guidance
prompting reasoning models 2026 what no longer works chain of thought role prompting obsolete
how to write a good prompt for a coding agent feature request 2026 spec-driven brief structure
underspecification ambiguity LLM coding agent failure clarifying questions research 2026
"context rot" long context degradation 2026 findings implications for prompt length
anchoring bias LLM agents own earlier output same context self-consistency reluctance to revise 2026
context isolation fresh context subagent reduces bias multi-step agent pipeline error propagation 2026
```

## Open verification work

1. Read the four **tier B** sources and confirm the claims attributed to them. The
   anchoring-mitigation claim gates a design decision.
2. Recover effect sizes from the two **tier A′** PDFs, or downgrade the confidence with
   which `TESTS.md § RED-4` leans on them.
3. Neither of these blocks the skill; both change how firmly its rationale can be stated.
