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
  assert.match(t, /overlap check unavailable/i, 'FGRAPH-7.5/9.6: fail-open note');
});

test('[FGRAPH-7.3][FGRAPH-7.4] brainstorm step-1 Done-when states overlaps', () => {
  const t = read('skills/discovery/brainstorm/SKILL.md');
  assert.match(t, /share[sd]? .*surface|no existing feature/i, 'FGRAPH-7.3/7.4: state overlaps or none');
});

test('[FGRAPH-8.1][FGRAPH-8.2] sync-spec regenerates and stages GRAPH.md', () => {
  const t = read('skills/track/sync-spec/SKILL.md');
  assert.match(t, /check-graph(?:\.mjs)? --harvest/, 'FGRAPH-8.1: regenerates');
  assert.match(t, /GRAPH\.md[\s\S]{0,40}stage it into this sync-spec commit/i, 'FGRAPH-8.2: stages GRAPH.md into the commit');
});

test('[FGRAPH-6.4] verify runs check-graph --verify', () => {
  assert.match(read('skills/execution/verify/SKILL.md'), /check-graph --verify/);
});

test('[FGRAPH-10.1][FGRAPH-10.5] code-review runs the duplication query and fails open', () => {
  const t = read('skills/review/code-review/SKILL.md');
  assert.match(t, /check-graph(?:\.mjs)? --query/, 'FGRAPH-10.1: code-review calls the query on changed files');
  assert.match(t, /overlap check unavailable/i, 'FGRAPH-10.5: fail-open note');
});

test('[FGRAPH-10.2][FGRAPH-10.3] Spec subagent gets neighbor cards and a reuse-miss directive', () => {
  const t = read('skills/review/code-review/SKILL.md');
  assert.match(t, /overlapping feature/i, 'FGRAPH-10.2: overlapping features named');
  assert.match(t, /neighbor cards/i, 'FGRAPH-10.2: neighbor cards injected into the Spec brief');
  assert.match(t, /reuse-miss/i, 'FGRAPH-10.3: reuse-miss finding directive');
  assert.match(t, /reimplement/i, 'FGRAPH-10.3: cites reimplementing neighbor behavior');
});

test('[FGRAPH-10.4] no-overlap statement', () => {
  const t = read('skills/review/code-review/SKILL.md');
  assert.match(t, /no existing feature shares/i, 'FGRAPH-10.4: states no overlap and injects nothing');
});

test('[FGRAPH-10.6] two-axis review is preserved', () => {
  const t = read('skills/review/code-review/SKILL.md');
  assert.match(t, /\*\*Standards subagent\*\*/, 'FGRAPH-10.6: Standards subagent still present');
  assert.match(t, /\*\*Spec subagent\*\*/, 'FGRAPH-10.6: Spec subagent still present');
});
