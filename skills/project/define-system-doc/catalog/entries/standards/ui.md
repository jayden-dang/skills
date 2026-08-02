# Entry: `standards/ui`

## Purpose and boundary
Hybrid 1A document for `standards/ui`.

## Canonical consumer path
`docs/standards/ui.md`

## Applicability
Adopt when the project needs this standing document.

## Mediated writer
`/define-system-doc` (`skills/project/define-system-doc/SKILL.md`)

## Template
`templates/standards/ui.md`

## Validator
`validators/standards/ui.md` (structural pass/fail)

## Evidence sources
Repository/runtime facts with grades; human confirmation for high-risk classes.

## Authority predicate
- **Absent:** no file at `docs/standards/ui.md`
- **Non-authoritative:** missing Approved status or structural validator fail
- **Approved:** `Status: Approved` and structural validator pass

## Real readers and decision points
| Reader | Decision point | Suggestion protocol |
|---|---|---|
| `skills/spec/design-solution/SKILL.md` | UI design | Yes |
| `skills/spec/plan-tasks/SKILL.md` | UI constraints | Yes |
| `skills/acceptance/validate-ui/SKILL.md` | UI acceptance | Yes |
| `skills/review/inspect-change/SKILL.md` | Standards axis | Optional |

## No-op when absent or non-authoritative
Named readers continue without failing solely for absence.

## Maturity
Authoritative only in `CATALOG.md`.
