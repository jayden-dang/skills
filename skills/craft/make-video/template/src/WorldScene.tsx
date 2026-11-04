import {Easing, interpolate, interpolateColors, useCurrentFrame} from 'remotion';
import {linesOf} from './fit';
import {clamp} from './GraphicScenes';
import {Scene, WorldArrow, WorldCamera, WorldChange, WorldObject} from './timing';
import {t} from './tokens';

/* One world for the whole explanation. Things stay on screen and change, so the eye never has to find its place again. */

type Props = {scene: Scene; starts: number[]; lengths: number[]};

export const WORLD_W = 1780;
export const WORLD_H = 740;
const MOVE = 22;
const EASE = Easing.bezier(0.45, 0, 0.2, 1);

const FONT: Record<string, number> = {card: 38, pill: 34, seat: 26, code: 31, note: 36};
const toneOf = (tone?: string) => (tone === 'accent' ? t.accent : tone === 'bad' ? t.bad : tone === 'muted' ? t.muted : t.ink);

type State = Required<Pick<WorldObject, 'x' | 'y' | 'w' | 'h'>> & WorldObject;
type Frame = {objects: Record<string, State>; arrows: WorldArrow[]; camera: WorldCamera};
const WHOLE: WorldCamera = {x: 0, y: 0, w: WORLD_W, h: WORLD_H};

// What the world looks like after each change: a change touches only what it names. A beat may hold a
// second change, `then`, part way through its line, so a long line does not sit on one still frame.
const framesOf = (scene: Scene) => {
  const objects: Record<string, State> = {};
  for (const o of scene.objects ?? []) objects[o.id] = {hidden: true, ...o} as State;
  let now: Frame = {objects, arrows: [], camera: WHOLE};
  const apply = (change: WorldChange) => {
    const next: Record<string, State> = {...now.objects};
    for (const [id, set] of Object.entries(change.set ?? {})) {
      if (!next[id]) throw new Error(`${scene.id}: a beat sets "${id}", which is not one of the objects.`);
      next[id] = {...next[id], hidden: false, ...set};
    }
    now = {objects: next, arrows: change.arrows ?? now.arrows, camera: change.camera ?? now.camera};
    return now;
  };
  const frames: Frame[] = [now];
  const marks: {beat: number; after: number}[] = [];
  scene.beats.forEach((beat, i) => {
    frames.push(apply(beat.world ?? {}));
    marks.push({beat: i, after: 0});
    if (beat.world?.then) {
      frames.push(apply(beat.world.then));
      marks.push({beat: i, after: beat.world.then.after});
    }
  });
  return {frames, marks};
};

const checkFit = (scene: Scene) => {
  for (const o of scene.objects ?? []) {
    const size = o.size ?? FONT[o.shape];
    const texts = [o.label, ...Object.values(scene.beats.map((b) => b.world?.set?.[o.id]?.label))];
    for (const text of texts) {
      if (!text || o.shape === 'code') continue;
      const lines = linesOf(text, size, o.w - 28, {font: t.fontSans, weight: 600});
      if (lines * size * 1.2 > o.h - (o.sub ? size : 0)) throw new Error(`${scene.id}: "${text}" does not fit ${o.id}. Make it larger or the text shorter.`);
    }
  }
};

export const worldSize = (scene: Scene) => {
  checkFit(scene);
  return {w: WORLD_W, h: WORLD_H};
};

const between = (a: number | undefined, b: number | undefined, p: number) => (a ?? 0) + ((b ?? 0) - (a ?? 0)) * p;

const Thing: React.FC<{from: State; to: State; p: number; pulse: number}> = ({from, to, p, pulse}) => {
  const box = {x: between(from.x, to.x, p), y: between(from.y, to.y, p), w: between(from.w, to.w, p), h: between(from.h, to.h, p)};
  const opacity = between(from.hidden ? 0 : 1, to.hidden ? 0 : 1, p);
  if (opacity <= 0) return null;
  const color = interpolateColors(p, [0, 1], [toneOf(from.tone), toneOf(to.tone)]);
  const size = to.size ?? FONT[to.shape];
  const quiet = to.shape === 'note';
  const round = to.shape === 'pill' ? 999 : t.radiusSmall;
  const filled = to.fill && !quiet;
  const text = (value: string | undefined, o: number, key: string) =>
    value ? (
      <div key={key} style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', justifyContent: to.head ? 'flex-start' : 'center', alignItems: to.shape === 'code' || quiet ? 'flex-start' : 'center', padding: to.head ? '18px 14px 0' : '0 14px', opacity: o, textAlign: to.shape === 'code' || quiet ? 'left' : 'center'}}>
        <div style={{fontFamily: to.shape === 'code' ? t.fontMono : t.fontSans, fontSize: size, fontWeight: quiet ? 500 : 600, lineHeight: 1.2, whiteSpace: to.shape === 'code' ? 'pre' : 'normal', color: filled ? t.panelSoft : color}}>{value}</div>
        {to.sub ? <div style={{fontFamily: t.fontMono, fontSize: Math.round(size * 0.62), color: filled ? t.panelSoft : t.muted, marginTop: 4}}>{to.sub}</div> : null}
      </div>
    ) : null;
  return (
    <div style={{position: 'absolute', left: box.x, top: box.y, width: box.w, height: box.h, opacity, boxSizing: 'border-box', borderRadius: round, background: filled ? color : quiet ? 'transparent' : t.panelSoft, border: quiet ? 'none' : `${Math.max(t.borderWidth, 2)}px solid ${color}`, scale: String(1 + 0.05 * pulse)}}>
      {from.label !== to.label ? text(from.label, Math.max(0, 1 - 2 * p), 'old') : null}
      {text(to.label, from.label !== to.label ? Math.max(0, 2 * p - 1) : 1, 'new')}
    </div>
  );
};

