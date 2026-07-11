# Tasks: Horizontal feature-graph layer

> **For agentic workers:** REQUIRED SUB-SKILL: use `execute-plan` to implement
> this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

Feature code: FGRAPH
Status: Implemented
Date: 2026-07-09
Requirements: ./requirements.md
Design: ./design.md

**Goal:** Add `scripts/check-graph.mjs` — a dependency-free sibling to `check-trace.mjs`
that harvests a horizontal feature graph (surface manifest, reverse index, summary cards)
from existing specs and wires it into brainstorm/sync-spec/verify.

**Architecture:** One `harvest(specsDir) → Graph` parser feeds three consumers —
`renderGraphMd` (writes `docs/specs/GRAPH.md`), `query` (JSON overlaps for skills), and a
`--verify` freshness diff. The pure core is exported for unit tests; a `main`-guarded CLI
wraps it, mirroring check-trace's config/flag conventions.

**Tech Stack:** Node ≥20.11 ESM (`.mjs`) — `import.meta.dirname`, as check-trace.test.mjs
already requires — zero dependencies, `node --test` (built-in) with
`node:assert/strict`, `spawnSync` + `os.tmpdir()` fixtures — identical to
`scripts/check-trace.test.mjs`. Markdown SKILL.md edits for wiring.

## Global Constraints

- **Zero dependencies.** No npm packages. Standard library only (`node:fs`, `node:path`,
  `node:url`, `node:test`, `node:assert`, `node:child_process`, `node:os`). Same as
  check-trace.
- **Test command:** `node --test scripts/check-graph.test.mjs scripts/check-graph.wiring.test.mjs`.
  Run the whole suite after every task. There is no configured lint/typecheck in this repo.
- **Mirror check-trace conventions:** `#!/usr/bin/env node` shebang, a doc-comment header,
  `loadConfig()` reading `docs/agents/trace.json` with a `DEFAULTS` merge, `--root`/`--json`
  flags, `walk()` with a `SKIP_DIRS` set, exit 1 on error. Read `scripts/check-trace.mjs`
  (lines 28–210) before writing any CLI code and match its idioms.
- **Exported pure core:** `harvest`, `query`, `renderGraphMd`, and the helper functions are
  `export`ed. The CLI body runs only under a main guard:
  `import { pathToFileURL } from 'node:url'; if (import.meta.url === pathToFileURL(process.argv[1]).href) { main(); }`.
- **Determinism:** every serialized output (GRAPH.md, JSON) uses total ordering (features
  by `code`, paths lexicographic, refs by `code`). Never rely on Map/Set insertion order in
  output.
- **No new authoring burden (FGRAPH-9.5):** `harvest` reads only the *existing* content of
  `requirements.md`/`design.md`/`tasks.md`. It must never require a new field or annotation.
- **The spike is throwaway:** `scratchpad/surface-spike.mjs` is the reference for the regexes
  only. Do NOT import it, do NOT copy it into the repo; it stays in scratchpad and is
  discarded. Re-derive the logic against the requirements.
