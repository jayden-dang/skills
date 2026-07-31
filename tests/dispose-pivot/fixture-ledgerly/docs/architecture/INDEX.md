# Architecture: Ledgerly

Status: Approved
Date: 2025-11-03

## Invariants

- **ARCH-1** Every write goes to the local SQLite store first; the sync layer only ever replays a committed local write.
- **ARCH-2** No module may read the network on a user-interactive code path.
- **ARCH-3** Ledger rows are single-owner; no row carries a tenant, org, or account-group identifier.
- **ARCH-4** Categorisation runs on-device; no transaction text leaves the device.

## Domains

None.
