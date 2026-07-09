# Design: Horizontal feature-graph layer

Feature code: FGRAPH
Status: Implemented
Date: 2026-07-09
Requirements: ./requirements.md

## Context

The skill set already keys everything on a feature code and enforces the *vertical*
trace with `scripts/check-trace.mjs` — a dependency-free ESM script that walks
`<specsDir>/<feature>/{requirements,tasks}.md`, reads config from
`docs/agents/trace.json` (default `specsDir: docs/specs`), takes `--root`/`--json`, and
exits 1 on error. FGRAPH adds the *horizontal* layer as its sibling, `check-graph.mjs`,
and must feel like the same tool: same config file, same flags, same failure discipline,
same "a script keeps this honest" philosophy.

The constraint that shapes everything: **the source of truth is the specs a feature
already writes** (`design.md`, `tasks.md`) — no new authoring (FGRAPH-9.5). The spike
(`scratchpad/surface-spike.mjs`, throwaway) proved a line-oriented token scanner harvests
a usable surface from those files, and exposed the two real hazards it must handle:
basename-vs-fullpath double counting and non-path junk tokens. Role accuracy
(owns vs touches) is explicitly *best-effort* — the dedup signal rides on shared-surface
*presence*, not on ownership being right (FGRAPH-2.3), which keeps the parser cheap.

The three consumers (brainstorm dedup at the gate, sync-spec freshness, verify/CI lint)
all want the same underlying graph, computed fresh. That points at a single spine —
**one `harvest()`, three renderers** — rather than three parsers that could drift.

`check-graph.mjs` diverges from `check-trace.mjs` in exactly one way: it **exports its
pure core** (`harvest`, `query`, `renderGraphMd`) behind a `main`-guarded CLI, because
FGRAPH's fine-grained parser requirements (normalization, dedup, junk rejection) are best
unit-tested as functions, not only through a black-box CLI. Everything else mirrors
check-trace.

## Decisions

1. **One script, exported core + main-guarded CLI.** `check-graph.mjs` exports `harvest`,
   `query`, `renderGraphMd`; the CLI runs only when invoked directly
   (`if (import.meta.url === pathToFileURL(process.argv[1]).href)`). Enables unit seams
   without a second file. (Divergence from check-trace, justified above.)
2. **One harvest, three consumers.** `harvest(specsDir) → Graph` is the only parser.
   `--harvest` writes `renderGraphMd(graph)`; `--query` runs `query(graph, criteria)`;
   `--verify` re-renders and diffs. Freshness (FGRAPH-5.4) is structural: query never
   reads GRAPH.md.
3. **GRAPH.md carries cards + the shared-surface table only**, not the full reverse
   index. The full index lives in-memory for `query`; the non-shared majority is noise in
   a committed file. Keeps diffs meaningful and determinism cheap.
4. **Config reuses `trace.json`.** `specsDir` shared with check-trace; an optional
   `graph` key (`sourceRoots`, `sourceExts`, `cardCap`) overrides internal DEFAULTS,
   mirroring how check-trace exposes `testGlobs`.
5. **Role is a best-effort booster, not a parser spine.** Generic line-verb hints classify
   by default; an explicit `Create:`/`Modify:` block label upgrades confidence. No repo is
   required to use those labels (FGRAPH-9.5).

No ADR: none of these is both hard-to-reverse and surprising — they follow check-trace's
established pattern. (Domain-modeling adds the five new glossary terms to CONTEXT.md:
Surface, Surface manifest, Reverse index, Shared surface, Summary card.)

## Architecture

### The Graph data model

Satisfies: FGRAPH-2.1, FGRAPH-2.2, FGRAPH-2.3

`harvest(specsDir)` returns a plain, JSON-serializable object — the single value every
consumer reads:

```
Graph = {
  features: [{ code, name, owns: [path], touches: [path], interfaces: [str], oos: [str] }],
  reverse:  { [path]: [{ code, role }] },   // full index, in-memory only
  shared:   [{ path, refs: [{ code, role }] }],  // refs.length >= 2, for GRAPH.md
}
```

Deletion test: a caller holding a `Graph` never needs to know how a path was tokenized,
normalized, or classified — it asks "who touches X" (`reverse`) or "what does F own"
(`features`). The interface is far narrower than the parsing it hides. Deep enough.

### Harvest parser (the hard part — designed twice)

