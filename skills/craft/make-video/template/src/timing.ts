import clips from './clips.json';
import script from './script.json';
import voice from './voice.json';

export const FPS = 30;
export const TRANSITION = 14;

export type Rect = {x: number; y: number; w: number; h: number};
export type Beat = {text: string; ref: string; clip?: string; rate?: number; focus?: Rect; ring?: Rect};
export type Scene = {
  id: string;
  kind: 'title' | 'points' | 'flow' | 'clip';
  title: string;
  subtitle?: string;
  staged?: string;
  points?: string[];
  sources?: string[];
  target?: string;
  note?: string;
  beats: Beat[];
};

export const scenes = (script as unknown as {scenes: Scene[]}).scenes;
const clipFrames = clips as unknown as Record<string, {frames: number}>;
const voiceFrames = voice as unknown as Record<string, number[]>;

const PACE: Record<Scene['kind'], {head: number; gap: number; tail: number}> = {
  title: {head: 24, gap: 10, tail: 28},
  points: {head: 20, gap: 10, tail: 24},
  flow: {head: 22, gap: 12, tail: 28},
  clip: {head: 8, gap: 8, tail: 18},
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

export const totalFrames = () => {
  const last = placed[placed.length - 1];
  return last ? last.from + last.duration : 0;
};
