# Requirements: check-trace `ignore` capability

Feature code: TRACE
Status: Approved
Date: 2026-07-09

<!--
Scope note: check-trace (scripts/check-trace.mjs) predates this repo's spec system and is
intentionally NOT retro-spec'd. This is a minimal spec for ONE new capability only — an
optional `ignore` list in docs/agents/trace.json that excludes fixture-bearing test files
from the trace scan.

Why: a repo's test files can legitimately contain example/fixture requirement IDs — e.g.
check-trace's own retirement-convention test (scripts/check-trace.test.mjs) embeds RET-1.1
and RET-9.9 as fixture strings. When such a file is scanned as a test file, check-trace
reads those IDs as real citations and fires false E1 "cites unknown requirement" errors.
`ignore` lets a repo exclude those files. Motivating consumer: the skills repo needs to scan
`scripts/` (where FGRAPH's tests live) while excluding check-trace.test.mjs, so FGRAPH can
reach a green trace gate and flip to Implemented.

Existing behavior (verified): loadConfig() reads docs/agents/trace.json merged over DEFAULTS
(specsDir, testGlobs = array of dir roots, testFilePattern = regex string). walk() collects
files under testGlobs whose repo-relative path matches testFilePattern; those become the
test-file set scanned for requirement-ID references.

Semantics (brainstorm decision): `ignore` is a path-SUBSTRING list — zero-dependency, no
glob/regex engine. A file is excluded if its repo-relative path contains any listed string.
-->

## 1. Ignore/exclude test files from the trace scan

**Story:** As a repo maintainer whose test files contain example or fixture requirement IDs, I want to exclude specific test files from check-trace's scan, so those fixture IDs do not fire false "cites unknown requirement" errors and I can still trace-check the rest of the repo.

- **TRACE-1.1** WHERE `docs/agents/trace.json` provides an `ignore` array, THE SYSTEM SHALL exclude from the test-file scan any file whose repo-relative path contains any of the listed substrings.
- **TRACE-1.2** WHEN an `ignore` entry excludes a file, THE SYSTEM SHALL NOT collect any requirement-ID references from that file, so a fixture ID inside it cannot fire an E1 "cites unknown requirement" error.
- **TRACE-1.3** IF `ignore` is absent, empty, or `trace.json` does not exist, THEN THE SYSTEM SHALL scan every test file exactly as before — the ignore filter is off by default.
- **TRACE-1.4** (guard) WHEN the ignore filter runs, THE SYSTEM SHALL CONTINUE TO apply `testGlobs` and `testFilePattern` unchanged; `ignore` is an additional exclusion layered on top of the existing file selection, never a replacement for it.
- **TRACE-1.5** (guard) WHEN no `ignore` is configured, THE SYSTEM SHALL CONTINUE TO produce byte-identical output and the same exit code as before this change.

## Out of Scope

- **Glob or regex matching** — `ignore` is a plain path-substring list; no `*`/`**` glob engine and no regex are introduced (that would add code to a zero-dependency tool for no proven need).
- **Ignoring requirements/spec files** — `ignore` filters the TEST-file walk only. It never excludes a `requirements.md`/`fixes.md` from defining IDs; a repo cannot use it to hide a real requirement from coverage checking.
- **Retro-spec'ing the rest of check-trace** — every other check-trace behavior (E1/E2/E3/W1/W2, the ID grammar, strikethrough retirement) remains as-built and unspec'd; this spec covers the `ignore` capability alone.
- **Per-rule or per-check ignores** — `ignore` excludes a whole file from the test scan; it does not suppress an individual error code on a still-scanned file.
