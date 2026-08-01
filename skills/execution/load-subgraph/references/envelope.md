# Result envelope

Every load-subgraph result MUST include:

```text
advisory: true
owns_coverage: { with_owns: W, registered: R, ratio: W/R }
p0: { matched: M, returned: K, truncated: bool }
neighbors: [ { code, shared_paths: n, via: path|term|both } … ]  # when neighbors
# or nodes / ancestors / descendants / codes for other queries
notes: [ … non-fatal parse skips … ]
```

Always print OWNS coverage so a thin neighborhood is visible as thin.
Banner: advisory — not a hard gate; never fail frame-change or review solely on neighbors.

MUST NOT include DEPENDS_ON / depends_on edges.
