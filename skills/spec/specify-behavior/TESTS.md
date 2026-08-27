# `specify-behavior` — Open Questions ownership (2026-08-27)

Companion to clarify-decisions v1.2.0 Owned unknowns. Model roster: grok-class.

## Baseline failure (pre-1.2.0)

| Scenario | Pressures | Observed | Rationalization |
|---|---|---|---|
| **S-OWNED-TBD-APPROVE** | authority + pragmatic | Bare `- TBD: SLO window` in Open Questions could reach Approve; clarify unknowns dropped | "Open Questions can stay messy" / "later NFR" |

## GREEN — v1.2.0 / wording 1.2.1

| Scenario | Required | Observed |
|---|---|---|
| S-OWNED-TBD-APPROVE | Block Approve on bare TBD; require owner · date · forbid-guess (`cấm đoán`) or resolve | **Pass** — agent refused Approve; cited Placeholder scan |

Wording 1.2.1: English **forbid-guess** primary; `cấm đoán` gloss retained.

## Rules this evidence owns

| Rule | Evidence |
|---|---|
| Bare TBD without owner/date/cấm đoán blocks `Status: Approved` | GREEN S-OWNED-TBD-APPROVE |
| Paste Owned unknowns from clarify close package into Open Questions | SKILL.md Step 5 Placeholder scan |
| Do not mark Reliability NFR `None` when close package already locked reliability | SKILL.md Step 5 Close-package ingest |