const center = (o: State) => ({x: o.x + o.w / 2, y: o.y + o.h / 2});
// Where the line from this box's center toward a point leaves the box.
const edge = (o: State, toward: {x: number; y: number}) => {
  const c = center(o);
  const dx = toward.x - c.x;
  const dy = toward.y - c.y;
  const s = Math.min(dx ? o.w / 2 / Math.abs(dx) : Infinity, dy ? o.h / 2 / Math.abs(dy) : Infinity);
  return {x: c.x + dx * s, y: c.y + dy * s};
};

export const WorldScene: React.FC<Props> = ({scene, starts, lengths}) => {
  const frame = useCurrentFrame();
  const {frames, marks} = framesOf(scene);
  const times = marks.map((m) => starts[m.beat] + Math.round(lengths[m.beat] * m.after));
  const step = times.reduce((last, at, i) => (frame >= at ? i : last), -1) + 1;
  const to = frames[step];
  const from = frames[Math.max(0, step - 1)];
  const at = step === 0 ? 0 : times[step - 1];
  const p = step === 0 ? 1 : interpolate(frame, [at, at + MOVE], [0, 1], {...clamp, easing: EASE});
  const pulse = step === 0 ? 0 : interpolate(frame, [at, at + 12, at + 34], [0, 1, 0], clamp);
  const camera = {x: between(from.camera.x, to.camera.x, p), y: between(from.camera.y, to.camera.y, p), w: between(from.camera.w, to.camera.w, p), h: between(from.camera.h, to.camera.h, p)};
  const zoom = Math.min(WORLD_W / camera.w, WORLD_H / camera.h);
  const live = (id: string): State => {
    const a = from.objects[id];
    const b = to.objects[id];
    if (!b) throw new Error(`${scene.id}: an arrow names "${id}", which is not one of the objects.`);
    return {...b, x: between(a.x, b.x, p), y: between(a.y, b.y, p), w: between(a.w, b.w, p), h: between(a.h, b.h, p)};
  };
  const kept = (a: WorldArrow) => from.arrows.some((o) => o.from === a.from && o.to === a.to);
  return (
    <div style={{position: 'absolute', inset: 0, overflow: 'hidden'}}>
      <div style={{position: 'absolute', left: 0, top: 0, width: WORLD_W, height: WORLD_H, transformOrigin: '0 0', transform: `translate(${(WORLD_W - camera.w * zoom) / 2 - camera.x * zoom}px, ${(WORLD_H - camera.h * zoom) / 2 - camera.y * zoom}px) scale(${zoom})`}}>
        {Object.keys(to.objects).map((id) => {
          const changed = JSON.stringify(from.objects[id]) !== JSON.stringify(to.objects[id]);
          return <Thing key={id} from={from.objects[id]} to={to.objects[id]} p={p} pulse={changed && !from.objects[id].hidden ? pulse : 0} />;
        })}
        <svg width={WORLD_W} height={WORLD_H} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
          {to.arrows.map((a) => {
            const [s, e] = [live(a.from), live(a.to)];
            const start = edge(s, center(e));
            const end = edge(e, center(s));
            const grow = kept(a) ? 1 : p;
            const tip = {x: start.x + (end.x - start.x) * grow, y: start.y + (end.y - start.y) * grow};
            const angle = Math.atan2(end.y - start.y, end.x - start.x);
            const wing = (turn: number) => `${tip.x - 16 * Math.cos(angle + turn)} ${tip.y - 16 * Math.sin(angle + turn)}`;
            return (
              <g key={`${a.from}-${a.to}`}>
                <line x1={start.x} y1={start.y} x2={tip.x} y2={tip.y} stroke={t.accent} strokeWidth={4} strokeLinecap="round" />
                {grow === 1 ? <path d={`M${wing(0.5)} L${tip.x} ${tip.y} L${wing(-0.5)}`} fill="none" stroke={t.accent} strokeWidth={4} strokeLinecap="round" strokeLinejoin="round" /> : null}
                {a.label ? <text x={(start.x + end.x) / 2} y={(start.y + end.y) / 2 - 14} textAnchor="middle" fontFamily={t.fontMono} fontSize={26} fontWeight={600} fill={t.accent} opacity={grow}>{a.label}</text> : null}
              </g>
            );
          })}
        </svg>
      </div>
    </div>
  );
};
