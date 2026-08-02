---
name: frame-change
description: Use at the very start of the idea-to-ship chain — when the user wants to
  add, build, or change a feature, behavior, or component, or to start a whole
  new project, and no requirements, design, or code exist yet. Triggers on
  "let's add…", "can we build…", "I'm thinking about…", "we should support…"
  before implementation has begun.
---

# Frame Change

Turn a raw idea into an agreed shape ready for spec work, through dialogue — not code.

**Where this sits:** `frame-change → (specify-behavior → design-solution → plan-tasks) → build-in-waves`. You are at **frame-change** — the first stage. Which later stages run is decided by the tier in step 5 (tier 0 skips straight to `test-first`; tier 1 stops at a mini-spec in `specify-behavior`; only tier 2 walks the full triad). Each of those stages owns its own todo list and creates it when invoked — do **not** pre-load their steps into this skill's list.

Shaping a *new* feature or project (nothing spec'd yet) is this skill. A small in-scope change to an **already-shipped, spec'd** feature is `amend-feature` instead — it reads the existing spec and routes the change to the light lane, escalating back here only when the change is genuinely new scope. If you were handed such a change, hand it to `amend-feature`.

<HARD-GATE>
Write NO code, scaffold NOTHING, and invoke NO implementation skill until this checklist has run and you have stated the ceremony tier out loud. For tier 0 the only permitted exit is `test-first`, and only after the tier is spoken; for tier ≥1, requirements are written and approved first. The only artifacts this skill may touch are notes, the glossary (CONTEXT.md), ADRs, the roadmap (`docs/roadmap/INDEX.md`, and only via `plan-milestones` at step 5), and — via its sub-skills — research notes and explicitly-marked throwaway run-spikes. This holds for EVERY request, no matter how simple it looks.
</HARD-GATE>

## "Too simple to need a design" is the trap

Small requests are exactly where unexamined assumptions burn the most work, because nobody bothered to check them. The output can be tiny — a tier decision and three sentences — but the process runs every time.

| Thought | Reality |
|---|---|
| "This is a one-liner, designing it is overhead" | Deciding it is tier 0 IS the design step — say so explicitly and move on. Skipping the decision is the overhead. |
| "The user already told me exactly what to build" | They told you a solution. You haven't confirmed the problem, the constraints, or what must keep working. |
| "I'll sketch a little code to clarify my thinking" | That's a run-spike. Run the `run-spike` sub-skill so it's throwaway by contract, not accidental production code. |
| "I'll write requirements after I confirm the approach compiles" | Code-first inverts the gate. Evidence questions get a research/run-spike detour; requirements still come first. |
| "Scaffolding isn't really implementation" | A repo skeleton is a stack decision enacted without approval. It's implementation. |
| "We talked enough, I basically know the answer" | If it isn't in an approved requirements.md, it lives only in this chat and dies with it. |
| "The other sub-features aren't in scope right now, so Out-of-Scope is the right home" | Out-of-Scope and an ADR record a *rejection*. Work you intend to do later is deferred to a milestone via `plan-milestones` — declining it destroys the plan you just made. |

**Red flags — stop and return to the checklist if you notice yourself:** opening an editor to "just try something"; running a generator/scaffolder; answering your own open question instead of asking; presenting one approach as the only option; drifting from interviewing into implementing.

## Checklist

**Todos first — GATE.** The very first action of every frame-change — before you read `CONTEXT.md`, dispatch a scan, or ask a single question — is to create the todo list: one todo per checklist item below (steps 1–6) via your harness's todo tool (`TodoWrite` in Claude Code; the equivalent in Kimi, Codex, or wherever this runs). This fires for EVERY request, no matter how simple it looks — the HARD-GATE above is what you must NOT do; this is what you MUST do first. The list holds this skill's six steps only; do not add downstream stages (`specify-behavior`, `design-solution`, `plan-tasks`) — each creates its own list on handoff. Do not proceed until the list exists, then complete the items in order, checking each off only when its **Done when** is met.

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

Read `CONTEXT.md` (use its vocabulary from here on) and `docs/specs/INDEX.md` (the feature codes and specs that already exist) directly — they are small and you need them in context. Read the **Project posture** in `docs/agents/project.md` when present — its delivery intent and lifecycle stage right-size the whole interview: a Run Spike / Research / Learning posture means do not burn questions on data migration, backward compatibility, or deprecation cost; a released / Scaling / Maintenance posture means weigh exactly those heavily. When the posture section is absent, do not assume one — proceed without right-sizing. Read **`## Team`** in the same file when present: if the **roster** is non-empty or a **Workflow band** override is set, derive the **band** and apply **packaging** using the rules and matrix written *in that section* (do not re-copy them here). State the band once. Solo: leaner peer-coordination language in approaches. Small/Multi: surface ownership and review capacity in approach trade-offs. Empty roster + blank override, or missing Team: do not invent a team and do not hard-fail. **Band never changes tier rules or Iron Laws.** When `docs/product/vision.md` exists, read it too and — once you grasp the idea — state whether it falls inside the stated product scope (an out-of-scope idea is worth surfacing before any spec work); if it does not exist, skip this, the layer is optional.

### Product context docs (optional)

**Applicability:** the idea touches users, success criteria, or product principles.

**Authority:** for each of `docs/product/personas.md`, `metrics.md`, `principles.md` —
**Approved** only when `Status: Approved` and the structural validator under
`skills/project/define-system-doc/validators/product/` passes; otherwise Absent or
Non-authoritative. Vision remains `docs/product/vision.md` (define-project).

**When Approved and applicable:** consult the doc(s) when checking scope, users, or
goals; they do not outrank vision non-goals/hard constraints.

**When absent or non-authoritative:** CONTINUE without failing solely for absence.
If personas/metrics/principles would materially right-size the interview, suggest
**at most once per entry key per frame-change run**
`/define-system-doc product/personas|metrics|principles` as fits; **NEVER**
auto-invoke `define-system-doc` (ARCH-5). For anything heavier — code, docs, and recent commits near this idea — dispatch a **scan subagent** that explores and writes a findings digest to `.skills/<CODE>/scan.md (or `.skills/_pending-<slug>/scan.md` before CODE)` (what exists near the idea, the files and seams it touches, applicable constraints — findings, not file dumps), returning only that path; work from the digest instead of pulling raw files into this conversation. (No subagents in this harness? Read the few relevant files directly.) If `docs/agents/project.md` or these files are missing, say so, suggest running `configure-repo`, and continue with what you have.

The scan digest (or your direct read) MUST include a **Blindspot** section: territory-specific traps, historical constraints, and questions a newcomer would not know to ask — grounded in this repo, not generic advice. When the user signals low familiarity with the module or domain, surface that Blindspot list to them before the first preference question in step 2.

Then check whether the idea already exists. REQUIRED SUB-SKILL: use `load-subgraph`
with the idea's **key terms** and any scan **candidate paths** (query `subgraph` or
`neighbors` as fits) so P0 term seeds and P1 path-derived structure both contribute.
Present neighbor **cards** from schema 1.1 fields (`path_evidence`, `term_evidence`,
`via_traces`); surface **`owns_coverage`**. **Grounded claims** (one home): follow
`skills/execution/load-subgraph/references/grounded-claims.md` for every conclusion
from the package. Hold a valid **retrieval package** for nested `clarify-decisions`
reuse.
*Done when: neighbor cards plus OWNS coverage are stated, or an explicit "no overlap"
(or no specs) with emptiness/coverage stated per grounded-claims.md.*

