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
  t = t.replace(/^\.\//, ''); // leading "./" so "./check-graph.mjs" dedups with "check-graph.mjs"
  return t;
}

export function isSourcePath(token, cfg) {
  const t = token;
  if (!t || /\s/.test(t)) return false;
  if (t.includes('*')) return false; // glob token, not a concrete path (FGRAPH-1.7)
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

const SKIP_DIRS = new Set(['node_modules', '.git', 'dist', 'build', 'target', 'coverage', '.next', '.skills', 'vendor']);
const BACKTICK_RE = /`([^`]+)`/g;
const WORD_RE = /[A-Za-z0-9_./-]+/g;

// A command-invocation line names a tool being run, not a surface being
// owned/touched — a path that appears ONLY on such lines is not surface.
const CMD_LINE_RE = /(^|\s)(node|npm|pnpm|npx|yarn|git|bash|sh|deno|bun)\s/;
function isCommandLine(line) {
  return CMD_LINE_RE.test(line) || /^\s*Run\b/i.test(line) || /^\s*\$ /.test(line);
}

/** Recursively collect files under dir for which predicate(fullPath) is true. */
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

/** Cap a Summary card list at `cap` entries, appending a "…(+N more)" elision marker. */
export function capList(items, cap) {
  if (items.length <= cap) return items;
  return [...items.slice(0, cap), `…(+${items.length - cap} more)`];
}

/** Extract the `## Out of Scope` bullet list from a requirements.md body (best-effort). */
export function extractOutOfScope(reqText) {
  const m = reqText.match(/##\s*Out of Scope\s*\n([\s\S]*?)(\n##\s|\n#\s|$)/i);
  if (!m) return [];
  return [...m[1].matchAll(/^\s*[-*]\s+(.+?)\s*$/gm)].map((x) => x[1].replace(/\*\*/g, '').trim());
}

const INTERFACE_LABEL_ONLY_RE = /^(?:produces|consumes|provides|exposes):?$/i;
const INTERFACE_LABEL_PREFIX_RE = /^(?:produces|consumes|provides|exposes):\s*/i;

/** A bullet whose text is just a bare section-lead label (`Produces:` etc), with no substance of its own. */
function isBareInterfaceLabel(text) { return INTERFACE_LABEL_ONLY_RE.test(text.trim()); }

/** Reduce a kept bullet's text to a short single-line entry: strip a leading
 * label prefix, truncate at the first ` — ` em-dash (drop trailing prose),
 * strip backticks, trim. */
function cleanInterfaceEntry(text) {
  let s = text.replace(INTERFACE_LABEL_PREFIX_RE, '');
  const dashIdx = s.indexOf(' — ');
  if (dashIdx !== -1) s = s.slice(0, dashIdx);
  return s.replace(/`/g, '').trim();
}

/** Extract bullet items under any `Interfaces:` heading across design.md/tasks.md bodies (best-effort).
 * Each entry is a short single-line signature: only the top-level bullets
 * under the heading are considered (a bare section-lead label like
 * `Produces:` has no substance of its own, so its direct children are
 * promoted instead); nested sub-bullets under a substantive top-level entry
 * are prose/detail and are skipped to avoid duplicating the entry. */
export function extractInterfaces(bodies) {
  const out = [];
  const HEADING_RE = /^\s*\*?\*?interfaces:?\*?\*?\s*$/im;
  for (const body of bodies) {
    if (!body) continue;
    const lines = body.split('\n');
    for (let i = 0; i < lines.length; i++) {
      if (!HEADING_RE.test(lines[i])) continue;
      const group = [];
      let j = i + 1;
      for (; j < lines.length && /^\s*[-*]\s+/.test(lines[j]); j++) {
        group.push({
          indent: lines[j].match(/^\s*/)[0].length,
          text: lines[j].replace(/^\s*[-*]\s+/, ''),
        });
      }
      if (group.length === 0) continue;
      const minIndent = Math.min(...group.map((g) => g.indent));
      for (let k = 0; k < group.length; k++) {
        if (group[k].indent !== minIndent) continue; // only top-level bullets
        const { text } = group[k];
        if (isBareInterfaceLabel(text)) {
          // Pass-through: this bullet contributes no signal of its own —
          // promote its direct children (the next indent level down) instead.
          const children = [];
          for (let m = k + 1; m < group.length && group[m].indent > minIndent; m++) children.push(group[m]);
          if (children.length === 0) continue;
          const childMin = Math.min(...children.map((c) => c.indent));
          for (const c of children) {
            if (c.indent !== childMin || isBareInterfaceLabel(c.text)) continue;
            const cleaned = cleanInterfaceEntry(c.text);
            if (cleaned) out.push(cleaned);
          }
          continue;
        }
        const cleaned = cleanInterfaceEntry(text);
        if (cleaned) out.push(cleaned);
      }
    }
  }
  return out;
}

/** Extract normalized source paths (with roles) from one design.md/tasks.md body. */
function scanSurface(text, cfg) {
  // path -> {role, keep}: `keep` tracks whether the path had at least one
  // NON-command-line occurrence (FGRAPH-1.8) — a path seen ONLY on
  // command-invocation lines (e.g. `Run \`node scripts/x.mjs\``) is not
  // surface, but a path that also appears in a Create/Modify bullet or
  // prose line must still be kept even if it's ALSO named on a command line.
  const raw = new Map();
  let blockLabel = null;
  let inFence = false;
  for (const line of text.split('\n')) {
    if (/^\s*(```|~~~)/.test(line)) { inFence = !inFence; blockLabel = null; continue; }
    if (inFence) continue;
    if (CREATE_LABEL.test(line)) blockLabel = 'create';
    else if (MODIFY_LABEL.test(line)) blockLabel = 'modify';
    else if (/^\s*$/.test(line) || /^\s*#{1,6}\s/.test(line) || /^\s*\*?\*?(files|interfaces|steps)\b/i.test(line)) blockLabel = null;
    const isCmd = isCommandLine(line);
    const cands = new Set();
    for (const m of line.matchAll(BACKTICK_RE)) cands.add(m[1]);
    for (const m of line.matchAll(WORD_RE)) cands.add(m[0]);
    for (const c of cands) {
      const p = normalizePath(c);
      if (!isSourcePath(p, cfg.graph)) continue;
      const role = classifyRole(line, blockLabel);
      const prev = raw.get(p);
      const keep = !!(prev && prev.keep) || !isCmd;
      const finalRole = (role === 'owns' || !prev) ? role : prev.role;
      raw.set(p, { role: finalRole, keep });
    }
  }
  const found = new Map(); // path -> role (owns beats touches)
  for (const [p, v] of raw) if (v.keep) found.set(p, v.role);
  return found;
}

/** Harvest the Surface manifest, Reverse index, and Shared surface from <specsDir>. */
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
    const designBody = readMaybe(path.join(dir, 'design.md'));
    const tasksBody = readMaybe(path.join(dir, 'tasks.md'));
    const surface = new Map();
    for (const body of [designBody, tasksBody]) {
      if (!body) continue;
      for (const [p, role] of scanSurface(body, cfg)) {
        if (role === 'owns' || !surface.has(p)) surface.set(p, role);
      }
    }
    // basename/full dedup within this feature, keeping the winning role: a
    // path is `owns` if EITHER the surviving fullest form, OR any basename
    // form of it that got collapsed away, was itself recorded as `owns`.
    const surfaceKeys = [...surface.keys()];
    const fullest = new Set(dedupeByFullest(surfaceKeys));
    const owns = [], touches = [];
    for (const p of fullest) {
      const isOwned = surfaceKeys.some((k) => (k === p || p.endsWith('/' + k)) && surface.get(k) === 'owns');
      (isOwned ? owns : touches).push(p);
    }
    // owns/touches stay UNCAPPED here: the reverse index and shared surface
    // below are built from these raw arrays, so a 13th shared file is never
    // silently dropped from FGRAPH-2.x just because the Summary card elides
    // it. The cap is applied in a separate pass, after reverse/shared exist.
    features.push({
      code, name,
      owns: owns.sort(),
      touches: touches.sort(),
      interfaces: extractInterfaces([designBody, tasksBody]),
      oos: extractOutOfScope(text),
    });
  }
  features.sort((a, b) => a.code.localeCompare(b.code));

  // FGRAPH-2.4: canonicalize each path to the FULLEST form of that file seen
  // across ALL features before indexing, so a bare basename in one feature
  // (`mathInputExtension.ts`) and the full path to the same file in another
  // feature (`src/components/mathInputExtension.ts`) merge into a single
  // reverse-index / shared-surface key instead of two separate ones.
  const allSurfacePaths = features.flatMap((f) => [...f.owns, ...f.touches]);
  const uniqAll = [...new Set(allSurfacePaths)];
  const canon = new Map(); // path -> fullest path seen for that file
  for (const p of uniqAll) {
    let fullest = p;
    for (const q of uniqAll) {
      if (q !== p && q.endsWith('/' + p) && q.length > fullest.length) fullest = q;
    }
    canon.set(p, fullest);
  }

  const reverse = {};
  for (const f of features) {
    for (const [p, role] of [...f.owns.map((p) => [p, 'owns']), ...f.touches.map((p) => [p, 'touches'])]) {
      const key = canon.get(p) ?? p;
      (reverse[key] ||= []).push({ code: f.code, role });
    }
  }
  for (const p of Object.keys(reverse)) reverse[p].sort((a, b) => a.code.localeCompare(b.code));
  const shared = Object.keys(reverse).filter((p) => reverse[p].length >= 2).sort()
    .map((p) => ({ path: p, refs: reverse[p] }));

  // Summary cards: cap each list AFTER reverse/shared have been derived from
  // the uncapped owns/touches above, so the capped card fields never feed
  // back into the index.
  const cap = cfg.graph.cardCap;
  for (const f of features) {
    f.owns = capList(f.owns, cap);
    f.touches = capList(f.touches, cap);
    f.interfaces = capList(f.interfaces, cap);
    f.oos = capList(f.oos, cap);
  }
  return { features, reverse, shared };
}

/**
 * Render the Graph into a deterministic markdown document: a generated
 * banner, one Summary card per feature (## Cards, sorted by code per
 * harvest()'s ordering), and a Shared surface table (sorted by path per
 * harvest()'s ordering). Pure: takes a Graph, returns a string, touches no
 * file — the CLI is responsible for writing GRAPH.md.
 */
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

/**
 * Query the Graph for features overlapping a set of paths (via the Reverse
 * index) or matching a keyword against name/out-of-scope (case-insensitive
 * substring). Results are ranked by overlapPaths.length descending, tied
 * broken by code for determinism. Each result carries the feature's full
 * Summary card.
 */
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

/** Load docs/agents/trace.json (optional), deep-merging the nested `graph` key over DEFAULTS.graph. */
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

/** Collect every value that follows a repeatable flag, e.g. --path a --path b -> ['a','b']. */
function collectFlag(args, name) {
  const out = [];
  for (let i = 0; i < args.length; i++) if (args[i] === name) out.push(args[i + 1]);
  return out;
}

/**
 * --verify lint: (1) freshness — the committed GRAPH.md must be byte-identical
 * to a fresh renderGraphMd(harvest(...)) render, and (2) registration — every
 * harvested feature code must appear in <specsDir>/INDEX.md. Exits 1 and
 * reports on either failure; exits 0 when both hold.
 */
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

if (import.meta.url === pathToFileURL(process.argv[1]).href) main();
