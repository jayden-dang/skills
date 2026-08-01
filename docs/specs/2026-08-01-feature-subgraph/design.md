# Design: Feature subgraph derivation

Feature code: FSUB
Status: Approved
Date: 2026-08-01
Approved: 2026-08-01 (user)
Requirements: ./requirements.md

## Context

Horizontal feature overlap today is **live grep** over `docs/specs/` on two
signals — candidate paths and key terms — with no generated index
(`docs/guide/concepts/feature-graph.md`, `docs/architecture/artifacts.md`).
That doctrine correctly rejects a materialized graph (staleness). It does not
give multi-hop queries, ranked path overlap, OWNS coverage honesty, or a
single place callers invoke.

The binding constraint is the frame measurement: optional hand-declared edges
fill ~10% (useless as a graph), while mandatory `**Files:**` blocks already
yield OWNS/OVERLAPS with zero new authoring — if and only if path noise is
denoised and the term channel is preserved for pre-code `frame-change`. The
alternative rejected is a committed `GRAPH.md` / JSON projection (previous
design failure) or a code-KG (Neo4j/Tree-sitter) that would violate ARCH-3 for
consumers and still would not mint feature IDs.

This pack already expresses deterministic multi-file checks as **skill prose**
with fixed `grep`/set rules (`audit-trace`) and proves rules with **Python under
`tests/` only** (roadmap, VPF fingerprint) — pure tests that read fixtures and
assert; they do not import an implementation from `skills/`. There is **no**
`.py` under `skills/` today; the only executable shipped inside a skill package
is `skills/ship/record-verdict/validate-records.sh`. FSUB continues that
pattern: **`passes.md` is the single shipped source of truth** for derivation
recipes; a **test-side reference implementation** under `tests/feature-subgraph/`
validates constants and edge cases against those recipes. It is not shipped to
consumers, is not imported by the skill, and does not create a Python module
under `skills/`.

### Architecture invariants relied on

- **ARCH-1** — P0–P5 and queries are fixed extraction + set ops; no LLM judgment
  of “real” ownership or overlap quality beyond the fixed rules.
- **ARCH-2** — missing roadmap / architecture / Files → no-op empty sets, not
  invented nodes.
- **ARCH-3** — consumers need only skills + markdown; the test-side reference is
  pack verify only, never a methodology dependency.
- **ARCH-4** — nodes reuse existing ID strings only.
- **ARCH-5** — `map-features` is user-invoked only; `load-subgraph` is
  model-invoked; callers name `/map-features`, never auto-invoke it.

## Decisions

1. **Derivation at ask time, never a graph file** — satisfies FSUB-1.3 / 7.5;
   no ADR superseding artifacts.md (derivation *is* the live-read doctrine).
2. **`passes.md` is the only shipped derivation SSOT** under
   `skills/execution/load-subgraph/references/`. Agents execute those recipes
   via `load-subgraph`. A **test-side** reference implementation at
   `tests/feature-subgraph/reference_derive.py` encodes the same rules for
   unit tests (bounds, stop-list, line-suffix, ranking fixtures). Recipes are
   **validated** by that reference; agent **conformance** to `passes.md` is
   covered by scenario seams — not by a claim that “tests cannot drift from
   prose.”
3. **Bounds (requirements Open Questions closed here):**
   - **`NEIGHBORS_MAX = 12`** — FSUB-2.3 truncation after rank by shared
     meaningful path count (prototype “top 12” domination case).
   - **`P0_SEED_MAX = 12`** — after ranking term seeds by *match score*
     (below), take top 12; report truncation like OWNS coverage so a
     flood is visible, not silent.
   - **P0 ranking:** for each candidate `CODE`, score =
     `(number of distinct seed terms that match that feature’s specs) × 1000
     + (total case-insensitive match hits across requirements/design/tasks
     files for that feature)`. Higher first; ties break by `CODE` ascending
     (deterministic).
   - **P0 term filters (pre-match):** drop terms with length &lt; 3 after trim;
     case-fold for match; match as substring of file text (parity with today’s
     loose grep), not whole-word only.
