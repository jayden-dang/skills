# Tasks: check-trace `ignore` capability

Feature code: TRACE
Status: Approved
Date: 2026-07-09
Requirements: ./requirements.md

**Goal:** Add an optional `ignore` substring-list to check-trace's config that excludes
fixture-bearing test files from the trace scan.

**Tech Stack:** Node ESM (`scripts/check-trace.mjs`), zero dependencies, `node --test`.

## Global Constraints

- Zero dependencies; substring match only (no glob/regex engine); `ignore` is off by default.
- Tests live in `scripts/check-trace.test.mjs` (spawnSync fixtures), tagged `[TRACE-1.x]`.

---

### Task 1: `ignore` filter in the test-file scan (tier-1, one capability)

Built as one change via `tdd`; check-trace had no prior spec (bootstrapped here). Each
criterion carries a `[TRACE-1.x]` test in `scripts/check-trace.test.mjs`.

**Files:**
- Modify: `scripts/check-trace.mjs` (`ignore: []` in DEFAULTS; walk predicate excludes files whose repo-relative path contains any non-empty ignore substring)
- Test: `scripts/check-trace.test.mjs`

**Delivered (test-first, all tagged):**
- [x] **TRACE-1.1** `ignore` excludes files whose repo-relative path contains a listed substring; empty/blank entries are no-ops — `[TRACE-1.1]`
- [x] **TRACE-1.2** an excluded file contributes no requirement-ID references (no false E1) — `[TRACE-1.2]`
- [x] **TRACE-1.3** absent/empty `ignore` or no trace.json → scan everything as before — `[TRACE-1.3]`
- [x] **TRACE-1.4** guard: `testGlobs`/`testFilePattern` still applied; `ignore` is additive — `[TRACE-1.4]`
- [x] **TRACE-1.5** guard: no `ignore` → byte-identical output + exit code — `[TRACE-1.5]`

Commits: `4e0b25c` (ignore filter), `b8ab172` (empty-entry hardening).

_Requirements: TRACE-1.1, TRACE-1.2, TRACE-1.3, TRACE-1.4, TRACE-1.5_

---

## Coverage check

Every TRACE ID (1.1–1.5) is cited by Task 1 and carries a `[TRACE-1.x]` test in
`scripts/check-trace.test.mjs`.

**Environment note:** TRACE stays `Approved`, not `Implemented`, in this repo. Its tests
live in `scripts/check-trace.test.mjs` — the very file the skills repo's `trace.json`
excludes (it holds the `RET-*` retirement fixtures). So check-trace cannot see TRACE's own
coverage here and would fire E2 if TRACE were marked Implemented. The tests exist and pass
(7/7); this is the same authoring-repo quirk that `ignore` exists to work around, one level
down. In a consuming repo whose tests are elsewhere, TRACE would flip cleanly.