- **New glossary terms** (created in Task 1's `CONTEXT.md`): Surface, Surface manifest,
  Reverse index, Shared surface, Summary card. Use this vocabulary in code comments.

## File Structure

| File | Create/Modify | Responsibility |
|---|---|---|
| `scripts/check-graph.mjs` | Create | The engine: exported pure core (`normalizePath`, `isSourcePath`, `dedupeByFullest`, `classifyRole`, `harvest`, `renderGraphMd`, `query`) + `main`-guarded CLI (`--harvest`/`--query`/`--verify`). |
| `scripts/check-graph.test.mjs` | Create | Unit + integration tests for the core and CLI (fixtures in `os.tmpdir()`). |
| `scripts/check-graph.wiring.test.mjs` | Create | Regression test asserting the SKILL.md wiring markers exist. |
| `CONTEXT.md` | Create | Repo glossary: the five new terms. |
| `skills/discovery/brainstorm/SKILL.md` | Modify | Step 1 gains the graph dedup query + Done-when. |
| `skills/track/sync-spec/SKILL.md` | Modify | Step f regenerates + stages `GRAPH.md`. |
| `skills/execution/verify/SKILL.md` | Modify | Claim→evidence "Requirements met" row adds `check-graph --verify`. |
| `docs/specs/GRAPH.md` | Generated (not committed by hand) | Produced by `--harvest`; created the first time the engine runs. |

---

### Task 1: Path-token helpers + scaffold + glossary

**Files:**
- Create: `scripts/check-graph.mjs`
- Create: `scripts/check-graph.test.mjs`
- Create: `CONTEXT.md`
- Test: `scripts/check-graph.test.mjs`

**Interfaces:**
- Produces:
  - `normalizePath(token: string) → string` — strips backticks/quotes and trailing
    locators (`:12`, `:1,2`, `(~12-20)`).
  - `isSourcePath(token: string, cfg: {sourceRoots: string[], sourceExts: string[]}) → boolean`
    — true iff token has a known extension OR sits under a known root AND has a real
    filename segment.
  - `dedupeByFullest(paths: string[]) → string[]` — collapses basename + fuller path to the
    fullest form.

- [x] **Step 1: Create the glossary.** Create `CONTEXT.md`:

```markdown
# Glossary

Domain terms for this repo. Keep definitions tight; challenge fuzzy usage.

- **Surface** — the set of source files a feature owns or touches, derived from its
  `design.md` and `tasks.md`.
- **Surface manifest** — one feature's Surface, split into `owns` and `touches`.
- **Reverse index** — the inverse mapping: a source path → the features that reference it.
- **Shared surface** — a path referenced by two or more features; the duplication signal.
- **Summary card** — a bounded per-feature digest (code, name, owned paths, interfaces,
  out-of-scope) used to load a neighbor's essence without its full spec.
```

- [x] **Step 2: Write the failing test.** Create `scripts/check-graph.test.mjs`:

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { normalizePath, isSourcePath, dedupeByFullest } from './check-graph.mjs';

const CFG = {
  sourceRoots: ['src', 'src-tauri', 'tests', 'test', 'crates', 'app', 'lib', 'packages'],
  sourceExts: ['ts', 'tsx', 'js', 'jsx', 'mjs', 'rs', 'css', 'scss'],
};

test('[FGRAPH-1.3] normalizePath strips locators and quoting', () => {
  assert.equal(normalizePath('`Editor.tsx:208`'), 'Editor.tsx');
  assert.equal(normalizePath('App.tsx:127,172'), 'App.tsx');
  assert.equal(normalizePath('src/components/Editor.tsx (~208-221)'), 'src/components/Editor.tsx');
  assert.equal(normalizePath('"src/lib/x.ts"'), 'src/lib/x.ts');
});

test('[FGRAPH-1.5] isSourcePath accepts real paths, rejects junk', () => {
  assert.equal(isSourcePath('src/components/Editor.tsx', CFG), true);
  assert.equal(isSourcePath('raki-domain/src/inline.rs', CFG), true);
  assert.equal(isSourcePath('src-tauri/', CFG), false); // bare root, no filename
  assert.equal(isSourcePath('.spec.ts', CFG), false);   // bare extension, no name
  assert.equal(isSourcePath('the quick brown', CFG), false);
});

test('[FGRAPH-1.4] dedupeByFullest collapses basename into full path', () => {
  const out = dedupeByFullest(['Editor.tsx', 'src/components/Editor.tsx', 'src/lib/x.ts']);
  assert.deepEqual([...out].sort(), ['src/components/Editor.tsx', 'src/lib/x.ts']);
});
```

Run: `node --test scripts/check-graph.test.mjs` — expect: fails, cannot import from
`./check-graph.mjs` (module missing).

- [x] **Step 3: Implement the scaffold + helpers.** Create `scripts/check-graph.mjs`:

```js
#!/usr/bin/env node
/**
 * check-graph — horizontal feature-graph layer (sibling to check-trace).
 *
 * Harvests, from each feature's existing design.md/tasks.md (NO new authoring):
 *   - a Surface manifest  (files a feature owns/touches)
 *   - a Reverse index     (path -> [{code, role}])
 *   - Summary cards       (code, name, owns, interfaces, out-of-scope)
 *
 * Modes: --harvest (write <specsDir>/GRAPH.md) | --query (JSON overlaps) | --verify (lint).
 * Config: docs/agents/trace.json (shared specsDir; optional "graph" key).
 */
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

export const DEFAULTS = {
  specsDir: 'docs/specs',
  graph: {
    sourceRoots: ['src', 'src-tauri', 'tests', 'test', 'e2e', 'crates', 'app', 'lib', 'packages'],
    sourceExts: ['ts', 'tsx', 'js', 'jsx', 'mjs', 'cjs', 'rs', 'css', 'scss', 'go', 'py'],
    cardCap: 12,
  },
};

const EXT_RE = (exts) => new RegExp(`\\.(${exts.join('|')})$`);

export function normalizePath(token) {
  let t = String(token).replace(/[`'"()]/g, '').trim();
  t = t.replace(/\s*~?\d[\d,\s-]*$/, '');   // trailing "(~208-221)" tails after paren-strip
  t = t.replace(/:\d+(?:[,\d]*)?$/, '');     // trailing :208 or :127,172 locator
  return t.trim();
}

export function isSourcePath(token, cfg) {
  const t = token;
  if (!t || /\s/.test(t)) return false;
  const hasExt = EXT_RE(cfg.sourceExts).test(t);
  const seg = t.split('/');
  const filename = seg[seg.length - 1];
  const hasRealFilename = filename.length > 0 && /[A-Za-z0-9]/.test(filename) && !/^\.\w+$/.test(filename);
  const underRoot = cfg.sourceRoots.some((r) => t === r + '/' || t.startsWith(r + '/'));
  if (hasExt && hasRealFilename) return true;
  if (underRoot && hasRealFilename && EXT_RE(cfg.sourceExts).test(filename)) return true;
  return false;
}

export function dedupeByFullest(paths) {
  const uniq = [...new Set(paths)];
  const kept = [];
  for (const p of uniq) {
    const isBasenameOfAnother = uniq.some((q) => q !== p && q.endsWith('/' + p));
    if (!isBasenameOfAnother) kept.push(p);
  }
  return kept;
}

function main() {
  console.error('check-graph: CLI not yet implemented');
  process.exit(2);
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) main();
```

Run: `node --test scripts/check-graph.test.mjs` — expect: 3 tests pass.

- [x] **Step 4: Commit.**

`git commit -m "feat(check-graph): path-token helpers + scaffold + glossary" # trailers: Implements: FGRAPH-1.3, Implements: FGRAPH-1.4, Implements: FGRAPH-1.5`

_Requirements: FGRAPH-1.3, FGRAPH-1.4, FGRAPH-1.5_

---

### Task 2: Best-effort role classification

**Files:**
- Modify: `scripts/check-graph.mjs`
- Test: `scripts/check-graph.test.mjs`

**Interfaces:**
- Produces: `classifyRole(line: string, blockLabel: 'create'|'modify'|null) → 'owns'|'touches'`
  — a `create` block label OR a create/new verb ⇒ `owns`; otherwise `touches`.

- [x] **Step 1: Write the failing test.** Append to `scripts/check-graph.test.mjs`:

```js
import { classifyRole } from './check-graph.mjs';

test('[FGRAPH-1.6] classifyRole: create signal owns, else touches', () => {
  assert.equal(classifyRole('- Create: `src/x.ts` — new picker', null), 'owns');
  assert.equal(classifyRole('add a new file src/y.ts', null), 'owns');
  assert.equal(classifyRole('- Modify: `src/x.ts` (extract helper)', null), 'touches');
  assert.equal(classifyRole('reuse `src/x.ts` from the plugin', null), 'touches');
  assert.equal(classifyRole('`src/x.ts` is referenced here', 'create'), 'owns');  // block wins
  assert.equal(classifyRole('`src/x.ts` mentioned in prose', null), 'touches');   // safe default
});
```

Run: `node --test scripts/check-graph.test.mjs` — expect: import of `classifyRole` fails.

- [x] **Step 2: Implement.** Add to `scripts/check-graph.mjs` (before `main`):

```js
const OWN_HINT = /\b(create|new file|adds? a? ?new file|scaffold)\b|\badd(?:ing)?\b.*\bnew\b/i;
const CREATE_LABEL = /^\s*-?\s*create:/i;
const MODIFY_LABEL = /^\s*-?\s*modify:/i;

export function classifyRole(line, blockLabel) {
  if (blockLabel === 'create' || CREATE_LABEL.test(line)) return 'owns';
  if (blockLabel === 'modify' || MODIFY_LABEL.test(line)) return 'touches';
  if (OWN_HINT.test(line)) return 'owns';
  return 'touches';
}
```

Run: `node --test scripts/check-graph.test.mjs` — expect: all pass.

- [x] **Step 3: Commit.**

`git commit -m "feat(check-graph): best-effort role classification" # trailer: Implements: FGRAPH-1.6`

_Requirements: FGRAPH-1.6_

---

### Task 3: harvest() — manifest, reverse index, shared surface

**Files:**
- Modify: `scripts/check-graph.mjs`
- Test: `scripts/check-graph.test.mjs`

**Interfaces:**
- Consumes: `normalizePath`, `isSourcePath`, `dedupeByFullest`, `classifyRole`, `DEFAULTS`.
- Produces: `harvest(specsDir: string, cfg?) → Graph` where
  `Graph = { features: [{code, name, owns: string[], touches: string[], interfaces: string[], oos: string[]}], reverse: {[path]: [{code, role}]}, shared: [{path, refs: [{code, role}]}] }`.
  (Cards — `interfaces`/`oos` — are populated in Task 4; Task 3 fills `owns`/`touches` and
  leaves `interfaces: []`, `oos: []`.)

- [x] **Step 1: Write the failing test.** Append to `scripts/check-graph.test.mjs`:

```js
import { harvest } from './check-graph.mjs';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

function specFixture(features) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'check-graph-'));
  const specs = path.join(root, 'docs/specs');
  for (const f of features) {
    const dir = path.join(specs, f.slug);
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, 'requirements.md'),
      `# Requirements: ${f.name}\nFeature code: ${f.code}\nStatus: Approved\n\n## Out of Scope\n${(f.oos||[]).map(x=>`- ${x}`).join('\n')}\n`);
    if (f.design) fs.writeFileSync(path.join(dir, 'design.md'), f.design);
    if (f.tasks) fs.writeFileSync(path.join(dir, 'tasks.md'), f.tasks);
  }
  return specs;
}

test('[FGRAPH-1.1][FGRAPH-1.2] harvest builds owns/touches from design+tasks', () => {
  const specs = specFixture([
    { slug: 'a-base', code: 'BASE', name: 'Base',
      tasks: '**Files:**\n- Create: `src/core/engine.ts`\n- Create: `src/core/util.ts`\n' },
    { slug: 'b-ext', code: 'EXT', name: 'Extension',
      tasks: '**Files:**\n- Modify: `src/core/engine.ts` (extend)\n- Create: `src/ext/plugin.ts`\n' },
  ]);
  const g = harvest(specs);
  const base = g.features.find((f) => f.code === 'BASE');
  const ext = g.features.find((f) => f.code === 'EXT');
  assert.ok(base.owns.includes('src/core/engine.ts'));
  assert.ok(ext.touches.includes('src/core/engine.ts'));
  assert.ok(ext.owns.includes('src/ext/plugin.ts'));
});

test('[FGRAPH-2.1][FGRAPH-2.2][FGRAPH-2.3] reverse index + shared surface', () => {
  const specs = specFixture([
    { slug: 'a-base', code: 'BASE', name: 'Base', tasks: '- Create: `src/core/engine.ts`\n' },
    { slug: 'b-ext', code: 'EXT', name: 'Extension', tasks: '- Modify: `src/core/engine.ts`\n' },
  ]);
  const g = harvest(specs);
  assert.deepEqual(g.reverse['src/core/engine.ts'].map((r) => r.code).sort(), ['BASE', 'EXT']);
  const shared = g.shared.find((s) => s.path === 'src/core/engine.ts');
  assert.equal(shared.refs.length, 2, 'referenced by 2 features → shared');
});

test('[FGRAPH-9.1] a feature with only requirements.md yields an empty manifest, no error', () => {
  const specs = specFixture([{ slug: 'a', code: 'ONLY', name: 'Only' }]);
  const g = harvest(specs);
  const f = g.features.find((x) => x.code === 'ONLY');
  assert.deepEqual(f.owns, []);
  assert.deepEqual(f.touches, []);
});
```

Run: `node --test scripts/check-graph.test.mjs` — expect: import of `harvest` fails.

- [x] **Step 2: Implement `harvest`.** Add to `scripts/check-graph.mjs` (before `main`):

```js
const SKIP_DIRS = new Set(['node_modules', '.git', 'dist', 'build', 'target', 'coverage', '.next', '.skills', 'vendor']);
const BACKTICK_RE = /`([^`]+)`/g;
const WORD_RE = /[A-Za-z0-9_./-]+/g;

function walk(dir, predicate, out = []) {
  let entries;
  try { entries = fs.readdirSync(dir, { withFileTypes: true }); } catch { return out; }
  for (const e of entries) {
    if (e.name.startsWith('.') && e.name !== '.') continue;
    const full = path.join(dir, e.name);
    if (e.isDirectory()) { if (!SKIP_DIRS.has(e.name)) walk(full, predicate, out); }
    else if (predicate(full)) out.push(full);
  }
  return out;
}

function readMaybe(p) { try { return fs.readFileSync(p, 'utf8'); } catch { return null; } }

/** Extract normalized source paths (with roles) from one design.md/tasks.md body. */
function scanSurface(text, cfg) {
  const found = new Map(); // path -> role (owns beats touches)
  let blockLabel = null;
  for (const line of text.split('\n')) {
    if (/^\s*-?\s*create:/i.test(line)) blockLabel = 'create';
    else if (/^\s*-?\s*modify:/i.test(line)) blockLabel = 'modify';
    else if (/^\s*\*?\*?(files|interfaces|steps)\b/i.test(line)) blockLabel = null;
    const cands = new Set();
    for (const m of line.matchAll(BACKTICK_RE)) cands.add(m[1]);
    for (const m of line.matchAll(WORD_RE)) cands.add(m[0]);
    for (const c of cands) {
      const p = normalizePath(c);
      if (!isSourcePath(p, cfg.graph)) continue;
      const role = classifyRole(line, blockLabel);
      if (role === 'owns' || !found.has(p)) found.set(p, role);
    }
  }
  return found; // Map<path, role>
}

export function harvest(specsDir, cfg = DEFAULTS) {
  const features = [];
  if (!fs.existsSync(specsDir)) return { features, reverse: {}, shared: [] };
  const reqFiles = walk(specsDir, (p) => p.endsWith('requirements.md'));
  for (const req of reqFiles.sort()) {
    const text = fs.readFileSync(req, 'utf8');
    const code = (text.match(/^Feature code:\s*([A-Z][A-Z0-9]{1,11})/m) || [])[1];
    if (!code) continue;
    const name = (text.match(/^#\s*Requirements:\s*(.+)$/m) || [])[1]?.trim() || code;
    const dir = path.dirname(req);
    const surface = new Map();
    for (const f of ['design.md', 'tasks.md']) {
      const body = readMaybe(path.join(dir, f));
      if (!body) continue;
      for (const [p, role] of scanSurface(body, cfg)) {
        if (role === 'owns' || !surface.has(p)) surface.set(p, role);
      }
    }
    // basename/full dedup within this feature, keeping the winning role
    const fullest = new Set(dedupeByFullest([...surface.keys()]));
    const owns = [], touches = [];
    for (const p of fullest) (surface.get(p) === 'owns' ? owns : touches).push(p);
    features.push({ code, name, owns: owns.sort(), touches: touches.sort(), interfaces: [], oos: [] });
  }
  features.sort((a, b) => a.code.localeCompare(b.code));

  const reverse = {};
  for (const f of features) {
    for (const [p, role] of [...f.owns.map((p) => [p, 'owns']), ...f.touches.map((p) => [p, 'touches'])]) {
      (reverse[p] ||= []).push({ code: f.code, role });
    }
  }
  for (const p of Object.keys(reverse)) reverse[p].sort((a, b) => a.code.localeCompare(b.code));
  const shared = Object.keys(reverse).filter((p) => reverse[p].length >= 2).sort()
    .map((p) => ({ path: p, refs: reverse[p] }));
  return { features, reverse, shared };
}
```

