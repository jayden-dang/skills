# `frame-change`

> The front door of the idea-to-ship chain. A raw idea becomes an agreed shape through dialogue, and no code is written until the ceremony tier has been said out loud.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | `CONTEXT.md` (glossary vocabulary), catalog query over `docs/specs/INDEX.md` (selected cards — not a full-table dump), `docs/agents/project.md`; code, docs, and recent commits near the idea via a scan subagent digest at `.skills/<CODE>/scan.md` |
| **Writes** | notes, the glossary (`CONTEXT.md`), ADRs, and — via sub-skills — research notes and explicitly-marked throwaway run-spikes; nothing else |
| **Calls** | [`load-subgraph`](load-subgraph.md); [`clarify-decisions`](clarify-decisions.md), [`define-domain`](define-domain.md), [`research`](research.md), [`run-spike`](run-spike.md), [`specify-behavior`](specify-behavior.md) (tier ≥ 1), [`test-first`](test-first.md) (tier 0) |
| **Called by** | the user (entry point of the chain); [`amend-feature`](amend-feature.md) when a change turns out to be genuinely new scope |

## When it fires

At the very start of the idea-to-ship chain — the user wants to add, build, or change a feature, behavior, or component, or to start a whole new project, and no requirements, design, or code exist yet. It triggers on openers like "let's add…", "can we build…", "I'm thinking about…", and "we should support…" before implementation has begun.

`frame-change` is for shaping something *new* — nothing spec'd yet.

A small in-scope change to an **already-shipped, spec'd** feature is [`amend-feature`](amend-feature.md) instead: it reads the existing spec and routes the change to the light lane, escalating back here only when the change is genuinely new scope. If you were handed such a change, hand it to `amend-feature`. The two skills share a shape — both end on a spoken tier decision — but they start from opposite places: `frame-change` from a blank page, `amend-feature` from a spec that already exists.

## The hard gate

The skill opens with a prohibition that holds for **every** request, no matter how simple it looks:

> Write NO code, scaffold NOTHING, and invoke NO implementation skill until the checklist has run and the ceremony tier has been stated out loud.

The only artifacts the skill may touch are notes, the glossary, ADRs, and — through its sub-skills — research notes and explicitly-marked throwaway run-spikes.

The gate has exactly two exits, and they are named exhaustively so there is no third path into code. For tier 0 the only permitted exit is [`test-first`](test-first.md), and only after the tier is spoken. For tier ≥ 1, requirements are written and approved first through [`specify-behavior`](specify-behavior.md), which carries its own approval gate. Scaffolding a repo skeleton counts as implementation — it enacts a stack decision without approval — so it too waits behind the gate.

## "Too simple to need a design" is the trap

Small requests are exactly where unexamined assumptions burn the most work, because nobody bothers to check them.

The output can be tiny — a tier decision and three sentences — but the process runs every time.

The skill carries a six-row rationalization table, each row a shortcut it exists to block. Read down the right column: every "Reality" is the thing the corresponding shortcut skips over.

| Thought | Reality |
|---|---|
| "This is a one-liner, designing it is overhead" | Deciding it is tier 0 IS the design step — say so explicitly and move on. Skipping the decision is the overhead. |
| "The user already told me exactly what to build" | They told you a solution. You haven't confirmed the problem, the constraints, or what must keep working. |
| "I'll sketch a little code to clarify my thinking" | That's a run-spike. Run the `run-spike` sub-skill so it's throwaway by contract, not accidental production code. |
| "I'll write requirements after I confirm the approach compiles" | Code-first inverts the gate. Evidence questions get a research/run-spike detour; requirements still come first. |
| "Scaffolding isn't really implementation" | A repo skeleton is a stack decision enacted without approval. It's implementation. |
| "We talked enough, I basically know the answer" | If it isn't in an approved requirements.md, it lives only in this chat and dies with it. |

**Red flags — stop and return to the checklist** if you notice yourself: opening an editor to "just try something"; running a generator or scaffolder; answering your own open question instead of asking; presenting one approach as the only option; drifting from interviewing into implementing.

## The checklist

Each item is a todo, completed in order. The order matters: context before questions, questions before evidence, evidence before approaches, approaches before the tier. Skipping ahead is how unexamined assumptions survive to the spec.

