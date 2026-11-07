import clips from './clips.json';
import script from './script.json';
import voice from './voice.json';
import words from './words.json';

export const FPS = 30;
export const TRANSITION = 14;
// A rested line in a concept film: the picture stands this long after the words, while the viewer thinks.
export const REST = 75;

export type Rect = {x: number; y: number; w: number; h: number};
export type Tone = 'ink' | 'accent' | 'warn' | 'bad' | 'muted';
export type WorldObject = {id: string; shape: 'card' | 'row' | 'seat' | 'code' | 'note'; x: number; y: number; w: number; h: number; label?: string; sub?: string; subTone?: Tone; index?: string; tone?: Tone; fill?: boolean; head?: boolean; size?: number; timer?: number; hidden?: boolean};
export type WorldArrow = {from: string; to: string; label?: string; tone?: Tone};
export type WorldCamera = Rect;
export type WorldChange = {set?: Record<string, Partial<WorldObject>>; arrows?: WorldArrow[]; camera?: WorldCamera; stats?: Record<string, number | string>};
export type Beat = {text: string; spoken?: string; ref: string; rest?: boolean; side?: 'before' | 'after'; clip?: string; rate?: number; focus?: Rect; ring?: Rect; mark?: number[]; world?: WorldChange & {then?: (WorldChange & {at: string})[]}};
export type Scene = {
  id: string;
  kind: 'title' | 'points' | 'flow' | 'clip' | 'ears' | 'sequence' | 'code' | 'table' | 'world' | 'manim' | 'compare' | 'stat' | 'timeline';
  title: string;
  subtitle?: string;
  staged?: string;
  full?: boolean;
  points?: string[];
  sources?: string[];
  target?: string;
  note?: string;
  rules?: {id: string; text: string}[];
  actors?: string[];
  steps?: {from: string; to: string; label: string}[];
  file?: string;
  lines?: string[];
  columns?: string[];
  rows?: string[][];
  objects?: WorldObject[];
  before?: string;
  after?: string;
  labels?: string[];
  rate?: number;
  stats?: {value: string; label: string}[];
  events?: {label: string; note?: string}[];
  beats: Beat[];
};

const held = script as unknown as {name?: string; planned?: string; scenes: Scene[]};
export const scenes = held.scenes;
export const planned = held.planned;
export const filmName = held.name;
const clipFrames = clips as unknown as Record<string, {frames: number}>;
const voiceFrames = voice as unknown as Record<string, number[]>;
const wordFrames = words as unknown as Record<string, number[][]>;

const PACE: Record<Scene['kind'], {head: number; gap: number; tail: number}> = {
  title: {head: 24, gap: 10, tail: 28},
  points: {head: 20, gap: 10, tail: 24},
  flow: {head: 22, gap: 12, tail: 28},
  clip: {head: 8, gap: 8, tail: 18},
  ears: {head: 18, gap: 8, tail: 20},
  sequence: {head: 18, gap: 8, tail: 20},
  code: {head: 18, gap: 8, tail: 20},
  table: {head: 18, gap: 8, tail: 20},
  world: {head: 18, gap: 10, tail: 30},
  manim: {head: 18, gap: 10, tail: 30},
  compare: {head: 8, gap: 8, tail: 18},
  stat: {head: 20, gap: 10, tail: 24},
  timeline: {head: 20, gap: 10, tail: 24},
};

export const clipLength = (beat: Beat) => (beat.clip ? Math.ceil(clipFrames[beat.clip].frames / (beat.rate ?? 1)) : 0);

export const layout = (scene: Scene) => {
  const pace = PACE[scene.kind];
  const lengths = voiceFrames[scene.id] ?? scene.beats.map((b) => Math.max(45, b.text.split(' ').length * 12));
  const starts: number[] = [];
  let at = pace.head;
  let clipEnd = 0;
  scene.beats.forEach((beat, i) => {
    const start = beat.clip ? Math.max(at, clipEnd) : at;
    starts.push(start);
    if (beat.clip) clipEnd = start + clipLength(beat);
    at = start + lengths[i] + pace.gap + (beat.rest ? REST : 0);
  });
  const last = starts.length - 1;
  // A compare plays both recordings from its first line, so it lasts at least as long as the longer one.
  if (scene.kind === 'compare') clipEnd = starts[0] + Math.max(...[scene.before, scene.after].map((c) => (c && clipFrames[c] ? Math.ceil(clipFrames[c].frames / (scene.rate ?? 1)) : 0)));
  return {starts, lengths, duration: Math.max(starts[last] + lengths[last] + pace.tail + (scene.beats[last].rest ? REST : 0), clipEnd + 10)};
};