Satisfies: FGRAPH-1.1, FGRAPH-1.2, FGRAPH-1.3, FGRAPH-1.4, FGRAPH-1.5, FGRAPH-1.6, FGRAPH-9.1

**Framing A — line-oriented token scanner** (the spike): iterate every line of
`design.md`/`tasks.md`, pull backtick-wrapped and bare word tokens, normalize, keep the
ones that look like paths, classify role from same-line verb hints. Simple, proven,
format-agnostic; role is line-local so a path named on a prose line gets no strong role.

**Framing B — section-aware structured parser**: recognize `tasks.md`'s `Files:` /
`- Create:` / `- Modify:` blocks and `design.md` file-map headings as typed regions and
attribute role from the region. More accurate role, but brittle — it assumes those exact
headings, which no requirement mandates.

**Chosen: hybrid, A as spine + B as a role booster.** The scanner (A) is the harvest
engine — it alone decides *which* paths exist (the part the spike validated). Block
detection (B) runs only to *upgrade role confidence*: a path under a `Create:` label →
`owns`; under `Modify:` → `touches`; otherwise fall back to A's line-verb hint; if neither,
`touches` (safe default — never invents ownership). Because role is best-effort
(FGRAPH-2.3), B staying shallow is acceptable. Pipeline of pure helpers, each a natural
unit test:

- `normalizePath(token)` — strip `` ` ``/quotes; drop trailing `:12`, `:1,2`, `(~12-20)`
  locators (FGRAPH-1.3).
- `isSourcePath(token)` — true iff it has a known extension (`sourceExts`) OR sits under a
  known root (`sourceRoots`) AND has a real filename segment; rejects bare `src-tauri/`,
  bare `.spec.ts` (FGRAPH-1.5).
- `dedupeByFullest(paths)` — collapse basename + fuller path to the fullest seen within a
  feature (FGRAPH-1.4).
- `classifyRole(line, blockLabel)` — B-boosted best-effort owns/touches: a `Create:`/`Modify:`
  block label (`blockLabel`) or a create-verb in the line wins, else `touches` (FGRAPH-1.6).

A feature with `requirements.md` but no `design.md`/`tasks.md` yields empty `owns`/`touches`
without error (FGRAPH-9.1).

### Summary cards

Satisfies: FGRAPH-3.1, FGRAPH-3.2, FGRAPH-3.3, FGRAPH-3.4

Built inside `harvest` per feature: `code` + `name` from `requirements.md` header; `owns`
from the manifest; `oos` from the `## Out of Scope` section (FGRAPH-3.2); `interfaces`
best-effort from `Interfaces:` blocks in `design.md`/`tasks.md` (FGRAPH-3.3). Each list is
truncated to `cardCap` (default 12) with an elision marker so a card stays far smaller
than its `requirements.md` (FGRAPH-3.4).

### GRAPH.md renderer

Satisfies: FGRAPH-4.1, FGRAPH-4.2, FGRAPH-4.3, FGRAPH-9.2

`renderGraphMd(graph)` returns a deterministic string: a `<!-- GENERATED … do not edit -->`
banner, a `## Cards` section (one `###` block per feature), and a `## Shared surface`
table. Determinism (FGRAPH-4.2) comes from total ordering: features by code; paths
lexicographically; a path's refs by code. `--harvest` writes it to
`<specsDir>/GRAPH.md`; `INDEX.md` is never opened for writing (FGRAPH-4.3). Empty specs →
banner + empty sections, exit 0 (FGRAPH-9.2).

### Query interface (the second hard part — designed twice)

Satisfies: FGRAPH-5.1, FGRAPH-5.2, FGRAPH-5.3, FGRAPH-5.4, FGRAPH-5.5, FGRAPH-5.6

**Framing A — graph-in-memory, query is a pure filter**: `query(graph, {paths, keywords})`
filters the already-harvested `Graph`. **Framing B — reparse GRAPH.md on query**: rejected —
violates freshness (FGRAPH-5.4) and needs a fragile GRAPH.md back-parser.

**Chosen: A.** `query` takes the in-memory graph the CLI just harvested (FGRAPH-5.4 free)
and returns matches: by path via `reverse` (FGRAPH-5.1), by keyword via case-insensitive
substring against each card's `name` + `oos` (FGRAPH-5.2), each result carrying its full
card. Results rank by count of overlapping paths, descending (FGRAPH-5.3). The CLI prints
`JSON.stringify` to stdout (FGRAPH-5.5). Reads only markdown, no network/build (FGRAPH-5.6,
guaranteed because `harvest` only does `fs.readFileSync` on `.md`).

