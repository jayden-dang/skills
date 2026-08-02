# Entry: `standards/INDEX`

## Purpose and boundary
Engineering standards document for `standards/INDEX`.

## Canonical consumer path
`docs/standards/INDEX.md`

## Applicability
Adopt when the project maintains standing engineering standards under `docs/standards/`.

## Mediated writer
`/define-system-doc` → `skills/project/define-system-doc/SKILL.md`.  
`define-project` owns migration of `docs/product/guidelines.md` to a pointer when standards exist.

## Template
`templates/standards/INDEX.md`

## Validator
`validators/standards/INDEX.md` (structural pass/fail)

## Evidence sources
Existing guidelines; house rules; test commands in `docs/agents/project.md`; human confirmation.

## Authority predicate
- **Absent:** no file at `docs/standards/INDEX.md`
- **Non-authoritative:** file exists but `Status` is not `Approved`, or structural validator fails
- **Approved:** `Status: Approved` and structural validator returns pass

## Real readers and decision points
| Reader | Decision point | Suggestion protocol |
|---|---|---|
| `skills/spec/plan-tasks/SKILL.md` | Global Constraints engineering rules | Yes — once per entry when standards material |
| `skills/execution/test-first/SKILL.md` | TDD procedure (testing.md) | Yes — once for standards/testing when material |
| `skills/review/inspect-change/SKILL.md` | Standards axis sources | Optional suggest once; never auto-invoke |
| `skills/project/define-project/SKILL.md` | Guidelines migration / project layer | Name define-system-doc; never parallel SSOT |

## No-op when absent or non-authoritative
Named readers fall back per skill rules (guidelines pointer or project.md).

## Maturity
Authoritative only in `CATALOG.md`.
