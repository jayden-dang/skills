import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import {fit, headFace, linesOf, wrap} from './fit';
import {Letters} from './Look';
import {Scene, wordStarts} from './timing';
import {t} from './tokens';

type Props = {scene: Scene; starts: number[]; lengths: number[]};

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const OUT = Easing.bezier(0.16, 1, 0.3, 1);
export const enter = (frame: number, at: number, length = 18) => interpolate(frame, [at, at + length], [0, 1], {...clamp, easing: OUT});

const MAX_H = 840;
const head = {fontFamily: t.fontHead, fontWeight: t.headWeight, letterSpacing: t.headTracking};

/* The window hugs its text, so each scene measures before it draws. */

const titleMetrics = (scene: Scene) => {
  const w = 1500;
  const title = fit(scene.id, scene.title, [104, 88, 74, 62], w - 120, 2, headFace);
  const sub = scene.subtitle ? fit(scene.id, scene.subtitle, [36, 32], w - 120, 2) : null;
  const h = Math.max(340, 150 + title.lines * title.size * 1.05 + (sub ? 24 + sub.lines * sub.size * 1.2 : 0));
  return {w, h, title, sub};
};

// Up to eight points, in two columns past five, so a list and its context share one screen.
const pointsMetrics = (scene: Scene) => {
  const points = scene.points ?? [];
  const cols = points.length > 5 ? 2 : 1;
  const w = points.length > 3 ? 1640 : 1500;
  const colW = (w - 144 - (cols - 1) * 56) / cols;
  const title = fit(scene.id, scene.title, [56, 48], w - 144, 2, headFace);
  const titleH = title.lines * title.size * 1.1 + 28;
  const perCol = Math.ceil(points.length / cols);
  for (const size of [44, 40, 36, 32, 28]) {
    const rows = points.map((p) => fit(scene.id, p, [size], colW - 46, 2).lines * size * 1.15 + size * 0.8);
    const tallest = Math.max(0, ...Array.from({length: cols}, (_, c) => rows.slice(c * perCol, (c + 1) * perCol).reduce((a, b) => a + b, 0)));
    const h = 112 + titleH + tallest;
    if (h <= MAX_H) return {w, h, title, size, rows, cols, colW, perCol};
  }
  throw new Error(`${scene.id}: too many points for one scene. Split it.`);
};

const flowMetrics = (scene: Scene) => {
  const w = 1560;
  const title = fit(scene.id, scene.title, [56, 48], w - 144, 2, headFace);
  const top = 60 + title.lines * title.size * 1.1 + 40;
  return {w, h: 720, title, top};
};

export const graphicSize = (scene: Scene) => {
  if (scene.kind === 'title') return titleMetrics(scene);
  if (scene.kind === 'points') return pointsMetrics(scene);
  return flowMetrics(scene);
};

// The title rises letter by letter, a later line and the subtitle on later words of the first line, so a long
// opening line does not stand still: a two-line title that only faded in held 5.1s.
export const TitleScene: React.FC<Props> = ({scene, starts, lengths}) => {
  const frame = useCurrentFrame();
  const {w, title, sub} = titleMetrics(scene);
  const lines = wrap(scene.title, title.size, w - 120, headFace);
  const words = wordStarts(scene, 0, lengths[0]);
  const at = (share: number) => starts[0] + words[Math.min(words.length - 1, Math.floor(words.length * share))];
  const lineStart = (i: number) => (i === 0 ? 8 : Math.max(8 + i * 14, at((0.35 * i) / Math.max(1, lines.length - 1))));
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', textAlign: 'center', padding: '0 60px'}}>
      {lines.map((line, i) => <Letters key={i} text={line} start={lineStart(i)} size={title.size} />)}
      {sub ? <div style={{fontSize: sub.size, fontWeight: 500, lineHeight: 1.2, color: t.muted, marginTop: 24, textWrap: 'balance', opacity: enter(frame, Math.max(18, at(0.6)), 22)}}>{scene.subtitle}</div> : null}
    </AbsoluteFill>
  );
};

// A point arrives on its beat. Extra points arrive evenly through the last beat.
export const pointAt = (starts: number[], lengths: number[], count: number, i: number) => {
  const last = starts.length - 1;
  if (i < last || count <= starts.length) return starts[Math.min(i, last)];
  return starts[last] + (i - last) * (lengths[last] / (count - last));
};

