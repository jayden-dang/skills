---
name: map-features
description: Use when a brownfield repo needs feature-code, ROAD binding, OWNS,
  or DEPENDS_ON candidate backfill for the skill set — propose then confirm;
  never auto-write graph edges. Run with /map-features.
disable-model-invocation: true
---

# Map Features (brownfield backfill)

User-invoked wizard. Sibling of `configure-repo` / `scan-architecture`:
**propose → human confirm → additive SSOT write**. Never materialize a graph file.

Model-invoked skills that detect brownfield mapping gaps MUST **name**
`/map-features` for the user and MUST NOT auto-invoke this skill (ARCH-5).

## Procedure

1. Scan `docs/specs/`, INDEX, roadmap (if present), and optional codebase paths.
2. Build proposals (do not write yet):

   | Kind | Source | On confirm write |
   |---|---|---|
   | Missing `Feature code:` | requirements without line | requirements.md header |
   | Empty ROAD bind | INDEX `—`/empty + live ROAD-N | INDEX cell only — never invent ROAD-N |
   | OWNS gap | significant paths not in any feature's denoised OWNS | prefer suggesting plan-tasks Files edit |
   | DEPENDS_ON candidate | `Reuse:` / `Interfaces: Consumes` cross-feature names | design/tasks prose only — **never** load-subgraph edges |

3. Present proposals. Write **only** what the user explicitly confirms.
4. MUST NOT auto-write DEPENDS_ON candidates. Unconfirmed candidates MUST NOT
   appear as edges when `load-subgraph` runs.
5. If a feature CODE cannot be resolved from INDEX or `Feature code:`, report it
   as a first-class backfill item. MUST NOT silently key by directory slug.
6. MUST NOT write `docs/specs/GRAPH.md` or any graph projection.

## Done when

Confirmed items are written additively; declined items left untouched; user has
the list of remaining gaps.
