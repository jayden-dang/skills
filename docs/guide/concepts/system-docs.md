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

First First-class entry: **`codebase/map`** → consumer path `docs/codebase/map.md`.

## Codebase Map + plan-tasks

When `docs/codebase/map.md` is **Approved** (Status + structural validator pass),
`plan-tasks` consults it while writing File Structure.

**Hard constraints outrank the map:** approved requirements/design, ARCH-N, standing
project constraints. On conflict: surface it, keep the hard constraint, suggest
`/define-system-doc codebase/map` — never auto-invoke (ARCH-5). Absent map: no-op;
optional one suggestion per run when placement is uncertain.

## Guides vs catalog

This page explains. Maturity and inventory live only in `CATALOG.md`. Architecture
`artifacts.md` links here; it does not restate catalog rows.

## Related skills

- `/define-project` — vision, architecture spine, guidelines
- `/define-system-doc` — one Hybrid 1A artifact at a time
- `plan-tasks` — File Structure + Codebase Map consult
