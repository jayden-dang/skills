# Design: Sharded Module Graph

Feature code: MODGRAPH
Status: Approved
Date: 2026-07-11
Requirements: ./requirements.md

## Context

M2 reorganizes the feature graph around M1's modules so it never renders as one
unbounded file and the query stops collapsing to alphabetical order on hub
files. Everything lives in `scripts/check_graph.py`, extending four existing
seams: `harvest(specs_dir, cfg)` → `{features, reverse, shared}`;
`render_graph_md(graph)` → the single flat `GRAPH.md` string;
`query(graph, paths, keywords)` → results ranked by `(-len(overlapPaths), code)`;
and `_run_verify(root, cfg, specs_dir, as_json)`. The module stays stdlib-only
and import-inert.

Two current-code facts shape the design. First, `harvest` **caps** each returned
feature's `owns` at `cardCap` (12) with a `"…(+N more)"` sentinel
(`check_graph.py:507-512`) — so homing cannot use the returned `owns`; it must
run on the uncapped list that exists only transiently inside `harvest` before
that pass. Second, `render_graph_md` is pure (graph → one string) and the CLI
writes it; M2 needs to emit *many* files (an index plus per-module shards) and
`--verify` needs to check that same set, so the render must produce a
file-set, not a single string, and one renderer must feed both write and verify
or they will drift.

The overriding constraint is graceful degradation, established by M1: a repo
with no valid manifest must render and verify exactly today's flat `GRAPH.md`,
write no shard files, and keep M1's boundary + registration checks running.

## Decisions

1. **Home features inside `harvest`, before the cap pass.** `harvest` calls
   `load_manifest(cfg)`; when a valid manifest exists it computes each feature's
   home from its **uncapped** owned list (available at `check_graph.py:458-461`)
   and stores `f["home"]` (a module code or `None`). No manifest / invalid
   manifest → `home` stays `None` for every feature (flat mode). This is the
   only place the full owned set is in scope, so homing belongs here; exposing an
   extra uncapped field on every feature just to home it elsewhere would be
   wasted surface.
2. **One pure renderer: `render_all(graph, cfg) → {relpath: content}`.** Keyed by
   specsDir-relative path. Flat mode (no homes) → `{"GRAPH.md": <today's flat
   string>}`, reusing `render_graph_md` verbatim so flat output is byte-identical
   to today. Manifest mode → `{"GRAPH.md": <index>, "modules/<CODE>.md": <shard>,
   …, "modules/_unassigned.md": <shard>}`. `--harvest` writes this dict and
   `--verify` compares against it, so they cannot drift. The dict interface hides
   all the flat-vs-sharded branching behind one call.
3. **The `(unassigned)` shard is `modules/_unassigned.md`.** A leading underscore
   cannot be a valid module code (`^[A-Z]…`), so it can never collide with a real
   shard filename.
4. **IDF ranking in `query`, cap/truncate at the `--query` CLI boundary.**
   `query` scores each result as `sum(1/df(p) for p in overlapPaths)` where
   `df(p) = len(reverse[p])` (already computed), orders by score desc then code,
   and returns the **complete** ranked list with a `score` field — pure and fully
   testable, and reusable by M3/M6. The top-N cap, omitted-count, and
   out-of-scope first-sentence truncation are presentation concerns applied in
   the `--query` CLI path, which emits `{"results": […], "omitted": N}`.
5. **`queryCap` is a new `graph` config key (default 8),** merged by the existing
   `load_config` deep-merge, overridable in `trace.json` like `cardCap`.
6. **`--harvest` prunes.** After writing `render_all`'s files it deletes any
   `modules/*.md` not in the rendered set, so removing a module — or the whole
   manifest — leaves no stale shard and keeps `--verify`'s set-equality honest.

No decision here is hard-to-reverse AND surprising AND a real trade-off, so no
ADR. `render_all` replacing a one-file render is notable but is exactly what the
approved requirements call for, and it is internal and test-covered.

## Architecture

### Feature homing in `harvest`

Satisfies: MODGRAPH-1.1, MODGRAPH-1.2, MODGRAPH-1.3

A helper `_home_module(owned_paths, modules) → code|None`: resolve every owned
path via `resolve_module`; if any path yields a list whose length ≠ 1 (orphan or
double-mapped), return `None`; collect the single code from each path; return it
iff all paths agree on one module, else `None`. `harvest` computes
`modules, errs = load_manifest(cfg)`; treats `errs` as no-manifest
(`modules = []`); and sets `f["home"] = _home_module(uncapped_owns, modules)`
(or `None` when `modules` is empty) on each feature **before** the `cap_list`
pass. Empty owned set → `None` (unassigned).

### `render_all` — flat, index, and shards

Satisfies: MODGRAPH-2.1, MODGRAPH-2.2, MODGRAPH-2.3, MODGRAPH-2.4, MODGRAPH-2.5, MODGRAPH-2.7, MODGRAPH-4.2

`render_all(graph, cfg) → dict[str, str]`. If no feature has a `home`
(flat/degraded mode) → `{"GRAPH.md": render_graph_md(graph)}` unchanged (4.2).
Otherwise:

- **`GRAPH.md` = the index:** the generated banner (2.7), a `## Modules` list —
  one line per module with ≥1 homed feature plus the `(unassigned)` bucket, each
  `CODE — Name (N features) → modules/<file>.md`, sorted by code — and a
  `## Cross-module shared surface` table listing each path in `graph["reverse"]`
  whose referencing features span **two or more distinct home modules**, naming
  those modules sorted (2.1, 2.2).