1. **Explore project context.** Read `CONTEXT.md` (adopt its vocabulary from here on). Query the capability catalog per [`catalog-query.md`](../../../skills/execution/load-subgraph/references/catalog-query.md) — selected domain/feature/OBS cards only; never paste the full INDEX. Read the **Project posture** in `docs/agents/project.md` when present and let it right-size the interview. Delivery intent sets the quality bar the approaches must meet, never a release state; **compat obligation** decides the migration lens — on None, approaches change shapes in place and spend no scope on backward compatibility, versioned names, or deprecation cost; on Internal / External, weigh exactly those. For anything heavier, dispatch a scan subagent that writes a findings digest to `.skills/<CODE>/scan.md` and returns only that path; work from the digest, not raw files. Then run the overlap check (below). If `docs/agents/project.md` or these files are missing, say so, suggest [`configure-repo`](configure-repo.md), and continue with what you have.
2. **Interview.** REQUIRED SUB-SKILL [`clarify-decisions`](clarify-decisions.md) — inline question cards (full context, never truncated pickers), blast-radius first, every branch walked, then a decisions table + constraints confirmed. Keep [`define-domain`](define-domain.md) active as a side effect throughout: challenge terms against the glossary, sharpen fuzzy language, and update `CONTEXT.md` the moment a term settles. If the request spans multiple independent subsystems, stop refining and decompose first (step 5).
3. **Detour when a question needs evidence, not opinion.** When the honest answer is "we'd have to check": facts about external systems, APIs, libraries, or standards go to [`research`](research.md) (primary sources, cited note); "does this model or flow actually feel right?" goes to [`run-spike`](run-spike.md) (a runnable throwaway answer). Return with the evidence and put the decision back to the user.
4. **Propose approaches.** Present 2–3 genuinely different approaches with trade-offs, lead with your recommendation and why, YAGNI-prune every option. The user picks.
5. **Decide the ceremony tier — out loud.** State the tier and why (table below). If the work spans multiple independent subsystems, decompose here: name the sub-features, their relationships, and build order; each gets its own full spec cycle and frame-change continues with the first only.
6. **Terminal state.** Tier ≥ 1: invoke `specify-behavior` — the ONLY exit; do not write code, scaffold, or invoke any implementation or design skill directly, because requirements come first and carry their own approval gate. Tier 0: hand off to `test-first` directly and say so.

## The overlap check

Step 1 runs **no catalog-staleness check**: it does not read `.skills/reverse-features/state.json`, does not compare `last_reconciled_sha` against `HEAD`, and does not name [`/map-features`](map-features.md). Keeping the catalog current is the user's call, made by running `/map-features` when they want it — see [Catalog currency](#catalog-currency) below. Run **`load-subgraph`** (REQUIRED SUB-SKILL) with the idea's **key terms** and the scan's **candidate paths**. The shared catalog is the registry (Domain router INDEX + `docs/specs/catalog/*.md`); derivation uses live `**Files:**` (OWNS) and term match (P0), returns ranked neighbors plus **OWNS coverage**. Present each neighbor as a short summary card (owned paths + Out-of-Scope), not the full spec.

The check is advisory, never a gate:

- **No `INDEX.md`** — say so once, name [`configure-repo`](configure-repo.md), at most once per session.
- **No `docs/specs/`** — note nothing to check against and continue.
- **Thin OWNS coverage** — report the ratio; thin is not an error.

Step 1 is done when you can state in one paragraph what the project is, what already exists near the idea, and which glossary terms apply — and you have named which existing features share the idea's surface (citing codes) or that none does, with OWNS coverage stated.

## Catalog currency

`frame-change` does **not** check whether the capability catalog is up to date. It reads the
catalog as it finds it and runs `load-subgraph` against that.

This is deliberate. The check it used to run compared `.skills/reverse-features/state.json`'s
`last_reconciled_sha` against `HEAD`, and after any merge or PR those differ — so on a repo
with normal git activity the predicate held on essentially every invocation, and every
`frame-change` spent a paragraph naming `/map-features`. Measured over eight recorded runs it
fired 8/8, including on a checkout with no git repo at all, where it produced only an
"explicit not-applicable" caveat.

