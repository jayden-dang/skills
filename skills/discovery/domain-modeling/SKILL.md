---
name: domain-modeling
description: Use when a domain term needs defining, a glossary term is being used
  inconsistently or fuzzily, or a hard-to-reverse architectural decision worth
  an ADR is being made — maintains the project glossary (CONTEXT.md) and
  architecture decision records (docs/adr). Also runs as a side-effect
  sub-skill when an interview or design skill calls for glossary and ADR
  upkeep.
---

# Domain Modeling

Actively build and sharpen the project's glossary while designing. Merely *reading* `CONTEXT.md` for vocabulary is a habit any skill has; this skill is for *changing* the model — challenging terms, probing edges, and writing settlements down the moment they happen.

## During the conversation

**Challenge terms against the glossary.** When the user's usage conflicts with `CONTEXT.md`, call it out on the spot: "Your glossary defines *cancellation* as voiding the whole order, but you seem to mean removing one line item — which is it?"

**Sharpen fuzzy language.** When a term is vague or overloaded, propose a precise canonical one: "You keep saying *account* — is that the Customer or the User? They differ here."

**Stress-test with edge-case scenarios.** When relationships between concepts come up, invent concrete scenarios that press on the boundaries: "A Member leaves mid-billing-cycle with an unpaid Invoice — what happens to their Workspace?" Force the boundary to be stated, not implied.

**Cross-reference the code.** When the user asserts how something works, check whether the code agrees. Surface contradictions explicitly: "The glossary (and you) say partial refunds exist, but the code only refunds full payments — which is right?" Never let the glossary and the code silently disagree.

## Updating CONTEXT.md

Update `CONTEXT.md` **inline, the instant a term is settled** — never batch glossary edits for later; batched terms get forgotten. If no `CONTEXT.md` exists yet, create it lazily when the first term settles (seed from this repo's `templates/CONTEXT.md`).

`CONTEXT.md` is a **glossary only**. No implementation details, no decisions, no spec fragments, no scratch notes — those belong in specs and ADRs. Term format:

```md
**Workspace**:
The top-level container a team collaborates in; owns all Notes and Folders.
_Avoid_: project, space, tenant
```

Be opinionated: one canonical term, competitors banished to the `_Avoid_` list. Definitions stay to one to three tight lines — what the thing *is*, not how it's built. Only project-specific concepts belong; general programming vocabulary does not.

## ADRs — sparingly, through the three-part gate

Offer an ADR only when **all three** hold:

1. **Hard to reverse** — changing course later carries real cost.
2. **Surprising without context** — a future reader would ask "why on earth this way?"
3. **A real trade-off** — genuine alternatives existed and one was chosen for specific reasons.

Any one missing → no ADR. Format: `docs/adr/NNNN-slug.md` (create the directory lazily), numbered sequentially — scan for the highest existing number and add one. Body is a short title plus **1–3 sentences**: context, decision, why. That's the whole document; recording *that* and *why* is the value, not filling sections.

If a new decision contradicts an existing ADR, flag the conflict to the user and resolve it explicitly (supersede the old ADR by number). Never silently override a recorded decision.