Run: `node --test scripts/check-graph.test.mjs` — expect: all pass.

- [x] **Step 3: Commit.**

`git commit -m "feat(check-graph): harvest manifest + reverse index + shared surface" # trailers: Implements: FGRAPH-1.1, FGRAPH-1.2, FGRAPH-2.1, FGRAPH-2.2, FGRAPH-2.3, FGRAPH-9.1`

_Requirements: FGRAPH-1.1, FGRAPH-1.2, FGRAPH-2.1, FGRAPH-2.2, FGRAPH-2.3, FGRAPH-9.1_

---

### Task 4: Summary cards (interfaces + out-of-scope + cap)

**Files:**
- Modify: `scripts/check-graph.mjs` (extend `harvest`)
- Test: `scripts/check-graph.test.mjs`

**Interfaces:**
- Produces: `harvest` now fills each feature's `interfaces: string[]` (from `Interfaces:`
  blocks) and `oos: string[]` (from the `## Out of Scope` section), each capped at
  `cfg.graph.cardCap` with a trailing `…(+N more)` marker when truncated.

- [x] **Step 1: Write the failing test.** Append to `scripts/check-graph.test.mjs`:

```js
test('[FGRAPH-3.1][FGRAPH-3.2] card carries name, owns, and out-of-scope', () => {
  const specs = specFixture([{ slug: 'a', code: 'CARD', name: 'Card feature',
    oos: ['No time zones', 'No recurrence'],
    tasks: '- Create: `src/card.ts`\n' }]);
  const f = harvest(specs).features.find((x) => x.code === 'CARD');
  assert.equal(f.name, 'Card feature');
  assert.ok(f.owns.includes('src/card.ts'));
  assert.deepEqual(f.oos, ['No time zones', 'No recurrence']);
});

test('[FGRAPH-3.3] interfaces harvested best-effort from Interfaces: blocks', () => {
  const specs = specFixture([{ slug: 'a', code: 'IFACE', name: 'Iface',
    design: '**Interfaces:**\n- `applyChipEdit(view, action)`\n- `ChipEditAction` union\n' }]);
  const f = harvest(specs).features.find((x) => x.code === 'IFACE');
  assert.ok(f.interfaces.some((s) => s.includes('applyChipEdit')));
});

test('[FGRAPH-3.4] card lists are capped at cardCap', () => {
  const many = Array.from({ length: 20 }, (_, i) => `No feature number ${i}`);
  const specs = specFixture([{ slug: 'a', code: 'CAP', name: 'Cap', oos: many }]);
  const cfg = { ...DEFAULTS, graph: { ...DEFAULTS.graph, cardCap: 5 } };
  const f = harvest(specs, cfg).features.find((x) => x.code === 'CAP');
  assert.equal(f.oos.length, 6, '5 items + 1 elision marker');
  assert.match(f.oos[5], /\+15 more/);
});
```

Run: `node --test scripts/check-graph.test.mjs` — expect: the three new tests fail
(`interfaces` empty, `oos` empty, no cap).

- [x] **Step 2: Implement.** In `scripts/check-graph.mjs`, add helpers and call them inside
the `harvest` per-feature loop (replace the `interfaces: [], oos: []` literals):

