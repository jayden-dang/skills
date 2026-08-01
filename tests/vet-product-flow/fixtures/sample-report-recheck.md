# Vet product flow — demo

- **slug:** `demo`
- **run_file:** `.skills/demo-review-product-flow.json`
- **cases_fingerprint:** `0000000000000000000000000000000000000000000000000000000000000000`
- **stamped_at:** `2026-08-01T11:00:00Z`
- **pass_kind:** `re-check`
- **prior_report:** `.skills/demo-vet-product-flow.md`
- **open_count:** 2
- **gate_hint:** `blocked`

## Open findings

### VPF-1
- **status:** open
- **severity:** Important
- surface_key: `ui:settings/empty — no rows`
- **situation:** Settings list empty-state still uncased after guide-gap pass 1.
- **evidence:** `src/pages/Settings.tsx:88` (EmptyState), route `/settings`

### VPF-2
- **status:** open
- **severity:** Minor
- surface_key: `ui:settings/error — load failed`
- **situation:** Settings page shows load-error banner when GET /api/settings fails; guide has no error kind on that surface.
- **evidence:** `src/pages/Settings.tsx:102` (ErrorBanner), route `/settings`

## Cleared this pass

_(none)_
