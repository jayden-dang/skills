# Entry: `ops/reliability`

## Purpose and boundary
Hybrid 1A document for `ops/reliability`.

## Canonical consumer path
`docs/ops/reliability.md`

## Applicability
Adopt when the project needs this standing document.

## Mediated writer
`/define-system-doc` (`skills/project/define-system-doc/SKILL.md`)

## Template
`templates/ops/reliability.md`

## Validator
`validators/ops/reliability.md` (structural pass/fail)

## Evidence sources
Repository/runtime facts with grades; human confirmation for high-risk classes.

## Authority predicate
- **Absent:** no file at `docs/ops/reliability.md`
- **Non-authoritative:** missing Approved status or structural validator fail
- **Approved:** `Status: Approved` and structural validator pass

## Real readers and decision points
| Reader | Decision point | Suggestion protocol |
|---|---|---|
| `skills/spec/specify-behavior/SKILL.md` | NFR Reliability grounding (Step 2b) | Yes — once per entry when Reliability NFR material |
| `skills/spec/design-solution/SKILL.md` | Reliability: SLO citations | Yes |
| `skills/execution/audit-trace/SKILL.md` | SLO referential integrity | No suggest |

## No-op when absent or non-authoritative
Named readers continue without failing solely for absence.

## Maturity
Authoritative only in `CATALOG.md`.
