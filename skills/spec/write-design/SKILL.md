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

Design for depth: a module's interface should be much simpler than what it
hides. Apply the deletion test — if this module vanished, how much would
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
