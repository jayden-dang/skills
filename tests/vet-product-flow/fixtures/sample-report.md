# Vet product flow — demo

- **slug:** `demo`
- **run_file:** `.skills/demo-review-product-flow.json`
- **cases_fingerprint:** `0000000000000000000000000000000000000000000000000000000000000000`
- **stamped_at:** `2026-08-01T10:00:00Z`
- **pass_kind:** `initial`
- **prior_report:** `—`
- **open_count:** 1
- **gate_hint:** `blocked`

## Open findings

### VPF-1
- **status:** open
- **severity:** Important
- surface_key: `ui:settings/empty — no rows`
- **situation:** Settings list already renders empty-state copy when zero rows; guide has only happy create/list.
- **evidence:** `src/pages/Settings.tsx:88` (EmptyState), route `/settings`

## Cleared this pass

_(none — initial pass)_