4. **Stop-list** = FSUB-2.4 app minimum ∪ pack extension single-segment tokens:
   `{skills, templates, hooks, scripts, docs}` (case-sensitive as token after
   path normalization). Basename stop-list as requirements. Extensible later
   without shrinking the required minimum.
5. **Line-suffix strip** before OWNS: trailing `:[0-9]+([,-][0-9]+)*` on the
   last path segment only (covers `:86`, `:25-44`, `:86,1030`).
6. **Result envelope** always includes: query kind, ordered neighbors or
   subgraph nodes, **OWNS coverage** `owned_with_files / registered_total`,
   optional `p0_truncated: true` + counts, and “advisory — not a gate” banner.
7. **`map-features`** at `skills/track/map-features/` — propose→confirm only;
   DEPENDS_ON candidates never enter load-subgraph edges.
8. **Callers:** only `frame-change` and `inspect-change` required to route
   neighbor discovery through `load-subgraph` (FSUB-1.15); guide
   `feature-graph.md` updated to describe derivation + coverage.
9. **No new audit-trace E-codes; no P6 runtime edges; no HTML viz this feature.**

## Architecture

### 1. Derivation core — passes P0–P5 + queries

Satisfies: FSUB-1.3, FSUB-1.4, FSUB-1.5, FSUB-1.6, FSUB-1.7, FSUB-1.8, FSUB-1.9, FSUB-1.10, FSUB-1.11, FSUB-1.13, FSUB-1.14, FSUB-1.16, FSUB-2.1, FSUB-2.2, FSUB-2.3, FSUB-2.4, FSUB-2.5, FSUB-2.6, FSUB-3.1, FSUB-3.2, FSUB-3.3, FSUB-3.4, FSUB-5.1, FSUB-5.2, FSUB-5.3, FSUB-8.1, FSUB-8.2, FSUB-8.3
Reuse: none — new code (rung 7); pattern borrowed from `audit-trace` fixed passes, not a shared library
Respects: ARCH-1, ARCH-2, ARCH-3, ARCH-4
Interface: the recipes in `passes.md` (agent-executed) and the result envelope
  shape; queries are `neighbors(code)`, `ancestors(code)`, `descendants(mile)`,
  `blast_radius(path)`, `subgraph(seeds: terms|codes|paths)`. No write API.
  Test-side only: `reference_derive.run(repo_root, query) → ResultEnvelope`
  mirrors those recipes for unit fixtures.
Depth: if this module vanished, callers must still know: “read specs live; extract
  OWNS/terms with fixed rules; set-intersect; rank+bound; report coverage” —
  not each regex.
Locality: shipped recipes under `skills/execution/load-subgraph/references/`;
  test-side reference under `tests/feature-subgraph/`; leave `audit-trace` body
  unchanged; leave pathfind alone

**Layout**

```
skills/execution/load-subgraph/          # shipped skill — markdown only
  SKILL.md
  references/
    passes.md              # P0–P5 exact recipes + stop-list + bounds (SSOT)
    envelope.md            # result shape for callers

tests/feature-subgraph/                  # pack tests only — not shipped as skill
  reference_derive.py      # test-side reference implementing passes.md
  fixtures/                # thin-repo, mega-owner-100, p0-flood, …
  scenarios.md             # prose-path / skill-path scenarios
```

Agents follow `passes.md` with `grep`/reads via `load-subgraph` — they never
import `reference_derive.py`. Unit tests import the reference to lock constants
and edge cases (NEIGHBORS_MAX, P0_SEED_MAX, stop-list, line-suffix, FSUB-2.6
domination, coverage ratio). That validates the **recipes’** intended math; it
does **not** prove an LLM executed the prose. Scenario seams cover the skill
path (FSUB-1.2 and agent-facing behavior).

**Registry load**