```js
function capList(items, cap) {
  if (items.length <= cap) return items;
  return [...items.slice(0, cap), `…(+${items.length - cap} more)`];
}

function extractOutOfScope(reqText) {
  const m = reqText.match(/##\s*Out of Scope\s*\n([\s\S]*?)(\n##\s|\n#\s|$)/i);
  if (!m) return [];
  return [...m[1].matchAll(/^\s*[-*]\s+(.+?)\s*$/gm)].map((x) => x[1].replace(/\*\*/g, '').trim());
}

function extractInterfaces(bodies) {
  const out = [];
  for (const body of bodies) {
    if (!body) continue;
    const re = /^\s*\*?\*?interfaces:?\*?\*?\s*$/im;
    const lines = body.split('\n');
    for (let i = 0; i < lines.length; i++) {
      if (!re.test(lines[i])) continue;
      for (let j = i + 1; j < lines.length && /^\s*[-*]\s+/.test(lines[j]); j++) {
        out.push(lines[j].replace(/^\s*[-*]\s+/, '').replace(/`/g, '').trim());
      }
    }
  }
  return out;
}
```

Then in the per-feature loop, after computing `owns`/`touches`, replace the `features.push`
with:

```js
    const designBody = readMaybe(path.join(dir, 'design.md'));
    const tasksBody = readMaybe(path.join(dir, 'tasks.md'));
    const cap = cfg.graph.cardCap;
    features.push({
      code, name,
      owns: capList(owns.sort(), cap),
      touches: capList(touches.sort(), cap),
      interfaces: capList(extractInterfaces([designBody, tasksBody]), cap),
      oos: capList(extractOutOfScope(text), cap),
    });
```

Note: `reverse`/`shared` must be built from the *uncapped* owns/touches — hoist the raw
arrays before capping, or build `reverse` from a parallel uncapped list, so a 13th shared
file is never dropped from the index. Keep the capped values only on the card fields.

Run: `node --test scripts/check-graph.test.mjs` — expect: all pass.

- [x] **Step 3: Commit.**

`git commit -m "feat(check-graph): summary cards with interfaces, out-of-scope, cap" # trailers: Implements: FGRAPH-3.1, FGRAPH-3.2, FGRAPH-3.3, FGRAPH-3.4`

_Requirements: FGRAPH-3.1, FGRAPH-3.2, FGRAPH-3.3, FGRAPH-3.4_

---

### Task 5: renderGraphMd() — deterministic GRAPH.md

**Files:**
- Modify: `scripts/check-graph.mjs`
- Test: `scripts/check-graph.test.mjs`

**Interfaces:**
- Produces: `renderGraphMd(graph: Graph) → string` — a deterministic markdown document:
  a generated-banner, a `## Cards` section (one `###` block per feature), and a
  `## Shared surface` table. Byte-identical across runs on identical input.

- [x] **Step 1: Write the failing test.** Append to `scripts/check-graph.test.mjs`:

```js
import { renderGraphMd } from './check-graph.mjs';

test('[FGRAPH-4.2] renderGraphMd is deterministic and banner-marked', () => {
  const specs = specFixture([
    { slug: 'b', code: 'BBB', name: 'B', tasks: '- Create: `src/b.ts`\n- Modify: `src/shared.ts`\n' },
    { slug: 'a', code: 'AAA', name: 'A', tasks: '- Create: `src/shared.ts`\n' },
  ]);
  const g = harvest(specs);
  const once = renderGraphMd(g);
  const twice = renderGraphMd(harvest(specs));
  assert.equal(once, twice, 'identical input → byte-identical output');
  assert.match(once, /GENERATED/);
  assert.ok(once.indexOf('AAA') < once.indexOf('BBB'), 'cards ordered by code');
  assert.match(once, /src\/shared\.ts.*AAA:owns.*BBB:touches/s);
});

test('[FGRAPH-9.2] empty specs render a well-formed empty graph', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'check-graph-empty-'));
  const g = harvest(path.join(root, 'docs/specs'));
  const md = renderGraphMd(g);
  assert.match(md, /GENERATED/);
  assert.match(md, /## Cards/);
});
```

Run: `node --test scripts/check-graph.test.mjs` — expect: import of `renderGraphMd` fails.

- [x] **Step 2: Implement.** Add to `scripts/check-graph.mjs`:

```js
export function renderGraphMd(graph) {
  const L = [];
  L.push('# Feature Graph');
  L.push('');
  L.push('<!-- GENERATED by `check-graph --harvest`. Do not edit by hand; regenerated by sync-spec. -->');
  L.push('');
  L.push('## Cards');
  L.push('');
  for (const f of graph.features) {
    L.push(`### ${f.code} — ${f.name}`);
    L.push(`- owns: ${f.owns.join(', ') || '—'}`);
    L.push(`- touches: ${f.touches.join(', ') || '—'}`);
    L.push(`- interfaces: ${f.interfaces.join(', ') || '—'}`);
    L.push(`- out-of-scope: ${f.oos.join(' | ') || '—'}`);
    L.push('');
  }
  L.push('## Shared surface');
  L.push('');
  L.push('| Path | Features |');
  L.push('|---|---|');
  for (const s of graph.shared) {
    L.push(`| ${s.path} | ${s.refs.map((r) => `${r.code}:${r.role}`).join(', ')} |`);
  }
  L.push('');
  return L.join('\n');
}
```

Run: `node --test scripts/check-graph.test.mjs` — expect: all pass.
(FGRAPH-4.3 — INDEX.md never written — is guaranteed structurally: `renderGraphMd` returns
a string and touches no file; the CLI in Task 7 writes only GRAPH.md. Asserted in Task 7.)

- [x] **Step 3: Commit.**

`git commit -m "feat(check-graph): deterministic GRAPH.md renderer" # trailers: Implements: FGRAPH-4.2, FGRAPH-4.3, FGRAPH-9.2`

_Requirements: FGRAPH-4.2, FGRAPH-4.3, FGRAPH-9.2_

---

### Task 6: query() — overlaps by path and keyword, ranked

**Files:**
- Modify: `scripts/check-graph.mjs`
- Test: `scripts/check-graph.test.mjs`

**Interfaces:**
- Produces: `query(graph: Graph, {paths?: string[], keywords?: string[]}) → {code, name, card, overlapPaths: string[]}[]`
  — features whose surface intersects `paths` (via `reverse`) or whose `name`/`oos` match a
  keyword (case-insensitive substring), ranked by `overlapPaths.length` descending. Each
  result carries the feature's full card.

- [x] **Step 1: Write the failing test.** Append to `scripts/check-graph.test.mjs`:

```js
import { query } from './check-graph.mjs';

test('[FGRAPH-5.1][FGRAPH-5.3] query by path returns ranked overlapping features', () => {
  const specs = specFixture([
    { slug: 'a', code: 'AAA', name: 'A', tasks: '- Create: `src/x.ts`\n- Create: `src/y.ts`\n' },
    { slug: 'b', code: 'BBB', name: 'B', tasks: '- Create: `src/y.ts`\n' },
  ]);
  const g = harvest(specs);
  const res = query(g, { paths: ['src/x.ts', 'src/y.ts'] });
  assert.equal(res[0].code, 'AAA', 'AAA overlaps 2 → ranked first');
  assert.equal(res[1].code, 'BBB', 'BBB overlaps 1');
  assert.ok(res[0].card, 'result carries the card');
});

test('[FGRAPH-5.2] query by keyword matches name and out-of-scope', () => {
  const specs = specFixture([{ slug: 'a', code: 'PICK', name: 'Picker widget',
    oos: ['No time zones'], tasks: '- Create: `src/p.ts`\n' }]);
  const g = harvest(specs);
  assert.equal(query(g, { keywords: ['picker'] })[0].code, 'PICK');
  assert.equal(query(g, { keywords: ['time zone'] })[0].code, 'PICK');
  assert.deepEqual(query(g, { keywords: ['nonexistent'] }), []);
});
```

