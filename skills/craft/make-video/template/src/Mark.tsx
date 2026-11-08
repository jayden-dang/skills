import {spring, useCurrentFrame} from 'remotion';
import {compareSize, GAP, LABEL_H, LINE_W, PANE_H, PANE_W, STAT_W, statSize} from './ChangeScenes';
import {fitOf, viewsOf} from './ClipScene';
import {fit, headFace, widthOf, wrap} from './fit';
import {pointAt, pointsMetrics, titleMetrics} from './GraphicScenes';
import {LEAD as CAMERA_LEAD, placed, Scene} from './timing';
import {t} from './tokens';

/* One mark lives through the whole film, so the eye never has to find its place again. It is the full stop of
   a title, the node of the newest event, the bullet of the point being read, the line under a number, the frame
   of the side being talked about, and the ring on the control a line says to press. A recording, a world or a
   Manim scene opens out of it and folds back into it. Each scene's place for it is worked out here from the
   scene's own layout, so a script never sets it. */

type Box = {x: number; y: number; w: number; h: number};
// Where a scene sits on screen: its window for each line, and the scale its content is drawn at.
export type Stage = {size: {w: number; h: number}; k: number; boxes: Box[]};
export type Pose = {at: number; box: Box; r: number; fill: number; o: number};

const TOP = 72;
const BOTTOM = 984;
const DOT = 18;
const LEAD = 4; // The mark gets there a little before the thing it marks.
const K = 1920 / 1600; // A recording's CSS pixels to the frame's.

const dot = (cx: number, cy: number, d = DOT): Box => ({x: cx - d / 2, y: cy - d / 2, w: d, h: d});
const pose = (at: number, box: Box, fill = 1, r?: number, o = 1): Pose => ({at, box, fill, o, r: r ?? Math.min(box.w, box.h) / 2});
const hide = (at: number, p: Pose): Pose => ({...p, at, o: 0});

// Where a graphic scene's title sits: the mark stands before it as its bullet.
const headOf = (scene: Scene, w: number) => {
  if (scene.kind === 'terminal') return {left: 56, top: 40, size: 34};
  if (scene.kind === 'chart') return {left: 56, top: 44, size: fit(scene.id, scene.title, [52, 44], w - 112, 1, headFace).size};
  if (['ears', 'sequence', 'code', 'table'].includes(scene.kind)) return {left: 72, top: 52, size: fit(scene.id, scene.title, [64, 54], w - 144, 1, headFace).size};
  return {left: 72, top: 56, size: fit(scene.id, scene.title, [56, 48], w - 144, 2, headFace).size};
};

