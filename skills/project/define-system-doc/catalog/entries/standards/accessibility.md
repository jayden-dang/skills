# Entry: `standards/accessibility`

## Purpose and boundary
Hybrid 1A document for `standards/accessibility`.

## Canonical consumer path
`docs/standards/accessibility.md`

## Applicability
Adopt when the project needs this standing document.

## Mediated writer
`/define-system-doc` (`skills/project/define-system-doc/SKILL.md`)

## Template
`templates/standards/accessibility.md`

## Validator
`validators/standards/accessibility.md` (structural pass/fail)

## Evidence sources
Repository/runtime facts with grades; human confirmation for high-risk classes.

## Authority predicate
- **Absent:** no file at `docs/standards/accessibility.md`
- **Non-authoritative:** missing Approved status or structural validator fail
- **Approved:** `Status: Approved` and structural validator pass

## Real readers and decision points
| Reader | Decision point | Suggestion protocol |
|---|---|---|
| `skills/spec/specify-behavior/SKILL.md` | NFR Accessibility grounding (Step 2b) | Yes — once per entry when UI a11y NFR material |
| `skills/spec/design-solution/SKILL.md` | a11y design | Yes |
| `skills/acceptance/validate-ui/SKILL.md` | a11y checks | Yes |
| `skills/review/inspect-change/SKILL.md` | Standards axis | Optional |

## No-op when absent or non-authoritative
Named readers continue without failing solely for absence.

## Maturity
Authoritative only in `CATALOG.md`.
