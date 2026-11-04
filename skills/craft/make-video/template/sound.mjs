// The quiet layer under the voice: a low bed and a small hit on each change. Written here, so it needs no licence.
// preview.mjs calls this; the film plays public/sound.wav when it exists.
import {writeFileSync} from 'node:fs';

const RATE = 44100;
// The bed stays under -30 dB, where check_video.py still hears a silence in the voice. The hits stay small
// enough that a hit on the voice's loudest moment keeps the film's peak under -1 dB.
const BED = 0.018;

const seeded = (seed) => () => ((seed = (seed * 1664525 + 1013904223) >>> 0) / 2 ** 32) * 2 - 1;

const tick = (add, at) => {
  for (let k = 0; k < RATE * 0.05; k++) add(at + k, 0.035 * Math.sin((2 * Math.PI * 1500 * k) / RATE) * Math.exp(-k / (RATE * 0.0125)));
};
const whoosh = (add, at, seconds = 0.5, gain = 0.1) => {
  const noise = seeded(at + 1);
  let y = 0;
  const n = RATE * seconds;
  for (let k = 0; k < n; k++) {
    const e = Math.sin((Math.PI * k) / n) ** 2;
    y += (0.01 + 0.2 * e) * (noise() - y);
    add(at + k, gain * y * e);
  }
};
const thud = (add, at) => {
  for (let k = 0; k < RATE * 0.45; k++) add(at + k, 0.07 * Math.sin((2 * Math.PI * (70 + 40 * Math.exp(-k / (RATE * 0.03))) * k) / RATE) * Math.exp(-k / (RATE * 0.09)));
};

export const writeSound = (events, frames, fps, out) => {
  const n = Math.ceil((frames / fps) * RATE);
  const data = new Float32Array(n);
  const add = (i, value) => {
    if (i >= 0 && i < n) data[i] += value;
  };
  const fade = RATE * 1.5;
  for (let k = 0; k < n; k++) {
    const s = k / RATE;
    const env = Math.min(1, k / fade, (n - k) / fade) * (0.75 + 0.25 * Math.sin(2 * Math.PI * 0.07 * s));
    data[k] += env * BED * (Math.sin(2 * Math.PI * 55 * s) + 0.6 * Math.sin(2 * Math.PI * 82.4 * s + 0.4 * Math.sin(2 * Math.PI * 0.11 * s)));
  }
  for (const {at, kind} of events) {
    const start = Math.round((at / fps) * RATE);
    if (kind === 'tick') tick(add, start);
    if (kind === 'whoosh') whoosh(add, start);
    if (kind === 'thud') thud(add, start);
  }
  const body = Buffer.alloc(n * 2);
  for (let k = 0; k < n; k++) body.writeInt16LE(Math.max(-32767, Math.min(32767, Math.round(data[k] * 32767))), k * 2);
  const head = Buffer.alloc(44);
  head.write('RIFF', 0);
  head.writeUInt32LE(36 + body.length, 4);
  head.write('WAVEfmt ', 8);
  head.writeUInt32LE(16, 16);
  head.writeUInt16LE(1, 20);
  head.writeUInt16LE(1, 22);
  head.writeUInt32LE(RATE, 24);
  head.writeUInt32LE(RATE * 2, 28);
  head.writeUInt16LE(2, 32);
  head.writeUInt16LE(16, 34);
  head.write('data', 36);
  head.writeUInt32LE(body.length, 40);
  writeFileSync(out, Buffer.concat([head, body]));
};
