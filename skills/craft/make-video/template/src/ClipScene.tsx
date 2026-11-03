import {Video} from '@remotion/media';
import {AbsoluteFill, Easing, Img, interpolate, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {clipLength, Rect, Scene} from './timing';
import {t} from './tokens';

// Recordings are driven at this CSS size; focus and ring rects use its pixels.
const VIEW_W = 1600;
const VIEW_H = 900;
const K = 1920 / VIEW_W;
const VISIBLE_H = 910;
const MOVE = 26;

const camera = (focus?: Rect) => {
  if (!focus) return {s: 1, x: 0, y: 0};
  const s = Math.max(1, Math.min(3, (1920 * 0.86) / (focus.w * K), (VISIBLE_H * 0.86) / (focus.h * K)));
  const cx = (focus.x + focus.w / 2) * K;
  const cy = (focus.y + focus.h / 2) * K;
  const clamp = (v: number, low: number) => Math.min(0, Math.max(low, v));
  return {s, x: clamp(960 - s * cx, 1920 - 1920 * s), y: clamp(VISIBLE_H / 2 - s * cy, 1080 - VIEW_H * K * s)};
};

export const ClipScene: React.FC<{scene: Scene; starts: number[]; lengths: number[]; duration: number}> = ({scene, starts, lengths, duration}) => {
  const frame = useCurrentFrame();
  let previous = camera();
  const input: number[] = [];
  const values: {s: number; x: number; y: number}[] = [];
  scene.beats.forEach((beat, i) => {
    const target = beat.focus === undefined && i > 0 ? previous : camera(beat.focus);
    const from = i === 0 ? 0 : starts[i];
    const nextStart = i + 1 < starts.length ? starts[i + 1] : duration;
    input.push(from, Math.min(from + MOVE, Math.max(from + 1, nextStart - 1)));
    values.push(previous, target);
    previous = target;
  });
  const at = (key: 's' | 'x' | 'y') =>
    interpolate(frame, input, values.map((v) => v[key]), {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
      easing: Easing.bezier(0.33, 0, 0.2, 1),
    });
  const entries = scene.beats.flatMap((beat, i) => (beat.clip ? [{beat, from: starts[i]}] : []));
  return (
    <AbsoluteFill style={{overflow: 'hidden'}}>
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
                opacity: interpolate(frame, [from + 8, from + 14, to - 6, to], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}),
              }}
            />
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
