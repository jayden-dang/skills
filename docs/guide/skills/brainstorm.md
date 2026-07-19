# `brainstorm`

> The front door of the idea-to-ship chain. A raw idea becomes an agreed shape through dialogue, and no code is written until the ceremony tier has been said out loud.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | `CONTEXT.md` (glossary vocabulary), `docs/specs/INDEX.md` (existing feature codes and specs), `docs/agents/project.md`; code, docs, and recent commits near the idea via a scan subagent digest at `.skills/<slug>-scan.md` |
| **Writes** | notes, the glossary (`CONTEXT.md`), ADRs, and — via sub-skills — research notes and explicitly-marked throwaway prototypes; nothing else |
| **Calls** | [`grilling`](grilling.md), [`domain-modeling`](domain-modeling.md), [`research`](research.md), [`prototype`](prototype.md), [`write-requirements`](write-requirements.md) (tier ≥ 1), [`tdd`](tdd.md) (tier 0) |
| **Called by** | the user (entry point of the chain); [`amend`](amend.md) when a change turns out to be genuinely new scope |

## When it fires

At the very start of the idea-to-ship chain — the user wants to add, build, or change a feature, behavior, or component, or to start a whole new project, and no requirements, design, or code exist yet. It triggers on openers like "let's add…", "can we build…", "I'm thinking about…", and "we should support…" before implementation has begun.

`brainstorm` is for shaping something *new* — nothing spec'd yet.

A small in-scope change to an **already-shipped, spec'd** feature is [`amend`](amend.md) instead: it reads the existing spec and routes the change to the light lane, escalating back here only when the change is genuinely new scope. If you were handed such a change, hand it to `amend`. The two skills share a shape — both end on a spoken tier decision — but they start from opposite places: `brainstorm` from a blank page, `amend` from a spec that already exists.

## The hard gate

The skill opens with a prohibition that holds for **every** request, no matter how simple it looks:

> Write NO code, scaffold NOTHING, and invoke NO implementation skill until the checklist has run and the ceremony tier has been stated out loud.

The only artifacts the skill may touch are notes, the glossary, ADRs, and — through its sub-skills — research notes and explicitly-marked throwaway prototypes.

The gate has exactly two exits, and they are named exhaustively so there is no third path into code. For tier 0 the only permitted exit is [`tdd`](tdd.md), and only after the tier is spoken. For tier ≥ 1, requirements are written and approved first through [`write-requirements`](write-requirements.md), which carries its own approval gate. Scaffolding a repo skeleton counts as implementation — it enacts a stack decision without approval — so it too waits behind the gate.

## "Too simple to need a design" is the trap

Small requests are exactly where unexamined assumptions burn the most work, because nobody bothers to check them.

The output can be tiny — a tier decision and three sentences — but the process runs every time.

The skill carries a six-row rationalization table, each row a shortcut it exists to block. Read down the right column: every "Reality" is the thing the corresponding shortcut skips over.

| Thought | Reality |
|---|---|
| "This is a one-liner, designing it is overhead" | Deciding it is tier 0 IS the design step — say so explicitly and move on. Skipping the decision is the overhead. |
| "The user already told me exactly what to build" | They told you a solution. You haven't confirmed the problem, the constraints, or what must keep working. |
| "I'll sketch a little code to clarify my thinking" | That's a prototype. Run the `prototype` sub-skill so it's throwaway by contract, not accidental production code. |
| "I'll write requirements after I confirm the approach compiles" | Code-first inverts the gate. Evidence questions get a research/prototype detour; requirements still come first. |
| "Scaffolding isn't really implementation" | A repo skeleton is a stack decision enacted without approval. It's implementation. |
| "We talked enough, I basically know the answer" | If it isn't in an approved requirements.md, it lives only in this chat and dies with it. |

**Red flags — stop and return to the checklist** if you notice yourself: opening an editor to "just try something"; running a generator or scaffolder; answering your own open question instead of asking; presenting one approach as the only option; drifting from interviewing into implementing.

## The checklist

Each item is a todo, completed in order. The order matters: context before questions, questions before evidence, evidence before approaches, approaches before the tier. Skipping ahead is how unexamined assumptions survive to the spec.

1. **Explore project context.** Read `CONTEXT.md` (adopt its vocabulary from here on) and `docs/specs/INDEX.md` directly — they are small and needed in context. Read the **Project posture** in `docs/agents/project.md` when present and let it right-size the interview: a Prototype / Research / Learning posture means do not spend questions on data migration, backward compatibility, or deprecation; a Released / Scaling / Maintenance posture means weigh exactly those. For anything heavier, dispatch a scan subagent that writes a findings digest to `.skills/<slug>-scan.md` and returns only that path; work from the digest, not raw files. Then run the overlap check (below). If `docs/agents/project.md` or these files are missing, say so, suggest [`setup-repo`](setup-repo.md), and continue with what you have.
2. **Interview.** REQUIRED SUB-SKILL [`grilling`](grilling.md) — one question at a time, a recommended answer per question, every branch walked. Keep [`domain-modeling`](domain-modeling.md) active as a side effect throughout: challenge terms against the glossary, sharpen fuzzy language, and update `CONTEXT.md` the moment a term settles. If the request spans multiple independent subsystems, stop refining and decompose first (step 5).
3. **Detour when a question needs evidence, not opinion.** When the honest answer is "we'd have to check": facts about external systems, APIs, libraries, or standards go to [`research`](research.md) (primary sources, cited note); "does this model or flow actually feel right?" goes to [`prototype`](prototype.md) (a runnable throwaway answer). Return with the evidence and put the decision back to the user.
4. **Propose approaches.** Present 2–3 genuinely different approaches with trade-offs, lead with your recommendation and why, YAGNI-prune every option. The user picks.
5. **Decide the ceremony tier — out loud.** State the tier and why (table below). If the work spans multiple independent subsystems, decompose here: name the sub-features, their relationships, and build order; each gets its own full spec cycle and brainstorm continues with the first only.
6. **Terminal state.** Tier ≥ 1: invoke `write-requirements` — the ONLY exit; do not write code, scaffold, or invoke any implementation or design skill directly, because requirements come first and carry their own approval gate. Tier 0: hand off to `tdd` directly and say so.

