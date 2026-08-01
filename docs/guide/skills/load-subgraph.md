# `load-subgraph`

> Ask-time derivation of a bounded feature subgraph (neighbors, ancestors, blast
> radius) from live specs — no generated graph file.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invoked |
| **Reads** | `docs/specs/**`, INDEX, optional roadmap/architecture |
| **Writes** | none (envelope in chat only) |
| **Called by** | `frame-change`, `inspect-change` |

See `skills/execution/load-subgraph/SKILL.md` and `references/passes.md`.