**Knowns inventory (REQUIRED before step 2).** Write four short bullets the rest of
the chain can reuse (chat is fine; optional `.skills/<CODE>/knowns.md (or `.skills/_pending-<slug>/knowns.md` before CODE)`):

- **Known knowns / locks** — hard constraints and outcomes that are settled (must-keep behaviors, posture constraints, explicit non-negotiables).
- **Known unknowns** — open questions that need research, run-spike, or a user decision.
- **Unknown knowns** — taste or standards the user can recognize but not yet specify (route via `run-spike` or references, not more prose questions alone).
- **Assumptions (not locks)** — solution shape the user proposed that is still a hypothesis until checked against territory (codebase, APIs, history). Never promote an assumption into a requirement SHALL until it is chosen as a lock.

**Pathfind knowns (when present).** WHERE the user points at a pathfind knowns package
(`.skills/pathfind/**/knowns.md`) or an open pathfind map, **seed** this inventory from
that package's locks and known unknowns. Do **not** re-open closed pathfind decisions
unless the user reopens the ticket. Pathfind knowns do **not** replace Blindspot or a
brownfield territory scan — still require Blindspot awareness on brownfield work.

**Done when:** you can state in one paragraph what the project is, what already exists near this idea, and which glossary terms apply — and you have stated which existing features share this idea's surface and how the new idea differs (citing feature codes), or that no existing feature shares its surface — **and** the Knowns inventory and Blindspot list exist.