const posesOf = (scene: Scene, from: number, starts: number[], lengths: number[], stage: Stage, next?: number): Pose[] => {
  const {size, k, boxes} = stage;
  const win = boxes[0];
  // A point in the scene's own layout, on screen.
  const ox = win.x + win.w / 2 - (size.w * k) / 2;
  const oy = win.y + win.h / 2 - (size.h * k) / 2;
  const at = (x: number, y: number, d = DOT) => dot(ox + x * k, oy + y * k, d * k);
  const arrive = from + (from > 0 ? 4 : 0);
  const kind = scene.kind;

  if (kind === 'title') {
    const {w, h, title, sub} = titleMetrics(scene);
    const lines = wrap(scene.title, title.size, w - 120, headFace);
    const last = lines[lines.length - 1];
    const lineH = title.size * 1.14;
    const block = lines.length * lineH + (sub ? 24 + sub.lines * sub.size * 1.2 : 0);
    const d = Math.max(DOT, title.size * 0.17);
    const x = w / 2 + widthOf(last, title.size, headFace) / 2 + d * 0.9;
    const y = h / 2 - block / 2 + (lines.length - 1) * lineH + title.size * 0.86;
    // The opening title's full stop pops in once its letters have landed; later titles receive it.
    return [pose(from === 0 ? 8 + last.length * 1.4 + 6 : arrive, at(x, y, d))];
  }
  if (kind === 'timeline') {
    const events = scene.events ?? [];
    const step = events.length > 1 ? (LINE_W - 220) / (events.length - 1) : 0;
    return events.map((_, i) => pose(i === 0 ? arrive : from + pointAt(starts, lengths, events.length, i) - LEAD, at(110 + i * step, 330, 26)));
  }
  if (kind === 'points') {
    const {title, rows, perCol, colW} = pointsMetrics(scene);
    const titleH = title.lines * title.size * 1.1 + 28;
    const points = scene.points ?? [];
    return points.map((_, i) => {
      const c = Math.floor(i / perCol);
      const top = 56 + titleH + rows.slice(c * perCol, i).reduce((a, b) => a + b, 0);
      return pose(i === 0 ? arrive : from + pointAt(starts, lengths, points.length, i) - LEAD, at(72 + c * (colW + 56) + 8, top + rows[i] / 2, 20));
    });
  }
  if (kind === 'stat') {
    const {title} = statSize(scene);
    const stats = scene.stats ?? [];
    const cell = (STAT_W - 144) / Math.max(1, stats.length);
    const y = 56 + title.lines * title.size * 1.1 + 48 + 128 + 4;
    return stats.flatMap((stat, i) => {
      const x = 72 + i * cell;
      const when = from + pointAt(starts, lengths, stats.length, i);
      const bar = {x: ox + x * k, y: oy + y * k, w: widthOf(stat.value, 128, headFace) * k, h: 6 * k};
      // It waits as a dot where the number will stand, then stretches under it as the number counts.
      return [pose(i === 0 ? arrive : when - 14, at(x + DOT / 2, y + 3)), pose(when + 2, bar, 1, 3)];
    });
  }
  if (kind === 'compare') {
    const pane = (side?: string): Box => {
      const x = side === 'after' ? 40 + PANE_W + GAP : 40;
      const w = side ? PANE_W : PANE_W * 2 + GAP;
      return {x: ox + (x - 8) * k, y: oy + (40 + LABEL_H - 8) * k, w: (w + 16) * k, h: (PANE_H + 16) * k};
    };
    return scene.beats.map((beat, i) => pose(i === 0 ? arrive : from + starts[i] - LEAD, pane(beat.side), 0, t.radiusSmall + 6));
  }
  if (kind === 'clip' || kind === 'world' || kind === 'manim') {
    // The stage opens out of the mark: it grows into the window's frame, then lets the picture have the screen.
    const frame = (box: Box, when: number, o = 1) => pose(when, box, 0, t.cut > 0 ? 4 : t.radius, o);
    const out: Pose[] = [frame(win, arrive), frame(win, arrive + 16, 0)];
    if (kind === 'clip') {
      const views = viewsOf(scene);
      const u = fitOf(scene).u;
      scene.beats.forEach((beat, i) => {
        if (!beat.ring) return;
        const v = views[i];
        const box = boxes[i] ?? win;
        const r = beat.ring;
        const ring = {x: box.x + u * (v.x + v.s * (r.x * K - 6)), y: box.y + u * (v.y + v.s * (r.y * K - 6)), w: u * v.s * (r.w * K + 12), h: u * v.s * (r.h * K + 12)};
        if (ring.x < box.x - 1 || ring.y < box.y - 1 || ring.x + ring.w > box.x + box.w + 1 || ring.y + ring.h > box.y + box.h + 1) {
          throw new Error(`${scene.id}-${i}: its ring is outside what its focus shows. Widen focus to take in the ring.`);
        }
        // It lands on the control with the camera, which sets off before the line.
        out.push(pose(from + starts[i] - CAMERA_LEAD + 6, ring, 0, t.radiusSmall), hide(from + starts[i] + lengths[i] + 6, pose(0, ring, 0, t.radiusSmall)));
      });
    }
    // Before the next scene, the frame comes back and folds into the mark.
    if (next !== undefined) out.push(frame(boxes[boxes.length - 1] ?? win, next - 8));
    return out;
  }
  const head = headOf(scene, size.w);
  return [pose(arrive, at(head.left / 2, head.top + head.size * 0.6, 16))];
};

const settle = (poses: Pose[]) => {
  // Two poses never share a frame, so every move has a start.
  for (let i = 1; i < poses.length; i++) if (poses[i].at <= poses[i - 1].at) poses[i] = {...poses[i], at: poses[i - 1].at + 1};
  for (const p of poses) {
    const {x, y, w, h} = p.box;
    if (p.o > 0 && (x < -1 || x + w > 1921 || y < TOP - 1 || y + h > BOTTOM + 1)) throw new Error(`the mark leaves the frame at frame ${p.at}: ${JSON.stringify(p.box)}`);
  }
  return poses;
};

export const markPoses = (stages: Stage[]) =>
  settle(placed.flatMap(({scene, from, starts, lengths}, s) => posesOf(scene, from, starts, lengths, stages[s], placed[s + 1] ? placed[s + 1].from : undefined).sort((a, b) => a.at - b.at)));

