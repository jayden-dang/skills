# Design: Feature Homing Refinement & Facets

Feature code: MODHOME
Status: Implemented
Date: 2026-07-11
Requirements: ./requirements.md

## Context

M2 (MODGRAPH) homes a feature by calling `_home_module(sorted(owns), modules)`
(`check_graph.py:161`, invoked at `:502`), which returns a single module code
only when every owned path resolves to exactly one module and those all agree —
and `None` for every other case: empty owns, an orphan path, a double-mapped
path, or paths spanning two or more modules. That `None` is lossy: the graph
cannot tell "this feature straddles AUTH and BILL, someone should split it" from
"this feature simply has no owned files yet." M3 recovers that lost information
and puts it to work, without changing where homing happens: it stays inside
`harvest`, the one place with the **uncapped** `owns`/`touches` lists, the loaded
`modules`, and the feature's `requirements.md` text all in scope at once
(`check_graph.py:454-504`; owns/touches are capped later, at `:536-541`).

Three facts shape the approach. First, `harvest` is the only producer of
per-feature derived state and `_run_verify` must format the split-signal and
invalid-override warnings **without re-walking specs** — so the diagnostics have
to be computed once in `harvest` and carried on the feature dict, with
`_run_verify` a pure formatter of what it finds there. Second, `render_graph_md`
(`:545`) reads only `code/name/owns/touches/interfaces/oos` and `graph["shared"]`
— never `home` — so any additive field (`facets`, homing diagnostics) leaves the
flat `GRAPH.md` byte-identical, and only the sharded `render_all` path
(`:580`, manifest mode) needs to change. Third, the whole feature is manifest-
gated already: `render_all`'s flat branch fires on `errs or not modules`
(`:585-586`), so when no valid manifest exists none of M3's derivation must have
any observable effect (MODHOME-4.1).

The overriding constraint, inherited from M1/M2: everything M3 adds is
**advisory** — the split signal and the invalid-override notice are `--verify`
*warnings* that never change the exit code — while M1's manifest-validity and
boundary errors stay errors.

## Decisions

1. **One richer classifier, `_home_feature`, subsumes homing.** A pure helper
   `_home_feature(owned_paths, touched_paths, override_code, module_codes,
   modules)` returns a record `{home, facets, spanned, unknown_override}`
   computed from a single `resolve_module` walk of the owned and touched paths.
   It is the sole home-derivation authority; the existing `_home_module(owned,
   modules)` is kept as a thin wrapper returning `_home_feature(owned, [], None,
   set(), modules)["home"]`, so its guard tests (`check_graph_test.py:563-575`,
   tagged MODGRAPH-1.2/1.3) keep pinning the same behavior through one
   implementation. Rejected: a separate `_spanned_modules` helper that
   `_run_verify` calls — verify only has the **capped** `owns`, so it cannot
   recompute spanning; the data must be produced in `harvest`.
2. **Spanning is defined narrowly: every owned path resolves cleanly to exactly
   one module, and the set of those modules has size ≥ 2.** If any owned path is
   an orphan (resolves to 0 modules) or double-mapped (resolves to ≥ 2), the
   feature is *unresolved*, not spanning — `home None`, `spanned []`, no split
   warning — exactly as today. This matches MODHOME-1.1's "distinct from … an
   orphan owned path, or a double-mapped owned path": orphan/double-mapped
   presence takes a feature out of the spanning category rather than mixing the
   two signals.
3. **Homing diagnostics ride on the feature dict as additive keys.** `harvest`
   sets three new keys per feature: `facets` (a sorted list, consumed by
   `render_all`), and `homing` (a dict `{spanned: [...], unknown_override:
   code|None}`, consumed only by `_run_verify`). The existing `home` key keeps
   its meaning and its first-class place. Nothing does whole-dict equality on
   features, and `render_graph_md` ignores unknown keys, so the additions are
   invisible to flat mode.