Run: `node --test scripts/check-graph.test.mjs` — expect: import of `query` fails.

- [x] **Step 2: Implement.** Add to `scripts/check-graph.mjs`:

```js
export function query(graph, { paths = [], keywords = [] } = {}) {
  const pathSet = new Set(paths);
  const kws = keywords.map((k) => k.toLowerCase()).filter(Boolean);
  const scored = new Map(); // code -> {feature, overlapPaths:Set}
  const bump = (code) => {
    if (!scored.has(code)) {
      const feature = graph.features.find((f) => f.code === code);
      scored.set(code, { feature, overlapPaths: new Set() });
    }
    return scored.get(code);
  };
  for (const p of pathSet) for (const ref of graph.reverse[p] || []) bump(ref.code).overlapPaths.add(p);
  for (const f of graph.features) {
    const hay = (f.name + ' ' + f.oos.join(' ')).toLowerCase();
    if (kws.some((k) => hay.includes(k))) bump(f.code);
  }
  return [...scored.values()]
    .map(({ feature, overlapPaths }) => ({
      code: feature.code, name: feature.name, card: feature,
      overlapPaths: [...overlapPaths].sort(),
    }))
    .sort((a, b) => b.overlapPaths.length - a.overlapPaths.length || a.code.localeCompare(b.code));
}
```

Run: `node --test scripts/check-graph.test.mjs` — expect: all pass.

- [x] **Step 3: Commit.**

`git commit -m "feat(check-graph): ranked query by path and keyword" # trailers: Implements: FGRAPH-5.1, FGRAPH-5.2, FGRAPH-5.3`

_Requirements: FGRAPH-5.1, FGRAPH-5.2, FGRAPH-5.3_

---

### Task 7: CLI — --harvest, --query, config, main guard

**Files:**
- Modify: `scripts/check-graph.mjs` (replace the stub `main`)
- Test: `scripts/check-graph.test.mjs` (integration, `spawnSync`)

**Interfaces:**
- Consumes: `harvest`, `renderGraphMd`, `query`, `DEFAULTS`.
- Produces: CLI `node check-graph.mjs [--harvest|--query|--verify] [--root R] [--json] [--path P]... [--keyword K]...`.
  `--harvest` writes `<specsDir>/GRAPH.md`. `--query` prints the `query` result as JSON to
  stdout. `loadConfig(root)` reads `docs/agents/trace.json` (optional), merging `graph`.

- [x] **Step 1: Write the failing test.** Append to `scripts/check-graph.test.mjs`:

```js
import { spawnSync } from 'node:child_process';
const CLI = path.join(import.meta.dirname, 'check-graph.mjs');
function cliFixture(features) { return path.dirname(path.dirname(specFixture(features))); } // repo root
function runCli(root, args) {
  const r = spawnSync('node', [CLI, ...args, '--root', root], { encoding: 'utf8' });
  return { code: r.status, out: r.stdout, err: r.stderr };
}

test('[FGRAPH-4.1][FGRAPH-4.3] --harvest writes GRAPH.md and leaves INDEX.md untouched', () => {
  const root = cliFixture([{ slug: 'a', code: 'AAA', name: 'A', tasks: '- Create: `src/a.ts`\n' }]);
  fs.writeFileSync(path.join(root, 'docs/specs/INDEX.md'), 'ORIGINAL');
  const { code } = runCli(root, ['--harvest']);
  assert.equal(code, 0);
  assert.match(fs.readFileSync(path.join(root, 'docs/specs/GRAPH.md'), 'utf8'), /AAA/);
  assert.equal(fs.readFileSync(path.join(root, 'docs/specs/INDEX.md'), 'utf8'), 'ORIGINAL');
});

test('[FGRAPH-5.4][FGRAPH-5.5] --query emits fresh JSON to stdout', () => {
  const root = cliFixture([{ slug: 'a', code: 'AAA', name: 'A', tasks: '- Create: `src/a.ts`\n' }]);
  // No GRAPH.md written; query must still work (fresh harvest).
  const { code, out } = runCli(root, ['--query', '--path', 'src/a.ts', '--json']);
  assert.equal(code, 0);
  const parsed = JSON.parse(out);
  assert.equal(parsed[0].code, 'AAA');
});

test('[FGRAPH-9.3] missing trace.json falls back to docs/specs', () => {
  const root = cliFixture([{ slug: 'a', code: 'AAA', name: 'A', tasks: '- Create: `src/a.ts`\n' }]);
  assert.equal(fs.existsSync(path.join(root, 'docs/agents/trace.json')), false);
  assert.equal(runCli(root, ['--harvest']).code, 0);
});
```

(FGRAPH-5.6 — reads only markdown, no network/build — holds by construction: `harvest`
does only `fs.readFileSync`. No separate assertion.)

Run: `node --test scripts/check-graph.test.mjs` — expect: the CLI tests fail (stub exits 2).

- [x] **Step 2: Implement the CLI.** In `scripts/check-graph.mjs`, replace `main` and add
`loadConfig`:

```js
export function loadConfig(root) {
  const p = path.join(root, 'docs/agents/trace.json');
  if (!fs.existsSync(p)) return DEFAULTS;
  try {
    const user = JSON.parse(fs.readFileSync(p, 'utf8'));
    return { ...DEFAULTS, ...user, graph: { ...DEFAULTS.graph, ...(user.graph || {}) } };
  } catch (e) {
    console.error(`check-graph: could not parse ${p}: ${e.message}`);
    process.exit(1);
  }
}

function collectFlag(args, name) {
  const out = [];
  for (let i = 0; i < args.length; i++) if (args[i] === name) out.push(args[i + 1]);
  return out;
}

function main() {
  const args = process.argv.slice(2);
  const rootIdx = args.indexOf('--root');
  const root = rootIdx !== -1 ? path.resolve(args[rootIdx + 1]) : process.cwd();
  const asJson = args.includes('--json');
  const cfg = loadConfig(root);
  const specsDir = path.join(root, cfg.specsDir);

  if (args.includes('--query')) {
    const graph = harvest(specsDir, cfg);
    const res = query(graph, { paths: collectFlag(args, '--path'), keywords: collectFlag(args, '--keyword') });
    console.log(asJson ? JSON.stringify(res, null, 2) : res.map((r) => `${r.code} (${r.overlapPaths.length})`).join('\n'));
    process.exit(0);
  }
  if (args.includes('--verify')) { runVerify(root, cfg, specsDir, asJson); return; } // Task 8
  // default: --harvest
  const graph = harvest(specsDir, cfg);
  if (!fs.existsSync(specsDir)) { console.error(`check-graph: no specs dir at ${cfg.specsDir}`); process.exit(0); }
  fs.writeFileSync(path.join(specsDir, 'GRAPH.md'), renderGraphMd(graph));
  console.log(`check-graph: wrote GRAPH.md — ${graph.features.length} features, ${graph.shared.length} shared paths.`);
  process.exit(0);
}
```

Add a temporary stub so the file parses before Task 8 lands `runVerify`:

```js
function runVerify() { console.error('check-graph: --verify implemented in Task 8'); process.exit(2); }
```

Run: `node --test scripts/check-graph.test.mjs` — expect: all pass (verify tests arrive in
Task 8).

- [x] **Step 3: Commit.**

`git commit -m "feat(check-graph): CLI harvest + query + config" # trailers: Implements: FGRAPH-4.1, FGRAPH-5.4, FGRAPH-5.5, FGRAPH-5.6, FGRAPH-9.3`

_Requirements: FGRAPH-4.1, FGRAPH-5.4, FGRAPH-5.5, FGRAPH-5.6, FGRAPH-9.3_

---

### Task 8: CLI --verify — freshness + unregistered-code lint

**Files:**
- Modify: `scripts/check-graph.mjs` (replace the `runVerify` stub)
- Test: `scripts/check-graph.test.mjs`

