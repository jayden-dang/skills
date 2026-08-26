# `reconcile-features`

> Reverse-track external commits and brownfield surfaces onto the capability
> catalog — known-impact, OBS candidates, no-spec-impact, uncertain — as a
> bounded advisory envelope plus local `.skills/reverse-features/` index.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invoked |
| **Reads** | git `base..head`, live `docs/specs/` (flat or optional sharded catalog), active OBS overlay |
| **Writes** | local `.skills/reverse-features/` only (stateless if not writable/ignored); never `docs/specs/**`, never consuming-repo CI |
| **Called by** | `frame-change` (reverse-track predicate in step 1), `inspect-change` (step 1b on pinned range); also standalone on reverse-track asks |

## What it produces

One envelope (`schema_version: "1"`, `recipe_id: "rfeat-1.0"`) per
`skills/execution/reconcile-features/references/envelope.md`, then index-then-advance
of pending OBS under `.skills/reverse-features/`.

Observations use `OBS-<6hex>` from evidence locators — never Feature CODEs.
Promotion/absorb/dismiss is human disposition; name `/map-features` for
confirm-then-write backfill.

## Bundled runner

Mechanical inventory (no overlay write by default):

```bash
python3 skills/execution/reconcile-features/scripts/reconcile.py \
  --repo <root> --base <sha> --head <sha> --mode changes-since-checkpoint

# Index OBS + advance checkpoint (requires .skills/ gitignored + writable)
python3 skills/execution/reconcile-features/scripts/reconcile.py \
  --repo <root> --base <sha> --head <sha> --mode changes-since-checkpoint \
  --write-overlay
```

Uses index-first OWNS (`scripts/owns.py`, flat or sharded INDEX), clustering
(`scripts/cluster.py`), overlay write (`scripts/overlay.py`), and a balanced
`FINDINGS_MAX` budget. Judgment corpus fixtures live under
`scripts/testdata/corpus/`.

## Modes

| Mode | When |
|---|---|
| `changes-since-checkpoint` | Valid `last_reconciled_sha` ancestor of HEAD, or post-pull `ORIG_HEAD..HEAD` |
| `full` / `brownfield-bootstrap` | Missing/stale checkpoint, or no specs yet (OBS only — no Approved SHALLs from code) |

See `skills/execution/reconcile-features/SKILL.md` and `references/passes.md`.
Design record: `docs/adr/0001-query-first-feature-territory.md`.
