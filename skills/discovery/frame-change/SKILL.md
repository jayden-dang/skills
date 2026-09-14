---
name: frame-change
version: 2.2.0
description: Use at the very start of the idea-to-ship chain — when the user wants to
  add, build, or change a feature, behavior, or component, or to start a new
  project, and the asked-for behavior has no spec yet. Produces an agreed shape
  and a spoken ceremony tier. Triggers on "let's add…", "can we build…",
  "I'm thinking about…", "we should support…" before implementation has begun.
---

# Frame Change

Turn a raw idea into an agreed shape through dialogue, not code. Trust product
judgment once the open set is named; do not script the interview as an itinerary.

**Where this sits:** first stage. Tier 0 exits to `test-first`; tier 1 to a
mini-spec in `specify-behavior`; tier 2 walks the full triad. Do not pre-load
downstream checklists. A small in-scope change to an already-shipped spec'd
feature is `amend-feature` — hand it there.

<HARD-GATE>
Write NO code, scaffold NOTHING, and invoke NO implementation skill until this
checklist has run and you have stated the ceremony tier out loud. For tier 0
the only permitted exit is `test-first`, and only after the tier is spoken; for
tier ≥1, requirements are written and approved first. The only artifacts this
skill may touch are notes, the glossary (CONTEXT.md), ADRs, the roadmap
(`docs/roadmap/INDEX.md`, and only via `plan-milestones` at step 5), and — via
its sub-skills — research notes, explicitly-marked throwaway run-spikes, and
the reverse-features overlay. This holds for EVERY request, no matter how
simple it looks.
</HARD-GATE>

| Thought | Reality |
|---|---|
| "This is a one-liner, designing it is overhead" | Deciding it is tier 0 IS the design step. Say so and move on. |
| "I'll sketch a little code to clarify my thinking" | That is a run-spike. REQUIRED SUB-SKILL: use `run-spike` so it is throwaway by contract. |
| "Scaffolding isn't really implementation" | A repo skeleton is a stack decision. It is implementation. |
| "The other sub-features aren't in scope, so Out-of-Scope" | Out-of-Scope records a rejection. Work you intend later is deferred via `plan-milestones`. |
| "I'll just invoke /map-features myself" | `/map-features` is user-invoked — name it only. |
| "INDEX is small — paste all 120 rows" | Catalog is query-first; `catalog-query.md` is the one home. |

## Checklist

**Todos first — GATE.** Before reading `CONTEXT.md` or asking a question, put
this skill's six steps on a visible list (harness todo tool, else a checklist
in the first reply). Downstream stages own their own lists. Check each off
only when its **Done when** is met.

**Right-size.** After step 1: plainly tier 0 (typo, recolor, copy, no behavior
change, no unconfirmed assumption) → brief step 2, skip 3–4, then step 5.
Anything else → the full path. If step 2 surfaces a behavior change, escalate.

### 1. Explore project context

Read `CONTEXT.md`. Do not paste `docs/specs/INDEX.md` into context. Load
`load-subgraph`'s `catalog-query.md` and run it (mode, query recipe, context
caps, exact CODE lookup), including any active OBS.

Read **Project posture** in `docs/agents/project.md` when present. WHEN Project
posture or `## Team` is present, read `project-posture.md` beside this file and
follow it exactly. Missing posture: proceed without right-sizing. **Band never
changes tier rules or Iron Laws.** When `docs/product/vision.md` exists, state
whether the idea falls inside product scope.

WHEN the idea touches users, success criteria, or product principles, read
`product-context.md` beside this file and follow it exactly.

Dispatch a **scan subagent** for code, docs, and recent commits near the idea
→ `.skills/<CODE>/scan.md` (or `.skills/_pending-<slug>/scan.md` before CODE).
Work from the digest. No subagents? Read the few relevant files. Missing
`docs/agents/project.md` → say so, suggest `configure-repo`, continue.

The digest MUST include a **Blindspot** section: territory-specific traps,
historical constraints, and questions a newcomer would not know to ask —
grounded in this repo. Low familiarity → surface Blindspot before the first
preference question in step 2.