**Interfaces:**
- Produces: `runVerify(root, cfg, specsDir, asJson)` — exit 1 if committed `GRAPH.md`
  differs from a fresh render, or if any harvested feature code is absent from `INDEX.md`;
  exit 0 when fresh and all codes registered.

- [x] **Step 1: Write the failing test.** Append to `scripts/check-graph.test.mjs`:

```js
test('[FGRAPH-6.1][FGRAPH-6.2] --verify fails on stale, passes when fresh', () => {
  const root = cliFixture([{ slug: 'a', code: 'AAA', name: 'A', tasks: '- Create: `src/a.ts`\n' }]);
  fs.writeFileSync(path.join(root, 'docs/specs/INDEX.md'), '| AAA | A | ./a/ | Approved |');
  assert.equal(runCli(root, ['--verify']).code, 1, 'no GRAPH.md yet → stale');
  runCli(root, ['--harvest']);
  assert.equal(runCli(root, ['--verify']).code, 0, 'after harvest → fresh');
  fs.appendFileSync(path.join(root, 'docs/specs/GRAPH.md'), '\nhand edit\n');
  assert.equal(runCli(root, ['--verify']).code, 1, 'hand edit → stale again');
});

test('[FGRAPH-6.3] --verify fails on a code absent from INDEX.md', () => {
  const root = cliFixture([{ slug: 'a', code: 'GHOST', name: 'Ghost', tasks: '- Create: `src/g.ts`\n' }]);
  fs.writeFileSync(path.join(root, 'docs/specs/INDEX.md'), '| OTHER | x | ./x/ | Draft |');
  runCli(root, ['--harvest']);
  const { code, err, out } = runCli(root, ['--verify']);
  assert.equal(code, 1);
  assert.match(err + out, /GHOST/);
});
```

Run: `node --test scripts/check-graph.test.mjs` — expect: verify tests fail (stub exits 2).

- [x] **Step 2: Implement.** In `scripts/check-graph.mjs`, replace the `runVerify` stub:

```js
function runVerify(root, cfg, specsDir, asJson) {
  const errors = [];
  const graph = harvest(specsDir, cfg);
  const graphMd = path.join(specsDir, 'GRAPH.md');
  const committed = fs.existsSync(graphMd) ? fs.readFileSync(graphMd, 'utf8') : null;
  const fresh = renderGraphMd(graph);
  if (committed !== fresh) errors.push('GRAPH.md is stale — run `check-graph --harvest` and commit the result.');

  const indexMd = path.join(specsDir, 'INDEX.md');
  const indexText = fs.existsSync(indexMd) ? fs.readFileSync(indexMd, 'utf8') : '';
  for (const f of graph.features) {
    const registered = new RegExp(`\\b${f.code}\\b`).test(indexText);
    if (!registered) errors.push(`E: feature code ${f.code} is not registered in INDEX.md`);
  }

  if (asJson) console.log(JSON.stringify({ errors }, null, 2));
  else { console.log(`check-graph --verify: ${errors.length ? 'FAIL' : 'OK'}`); for (const e of errors) console.log(`  ${e}`); }
  process.exit(errors.length ? 1 : 0);
}
```

Run: `node --test scripts/check-graph.test.mjs` — expect: all pass.

- [x] **Step 3: Commit.**

`git commit -m "feat(check-graph): --verify freshness + unregistered-code lint" # trailers: Implements: FGRAPH-6.1, FGRAPH-6.2, FGRAPH-6.3`

_Requirements: FGRAPH-6.1, FGRAPH-6.2, FGRAPH-6.3_

---

### Task 9: Guard tests — check-trace unaffected, no authoring burden

**Files:**
- Modify: `scripts/check-graph.test.mjs`
- Test: `scripts/check-graph.test.mjs`

**Interfaces:**
- Consumes: existing `scripts/check-trace.test.mjs`, `harvest`.

- [x] **Step 1: Write the tests (these should PASS immediately — they assert guards hold).**
Append to `scripts/check-graph.test.mjs`:

```js
test('[FGRAPH-9.4] the existing check-trace test suite still passes', () => {
  const r = spawnSync('node', ['--test', path.join(import.meta.dirname, 'check-trace.test.mjs')], { encoding: 'utf8' });
  assert.equal(r.status, 0, 'check-graph must not disturb check-trace: ' + r.stdout + r.stderr);
});

test('[FGRAPH-9.5] harvest needs no new fields — vanilla specs yield a non-empty graph', () => {
  // A spec authored to the STANDARD templates only (no graph-specific annotations).
  const specs = specFixture([{ slug: 'plain', code: 'PLAIN', name: 'Plain feature',
    design: '### Component\nSatisfies: PLAIN-1.1\nLives in `src/plain/core.ts`.\n',
    tasks: '**Files:**\n- Create: `src/plain/core.ts`\n- Modify: `src/plain/wire.ts`\n' }]);
  const f = harvest(specs).features.find((x) => x.code === 'PLAIN');
  assert.ok(f.owns.length + f.touches.length >= 2, 'surface harvested from standard specs alone');
});
```

Run: `node --test scripts/check-graph.test.mjs` — expect: both pass. If FGRAPH-9.4 fails,
check-graph has coupled to check-trace — stop and fix the coupling, do not edit the test.

- [x] **Step 2: Commit.**

`git commit -m "test(check-graph): guard check-trace and no-authoring-burden" # trailers: Guards: FGRAPH-9.4, Guards: FGRAPH-9.5`

_Requirements: FGRAPH-9.4, FGRAPH-9.5_

---

### Task 10: Skill wiring + wiring regression test

**Files:**
- Create: `scripts/check-graph.wiring.test.mjs`
- Modify: `skills/discovery/brainstorm/SKILL.md`
- Modify: `skills/track/sync-spec/SKILL.md`
- Modify: `skills/execution/verify/SKILL.md`
- Test: `scripts/check-graph.wiring.test.mjs`

**Interfaces:**
- Consumes: the three SKILL.md files (asserts durable wiring markers exist in them).

- [x] **Step 1: Write the failing test.** Create `scripts/check-graph.wiring.test.mjs`:

```js
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const repo = path.dirname(import.meta.dirname);
const read = (rel) => fs.readFileSync(path.join(repo, rel), 'utf8');

test('[FGRAPH-7.1][FGRAPH-7.2][FGRAPH-7.5][FGRAPH-9.6] brainstorm wires the graph query', () => {
  const t = read('skills/discovery/brainstorm/SKILL.md');
  assert.match(t, /check-graph(?:\.mjs)? --query/, 'FGRAPH-7.1: brainstorm calls the query');
  assert.match(t, /card/i, 'FGRAPH-7.2: presents cards');
  assert.match(t, /unavailable|fail-open|continue/i, 'FGRAPH-7.5/9.6: fail-open note');
});

test('[FGRAPH-7.3][FGRAPH-7.4] brainstorm step-1 Done-when states overlaps', () => {
  const t = read('skills/discovery/brainstorm/SKILL.md');
  assert.match(t, /share[sd]? .*surface|no existing feature/i, 'FGRAPH-7.3/7.4: state overlaps or none');
});

test('[FGRAPH-8.1][FGRAPH-8.2] sync-spec regenerates and stages GRAPH.md', () => {
  const t = read('skills/track/sync-spec/SKILL.md');
  assert.match(t, /check-graph(?:\.mjs)? --harvest/, 'FGRAPH-8.1: regenerates');
  assert.match(t, /GRAPH\.md/, 'FGRAPH-8.2: stages GRAPH.md into the commit');
});

test('[FGRAPH-6.4] verify runs check-graph --verify', () => {
  assert.match(read('skills/execution/verify/SKILL.md'), /check-graph --verify/);
});
```

Run: `node --test scripts/check-graph.wiring.test.mjs` — expect: all four fail (markers
absent).

- [x] **Step 2: Wire brainstorm.** In `skills/discovery/brainstorm/SKILL.md`, step 1
("Explore project context"), after the scan-subagent sentence, add:

