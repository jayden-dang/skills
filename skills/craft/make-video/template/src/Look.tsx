import {Easing, interpolate, random, useCurrentFrame} from 'remotion';
import {t} from './tokens';

/* The film's moving parts. Every one of them takes the frame it starts on, so it can land on a word. */

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;
const OUT = Easing.bezier(0.16, 1, 0.3, 1);
const IO = Easing.bezier(0.65, 0, 0.2, 1);
export const rise = (frame: number, start: number, length = 24) => interpolate(frame, [start, start + length], [0, 1], {...clamp, easing: OUT});
export const glide = (frame: number, start: number, length = 24) => interpolate(frame, [start, start + length], [0, 1], {...clamp, easing: IO});

const GLYPHS = 'ABCDEFGHKLMNPRSTUVXYZ0123456789/#:_';

// Mono text that resolves from noise, left to right.
export const Decode: React.FC<{text: string; start: number; size: number; color?: string; speed?: number; tracking?: string; weight?: number}> = ({text, start, size, color = t.ink, speed = 1.1, tracking = '0.08em', weight = 400}) => {
  const frame = useCurrentFrame();
  const shown = [...text].map((c, i) => {
    if (frame < start + i * speed * 0.5) return ' ';
    if (c === ' ' || frame >= start + 6 + i * speed) return c;
    return GLYPHS[Math.floor(random(`${text}-${i}-${Math.floor(frame / 2)}`) * GLYPHS.length)];
  });
  return <span style={{fontFamily: t.fontMono, fontSize: size, letterSpacing: tracking, color, fontWeight: weight, whiteSpace: 'pre'}}>{shown.join('')}</span>;
};

// Large text whose letters rise into place behind a mask.
export const Letters: React.FC<{text: string; start: number; size: number; color?: string; weight?: number}> = ({text, start, size, color = t.ink, weight = t.headWeight}) => {
  const frame = useCurrentFrame();
  return (
    <span style={{display: 'inline-flex', overflow: 'hidden', fontFamily: t.fontHead, fontSize: size, fontWeight: weight, lineHeight: 1.08, letterSpacing: t.headTracking, color, paddingBottom: size * 0.06}}>
      {[...text].map((c, i) => (
        <span key={i} style={{display: 'inline-block', transform: `translateY(${(1 - rise(frame, start + i * 1.4, 20)) * 112}%)`, whiteSpace: 'pre'}}>{c}</span>
      ))}
    </span>
  );
};

export const cutShape = (w: number, h: number) => `polygon(${t.cut}px 0, ${w}px 0, ${w}px ${h - t.cut}px, ${w - t.cut}px ${h}px, 0 ${h}px, 0 ${t.cut}px)`;

// The edge of a window or a card: it draws itself on, and its colors keep turning.
export const Edge: React.FC<{id: string; w: number; h: number; draw?: number; color?: string; width?: number; brackets?: number}> = ({id, w, h, draw = 1, color, width = 2, brackets = 0}) => {
  const frame = useCurrentFrame();
  const stops = [0, 0.38, 0.52, 1];
  const c = t.cut;
  const path = c > 0 ? `M${c} 1 H${w - 1} V${h - c} L${w - c} ${h - 1} H1 V${c} Z` : `M${t.radius} 1 H${w - t.radius} Q${w - 1} 1 ${w - 1} ${t.radius} V${h - t.radius} Q${w - 1} ${h - 1} ${w - t.radius} ${h - 1} H${t.radius} Q1 ${h - 1} 1 ${h - t.radius} V${t.radius} Q1 1 ${t.radius} 1 Z`;
  const stroke = color ?? (t.spectrum.length ? `url(#${id})` : t.panelBorder);
  const corner = (px: number, py: number, sx: number, sy: number) => `M${px} ${py + sy * 22} V${py} H${px + sx * 22}`;
  return (
    <svg width={w} height={h} style={{position: 'absolute', left: 0, top: 0, overflow: 'visible', pointerEvents: 'none'}}>
      {t.spectrum.length ? (
        <defs>
          <linearGradient id={id} gradientUnits="userSpaceOnUse" x1={0} y1={0} x2={w} y2={h} gradientTransform={`rotate(${frame * 0.6} ${w / 2} ${h / 2})`}>
            {t.spectrum.map((value, i) => <stop key={value} offset={stops[i] ?? 1} stopColor={value} />)}
          </linearGradient>
        </defs>
      ) : null}
      <path d={path} fill="none" stroke={stroke} strokeWidth={width} pathLength={1} strokeDasharray={1} strokeDashoffset={1 - draw} />
      {brackets > 0 ? (
        <g fill="none" stroke={t.ink} strokeWidth={1.5} opacity={draw}>
          <path d={corner(-brackets, -brackets, 1, 1)} />
          <path d={corner(w + brackets, h + brackets, -1, -1)} />
        </g>
      ) : null}
    </svg>
  );
};

export type Point = {x: number; y: number};
type Axis = 'x' | 'y';

const controls = (a: Point, b: Point, axis: Axis) => {
  const d = (b[axis] - a[axis]) * 0.48;
  return axis === 'x' ? {c1: {x: a.x + d, y: a.y}, c2: {x: b.x - d, y: b.y}} : {c1: {x: a.x, y: a.y + d}, c2: {x: b.x, y: b.y - d}};
};

