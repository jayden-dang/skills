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

Author any of these with `/define-system-doc <entry-key>`.

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