```markdown
Then run the feature-graph dedup check: `node scripts/check-graph.mjs --query --json`
passing the scan's candidate files as `--path` and the idea's key terms as `--keyword`.
Present any returned features as their summary **cards** (not full specs) — each card's
owned paths and Out-of-Scope list show what the neighbor already covers. If `check-graph`
is absent or errors, note "automated overlap check unavailable" and continue with manual
exploration (this also covers harnesses without subagents — query on the idea's terms
directly).
```

And extend the step-1 **Done when** to: "… and you have stated which existing features
share this idea's surface and how the new idea differs (citing feature codes), or that no
existing feature shares its surface."

- [x] **Step 3: Wire sync-spec.** In `skills/track/sync-spec/SKILL.md`, step **f (After
picture)**, add after the check-trace re-run:

```markdown
Then regenerate the feature graph: `node scripts/check-graph.mjs --harvest`. If `GRAPH.md`
changed, stage it into this sync-spec commit alongside the `Status:`/`INDEX.md` edits so
the committed graph tracks the triad.
```

- [x] **Step 4: Wire verify.** In `skills/execution/verify/SKILL.md`, the claim→evidence
table "Requirements met" row, change the evidence cell to: ``check-trace` **and**
`check-graph --verify` pass AND each acceptance criterion checked off individually against
observed behavior`.

Run: `node --test scripts/check-graph.wiring.test.mjs` — expect: all pass.

- [x] **Step 5: Commit.**

`git commit -m "feat(fgraph): wire feature graph into brainstorm, sync-spec, verify" # trailers: Implements: FGRAPH-6.4, FGRAPH-7.1, FGRAPH-7.2, FGRAPH-7.3, FGRAPH-7.4, FGRAPH-7.5, FGRAPH-8.1, FGRAPH-8.2, FGRAPH-9.6`

_Requirements: FGRAPH-6.4, FGRAPH-7.1, FGRAPH-7.2, FGRAPH-7.3, FGRAPH-7.4, FGRAPH-7.5, FGRAPH-8.1, FGRAPH-8.2, FGRAPH-9.6_

---

### Task 11: Generate the graph + mark the spec Implemented

**Files:**
- Generated: `docs/specs/GRAPH.md`
- Modify: `docs/specs/2026-07-09-feature-graph/requirements.md` (Status)
- Modify: `docs/specs/2026-07-09-feature-graph/design.md` (Status)
- Modify: `docs/specs/INDEX.md` (FGRAPH row → Implemented)

**Interfaces:** none (integration/cleanup).

- [x] **Step 1: Generate the committed graph.** Run
`node scripts/check-graph.mjs --harvest` at the repo root. Confirm `docs/specs/GRAPH.md`
now exists and contains an `FGRAPH` card. Run `node scripts/check-graph.mjs --verify` —
expect exit 0.
- [x] **Step 2: Full suite green.** Run
`node --test scripts/check-graph.test.mjs scripts/check-graph.wiring.test.mjs scripts/check-trace.test.mjs`
— expect all pass. Run `node scripts/check-trace.mjs` — expect no new errors.
- [x] **Step 3: Confirm the spike is gone.** Verify `scratchpad/surface-spike.mjs` was
never copied into the repo (`git ls-files | grep surface-spike` returns nothing). The
scratchpad copy is throwaway and left untracked.
- [x] **Step 4: Transition status** (this is what makes E2 apply — every FGRAPH ID must now
have a covering test). Set `Status: Implemented` in `requirements.md` and `design.md`, and
update the FGRAPH row in `docs/specs/INDEX.md` to `Implemented`. Run
`node scripts/check-trace.mjs` — expect: zero E2 errors for FGRAPH (every ID has a tagged
test).
- [x] **Step 5: Commit.**

`git commit -m "chore(fgraph): generate GRAPH.md, mark FGRAPH Implemented"`

_Requirements: (integration — no new IDs; closes out FGRAPH coverage)_

---

## Task 12: Distribution — vendor the linters and wire setup-repo (Story 11)

**Files:**
- Create: `scripts/vendor-linters.mjs`, `scripts/vendor-linters.test.mjs`
- Modify: `scripts/check-graph.mjs` (symlink-safe entry-point guard), `scripts/check-trace.mjs` (stamp)
- Modify: `scripts/check-graph.wiring.test.mjs`
- Modify: `templates/agents/project.md`, `templates/githooks/pre-push`
- Modify: `skills/setup/setup-repo/SKILL.md`, `skills/discovery/brainstorm/SKILL.md`,
  `skills/review/code-review/SKILL.md`, `skills/execution/verify/SKILL.md`

**Interfaces:**
- `computeStamp(src: string) → string` — 12-hex sha256 of the body, stamp line excluded
- `readStamp(src: string) → {name, digest} | null`
- `restamp(src: string, name: string) → string` — idempotent
- `install(from, to, {scriptsDir}) → {name, dest, digest, action}[]`
- `checkDrift(from, to, {scriptsDir}) → {name, status, expected, found}[]` — status is `ok`|`missing`|`outdated`|`modified`
- CLI: `vendor-linters.mjs (--install|--check|--stamp) [--from R] [--to R] [--scripts-dir D]`

- [x] **Step 1: Stamp the linters (RED→GREEN).** Assert each of `check-graph.mjs` /
`check-trace.mjs` carries `// @skills-linter: <name> sha256:<12hex>` matching an
independently-computed `node:crypto` digest of its body. Add the stamp lines below the shebang.
- [x] **Step 2: `vendor-linters.mjs` (RED→GREEN).** E2E seam: scratch skill-set root + scratch
consumer repo. Cover install byte-identity, a vendored linter that actually *runs*, and the four
drift verdicts — `missing`, `outdated` (the bot-repo case), `modified` (hand-edited, stamp
untouched), `ok`. `checkDrift` must not mutate the consumer repo.
- [x] **Step 3: Fix the entry-point guard.** The E2E run exposed
`import.meta.url === pathToFileURL(process.argv[1]).href` failing under a symlinked path
(macOS `/var` → `/private/var`): `main()` never ran, so the CLI printed nothing and exited **0**.
Compare `fs.realpathSync` of both sides, and guard `argv[1] === undefined`. Re-stamp after.
- [x] **Step 4: Templates (RED→GREEN).** Graph row in `templates/agents/project.md`;
`check-graph.mjs --verify` in `templates/githooks/pre-push`.
- [x] **Step 5: setup-repo wiring (RED→GREEN).** Vendoring + drift-report step; graph lint in the
existing-CI opt-in and the pre-push fill; proving gate seeds `GRAPH.md` and classifies a dead
`check-graph` as a wiring failure.
- [x] **Step 6: Loud-once remedy (RED→GREEN).** brainstorm + code-review name `setup-repo` when
`check-graph` is *absent*, once per session, still failing open. Fix `verify/SKILL.md`'s
nonexistent bare `check-graph` binary to `node scripts/check-graph.mjs --verify`, and retarget the
wiring assertion that had enshrined the broken spelling.
- [x] **Step 7: Mutation-check every new test.** For each: revert the behavior in a scratch copy,
confirm the mapped test fails. The FGRAPH-11.14 guard initially survived — its fixture was an
empty dir, so `check-trace` early-exited and both copies trivially agreed. Rebuilt on a real
spec + covering test; its fixture requirement ID is assembled at runtime so this file's own
string does not fire a bogus E1.
- [x] **Step 8: Gates.** `node --test scripts/*.test.mjs` (74 pass) and `node scripts/check-trace.mjs`
(exit 0). Note the suite command: `node --test scripts/` runs `check-trace.mjs` *as* a test file.

_Requirements: FGRAPH-11.1, FGRAPH-11.2, FGRAPH-11.3, FGRAPH-11.4, FGRAPH-11.5, FGRAPH-11.6, FGRAPH-11.7, FGRAPH-11.8, FGRAPH-11.9, FGRAPH-11.10, FGRAPH-11.11, FGRAPH-11.12, FGRAPH-11.13, FGRAPH-11.14_