- Parse `docs/specs/INDEX.md` table rows: `CODE`, name, spec dir, status, roadmap cell.
- For each CODE, resolve `Feature code:` from that feature’s `requirements.md`
  when present; if INDEX and requirements disagree, prefer INDEX for registry
  membership and flag in envelope notes (map-features later backfills).
- Never key by directory slug when CODE is available (FSUB-1.14).

**P0 TERMS** (`passes.md`)

1. Input: list of seed terms (caller-supplied).
2. Filter: drop empty and length &lt; 3.
3. For each registered feature, scan `requirements.md`, `design.md`, `tasks.md`
   under its spec dir (skip missing files).
4. Case-insensitive substring match of each term in file text.
5. Score and rank as Decision 3; keep top `P0_SEED_MAX` (12); set
   `p0_truncated` if more matched.
6. Emit seed CODE set.

**P1 OWNS**

1. For each feature with `tasks.md`, find blocks headed `**Files:**` (or
   `Files:`).
2. Extract path tokens from:
   - bullets `- Create:|Modify:|Move:|Test:` (optional backticks) then path;
   - remaining path-like tokens under the block (legacy prose): sequences
     matching `[A-Za-z0-9_./-]+\.[A-Za-z0-9]+` or directory-looking
     `…/…` tokens.
3. Strip glued line suffix per Decision 5.
4. Normalize: strip surrounding backticks and whitespace; keep repo-relative form.
5. Empty → empty OWNS set (FSUB-5.3); unparseable block → empty + non-fatal note
   (FSUB-8.3).

**Denoise (meaningful paths)**

- Drop if basename ∈ manifest/lockfile stop-list (FSUB-2.4).
- Drop if path is a **single segment** ∈ workspace-root set ∪ pack extension
  (Decision 4).
- Do **not** expand to ancestors; equality is exact string on normalized token.
- Explicit directory ownership: token ending with `/` or with no file extension
  **and** present as a full Files entry (not a parent of another token) counts
  as that directory only — children are not implied (FSUB-2.2).

**P2 OVERLAPS**

- For each unordered pair of CODEs, if `|meaningful(OWNS_a) ∩ meaningful(OWNS_b)| > 0`,
  edge with weight = intersection cardinality.
- No edge from stop-list-only intersection (FSUB-2.5).

**P3 IMPLEMENTS** — INDEX roadmap cell live `ROAD-N` only; `—`/empty skip.

**P4 CONTAINS** — parse roadmap Members `**ROAD-N**` under each `## MILE-N`;
Goals: `GOAL-N` citations → `GOAL → MILE`. Absent roadmap → no-op (FSUB-5.2).

**P5 RESPECTS** — `Respects:.*ARCH-N` in design.md; absent architecture dir →
no-op (FSUB-5.1). Display-only in envelope; does not change audit-trace.

**Queries**

| Query | Algorithm |
|---|---|
| `neighbors(CODE)` | See **neighbors merge rule** below (union **before** single truncation). |
| `ancestors(CODE)` | IMPLEMENTS → ROAD → CONTAINS reverse to MILE → GOAL; bare CODE if no roadmap. |
| `descendants(MILE-N)` | member ROADs → CODEs with IMPLEMENTS. |
| `blast_radius(path)` | normalize path; CODEs whose OWNS contain exact token or explicit dir prefix match **only when** owned token is a directory ownership token; then their OVERLAPS neighbors one hop. |
| `subgraph(seed)` | resolve terms→P0, paths→OWNS owners, codes as-is; expand 1 hop OVERLAPS + ancestors skeleton; bound node list to `NEIGHBORS_MAX * 3` (36) by weight then CODE. |

**neighbors merge rule (Note C — bound always holds)**

1. Build **path candidates**: other CODEs with positive OVERLAPS shared-path weight
   against the focus CODE; `path_weight = |intersection|`.
