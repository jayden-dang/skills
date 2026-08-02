# Design: Feature-subgraph retrieval upgrade (Wave A)

Feature code: FSUBR
Status: Implemented
Date: 2026-08-02
Approved: 2026-08-02 (user)
Requirements: ./requirements.md

## Context

FSUB already ships ask-time feature-subgraph derivation: `load-subgraph` with
`passes.md` recipes, `envelope.md` shape, a pack-only `reference_derive.py`
oracle, and required callers `frame-change` / `inspect-change`. Neighbor rows
expose `shared_paths` as an **integer** count and `via` only — not concrete
paths or typed traces. P1 OWNS extraction uses first-Files-only parse and a
naive body cut at `\n### `, so Step/unittest prose after the first Files block
pollutes OWNS with code-shaped tokens and drops later-task paths. Live diagnosis
showed mega-components driven by that pollution; a cleaned-graph spike showed
query-local stars stay bounded while global partitions do not.

**Binding constraint:** keep derivation **deterministic** and **markdown-only**
for consumers (ARCH-1, ARCH-3): evolve `passes.md` / `envelope.md` / skill prose
and the test oracle in place — Approach A — not a parallel skill, graph DB, or
LLM extraction pipeline. The rejected alternative is dual-schema forever or
`load-subgraph-v2`, which would fork ownership of the same Files surface.

**Spine reliance:** ARCH-1 (fixed set ops), ARCH-2 (optional layers no-op),
ARCH-3 (no Python under skills; no Neo4j mandate), ARCH-4 (IDs immutable —
FSUBR IDs Approved), ARCH-5 (user-invoked skills not auto-called). No ADR: no
invariant contradiction; P6 and work-graph remain Out of Scope for FSUBR.

## Decisions

1. **In-place delta (Approach A)** on `skills/execution/load-subgraph/**` +
   test oracle + listed caller skills; FSUB triad stays Implemented baseline.
2. **`schema_version: "1.1"`** on every neighbors and cluster payload; callers
   ignore unknown future `via_traces` kinds.
3. **P1 multi-block + fence-aware semantic stop**; **reject-unsafe-first**
   classifier with **provenance** (Architecture §1); decision table for fixtures.
4. **`cluster` requires exactly one focus CODE**; resolve terms/paths before invoke.
5. **Two-stage derivation snapshot** (in-memory only): Stage A core reads + OWNS;
   Stage B cluster-only OOS loads; queries perform **zero** file IO; fingerprints
   reuse Stage bytes.
6. **Frozen cluster / evidence constants** (rationale unchanged):
   - `CLUSTER_K = 1`, `CLUSTER_MEMBERS_MAX = 8`, focus first, weight↓ CODE↑
   - `PATH_EVIDENCE_MAX = 5`, `TERM_EVIDENCE_MAX = 5`
   - `OOS_ITEM_MAX = 6`, `OOS_TEXT_CEILING = 1200` display code points
   - Path order lex asc; term casefold dedupe; OOS key vs display text
7. **Coverage:** `owns_coverage` only.
8. **Package validity:** content fingerprints of every artifact actually read,
   including optional-layer **presence/absence sentinels**; rederive if any
   change or if fingerprints cannot be established; re-derive **reuses** prior
   bytes already in the package/session buffer when re-hashing is not enough —
   see §0 (no second FS read of the same path in one invocation).
9. **No on-disk session cache.** Notes: **no silent 32-cap** — all reliability
   notes for the query are retained (dedupe by kind+code+detail only).
10. **Grounded-claim protocol** on every retrieval caller.

### Rationale for frozen constants

**`CLUSTER_K = 1`.** After P1 tightening, weight is meaningful shared path
cardinality. A single shared file is often a true coupling. The cleaned-graph
spike showed global CC still mega-merges; **query-local** membership + **member
cap** bounds output. Post-P1 goldens: (a) exactly one shared path → eligible;
(b) high-degree focus → truncated returned set, `members_truncated` true.

**`CLUSTER_MEMBERS_MAX = 8` and OOS caps.** Context budget for frame/design/plan
beside Summary cards. Fixed integers, not adaptive.

## Architecture

### 0. Per-query derivation snapshot (in-memory)

Satisfies: FSUBR-10.1
Reuse: rung 7 — new in-process structure; pattern from FSUB “one pass then set ops”
Respects: ARCH-1, ARCH-2, ARCH-3
Interface: `build_snapshot(repo_root, query) → DerivationSnapshot`; queries are pure
  functions of the snapshot (no file IO); `snapshot.read_ledger` lists each path once