### Verify mode

Satisfies: FGRAPH-6.1, FGRAPH-6.2, FGRAPH-6.3

`--verify` computes `renderGraphMd(harvest(specsDir))` and compares byte-for-byte with the
committed `GRAPH.md`: differ → print a staleness diff summary, exit 1 (FGRAPH-6.1);
identical → exit 0 (FGRAPH-6.2). Separately, any harvested feature code absent from
`INDEX.md` → report + exit 1 (FGRAPH-6.3). Mirrors check-trace's error reporting and
`--json` shape.

### CLI wrapper and config

Satisfies: FGRAPH-9.3

`main`-guarded arg parse (`--harvest|--query|--verify`, `--root`, `--json`, query takes
`--path`/`--keyword` repeatables). `loadConfig()` copied from check-trace: read
`docs/agents/trace.json` if present, else DEFAULTS; missing `graph` key → internal
`sourceRoots`/`sourceExts`/`cardCap` DEFAULTS; missing `trace.json` → `specsDir` falls
back to `docs/specs` (FGRAPH-9.3). Missing specsDir → exit 0, matching check-trace (the empty-graph
behavior itself is FGRAPH-9.2, owned by the GRAPH.md renderer section).

### Skill wiring — brainstorm

Satisfies: FGRAPH-7.1, FGRAPH-7.2, FGRAPH-7.3, FGRAPH-7.4, FGRAPH-7.5, FGRAPH-9.6

Edit `skills/discovery/brainstorm/SKILL.md` step 1 ("Explore project context"). After the
scan subagent returns candidate files, call
`node scripts/check-graph.mjs --query --json` with those paths and the idea's key terms as
`--keyword`s; present returned features as **cards, not specs** (FGRAPH-7.2). The step-1
**Done when** gains: "state which existing features share this idea's surface and how this
differs, citing codes" (FGRAPH-7.3), or "no existing feature shares the surface" when empty
(FGRAPH-7.4). A wrapping instruction makes the query **fail-open**: if the script errors or
is absent, note "automated overlap check unavailable" and continue manual exploration
(FGRAPH-7.5) — including harnesses without subagents, where the query runs directly on the
idea's terms (FGRAPH-9.6).

### Skill wiring — sync-spec

Satisfies: FGRAPH-8.1, FGRAPH-8.2

Edit `skills/track/sync-spec/SKILL.md`. In step **f (After picture)**, after check-trace,
run `node scripts/check-graph.mjs --harvest` to regenerate `GRAPH.md` (FGRAPH-8.1); if it
changed, stage it into the sync-spec commit alongside the `Status:`/`INDEX.md` edits
(FGRAPH-8.2).

### Skill wiring — verify

Satisfies: FGRAPH-6.4

Edit `skills/execution/verify/SKILL.md`. In the claim→evidence table, the "Requirements
met" row's evidence becomes `check-trace` **and** `check-graph --verify` both pass
(FGRAPH-6.4).

### Guards

Satisfies: FGRAPH-9.4, FGRAPH-9.5

FGRAPH-9.4 (check-trace unchanged): `check-graph.mjs` is a new file touching no
check-trace code or output; guarded by check-trace's own existing test suite staying green.
FGRAPH-9.5 (no new authoring burden): structural — `harvest` reads only existing
`requirements/design/tasks.md` content and mandates no new fields; guarded by running the
harvest against the untouched `bot` repo specs and asserting a non-empty graph.

### Harvest-quality amendment (post-ship, tier-1)

Satisfies: FGRAPH-1.7, FGRAPH-1.8, FGRAPH-1.9, FGRAPH-2.4, FGRAPH-2.5, FGRAPH-3.5, FGRAPH-4.4

Dogfooding `check-graph --harvest` on the bot repo's 4 real features exposed four harvest-quality
defects; each is a refinement of an existing component above, at the same seams (no new seam):