### 2. Interview

This remains frame-change step 2 — **not** a stage write-handoff and not a new skill session. Apply the `clarify-decisions` **protocol** for the single question channel; keep this skill's todo list live; do not open a competing list or re-announce that you are "switching to clarify-decisions."

**Protocol (always):** apply `clarify-decisions` end-to-end for this step — channel, open-set stop, rich card slots, close package. Do **not** invent a thinner interview from this paragraph; the card recipe and stop rule live only in `clarify-decisions`.

REQUIRED SUB-SKILL: use `clarify-decisions` for the full rules (channel Iron Law, open-set Iron Law, rich question-card recipe, pre-implementation interview map, close package, posture pruning, team-band packaging, no-enact gate, nested-todo contract). Load it once when this step starts if it is not already in context; then stay on this checklist.

(Provisional tier 0 from the early read? Right-size this: confirm the problem, the one constraint, and what must keep working in a question or two — not a full decision-tree walk — and if nothing new surfaces, proceed to step 5.)

Keep `define-domain` active as a **passive** side effect for the whole interview: record a term to `CONTEXT.md` the instant it settles and cross-reference the code — but it does not open a second question channel. A term that needs the user (a challenge, a disambiguation, an edge-case probe) becomes the next question in the interview's one-at-a-time stream, never a competing interruption (REQUIRED SUB-SKILL: use `define-domain`).

Before drilling into details, check scope: if the request spans multiple independent subsystems, stop refining and decompose first (step 5).

**Done when:** the open set is empty of high-blast judgment calls and the clarify-decisions close package is confirmed.

### 3. Detour when a question needs evidence, not opinion

*Full-path only; tier 0 skips this.*

Some questions can't be answered by preference. When the honest answer is "we'd have to check":

- Facts about external systems, APIs, libraries, or standards → REQUIRED SUB-SKILL: use `research` (primary sources, cited note — it reaches for the Context7 MCP for current, version-accurate library facts rather than training-cutoff memory).
- "Does this model/flow actually feel right?" → REQUIRED SUB-SKILL: use `run-spike` (runnable throwaway answer).

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
| **0** | typo-level, no behavior change | no spec — go straight to `test-first` |
| **1** | behavior change ≤ ~half a day | mini-spec: fix REQ + SHALL-CONTINUE-TO guard in the owning requirements.md |
| **2** | multi-task feature | full requirements → design → plan triad |

If the work spans multiple independent subsystems, decompose it here: name the sub-features, their relationships, and build order. Each sub-feature gets its own full spec cycle.

**Two or more sub-features means the decomposition gets written down before you go any further.** REQUIRED SUB-SKILL: use `plan-milestones` to persist every sub-feature as a `ROAD-N` item — appending to `docs/roadmap/INDEX.md` when it already exists, authoring it when it does not. A sub-feature you are not building first is **deferred to a later milestone**, not declined: an Out-of-Scope line or an ADR records a *rejection*, and a decomposition is not a rejection. Then continue with the first item only.

**Done when:** you have said "This is tier N because ..." and, if decomposed, every sub-feature exists as a `ROAD-N` in `docs/roadmap/INDEX.md` and you have named which one goes first.

### 6. Terminal state

- **Tier ≥ 1:** REQUIRED SUB-SKILL: use `specify-behavior`. This is the ONLY exit. Do not write code, do not scaffold, do not invoke any implementation or design skill directly — requirements come first and carry their own approval gate.
- **Tier 0:** state the tier, then REQUIRED SUB-SKILL: use `test-first`.

**Done when:** `specify-behavior` has been invoked (tier ≥1) or the tier-0 write-handoff is stated.