Depth: if vanished, callers rebuild: Stage A core load once; Stage B optional
  member OOS loads once; fingerprint from buffered bytes; queries pure on snapshot
Locality: extend `passes.md` procedure + `reference_derive.run`; leave skill free of Python

**Two-stage build (query-aware):**

| Stage | When | Reads (each path ≤1) |
|---|---|---|
| **A — Core** | every query | `docs/specs/INDEX.md`; each registered feature’s `tasks.md` (if present); for P0/neighbors terms: each feature’s `requirements.md`, `design.md`, `tasks.md` already buffered; optional `docs/roadmap/INDEX.md` and `docs/architecture/**` **presence check + content if present** for P3–P5 |
| **B — Cluster OOS** | only `query.kind == cluster` after eligible members computed **in memory** from Stage A OWNS | each **returned** member’s `requirements.md` if not already in `source_texts` |

Stage B **never** re-reads a path already in `source_texts`. Member eligibility and
caps are computed from Stage A only; OOS union uses Stage A+B texts.

**`DerivationSnapshot` fields:**

| Field | Content |
|---|---|
| `registry` | INDEX rows |
| `source_texts` | path → UTF-8 text (successful reads only) |
| `source_bytes` | path → raw bytes (same read; used for fingerprint + decode) |
| `owns` | CODE → `{ paths: set[str], notes: [Note] }` |
| `owns_coverage` | with_owns, registered |
| `p3_p4_p5` | edges or empty |
| `notes` | all non-fatal notes for this query (**no count cap**; dedupe kind+code+detail) |
| `fingerprints` | path → `{ sha256, present: bool }` for every path **considered** (see below) |
| `read_ledger` | ordered list of `{ path, op: "read"|"stat_absent" }` — each path at most once |
| `schema_version` / `recipe_id` | `"1.1"` / `"fsubr-1.1"` |

**Optional-layer fingerprints:** for roadmap INDEX and architecture INDEX (or dir
sentinel file design freezes as `docs/architecture/INDEX.md` if present else
stat of `docs/architecture/` via recording `present:false` for
`docs/roadmap/INDEX.md` and `docs/architecture/INDEX.md` when absent). If a layer
**appears** later, fingerprint set changes → package invalid → rederive.

**Read-once + re-derive:** Within one invocation, the filesystem adapter records
each path once in `read_ledger`. If package validation needs content hashes,
it hashes **`source_bytes` already held** or performs a single validation read
that **becomes** the Stage A buffer for that path if rederive continues — never
read-then-read-again for the same path.

**Queries (neighbors, cluster, blast_radius, …):** take only
`(snapshot, query_args)`; **zero** file IO.

**Note kinds:**

| kind | When |
|---|---|
| `p1_block_skipped` | Files block structural failure (§1) |
| `p1_file_unreadable` | existing tasks.md (or SSOT) **read or UTF-8 decode fails** |
| `cluster_focus_invalid` | focus zero/many / not registered |

**Missing `tasks.md`:** not an error — OWNS empty, **no** `p1_file_unreadable`
(baseline empty / FSUB no-op).

### 1. P1 OWNS tightening

Satisfies: FSUBR-2.1, FSUBR-2.2, FSUBR-2.3, FSUBR-2.4, FSUBR-2.5, FSUBR-2.6, FSUBR-2.7, FSUBR-2.8, FSUBR-2.9, FSUBR-10.3, FSUBR-10.4
Reuse: rung 2 — extend `passes.md` Pass P1 and `extract_owns_from_tasks_text`
Respects: ARCH-1, ARCH-3
Interface: `extract_owns_from_tasks_text(text) → { paths: set[str], notes: [Note] }`
Depth: n/a — extends FSUB P1 / `extract_owns_from_tasks_text`
Locality: extend `passes.md` + `reference_derive.py`; leave map-features; leave audit-trace

#### Multi-block + fence-aware stop

Same as prior freeze: all Files headers; fence tracker; stop at next Files,
`#{2,6}` heading, Reuse, Interfaces, Depends-on, Steps/checklist — **outside**
fences only.

#### Candidate provenance

Each candidate is tagged at extraction:

| provenance | Source |
|---|---|
| `labeled` | Create/Modify/Move/Test bullet path |
| `backticked` | `` `path` `` token inside Files body |
| `slash_path` | unquoted token containing `/` |
| `unquoted_prose` | other unquoted path-like token in Files body |

#### Classifier pipeline (fixed order)

For each raw candidate with its provenance:

1. **Strip wrappers lightly for inspection:** remember if originally backticked;
   strip surrounding backticks for the working string; strip trailing `#` comments;
   apply **glued line-suffix strip** (`:[0-9]+([,-][0-9]+)*`).
