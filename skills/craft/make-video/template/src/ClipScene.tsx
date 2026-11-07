import {Video} from '@remotion/media';
import {Easing, Img, interpolate, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {clipLength, Rect, Scene} from './timing';
import {t} from './tokens';

// Recordings are driven at this CSS size; focus and ring rects use its pixels.
const VIEW_W = 1600;
const K = 1920 / VIEW_W;
export const CLIP_W = 1540;
// A full scene fills the frame between the two bands, edge to edge, with no window.
export const FULL = {x: 0, y: 72, w: 1920, h: 912};
type Fit = {w: number; maxH: number; minH: number; u: number};
const WINDOWED: Fit = {w: CLIP_W, maxH: (CLIP_W * 9) / 16, minH: 300, u: CLIP_W / 1920};
const FILLED: Fit = {w: FULL.w, maxH: FULL.h, minH: FULL.h, u: 1};
const fitOf = (scene: Scene) => (scene.full ? FILLED : WINDOWED);
export const MOVE = 24;
export const MOVE_EASING = Easing.bezier(0.5, 0, 0.1, 1);
const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

type View = {h: number; s: number; x: number; y: number};

// What the window shows for one rect. It keeps only as much height as the rect needs, so the app's
// empty space below a short subject stays out of the film.
const viewOf = (focus: Rect | undefined, {maxH: CLIP_MAX_H, minH: CLIP_MIN_H, u: U}: Fit): View => {
  if (!focus) return {h: CLIP_MAX_H, s: 1, x: 0, y: 0};
  const fw = focus.w * K;
  const fh = focus.h * K;
  const s = Math.max(1, Math.min(3, (1920 * 0.92) / fw, (CLIP_MAX_H / U) * (0.86 / fh)));
  const h = Math.max(CLIP_MIN_H, Math.min(CLIP_MAX_H, ((fh * s) / 0.86) * U));
  const visible = h / U;
  const limit = (v: number, low: number) => Math.min(0, Math.max(low, v));
  return {
    h,
    s,
    x: limit(960 - s * (focus.x + focus.w / 2) * K, 1920 - 1920 * s),
    y: limit(visible / 2 - s * (focus.y + focus.h / 2) * K, visible - 1080 * s),
  };
};

// One view per line. A line with no focus keeps the view before it.
const viewsOf = (scene: Scene) => {
  const fit = fitOf(scene);
  let previous = viewOf(undefined, fit);
  return scene.beats.map((beat) => (previous = beat.focus ? viewOf(beat.focus, fit) : previous));
};

export const clipHeights = (scene: Scene) => viewsOf(scene).map((view) => view.h);

// Plays inside the window; everything here is drawn at 1920x1080 and scaled down.
export const ClipScene: React.FC<{scene: Scene; starts: number[]; lengths: number[]; duration: number}> = ({scene, starts, lengths, duration}) => {
  const frame = useCurrentFrame();
  const views = viewsOf(scene);
  const input: number[] = [];
  const values: View[] = [];
  let current = views[0];
  views.forEach((view, i) => {
    if (i === 0) return;
    const start = Math.max(starts[i], (input[input.length - 1] ?? -1) + 1);
    input.push(start, start + MOVE);
    values.push(current, view);
    current = view;
  });
  const at = (key: 's' | 'x' | 'y') => (input.length ? interpolate(frame, input, values.map((v) => v[key]), {...clamp, easing: MOVE_EASING}) : views[0][key]);
  const entries = scene.beats.flatMap((beat, i) => (beat.clip ? [{beat, from: starts[i]}] : []));
  return (
    <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transformOrigin: '0 0', scale: String(fitOf(scene).u)}}>
      <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transformOrigin: '0 0', translate: `${at('x')}px ${at('y')}px`, scale: String(at('s'))}}>
        {entries.map(({beat, from}, i) => {
          const until = entries[i + 1]?.from ?? duration;
          return (
            <Sequence key={`${beat.clip}-${from}`} from={from} durationInFrames={until - from} layout="none" name={beat.clip}>
              <Img src={staticFile(`clips/${beat.clip}-last.png`)} style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080}} />
              <Sequence durationInFrames={clipLength(beat)} layout="none">
                <Video muted playbackRate={beat.rate ?? 1} src={staticFile(`clips/${beat.clip}.mp4`)} style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080}} />
              </Sequence>
            </Sequence>
          );
        })}
        {scene.beats.map((beat, i) => {
          if (!beat.ring) return null;
          const from = starts[i];
          const to = from + lengths[i] + 6;
          return (
            <div
              key={`ring-${i}`}
              style={{
                position: 'absolute',
                left: beat.ring.x * K - 6,
                top: beat.ring.y * K - 6,
                width: beat.ring.w * K + 12,
                height: beat.ring.h * K + 12,
                borderRadius: t.radiusSmall,
                border: `3px solid ${t.accent}`,
                opacity: interpolate(frame, [from + 8, from + 14, to - 6, to], [0, 1, 1, 0], clamp),
              }}
            />
          );
        })}
      </div>
    </div>
  );
};
