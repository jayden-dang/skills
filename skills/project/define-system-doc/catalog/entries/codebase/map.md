# Entry: `codebase/map`

## Purpose and boundary
Codebase Map: placement and top-level layout guidance for where new code belongs. Not the architecture invariant spine and not the feature registry (`docs/specs/INDEX.md`).

## Canonical consumer path
`docs/codebase/map.md`

## Applicability
Use when planning or placing production code paths and the repository benefits from standing placement rules.

## Mediated writer
`/define-system-doc` → `skills/project/define-system-doc/SKILL.md` (one artifact per invocation)

## Template
`templates/codebase/map.md` (skill-local under define-system-doc)

## Validator
`validators/codebase/map.md` (structural pass/fail)

## Evidence sources
Repository tree listing; existing path conventions; human confirmation for ownership claims.

## Authority predicate
- **Absent:** no file at `docs/codebase/map.md`
- **Non-authoritative:** file exists but `Status` is not `Approved`, or structural validator fails
- **Approved:** `Status: Approved` and structural validator returns pass

## Real readers and decision points
| Reader | Decision point | Suggestion protocol |
|---|---|---|
| `skills/spec/plan-tasks/SKILL.md` | File Structure / path placement | Yes — when placement uncertain and map not authoritative; exact `/define-system-doc codebase/map` |

## No-op when absent or non-authoritative
`plan-tasks` continues without failing solely for map absence; may suggest authoring once per run.

## Maturity
Authoritative only in `CATALOG.md` (do not duplicate maturity here).