- **Glob rejection (1.7)** — `isSourcePath` rejects any token containing `*` before the extension/root checks.
- **Command-path exclusion (1.8) + guard (1.9)** — `scanSurface` tracks, per path, whether it had a
  non-command occurrence; a path seen only on command-invocation lines is dropped. `CMD_LINE_RE` is
  **anchored** — a command word counts only at line-start (with optional `-*>` bullet / `$` prompt) or
  immediately after a backtick — so ordinary prose containing "node"/"git"/etc. is not misread as a command
  (the 1.9 guard). Real surface in unfenced `Files:`/`Create:`/`Modify:` bullets and prose backticks is preserved.
- **Cross-feature dedup (2.4) + guard (2.5)** — `harvest` builds a global `canon` map (basename → fullest
  path seen across ALL features) and keys the reverse index / shared surface by the canonical form, so a file
  referenced bare in one spec and full-path in another is one shared surface. Distinct files sharing a basename
  (`a/util.ts` vs `b/util.ts`) are not merged (suffix match only). The validated CHIPUI↔INLTASK surface still resolves.
- **Lean interfaces (3.5)** — `extractInterfaces` keeps only top-level `Interfaces:` bullets, drops bare
  `Produces:`/`Consumes:` labels (promoting their child substance), and truncates each entry at the first ` — `
  to keep the signature, not the prose.
- **Determinism guard (4.4)** — all of the above preserve total ordering; `renderGraphMd(harvest(x))` stays byte-stable.

### Code-review duplication check (post-ship, tier-1) — Story 10

Satisfies: FGRAPH-10.1, FGRAPH-10.2, FGRAPH-10.3, FGRAPH-10.4, FGRAPH-10.5, FGRAPH-10.6

The 4th graph consumer, alongside brainstorm/sync-spec/verify — a purely advisory wiring of the
existing `--query` mode into `skills/review/code-review/SKILL.md`, at the same seam as the other
consumers (a wiring regression test in `check-graph.wiring.test.mjs` asserting the durable markers).
A new controller step `## 3a` runs `check-graph --query` on the diff's changed source files (from the
range pinned in step 1); when overlaps are found and the Spec axis runs, the overlapping features'
summary cards are added to the Spec subagent's brief, which is directed to raise a **reuse-miss**
finding — citing the neighbor's feature code — where the diff rebuilds behavior a shares-surface
neighbor owns. No new `check-graph` capability: it consumes `query`'s existing output. Fail-open and
empty-overlap paths mirror brainstorm (FGRAPH-7.4/7.5). The Standards axis, aggregate step, verdict,
and the "never pre-judge findings" rule are untouched (FGRAPH-10.6).

## Seams for testing

Unit seams are the exported pure functions; the integration seam is the CLI black-box
(temp-repo fixture + `spawnSync` + `--json`), exactly as `check-trace.test.mjs` works.
Skill-behavior requirements are verified by acceptance/pressure-test, not check-graph units.

| Seam | Kind | Covers |
|---|---|---|
| `harvest(specsDir)` (exported) | unit | FGRAPH-1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4, 9.1 |
| `query(graph, criteria)` (exported) | unit | FGRAPH-5.1, 5.2, 5.3 |
| `renderGraphMd(graph)` (exported) | unit | FGRAPH-4.2, 4.3, 9.2 |
| `check-graph.mjs` CLI (`--root`, `--json`) | integration | FGRAPH-4.1, 5.4, 5.5, 5.6, 6.1, 6.2, 6.3, 9.3 |
| check-trace's own test suite stays green | integration | FGRAPH-9.4 |
| harvest over the `bot` repo specs | integration | FGRAPH-9.5 |
| brainstorm SKILL.md behavior | pressure-test | FGRAPH-7.1, 7.2, 7.3, 7.4, 7.5, 9.6 |
| sync-spec SKILL.md behavior | pressure-test | FGRAPH-8.1, 8.2 |
| verify SKILL.md behavior | pressure-test | FGRAPH-6.4 |

## Coverage check

Every FGRAPH ID 1.1–9.6 appears in exactly one `Satisfies:` line above. No deliberately
unmapped requirements. Cross-check: 2.1/2.2/2.3 → Graph data model; 1.1–1.6 + 9.1 →
Harvest parser; 3.x → Cards; 4.x + 9.2 → GRAPH.md renderer; 5.x → Query; 6.1–6.3 →
Verify mode; 6.4 → verify wiring; 7.x + 9.6 → brainstorm wiring; 8.x → sync-spec wiring;
9.3 → CLI/config; 9.4/9.5 → Guards.
