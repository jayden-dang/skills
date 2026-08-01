# load-subgraph passes (shipped SSOT)

Agents execute these recipes with grep/file reads and set operations.
Constants MUST match the test-side reference (`tests/feature-subgraph/reference_derive.py`).

## Constants

- `NEIGHBORS_MAX = 12`
- `P0_SEED_MAX = 12`
- Line-suffix strip: trailing `:[0-9]+([,-][0-9]+)*` on the last path segment
- P0 score = `(distinct_seed_terms_matched × 1000) + raw_casefold_hits`; ties by CODE ascending
- Manifest/lock basenames: package.json, Cargo.toml, go.mod, pyproject.toml, Gemfile, composer.json, Package.swift, package-lock.json, yarn.lock, pnpm-lock.yaml, Cargo.lock, poetry.lock, Gemfile.lock, composer.lock
- Workspace single-segment stop: src, lib, app, apps, packages, services, crates, cmd, internal, vendor, node_modules, dist, build, target, out, skills, templates, hooks, scripts, docs

## P0 TERMS

Match caller key terms (length ≥ 3) case-insensitively as substrings in each feature's requirements.md, design.md, tasks.md. Rank by score; keep top P0_SEED_MAX; set truncated if more matched.

## P1 OWNS

From each feature's tasks.md `**Files:**` blocks: Create/Modify/Move/Test bullets and prose path tokens; strip line suffixes; associate with CODE from INDEX / Feature code: line. Never key by directory slug when CODE exists. Empty if no tasks/Files.

## Denoise

Drop manifest/lock basenames and single-segment workspace roots. No ancestor expansion. Exact token equality only (or explicit directory ownership token alone).

## P2 OVERLAPS

Undirected edge when denoised OWNS intersection non-empty; weight = intersection cardinality.

## P3 IMPLEMENTS

INDEX Roadmap item cell → live ROAD-N; empty/— skip.

## P4 CONTAINS

Roadmap MILE members ROAD-N; Goals: GOAL-N → MILE. Absent roadmap → no-op.

## P5 RESPECTS

design.md `Respects: ARCH-N` when docs/architecture/ exists; else no-op. Display only; does not change audit-trace.

## neighbors merge

1. Path candidates: positive OVERLAPS weight
2. Term candidates: P0 seeds when terms supplied
3. Union **before** truncate
4. Sort (path_weight desc, via both>path>term, CODE asc)
5. Truncate once to NEIGHBORS_MAX

## Queries

- `neighbors(CODE)` — merge rule above
- `ancestors(CODE)` — CODE → ROAD → MILE → GOAL; bare CODE if no roadmap
- `descendants(MILE-N)` — member ROADs and implementing CODEs
- `blast_radius(path)` — exact OWNS or directory ownership prefix only
- `subgraph(seed)` — resolve terms/paths/codes; 1-hop OVERLAPS; bound nodes to NEIGHBORS_MAX×3

## Forbidden

- Write GRAPH.md or any committed graph projection
- Derive runtime DEPENDS_ON feature edges
- Import test-side reference_derive into the skill