4. **The `Module:` override is a header line, parsed like `Feature code:`.** A
   new module-level regex `_MODULE_OVERRIDE_RE = ^Module:\s*([A-Z][A-Z0-9]{1,11})`
   (MULTILINE) reads the feature's `requirements.md` text (in scope at
   `:464-465`), the same convention as `_FEATURE_CODE_RE`. `harvest` passes the
   captured code to `_home_feature` **only when a manifest is present**
   (`override_code = … if _manifest_modules else None`), so a stray `Module:`
   line in a repo with no manifest triggers no override processing (MODHOME-4.1).
5. **A valid override wins and silences the span; an invalid one is inert but
   noisy.** In `_home_feature`: if `override_code in module_codes`, `home =
   override_code` and `spanned = []` (the override *is* the "declare a home"
   answer — MODHOME-3.2); if `override_code` is set but unknown, `home` stays the
   derived value and `unknown_override = override_code` (MODHOME-3.3). Facets are
   always computed against the **final** home.
6. **The shard row gains a Facets column.** `render_all`'s `shard()` row becomes
   `| Feature | Name | Owns | Facets |`. This is a deliberate format change to
   the M2 shards; the MODGRAPH shard tests that assert the 3-column row are
   updated as part of this slice (called out in the plan), the same way M2
   updated the `--query` envelope tests.

No decision here is hard-to-reverse AND surprising AND a real trade-off, so no
ADR. `_home_feature` is a single-shape extension of an existing pure helper, not
a new boundary, so no parallel design exploration.

## Architecture

### `_home_feature` — the homing classifier

Satisfies: MODHOME-1.1, MODHOME-2.1, MODHOME-2.2, MODHOME-2.3, MODHOME-2.4, MODHOME-3.1, MODHOME-3.2, MODHOME-3.3, MODHOME-4.2

Pure function, no I/O:

```
_home_feature(owned_paths, touched_paths, override_code, module_codes, modules)
  -> {"home": code|None, "facets": [code…], "spanned": [code…],
      "unknown_override": code|None}
```

- **Derive from owned** (MODHOME-1.1): resolve each owned path; if any resolves
  to ≠ 1 module, the feature is unresolved → `derived_home None`, `spanned []`.
  Otherwise let `uniq = sorted(set(single resolutions))`: size 1 → `derived_home
  = uniq[0]`; size ≥ 2 → `spanned = uniq` (`derived_home None`).
- **Apply override** (MODHOME-3.1, 3.2, 3.3): start `home = derived_home`. If
  `override_code` is set and in `module_codes` → `home = override_code`,
  `spanned = []`. If set and not in `module_codes` → `unknown_override =
  override_code` (home unchanged). If unset → derived stands.
- **Derive facets** (MODHOME-2.1–2.4): only when `home is not None`, collect the
  sole resolution of each touched path that resolves to exactly one module and
  differs from `home`; `facets = sorted(set(...))`. A touched path resolving to 0
  or ≥ 2 modules contributes nothing (2.4); `home` is excluded (2.2); the set +
  sort make it deterministic (2.3). When `home is None`, `facets = []`.

`_home_module(owned, modules)` becomes `return _home_feature(owned, [], None,
set(), modules)["home"]` (MODHOME-4.2: the same-single-module home is unchanged).

### `harvest` — parse the override, carry the diagnostics

Satisfies: MODHOME-3.1, MODHOME-4.1, MODHOME-4.4

`harvest` already loads `_manifest_modules` (`:459-461`) and reads each feature's
`text` (`:464`). It computes once `_module_codes = {m["code"] for m in
_manifest_modules if m.get("code")}`; per feature, `override_code =
_MODULE_OVERRIDE_RE.search(text).group(1) if a match and _manifest_modules else
None`. It calls `_home_feature(sorted(owns), sorted(touches), override_code,
_module_codes, _manifest_modules)` and stores on the feature dict:
`home = rec["home"]`, `facets = rec["facets"]`, `homing = {"spanned":
rec["spanned"], "unknown_override": rec["unknown_override"]}`. `facets` is a
small list of module codes (bounded by the module count), so the `:536-541` card
cap does not touch it. With no manifest, `_manifest_modules == []` →
`override_code None`, and every path resolves against `[]` to `[]` → every
feature gets `home None, facets [], spanned [], unknown_override None`
(MODHOME-4.1). Existing card fields are untouched; the three additions are purely
additive (MODHOME-4.4).

