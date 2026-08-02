# Testing standards

Status: Approved
Date: 2026-08-02

## Purpose and boundary

How this skill-set pack is tested and how consumer features should apply test-first.

## Strategy

| Layer | Purpose | When required |
|---|---|---|
| unit | Contract tests over skill markdown, fixtures, scripts | Every pack behavior change |
| integration / e2e | Consumer app acceptance (`validate-api` / `validate-ui`) | When a consumer app surface exists |
| pressure / scenario | Process pressure suites under `tests/` | When skill process changes |

## Test-first rules

- No production code (including skill procedure that changes behavior) without a failing test first when this pack's test-first skill applies.
- Prefer domain-language assertions; do not require requirement IDs in application/test source (docs-only spine).
- Pack fixture tests may embed greppable `CODE-N.M` when testing this skill set itself.

## Mocks and boundaries

- Mock only at system boundaries for consumer apps; do not assert on mock call counts as proof of behavior.
- For pack tests, prefer file/fixture observation over process mocks.

## Verify commands (this pack)

See `docs/agents/project.md`: lint scripts + `python3 -m unittest discover -s tests`.

## Not a substitute for acceptance

Unit conventions here do not replace `validate-feature` / e2e acceptance for consumer apps.
