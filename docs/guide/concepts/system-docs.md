# System documentation model

Standing project docs above any single feature: product intent, architecture shape,
codebase placement, security, standards, and operations. Feature requirements stay in
`docs/specs/`.

## Pack catalog (SSOT)

The skill set ships a **pack-local** catalog (not copied into every consumer repo):

- Index: `skills/project/define-system-doc/catalog/CATALOG.md` — Entry key | Maturity | package pointer
- Packages: `skills/project/define-system-doc/catalog/entries/<entry-key>.md`

**Hybrid 1A** is exactly the entry-key set in that catalog (36 keys), including
`product/vision`, `architecture/INDEX`, `codebase/map`, `security/*`, `standards/*`,
`ops/*`, `roadmap/INDEX`, `specs/INDEX`, `adr`, `agents/config`, `glossary`, `out-of-scope`,
and related rows.

### Maturity (pack support)

| Maturity | Meaning |
|---|---|
| **First-class** | Full package: template (if template-mediated), validator, writer, real consult hook, reader tests, guide coverage |
| **Recognized** | In the official model with purpose/path; no pack template/validator/reader claimed |
| **Deferred** | Possibility only; fields may be `None — deferred` |

Consumer adoption is **derived** (`Absent` | `Non-authoritative` | `Approved`), never stored in the pack catalog. Authority predicates are **per entry**.

## Authoring: `/define-system-doc`

User-invoked skill `define-system-doc` authors **one** entry per run. Unfinished work:

```
.skills/system-docs/<entry-key>/{state,evidence,proposal}.md
```

Canonical consumer files are written only after explicit approval of a **structural**
validator-passing proposal. The mediated workflow never creates canonical Draft files.

### First-class codebase entries

| Entry key | Consumer path | Primary readers |
|---|---|---|
| `codebase/map` | `docs/codebase/map.md` | `plan-tasks` |
| `codebase/modules` | `docs/codebase/modules.md` | `plan-tasks`, `design-solution`, `inspect-change` |
| `codebase/ownership` | `docs/codebase/ownership.md` | `plan-tasks`, `design-solution`, `inspect-change` (advisory only — not authz) |
| `codebase/dependencies` | `docs/codebase/dependencies.md` | `plan-tasks`, `design-solution`, `inspect-change` |
| `product/personas` | `docs/product/personas.md` | `frame-change`, `validate-feature`, `define-project` |
| `product/metrics` | `docs/product/metrics.md` | `frame-change`, `validate-feature`, `define-project` |
| `product/principles` | `docs/product/principles.md` | `frame-change`, `validate-feature`, `define-project` |
| `architecture/system` | `docs/architecture/system.md` | `design-solution`, `define-project` |
| `architecture/data` | `docs/architecture/data.md` | `design-solution`, `define-project` |
| `architecture/integrations` | `docs/architecture/integrations.md` | `design-solution`, `define-project` |
| `architecture/runtime` | `docs/architecture/runtime.md` | `design-solution`, `define-project` |
| `standards/INDEX` | `docs/standards/INDEX.md` | `plan-tasks`, `inspect-change`, `define-project` |
| `standards/testing` | `docs/standards/testing.md` | `plan-tasks`, `test-first`, `inspect-change` |
| `standards/errors-logging` | `docs/standards/errors-logging.md` | `plan-tasks`, `inspect-change` |
| `standards/api` … `observability` | `docs/standards/<name>.md` | design-solution, plan-tasks, validate-api/ui, inspect-change |
| `security/threat-model` | `docs/security/threat-model.md` | design-solution (`Security:` TB/THR), audit-trace |
| `security/posture` | `docs/security/posture.md` | design-solution |
| `security/compliance` | `docs/security/compliance.md` | design-solution (`Security:` CMP), audit-trace |
| `ops/deployment` | `docs/ops/deployment.md` | cut-release (narrative only; commands in project.md) |
| `ops/reliability` | `docs/ops/reliability.md` | design-solution (`Reliability:` SLO), audit-trace |
| `ops/observability` | `docs/ops/observability.md` | root-cause (after red loop) |
| `ops/disaster-recovery` | `docs/ops/disaster-recovery.md` | root-cause (after red loop) |
| `ops/runbooks` | `docs/ops/runbooks.md` | root-cause (after red loop) |

**All 36 Hybrid 1A catalog rows are First-class** in the pack (remaining rows use existing
owner skills: vision, ARCH INDEX, roadmap, specs INDEX, ADR, agents, glossary, OOS, guidelines pointer).

### System IDs (docs-only)

| Family | Defined in | Cited from design.md |
|---|---|---|
| `TB-N`, `THR-N` | `docs/security/threat-model.md` | `Security:` line only |
| `CMP-N` | `docs/security/compliance.md` | `Security:` line only |
| `SLO-N` | `docs/ops/reliability.md` | `Reliability:` line only |
| `ARCH-N` | `docs/architecture/INDEX.md` | `Respects:` only |

`audit-trace` enforces referential integrity (E6–E10) when defining docs exist. No semantic
judgment; no uncited-live-ID warning; no app/test grep.

Author any of these with `/define-system-doc <entry-key>`. Vision and ARCH-N spine stay with `/define-project`.

### Guidelines migration

Canonical engineering rules live under **`docs/standards/`**. `docs/product/guidelines.md`
is a **pointer only** after migration (legacy fallback only while unmigrated content
remains). Never keep parallel SSOTs.

## Codebase Map + navigation + plan-tasks

When a codebase doc is **Approved** (Status + structural validator pass), named
readers consult it under **hard constraints** (approved requirements/design, ARCH-N,
standing project constraints). On conflict: surface it, keep the hard constraint,
suggest `/define-system-doc <entry-key>` — never auto-invoke (ARCH-5). Absent doc:
no-op; optional one suggestion per entry key per skill run when the gap is material.

`design-solution` consults modules/dependencies when designing cross-module structure.
`inspect-change` may surface advisory findings when a diff conflicts with Approved nav docs.

## Guides vs catalog

This page explains. Maturity and inventory live only in `CATALOG.md`. Architecture
`artifacts.md` links here; it does not restate catalog rows.

## Related skills

- `/define-project` — vision, architecture spine, guidelines
- `/define-system-doc` — one Hybrid 1A artifact at a time
- `plan-tasks` — File Structure + Codebase Map consult
