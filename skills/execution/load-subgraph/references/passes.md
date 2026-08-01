# load-subgraph passes (shipped SSOT)

Deterministic recipes. Run against the consumer **repo root**. Two agents on the
same tree with the same query MUST produce the same edge set and seed set
(finding-set identity, not wording).

**Constants (immutable for v1):**

| Name | Value |
|---|---|
| `NEIGHBORS_MAX` | `12` |
| `P0_SEED_MAX` | `12` |
| Line-suffix strip | trailing `:[0-9]+([,-][0-9]+)*` on the path token only |

**Stop-list — basenames (exact):**  
`package.json` `Cargo.toml` `go.mod` `pyproject.toml` `Gemfile` `composer.json`  
`Package.swift` `package-lock.json` `yarn.lock` `pnpm-lock.yaml` `Cargo.lock`  
`poetry.lock` `Gemfile.lock` `composer.lock`

**Stop-list — single path segment only (exact, whole token):**  
`src` `lib` `app` `apps` `packages` `services` `crates` `cmd` `internal`  
`vendor` `node_modules` `dist` `build` `target` `out` `skills` `templates`  
`hooks` `scripts` `docs`

---

## Pass R — Registry

1. Read `docs/specs/INDEX.md` if present; else empty registry, stop after reporting
   no specs.
2. Each table row matching:
   `\| CODE \| … \| ./path/ \| Status \| ROAD-or-— \|`
   where `CODE` is `[A-Z][A-Z0-9]{1,11}` length 2–12.
3. Spec dir = path relative to `docs/specs/` (strip `./` and trailing `/`).
4. For each CODE, if `requirements.md` has `Feature code: X`, prefer INDEX CODE
   for membership; note mismatch in envelope `notes` — never key by directory slug.

---

## Pass P1 — OWNS

For each registered CODE with `tasks.md`:

1. Split on `**Files:**` or a line that is only `Files:`; take the block until
   the next `### ` heading (or EOF).
2. Extract paths:
   - Lines matching  
     `^\s*[-*]\s*(Create|Modify|Move|Test)\s*:\s*`?([^`\n#]+)`?`  
     → path = group 2, trim, drop `#` comments.
   - Other path-like tokens in the block matching  
     `` `?[A-Za-z0-9_./@+-]+(\.[A-Za-z0-9]+)?`? ``  
     that contain `/` or a file extension.
3. For each token, strip backticks, then apply line-suffix strip (constant above).
4. OWNS(CODE) = set of remaining path strings. Missing tasks.md / missing Files
   block → empty set (do not invent paths).

---

## Pass D — Denoise

For a path set S, keep only tokens where:

1. basename (last segment) ∉ stop-list basenames, and  
2. token is **not** a single segment in the single-segment stop-list.

**No ancestor expansion.** Equality is exact string match after denoise.  
Directory ownership: a token counts as a directory only if it ends with `/` or
has no `.` in the last segment **and** was listed as a full Files entry — never
imply children from a parent path.

`meaningful(S) = denoise(S)`.

---

## Pass P2 — OVERLAPS

For each unordered pair of distinct CODEs:

- weight = `|meaningful(OWNS_a) ∩ meaningful(OWNS_b)|`
- if weight > 0, emit undirected edge with that weight
- stop-list-only intersection ⇒ weight 0 ⇒ no edge

---

## Pass P0 — TERMS (only when caller supplies terms)

1. Filter terms: trim; drop length < 3.
2. For each CODE, read available `requirements.md`, `design.md`, `tasks.md` under
   its spec dir (skip missing). Concatenate text; casefold to lower.
3. For each term, casefold; count substring occurrences in that text.
4. `distinct` = number of terms with count > 0; `hits` = sum of counts.  
   If distinct = 0, CODE is not a seed.
5. score = `distinct * 1000 + hits`.
6. Sort seeds by score desc, then CODE asc.  
   `matched` = full count; keep first `P0_SEED_MAX`;  
   `truncated = matched > P0_SEED_MAX`.

---

## Pass P3 — IMPLEMENTS

From INDEX Roadmap-item cell: if it matches `ROAD-\d+` once, edge CODE → ROAD-N.  
Empty, `—`, or missing → no edge (not an error).

---

## Pass P4 — CONTAINS (only if `docs/roadmap/INDEX.md` exists)

1. For each `## MILE-N` section, collect `ROAD-\d+` under Members.  
2. Goals: lines with `Goals:` → collect `GOAL-\d+` as GOAL → MILE.  
3. Absent file → no-op (empty).

---

## Pass P5 — RESPECTS (only if `docs/architecture/` exists)

In each `docs/specs/**/design.md`, lines containing `Respects:`: extract
`ARCH-\d+`. Absent architecture dir → no-op. Display-only; does not change
`audit-trace`.

---

## Query: neighbors(CODE[, terms])

1. Path candidates = other CODEs with P2 weight > 0; `path_weight` = weight.  
2. If terms given, term candidates = P0 seed CODEs minus focus.  
3. **Union** path ∪ term candidates **before** any cut.  
4. For each candidate:  
   - `via` = both | path | term  
   - sort key = `(path_weight desc, via_rank desc, CODE asc)`  
     where both=2, path=1, term=0  
5. **Truncate once** to `NEIGHBORS_MAX`. Never append after truncate.

---

## Query: ancestors / descendants / blast_radius / subgraph

- **ancestors(CODE):** CODE, then IMPLEMENTS ROAD if any, then MILE containing that
  ROAD, then GOALs of that MILE; if no roadmap layer → `[CODE]` only.
- **descendants(MILE-N):** member ROADs + CODEs with IMPLEMENTS into those ROADs.
- **blast_radius(path):** strip line-suffix; CODEs whose OWNS contain exact path,
  or directory-token ownership (dir token only) where path is under that dir;
  never expand arbitrary ancestors.
- **subgraph(seeds):** resolve terms→P0, paths→OWNS owners, codes as-is; expand
  one hop via OVERLAPS; bound node list to `NEIGHBORS_MAX * 3` (seeds first, then
  CODE asc).

---

## Envelope (every query)

Always set:

- `advisory: true`
- `owns_coverage: { with_owns, registered, ratio }` where  
  `with_owns` = count of CODEs with non-empty OWNS,  
  `registered` = registry size
- `p0: { matched, returned, truncated }` when P0 ran; else zeros
- never a `depends_on` / `DEPENDS_ON` field
- never write any file under `docs/` for the graph