## The overlap check

Step 1 searches the specs directly for a feature that already covers this surface. `docs/specs/INDEX.md` is the registry — it maps every feature code to its spec folder and the surface it owns — so start there, then `grep docs/specs/` for the idea's key terms and for the scan's candidate paths. Each hit points at a neighboring feature; read that feature's `requirements.md` header and present it as a short summary (not the full spec) — its owned paths and Out-of-Scope list show what the neighbor already covers, so the new idea can be positioned against or distinguished from them.

The check is a convenience, not a gate, so it never blocks progress:

- **No `INDEX.md`** — the registry has not been set up in this repo. Say so once, name [`setup-repo`](setup-repo.md) as the remedy, and say it **at most once per session**: a repo without the registry must not be nagged on every idea. Fall back to grepping `docs/specs/` directly.
- **No `docs/specs/` at all** — note there is nothing to check against yet and continue.

This also covers harnesses without subagents: when the scan step cannot dispatch one, read the few relevant files directly and grep the specs on the idea's terms by hand. The overlap check is there to catch a duplicate feature early; missing it costs a manual read, not the gate.

Either way, continue with manual exploration. Step 1 is done when you can state in one paragraph what the project is, what already exists near the idea, and which glossary terms apply — and you have named which existing features share the idea's surface and how the new idea differs (citing feature codes), or that none does.

## The ceremony tiers

The single most important output of the skill is the tier decision, spoken as "This is tier N because …". Deciding the tier *is* the design step for small work; naming it is not overhead, skipping it is.

If the work spans multiple independent subsystems, this is also where it is decomposed: name the sub-features, their relationships, and the build order. Each sub-feature then gets its own full spec cycle, and brainstorm continues with the first one only.

| Tier | When | What follows |
|---|---|---|
| **0** | typo-level, no behavior change | no spec — go straight to `tdd` |
| **1** | behavior change ≤ ~half a day | mini-spec: fix REQ + SHALL-CONTINUE-TO guard in the owning requirements.md |
| **2** | multi-task feature | full requirements → design → plan triad |

## Worked example

A user opens with "we should let people export their notes as PDF." Nothing is spec'd, so `brainstorm` fires and the hard gate is in force from the first word.

**Step 1.** Read `CONTEXT.md` and `docs/specs/INDEX.md` directly; dispatch a scan subagent that writes its digest to `.skills/pdf-export-scan.md` and reports the notes module already owns a Markdown export at `src/export/`. `INDEX.md` lists a feature owning that path, so grep `docs/specs/` for `export` and `pdf` and read its `requirements.md` header: `EXPORT-2`, owning `src/export/` with "PDF rendering" on its Out-of-Scope list.

State the one-paragraph context: "The project is a notes app; `EXPORT-2` already owns Markdown export and explicitly excludes PDF, so this idea is adjacent-but-new, and the glossary term *export* already applies."

**Step 2.** Interview through `grilling`, one question at a time, each with a recommendation: paginated or single-flow? Client-side or server render? What must keep working (the existing Markdown path)? The term "export" is already in the glossary; "render target" is fuzzy, so `domain-modeling` sharpens it and writes the settled term into `CONTEXT.md` inline, the moment it lands.

**Step 3.** "Can the browser print API produce acceptable page breaks?" is a fact, not a preference — so guessing is not allowed. Detour to `research`, come back with a cited note, and put the resulting decision to the user through `grilling` like any other.

**Step 4.** Present two genuinely different approaches: client-side `window.print()` to PDF versus a server-side headless renderer. Lead with the recommendation — the client path, no new infra — and YAGNI-prune a templating engine nobody asked for.

The user picks, possibly a hybrid.

**Step 5.** "This is tier 2 because it adds a multi-task user-facing feature with a new dependency." The tier is spoken, with its reason, before any exit is taken.

**Step 6.** Invoke `write-requirements` — the only permitted exit for tier ≥ 1. No code has been written, nothing has been scaffolded, and the whole shape of the feature now lives in an artifact that will outlast the chat.

## Why it is written the way it is

`brainstorm` is a **pressure-gate skill**: the failure it was written against is an agent that, handed a "simple" request, opens an editor and starts building before the problem is confirmed.

That failure class calls for a hard prohibition plus a rationalization table plus a red-flags list — the same shape as [`tdd`](tdd.md), because both fight an agent that knows the rule and breaks it under pressure. Each row of the rationalization table is a shortcut observed in practice and countered by name; "Too simple to need a design" is the headline trap because small requests are where the gate feels most like overhead and is most often skipped.

The tier decision is forced to be spoken out loud so it cannot be quietly skipped, and the two exits are named exhaustively so there is no third path into code. The output can be three sentences, but the process runs every time — that invariance is the whole point.

## See also

- [Ceremony tiers](../methodology/ceremony-tiers.md) — the 0/1/2 decision in full
- [`amend`](amend.md) — the sibling for changes to already-shipped features
- [`write-requirements`](write-requirements.md) — the tier ≥ 1 exit
