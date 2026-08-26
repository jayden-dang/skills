# `audit-trace` — catalog integrity (v1.1.0)

**Roster:** grok-4.6, grok-4.5.
**Scenario:** `.skills/_pending-reconcile/red-audit-catalog-scenario.md`.

## Failure class

**Omits catalog checks.** v1.0.0 covered triad + optional ARCH/system IDs only.
Duplicate INDEX CODEs, OBS tokens in Code cells, and missing shard paths were
invisible to prove-claim / cut-release.

Form: optional catalog passes (when INDEX exists) + finding codes E11–E13 / W4–W5.

### RED (v1.0.0)

| Run | Model | FINDING_CODES | REPORTS_DUP / OBS / SHARD |
|---|---|---|---|
| catalog defects + clean triad | grok-4.5 | none | no / no / no |
| same | grok-4.6 | none | no / no / no |

Verbatim: "The skill never greps docs/specs/INDEX.md" / "Catalog integrity is
outside this skill’s passes."

### GREEN (v1.1.0)

| Run | Model | FINDING_CODES |
|---|---|---|
| same | grok-4.5 | E11,E12,E13 |
| same | grok-4.6 | E11,E12,E13 |

Both: `REPORTS_DUP_CODE: yes`, `REPORTS_OBS_IN_CATALOG: yes`,
`REPORTS_MISSING_SHARD: yes`.

## Quality pass (v1.1.1) — author-skills wording sweep

E13 token locked to OBS-<6hex>; opening table is the one code list; "The rules"
no longer a stale subset; W5 skip tied to INDEX absence as contracted.
