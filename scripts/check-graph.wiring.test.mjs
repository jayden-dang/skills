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