**The trade-off, stated plainly.** With no staleness check, `frame-change`'s overlap finding
is only as current as the catalog. If features have landed that were never indexed, step 1
can report "no overlap" when an un-indexed neighbor exists. The judgment is that a warning
which fires every single time carries no information — an always-on signal is not a signal —
and that catalog currency is better handled deliberately.

**So: run [`/map-features`](map-features.md) yourself** when you have pulled work you did not
write, after a batch of merges, or whenever the catalog feels behind. It is a user-invoked
skill (`disable-model-invocation: true`) and always was — this change removes the automatic
nagging, not the capability.

## The ceremony tiers

The single most important output of the skill is the tier decision, spoken as "This is tier N because …". Deciding the tier *is* the design step for small work; naming it is not overhead, skipping it is.

If the work spans multiple independent subsystems, this is also where it is decomposed: name the sub-features, their relationships, and the build order. Each sub-feature then gets its own full spec cycle, and frame-change continues with the first one only.

| Tier | When | What follows |
|---|---|---|
| **0** | typo-level, no behavior change | no spec — go straight to `test-first` |
| **1** | behavior change ≤ ~half a day | mini-spec: fix REQ + SHALL-CONTINUE-TO guard in the owning requirements.md |
| **2** | multi-task feature | full requirements → design → plan triad |

## Worked example

A user opens with "we should let people export their notes as PDF." Nothing is spec'd, so `frame-change` fires and the hard gate is in force from the first word.

**Step 1.** Read `CONTEXT.md`; query the catalog for export/pdf-adjacent cards (not the whole INDEX); dispatch a scan subagent that writes its digest to `.skills/pdf-export-scan.md` and reports the notes module already owns a Markdown export at `src/export/`. Run `load-subgraph` with terms `export`/`pdf` and path `src/export/`; the envelope surfaces neighbor `EXPORT-2` with "PDF rendering" on its Out-of-Scope list and non-empty OWNS coverage.

State the one-paragraph context: "The project is a notes app; `EXPORT-2` already owns Markdown export and explicitly excludes PDF, so this idea is adjacent-but-new, and the glossary term *export* already applies."

**Step 2.** Interview through `clarify-decisions` question cards (radius, why it matters, options with consequences, recommendation): paginated or single-flow? Client-side or server render? What must keep working (the existing Markdown path)? The term "export" is already in the glossary; "render target" is fuzzy, so `define-domain` sharpens it and writes the settled term into `CONTEXT.md` inline, the moment it lands. Branches close with a decisions table the user confirms.

**Step 3.** "Can the browser print API produce acceptable page breaks?" is a fact, not a preference — so guessing is not allowed. Detour to `research`, come back with a cited note, and put the resulting decision to the user through `clarify-decisions` like any other.

**Step 4.** Present two genuinely different approaches: client-side `window.print()` to PDF versus a server-side headless renderer. Lead with the recommendation — the client path, no new infra — and YAGNI-prune a templating engine nobody asked for.

The user picks, possibly a hybrid.

**Step 5.** "This is tier 2 because it adds a multi-task user-facing feature with a new dependency." The tier is spoken, with its reason, before any exit is taken.

**Step 6.** Invoke `specify-behavior` — the only permitted exit for tier ≥ 1. No code has been written, nothing has been scaffolded, and the whole shape of the feature now lives in an artifact that will outlast the chat.

## Why it is written the way it is

`frame-change` is a **pressure-gate skill**: the failure it was written against is an agent that, handed a "simple" request, opens an editor and starts building before the problem is confirmed.

That failure class calls for a hard prohibition plus a rationalization table plus a red-flags list — the same shape as [`test-first`](test-first.md), because both fight an agent that knows the rule and breaks it under pressure. Each row of the rationalization table is a shortcut observed in practice and countered by name; "Too simple to need a design" is the headline trap because small requests are where the gate feels most like overhead and is most often skipped.

The tier decision is forced to be spoken out loud so it cannot be quietly skipped, and the two exits are named exhaustively so there is no third path into code. The output can be three sentences, but the process runs every time — that invariance is the whole point.

## See also

- [Ceremony tiers](../methodology/ceremony-tiers.md) — the 0/1/2 decision in full
- [`amend-feature`](amend-feature.md) — the sibling for changes to already-shipped features
- [`specify-behavior`](specify-behavior.md) — the tier ≥ 1 exit
