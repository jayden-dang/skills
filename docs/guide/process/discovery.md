# Phase 1 — Discovery

**Skills:** [`brainstorm`](../skills/brainstorm.md) · [`grilling`](../skills/grilling.md) · [`research`](../skills/research.md) · [`prototype`](../skills/prototype.md) · [`domain-modeling`](../skills/domain-modeling.md)

**Produces:** an agreed shape, a stated ceremony tier, an updated glossary, possibly an ADR, and — for tier ≥ 1 — an invocation of `write-requirements`.

**Produces no code.** This is the gate.

## The hard gate

`brainstorm` opens with it:

> Write NO code, scaffold NOTHING, and invoke NO implementation skill until this checklist has run and you have stated the ceremony tier out loud.

The only artifacts it may touch are notes, the glossary (`CONTEXT.md`), ADRs, and — through its sub-skills — research notes and explicitly-marked throwaway prototypes.

"Scaffolding isn't really implementation" is named and rejected: a repo skeleton is a stack decision enacted without approval.

## "Too simple to need a design" is the trap

Small requests are exactly where unexamined assumptions burn the most work, because nobody bothered to check them. The *output* can be tiny — a tier decision and three sentences. The *process* runs every time.

Watch for these, and return to the checklist if you catch yourself: opening an editor to "just try something"; running a generator or scaffolder; answering your own open question instead of asking it; presenting one approach as the only option; drifting from interviewing into implementing.

## The checklist

### 1. Explore project context

Read `CONTEXT.md` (and use its vocabulary from here on) and `docs/specs/INDEX.md` directly — they are small and you need them in context.

For anything heavier, dispatch a **scan subagent** that explores the code, docs, and recent commits near the idea, writes a findings digest to `.skills/<slug>-scan.md`, and returns only that path. Work from the digest. The point is to keep raw source out of the conversation that is about to hold every design decision.

Then run the [feature-graph](../concepts/feature-graph.md) dedup check:

```bash
node scripts/check-graph.mjs --query --json --path <candidate-file> --keyword <term>
```

Any returned features are presented as their **summary cards, not their full specs**. Each card's owned paths and Out-of-Scope list show what the neighbor already covers.

**Done when** you can state in one paragraph what the project is, what already exists near this idea, and which glossary terms apply — *and* you have named which existing features share this idea's surface and how the new idea differs, citing feature codes, or stated that none do.

### 2. Interview

`grilling` takes over. Its five rules are the whole method:

- **One question per message.** A wall of questions is bewildering; a single question gets a real answer.
- **Every question ships your recommended answer** and a one-line reason. The user can accept in two words or push back.
- **Walk every branch of the decision tree**, in dependency order. An early answer opens some branches and closes others.
- **Facts are yours; decisions are the user's.** If the answer already exists in the codebase or the docs, look it up. Never ask the user to recall what you can read.
- **Enact nothing** until the user explicitly confirms a shared understanding.

`domain-modeling` runs as a side effect throughout: challenge terms against the glossary the moment usage conflicts with it, sharpen fuzzy language into one canonical term, stress-test relationships with concrete edge cases, and cross-reference the code when the user asserts how something works. Update `CONTEXT.md` **inline, the instant a term settles** — batched glossary edits get forgotten.

Before drilling into details, check scope. If the request spans multiple independent subsystems, stop refining and decompose (step 5).

### 3. Detour when a question needs evidence, not opinion

Some questions cannot be answered by preference. When the honest answer is "we'd have to check":

- **Facts about external systems, APIs, libraries, or standards** → `research`. Primary sources only — the source that *owns* the fact. Tutorials and blog posts are leads, not evidence; chase every claim back to the owning source and cite that. The output is exactly one markdown file, every claim carrying a citation, conclusions separated from what the sources say, ending in an "Open decisions" section.

- **"Does this model or flow actually feel right?"** → `prototype`. Throwaway code whose only job is to answer one design question. Two branches: a terminal app over a pure logic module, or several structurally different variants of one screen. Six rules bind both — throwaway from day one and marked as such, one command to run, no persistence, no polish, surface internal state, delete or absorb when done.

The prototype's code does not matter afterward. **Only the answer does.** Capture it in an ADR, a requirement, or the commit message that deletes the prototype.

Then return to the interview with the evidence and put the decision back to the user. Research informs; it never decides.

**Done when** no pending question is being answered by guesswork.

### 4. Propose approaches

Present two or three genuinely different approaches with trade-offs. Lead with your recommendation and why. YAGNI-prune every option. The user picks — possibly a hybrid.

### 5. Decide the ceremony tier — out loud

| Tier | When | What follows |
|---|---|---|
| **0** | typo-level, no behavior change | no spec — straight to `tdd` |
| **1** | behavior change ≤ ~half a day | mini-spec: a fix requirement + a `SHALL CONTINUE TO` guard |
| **2** | multi-task feature | the full requirements → design → plan triad |

If the work spans multiple independent subsystems, decompose here: name the sub-features, their relationships, and the build order. Each gets its own full spec cycle; `brainstorm` continues with the first one only.

**Done when** you have literally said "This is tier N because …".

### 6. Terminal state

- **Tier ≥ 1:** invoke `write-requirements`. This is the *only* exit. No code, no scaffolding, no design skill invoked directly — requirements come first and carry their own approval gate.
- **Tier 0:** hand off to `tdd` and say so.

## ADRs — sparingly

`domain-modeling` owns the ADR gate, and it is a **three-part AND**:

1. **Hard to reverse** — changing course later carries real cost.
2. **Surprising without context** — a future reader would ask "why on earth this way?"
3. **A real trade-off** — genuine alternatives existed and one was chosen for specific reasons.

Any one missing means no ADR. The body is one to three sentences. Recording *that* and *why* is the value, not filling sections.

## When it is `amend` instead

`brainstorm` is for shaping something *new*. A small in-scope change to an already-shipped, spec'd feature is [`amend`](../skills/amend.md) — it reads the existing triad, classifies the change against it, and routes to the lightest lane, escalating back here only when the change is genuinely new scope.

If you were handed such a change, hand it to `amend`.

## Next

→ [Phase 2 — Specification](specification.md)

## See also

- [The gates](../concepts/gates.md) — why the hard gate is written as a prohibition
- [Ceremony tiers](../methodology/ceremony-tiers.md) — the decision this phase exists to make
- [The feature graph](../concepts/feature-graph.md) — the dedup check in step 1