export const PointsScene: React.FC<Props> = ({scene, starts, lengths}) => {
  const frame = useCurrentFrame();
  const {title, size, rows, cols, colW, perCol} = pointsMetrics(scene);
  const points = scene.points ?? [];
  return (
    <div style={{position: 'absolute', inset: 0, padding: '56px 72px', boxSizing: 'border-box'}}>
      <div style={{...head, fontSize: title.size, lineHeight: 1.1, marginBottom: 28, opacity: enter(frame, 6, 20)}}>{scene.title}</div>
      <div style={{display: 'grid', gridTemplateColumns: `repeat(${cols}, ${colW}px)`, gridTemplateRows: `repeat(${perCol}, auto)`, gridAutoFlow: 'column', columnGap: 56, alignItems: 'start'}}>
      {points.map((p, i) => {
        const shown = enter(frame, pointAt(starts, lengths, points.length, i), 16);
        return (
          <div key={p} style={{display: 'flex', alignItems: 'center', height: rows[i], fontSize: size, fontWeight: 550, lineHeight: 1.15, letterSpacing: '-0.01em', opacity: 0.16 + 0.84 * shown, translate: `${(shown - 1) * 14}px 0px`}}>
            <div style={{width: 16, height: 16, borderRadius: t.radius === 0 ? 0 : 99, background: t.accent, marginRight: 30, flexShrink: 0, opacity: shown}} />
            {p}
          </div>
        );
      })}
      </div>
    </div>
  );
};

export const FlowScene: React.FC<Props> = ({scene, starts}) => {
  const frame = useCurrentFrame();
  const {w, h, title, top} = flowMetrics(scene);
  const sources = scene.sources ?? [];
  const width = w - 144;
  const height = h - top - 40;
  const chipW = width * 0.34;
  const chipH = Math.min(96, (height / Math.max(1, sources.length)) * 0.82);
  const spread = sources.length > 1 ? Math.min((height - chipH) / (sources.length - 1), 150) : 0;
  const midY = height / 2;
  const y = (i: number) => midY + (i - (sources.length - 1) / 2) * spread;
  const targetX = width * 0.66;
  const targetW = width - targetX;
  const target = fit(scene.id, scene.target ?? '', [120, 96, 76, 60, 48], targetW, 2, headFace);
  const note = scene.note ? fit(scene.id, scene.note, [30, 26], targetW, 3) : null;
  const targetP = enter(frame, starts[0] + 24);
  const labelSize = [36, 30, 26].find((size) => sources.every((s) => {
    const lines = linesOf(s, size, chipW - 52);
    return lines <= 2 && lines * size * 1.1 <= chipH - 14;
  }));
  if (!labelSize) throw new Error(`${scene.id}: the sources do not fit. Shorten them, or use fewer.`);
  return (
    <div style={{position: 'absolute', inset: 0}}>
      <div style={{...head, position: 'absolute', left: 72, right: 72, top: 56, fontSize: title.size, lineHeight: 1.1, opacity: enter(frame, 6, 20)}}>{scene.title}</div>
      <div style={{position: 'absolute', left: 72, top, width, height}}>
        <svg width={width} height={height} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
          {sources.map((_, i) => {
            const at = starts[Math.min(i, starts.length - 1)];
            const p = interpolate(frame, [at + 6, at + 26], [0, 1], {...clamp, easing: Easing.bezier(0.45, 0, 0.3, 1)});
            return <path key={i} d={`M${chipW} ${y(i)} C ${chipW + 136} ${y(i)}, ${targetX - 154} ${midY}, ${targetX - 10} ${midY}`} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - p} fill="none" stroke={t.accent} strokeWidth={4} strokeLinecap="round" opacity={p > 0 ? 1 : 0} />;
          })}
        </svg>
        {sources.map((s, i) => {
          const p = enter(frame, starts[Math.min(i, starts.length - 1)]);
          return (
            <div key={s} style={{position: 'absolute', left: 0, top: y(i) - chipH / 2, width: chipW, height: chipH, boxSizing: 'border-box', padding: '0 26px', display: 'flex', alignItems: 'center', borderRadius: t.radiusSmall, background: t.panelSoft, border: `${t.borderWidth}px solid ${t.panelBorder}`, color: t.ink, fontSize: labelSize, fontWeight: 600, lineHeight: 1.1, opacity: p, translate: `${(p - 1) * 24}px 0px`}}>
              {s}
            </div>
          );
        })}
        <div style={{...head, position: 'absolute', left: targetX, top: midY - (target.lines * target.size * 1.02) / 2 - (note ? 30 : 0), width: targetW, fontSize: target.size, lineHeight: 1.02, color: t.accent, opacity: targetP, scale: String(0.92 + 0.08 * targetP)}}>{scene.target}</div>
        {note ? <div style={{position: 'absolute', left: targetX, top: midY + (target.lines * target.size * 1.02) / 2 - 12, width: targetW, color: t.muted, fontSize: note.size, fontWeight: 500, lineHeight: 1.22, opacity: enter(frame, starts[starts.length - 1])}}>{scene.note}</div> : null}
      </div>
    </div>
  );
};