type State = Box & {r: number; fill: number; o: number};
const of = (p: Pose): State => ({...p.box, r: p.r, fill: p.fill, o: p.o});
const mix = (a: State, b: State, k: number): State => {
  const c = Math.min(1, Math.max(0, k));
  return {x: a.x + (b.x - a.x) * k, y: a.y + (b.y - a.y) * k, w: a.w + (b.w - a.w) * k, h: a.h + (b.h - a.h) * k, r: a.r + (b.r - a.r) * k, fill: a.fill + (b.fill - a.fill) * c, o: a.o + (b.o - a.o) * c};
};
const travel = (frame: number) => spring({frame, fps: 30, config: {damping: 16, stiffness: 140, mass: 0.9}});

// The film's camera follows the mark, and leads it: it turns toward where the mark is going a little before the mark
// sets off. Only the ground moves, so a hold is still a hold. It rests while the mark is hidden inside a stage.
const CENTER = {x: 960, y: (TOP + BOTTOM) / 2};
const FOLLOW = 0.07;
const HEAD_START = 6;
const pan = (frame: number) => spring({frame, fps: 30, config: {damping: 30, stiffness: 50, mass: 1.2}});
export const follow = (poses: Pose[], frame: number) => {
  const keys = poses.filter((p) => p.o > 0).map((p) => ({at: p.at - HEAD_START, x: (CENTER.x - (p.box.x + p.box.w / 2)) * FOLLOW, y: (CENTER.y - (p.box.y + p.box.h / 2)) * FOLLOW}));
  if (!keys.length || frame < keys[0].at) return {x: keys[0]?.x ?? 0, y: keys[0]?.y ?? 0};
  let from = keys[0];
  let k = 0;
  for (let i = 1; i < keys.length && keys[i].at <= frame; i++) {
    if (i > 1) {
      const q = pan(keys[i].at - keys[i - 1].at);
      from = {at: 0, x: from.x + (keys[i - 1].x - from.x) * q, y: from.y + (keys[i - 1].y - from.y) * q};
    }
    k = i;
  }
  const q = k === 0 ? 1 : pan(frame - keys[k].at);
  return {x: from.x + (keys[k].x - from.x) * q, y: from.y + (keys[k].y - from.y) * q};
};

export const Mark: React.FC<{poses: Pose[]}> = ({poses}) => {
  const frame = useCurrentFrame();
  if (!poses.length || frame < poses[0].at) return null;
  // Each move starts from wherever the last one had got to, so a quick second move never jumps.
  let from = of(poses[0]);
  let k = 0;
  for (let i = 1; i < poses.length && poses[i].at <= frame; i++) {
    if (i > 1) from = mix(from, of(poses[i - 1]), travel(poses[i].at - poses[i - 1].at));
    k = i;
  }
  const target = of(poses[k]);
  const p = k === 0 ? 1 : travel(frame - poses[k].at);
  const s = mix(from, target, p);
  // Only something small is solid: a dot that grows into a frame empties as it grows, and fills again as it shrinks.
  s.fill = Math.max(from.fill, target.fill) * Math.min(1, Math.max(0, (60 - Math.min(s.w, s.h)) / 30));
  // A long move arcs, like something thrown, rather than sliding in a straight line.
  const dist = Math.hypot(target.x - from.x, target.y - from.y);
  const lift = k > 0 && dist > 220 && Math.max(target.w, from.w) < 120 ? Math.sin(Math.PI * Math.min(1, Math.max(0, p))) * Math.min(140, dist * 0.22) : 0;
  const pop = k === 0 ? spring({frame: frame - poses[0].at, fps: 30, config: {damping: 10, stiffness: 160}}) : 1;
  if (s.o <= 0.01) return null;
  return (
    <div
      style={{
        position: 'absolute',
        left: s.x + (s.w * (1 - pop)) / 2,
        top: s.y - lift + (s.h * (1 - pop)) / 2,
        width: s.w * pop,
        height: s.h * pop,
        borderRadius: Math.max(0, s.r),
        boxSizing: 'border-box',
        border: `3px solid ${t.accent}`,
        background: `color-mix(in srgb, ${t.accent} ${Math.round(s.fill * 100)}%, transparent)`,
        boxShadow: `0 0 ${10 + 18 * s.fill}px color-mix(in srgb, ${t.accent} 45%, transparent)`,
        opacity: s.o,
        pointerEvents: 'none',
      }}
    />
  );
};