2. If the caller supplied key terms, run P0 and take the truncated seed set
   (`P0_SEED_MAX`); those CODEs are **term candidates** (exclude the focus CODE).
3. Form the **union** of path candidates and term candidates **before** any
   neighbor list cut. For each code in the union set:
   - `path_weight` as above, or `0` if term-only;
   - `via` = `path` \| `term` \| `both`;
   - sort key = `(path_weight desc, via_rank desc, CODE asc)` where
     `via_rank` is `both=2`, `path=1`, `term=0` so path evidence outranks
     term-only at equal weight, and dual-signal outranks path-only at equal weight.
4. **Truncate once** to `NEIGHBORS_MAX` (12). Term seeds **compete for slots**
   inside that cap; they are never appended after truncation (that would break
   FSUB-2.3’s fixed maximum). If path-only candidates already fill 12 slots,
   lower-ranked term-only codes are dropped and `p0` / notes may record that
   term seeds were truncated by the neighbor bound.

**Result envelope** (always)

```text
advisory: true
owns_coverage: { with_owns: W, registered: R, ratio: W/R }
p0: { matched: M, returned: K, truncated: bool }
neighbors: [ { code, shared_paths: n, via: path|term|both } … ]
# or nodes/edges for subgraph
notes: [ … non-fatal parse skips … ]
```

No `DEPENDS_ON` field (FSUB-1.13).

### 2. Skill package — `load-subgraph`

Satisfies: FSUB-1.1, FSUB-1.2, FSUB-1.12, FSUB-7.1, FSUB-7.2, FSUB-7.4, FSUB-7.5
Reuse: rung 2 — skill shape of `audit-trace` (model-invoked, fixed passes, report)
Respects: ARCH-1, ARCH-5
Interface: REQUIRED SUB-SKILL entry for callers; inputs = repo root + query +
  optional terms/paths; output = envelope markdown in chat (no graph file write).
  Execution path is **only** `references/passes.md` + `envelope.md` — no Python.
Depth: n/a — extends audit-trace *shape*; recipes live in module 1’s `passes.md`
Locality: new skill dir (markdown only); leave pathfind (FSUB-7.4); callers in module 4

**SKILL.md checklist**

1. Resolve repo root; refuse inventing docs/specs.
2. Execute P0–P5 and the requested query **by following `references/passes.md`**
   (grep/reads/set ops). Do not call or invent a local Python helper.
3. Render envelope per `envelope.md`; always print OWNS coverage and advisory banner.
4. NEVER write GRAPH.md / JSON under docs/.
5. NEVER fail a gate on thin neighborhood.
6. Rationalization table: “skip P0, paths enough”; “boolean neighbors fine”;
   “empty OWNS means no features”; “materialize for speed”; “import the test
   reference in production”.

**FSUB-1.2 (determinism of the skill path):** two independent runs of
`load-subgraph` against the same frozen fixture tree (same query inputs) MUST
yield the same edge set and seed set. Covered by a **scenario** that (a) freezes
a fixture, (b) requires the skill body to name only `passes.md` as the procedure,
and (c) asserts identical envelopes across two scripted runs of the recipe
(via the test-side reference used as an oracle for expected output, plus a
scenario that the skill does not diverge from naming that procedure). The unit
tests on `reference_derive.py` prove the **recipe math** is deterministic; they
are not the sole coverage of FSUB-1.2.

### 3. Skill package — `map-features`

Satisfies: FSUB-6.1, FSUB-6.2, FSUB-6.3, FSUB-6.4, FSUB-6.5, FSUB-6.6, FSUB-7.6
Reuse: rung 2 — wizard shape of `configure-repo` (propose→confirm→additive write)
  + scan posture of `scan-architecture` (user-invoked, no auto)
Respects: ARCH-5, ARCH-2
Interface: `/map-features`; steps A–D proposals; write only confirmed items
Depth: if vanished, callers need “scan gaps → human confirm → edit SSOT only”
Locality: `skills/track/map-features/`; leave configure-repo; leave load-subgraph edges

