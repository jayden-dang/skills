import { test } from 'node:test';
import assert from 'node:assert/strict';
import { normalizePath, isSourcePath, dedupeByFullest, classifyRole } from './check-graph.mjs';

const CFG = {
  sourceRoots: ['src', 'src-tauri', 'tests', 'test', 'crates', 'app', 'lib', 'packages'],
  sourceExts: ['ts', 'tsx', 'js', 'jsx', 'mjs', 'rs', 'css', 'scss'],
};

test('[FGRAPH-1.3] normalizePath strips locators and quoting', () => {
  assert.equal(normalizePath('`Editor.tsx:208`'), 'Editor.tsx');
  assert.equal(normalizePath('App.tsx:127,172'), 'App.tsx');
  assert.equal(normalizePath('src/components/Editor.tsx (~208-221)'), 'src/components/Editor.tsx');
  assert.equal(normalizePath('"src/lib/x.ts"'), 'src/lib/x.ts');
  assert.equal(normalizePath('`Editor.tsx:208` (~208-221)'), 'Editor.tsx');
  assert.equal(normalizePath('./check-graph.mjs'), 'check-graph.mjs');
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

test('[FGRAPH-1.6] classifyRole: create signal owns, else touches', () => {
  assert.equal(classifyRole('- Create: `src/x.ts` — new picker', null), 'owns');
  assert.equal(classifyRole('add a new file src/y.ts', null), 'owns');
  assert.equal(classifyRole('- Modify: `src/x.ts` (extract helper)', null), 'touches');
  assert.equal(classifyRole('reuse `src/x.ts` from the plugin', null), 'touches');
  assert.equal(classifyRole('`src/x.ts` is referenced here', 'create'), 'owns');  // block wins
  assert.equal(classifyRole('`src/x.ts` mentioned in prose', null), 'touches');   // safe default
  assert.equal(classifyRole('Modify the config to add a new dependency version check', null), 'touches');
  assert.equal(classifyRole('Add a toggle for the new settings pane while modifying things', null), 'touches');
});

import { harvest, DEFAULTS } from './check-graph.mjs';
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

test('[FGRAPH-1.6] scanSurface: blockLabel does not leak past a blank line or heading', () => {
  const specs = specFixture([
    { slug: 'a-leak', code: 'LEAK', name: 'Leak',
      design: '**Files:**\n- Create: `src/new/thing.ts`\n\n## Notes\nSee also `src/old/legacy.ts`.\n' },
  ]);
  const g = harvest(specs);
  const f = g.features.find((x) => x.code === 'LEAK');
  assert.ok(f.owns.includes('src/new/thing.ts'), 'the actually-created file is owned');
  assert.ok(f.touches.includes('src/old/legacy.ts'), 'a mere reference after the block ended is only touched');
  assert.ok(!f.owns.includes('src/old/legacy.ts'), 'stale create block label must not leak onto later prose');
});

test('[FGRAPH-1.2] scanSurface ignores paths inside fenced code blocks', () => {
  const specs = specFixture([{ slug: 'a', code: 'FENCE', name: 'Fence',
    tasks: '**Files:**\n- Create: `src/real.ts`\n\n```js\nimport x from "src/fake.ts";\nconst p = "App.tsx";\n```\n' }]);
  const f = harvest(specs).features.find((x) => x.code === 'FENCE');
  assert.ok(f.owns.includes('src/real.ts'), 'unfenced Create path kept');
  assert.ok(!f.owns.includes('src/fake.ts') && !f.touches.includes('src/fake.ts'), 'fenced path excluded');
  assert.ok(!f.owns.includes('App.tsx') && !f.touches.includes('App.tsx'), 'fenced path excluded');
});

test('[FGRAPH-1.6] harvest: owns beats touches across basename/fullpath dedup within a feature', () => {
  const specs = specFixture([
    { slug: 'a-dedup', code: 'DEDUP', name: 'Dedup',
      tasks: '- Create: `engine.ts`\n',
      design: 'This references the existing `src/core/engine.ts` module.\n' },
  ]);
  const g = harvest(specs);
  const f = g.features.find((x) => x.code === 'DEDUP');
  assert.ok(f.owns.includes('src/core/engine.ts'), 'owns must win over touches after dedup collapses basename into full path');
  assert.ok(!f.touches.includes('src/core/engine.ts'));
});

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

test('[FGRAPH-3.3] interfaces drop bare Produces/Consumes labels, keep substance', () => {
  const specs = specFixture([{ slug: 'a', code: 'IF2', name: 'If2',
    design: '**Interfaces:**\n- Produces:\n  - `doThing(x) → y`\n- Consumes: `helper()`\n' }]);
  const f = harvest(specs).features.find((x) => x.code === 'IF2');
  assert.ok(f.interfaces.some((s) => s.includes('doThing')), 'substance kept');
  assert.ok(f.interfaces.some((s) => s.includes('helper')), 'inline consumes substance kept');
  assert.ok(!f.interfaces.some((s) => /^(produces|consumes):?$/i.test(s.trim())), 'no bare label entries');
});

test('[FGRAPH-3.4] card lists are capped at cardCap', () => {
  const many = Array.from({ length: 20 }, (_, i) => `No feature number ${i}`);
  const specs = specFixture([{ slug: 'a', code: 'CAP', name: 'Cap', oos: many }]);
  const cfg = { ...DEFAULTS, graph: { ...DEFAULTS.graph, cardCap: 5 } };
  const f = harvest(specs, cfg).features.find((x) => x.code === 'CAP');
  assert.equal(f.oos.length, 6, '5 items + 1 elision marker');
  assert.match(f.oos[5], /\+15 more/);
});

test('[FGRAPH-3.4] cap on owns/touches does not drop a shared path from the reverse index', () => {
  // BASE owns 13 files (over the default cardCap of 12); the 13th (by sort
  // order) is also touched by EXT, making it a shared surface. The capped
  // card field must elide it, but the reverse index / shared list — built
  // from the uncapped surface — must still carry the full reference.
  const owned = Array.from({ length: 13 }, (_, i) => `src/gen/file${String(i).padStart(2, '0')}.ts`);
  const specs = specFixture([
    { slug: 'a-base', code: 'BASE', name: 'Base',
      tasks: owned.map((p) => `- Create: \`${p}\`\n`).join('') },
    { slug: 'b-ext', code: 'EXT', name: 'Extension',
      tasks: `- Modify: \`${owned[owned.length - 1]}\`\n` },
  ]);
  const g = harvest(specs);
  const base = g.features.find((f) => f.code === 'BASE');
  const shared = owned[owned.length - 1];
  assert.equal(base.owns.length, 13, 'card field is capped at 12 + 1 elision marker');
  assert.match(base.owns[12], /\+1 more/);
  assert.ok(!base.owns.includes(shared), 'the 13th file is elided from the capped card field');
  assert.ok(g.reverse[shared], 'the 13th file must still appear in the reverse index');
  assert.deepEqual(g.reverse[shared].map((r) => r.code).sort(), ['BASE', 'EXT']);
  const sharedEntry = g.shared.find((s) => s.path === shared);
  assert.ok(sharedEntry, 'the 13th file must still appear in the shared-surface list');
  assert.equal(sharedEntry.refs.length, 2);
});

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

test('[FGRAPH-4.3] renderGraphMd is a pure string function — no file side effects', () => {
  const specs = specFixture([{ slug: 'a', code: 'PURE', name: 'Pure', tasks: '- Create: `src/pure.ts`\n' }]);
  const g = harvest(specs);
  const before = new Set(fs.readdirSync(path.join(specs)));
  const result = renderGraphMd(g);
  assert.equal(typeof result, 'string');
  const after = new Set(fs.readdirSync(path.join(specs)));
  assert.deepEqual(before, after, 'renderGraphMd must not write any file into specsDir');
  assert.ok(!fs.existsSync(path.join(specs, 'GRAPH.md')), 'renderGraphMd must never write GRAPH.md itself');
});

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

test('[FGRAPH-5.3] query by path ranks a 2-overlap feature above a 1-overlap feature, with deterministic tie-break', () => {
  const specs = specFixture([
    { slug: 'z', code: 'ZZZ', name: 'Z', tasks: '- Create: `src/only.ts`\n' },
    { slug: 'a', code: 'AAA', name: 'A', tasks: '- Create: `src/one.ts`\n- Create: `src/two.ts`\n' },
  ]);
  const g = harvest(specs);
  const res = query(g, { paths: ['src/one.ts', 'src/two.ts', 'src/only.ts'] });
  assert.deepEqual(res.map((r) => r.code), ['AAA', 'ZZZ'], 'higher overlap count ranks first regardless of code order');
  assert.deepEqual(res[0].overlapPaths, ['src/one.ts', 'src/two.ts'], 'overlapPaths lists the actually-overlapping paths, sorted');
});

test('[FGRAPH-5.3] query breaks a genuine overlap-count tie by code ascending, not path-argument order', () => {
  const specs = specFixture([
    { slug: 'z', code: 'ZZZ', name: 'Zebra widget', tasks: '- Create: `src/z.ts`\n' },
    { slug: 'a', code: 'AAA', name: 'Alpha widget', tasks: '- Create: `src/a.ts`\n' },
  ]);
  const g = harvest(specs);
  // ZZZ and AAA each own exactly one distinct file, so querying both paths
  // ties them at overlapPaths.length === 1. The path-argument order lists
  // ZZZ's file first, so a stable sort with the tie-break comparator
  // deleted would preserve that path-argument order (['ZZZ','AAA']) —
  // JS's keyword-loop iteration happens to sort by code already, which is
  // why a keyword-based tie test can't detect a missing tie-break, but a
  // path-based tie in a non-code order can. Only the explicit
  // `|| a.code.localeCompare(b.code)` clause forces ascending-code order.
  const res = query(g, { paths: ['src/z.ts', 'src/a.ts'] });
  assert.deepEqual(res.map((r) => r.code), ['AAA', 'ZZZ'], 'equal overlap count → ascending by code, not path-argument order');
});

import { spawnSync } from 'node:child_process';

const CLI = path.join(import.meta.dirname, 'check-graph.mjs');

/** specFixture() returns <root>/docs/specs; walk back up to <root> for CLI --root. */
function cliFixture(features) { return path.dirname(path.dirname(specFixture(features))); }

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

test('[FGRAPH-5.6] check-graph reads only markdown — no network/build/child_process', () => {
  const src = fs.readFileSync(path.join(import.meta.dirname, 'check-graph.mjs'), 'utf8');
  assert.doesNotMatch(src, /from ['"](?:node:)?(?:child_process|http|https|net|dns|dgram)['"]/, 'no network/process imports');
  assert.doesNotMatch(src, /\bfetch\s*\(/, 'no fetch');
  assert.doesNotMatch(src, /\b(?:execSync|spawnSync|spawn|exec)\s*\(/, 'no subprocess/build calls');
});
