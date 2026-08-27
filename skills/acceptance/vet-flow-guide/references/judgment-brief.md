# Judgment brief — vet-flow-guide

Fill every field before dispatching a read-only judgment subagent (or before an
inline `AUTHORING CLOSED` pass). Keep under 400 words of free prose beyond the
paths. Do not pre-judge findings. Do not attach full session history.

## Paths (required)

| Field | Value |
|---|---|
| **Run file path** | `.skills/<CODE>/flow-guide.json` (repo-relative) |
| **Report path** | `.skills/<CODE>/vet-flow-guide.md` |
| **Prior report** (re-check) | path or `—` |
| **pass_kind** | `initial` \| `re-check` |

## Optional triad paths

| Field | Value |
|---|---|
| **requirements.md** | `docs/specs/<feature>/requirements.md` or `—` |
| **design.md** | path or `—` |
| **tasks.md** | path or `—` |

Use triad only for Out-of-Scope / persist / spec claims. Implementation claims
require opened product code.

## Product surfaces to open

List concrete product paths from design/tasks/known app layout (routes, pages,
components). Not a fictional “source roots” config field.

- …

## Read-only rules (non-negotiable)

1. **Read-only** on the product codebase — no patches, no commits to product.
2. **Do not write or modify the run file** — no case adds/edits, no `rev` bumps
   from this pass.
3. **May write** only the vet **report** at the report path (or return full
   report markdown for the controller to write verbatim).
4. Do not self-declare clean without writing the report.
5. Do not invent chaos/load/race/fuzz suites, novelty/feel taste, speculative
   “users will want” items, or global “ready to ship” stamps.
6. Skip candidate surfaces you did not open; require file/symbol/route evidence
   on every missing-situation finding.
7. Finding ids: `VFG-N` integers; reuse `surface_key` → id map from prior report
   on re-check.

## Map procedure (summary)

1. Open user-observable shipped paths/states from product code.
2. Match each against run-file cases (judgment match).
3. Emit missing-situation findings with `surface_key`, severity, situation,
   evidence.
4. Stamp `cases_fingerprint` per `report-schema.md`; write the report.

## Return

Report path + open_count. Controller does not re-judge content.