**Proposal kinds**

| Kind | Source | Write target on confirm |
|---|---|---|
| Missing `Feature code:` | requirements without line but under INDEX/spec dir | requirements.md header |
| Empty ROAD bind | INDEX `—`/empty + user/heuristic ROAD | INDEX cell only (never invent ROAD-N) |
| OWNS gap | high-churn paths under src/skills not in any OWNS | optional note in design/tasks — **prefer** suggesting plan-tasks Files edit, not inventing ownership |
| DEPENDS_ON candidate | Reuse: / Interfaces: Consumes cross-feature names | design.md prose note or tasks Reuse — **never** load-subgraph edge store |

Unconfirmed DEPENDS_ON never appears in derive (FSUB-6.4). Unresolvable CODE →
first-class list item, no slug keying (FSUB-6.5).

### 4. Caller integration — frame-change & inspect-change

Satisfies: FSUB-1.15
Reuse: rung 2 — replace inline overlap grep steps with `load-subgraph` invoke
Locality: extend `skills/discovery/frame-change/SKILL.md`,
  `skills/review/inspect-change/SKILL.md`; leave pathfind
Interface: both pass idea terms + candidate paths into `subgraph` / `neighbors`;
  present Summary cards + OWNS coverage line; still non-blocking
Depth: n/a — extends frame-change / inspect-change

**frame-change:** seed terms from idea keywords; paths from scan digest when
any; if no paths yet, P0-only neighborhood is valid (FSUB-1.5 reason).

**inspect-change:** seed paths from diff; optional terms from PR title/body;
neighbor cards to Spec subagent for reuse-miss.

Update `docs/guide/concepts/feature-graph.md` to describe load-subgraph as the
implementation of the dual signal + coverage honesty (doctrine unchanged:
advisory, live read, no generated SSOT graph).

### 5. Harden Files grammar — plan-tasks + template

Satisfies: FSUB-4.1, FSUB-4.2, FSUB-7.3, FSUB-7.7
Reuse: rung 2 — extend existing Files authoring rules
Locality: `templates/tasks.md`, `skills/spec/plan-tasks/SKILL.md` only
Interface: documented example:

```markdown
**Files:**
- Create: `src/foo/bar.ts`
- Modify: `src/foo/baz.ts`  # lines 86–103 — not path:86-103
- Test: `tests/test_foo.py`
```

Legacy parse remains in `passes.md` / story 3. Task-level `Depends-on: Task N`
unchanged (FSUB-7.7).

### 6. Pack inventory and guide

Satisfies: none — packaging / inventory only (no criterion IDs; discoverability
  of `load-subgraph` and `map-features` is carried by FSUB-1.1 / FSUB-6.1 on
  modules 2 and 3)
Reuse: rung 2 — AGENTS / architecture skills tables / guide skills list
Locality: extend `AGENTS.md`, `docs/architecture/skills.md`,
  `docs/architecture/workflows.md` (horizontal neighbor step names load-subgraph),
  `docs/guide/concepts/feature-graph.md`, `docs/guide/skills/` pages for the two
  skills; plugin.json if skills are enumerated
Depth: n/a

## Seams for testing

Two layers — do not conflate them:

1. **Test-side reference** (`tests/feature-subgraph/reference_derive.py`) — unit
   seams that lock recipe math and fixtures. Not the skill execution path.
2. **Skill / prose path** (`load-subgraph` + `passes.md`) — scenario and source
   contracts. This is what agents run.