### `render_all` — facets in the shard row; spanning to `(unassigned)`

Satisfies: MODHOME-1.4, MODHOME-2.5, MODHOME-4.1

Flat mode (no manifest) is unchanged: `{"GRAPH.md": render_graph_md(graph)}`,
byte-identical (MODHOME-4.1). In manifest mode, `shard()`'s header becomes
`| Feature | Name | Owns | Facets |` and each row appends `', '.join(f.get
("facets") or []) or '—'` (MODHOME-2.5). Grouping is unchanged: a spanning
feature has `home None`, so `by_module[None]` places it in
`modules/_unassigned.md` — no feature dropped (MODHOME-1.4). The index
(`GRAPH.md`) and its cross-module shared-surface table are unchanged.

### `_run_verify` — split-signal and invalid-override warnings

Satisfies: MODHOME-1.2, MODHOME-1.3, MODHOME-3.3, MODHOME-3.4, MODHOME-4.3

Inside the existing `elif modules:` branch (only when a valid manifest is
present, `:841-844`), after the boundary check, iterate `graph["features"]` and
append to the existing `warnings` list:

- if `f["homing"]["spanned"]` is non-empty → `W: feature <code> owns files
  spanning modules <a, b> — split it per module or declare a home with a
  `Module:` header line` (MODHOME-1.2);
- if `f["homing"]["unknown_override"]` → `W: feature <code> declares
  Module: <code> which is not a known module — override ignored` (MODHOME-3.3).

Because these use the `warnings` channel, they are printed and included in
`--json` but never affect the `1 if errors else 0` exit code (MODHOME-1.3, 3.4).
The manifest-validity and boundary **error** paths (`:838-844`) are untouched
(MODHOME-4.3). Gating on `elif modules:` means no warnings in flat mode
(MODHOME-4.1).

### Import inertness (infrastructure)

Satisfies: MODHOME-4.5

`_home_feature` and `_MODULE_OVERRIDE_RE` are a `def` and a module-level
constant; nothing new runs at import (MODHOME-4.5).

## Seams for testing

One new unit seam (`_home_feature`); everything else reuses M2's seams.

| Seam | Kind | Covers |
|---|---|---|
| `_home_feature(owned, touched, override, module_codes, modules)` | unit | MODHOME-1.1, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 4.2 |
| `harvest(specs_dir, cfg)` over a spec fixture (override parse, additive fields, no-manifest degradation) | integration | MODHOME-3.1, 4.1, 4.4 |
| `render_all(graph, cfg)` (shard facets column; spanning → `_unassigned`) | unit | MODHOME-1.4, 2.5, 4.1 |
| `--verify` via `main` (split + invalid-override warnings, advisory) | integration | MODHOME-1.2, 1.3, 3.3, 3.4, 4.3 |
| import-inertness reload check | unit | MODHOME-4.5 |

## Coverage check

All 18 requirement IDs are covered by a Satisfies line. Most map to exactly one
section; three (3.1, 3.3, 4.1) are cross-cutting and are named on both
contributing sections, because the behavior genuinely spans two seams:

- Story 1 — 1.1 → `_home_feature`; 1.2, 1.3 → `_run_verify`; 1.4 → `render_all`.
- Story 2 — 2.1, 2.2, 2.3, 2.4 → `_home_feature`; 2.5 → `render_all`.
- Story 3 — 3.1 → `_home_feature` (applies override) + `harvest` (parses the
  header line); 3.2 → `_home_feature`; 3.3 → `_home_feature` (detects unknown) +
  `_run_verify` (warns); 3.4 → `_run_verify`.
- Story 4 — 4.1 → `harvest` (degradation) + `render_all` (flat branch); 4.2 →
  `_home_feature`; 4.3 → `_run_verify`; 4.4 → `harvest`; 4.5 → import inertness.

No IDs are deliberately unmapped.
