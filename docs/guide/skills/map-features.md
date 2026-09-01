# `map-features`

> Confirm-then-write ops for the **shared** capability catalog — Domain router
> on `docs/specs/INDEX.md` plus feature cards in `docs/specs/catalog/*.md`.
> Reverse-track (ex-`reconcile-features`) is **dispose step 0**, not a separate
> skill.

|  |  |
|---|---|
| **Bucket** | track |
| **Invocation** | user-invoked only — `/map-features` |
| **Reads** | Domain router INDEX + `docs/specs/catalog/*.md`, optional roadmap, `.skills/reverse-features/`, `docs/agents/project.md` Catalog sync |
| **Writes** | confirmed SSOT edits only; dispose never scaffolds a full triad; materialize may write **Draft** stubs under index-only |
| **Preflight** | Missing INDEX → stop; name `/configure-repo`. Flat `| Code | … |` table on INDEX → propose **Domain boundary** migrate (not a valid live registry) |

Team catalog-sync how-to: [`catalog-sync.md`](catalog-sync.md).  
Former `reconcile-features` page: [`reconcile-features.md`](reconcile-features.md) (redirect).

## Shared catalog only

| File | Role |
|---|---|
| `docs/specs/INDEX.md` | **Domain router** — `\| Domain \| Scope \| Surface roots \| Feature catalog \|` |
| `docs/specs/catalog/<domain>.md` | Feature cards for that domain |

Register new CODEs in the owning **shard**, not on the router. A flat feature
table on INDEX is invalid for query — empty registry until migrated.

## Modes

| Mode | When | Writes |
|---|---|---|
| `dispose` (default) | always | step 0 reverse envelope/OBS; then promote/absorb/dismiss, Recognized shard cards, Feature code / ROAD / OWNS / Domain-boundary proposals |
| `export` | `Catalog sync: index-only` | Refresh shard (or router) cells from **local** triad |
| `materialize` | `Catalog sync: index-only` | Draft stub triad at Spec path (`templates/triad-stub/`) |

Opt in via `/configure-repo` Decision L → `docs/agents/project.md`:

```markdown
- **Catalog sync:** `index-only`
```

That also expects the gitignore snippet tracking INDEX (± `catalog/`) while
ignoring `docs/specs/*/` feature dirs. Do not `git add -f` those dirs.

## Dispose

### 0. Reverse (always first)

Mechanical reverse track before the gap scan. Prefer:

```bash
python3 skills/track/map-features/scripts/reconcile.py \
  --repo <root> --base <sha> --head <sha> --mode <mode>
```

Add `--write-overlay` when `.skills/` is writable and gitignored. Modes:
`changes-since-checkpoint` | `full` | `brownfield-bootstrap` — see
`skills/track/map-features/references/passes.md`. Prints one
`references/envelope.md` envelope (advisory). Indexes OBS under
`.skills/reverse-features/` or stays stateless. Does **not** mint Feature CODEs
or write INDEX — overlay + envelope only.

### 1–3. Scan → propose → confirm-write

| Kind | On confirm |
|---|---|
| Domain boundary | Shared router + shard stub(s); migrate flat INDEX rows into `catalog/<domain>.md` |
| Missing Feature code | `Feature code:` line in requirements |
| Empty ROAD bind | Shard Roadmap cell → live `ROAD-N` only (never mint) |
| OWNS gap | `tasks.md` Files Create/Modify/Test line |
| DEPENDS_ON candidate | Reuse prose only — never a load-subgraph edge |
| Recognized capability | Compact catalog card in a **shard** (Spec may be `—`); **no triad** |
| OBS disposition | promote / absorb / dismiss + tombstone; promote writes Recognized shard card |

Prefer promoting OBS that cite `observation_id` / surface roots over free-floating
Recognized rows. Batch confirm is allowed (`Confirm P01-P06; decline P07-P15` or
`Confirm batch Core`); promote/absorb still need an explicit CODE token.

See `skills/track/map-features/SKILL.md` and
`skills/execution/load-subgraph/references/catalog-query.md`.

## Callers (name only — never auto-invoke)

| Skill | When to **name** `/map-features` |
|---|---|
| `frame-change` | Reverse predicate holds (stale/missing checkpoint or post-pull) |
| `inspect-change` | After read-only reverse scripts; pending OBS need dispose |
| `load-subgraph` | Envelope/observations band shows pending OBS |
| standalone | Reverse-track, dispose OBS, migrate flat→shared, or catalog backfill |

`inspect-change` may run `scripts/reconcile.py` **read-only** for an advisory
envelope; it must not perform dispose writes.

## Team sync story (INDEX-only)

Full migration notes: [`catalog-sync.md`](catalog-sync.md).

1. Teammate A builds with local triad (gitignored) → `/map-features` **export**
   refreshes the shard → commit/push INDEX (± `catalog/`) only.
2. Teammate B pulls → `/map-features` **materialize** CODE → Draft stubs →
   `specify-behavior` as needed.
3. Reverse + dispose: `/map-features` **dispose** (step 0 reverse, then
   promote/absorb/dismiss). Prefer promote rows that cite `OBS-…` provenance.
