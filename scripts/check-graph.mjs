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
  // Apply both strip regexes repeatedly to a fixpoint: a token can carry a
  // colon-form locator (:208 or :127,172) AND a paren-tail (~208-221) at the
  // same time, in either order, so a single fixed pass can't be trusted to
  // fully reduce it (e.g. "Editor.tsx:208 (~208-221)" needs both applied).
  let prev;
  do {
    prev = t;
    t = t.replace(/:\d+(?:[,\d]*)?$/, '');   // trailing :208 or :127,172 locator
    t = t.replace(/\s*~?\d[\d,\s-]*$/, '');  // trailing "(~208-221)" tail after paren-strip
    t = t.trim();
  } while (t !== prev);
  return t;
}

export function isSourcePath(token, cfg) {
  const t = token;
  if (!t || /\s/.test(t)) return false;
  const hasExt = EXT_RE(cfg.sourceExts).test(t);
  const seg = t.split('/');
  const filename = seg[seg.length - 1];
  // A "real" filename has a name part before any extension; a token that is
  // just a dot-prefixed suffix (".spec.ts") is a bare-extension pattern, not
  // a concrete path, so it's rejected here regardless of hasExt.
  const hasRealFilename = filename.length > 0 && !filename.startsWith('.') && /[A-Za-z0-9]/.test(filename);
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

const OWN_HINT = /\b(create|new file|adds? a? ?new file|scaffold)\b/i;
const CREATE_LABEL = /^\s*-?\s*create:/i;
const MODIFY_LABEL = /^\s*-?\s*modify:/i;

// Best-effort role classification: a `create` block label, or a create/new
// verb in the line itself, means the feature owns the surface; a `modify`
// block label means it only touches it. Everything else defaults to the
// safer "touches" (no false ownership claims from ambiguous prose).
export function classifyRole(line, blockLabel) {
  if (blockLabel === 'create' || CREATE_LABEL.test(line)) return 'owns';
  if (blockLabel === 'modify' || MODIFY_LABEL.test(line)) return 'touches';
  if (OWN_HINT.test(line)) return 'owns';
  return 'touches';
}

function main() {
  console.error('check-graph: CLI not yet implemented');
  process.exit(2);
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) main();
