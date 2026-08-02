# Entry: `standards/security-coding`

## Purpose and boundary
Hybrid 1A document for `standards/security-coding`.

## Canonical consumer path
`docs/standards/security-coding.md`

## Applicability
Adopt when the project needs this standing document.

## Mediated writer
`/define-system-doc` (`skills/project/define-system-doc/SKILL.md`)

## Template
`templates/standards/security-coding.md`

## Validator
`validators/standards/security-coding.md` (structural pass/fail)

## Evidence sources
Repository/runtime facts with grades; human confirmation for high-risk classes.

## Authority predicate
- **Absent:** no file at `docs/standards/security-coding.md`
- **Non-authoritative:** missing Approved status or structural validator fail
- **Approved:** `Status: Approved` and structural validator pass

## Real readers and decision points
| Reader | Decision point | Suggestion protocol |
|---|---|---|
| `skills/spec/design-solution/SKILL.md` | security-sensitive design | Yes |
| `skills/review/inspect-change/SKILL.md` | Standards/security | Optional |

## No-op when absent or non-authoritative
Named readers continue without failing solely for absence.

## Maturity
Authoritative only in `CATALOG.md`.
