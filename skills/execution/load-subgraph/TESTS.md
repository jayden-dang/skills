# `load-subgraph` — catalog query / Pass R modes (v1.1.0)

**Roster:** grok-4.6, grok-4.5 (shared with frame-change catalog RED).

## Edit — Pass R flat + sharded; snapshot ≠ chat dump

**Origin.** Query-first catalog slice. `frame-change` v1.1.0 RED showed agents
paste all 120 INDEX rows when told INDEX is small (`FULL_INDEX_IN_CONTEXT: yes`).
Pass R already read INDEX for the registry set; it lacked sharded mode and a
one-home context policy.

**Form:** `references/catalog-query.md` (modes, caps, recipe) + Pass R mode
detect; SKILL clarifies snapshot enumeration ≠ chat dump.

**Contract check:** flat bootstrap INDEX still parses; sharded router reads
listed `docs/specs/catalog/*.md` shards into `registered`; OBS cards are not
registry members.
