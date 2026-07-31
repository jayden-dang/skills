# `anchor-project`

> Above the per-feature workflow sits an optional layer: the product north star and the architecture invariants that keep independently-built features from drifting apart.

|  |  |
|---|---|
| **Bucket** | project |
| **Invocation** | `/anchor-project` (user-invoked; `disable-model-invocation: true`) |
| **Reads** | the templates; the existing layer docs (update/validate); the codebase (brownfield ratification) |
| **Writes** | `docs/product/vision.md`, `docs/architecture/INDEX.md` (+ per-domain files), `docs/product/guidelines.md` |
| **Calls** | [`probe-decisions`](probe-decisions.md), [`define-domain`](define-domain.md) (ADR gate), [`judge-invariants`](judge-invariants.md) (validate mode) |
| **Called by** | nobody — it is user-invoked. Offered by [`configure-repo`](configure-repo.md) (decision **I**) and [`bootstrap-repo`](bootstrap-repo.md) at init |

## When it fires

At the start of a **large or long-lived project**, before feature work, to establish the optional project-documentation layer — or later to update or validate it. Small repos do not need it: the feature workflow (`frame-change` → spec → `build-continuous`) runs fully without it, and nothing here is a gate.

## The three modes

- **create** — nothing exists yet. Brownfield check (if source already exists, the spine *ratifies* it rather than designing greenfield), then a [`probe-decisions`](probe-decisions.md) interview draws out the vision and the load-bearing invariants, then the three docs are written from templates.
- **update** — revise against a change signal. WHERE the change is a pivot that collides with shipped features or live invariants, stop and name [`/dispose-pivot`](dispose-pivot.md) first (disposition ledger); continue only after that ledger is confirmed. Hard-to-reverse decisions get an ADR via [`define-domain`](define-domain.md); a retired invariant is struck (strikethrough on the live `**ARCH-N**` line only — never in comments/templates), never renumbered.
- **validate** — walk each doc against its template, run [`judge-invariants`](judge-invariants.md) across the feature `design.md` files, and run the [`audit-trace`](audit-trace.md) invariant integrity check.

## The architecture spine

The spine is not a diagram doc — it is the small set of **invariants** that keep independently-built features consistent, each a greppable `**ARCH-N**` ID plus one imperative rule. A feature `design.md` cites the ones it relies on as `Respects: ARCH-N`, and [`audit-trace`](audit-trace.md) verifies those citations point at a live invariant.

## Optionality

The whole layer is optional. `configure-repo` gates it behind a default-**No** decision; feature skills consult it through no-op-if-absent hooks. A repo that opts into nothing behaves exactly as it did before this layer existed.

## See also

- [`judge-invariants`](judge-invariants.md) — the advisory conformance check `anchor-project` runs in validate mode
- [`audit-trace`](audit-trace.md) — the deterministic referential-integrity check for `Respects: ARCH-N` citations
- [`design-solution`](design-solution.md) — cites invariants as `Respects: ARCH-N`
- [`define-domain`](define-domain.md) — owns the ADR gate the update mode routes through
