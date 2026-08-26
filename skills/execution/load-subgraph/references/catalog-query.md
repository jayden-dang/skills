# Catalog query (one home)

Query-first capability catalog for agent **context** selection. Deterministic
registry snapshots (`passes.md` Pass R) may still enumerate every CODE on disk;
**chat/context must not**. Callers that need selected cards point here — do not
restate the caps or grammars elsewhere.

## Contents

- [Modes](#modes)
- [Card grammars](#card-grammars)
- [Context caps](#context-caps)
- [Query recipe](#query-recipe)
- [Exact CODE lookup](#exact-code-lookup)
- [Forbidden](#forbidden)

## Modes

Detect from `docs/specs/INDEX.md` (tracked or local overlay):

| Mode | When |
|---|---|
| **flat** | Feature table with `| Code | … | Spec | Status | … |` rows (bootstrap default) |
| **sharded** | Domain router table with `| Domain | Scope | Surface roots | Feature catalog |` and shard paths under `docs/specs/catalog/` |

Flat stays valid forever for small repos. Sharded is optional scale-out — no
consuming-repo migration is required by this pack. Infer mode from the file;
do not invent a tracked automation config.

## Card grammars

**Domain router row (sharded INDEX):** Domain id, one-line scope, 1–3 surface
roots, path to feature shard (`./catalog/<domain>.md`).

**Recognized feature card (flat INDEX row or shard row):**

| Field | Rule |
|---|---|
| Code | Immutable `[A-Z][A-Z0-9]{1,11}` length 2–12 |
| Maturity / Status | Catalog lifecycle or requirements Status — do not invent a third status system in prose |
| Capability | One sentence |
| Match terms | Bounded nouns/verbs; not full Files lists |
| Surface roots | 1–3 stable ownership prefixes |
| Spec | Relative pointer to triad dir (may be empty for Recognized-without-triad until a later slice) |

**Observed card** (local `.skills/reverse-features/active/*.md`): same compact
shape with `OBS-<6hex>`, state, confidence, evidence pointer — see
`reconcile-features` passes. Merge into the same result set as Recognized when
querying; never treat OBS as a Feature CODE.

## Context caps

Pack constants for **agent context selection** (not for Pass R disk enumeration):

| Name | Value |
|---|---|
| `DOMAINS_MAX` | `2` |
| `DIRECT_CARDS_MAX` | `4` |
| `NEIGHBOR_CARDS_MAX` | `2` |

`load-subgraph` envelope caps (`NEIGHBORS_MAX` = 12, etc.) stay in `passes.md`.
Do not raise context caps to match the envelope.

## Query recipe

1. Extract intent **terms** + candidate **paths** from the ask / scan / diff.
2. If sharded: score domain rows by surface-root path match first, then terms;
   keep ≤ `DOMAINS_MAX` domain cards. If flat: treat INDEX as one logical domain.
3. Query Recognized rows (flat table or selected shards) **and** active OBS
   overlay for those domains. Rank: exact/ancestor surface-root hits first, then
   term hits. Drop generic path stopwords (`apps`, `src`, `internal`, … — same
   spirit as load-subgraph / reconcile stop-lists).
4. Keep ≤ `DIRECT_CARDS_MAX` direct cards (Recognized + OBS) and ≤
   `NEIGHBOR_CARDS_MAX` one-hop neighbors if already known from a prior
   load-subgraph package; otherwise leave neighbors to `load-subgraph`.
5. Present two bands: **Recognized features** and **Observed candidates**.
6. Open `requirements.md` / `tasks.md` / OBS evidence **only** for selected cards.
7. Absence claims must carry catalog mode + `owns_coverage` when a subgraph
   package exists (grounded-claims.md).

## Exact CODE lookup

Resolve a known CODE with fixed search — do not load the whole catalog into
context:

```bash
# flat or shard files
rg -n '^\\| <CODE> \\|' docs/specs/INDEX.md docs/specs/catalog -g '*.md'
```

## Forbidden

- Claiming INDEX is “small” as a reason to dump every row into context
- Pasting the full feature table into knowns, scan digests, or step-1 chat
- Treating OBS ids as Feature CODEs
- Writing `docs/specs/GRAPH.md` or a second catalog SSOT
- Requiring consuming repos to shard
