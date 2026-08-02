# Entry: `standards/api`

## Purpose and boundary
Hybrid 1A document for `standards/api`.

## Canonical consumer path
`docs/standards/api.md`

## Applicability
Adopt when the project needs this standing document.

## Mediated writer
`/define-system-doc` (`skills/project/define-system-doc/SKILL.md`)

## Template
`templates/standards/api.md`

## Validator
`validators/standards/api.md` (structural pass/fail)

## Evidence sources
Repository/runtime facts with grades; human confirmation for high-risk classes.

## Authority predicate
- **Absent:** no file at `docs/standards/api.md`
- **Non-authoritative:** missing Approved status or structural validator fail
- **Approved:** `Status: Approved` and structural validator pass

## Real readers and decision points
| Reader | Decision point | Suggestion protocol |
|---|---|---|
| `skills/spec/design-solution/SKILL.md` | API design sections | Yes once/entry |
| `skills/spec/plan-tasks/SKILL.md` | API-related constraints | Yes once/entry |
| `skills/acceptance/validate-api/SKILL.md` | API acceptance | Yes once when API surface |
| `skills/review/inspect-change/SKILL.md` | Standards axis | Optional suggest |

## No-op when absent or non-authoritative
Named readers continue without failing solely for absence.

## Maturity
Authoritative only in `CATALOG.md`.