---

### Task 12: Harvest-quality amendment (tier-1, post-ship)

Added after dogfooding `check-graph --harvest` on the bot repo's 4 real features surfaced
four harvest-quality defects. Built as one `amend` via `tdd` (not discrete planned tasks);
each criterion carries a `[FGRAPH-N.M]` test in `scripts/check-graph.test.mjs`.

**Files:**
- Modify: `scripts/check-graph.mjs` (isSourcePath glob reject; scanSurface command-line filter + anchored `CMD_LINE_RE`; global cross-feature `canon` map in `harvest`; lean `extractInterfaces`)
- Test: `scripts/check-graph.test.mjs`

**Delivered (test-first, all tagged):**
- [x] **FGRAPH-1.7** reject glob tokens (`e2e/*.spec.ts`) — `[FGRAPH-1.7]`
- [x] **FGRAPH-1.8** exclude paths appearing only in command-invocation lines (anchored) — `[FGRAPH-1.8]`
- [x] **FGRAPH-1.9** guard: unfenced Files/Create/Modify bullets + prose backticks still harvested (incl. command-word-as-prose) — `[FGRAPH-1.9]`
- [x] **FGRAPH-2.4** cross-feature basename↔fullpath merge in reverse index/shared surface — `[FGRAPH-2.4]`
- [x] **FGRAPH-2.5** guard: CHIPUI↔INLTASK-style shared surface still detected — `[FGRAPH-2.5]`
- [x] **FGRAPH-3.5** interfaces as short single-line entries (drop labels/nesting/prose) — `[FGRAPH-3.5]`
- [x] **FGRAPH-4.4** guard: GRAPH.md stays deterministic/byte-stable — `[FGRAPH-4.4]`

Commits: `31df422` (amendment), `72225b9` (anchor command detection). Acceptance: re-harvested
the bot's 4 features; all four noise classes gone, shared-surface table clean.

_Requirements: FGRAPH-1.7, FGRAPH-1.8, FGRAPH-1.9, FGRAPH-2.4, FGRAPH-2.5, FGRAPH-3.5, FGRAPH-4.4_

---

### Task 13: Code-review duplication check — Story 10 (tier-1, post-ship)

The 4th graph consumer, reclaiming Out-of-Scope item #4. Advisory: code-review queries the
graph with the diff's changed files and injects overlapping features' cards into the Spec
subagent's brief; the reviewer flags reuse-misses citing the neighbor's feature code. Built
as one wiring change via `tdd`; guarded by a wiring regression test.

**Files:**
- Modify: `skills/review/code-review/SKILL.md` (new `## 3a` graph-query step; Spec-subagent brief gains neighbor cards + reuse-miss directive)
- Test: `scripts/check-graph.wiring.test.mjs` (asserts the code-review wiring markers)

**Delivered (test-first, all tagged in `check-graph.wiring.test.mjs`):**
- [x] **FGRAPH-10.1** code-review queries `check-graph --query` with the diff's changed source files — `[FGRAPH-10.1]`
- [x] **FGRAPH-10.2** overlapping features' cards injected into the Spec subagent brief — `[FGRAPH-10.2]`
- [x] **FGRAPH-10.3** Spec brief directs reuse-miss findings citing the neighbor's feature code — `[FGRAPH-10.3]`
- [x] **FGRAPH-10.4** no overlap → state none, inject nothing — `[FGRAPH-10.4]`
- [x] **FGRAPH-10.5** fail-open when check-graph unavailable — `[FGRAPH-10.5]`
- [x] **FGRAPH-10.6** guard: Standards+Spec two-axis review unchanged — `[FGRAPH-10.6]`

Commit: `dba5244`. Reviewed clean (two-axis structure + "never pre-judge" rule verified untouched).

_Requirements: FGRAPH-10.1, FGRAPH-10.2, FGRAPH-10.3, FGRAPH-10.4, FGRAPH-10.5, FGRAPH-10.6_

---

## Coverage check

Every FGRAPH requirement ID is cited by exactly one task footer **and** carries a tagged
test:

| Req | Task | Tagged test |
|---|---|---|
| 1.1, 1.2 | 3 | `[FGRAPH-1.1][FGRAPH-1.2]` harvest owns/touches |
| 1.3 | 1 | `[FGRAPH-1.3]` normalizePath |
| 1.4 | 1 | `[FGRAPH-1.4]` dedupeByFullest |
| 1.5 | 1 | `[FGRAPH-1.5]` isSourcePath |
| 1.6 | 2 | `[FGRAPH-1.6]` classifyRole |
| 2.1, 2.2, 2.3 | 3 | `[FGRAPH-2.1][FGRAPH-2.2][FGRAPH-2.3]` reverse/shared |
| 3.1, 3.2 | 4 | `[FGRAPH-3.1][FGRAPH-3.2]` card content |
| 3.3 | 4 | `[FGRAPH-3.3]` interfaces |
| 3.4 | 4 | `[FGRAPH-3.4]` cap |
| 4.1, 4.3 | 7 | `[FGRAPH-4.1][FGRAPH-4.3]` CLI harvest + INDEX untouched |
| 4.2 | 5 | `[FGRAPH-4.2]` determinism |
| 5.1, 5.3 | 6 | `[FGRAPH-5.1][FGRAPH-5.3]` query rank |
| 5.2 | 6 | `[FGRAPH-5.2]` keyword |
| 5.4, 5.5 | 7 | `[FGRAPH-5.4][FGRAPH-5.5]` fresh JSON |
| 5.6 | 7 | (structural — harvest reads only markdown; noted, no assertion) |
| 6.1, 6.2 | 8 | `[FGRAPH-6.1][FGRAPH-6.2]` verify freshness |
| 6.3 | 8 | `[FGRAPH-6.3]` unregistered code |
| 6.4 | 10 | `[FGRAPH-6.4]` verify wiring |
| 7.1–7.5 | 10 | `[FGRAPH-7.1..7.5]` brainstorm wiring |
| 8.1, 8.2 | 10 | `[FGRAPH-8.1][FGRAPH-8.2]` sync-spec wiring |
| 9.1 | 3 | `[FGRAPH-9.1]` requirements-only feature |
| 9.2 | 5 | `[FGRAPH-9.2]` empty graph |
| 9.3 | 7 | `[FGRAPH-9.3]` config fallback |
| 9.4, 9.5 | 9 | `[FGRAPH-9.4][FGRAPH-9.5]` guards |
| 9.6 | 10 | `[FGRAPH-9.6]` brainstorm no-subagent path |
| 11.1, 11.2, 11.3 | 12 | `[FGRAPH-11.1..11.3]` stamp, install, four drift verdicts (E2E) |
| 11.4, 11.5 | 12 | `[FGRAPH-11.4][FGRAPH-11.5]` project.md Graph row, pre-push graph lint |
| 11.6–11.9 | 12 | `[FGRAPH-11.6..11.9]` setup-repo CI opt-in + proving gate |
| 11.10, 11.11, 11.12 | 12 | `[FGRAPH-11.10..11.12]` loud-once remedy, still fails open |
| 11.13, 11.14 | 12 | `[FGRAPH-11.13][FGRAPH-11.14]` guards: no authoring burden; check-trace behavior identical |

**Reconciliation with the design seam table:** design listed 7.x/8.x/6.4 as *pressure-test*;
this plan strengthens them to an automatable **wiring regression test**
(`check-graph.wiring.test.mjs`) that asserts the durable SKILL.md markers — satisfying E2
while leaving behavioral pressure-testing as an additional acceptance-time check. FGRAPH-9.5
is tested with a self-contained vanilla-spec fixture rather than the external `bot` repo
(unavailable in this repo's test env); the assertion is equivalent (standard specs alone
yield a surface). FGRAPH-5.6 is guaranteed structurally (harvest does only `fs.readFileSync`
on `.md`) and is noted rather than asserted. No requirement is left uncovered; no requirement
was found wrong or infeasible, so no upstream sync-back was needed.
