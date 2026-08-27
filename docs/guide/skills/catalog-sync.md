# Catalog sync (INDEX-only)

Optional team posture: sync a **thin feature catalog** on git; keep full
requirements/design/tasks as **local workbenches**.

## Opt in

```bash
# In the consumer repo
/configure-repo
# Decision L → Catalog sync: index-only
```

Writes `Catalog sync: index-only` to `docs/agents/project.md` and appends
gitignore so `docs/specs/INDEX.md` (± `docs/specs/catalog/`) stays tracked while
`docs/specs/*/` feature dirs stay local. **Do not** `git add -f` those dirs.

## Loop

| Who | Steps |
|---|---|
| A (author) | Local triad → `/map-features` **export** → commit/push **INDEX only** |
| B (teammate) | `git pull` → `/map-features` **materialize** CODE → Draft stubs → `specify-behavior` when needed |
| Either | `reconcile-features` for OBS → `/map-features` **dispose** |

## Migrate full-triad → index-only

1. Ensure INDEX is complete for live CODEs (`/map-features` dispose / export dry-run).
2. `/configure-repo` → set Catalog sync `index-only` (gitignore snippet).
3. For each feature dir already tracked: `git rm -r --cached docs/specs/<slug>/` (keep files on disk).
4. Commit INDEX + `.gitignore` only. Warn the team about `git add -f`.

## Migrate index-only → full-triad

1. Set Catalog sync `full-triad` (or remove the field).
2. Remove the index-only gitignore block.
3. `git add docs/specs/<slug>/` for dirs the team agrees to share.
4. Export/materialize modes disable until `index-only` again.

## Stub fingerprint

Materialize stubs start with:

```html
<!-- map-features-materialize-stub: v1 -->
```

If a target file exists **without** this marker (or with real content), refuse
clobber — ask the user.

See also: [`map-features`](map-features.md), [`reconcile-features`](reconcile-features.md).