2. **Empty → drop.**
3. **Reject unsafe / sentinel forms (before any accept):**
   - token ∈ {`.`, `..`}  
   - URL schemes: `://` or leading `http:` / `https:` / `file:`  
   - absolute path: starts with `/` or Windows `^[A-Za-z]:[\\/]`  
   - traversal: any segment `..` after split on `/`  
   - trailing prose punctuation: ends with `.` `,` `;` `:` `)` `]` `}` (after suffix strip)
     — catches `pass.`, `contract.`, `nothing.`  
4. **Provenance-gated accept:**
   - If provenance ∈ {`labeled`, `backticked`}: accept if the token is a
     **plausible path form**: contains `/`, **or** is a single segment matching
     `^[A-Za-z0-9._-]+$` with **no** consecutive `..`, **or** starts with `.`
     and length>1 (dotfile). Unknown extensions allowed under labeled/backticked.
   - If provenance is `slash_path`: accept if no remaining reject rules and
     denoise will apply; segments must not be empty.
   - If provenance is `unquoted_prose`: accept **only if**:
     - root **dotfile** form: matches `^\.[A-Za-z0-9][A-Za-z0-9._-]*$` (e.g.
       `.gitignore`, `.env.example`) — **not** `.` or `..` (already rejected); or  
     - basename matches **broad extension set** (documented freeze):  
       `.md .py .ts .tsx .js .jsx .mjs .cjs .sh .bash .zsh .json .yml .yaml .toml
       .lock .txt .html .css .svg .rs .go .java .kt .swift .rb .php .cs .cpp .h
       .hpp .sql .proto .graphql .vue .svelte .r .jl .scala .clj .ex .exs .erl
       .hs .lua .pl .pm .rake .gradle .cmake .mk`  
       **or**
     - single-segment **well-known root basename** (**no `.` characters** in the
       token): exact set  
       `{Makefile, Dockerfile, LICENSE, COPYING, NOTICE, AUTHORS, CONTRIBUTING,
       CHANGELOG, HISTORY, Rakefile, Procfile, Vagrantfile}`  
       (case-sensitive as written in token after normalize). **Not** `Gemfile` —
       denoise basenames own that token (would always be stripped after accept).
5. **Denoise** (existing FSUB stop-lists).
6. Else **drop**.

**Explicit non-accepts for dotted identifiers:** `self.assertEqual`,
`unittest.TestCase`, `json.loads`, `re.search` fail step 3 (if ending issues)
or step 4 unquoted_prose (no slash; not in extension set as filename with
allowed ext — `loads` is not an ext list entry; multi-dot identifiers are not
single-segment well-known roots). They never get `labeled`/`backticked` unless
authored that way in Files (which would be author error; still if labeled
`Create: self.assertEqual` the plausible-path single segment would accept —
fixture documents that labeled explicit nonsense is accepted; production tasks
use real paths).

#### Decision table (locked fixtures)

| Token | Provenance | Result | Why |
|---|---|---|---|
| `AGENTS.md` | labeled or backticked | **accept** | labeled/backticked plausible segment |
| `AGENTS.md` | unquoted_prose | **accept** | `.md` in broad set |
| `README.md` | unquoted_prose | **accept** | `.md` |
| `foo.py` | unquoted_prose | **accept** | `.py` |
| `assertions.md` | unquoted_prose | **accept** | `.md` (not substring-assert kill) |
| `Makefile` | unquoted_prose | **accept** | well-known root, no dots |
| `Makefile` | labeled | **accept** | labeled plausible |
| `.gitignore` | labeled/backticked/unquoted | **accept** | dotfile form after reject step (not `.`/`..`) |
| `src/app/App.tsx` | slash_path | **accept** | slash path |
| `.claude-plugin/plugin.json` | slash_path | **accept** | slash path |
| `.` | any | **reject** | sentinel |
| `..` | any | **reject** | sentinel (not “dotfile”) |
| `pass.` | unquoted_prose | **reject** | trailing punctuation |
| `contract.` | unquoted_prose | **reject** | trailing punctuation |
| `self.assertEqual` | unquoted_prose | **reject** | not broad-ext filename; not well-known root |
| `unittest.TestCase` | unquoted_prose | **reject** | same |
| `json.loads` | unquoted_prose | **reject** | same |
| `re.search` | unquoted_prose | **reject** | same |
| `nothing` | unquoted_prose | **reject** | no ext; not well-known root |
| `weird.xyz` | unquoted_prose | **reject** | ext not in broad set |
| `weird.xyz` | labeled | **accept** | labeled allows unknown ext |
| `Create: src/later.ts` (task 2+) | labeled | **accept** | multi-block retention |

