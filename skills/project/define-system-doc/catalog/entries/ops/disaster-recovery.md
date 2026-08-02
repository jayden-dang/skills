# Entry: `ops/disaster-recovery`

## Purpose and boundary
Hybrid 1A document for `ops/disaster-recovery`.

## Canonical consumer path
`docs/ops/disaster-recovery.md`

## Applicability
Adopt when the project needs this standing document.

## Mediated writer
`/define-system-doc` (`skills/project/define-system-doc/SKILL.md`)

## Template
`templates/ops/disaster-recovery.md`

## Validator
`validators/ops/disaster-recovery.md` (structural pass/fail)

## Evidence sources
Repository/runtime facts with grades; human confirmation for high-risk classes.

## Authority predicate
- **Absent:** no file at `docs/ops/disaster-recovery.md`
- **Non-authoritative:** missing Approved status or structural validator fail
- **Approved:** `Status: Approved` and structural validator pass

## Real readers and decision points
| Reader | Decision point | Suggestion protocol |
|---|---|---|
| `skills/execution/root-cause/SKILL.md` | recovery context | Optional |

## No-op when absent or non-authoritative
Named readers continue without failing solely for absence.

## Maturity
Authoritative only in `CATALOG.md`.
