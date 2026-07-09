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
function fixture({ requirements, files = {}, traceJson }) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'check-trace-'));
  const specDir = path.join(root, 'docs/specs/feature');
  fs.mkdirSync(specDir, { recursive: true });
  fs.writeFileSync(path.join(specDir, 'requirements.md'), requirements);
  for (const [rel, body] of Object.entries(files)) {
    const p = path.join(root, rel);
    fs.mkdirSync(path.dirname(p), { recursive: true });
    fs.writeFileSync(p, body);
  }
  if (traceJson) {
    const agentsDir = path.join(root, 'docs/agents');
    fs.mkdirSync(agentsDir, { recursive: true });
    fs.writeFileSync(path.join(agentsDir, 'trace.json'), JSON.stringify(traceJson));
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

// ---------------------------------------------------------------- ignore list (TRACE-1.x)

const IGNORE_REQUIREMENTS = [
  '# Requirements: ignore',
  'Feature code: IGN',
  'Status: Approved',
  '',
  '- **IGN-1.1** THE SYSTEM SHALL do something unrelated to the fixture file.',
  '',
].join('\n');

test('[TRACE-1.1][TRACE-1.2] docs/agents/trace.json ignore excludes matching test files, so their fixture IDs never fire E1', () => {
  const root = fixture({
    requirements: IGNORE_REQUIREMENTS,
    files: { 'src/x.test.ts': "it('[GHOST-9.9] x', () => {})" },
    traceJson: { ignore: ['x.test.ts'] },
  });
  try {
    const { code, summary } = run(root);
    assert.deepEqual(summary.errors, [], 'the ignored file contributes no reference to GHOST-9.9, so no E1 fires');
    assert.equal(code, 0, 'clean exit');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('[TRACE-1.3] an empty ignore array scans every test file — unknown ID still fires E1', () => {
  const root = fixture({
    requirements: IGNORE_REQUIREMENTS,
    files: { 'src/x.test.ts': "it('[GHOST-9.9] x', () => {})" },
    traceJson: { ignore: [] },
  });
  try {
    const { code, summary } = run(root);
    assert.equal(summary.errors.length, 1, 'exactly one error');
    assert.match(summary.errors[0], /^E1 test cites unknown requirement GHOST-9\.9/, 'E1 fires — ignore is off by default');
    assert.equal(code, 1, 'non-zero exit on error');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('[TRACE-1.5] with no trace.json at all, an unknown-ID test file fires E1 exactly as before this change', () => {
  const root = fixture({
    requirements: IGNORE_REQUIREMENTS,
    files: { 'src/x.test.ts': "it('[GHOST-9.9] x', () => {})" },
    // no traceJson — docs/agents/trace.json does not exist
  });
  try {
    const { code, summary } = run(root);
    assert.deepEqual(
      summary.errors,
      ['E1 test cites unknown requirement GHOST-9.9 (src/x.test.ts)'],
      'byte-identical error text to pre-ignore behavior'
    );
    assert.equal(summary.testFilesScanned, 1, 'the file is still scanned');
    assert.equal(code, 1, 'non-zero exit on error');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('[TRACE-1.1] a blank ignore entry ("") does not exclude every test file', () => {
  const root = fixture({
    requirements: [
      '# Requirements: ignore blank entries',
      'Feature code: IGN',
      'Status: Implemented',
      '',
      '- **IGN-2.1** THE SYSTEM SHALL do something unrelated to the fixture file.',
      '',
    ].join('\n'),
    files: { 'src/good.test.ts': "it('[IGN-2.1] covered', () => {})" },
    // A stray/blank entry in `ignore` must be a no-op, not `rel.includes("")` (always true).
    traceJson: { ignore: [''] },
  });
  try {
    const { code, summary } = run(root);
    assert.ok(summary.testFilesScanned >= 1, 'the real test file is still scanned; an empty ignore entry must not match every path');
    assert.equal(summary.testedRequirements, 1, 'IGN-2.1 is still discovered as covered, not silently excluded');
    assert.deepEqual(summary.errors, [], 'Implemented IGN-2.1 has a covering test, so no E2 fires');
    assert.equal(code, 0, 'clean exit');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});

test('[TRACE-1.4] ignore only adds an exclusion — testGlobs/testFilePattern selection and coverage still work for non-ignored files', () => {
  const root = fixture({
    requirements: IGNORE_REQUIREMENTS,
    files: {
      'src/good.test.ts': "it('[IGN-1.1] covered', () => {})",
      'src/x.test.ts': "it('[GHOST-9.9] x', () => {})",
    },
    traceJson: { ignore: ['x.test.ts'] },
  });
  try {
    const { code, summary } = run(root);
    assert.equal(summary.testedRequirements, 1, 'IGN-1.1 is still discovered and counted as tested via normal testGlobs/testFilePattern selection');
    assert.deepEqual(summary.errors, [], 'the ignored file still contributes nothing, and the non-ignored file cites a known ID');
    assert.equal(code, 0, 'clean exit');
  } finally {
    fs.rmSync(root, { recursive: true, force: true });
  }
});