#### Malformed block (FSUBR-10.3)

Skip block with `p1_block_skipped` when fence depth ≠ 0 at the stop boundary
(`detail: unclosed_fence`). Whole-line Files headers with no body (EOF after the
header line) yield an empty body — **not** a separate `truncated_header` note.

**Fixture recovery (recommended freeze):** malformed block is the **last** Files
block in the file. Valid siblings **before** it remain outside the unclosed fence.

Exact fixture `tests/feature-subgraph/fixtures/p1-malformed-block/`:

```text
### Task A
**Files:**
- Create: `src/ok.ts`
**Reuse:** none

### Task B
**Files:**
- Create: `src/also.ts`
**Reuse:** none

### Task C
**Files:**
- Create: `src/lost.ts`
```  
```python
# unclosed fence — no closing fence before EOF
x = 1
```

Expected: OWNS includes `src/ok.ts`, `src/also.ts`; does **not** require
`src/lost.ts` (inside unclosed fence body); note `p1_block_skipped` for the
feature; **no** hard resync across fence (trade-off: author must close fences
or place broken blocks last — documented).

#### Unreadable file (FSUBR-10.4)

**Missing `tasks.md`:** empty OWNS, no note (baseline).

**Unreadable:** path **exists** in the fixture tree but read/decode fails —
e.g. invalid UTF-8 bytes in `tasks.md`, or test FS adapter raises
`PermissionError`/`OSError` on open. Emit `p1_file_unreadable`, empty paths,
continue other features.

### 2. Envelope schema 1.1 (neighbors)

Satisfies: FSUBR-1.1, FSUBR-1.2, FSUBR-1.3, FSUBR-1.4, FSUBR-1.5, FSUBR-1.6, FSUBR-1.7, FSUBR-1.8, FSUBR-1.9, FSUBR-1.10, FSUBR-1.11, FSUBR-1.12, FSUBR-9.3
Reuse: rung 2 — extend `envelope.md` + neighbors recipe
Respects: ARCH-1, ARCH-3
Interface: neighbors payload; integer `shared_paths`; `notes` from snapshot
Depth: n/a — extends FSUB envelope / neighbors merge
Locality: extend `envelope.md`, `passes.md`, oracle

(Field shapes, path lex order, term casefold, via_traces, forbidden bags —
unchanged from prior freeze; consume **snapshot only**.)

### 3. Query `cluster`

Satisfies: FSUBR-3.1, FSUBR-3.2, FSUBR-3.3, FSUBR-3.4, FSUBR-3.5, FSUBR-3.6, FSUBR-3.7, FSUBR-3.8, FSUBR-3.9, FSUBR-3.10, FSUBR-3.11, FSUBR-3.12, FSUBR-3.13, FSUBR-3.14, FSUBR-3.15
Reuse: rung 2 — pure function of snapshot after Stage B
Respects: ARCH-1, ARCH-3
Interface: `cluster(focus, snapshot) → payload`; no file IO
Depth: n/a — extends load-subgraph query set
Locality: extend `passes.md`, `envelope.md`, oracle

Eligibility, caps, path_evidence, OOS display/key/ceiling — as prior freeze.
OOS texts come only from `snapshot.source_texts` populated by Stage B.

### 4. Retrieval package + caller skills

Satisfies: FSUBR-4.1, FSUBR-4.2, FSUBR-4.3, FSUBR-4.4, FSUBR-5.1, FSUBR-5.2, FSUBR-5.3, FSUBR-6.1, FSUBR-7.1, FSUBR-7.2, FSUBR-8.1, FSUBR-8.2, FSUBR-9.8, FSUBR-9.11, FSUBR-9.12, FSUBR-9.13, FSUBR-9.14, FSUBR-9.15
Reuse: rung 2 — extend skill bodies
Respects: ARCH-1, ARCH-2, ARCH-5
Interface: package =
  `{ envelope_markdown, seeds, fingerprints: map path→{sha256, present}, schema_version, recipe_id, buffered_bytes?: map path→bytes }`
Depth: n/a — extends frame-change, inspect-change, clarify-decisions, design-solution, plan-tasks, root-cause
Locality: extend those skills; leave build-family

**Validity (FSUBR-9.14):** seeds + schema/recipe match; for every fingerprint
entry, `present` and `sha256` still hold (absent stays absent; present content
unchanged). Optional layers use presence sentinels. If invalid → rederive using
buffered bytes when available so the same path is not double-read.

**Caller table:** nested + standalone clarify; all rows use grounded claims;
plan-tasks blast_radius + cluster(feature CODE); root-cause after Phase 2.