| Seam | Kind | Covers |
|---|---|---|
| `reference_derive.py` P1 legacy parse + line-suffix strip | unit | FSUB-3.1–3.4, FSUB-1.6 |
| `reference_derive.py` denoise stop-list + no ancestor expand | unit | FSUB-2.1, 2.2, 2.4, 2.5 |
| `reference_derive.py` neighbors rank + NEIGHBORS_MAX + 100+ path fixture | unit | FSUB-2.3, 2.6 |
| `reference_derive.py` neighbors union-before-truncate ≤ NEIGHBORS_MAX with terms | unit | FSUB-2.3 (merge rule) |
| `reference_derive.py` P0 rank + P0_SEED_MAX truncation | unit | FSUB-1.5, 1.11 (term resolve) |
| `reference_derive.py` P3/P4/P5 no-op without roadmap/architecture | unit | FSUB-5.1–5.3 |
| `reference_derive.py` OWNS coverage ratio on envelope | unit | FSUB-1.16 |
| `reference_derive.py` dual-run same fixture → same envelope (recipe math) | unit | FSUB-8.1 (bounded reads); supports oracle for FSUB-1.2 |
| `reference_derive.py` passive path/prose not executed | unit | FSUB-8.2 |
| Corrupt Files block skips feature, others remain | unit | FSUB-8.3 |
| Skill frontmatter: load-subgraph model-invoked; map-features user-invoked at `skills/track/map-features/` | unit / source contract | FSUB-1.1, FSUB-6.1, FSUB-6.6 |
| Source contract: no `*.py` under `skills/execution/load-subgraph/`; skill names only `passes.md` | unit / source | FSUB-1.1, ARCH-3 posture |
| **Scenario: two independent load-subgraph runs on frozen fixture → identical edge+seed sets (skill path / FSUB-1.2)** | scenario | **FSUB-1.2** |
| Scenario: skill procedure is passes.md only (no import of test reference) | scenario | FSUB-1.2, 1.1 |
| Scenario: no GRAPH.md write; advisory non-gate | scenario | FSUB-1.3, 1.12, 7.2, 7.5 |
| Scenario: frame-change / inspect-change call load-subgraph (dual signal) | scenario | FSUB-1.15 |
| Scenario: map-features propose/confirm; DEPENDS_ON not auto edge | scenario | FSUB-6.2–6.5 |
| Scenario: plan-tasks hardened Files examples in template | scenario / source | FSUB-4.1–4.2, 7.3 |
| Guards: audit-trace E-codes unchanged; task Depends-on parallelism | scenario | FSUB-7.1, 7.7, 1.13 |
| Trigger / inventory lists both skills | unit / trigger | packaging of FSUB-1.1, 6.1 |

Fixture root: `tests/feature-subgraph/fixtures/` (thin-repo, dense-Files,
legacy-glued-lines, mega-owner-100, no-roadmap, no-architecture, p0-flood).

## Coverage check

Every requirement ID appears in **exactly one** Satisfies line (module 6 cites
**no** IDs):

| IDs | Module |
|---|---|
| 1.3–1.11, 1.13, 1.14, 1.16 | Derivation core |
| 2.1–2.6 | Derivation core |
| 3.1–3.4 | Derivation core |
| 5.1–5.3 | Derivation core |
| 8.1–8.3 | Derivation core |
| 1.1, 1.2, 1.12, 7.1, 7.2, 7.4, 7.5 | load-subgraph skill |
| 1.15 | Caller integration |
| 6.1–6.6, 7.6 | map-features |
| 4.1, 4.2, 7.3, 7.7 | Harden Files / plan-tasks |
| *(none)* | Pack inventory (packaging only) |

Deliberately unmapped: none. Accessibility None needs no Satisfies.

**Count:** 16+6+4+2+3+6+7+3 = 47 behavioral/NFR IDs (excl. Accessibility None).
1.2 lives on the skill module (prose path), not solely on the test reference.

### Open Questions from requirements — design answers

| # | Answer |
|---|---|
| P0 seed bound + ranking | `P0_SEED_MAX = 12`; score = terms_hit×1000 + raw_hits; truncate + report |
| neighbors N | `NEIGHBORS_MAX = 12` |
| Pack stop-list | + `skills`, `templates`, `hooks`, `scripts`, `docs` (single segment) |
| Fixtures | `tests/feature-subgraph/fixtures/` as above |
