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
