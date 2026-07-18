---
name: write-design
description: Use when approved requirements need their technical design — the design.md /
  architecture doc spelling out HOW the requirements get built. After
  write-requirements, before write-plan.
---

Produce `docs/specs/<YYYY-MM-DD>-<feature>/design.md`: HOW the approved requirements
get satisfied. Start from the skill set's `templates/design.md` — resolve
`templates/` as `${CLAUDE_PLUGIN_ROOT}/templates` when installed as a plugin,
otherwise `../../../templates` relative to this SKILL.md. Every heading in it is a
REQUIRED slot. The requirements file is your input contract — read it fully first.

Create a todo per step (1–4) before starting, and complete them in order — this skill owns its own list, distinct from `write-requirements`' upstream and `write-plan`'s downstream. Check each off only when its **Done when:** is met.

## Step 1: Context and decisions

Explain in 2–4 paragraphs what exists today and which constraint shapes the
approach. To learn "what exists today" without flooding this context, dispatch
a **scan subagent** to map the touched surface — the seams the design will name:
current signatures, data shapes, save/load paths — returning a digest file
(`.skills/<slug>-scan.md`), not raw source. Design against the digest; pull a
specific file into context only when a decision hinges on its exact contents.
(No subagents? Read the surface directly, but only the parts a decision needs.)
Record the decisions locked during discovery as a numbered list.
Any decision that is hard to reverse AND surprising without context AND a real
trade-off also gets an ADR (REQUIRED SUB-SKILL: `domain-modeling` owns the ADR
gate).

When a `docs/architecture/` spine exists, its `**ARCH-N**` invariants are inputs to
this design: read them and note which ones this feature relies on (you will cite them
in Step 2). If a design decision must *contradict* an invariant, that is an
ADR-or-supersede event — record the ADR, or supersede the invariant by strikethrough
in the spine — never a silent violation. No spine? Skip this; the layer is optional.
**Done when:** a newcomer could state why this approach over the obvious
alternative.

## Step 2: Architecture with Satisfies lines

One `###` section per component or area. Every section carries a
`Satisfies: CODE-N.M, CODE-N.M` line naming the requirement IDs it exists to
meet. A section with no Satisfies line is either infrastructure (say so) or
does not belong in this feature. When the design relies on an architecture
invariant (Step 1), the section also carries a `Respects: ARCH-N` line — the
`trace` check verifies that citation points at a live invariant.
Every section also carries a `Reuse: <rung> — <concrete target>` line beside its `Satisfies:`
line, naming the highest ladder rung that held and the concrete existing artifact it builds on
(e.g. `Reuse: existing — extends src/util/dates:parseISO (rung 2)`, `Reuse: dependency — zod
(rung 5)`), or `Reuse: none — new code (rung 7)` carrying a one-line reason no lower rung held.
Adopting a brand-new third-party dependency — one the project does not already use — is the
**user's decision, not yours to make silently**. When the ladder lands on a library the project
hasn't adopted, stop and put it to the user as an explicit choice: *"I want to add `<library>`
to handle `<problem>`"* — in plain language, say what the library is, why it fits this problem
better than hand-rolling it, and what it costs (a new dependency to maintain, its footprint and
supply-chain surface). Ground that pitch in current facts, not memory: look up the library's
latest stable version and present API through the **Context7 MCP** (or `research`, which uses
it) before you name it — a pitch built on a training-cutoff recollection can cite a version,
package name, or API that no longer exists. Wait for their agreement before writing it into the
design as the chosen approach; if they decline, fall back down the ladder — an already-installed
dependency, or the minimum new code that works. An *already-installed* dependency (rung 5) needs no such ask —
reuse it freely. The `Reuse:` line itself stays advisory; it is the new-dependency *adoption*
that is the user's call.

For the genuinely hard parts, design it twice: dispatch 2–3 parallel subagents
with divergent constraints (minimize the interface / maximize flexibility /
optimize the common caller), compare on interface depth and seam placement,
and commit to one with a stated reason. Be opinionated — the user wants a
strong recommendation, not a menu. "Genuinely hard" means the interface itself
is in question — a new persistence boundary, a concurrency model, a plugin
seam. A part with one obvious shape does not qualify: adding a field to an
existing store, wiring a new route through an established pattern, or a plain
CRUD form is a single-design job, and spawning three subagents to converge on
the same answer is wasted motion.