- **`modules/<CODE>.md` per module** with ≥1 homed feature: banner + a compact
  table, one **row** per homed feature (`| CODE | Name | owns-summary |`), not a
  full card, features sorted by code (2.3).
- **`modules/_unassigned.md`** when any feature has `home is None`, same row
  format, so no feature is dropped (2.4).

Every list is sorted (modules, features, paths) so re-render is byte-identical
(2.5). `render_all` is pure — it returns content, writes nothing.

### `--harvest`: write, then prune

Satisfies: MODGRAPH-2.6

The `--harvest` path computes `files = render_all(graph, cfg)`, writes each
`specs_dir/<relpath>` (creating `modules/` as needed), then enumerates existing
`specs_dir/modules/*.md` and deletes any whose relpath is not a key of `files`
(2.6) — this also cleans up when a manifest is removed (flat `files` has no
`modules/` entries). The printed summary is unchanged.

### `query`: IDF ranking

Satisfies: MODGRAPH-3.1, MODGRAPH-3.2, MODGRAPH-4.5

Replace the sort key. For each scored result, `score = sum(1.0 / len(reverse[p])
for p in overlapPaths)` (3.1). Sort by `(-score, code)` (3.2), so a path shared
by many features barely moves the ranking while a rarely-shared path dominates —
and identical-hub-only candidates no longer collapse to alphabetical. Each
result keeps `code`, `name`, `card`, `overlapPaths` and gains `score` (4.5:
existing fields preserved; `score` is additive).

### `--query`: cap, omitted count, out-of-scope truncation

Satisfies: MODGRAPH-3.3, MODGRAPH-3.4, MODGRAPH-3.5

The `--query` CLI takes the full ranked list, keeps the first `cfg["graph"]
["queryCap"]` results (3.3), and emits — in **JSON mode** — `{"results": [...],
"omitted": max(0, total - cap)}` (3.4); in **text mode**, the capped
`CODE (n)` lines followed by a `(+N more omitted)` trailer when `omitted > 0`.
Before emitting, each kept card's `oos` entries are passed through
`_first_sentence(s)` — text up to and including the first sentence terminator,
else the whole string (3.5). A helper `_first_sentence` is the tested unit.

**Output-shape compatibility.** Wrapping the JSON list in a `{results, omitted}`
envelope is a deliberate contract change. Three existing `--query` CLI tests
assert the bare list (`check_graph_test.py` lines 765, 793, 839) and MUST be updated to
the envelope as part of this slice — the plan carries that as explicit task
steps. The skills that *consume* `--query` (`brainstorm`, `code-review`) read the
output as an agent, not as parsed code, so they degrade gracefully in the window
before **M6** re-wires their documented shape; M6 owns that doc sync. No other
code parses the `--query` output.

### `--verify`: shard-set + content equality

Satisfies: MODGRAPH-4.1, MODGRAPH-4.3, MODGRAPH-4.4

Replace the single-`GRAPH.md` freshness check with: `files = render_all(graph,
cfg)`; for each `(relpath, content)` compare the committed
`specs_dir/<relpath>` — missing or differing → an error naming the file; then
enumerate committed `specs_dir/modules/*.md` and flag any not in `files` as a
stale shard (4.1). In flat mode `files == {"GRAPH.md": …}`, so this reduces to
today's behavior. The existing registration check (4.4) and M1's
`_verify_boundaries` call (4.3) are untouched and still run.

### Import inertness (infrastructure)

Satisfies: MODGRAPH-4.6

All new symbols are `def`s or module-level constants (a `queryCap` default in
`DEFAULTS["graph"]`); nothing runs at import (4.6).

## Seams for testing

New pure functions are tested inside the existing `check_graph_test.py`
module-unit surface; CLI behaviors via `main([...])` over a `_tmp_repo` fixture,
exactly as M1's tests do — no new public seam beyond these functions.

| Seam | Kind | Covers |
|---|---|---|
| `_home_module(owned_paths, modules)` | unit | MODGRAPH-1.1, 1.2, 1.3 |
| `render_all(graph, cfg)` over a harvested graph | unit | MODGRAPH-2.1, 2.2, 2.3, 2.4, 2.5, 2.7, 4.2 |
| `--harvest` via `main` over a tmp repo (write + prune) | integration | MODGRAPH-2.6 |
| `query(graph, paths, keywords)` | unit | MODGRAPH-3.1, 3.2, 4.5 |
| `--query` via `main` (cap/omitted/oos) | integration | MODGRAPH-3.3, 3.4, 3.5 |
| `--verify` via `main` (shard set + content, degrade) | integration | MODGRAPH-4.1, 4.3, 4.4 |
| import-inertness reload check | unit | MODGRAPH-4.6 |

## Coverage check

All 21 requirement IDs map to exactly one Satisfies line:

- Story 1 — 1.1, 1.2, 1.3 → Feature homing in `harvest`.
- Story 2 — 2.1, 2.2, 2.3, 2.4, 2.5, 2.7 → `render_all`; 2.6 → `--harvest` prune.
- Story 3 — 3.1, 3.2 → `query`; 3.3, 3.4, 3.5 → `--query` CLI.
- Story 4 — 4.1, 4.3, 4.4 → `--verify`; 4.2 → `render_all` (flat branch); 4.5 →
  `query` (fields preserved); 4.6 → import inertness.

No IDs are deliberately unmapped.
