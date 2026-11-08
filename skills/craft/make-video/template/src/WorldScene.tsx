import {Easing, interpolate, useCurrentFrame} from 'remotion';
import {linesOf} from './fit';
import {Arc, clamp, cutShape, Decode, Edge, glide, Letters, Point, rise} from './Look';
import {LEAD, Scene, Tone, WorldArrow, WorldCamera, WorldChange, WorldObject, worldSteps} from './timing';
import {t} from './tokens';

/* One world for the whole explanation. Things stay on screen and change on the word that names the change, so the eye never has to find its place again. */

type Props = {scene: Scene; starts: number[]; lengths: number[]};

export const WORLD_W = 1800;
export const WORLD_H = 840;
const MOVE = 22;
const EASE = Easing.bezier(0.45, 0, 0.2, 1);

// Labels sized so a world holds more at once; code and notes stay at 30, the smallest a camera's widest view reads.
const FONT: Record<string, number> = {card: 38, head: 76, row: 50, seat: 46, code: 31, note: 30};
const toneOf = (tone?: Tone, fallback = t.ink) => (tone === 'accent' ? t.accent : tone === 'bad' ? t.bad : tone === 'warn' ? t.warn : tone === 'muted' ? t.muted : tone === 'ink' ? t.ink : fallback);
const sizeOf = (o: WorldObject) => o.size ?? (o.shape === 'card' && o.head ? FONT.head : FONT[o.shape]);

type State = Required<Pick<WorldObject, 'x' | 'y' | 'w' | 'h'>> & WorldObject;
type Frame = {objects: Record<string, State>; arrows: WorldArrow[]; camera: WorldCamera};
const WHOLE: WorldCamera = {x: 0, y: 0, w: WORLD_W, h: WORLD_H};
const NEVER = -100000;
type Since = {shown: number; label: number; sub: number; timer: number};

// What the world looks like after each change: a change touches only what it names. `since` keeps the
// frame each thing last changed on, so its entrance or its new label starts there.
const framesOf = (scene: Scene, starts: number[], lengths: number[]) => {
  let objects: Record<string, State> = {};
  const since: Record<string, Since> = {};
  for (const o of scene.objects ?? []) {
    objects[o.id] = {hidden: true, ...o} as State;
    since[o.id] = {shown: NEVER, label: NEVER, sub: NEVER, timer: NEVER};
  }
  let now: Frame = {objects, arrows: [], camera: WHOLE};
  const frames: Frame[] = [now];
  const sinces: Record<string, Since>[] = [since];
  const times: number[] = [];
  const steps = worldSteps(scene, starts, lengths);
  for (const {change, at} of steps) {
    const next: Record<string, State> = {...now.objects};
    const marks: Record<string, Since> = {...sinces[sinces.length - 1]};
    for (const [id, set] of Object.entries((change as WorldChange).set ?? {})) {
      if (!next[id]) throw new Error(`${scene.id}: a beat sets "${id}", which is not one of the objects.`);
      const was = next[id];
      next[id] = {...was, hidden: false, ...set};
      marks[id] = {
        shown: was.hidden && !next[id].hidden ? at : marks[id].shown,
        label: was.label !== next[id].label ? at : marks[id].label,
        sub: was.sub !== next[id].sub ? at : marks[id].sub,
        timer: was.timer !== next[id].timer ? at : marks[id].timer,
      };
    }
    objects = next;
    now = {objects, arrows: change.arrows ?? now.arrows, camera: change.camera ?? now.camera};
    frames.push(now);
    sinces.push(marks);
    times.push(at);
  }
  return {frames, sinces, times};
};

const checkFit = (scene: Scene) => {
  const beats = scene.beats.flatMap((b) => [b.world, ...(b.world?.then ?? [])]);
  for (const o of scene.objects ?? []) {
    const texts = [o.label, ...beats.map((b) => b?.set?.[o.id]?.label)];
    for (const text of texts) {
      if (!text || o.shape === 'code') continue;
      const size = sizeOf(o);
      const face = o.shape === 'note' ? {font: t.fontMono, weight: 400, tracking: 0.08} : {font: t.fontSans, weight: 400};
      const lines = linesOf(o.shape === 'note' ? text.toUpperCase() : text, size, o.w - 28, face);
      if (lines * size * 1.2 > o.h) throw new Error(`${scene.id}: "${text}" does not fit ${o.id}. Make it larger or the text shorter.`);
    }
  }
};

