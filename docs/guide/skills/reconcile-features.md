# `reconcile-features` (removed)

> Reverse-track is no longer a separate skill. It lives inside
> [`/map-features`](map-features.md) as **dispose step 0**.

|  |  |
|---|---|
| **Status** | deleted / folded |
| **Use instead** | [`map-features`](map-features.md) — dispose mode |
| **Runner path** | `skills/track/map-features/scripts/reconcile.py` |

Model-invoked callers (`frame-change`, `inspect-change`) **name** `/map-features`
when the reverse predicate holds or pending OBS need disposition. They must not
auto-invoke it, and they must not invent a `reconcile-features` skill call.

`inspect-change` may still run the reverse runner **read-only** for an advisory
envelope on the pinned range; dispose writes stay with `/map-features`.

See also: [`catalog-sync.md`](catalog-sync.md),
[`load-subgraph`](load-subgraph.md),
`skills/track/map-features/references/passes.md`.
