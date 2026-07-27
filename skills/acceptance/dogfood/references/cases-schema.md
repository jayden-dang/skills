# Cases catalog schema (v1)

Load when authoring or validating a dogfood cases file. Canonical contract:
`docs/specs/2026-07-27-dogfood-cli/contract.md`.

## Path

`.skills/<slug>-dogfood.cases.yaml`

## Required top-level

| Field | Type | Notes |
|---|---|---|
| `version` | `1` | Only version supported |
| `feature` | string | Short label |
| `slug` | string | Path stem for ledger/html names |
| `title` | string | Human guide H1 |
| `origin` | string | Local app origin, e.g. `http://localhost:5173` |
| `intro` | string | Optional multi-line intro |
| `sections` | list | Non-empty |

## Required per case

| Field | Notes |
|---|---|
| `id` | Stable, unique (`CASE-1`) |
| `req` | Requirement id (`NOTE-1.1`) |
| `kind` | `happy` \| `edge` \| `error` \| `nonbehavior` \| `persist` \| `visual` \| `journey` |
| `title` | Human label |
| `setup` | Independent precondition |
| `try` | Copy-pasteable steps |
| `expect` | What the user must see (grounded) |
| `backend` | Server assertion, or literal `presentational` |

## CLI

```bash
python3 skills/acceptance/dogfood/scripts/dogfood list .skills/<slug>-dogfood.cases.yaml
python3 skills/acceptance/dogfood/scripts/dogfood render .skills/<slug>-dogfood.cases.yaml -o .skills/<slug>-dogfood.html
python3 skills/acceptance/dogfood/scripts/dogfood init .skills/<slug>-dogfood.cases.yaml -o .skills/<slug>-dogfood-run.md
python3 skills/acceptance/dogfood/scripts/dogfood show .skills/<slug>-dogfood.cases.yaml CASE-1
python3 skills/acceptance/dogfood/scripts/dogfood mark .skills/<slug>-dogfood-run.md CASE-1 pass \
  --saw 'list shows "Alpha"' --server 'GET /api/notes includes Alpha'
python3 skills/acceptance/dogfood/scripts/dogfood status .skills/<slug>-dogfood-run.md
python3 skills/acceptance/dogfood/scripts/dogfood next .skills/<slug>-dogfood-run.md
python3 skills/acceptance/dogfood/scripts/dogfood report .skills/<slug>-dogfood-run.md -o .skills/<slug>-dogfood-report.md
```

Resolve the script relative to this skill package when installed via the skills CLI
(not only this monorepo path).
