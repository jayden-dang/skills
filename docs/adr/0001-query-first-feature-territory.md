# ADR 0001 — Query-first feature territory with a derived graph

- **Status:** Accepted (2026-08-26)
- **Decision makers:** maintainer (`jayden-dang/skills`)
- **Research:** `.skills/research/2026-08-26-reverse-feature-spec-tracking.md`

## Context

Brownfield and team repos need reverse tracking when contributors do not use
this skill set and may not know Feature CODEs. Specs may be shared (`klynt`) or
local/gitignored (`mailgate`). Consuming-repo CI/hooks are out of scope
(zero-footprint). Forward tracking from Feature ID already works; the gap is
code/history → impacted feature or observed capability candidate.

## Decision

1. **Canonical authority** is a query-first capability catalog (`docs/specs/INDEX.md`
   as router, optional domain shards, compact feature cards). Immutable Feature
   CODEs live only there after human disposition.
2. **Observations** stay local under `.skills/reverse-features/` (active cards +
   evidence + tombstones). They are not CODEs and never auto-Approve SHALLs.
3. **Reconciler** ships in the skill pack as model-invoked `reconcile-features`
   (recipe `rfeat-1.0`): rename-aware git inventory → classify → advisory
   envelope → index then advance checkpoint. No Graphify in v1.
4. **Feature graph**, if present later, is derived, disposable, and loses to the
   catalog on conflict. Graphify may become an optional evidence adapter only
   after native extractors prove precision — not a dependency.

## Consequences

- Drift is detected when a spec-aware session next reads the checkout — not at
  external merge time.
- `frame-change` and `inspect-change` REQUIRED SUB-SKILL `reconcile-features`
  (predicate / step 1b).
- Agent context selection follows
  `skills/execution/load-subgraph/references/catalog-query.md` (flat + optional
  sharded; `DOMAINS_MAX` / `DIRECT_CARDS_MAX` / `NEIGHBOR_CARDS_MAX`). Pass R may
  still enumerate the registry on disk; chat must not dump it.
- Brownfield bootstrap proposes OBS / Recognized cards; full triads stay
  spec-on-change after human confirm.