const along = (a: Point, b: Point, axis: Axis, p: number): Point => {
  const {c1, c2} = controls(a, b, axis);
  const u = 1 - p;
  const on = (k: Axis) => u * u * u * a[k] + 3 * u * u * p * c1[k] + 3 * u * p * p * c2[k] + p * p * p * b[k];
  return {x: on('x'), y: on('y')};
};

// A line that travels from one thing to another with a bright head, then keeps a dot moving along it.
export const Arc: React.FC<{a: Point; b: Point; axis?: Axis; p: number; color: string; label?: string; seed?: number}> = ({a, b, axis = 'x', p, color, label, seed = 0}) => {
  const frame = useCurrentFrame();
  if (p <= 0) return null;
  const {c1, c2} = controls(a, b, axis);
  const d = `M${a.x} ${a.y} C${c1.x} ${c1.y} ${c2.x} ${c2.y} ${b.x} ${b.y}`;
  const head = along(a, b, axis, p);
  const flow = along(a, b, axis, ((frame + seed * 17) % 54) / 54);
  const middle = along(a, b, axis, 0.5);
  return (
    <g>
      <path d={d} fill="none" stroke={color} strokeOpacity={0.18} strokeWidth={9} pathLength={1} strokeDasharray={`${p} 1`} strokeLinecap="round" />
      <path d={d} fill="none" stroke={color} strokeWidth={2.5} pathLength={1} strokeDasharray={`${p} 1`} strokeLinecap="round" />
      <circle cx={head.x} cy={head.y} r={p < 1 ? 7 : 5} fill={p < 1 ? t.ink : color} style={p < 1 ? {filter: `drop-shadow(0 0 10px ${color})`} : undefined} />
      {p >= 1 ? <circle cx={flow.x} cy={flow.y} r={3.5} fill={t.ink} opacity={0.85} /> : null}
      {label ? <text x={middle.x} y={middle.y - 16} textAnchor="middle" fontFamily={t.fontMono} fontSize={26} fontWeight={500} fill={color} opacity={p}>{label}</text> : null}
    </g>
  );
};

// One value that rolls to the next when it changes.
export const Roll: React.FC<{before?: string; value: string; since: number; size: number; color: string}> = ({before, value, since, size, color}) => {
  const frame = useCurrentFrame();
  const p = rise(frame, since, 14);
  const old = before ?? value;
  return (
    <span style={{position: 'relative', display: 'inline-block', height: size * 1.1, minWidth: size * 0.62 * Math.max(value.length, old.length), overflow: 'hidden', fontFamily: t.fontHead, fontWeight: t.headWeight, fontSize: size, lineHeight: 1.1, color, fontVariantNumeric: 'tabular-nums', whiteSpace: 'nowrap'}}>
      {before !== undefined ? <span style={{position: 'absolute', left: 0, transform: `translateY(${-p * 100}%)`}}>{old}</span> : null}
      <span style={{position: 'absolute', left: 0, transform: `translateY(${before !== undefined ? (1 - p) * 100 : 0}%)`}}>{value}</span>
    </span>
  );
};

// A slow drift of color behind everything, so the ground is never a flat fill.
export const Glow: React.FC = () => {
  const frame = useCurrentFrame();
  if (t.spectrum.length === 0) return null;
  const x = 40 + Math.sin(frame / 140) * 18;
  const y = 50 + Math.cos(frame / 110) * 16;
  return <div style={{position: 'absolute', inset: 0, background: `radial-gradient(900px 620px at ${x}% ${y}%, ${t.spectrum[3]}22, transparent 70%), radial-gradient(700px 500px at ${100 - x}% ${100 - y}%, ${t.spectrum[2]}10, transparent 70%)`}} />;
};

// What sits behind everything, chosen by the look. A grid and a sheet stand still, so they never hide a hold from the check.
export const Backdrop: React.FC = () => {
  // A project's own tokens may predate the slot, so a missing one is the default glow.
  const backdrop = (t as {backdrop?: string}).backdrop ?? 'glow';
  if (backdrop === 'grid') {
    const minor = `${t.line}55`;
    return (
      <div style={{position: 'absolute', inset: 0, backgroundImage: `linear-gradient(${t.line} 1px, transparent 1px), linear-gradient(90deg, ${t.line} 1px, transparent 1px), linear-gradient(${minor} 1px, transparent 1px), linear-gradient(90deg, ${minor} 1px, transparent 1px)`, backgroundSize: '160px 160px, 160px 160px, 32px 32px, 32px 32px', backgroundPosition: '-1px -1px', opacity: 0.55}}>
        <div style={{position: 'absolute', inset: 0, background: `radial-gradient(1200px 700px at 50% 45%, transparent 40%, ${t.ground} 100%)`}} />
      </div>
    );
  }
  if (backdrop === 'paper') {
    return <div style={{position: 'absolute', inset: 0, background: `radial-gradient(1400px 900px at 50% 40%, #ffffff55, transparent 70%), radial-gradient(1200px 800px at 50% 50%, transparent 55%, #00000014 100%)`}} />;
  }
  if (backdrop === 'none') return null;
  return <Glow />;
};
