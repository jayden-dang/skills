/**
 * Regression tests for check-trace's retirement convention.
 *
 * Run: node --test scripts/check-trace.test.mjs   (Node 18+, no dependencies)
 *
 * Guards the documented rule that a struck-through requirement
 * (`~~**CODE-N.M**~~`) is retired: it is excluded from the definition count and
 * from coverage, so it can never fire E2 ("Implemented requirement with no
 * covering test"). The convention was documented long before it was
 * implemented — these tests exist so it can't silently rot again.
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const CHECK_TRACE = path.join(import.meta.dirname, 'check-trace.mjs');

/** Build a throwaway repo root with one spec file (and optional test files). */
function fixture({ requirements, files = {} }) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'check-trace-'));
  const specDir = path.join(root, 'docs/specs/feature');
  fs.mkdirSync(specDir, { recursive: true });
  fs.writeFileSync(path.join(specDir, 'requirements.md'), requirements);
  for (const [rel, body] of Object.entries(files)) {
    const p = path.join(root, rel);
    fs.mkdirSync(path.dirname(p), { recursive: true });
    fs.writeFileSync(p, body);
  }
  return root;
}

/** Run check-trace against a root; return { code, summary }. */
function run(root) {
  const r = spawnSync('node', [CHECK_TRACE, '--root', root, '--json'], { encoding: 'utf8' });
  return { code: r.status, summary: JSON.parse(r.stdout) };
}

test('a struck-through requirement is retired: not counted, cannot fire E2', () => {
  const root = fixture({
    requirements: [
      '# Requirements: retirement',
      'Feature code: RET',
      'Status: Implemented',
      '',
      '- **RET-1.1** THE SYSTEM SHALL do the live thing.',
      '- ~~**RET-9.9**~~ superseded by RET-1.1 — retired, deliberately untested.',
      '',
    ].join('\n'),
    // RET-1.1 has a covering test; RET-9.9 has none.
    files: { 'src/cover.test.ts': "it('[RET-1.1] covered', () => {})" },
  });
  try {
    const { code, summary } = run(root);
    assert.equal(summary.requirements, 1, 'only RET-1.1 is a definition; RET-9.9 is retired');
    assert.deepEqual(summary.errors, [], 'no E2 for the retired RET-9.9');
    assert.equal(code, 0, 'clean exit');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('the same ID left bold (not struck) still fires E2 — strip is strikethrough-specific', () => {
  const root = fixture({
    requirements: [
      '# Requirements: retirement',
      'Feature code: RET',
      'Status: Implemented',
      '',
      '- **RET-9.9** THE SYSTEM SHALL do a thing nobody tested.',
      '',
    ].join('\n'),
    // No covering test anywhere.
  });
  try {
    const { code, summary } = run(root);
    assert.equal(summary.requirements, 1, 'RET-9.9 counts as a definition when bold');
    assert.equal(summary.errors.length, 1, 'exactly one error');
    assert.match(summary.errors[0], /^E2 RET-9\.9\b/, 'E2 still fires for a genuinely uncovered requirement');
    assert.equal(code, 1, 'non-zero exit on error');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
