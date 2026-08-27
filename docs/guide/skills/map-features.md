# `map-features`

> Confirm-then-write catalog mapping — dispose OBS/OWNS gaps; optionally
> **export** / **materialize** when the repo opts into INDEX-only catalog sync.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | user-invoked only — `/map-features` |
| **Reads** | `docs/specs/` (flat or sharded), optional roadmap, `.skills/reverse-features/active/`, `docs/agents/project.md` Catalog sync |
| **Writes** | confirmed SSOT edits only; dispose never scaffolds a full triad; materialize may write **Draft** stubs under index-only |
| **Preflight** | Missing `docs/specs/INDEX.md` → stop; name `/configure-repo` |

Team catalog-sync how-to: [`catalog-sync.md`](catalog-sync.md).

## Modes

| Mode | When | Writes |
|---|---|---|
| `dispose` | always | OBS promote/absorb/dismiss, Recognized cards, Feature code / ROAD / OWNS Files proposals |
| `export` | `Catalog sync: index-only` | Refresh INDEX (± shard) cells from **local** triad |
| `materialize` | `Catalog sync: index-only` | Draft stub triad at INDEX Spec path (`templates/triad-stub/`) |

Opt in via `/configure-repo` Decision L → `docs/agents/project.md`:

```markdown
- **Catalog sync:** `index-only`
```

That also expects the gitignore snippet tracking INDEX (± `catalog/`) while
ignoring `docs/specs/*/` feature dirs. Do not `git add -f` those dirs.

## Dispose kinds (v1.1+)

| Kind | Confirm writes |
|---|---|
| Domain boundary | Sharded router + shard stub; flat = deferred |
| Recognized capability | Compact INDEX/shard card only (Spec may be `—`) |
| OBS disposition | promote / absorb / dismiss — promote also writes Recognized card |

See `skills/track/map-features/SKILL.md` and
`skills/execution/load-subgraph/references/catalog-query.md`.

## Team sync story (INDEX-only)

Full migration notes: [`catalog-sync.md`](catalog-sync.md).

1. Teammate A builds with local triad (gitignored) → `/map-features` **export**
   refreshes INDEX → commit/push INDEX only.
2. Teammate B pulls → `/map-features` **materialize** CODE → Draft stubs →
   `specify-behavior` as needed.
3. Reverse-track: `reconcile-features` (OBS) → `/map-features` **dispose**.
   Prefer promote rows that cite `OBS-…` provenance from the overlay.
