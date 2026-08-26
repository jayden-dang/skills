# `map-features`

> Brownfield backfill for Feature code lines, ROAD bindings, OWNS gaps,
> DEPENDS_ON *candidates*, domain boundaries, Recognized catalog cards, and OBS
> dispositions — propose, confirm, additive SSOT only.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | user-invoked only — `/map-features` |
| **Reads** | `docs/specs/` (flat or sharded), optional roadmap, `.skills/reverse-features/active/` |
| **Writes** | confirmed SSOT edits only; catalog cards / INDEX rows / Files lines / OBS tombstones; never a graph projection; never a full triad |

## New kinds (v1.1.0)

| Kind | Confirm writes |
|---|---|
| Domain boundary | Sharded router + shard stub; flat = deferred |
| Recognized capability | Compact INDEX/shard card only (Spec may be `—`) |
| OBS disposition | promote / absorb / dismiss — promote also writes Recognized card |

See `skills/track/map-features/SKILL.md` and
`skills/execution/load-subgraph/references/catalog-query.md`.
