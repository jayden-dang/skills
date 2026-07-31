# Phase 1 — Discovery

**Skills:** [`frame-change`](../skills/frame-change.md) · [`clarify-decisions`](../skills/clarify-decisions.md) · [`research`](../skills/research.md) · [`run-spike`](../skills/run-spike.md) · [`define-domain`](../skills/define-domain.md)

**Produces:** an agreed shape, a stated ceremony tier, an updated glossary, possibly an ADR, and — for tier ≥ 1 — an invocation of `specify-behavior`.

**Produces no code.** This is the gate.

## The hard gate

`frame-change` opens with it:

> Write NO code, scaffold NOTHING, and invoke NO implementation skill until this checklist has run and you have stated the ceremony tier out loud.

The only artifacts it may touch are notes, the glossary (`CONTEXT.md`), ADRs, and — through its sub-skills — research notes and explicitly-marked throwaway run-spikes.

"Scaffolding isn't really implementation" is named and rejected: a repo skeleton is a stack decision enacted without approval.

## "Too simple to need a design" is the trap

Small requests are exactly where unexamined assumptions burn the most work, because nobody bothered to check them. The *output* can be tiny — a tier decision and three sentences. The *process* runs every time.

Watch for these, and return to the checklist if you catch yourself: opening an editor to "just try something"; running a generator or scaffolder; answering your own open question instead of asking it; presenting one approach as the only option; drifting from interviewing into implementing.

## The checklist

### 1. Explore project context

Read `CONTEXT.md` (and use its vocabulary from here on) and `docs/specs/INDEX.md` directly — they are small and you need them in context.

For anything heavier, dispatch a **scan subagent** that explores the code, docs, and recent commits near the idea, writes a findings digest to `.skills/<slug>-scan.md`, and returns only that path. Work from the digest. The point is to keep raw source out of the conversation that is about to hold every design decision.

Then run the [feature-overlap](../concepts/feature-graph.md) search — an inline `grep` over `docs/specs/` for the new idea's key terms and candidate file paths:

```bash
grep -rli -e '<term>' -e '<candidate-path>' docs/specs/
```

Any feature whose spec matches is read as its **Summary card, not its full spec** — the digest at the top of the spec (code, name, owned paths, Out of Scope). Those owned paths and the Out-of-Scope list show what the neighbor already covers.

**Done when** you can state in one paragraph what the project is, what already exists near this idea, and which glossary terms apply — *and* you have named which existing features share this idea's surface and how the new idea differs, citing feature codes, or stated that none do.

### 2. Interview

`clarify-decisions` takes over. The load-bearing rules:

- **Inline chat only** — never a truncated MCQ picker; every question needs full context.
- **One question card per message** — radius, why it matters, options with consequences, recommendation. Wait for the answer.
- **Blast-radius first** — architecture, data, and auth before polish, even when the user asks for color first.
- **Walk every branch** of the decision tree, in dependency order.
- **Facts are yours; decisions are the user's.** Look up the codebase and the parent's Blindspot / Knowns digests; only judgment calls go to the user.
- **Close package** — decisions table + ready-to-paste constraints + explicit confirmation before anything is enacted.

`define-domain` runs as a side effect throughout: challenge terms against the glossary the moment usage conflicts with it, sharpen fuzzy language into one canonical term, stress-test relationships with concrete edge cases, and cross-reference the code when the user asserts how something works. Update `CONTEXT.md` **inline, the instant a term settles** — batched glossary edits get forgotten.

Before drilling into details, check scope. If the request spans multiple independent subsystems, stop refining and decompose (step 5).

### 3. Detour when a question needs evidence, not opinion

Some questions cannot be answered by preference. When the honest answer is "we'd have to check":

- **Facts about external systems, APIs, libraries, or standards** → `research`. Primary sources only — the source that *owns* the fact. Tutorials and blog posts are leads, not evidence; chase every claim back to the owning source and cite that. The output is exactly one markdown file, every claim carrying a citation, conclusions separated from what the sources say, ending in an "Open decisions" section.

- **"Does this model or flow actually feel right?"** → `run-spike`. Throwaway code whose only job is to answer one design question. Two branches: a terminal app over a pure logic module, or several structurally different variants of one screen. Six rules bind both — throwaway from day one and marked as such, one command to run, no persistence, no polish, surface internal state, delete or absorb when done.

The run-spike's code does not matter afterward. **Only the answer does.** Capture it in an ADR, a requirement, or the commit message that deletes the run-spike.

Then return to the interview with the evidence and put the decision back to the user. Research informs; it never decides.

**Done when** no pending question is being answered by guesswork.

### 4. Propose approaches

Present two or three genuinely different approaches with trade-offs. Lead with your recommendation and why. YAGNI-prune every option. The user picks — possibly a hybrid.

### 5. Decide the ceremony tier — out loud

| Tier | When | What follows |
|---|---|---|
| **0** | typo-level, no behavior change | no spec — straight to `test-first` |
| **1** | behavior change ≤ ~half a day | mini-spec: a fix requirement + a `SHALL CONTINUE TO` guard |
| **2** | multi-task feature | the full requirements → design → plan triad |

If the work spans multiple independent subsystems, decompose here: name the sub-features, their relationships, and the build order. Each gets its own full spec cycle; `frame-change` continues with the first one only.

**Done when** you have literally said "This is tier N because …".

### 6. Terminal state

- **Tier ≥ 1:** invoke `specify-behavior`. This is the *only* exit. No code, no scaffolding, no design skill invoked directly — requirements come first and carry their own approval gate.
- **Tier 0:** hand off to `test-first` and say so.

## ADRs — sparingly

`define-domain` owns the ADR gate, and it is a **three-part AND**:

1. **Hard to reverse** — changing course later carries real cost.
2. **Surprising without context** — a future reader would ask "why on earth this way?"
3. **A real trade-off** — genuine alternatives existed and one was chosen for specific reasons.

Any one missing means no ADR. The body is one to three sentences. Recording *that* and *why* is the value, not filling sections.

## When it is `amend-feature` instead

`frame-change` is for shaping something *new*. A small in-scope change to an already-shipped, spec'd feature is [`amend-feature`](../skills/amend-feature.md) — it reads the existing triad, classifies the change against it, and routes to the lightest lane, escalating back here only when the change is genuinely new scope.

If you were handed such a change, hand it to `amend-feature`.

## Next

→ [Phase 2 — Specification](specification.md)

## See also

- [The gates](../concepts/gates.md) — why the hard gate is written as a prohibition
- [Ceremony tiers](../methodology/ceremony-tiers.md) — the decision this phase exists to make
- [Feature overlap](../concepts/feature-graph.md) — the `docs/specs/` search in step 1
