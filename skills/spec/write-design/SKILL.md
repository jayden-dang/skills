---
name: write-design
description: Use when requirements are approved and the technical design needs to be written — after write-requirements, before write-plan
---

Produce `docs/specs/<date>-<feature>/design.md`: HOW the approved requirements
get satisfied. Start from `templates/design.md`. The requirements file is your
input contract — read it fully first.

## Step 1: Context and decisions

Explain in 2–4 paragraphs what exists today and which constraint shapes the
approach. Record the decisions locked during discovery as a numbered list.
Any decision that is hard to reverse AND surprising without context AND a real
trade-off also gets an ADR (REQUIRED SUB-SKILL: `domain-modeling` owns the ADR
gate).
**Done when:** a newcomer could state why this approach over the obvious
alternative.

## Step 2: Architecture with Satisfies lines

One `###` section per component or area. Every section carries a
`Satisfies: CODE-N.M, CODE-N.M` line naming the requirement IDs it exists to
meet. A section with no Satisfies line is either infrastructure (say so) or
does not belong in this feature.

For the genuinely hard parts, design it twice: dispatch 2–3 parallel subagents
with divergent constraints (minimize the interface / maximize flexibility /
optimize the common caller), compare on interface depth and seam placement,
and commit to one with a stated reason. Be opinionated — the user wants a
strong recommendation, not a menu.

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

Present the FILE to the user, section by section for large designs, and STOP
for approval. On approval set `Status: Approved`.

## Exit

REQUIRED SUB-SKILL: use `write-plan`.
