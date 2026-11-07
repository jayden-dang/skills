// Draws the last moment of every line into out/preview.png, in seconds, before you spend a full render.
// Usage, from the project folder: node preview.mjs
import {execFileSync} from 'node:child_process';
import {mkdirSync, rmSync, writeFileSync} from 'node:fs';
import {resolve} from 'node:path';
import {openBrowser, renderStill, selectComposition} from '@remotion/renderer';
import {writeSound} from './sound.mjs';

const serveUrl = resolve('out/bundle');
execFileSync('npx', ['remotion', 'bundle', `--out-dir=${serveUrl}`, '--log=error'], {stdio: 'inherit'});

const browser = await openBrowser('chrome');
const composition = await selectComposition({serveUrl, id: 'Film', puppeteerInstance: browser});
const {beats, scenes, events, timing} = composition.props;
mkdirSync('public', {recursive: true});
writeSound(events, composition.durationInFrames, composition.fps, 'public/sound.wav');

rmSync('out/preview', {recursive: true, force: true});
mkdirSync('out/preview', {recursive: true});
for (const [i, frame] of beats.entries()) {
  const output = `out/preview/${String(i).padStart(3, '0')}.png`;
  await renderStill({composition, serveUrl, frame, output, puppeteerInstance: browser, imageFormat: 'png'});
}
await browser.close({silent: true});

writeFileSync('out/beats.json', JSON.stringify(beats));
writeFileSync('out/scenes.json', JSON.stringify(scenes, null, 1));
writeFileSync('out/timing.json', JSON.stringify(timing));
const rows = Math.ceil(beats.length / 4);
execFileSync('ffmpeg', ['-v', 'error', '-y', '-framerate', '1', '-pattern_type', 'glob', '-i', 'out/preview/*.png', '-vf', `scale=640:-1,tile=4x${rows}`, '-frames:v', '1', 'out/preview.png'], {stdio: 'inherit'});
console.log(`preview: ${resolve('out/preview.png')} (${beats.length} lines; full size in out/preview/)`);
