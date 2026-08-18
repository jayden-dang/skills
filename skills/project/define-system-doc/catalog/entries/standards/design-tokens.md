# Entry: `standards/design-tokens`

## Purpose and boundary
Hybrid 1A document for `standards/design-tokens` — the product-UI visual
contract: allowed stack, token vocabulary and source of truth, numeric floors,
named forbidden patterns, component inventory.

## Canonical consumer path
`docs/standards/design-tokens.md`

## Applicability
Adopt when the project ships browser-rendered UI and wants its visual
vocabulary enforced rather than re-invented per feature.

## Mediated writer
`/define-system-doc` (`skills/project/define-system-doc/SKILL.md`)

## Template
`templates/standards/design-tokens.md`

## Validator
`validators/standards/design-tokens.md` (structural pass/fail)

## Evidence sources
The repo's real token/theme/component files (paths, values); human
confirmation for stack and forbidden-pattern choices.

## Authority predicate
- **Absent:** no file at `docs/standards/design-tokens.md`
- **Non-authoritative:** missing Approved status or structural validator fail
- **Approved:** `Status: Approved` and structural validator pass

## Real readers and decision points
| Reader | Decision point | Suggestion protocol |
|---|---|---|
| `skills/spec/design-solution/SKILL.md` | Step 2b `Grounding:` | Yes |
| `skills/review/review-ui/SKILL.md` | Step 3 contract | Yes |
| `skills/craft/craft-page/SKILL.md` | §2 precedence (existing system) | Optional |
| `skills/acceptance/validate-ui/SKILL.md` | UI acceptance | Optional |

## No-op when absent or non-authoritative
Named readers continue without failing solely for absence.

## Maturity
Authoritative only in `CATALOG.md`.
