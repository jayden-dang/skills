#!/usr/bin/env node
/**
 * check-trace — requirements traceability linter.
 *
 * Sources of truth:
 *   <specsDir>/<feature>/requirements.md   defines requirement IDs (**CODE-N.M**)
 *   <specsDir>/fixes.md                    optional shared home for tier-1 fix/guard requirements
 *
 * References:
 *   <specsDir>/<feature>/tasks.md          task footers: _Requirements: CODE-N.M, CODE-N.M_
 *   test files (globs)                     IDs in tags/annotations/names/comments, e.g. @CODE-N.M,
 *                                          annotate('CODE-N.M', ...), /// REQ: CODE-N.M
 *
 * Checks:
 *   E1  a task or test cites an ID that is not defined in any requirements file
 *   E2  a requirements file with Status Implemented/Shipped has a requirement with zero test references
 *   E3  the same ID is defined more than once
 *   W1  a requirements file with Status Approved has a requirement not cited by any task
 *   W2  a requirements file is missing a Status line or feature code
 *
 * Exit code 1 on any error (and on warnings with --strict), 0 otherwise.
 *
 * Usage: node check-trace.mjs [--strict] [--json] [--root <repo-root>]
 * Config (optional): docs/agents/trace.json
 *   { "specsDir": "docs/specs", "testGlobs": ["tests/", "e2e/", "src/"], "testFilePattern": "\\.(test|spec)\\.|/tests?/|/e2e/|_test\\." }
 */

import fs from 'node:fs';
import path from 'node:path';

const args = process.argv.slice(2);
const strict = args.includes('--strict');
const asJson = args.includes('--json');
const rootIdx = args.indexOf('--root');
const ROOT = rootIdx !== -1 ? path.resolve(args[rootIdx + 1]) : process.cwd();

const DEFAULTS = {
  specsDir: 'docs/specs',
  // Directories scanned for test files (relative to root).
  testGlobs: ['tests', 'test', 'e2e', 'src', 'src-tauri', 'crates', 'app', 'lib', 'packages'],
  // A file is a test file if its path matches this regex.
  testFilePattern: '(\\.(test|spec)\\.[cm]?[jt]sx?$)|([/\\\\]tests?[/\\\\])|([/\\\\]e2e[/\\\\])|(_test\\.(rs|go|py)$)|(\\.rs$)',
};

function loadConfig() {
  const p = path.join(ROOT, 'docs/agents/trace.json');
  if (!fs.existsSync(p)) return DEFAULTS;
  try {
    return { ...DEFAULTS, ...JSON.parse(fs.readFileSync(p, 'utf8')) };
  } catch (e) {
    console.error(`check-trace: could not parse ${p}: ${e.message}`);
    process.exit(1);
  }
}

const cfg = loadConfig();
// No trailing \b: markdown italics footers end `..._`, and `_` is a word char,
// which would silently drop the last ID on the line. Guard against partial
// number matches with a lookahead instead.
const ID_RE = /\b([A-Z][A-Z0-9]{1,11})-(\d+)\.(\d+)(?![.\d])/g;
const SKIP_DIRS = new Set(['node_modules', '.git', 'dist', 'build', 'target', 'coverage', '.next', '.skills', 'vendor']);

/** Recursively collect files under dir for which predicate(relPath) is true. */
function walk(dir, predicate, out = []) {
  let entries;
  try {
    entries = fs.readdirSync(dir, { withFileTypes: true });
  } catch {
    return out;
  }
  for (const entry of entries) {
    if (entry.name.startsWith('.') && entry.name !== '.') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (!SKIP_DIRS.has(entry.name)) walk(full, predicate, out);
    } else if (predicate(path.relative(ROOT, full))) {
      out.push(full);
    }
  }
  return out;
}

function extractIds(text) {
  const ids = [];
  for (const m of text.matchAll(ID_RE)) ids.push(m[0]);
  return ids;
}

// ---------------------------------------------------------------- collect
const specsDir = path.join(ROOT, cfg.specsDir);
if (!fs.existsSync(specsDir)) {
  console.error(`check-trace: no specs directory at ${cfg.specsDir} — nothing to check.`);
  process.exit(0);
}

/** id -> { file, status } */
const defined = new Map();
/** id -> [files] for duplicate detection */
const definitionSites = new Map();
/** file -> { status, ids } */
const reqFiles = [];
const warnings = [];
const errors = [];

