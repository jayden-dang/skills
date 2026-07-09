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
