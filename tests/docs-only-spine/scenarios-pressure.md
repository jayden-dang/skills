# DOSP pressure scenarios

## P1 — ID only in application-like path (must not E1)

**Setup:** A string `SHELL-9.9` appears only under a path outside `docs/specs/`
(e.g. a consumer `src/foo.test.ts` or a fixture that looks like app code).

**Expect:** docs-only `audit-trace` does **not** emit E1 for that path. E1 fires
only when `_Requirements:` (or ARCH/decision rules) cite an undefined ID.

## P2 — Unknown ID on task footer (must E1)

**Setup:** `tasks.md` contains `_Requirements: FAKE-1.1_` and no bold definition.

**Expect:** E1 for FAKE-1.1 citing the tasks file.

## P3 — Implemented without test tags (must not E2)

**Setup:** Status Implemented, tasks cite IDs, no ID strings in any test file.

**Expect:** No E2 (E2 does not exist). Status flip evidence is process, not grep.