const requirementFiles = walk(specsDir, (rel) => rel.endsWith('requirements.md') || rel.endsWith('fixes.md'));
for (const file of requirementFiles) {
  const rel = path.relative(ROOT, file);
  const text = fs.readFileSync(file, 'utf8');
  const statusMatch = text.match(/^Status:\s*(Draft|Approved|Implemented|Shipped)/m);
  const codeMatch = text.match(/^Feature code:\s*([A-Z][A-Z0-9]{1,11})/m);
  const status = statusMatch ? statusMatch[1] : null;
  if (!statusMatch && !rel.endsWith('fixes.md')) warnings.push(`W2 ${rel}: missing "Status:" line`);
  if (!codeMatch && !rel.endsWith('fixes.md')) warnings.push(`W2 ${rel}: missing "Feature code:" line`);

  // Only bold-defined IDs (**CODE-N.M**) count as definitions; struck-through
  // (~~**CODE-N.M**~~) are retired and deliberately excluded from coverage.
  const ids = [];
  const scannable = text.replace(/~~.*?~~/g, '');
  for (const m of scannable.matchAll(/\*\*([A-Z][A-Z0-9]{1,11}-\d+\.\d+)\*\*/g)) {
    const id = m[1];
    ids.push(id);
    if (!definitionSites.has(id)) definitionSites.set(id, []);
    definitionSites.get(id).push(rel);
    defined.set(id, { file: rel, status });
  }
  reqFiles.push({ rel, status, ids });
}

for (const [id, sites] of definitionSites) {
  if (sites.length > 1) errors.push(`E3 duplicate definition of ${id} in: ${[...new Set(sites)].join(', ')}`);
}

// Task references: tasks.md footers.
const taskRefs = new Map(); // id -> [file]
const taskFiles = walk(specsDir, (rel) => rel.endsWith('tasks.md'));
for (const file of taskFiles) {
  const rel = path.relative(ROOT, file);
  const text = fs.readFileSync(file, 'utf8');
  for (const line of text.split('\n')) {
    if (!/_Requirements:/.test(line)) continue;
    for (const id of extractIds(line)) {
      if (!taskRefs.has(id)) taskRefs.set(id, []);
      taskRefs.get(id).push(rel);
    }
  }
}

// Test references: any defined-looking ID appearing in a test file.
const testRefs = new Map(); // id -> [file]
const fileRe = new RegExp(cfg.testFilePattern);
const roots = cfg.testGlobs.map((g) => path.join(ROOT, g)).filter((p) => fs.existsSync(p));
const testFiles = [];
for (const r of roots) walk(r, (rel) => fileRe.test(rel), testFiles);
for (const file of [...new Set(testFiles)]) {
  const rel = path.relative(ROOT, file);
  let text;
  try {
    text = fs.readFileSync(file, 'utf8');
  } catch {
    continue;
  }
  for (const id of new Set(extractIds(text))) {
    if (!testRefs.has(id)) testRefs.set(id, []);
    testRefs.get(id).push(rel);
  }
}

// ---------------------------------------------------------------- checks
for (const [id, files] of taskRefs) {
  if (!defined.has(id)) errors.push(`E1 task cites unknown requirement ${id} (${[...new Set(files)].join(', ')})`);
}
for (const [id, files] of testRefs) {
  if (!defined.has(id)) errors.push(`E1 test cites unknown requirement ${id} (${[...new Set(files)][0]}${files.length > 1 ? `, +${files.length - 1} more` : ''})`);
}
for (const { rel, status, ids } of reqFiles) {
  for (const id of ids) {
    const tested = testRefs.has(id);
    const tasked = taskRefs.has(id);
    if ((status === 'Implemented' || status === 'Shipped') && !tested) {
      errors.push(`E2 ${id} (${rel}, ${status}) has no covering test`);
    }
    if (status === 'Approved' && !tasked) {
      warnings.push(`W1 ${id} (${rel}, Approved) is not cited by any task`);
    }
  }
}

// ---------------------------------------------------------------- report
const summary = {
  requirements: defined.size,
  requirementFiles: reqFiles.length,
  taskCitations: taskRefs.size,
  testedRequirements: [...defined.keys()].filter((id) => testRefs.has(id)).length,
  testFilesScanned: new Set(testFiles).size,
  errors,
  warnings,
};

if (asJson) {
  console.log(JSON.stringify(summary, null, 2));
} else {
  console.log(`check-trace: ${summary.requirements} requirements in ${summary.requirementFiles} files; ` +
    `${summary.testedRequirements} covered by tests; ${summary.taskCitations} cited by tasks; ` +
    `${summary.testFilesScanned} test files scanned.`);
  for (const w of warnings) console.log(`  warn  ${w}`);
  for (const e of errors) console.log(`  ERROR ${e}`);
}

if (errors.length > 0 || (strict && warnings.length > 0)) process.exit(1);