export const worldSize = (scene: Scene) => {
  checkFit(scene);
  return {w: WORLD_W, h: WORLD_H};
};

const between = (a: number | undefined, b: number | undefined, p: number) => (a ?? 0) + ((b ?? 0) - (a ?? 0)) * p;

const clockOf = (left: number) => `${String(Math.floor(left / 60)).padStart(2, '0')}:${String(left % 60).padStart(2, '0')}`;

type Drawn = {o: State; was: State; since: Since; p: number};

const Card: React.FC<Drawn> = ({o, since}) => {
  const frame = useCurrentFrame();
  const c = toneOf(o.tone, '');
  const draw = glide(frame, since.shown, 34);
  const fill = rise(frame, since.shown + 8, 30);
  const out = (1 - rise(frame, since.shown + 6, 30)) * 26 + 10;
  const size = sizeOf(o);
  const pad = 36;
  return (
    <>
      <div style={{position: 'absolute', inset: 0, opacity: fill, background: t.panel, clipPath: t.cut > 0 ? cutShape(o.w, o.h) : undefined, borderRadius: t.cut > 0 ? 0 : t.radius}} />
      <Edge id={`edge-${o.id}`} w={o.w} h={o.h} draw={draw} color={c || undefined} brackets={out} />
      {o.head ? (
        <div style={{position: 'absolute', left: pad, right: pad, top: 28, display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 24}}>
          <Letters key={since.label} text={o.label ?? ''} start={Math.max(since.shown + 6, since.label)} size={size} color={c || t.ink} />
          {o.sub ? (
            <span style={{flexShrink: 0, padding: o.subTone ? '8px 14px' : 0, border: o.subTone ? `1px solid ${toneOf(o.subTone)}` : 'none', opacity: rise(frame, since.sub, 12)}}>
              <Decode text={o.sub.toUpperCase()} start={since.sub} size={28} color={o.subTone ? toneOf(o.subTone) : t.muted} />
            </span>
          ) : null}
        </div>
      ) : (
        <div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: '0 20px', fontSize: size, lineHeight: 1.2, color: c || t.ink, opacity: rise(frame, Math.max(since.shown + 6, since.label), 14)}}>
          {o.label}
          {o.sub ? <div style={{marginTop: 6}}><Decode text={o.sub.toUpperCase()} start={since.sub} size={Math.round(size * 0.55)} color={o.subTone ? toneOf(o.subTone) : t.muted} /></div> : null}
        </div>
      )}
    </>
  );
};

const Row: React.FC<Drawn> = ({o, since}) => {
  const frame = useCurrentFrame();
  const p = rise(frame, since.shown, 26);
  const size = sizeOf(o);
  const muted = o.tone === 'muted';
  const color = muted ? t.ink : toneOf(o.tone);
  const wash = o.fill ? rise(frame, since.label > since.sub ? since.label : since.sub, 18) : 0;
  return (
    <div style={{position: 'absolute', inset: 0, clipPath: `inset(0 ${(1 - p) * 100}% 0 0)`, borderBottom: `1px solid ${t.line}`, display: 'flex', alignItems: 'center', gap: 22, padding: '0 8px', opacity: muted ? 0.5 : 1, background: wash ? `linear-gradient(90deg, color-mix(in srgb, ${color} ${wash * 18}%, transparent), transparent 70%)` : 'none'}}>
      {o.index ? <span style={{fontFamily: t.fontMono, fontSize: 24, color: t.muted}}>{o.index}</span> : null}
      <span key={since.label} style={{fontSize: size, fontWeight: 400, letterSpacing: '-0.01em', color, opacity: rise(frame, since.label, 14)}}>{o.label}</span>
      {o.sub ? (
        <span style={{marginLeft: 'auto'}}>
          <Decode key={o.sub} text={o.sub.toUpperCase()} start={since.sub} size={30} weight={500} color={toneOf(o.subTone, t.muted)} />
        </span>
      ) : null}
    </div>
  );
};

