import clips from './clips.json';
import script from './script.json';
import voice from './voice.json';

export const FPS = 30;
export const TRANSITION = 14;

export type Rect = {x: number; y: number; w: number; h: number};
export type WorldObject = {id: string; shape: 'card' | 'pill' | 'seat' | 'code' | 'note'; x: number; y: number; w: number; h: number; label?: string; sub?: string; tone?: 'ink' | 'accent' | 'bad' | 'muted'; fill?: boolean; head?: boolean; size?: number; hidden?: boolean};
export type WorldArrow = {from: string; to: string; label?: string};
export type WorldCamera = Rect;
export type WorldChange = {set?: Record<string, Partial<WorldObject>>; arrows?: WorldArrow[]; camera?: WorldCamera};
export type Beat = {text: string; spoken?: string; ref: string; clip?: string; rate?: number; focus?: Rect; ring?: Rect; mark?: number[]; world?: WorldChange & {then?: WorldChange & {after: number}}};
export type Scene = {
  id: string;
  kind: 'title' | 'points' | 'flow' | 'clip' | 'ears' | 'sequence' | 'code' | 'table' | 'world';
  title: string;
  subtitle?: string;
  staged?: string;
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
  beats: Beat[];
};

export const scenes = (script as unknown as {scenes: Scene[]}).scenes;
export const planned = (script as unknown as {planned?: string}).planned;
const clipFrames = clips as unknown as Record<string, {frames: number}>;
const voiceFrames = voice as unknown as Record<string, number[]>;

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
};

export const clipLength = (beat: Beat) => (beat.clip ? Math.ceil(clipFrames[beat.clip].frames / (beat.rate ?? 1)) : 0);

export const layout = (scene: Scene) => {
  const pace = PACE[scene.kind];
  const lengths = voiceFrames[scene.id] ?? scene.beats.map(() => 60);
  const starts: number[] = [];
  let at = pace.head;
  let clipEnd = 0;
  scene.beats.forEach((beat, i) => {
    const start = beat.clip ? Math.max(at, clipEnd) : at;
    starts.push(start);
    if (beat.clip) clipEnd = start + clipLength(beat);
    at = start + lengths[i] + pace.gap;
  });
  const last = starts.length - 1;
  return {starts, lengths, duration: Math.max(starts[last] + lengths[last] + pace.tail, clipEnd + 10)};
};

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

export const totalFrames = () => {
  const last = placed[placed.length - 1];
  return last ? last.from + last.duration : 0;
};