**Grounded-claims packaging (as shipped):** recipe lives in one home —
`skills/execution/load-subgraph/references/grounded-claims.md` (cite triple,
`with_owns < registered` before absence claims, emptiness-first, no invent,
ignore unknown `via_traces`). Callers point at that file; they do not restate
the recipe. Contract tests enforce the pointer layout.

### 5. Guide and inventory

Satisfies: FSUBR-9.9, FSUBR-9.10
Reuse: rung 2 — extend guide pages and inventory tables
Respects: ARCH-3
Interface: human-readable `cluster` + callers
Depth: n/a — extends `docs/guide/concepts/feature-graph.md`, `docs/guide/START-HERE.md`, `docs/guide/skills/README.md`, AGENTS / architecture tables as needed
Locality: extend those files; leave pathfind docs

### 6. Guards (carry-forward)

Satisfies: FSUBR-9.1, FSUBR-9.2, FSUBR-9.4, FSUBR-9.5, FSUBR-9.6, FSUBR-9.7
Reuse: rung 2 — preserve FSUB contracts
Respects: ARCH-1, ARCH-2, ARCH-3
Interface: no GRAPH.md / depends_on; advisory; oracle pack-only; audit-trace unchanged; pathfind separate; P3–P5 no-op
Depth: n/a — extends FSUB guard posture in `passes.md`, `envelope.md`, `load-subgraph/SKILL.md`, scenarios
Locality: leave audit-trace impl, pathfind, FSUB requirements bodies

### 7. Security NFR

Satisfies: FSUBR-10.2
Reuse: rung 2 — extend feature-subgraph security fixtures
Respects: ARCH-1, ARCH-3
Interface: passive path/prose data (no instruction execution)
Depth: n/a — extends `tests/feature-subgraph/` fixtures
Locality: extend tests only

*(FSUBR-10.1 lives only on Module 0.)*

## Seams for testing

| Seam | Kind | Covers |
|---|---|---|
| `extract_owns_from_tasks_text` + classifier decision table (all rows) | unit | FSUBR-2.1–2.9 |
| malformed last-block fixture + `p1_block_skipped` | unit | FSUBR-10.3 |
| unreadable: invalid UTF-8 tasks.md or FS adapter error (not missing file) | unit | FSUBR-10.4 |
| missing tasks.md → empty OWNS, no unreadable note | unit | FSUBR-2.x baseline / 5.3 empty |
| note list retains all reliability notes (no count drop) | unit | FSUBR-10.3, 10.4 |
| `snapshot.read_ledger`: each path ≤1 | unit | FSUBR-10.1 |
| queries invoked with IO-disabled adapter (raise on any read) | unit | snapshot purity |
| neighbors 1.1 evidence orders | unit | FSUBR-1.* |
| cluster k=1, truncation formula, OOS | unit | FSUBR-3.* |
| package fingerprint presence sentinels | unit | FSUBR-9.14 |
| skill prose callers + grounded claims | scenario | FSUBR-4–8, 9.8, 9.11–9.15 |
| guide/inventory | source | FSUBR-9.9–9.10 |
| no GRAPH / no depends_on / no skill py | source | FSUBR-9.1, 9.2, 9.4 |

## Coverage check

| Module | Satisfies (exclusive) | Count |
|---|---|---|
| 0 Snapshot | FSUBR-10.1 | 1 |
| 1 P1 | 2.1–2.9, 10.3, 10.4 | 11 |
| 2 Envelope | 1.1–1.12, 9.3 | 13 |
| 3 cluster | 3.1–3.15 | 15 |
| 4 Callers | 4.1–4.4, 5.1–5.3, 6.1, 7.1–7.2, 8.1–8.2, 9.8, 9.11–9.15 | 18 |
| 5 Guide | 9.9, 9.10 | 2 |
| 6 Guards | 9.1, 9.2, 9.4, 9.5, 9.6, 9.7 | 6 |
| 7 Security NFR | 10.2 | 1 |
| **Total** | | **67** |

Literal `Satisfies:` extraction must yield **67 total, 67 unique, 0 dup/missing/extra**.

**Deliberately unmapped:** Accessibility None only.

### Frozen constants summary

| Name | Value |
|---|---|
| `CLUSTER_K` | 1 |
| `CLUSTER_MEMBERS_MAX` | 8 |
| evidence max | 5 / 5 |
| OOS | 6 items / 1200 display code points |
| `recipe_id` | `fsubr-1.1` |
| note kinds | `p1_block_skipped`, `p1_file_unreadable`, `cluster_focus_invalid` |
| note cap | **none** (dedupe only) |
