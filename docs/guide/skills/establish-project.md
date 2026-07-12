# `establish-project`

> Above the per-feature workflow sits an optional layer: the product north star and the architecture invariants that keep independently-built features from drifting apart.

|  |  |
|---|---|
| **Bucket** | project |
| **Invocation** | `/establish-project` (user-invoked; `disable-model-invocation: true`) |
| **Reads** | the templates; the existing layer docs (update/validate); the codebase (brownfield ratification) |
| **Writes** | `docs/product/vision.md`, `docs/architecture/INDEX.md` (+ per-domain files), `docs/product/guidelines.md` |
| **Calls** | [`grilling`](grilling.md), [`domain-modeling`](domain-modeling.md) (ADR gate), [`check-invariants`](check-invariants.md) (validate mode) |
| **Called by** | nobody — it is user-invoked. Offered by [`setup-repo`](setup-repo.md) (decision G) and [`scaffold-project`](scaffold-project.md) at init |

## When it fires

At the start of a **large or long-lived project**, before feature work, to establish the optional project-documentation layer — or later to update or validate it. Small repos do not need it: the feature workflow (`brainstorm` → spec → `execute-plan`) runs fully without it, and nothing here is a gate.

## The three modes

- **create** — nothing exists yet. Brownfield check (if source already exists, the spine *ratifies* it rather than designing greenfield), then a [`grilling`](grilling.md) interview draws out the vision and the load-bearing invariants, then the three docs are written from templates.
- **update** — revise against a change signal. Hard-to-reverse decisions get an ADR via [`domain-modeling`](domain-modeling.md); a retired invariant is struck (`~~**ARCH-3**~~`), never renumbered.
- **validate** — walk each doc against its template, run [`check-invariants`](check-invariants.md) across the feature `design.md` files, and run the [`trace`](trace.md) invariant integrity check.

## The architecture spine

The spine is not a diagram doc — it is the small set of **invariants** that keep independently-built features consistent, each a greppable `**ARCH-N**` ID plus one imperative rule. A feature `design.md` cites the ones it relies on as `Respects: ARCH-N`, and [`trace`](trace.md) verifies those citations point at a live invariant.

## Optionality

The whole layer is optional. `setup-repo` gates it behind a default-**No** decision; feature skills consult it through no-op-if-absent hooks. A repo that opts into nothing behaves exactly as it did before this layer existed.

## See also

- [`check-invariants`](check-invariants.md) — the advisory conformance check `establish-project` runs in validate mode
- [`trace`](trace.md) — the deterministic referential-integrity check for `Respects: ARCH-N` citations
- [`write-design`](write-design.md) — cites invariants as `Respects: ARCH-N`
- [`domain-modeling`](domain-modeling.md) — owns the ADR gate the update mode routes through