**Guarantee check — REQUIRED before a safety word reaches the user, and a word
already in their ask counts.** *Safe, atomic, idempotent, exactly-once, never
double-, ordered, unique* — inheriting one from the request as settled is the
same claim, made silently. For each: name the **failure it must survive** and
the **`file:line` that makes it survive**; take the failure this code path
makes observable (a timeout, a crash mid-write, a retry, a second caller) and
call the others untested. No line → say **unverified** as you state it, and log
a known unknown. Describing a mechanism is not checking it. Three runs quoted
`idem.release(key)` from a catch that drops the key on PSP timeout and called
it "never double-refunds."

Then check whether the idea already exists. REQUIRED SUB-SKILL: use
`load-subgraph` with the idea's **key terms** and any scan **candidate paths**.
Present neighbor cards from schema 1.1; surface **`owns_coverage`**. Grounded
claims: follow `skills/execution/load-subgraph/references/grounded-claims.md`.
Hold a valid retrieval package for nested `clarify-decisions`.
*Done when: neighbor cards plus OWNS coverage are stated, or an explicit "no
overlap" with emptiness/coverage stated per grounded-claims.md.*

**Knowns inventory (REQUIRED before step 2).** Four short bullets (chat is
fine; optional `.skills/<CODE>/knowns.md`):

- **Known knowns / locks** — settled constraints and must-keep behaviors.
- **Known unknowns** — open questions that need research, run-spike, or a user decision.
- **Unknown knowns** — taste the user can recognize but not yet specify.
- **Assumptions (not locks)** — solution shape the user proposed. Never promote
  an assumption into a requirement SHALL until it is chosen as a lock.

WHERE the user points at a pathfind knowns package, seed from it. Do not re-open
closed pathfind decisions. Pathfind knowns do not replace Blindspot or a
brownfield scan.

**Done when:** one paragraph on what the project is, what exists near the idea,
which glossary terms apply, which features share the surface (or none) —
**and** the Knowns inventory and Blindspot list exist.

### 2. Interview

Stay on this checklist. Apply the `clarify-decisions` **protocol** for the
single question channel. Do not invent a thinner interview.

REQUIRED SUB-SKILL: use `clarify-decisions`. Keep `define-domain` as a passive
side effect (REQUIRED SUB-SKILL: use `define-domain`).

Provisional tier 0? Mark the nested interview **brief / tier-0** so coverage
stays OFF. Confirm problem, one constraint, and must-keep-working, then step 5
if nothing new surfaces.

If the request spans multiple independent subsystems, stop refining and
decompose at step 5.

**Done when:** the open set is empty of high-blast judgment calls and the
clarify-decisions close package is confirmed.

### 3. Detour when a question needs evidence

*Full-path only; tier 0 skips this.*

- External facts, APIs, libraries, standards → REQUIRED SUB-SKILL: use `research`
  (Context7 MCP for current library docs).
- "Does this model/flow actually feel right?" → REQUIRED SUB-SKILL: use `run-spike`.

Return with the evidence and put the decision back to the user.
**Done when:** no pending question is being answered by guesswork.

### 4. Propose approaches

*Full-path only; tier 0 skips this.* Present 2–3 genuinely different approaches
with trade-offs. Lead with a recommendation. YAGNI-prune. The user picks.
**Done when:** the user has chosen an approach (possibly a hybrid).

### 5. Decide the ceremony tier — out loud

| Tier | When | What follows |
|---|---|---|
| **0** | typo-level, no behavior change | no spec — `test-first` |
| **1** | behavior change ≤ ~half a day | mini-spec: fix REQ + SHALL-CONTINUE-TO guard |
| **2** | multi-task feature | full requirements → design → plan triad |

If the work spans multiple independent subsystems, decompose here. Two or more
sub-features: REQUIRED SUB-SKILL: use `plan-milestones` so every sub-feature
exists as a `ROAD-N`. Deferred, not declined.

**Done when:** you have said "This is tier N because ..." and, if decomposed,
every sub-feature exists as a `ROAD-N` and you have named which one goes first.

### 6. Terminal state

- **Tier ≥ 1:** REQUIRED SUB-SKILL: use `specify-behavior`. The ONLY exit.
- **Tier 0:** state the tier, then REQUIRED SUB-SKILL: use `test-first`.

**Done when:** `specify-behavior` has been invoked (tier ≥1) or the tier-0
write-handoff is stated.
