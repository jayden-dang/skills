# `domain-modeling`

> Build and sharpen the project's shared vocabulary while designing — settling terms into the glossary the instant they land, and recording only the rare decisions that earn an ADR.

|  |  |
|---|---|
| **Bucket** | discovery |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | `CONTEXT.md` (the glossary), the code (to check it agrees with the glossary), `docs/adr/` (existing ADRs and their numbers) |
| **Writes** | `CONTEXT.md` (glossary terms, inline); `docs/adr/NNNN-slug.md` (sparingly, through the three-part gate) |
| **Calls** | — |
| **Called by** | [`brainstorm`](brainstorm.md) and other interview/design skills, as a side-effect sub-skill kept active during the conversation; [`prototype`](prototype.md) (for its ADR gate) |

## When it fires

When a domain term needs defining, when a glossary term is being used inconsistently or fuzzily, or when a hard-to-reverse architectural decision worth an ADR is being made.

It also runs as a **side-effect sub-skill**: an interview or design skill keeps it active so the glossary and ADRs stay current as the conversation moves. Merely *reading* `CONTEXT.md` for vocabulary is a habit any skill has — this skill is for *changing* the model, challenging terms, probing edges, and writing settlements down the moment they happen.

## During the conversation

The skill works the live conversation on four fronts:

- **Challenge terms against the glossary.** When the user's usage conflicts with `CONTEXT.md`, call it out on the spot: "Your glossary defines *cancellation* as voiding the whole order, but you seem to mean removing one line item — which is it?"
- **Sharpen fuzzy language.** When a term is vague or overloaded, propose a precise canonical one: "You keep saying *account* — is that the Customer or the User? They differ here."
- **Stress-test with edge-case scenarios.** When relationships between concepts come up, invent concrete scenarios that press the boundaries: "A Member leaves mid-billing-cycle with an unpaid Invoice — what happens to their Workspace?" Force the boundary to be stated, not implied.
- **Cross-reference the code.** When the user asserts how something works, check whether the code agrees and surface contradictions explicitly. Never let the glossary and the code silently disagree.

## Updating CONTEXT.md

`CONTEXT.md` is updated **inline, the instant a term is settled** — never batched for later, because batched terms get forgotten. The edit happens in the same turn the term lands, not at the end of the interview.

If no `CONTEXT.md` exists yet, it is created lazily when the first term settles, seeded from this repo's `templates/CONTEXT.md`.

`CONTEXT.md` is a **glossary only**: no implementation details, no decisions, no spec fragments, no scratch notes — those belong in specs and ADRs. The moment those leak in, the glossary stops being a place people trust to look up a word.

The term format is opinionated — one canonical term, competitors banished to an `_Avoid_:` list:

```md
**Workspace**:
The top-level container a team collaborates in; owns all Notes and Folders.
_Avoid_: project, space, tenant
```

Definitions stay to one to three tight lines — what the thing *is*, not how it is built. Only project-specific concepts belong; general programming vocabulary does not, because a glossary of things everyone already knows is one nobody reads.

## ADRs — sparingly, through the three-part gate

An ADR is offered only when **all three** hold:

1. **Hard to reverse** — changing course later carries real cost.
2. **Surprising without context** — a future reader would ask "why on earth this way?"
3. **A real trade-off** — genuine alternatives existed and one was chosen for specific reasons.

Any one missing means no ADR — a reversible choice, an obvious one, or a decision with no real alternative all fail the gate and belong in a commit message instead.

The format is `docs/adr/NNNN-slug.md` (directory created lazily), numbered sequentially by scanning for the highest existing number and adding one. The body is a short title plus **1–3 sentences** — context, decision, why. That is the whole document; recording *that* and *why* is the value, not filling sections.

If a new decision contradicts an existing ADR, the conflict is flagged to the user and resolved explicitly by **superseding the old ADR by number**. A recorded decision is never silently overridden.

## Worked example

**A glossary term settling.** Mid-interview the user keeps saying "the space" for both the shared team area and a single document's canvas. `domain-modeling` challenges it: "Two different things are both *space* here — the team container and the drawing surface. Can we call the container a Workspace and the surface a Canvas?" The user agrees, and `CONTEXT.md` is edited *right then*:

```md
**Workspace**:
The top-level container a team collaborates in; owns all Notes and Folders.
_Avoid_: space, project, tenant
```

**An ADR that passes the gate.** The team decides to store all timestamps as UTC and convert only at the display edge. Hard to reverse (every stored row and query assumes it), surprising without context (a reader sees no local times anywhere and wonders why), and a real trade-off (local-time storage was on the table and rejected for cross-timezone reporting). All three hold, so `docs/adr/0007-utc-everywhere.md` is written:

> **UTC everywhere, convert at the edge.** All persisted timestamps are UTC; conversion to local time happens only in the presentation layer. Chosen over per-row timezone storage because reporting spans timezones and mixed storage made aggregate queries error-prone.

**An ADR that fails the gate.** "We'll use the project's existing logger instead of adding a new one." It is a real choice, but reversing it is cheap, no future reader is surprised, and there was no meaningful trade-off — one leg missing is enough. **No ADR.** It lives in the commit message, not `docs/adr/`.

## Why it is written the way it is

Two decay patterns shape the skill.

The first is the **glossary that drifts** — terms defined once, then used loosely until the document is fiction. The inline-the-instant-it-settles rule fights the batching that loses terms, and the glossary-only scope keeps `CONTEXT.md` a tight, trusted reference instead of a junk drawer of half-decisions and spec fragments. The opinionated `_Avoid_:` list does the rest: it does not just define the winner, it names the losing synonyms so they stop leaking back into the conversation.

The second is **ADR inflation** — every decision written up until the folder is noise and the genuinely important calls are buried. The three-part gate is deliberately strict so an ADR stays a signal that *this one is hard to reverse and non-obvious*. The 1–3 sentence body keeps writing one cheap enough that the gate, not effort, is what limits them — and superseding by number, rather than editing in place, keeps the trail of *why we changed our minds* intact.

## See also

- [`brainstorm`](brainstorm.md) — keeps this skill active through its interview
- [`grilling`](grilling.md) — the interview it runs alongside, sharpening terms as decisions surface
- [Artifacts](../concepts/artifacts.md) — where `CONTEXT.md` and ADRs sit among the durable records
- [Gates](../concepts/gates.md) — where the three-part ADR gate sits among the set's other gates
- [Requirement IDs](../concepts/requirement-ids.md) — the vocabulary the glossary feeds into specs