// Where each word of a line starts, in frames from the line's start: measured by voice.py, shared evenly before there is a voice.
export const wordStarts = (scene: Scene, beat: number, length: number) => {
  const count = scene.beats[beat].text.split(/\s+/).length;
  const measured = wordFrames[scene.id]?.[beat];
  return measured && measured.length === count ? measured : Array.from({length: count}, (_, i) => Math.round((length * i) / count));
};

const bare = (text: string) => text.split(/\s+/).map((w) => w.replace(/^[^\p{L}\p{N}]+|[^\p{L}\p{N}]+$/gu, '').toLowerCase());

// The word of a line that a phrase starts on.
export const phraseAt = (scene: Scene, beat: number, phrase: string) => {
  const line = bare(scene.beats[beat].text);
  const wanted = bare(phrase);
  for (let i = 0; i <= line.length - wanted.length; i++) {
    if (wanted.every((w, k) => line[i + k] === w)) return i;
  }
  throw new Error(`${scene.id}-${beat}: "${phrase}" is not in the line.`);
};

// Every change a world makes, in order, with the frame it lands on inside its scene.
export const worldSteps = (scene: Scene, starts: number[], lengths: number[]) =>
  scene.beats.flatMap((beat, i) => {
    const times = wordStarts(scene, i, lengths[i]);
    const {then, ...first} = beat.world ?? {};
    return [
      {change: first as WorldChange, at: starts[i], beat: i},
      ...(then ?? []).map((step) => ({change: step as WorldChange, at: starts[i] + times[phraseAt(scene, i, step.at)], beat: i})),
    ];
  });

// Each scene with its absolute start. Neighbours overlap by TRANSITION.
export const placed = (() => {
  let from = 0;
  return scenes.map((scene) => {
    const entry = {scene, from, ...layout(scene)};
    from += entry.duration - TRANSITION;
    return entry;
  });
})();

// The last moment of every line: what the preview and the contact sheet show.
export const beatFrames = () => placed.flatMap(({from, starts, lengths}) => starts.map((start, i) => from + start + lengths[i] - 4));

// Where each scene starts and what it cites: the index beside a finished film.
export const sceneIndex = () =>
  placed.map(({scene, from}) => ({id: scene.id, title: scene.title, seconds: Math.round(from / FPS), refs: scene.beats.map((b) => b.ref).join(', ')}));

// What a Manim scene times itself to: preview.mjs writes it to out/timing.json, and render_manim.py reads it.
export const sceneTiming = () =>
  Object.fromEntries(placed.map(({scene, duration, starts, lengths}) => [scene.id, {duration, starts, lengths, words: scene.beats.map((_, i) => wordStarts(scene, i, lengths[i]))}]));

// The pause after each rested line, in film frames: preview.mjs writes them to out/rests.json for the check.
export const restWindows = () =>
  placed.flatMap(({scene, from, starts, lengths}) => scene.beats.flatMap((beat, i) => (beat.rest ? [[from + starts[i] + lengths[i], from + starts[i] + lengths[i] + REST]] : [])));

export const totalFrames = () => {
  const last = placed[placed.length - 1];
  return last ? last.from + last.duration : 0;
};

// What the sound layer plays over the voice: a soft hit on each change, a heavier one when something goes wrong.
export type SoundEvent = {at: number; kind: 'tick' | 'whoosh' | 'thud'};
export const soundEvents = (): SoundEvent[] => {
  const events: SoundEvent[] = [{at: 0, kind: 'whoosh'}];
  for (const {scene, from, starts, lengths} of placed) {
    if (from > 0) events.push({at: from, kind: 'whoosh'});
    if (scene.kind !== 'world') {
      starts.forEach((start) => events.push({at: from + start, kind: 'tick'}));
      continue;
    }
    for (const {change, at} of worldSteps(scene, starts, lengths)) {
      const values = Object.values(change.set ?? {});
      if (values.some((v) => v.tone === 'bad' || v.subTone === 'bad')) events.push({at: from + at, kind: 'thud'});
      else if (change.arrows?.length) events.push({at: from + at, kind: 'whoosh'});
      else if (values.length || change.stats) events.push({at: from + at, kind: 'tick'});
    }
  }
  return events.sort((a, b) => a.at - b.at).filter((e, i, all) => i === 0 || e.at - all[i - 1].at >= 6);
};
