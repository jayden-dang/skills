# Entry: `standards/observability`

## Purpose and boundary
Hybrid 1A document for `standards/observability`.

## Canonical consumer path
`docs/standards/observability.md`

## Applicability
Adopt when the project needs this standing document.

## Mediated writer
`/define-system-doc` (`skills/project/define-system-doc/SKILL.md`)

## Template
`templates/standards/observability.md`

## Validator
`validators/standards/observability.md` (structural pass/fail)

## Evidence sources
Repository/runtime facts with grades; human confirmation for high-risk classes.

## Authority predicate
- **Absent:** no file at `docs/standards/observability.md`
- **Non-authoritative:** missing Approved status or structural validator fail
- **Approved:** `Status: Approved` and structural validator pass

## Real readers and decision points
| Reader | Decision point | Suggestion protocol |
|---|---|---|
| `skills/spec/design-solution/SKILL.md` | instrumentation design | Yes |
| `skills/spec/plan-tasks/SKILL.md` | observability constraints | Yes |

## No-op when absent or non-authoritative
Named readers continue without failing solely for absence.

## Maturity
Authoritative only in `CATALOG.md`.
