---
name: brainstorm
description: Use at the very start of the idea-to-ship chain — when the user wants to
  add, build, or change a feature, behavior, or component, or to start a whole
  new project, and no requirements, design, or code exist yet. Triggers on
  "let's add…", "can we build…", "I'm thinking about…", "we should support…"
  before implementation has begun.
---

# Brainstorm

Turn a raw idea into an agreed shape ready for spec work, through dialogue — not code.

Shaping a *new* feature or project (nothing spec'd yet) is this skill. A small in-scope change to an **already-shipped, spec'd** feature is `amend` instead — it reads the existing spec and routes the change to the light lane, escalating back here only when the change is genuinely new scope. If you were handed such a change, hand it to `amend`.

<HARD-GATE>
Write NO code, scaffold NOTHING, and invoke NO implementation skill until this checklist has run and you have stated the ceremony tier out loud. For tier 0 the only permitted exit is `tdd`, and only after the tier is spoken; for tier ≥1, requirements are written and approved first. The only artifacts this skill may touch are notes, the glossary (CONTEXT.md), ADRs, and — via its sub-skills — research notes and explicitly-marked throwaway prototypes. This holds for EVERY request, no matter how simple it looks.
</HARD-GATE>

## "Too simple to need a design" is the trap

Small requests are exactly where unexamined assumptions burn the most work, because nobody bothered to check them. The output can be tiny — a tier decision and three sentences — but the process runs every time.

| Thought | Reality |
|---|---|
| "This is a one-liner, designing it is overhead" | Deciding it is tier 0 IS the design step — say so explicitly and move on. Skipping the decision is the overhead. |
| "The user already told me exactly what to build" | They told you a solution. You haven't confirmed the problem, the constraints, or what must keep working. |
| "I'll sketch a little code to clarify my thinking" | That's a prototype. Run the `prototype` sub-skill so it's throwaway by contract, not accidental production code. |
| "I'll write requirements after I confirm the approach compiles" | Code-first inverts the gate. Evidence questions get a research/prototype detour; requirements still come first. |
| "Scaffolding isn't really implementation" | A repo skeleton is a stack decision enacted without approval. It's implementation. |
| "We talked enough, I basically know the answer" | If it isn't in an approved requirements.md, it lives only in this chat and dies with it. |

**Red flags — stop and return to the checklist if you notice yourself:** opening an editor to "just try something"; running a generator/scaffolder; answering your own open question instead of asking; presenting one approach as the only option; drifting from interviewing into implementing.

## Checklist

Create a todo for each item and complete them in order.

**Right-size with an early tier read.** Once step 1 gives you the context, make a
*provisional* tier call:

- **Plainly tier 0** — a typo, recolor, label, or copy edit, with no behavior
  change, no unconfirmed assumption, and nothing to guard → brief step 2, skip
  steps 3–4, then step 5.
- **Anything else** — a behavior change, an unknown, or a real design choice →
  the full path.

Provisional means provisional: if step 2 surfaces any of those, it was never tier 0
— escalate to the full path.

### 1. Explore project context

Read `CONTEXT.md` (use its vocabulary from here on) and `docs/specs/INDEX.md` (the feature codes and specs that already exist) directly — they are small and you need them in context. When `docs/product/vision.md` exists, read it too and — once you grasp the idea — state whether it falls inside the stated product scope (an out-of-scope idea is worth surfacing before any spec work); if it does not exist, skip this, the layer is optional. For anything heavier — code, docs, and recent commits near this idea — dispatch a **scan subagent** that explores and writes a findings digest to `.skills/<slug>-scan.md` (what exists near the idea, the files and seams it touches, applicable constraints — findings, not file dumps), returning only that path; work from the digest instead of pulling raw files into this conversation. (No subagents in this harness? Read the few relevant files directly.) If `docs/agents/project.md` or these files are missing, say so, suggest running `setup-repo`, and continue with what you have.

Then check whether the idea already exists. Search `docs/specs/` for overlap: grep the
idea's candidate feature codes and key terms across `requirements.md` files, and cross-check
the scan's candidate file paths against what existing specs already own (grep those paths in
`design.md`/`tasks.md`). Read any match and present the neighbor as a summary **card** (not
the full spec) — its feature code, owned paths, and Out-of-Scope list show what it already
covers. `docs/specs/INDEX.md` is the registry to consult first. This never blocks the gate:
if nothing overlaps, say so and move on; if `docs/specs/` does not exist yet, note it and
continue with manual exploration.

**Done when:** you can state in one paragraph what the project is, what already exists near this idea, and which glossary terms apply — and you have stated which existing features share this idea's surface and how the new idea differs (citing feature codes), or that no existing feature shares its surface.

### 2. Interview

REQUIRED SUB-SKILL: use `grilling` — it owns the single question channel. (Provisional tier 0 from the early read? Right-size this: confirm the problem, the one constraint, and what must keep working in a question or two — not a full decision-tree walk — and if nothing new surfaces, proceed to step 5.)

Keep `domain-modeling` active as a **passive** side effect for the whole interview: record a term to `CONTEXT.md` the instant it settles and cross-reference the code — but it does not open a second question channel. A term that needs the user (a challenge, a disambiguation, an edge-case probe) becomes the next question in `grilling`'s one-at-a-time stream, never a competing interruption (REQUIRED SUB-SKILL: use `domain-modeling`).

Before drilling into details, check scope: if the request spans multiple independent subsystems, stop refining and decompose first (step 5).

**Done when:** the user has answered every open decision and no unexplored branch remains.

### 3. Detour when a question needs evidence, not opinion

*Full-path only; tier 0 skips this.*

Some questions can't be answered by preference. When the honest answer is "we'd have to check":

- Facts about external systems, APIs, libraries, or standards → REQUIRED SUB-SKILL: use `research` (primary sources, cited note).
- "Does this model/flow actually feel right?" → REQUIRED SUB-SKILL: use `prototype` (runnable throwaway answer).

Return to the interview with the evidence and put the decision back to the user.

**Done when:** no pending question is being answered by guesswork.

### 4. Propose approaches

*Full-path only; tier 0 skips this.*

Present 2–3 genuinely different approaches with trade-offs. Lead with your recommendation and why. YAGNI-prune every option. The user picks.

**Done when:** the user has chosen an approach (possibly a hybrid).

### 5. Decide the ceremony tier — out loud

State the tier explicitly and why:

| Tier | When | What follows |
|---|---|---|
| **0** | typo-level, no behavior change | no spec — go straight to `tdd` |
| **1** | behavior change ≤ ~half a day | mini-spec: fix REQ + SHALL-CONTINUE-TO guard in the owning requirements.md |
| **2** | multi-task feature | full requirements → design → plan triad |

If the work spans multiple independent subsystems, decompose it here: name the sub-features, their relationships, and build order. Each sub-feature gets its own full spec cycle; brainstorm continues with the first one only.

**Done when:** you have said "This is tier N because ..." and, if decomposed, listed the sub-features and which one goes first.

### 6. Terminal state

- **Tier ≥ 1:** REQUIRED SUB-SKILL: use `write-requirements`. This is the ONLY exit. Do not write code, do not scaffold, do not invoke any implementation or design skill directly — requirements come first and carry their own approval gate.
- **Tier 0:** state the tier, then REQUIRED SUB-SKILL: use `tdd`.

**Done when:** `write-requirements` has been invoked (tier ≥1) or the tier-0 handoff is stated.
