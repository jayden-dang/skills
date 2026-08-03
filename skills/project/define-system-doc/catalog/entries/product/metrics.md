# Entry: `product/metrics`

## Purpose and boundary
Standing Hybrid 1A document for `product/metrics`.

## Canonical consumer path
`docs/product/metrics.md`

## Applicability
Adopt when the project needs this standing product or architecture-shape document.

## Mediated writer
Primary progressive author: `/define-system-doc` (`skills/project/define-system-doc/SKILL.md`).
`define-project` may also maintain product/architecture layer docs when updating the project layer; it must not invent parallel SSOTs.

## Template
`templates/product/metrics.md`

## Validator
`validators/product/metrics.md` (structural pass/fail)

## Evidence sources
Product interviews, vision goals, codebase topology; human confirmation for standing claims.

## Authority predicate
- **Absent:** no file at `docs/product/metrics.md`
- **Non-authoritative:** file exists but `Status` is not `Approved`, or structural validator fails
- **Approved:** `Status: Approved` and structural validator returns pass

## Real readers and decision points
| Reader | Decision point | Suggestion protocol |
|---|---|---|
| `skills/discovery/frame-change/SKILL.md` | Product scope / users / goals check | Yes — once per entry per frame-change when material |
| `skills/spec/specify-behavior/SKILL.md` | NFR Performance grounding (Step 2b) | Yes — once per entry when Performance NFR material |
| `skills/acceptance/validate-feature/SKILL.md` | Acceptance checklist / success criteria | Yes — once per entry per validate-feature when metrics/personas material |
| `skills/project/define-project/SKILL.md` | Project layer create/update | No auto; may name define-system-doc |

## No-op when absent or non-authoritative
Named readers continue without failing solely for absence.

## Maturity
Authoritative only in `CATALOG.md`.
