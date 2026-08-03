# Entry: `security/compliance`

## Purpose and boundary
Hybrid 1A document for `security/compliance`.

## Canonical consumer path
`docs/security/compliance.md`

## Applicability
Adopt when the project needs this standing document.

## Mediated writer
`/define-system-doc` (`skills/project/define-system-doc/SKILL.md`)

## Template
`templates/security/compliance.md`

## Validator
`validators/security/compliance.md` (structural pass/fail)

## Evidence sources
Repository/runtime facts with grades; human confirmation for high-risk classes.

## Authority predicate
- **Absent:** no file at `docs/security/compliance.md`
- **Non-authoritative:** missing Approved status or structural validator fail
- **Approved:** `Status: Approved` and structural validator pass

## Real readers and decision points
| Reader | Decision point | Suggestion protocol |
|---|---|---|
| `skills/spec/specify-behavior/SKILL.md` | NFR Security grounding when regulatory (Step 2b) | Yes — once per entry when compliance material |
| `skills/spec/design-solution/SKILL.md` | Security: CMP citations | Yes |
| `skills/execution/audit-trace/SKILL.md` | CMP referential integrity | No suggest |

## No-op when absent or non-authoritative
Named readers continue without failing solely for absence.

## Maturity
Authoritative only in `CATALOG.md`.