Before committing to build any component, climb the **reuse ladder** and stop at the highest
rung that holds — the cheapest thing that already works beats new code:

1. **Does it need to exist at all?** No requirement forces it → cut it (YAGNI).
2. **Already in this codebase?** A helper, util, type, or pattern the Step-1 scan found →
   reuse or extend it; re-implementing what is a few files over is the most common slop.
3. **Standard library or language builtin does it?** Use it.
4. **A platform / framework / runtime feature covers it?** Prefer it over hand-rolled code.
5. **An already-installed dependency solves it?** Use it — never add a new dependency for what
   a few lines do.
6. **Can it be one line?** One line.
7. **Only then** — the minimum new code that works.

The ladder is a reflex, not a research project: it climbs the Step-1 scan digest ("what
exists today") and runs only *after* you understand the problem — trace the real flow the
change touches first, then climb. It never licenses cutting a corner that matters: do not
prune away input validation at trust boundaries, error handling that prevents data loss,
security, accessibility, or anything the requirements explicitly asked for.

The three levers chain, each with a distinct job: the **scan** (Step 1) gathers what exists;
the **ladder** decides *whether* to build; the **deletion test** (below) refines *how deep*
to build — and applies only to a rung-7 new component.

Design for depth: for a rung-7 new component, a module's interface should be much simpler
than what it hides. Apply the deletion test — if this module vanished, how much would
callers need to know to rebuild it? If the answer is "everything it did", the
interface is shallow; redesign it.
**Done when:** every architecture section has a Satisfies line.

## Step 3: Agree the seams for testing

Fill the "Seams for testing" table: the public boundaries tests will be
written at, which requirement IDs each seam covers, and the test kind
(unit/integration/e2e). Prefer existing seams; the ideal number of NEW seams
is zero or one. The `tdd` skill refuses to write tests at seams not agreed
here — this table is the contract.
**Done when:** every requirement ID maps to at least one seam row.

## Step 4: Coverage self-check, then the approval gate

Walk requirements.md top to bottom: every ID appears in exactly one Satisfies
line (or is listed as deliberately unmapped, with a reason). Then scan for
placeholders and internal contradictions (a name used two ways, a data flow
that skips a component).

- **Reuse coverage:** every architecture section carries a `Reuse:` line, and every rung-7 or
  new-dependency line carries its one-line justification.

**Independent design review — dispatch, don't self-review.** Fresh context has
no stake in your framing (the bias that reinterprets a stale requirement rather
than catching it). Dispatch a review subagent with this design, requirements.md,
and the repo; have it verify every code-facing claim — each named seam,
signature, and data path exists as described, and each `Satisfies:` mapping is
achievable at that seam — grepping/reading real files, citing `file:line`,
defaulting to flag. Findings go to `.skills/<slug>-design-review.md`; you fix them
without loading the code here. (No subagents? Do this pass yourself in a fresh
read of the code.)

**Upstream sync-back — do not skip.** Designing routinely surfaces a fact that
contradicts an *approved* requirement: a premise that turned out false, a
mechanism the requirement named wrong, a constraint that does not hold (e.g. the
requirement says the stored body is ProseMirror-JSON but you discover it is
Markdown). When that happens you MUST correct the requirement's own text and
re-surface it for approval — never satisfy a requirement by quietly
reinterpreting words you now know are false. A `Satisfies:` line pointing at a
requirement whose wording is wrong makes the trace spine cite a lie, and the
error survives all the way to code. The same holds for an ADR you are writing
that contradicts an existing one: supersede it explicitly by number. If you
changed any requirement, say exactly which and why when you present for approval.

Present the FILE to the user, section by section for large designs, and STOP
for approval. On approval set `Status: Approved`.

## Exit

REQUIRED SUB-SKILL: use `write-plan`.