// A place that can be taken. A new label turns it over like a card.
const Seat: React.FC<Drawn> = ({o, was, since}) => {
  const frame = useCurrentFrame();
  const p = rise(frame, since.shown, 24);
  const turned = since.label > since.shown;
  const flip = turned ? glide(frame, since.label, 20) : 1;
  const front = flip < 0.5;
  const shownState = front ? was : o;
  const color = toneOf(shownState.tone, t.accent);
  const pulse = 0.55 + 0.45 * Math.sin(frame / 7);
  const size = sizeOf(o);
  const left = o.timer ? Math.max(0, o.timer - Math.floor(Math.max(0, frame - since.timer) / 30)) : null;
  const idle = !o.tone || o.tone === 'accent';
  return (
    <div style={{position: 'absolute', inset: 0, opacity: p, transform: p < 1 || (turned && flip < 1) ? `perspective(1000px) translateY(${(1 - p) * 30}px) rotateX(${(turned ? flip : 0) * 180}deg)` : 'none'}}>
      <div style={{position: 'absolute', inset: 0, transform: turned && !front && flip < 1 ? 'rotateX(180deg)' : 'none', boxSizing: 'border-box', border: `1.5px solid ${color}`, background: `color-mix(in srgb, ${color} ${idle && !o.timer ? 5 + pulse * 5 : 9}%, transparent)`, display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 28px', fontSize: size, color: t.ink}}>
        <span style={{fontWeight: 400}}>{shownState.label}</span>
        <span style={{textAlign: 'right', fontFamily: t.fontMono, color}}>
          {shownState.sub ? <div style={{fontSize: 22, letterSpacing: '0.08em'}}>{shownState.sub.toUpperCase()}</div> : null}
          {left !== null && !(front && turned) ? <div style={{fontSize: 46, fontVariantNumeric: 'tabular-nums'}}>{clockOf(left)}</div> : null}
        </span>
      </div>
    </div>
  );
};

const Note: React.FC<Drawn> = ({o, since}) => (
  <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', flexWrap: 'wrap', paddingLeft: 16}}>
    <Decode key={o.label} text={(o.label ?? '').toUpperCase()} start={Math.max(since.shown, since.label)} size={sizeOf(o)} color={toneOf(o.tone, t.muted)} />
  </div>
);

const Code: React.FC<Drawn> = ({o, since}) => {
  const frame = useCurrentFrame();
  return (
    <div style={{position: 'absolute', inset: 0, boxSizing: 'border-box', display: 'flex', alignItems: 'center', padding: '0 18px', border: `1px solid ${toneOf(o.tone, t.panelBorder)}`, background: t.panelSoft, fontFamily: t.fontMono, fontSize: sizeOf(o), whiteSpace: 'pre', color: toneOf(o.tone), opacity: rise(frame, since.shown, 16)}}>
      <span key={since.label} style={{opacity: rise(frame, since.label, 12)}}>{o.label}</span>
    </div>
  );
};

const SHAPES = {card: Card, row: Row, seat: Seat, note: Note, code: Code};

const Thing: React.FC<{from: State; to: State; p: number; since: Since}> = ({from, to, p, since}) => {
  const box = {x: between(from.x, to.x, p), y: between(from.y, to.y, p), w: between(from.w, to.w, p), h: between(from.h, to.h, p)};
  const gone = to.hidden ? 1 - p : 1;
  if (gone <= 0 || (from.hidden && to.hidden)) return null;
  const Shape = SHAPES[to.shape];
  return (
    <div style={{position: 'absolute', left: box.x, top: box.y, width: box.w, height: box.h, opacity: gone}}>
      <Shape o={{...to, ...box}} was={from} since={since} p={p} />
    </div>
  );
};

const center = (o: State): Point => ({x: o.x + o.w / 2, y: o.y + o.h / 2});
// An arrow leaves the side of a box that faces where it is going, and leaves it square.
const ends = (a: State, b: State) => {
  const [ca, cb] = [center(a), center(b)];
  const dx = cb.x - ca.x;
  const dy = cb.y - ca.y;
  if (Math.abs(dx) >= Math.abs(dy)) {
    const s = Math.sign(dx) || 1;
    return {axis: 'x' as const, start: {x: ca.x + (s * a.w) / 2, y: ca.y}, end: {x: cb.x - (s * b.w) / 2, y: cb.y}};
  }
  const s = Math.sign(dy) || 1;
  return {axis: 'y' as const, start: {x: ca.x, y: ca.y + (s * a.h) / 2}, end: {x: cb.x, y: cb.y - (s * b.h) / 2}};
};

export const WorldScene: React.FC<Props> = ({scene, starts, lengths}) => {
  const frame = useCurrentFrame();
  const {frames, sinces, times} = framesOf(scene, starts, lengths);
  const step = times.reduce((last, at, i) => (frame >= at ? i : last), -1) + 1;
  const to = frames[step];
  const from = frames[Math.max(0, step - 1)];
  const at = step === 0 ? 0 : times[step - 1];
  const p = step === 0 ? 1 : interpolate(frame, [at, at + MOVE], [0, 1], {...clamp, easing: EASE});
  // Things change on their word; the camera sets off before it, so it is already there when the word lands.
  const shot = times.reduce((last, when, i) => (frame >= when - LEAD ? i : last), -1) + 1;
  const [a, b] = [frames[Math.max(0, shot - 1)].camera, frames[shot].camera];
  const pc = shot === 0 ? 1 : interpolate(frame, [times[shot - 1] - LEAD, times[shot - 1] - LEAD + MOVE], [0, 1], {...clamp, easing: EASE});
  const camera = {x: between(a.x, b.x, pc), y: between(a.y, b.y, pc), w: between(a.w, b.w, pc), h: between(a.h, b.h, pc)};
  const zoom = Math.min(WORLD_W / camera.w, WORLD_H / camera.h);
  const live = (id: string): State => {
    const a = from.objects[id];
    const b = to.objects[id];
    if (!b) throw new Error(`${scene.id}: an arrow names "${id}", which is not one of the objects.`);
    return {...b, x: between(a.x, b.x, p), y: between(a.y, b.y, p), w: between(a.w, b.w, p), h: between(a.h, b.h, p)};
  };
  // An arrow's line starts travelling on the change that first drew it.
  const drawnAt = (a: WorldArrow) => {
    let first = at;
    for (let i = step; i > 0; i--) {
      if (!frames[i].arrows.some((o) => o.from === a.from && o.to === a.to)) break;
      first = times[i - 1];
    }
    return first;
  };
  const duration = (starts[starts.length - 1] ?? 0) + (lengths[lengths.length - 1] ?? 0);
  const push = interpolate(frame, [0, Math.max(1, duration)], [1, 1.012], clamp);
  const sway = Math.sin(frame / 80) * 0.5;
  return (
    <div style={{position: 'absolute', inset: 0, transform: `perspective(2400px) rotateY(${sway}deg) scale(${push})`, transformOrigin: `${WORLD_W / 2}px ${WORLD_H / 2}px`}}>
      <div style={{position: 'absolute', left: 0, top: 0, width: WORLD_W, height: WORLD_H, transformOrigin: '0 0', transform: `translate(${(WORLD_W - camera.w * zoom) / 2 - camera.x * zoom}px, ${(WORLD_H - camera.h * zoom) / 2 - camera.y * zoom}px) scale(${zoom})`}}>
        {Object.keys(to.objects).map((id) => (
          <Thing key={id} from={from.objects[id]} to={to.objects[id]} p={p} since={sinces[step][id]} />
        ))}
        <svg width={WORLD_W} height={WORLD_H} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible'}}>
          {to.arrows.map((a, i) => {
            const {axis, start, end} = ends(live(a.from), live(a.to));
            return <Arc key={`${a.from}-${a.to}`} a={start} b={end} axis={axis} p={glide(frame, drawnAt(a), 20)} color={toneOf(a.tone, t.accent)} label={a.label} seed={i} />;
          })}
        </svg>
      </div>
    </div>
  );
};
