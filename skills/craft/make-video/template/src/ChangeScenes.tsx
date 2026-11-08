import {Video} from '@remotion/media';
import {getStaticFiles, Img, interpolate, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {fit, headFace} from './fit';
import {clamp, enter, pointAt} from './GraphicScenes';
import {Decode, Roll} from './Look';
import {MOVE, MOVE_EASING} from './ClipScene';
import {LEAD, Rect, Scene, TRANSITION} from './timing';
import {t} from './tokens';

/* Scenes for what changed: two recordings side by side, a number that is the news, and the order things happened in. */

type Props = {scene: Scene; starts: number[]; lengths: number[]};
const head = {fontFamily: t.fontHead, fontWeight: t.headWeight, letterSpacing: t.headTracking};

export const PANE_W = 880;
export const PANE_H = (PANE_W * 9) / 16;
export const GAP = 40;
export const LABEL_H = 64;
export const compareSize = () => ({w: PANE_W * 2 + GAP + 80, h: PANE_H + LABEL_H + 80});

const has = (name: string) => getStaticFiles().some((f) => f.name === name);

// A line's focus, in the recording's CSS pixels at 1600 wide, zooms both sides to the same place.
const K = 1920 / 1600;
type View = {s: number; x: number; y: number};
const viewOf = (focus?: Rect): View => {
  if (!focus) return {s: 1, x: 0, y: 0};
  const s = Math.max(1, Math.min(3, (1920 * 0.92) / (focus.w * K), (1080 * 0.86) / (focus.h * K)));
  const limit = (v: number, low: number) => Math.min(0, Math.max(low, v));
  return {s, x: limit(960 - s * (focus.x + focus.w / 2) * K, 1920 - 1920 * s), y: limit(540 - s * (focus.y + focus.h / 2) * K, 1080 - 1080 * s)};
};
const useView = (scene: Scene, starts: number[]) => {
  const frame = useCurrentFrame();
  let previous = viewOf();
  const views = scene.beats.map((beat) => (previous = beat.focus ? viewOf(beat.focus) : previous));
  const input: number[] = [];
  const values: View[] = [];
  views.forEach((view, i) => {
    if (i === 0) return;
    const start = Math.max(starts[i] - LEAD, (input[input.length - 1] ?? -1) + 1);
    input.push(start, start + MOVE);
    values.push(views[i - 1], view);
  });
  const at = (key: keyof View) => (input.length ? interpolate(frame, input, values.map((v) => v[key]), {...clamp, easing: MOVE_EASING}) : views[0][key]);
  return {s: at('s'), x: at('x'), y: at('y')};
};

// One side of a compare: its recording, then its last frame, dimmed while the line is about the other side.
const Pane: React.FC<{clip?: string; label: string; x: number; start: number; dim: number; rate: number; view: View}> = ({clip, label, x, start, dim, rate, view}) => {
  const frame = useCurrentFrame();
  const p = enter(frame, start, 18);
  const src = clip ? `clips/${clip}.mp4` : '';
  return (
    <div style={{position: 'absolute', left: x, top: 40, width: PANE_W, opacity: p * (1 - 0.6 * dim)}}>
      <div style={{height: LABEL_H, display: 'flex', alignItems: 'center'}}>
        <Decode text={label.toUpperCase()} start={start + 4} size={26} color={dim > 0.5 ? t.muted : t.accent} />
      </div>
      <div style={{position: 'relative', width: PANE_W, height: PANE_H, overflow: 'hidden', borderRadius: t.radiusSmall, border: `${t.borderWidth}px solid ${t.panelBorder}`, background: t.panelSoft}}>
        <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transformOrigin: '0 0', scale: String(PANE_W / 1920)}}>
          <div style={{position: 'absolute', left: 0, top: 0, width: 1920, height: 1080, transformOrigin: '0 0', translate: `${view.x}px ${view.y}px`, scale: String(view.s)}}>
            {clip && has(`clips/${clip}-last.png`) ? <Img src={staticFile(`clips/${clip}-last.png`)} style={{position: 'absolute', inset: 0, width: 1920, height: 1080}} /> : null}
            {clip && has(src) ? (
              <Sequence from={start} layout="none">
                <Video muted playbackRate={rate} src={staticFile(src)} style={{position: 'absolute', inset: 0, width: 1920, height: 1080}} />
              </Sequence>
            ) : null}
          </div>
        </div>
        {!clip || !has(src) ? <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: t.fontMono, fontSize: 24, color: t.warn}}>{`clips/${clip ?? '?'}.mp4 is not added yet`}</div> : null}
      </div>
    </div>
  );
};

export const CompareScene: React.FC<Props> = ({scene, starts}) => {
  const frame = useCurrentFrame();
  const [before, after] = scene.labels ?? ['Before', 'After'];
  // Each line may say which side it is about; the other side dims until a line names it or names neither.
  const sideAt = (key: 'before' | 'after') => {
    const input: number[] = [];
    const values: number[] = [];
    scene.beats.forEach((beat, i) => {
      input.push(starts[i], starts[i] + 10);
      const dim = beat.side && beat.side !== key ? 1 : 0;
      values.push(values.length ? values[values.length - 1] : dim, dim);
    });
    return input.length > 1 ? interpolate(frame, input, values, clamp) : 0;
  };
  const rate = scene.rate ?? 1;
  const view = useView(scene, starts);
  return (
    <div style={{position: 'absolute', inset: 0}}>
      {/* Both sides come in with the transition and start playing as the window lands, so the frame is never empty. */}
      <Pane clip={scene.before} label={before} x={40} start={Math.round(TRANSITION * 0.42)} dim={sideAt('before')} rate={rate} view={view} />
      <Pane clip={scene.after} label={after} x={40 + PANE_W + GAP} start={Math.round(TRANSITION * 0.42)} dim={sideAt('after')} rate={rate} view={view} />
    </div>
  );
};

export const STAT_W = 1500;
export const statSize = (scene: Scene) => {
  const title = fit(scene.id, scene.title, [56, 48], STAT_W - 144, 2, headFace);
  return {w: STAT_W, h: Math.min(840, 112 + title.lines * title.size * 1.1 + 40 + 240), title};
};

// A number that is the news: it rolls up from zero on its line.
export const StatScene: React.FC<Props> = ({scene, starts, lengths}) => {
  const frame = useCurrentFrame();
  const {title} = statSize(scene);
  const stats = scene.stats ?? [];
  const cell = (STAT_W - 144) / Math.max(1, stats.length);
  return (
    <div style={{position: 'absolute', inset: 0, padding: '56px 72px', boxSizing: 'border-box'}}>
      <div style={{...head, fontSize: title.size, lineHeight: 1.1, opacity: enter(frame, 6, 20)}}>{scene.title}</div>
      <div style={{display: 'flex', marginTop: 48}}>
        {stats.map((stat, i) => {
          const at = pointAt(starts, lengths, stats.length, i);
          const n = Number(stat.value.replace(/,/g, ''));
          const counting = Number.isFinite(n) && Number.isInteger(n) && n > 0 && n < 100000;
          const shown = counting ? String(Math.round(n * interpolate(frame, [at, at + 24], [0, 1], clamp))) : stat.value;
          const label = fit(`${scene.id}-${i}`, stat.label, [28, 26, 24], cell - 40, 2);
          return (
            <div key={i} style={{width: cell, opacity: enter(frame, at, 14)}}>
              {counting ? <div style={{...head, fontSize: 128, lineHeight: 1, color: t.accent, fontVariantNumeric: 'tabular-nums'}}>{shown}</div> : <Roll value={stat.value} since={at} size={128} color={t.accent} />}
              <div style={{fontSize: label.size, lineHeight: 1.2, color: t.muted, marginTop: 18, paddingRight: 40}}>{stat.label}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export const LINE_W = 1640;
export const timelineSize = () => ({w: LINE_W, h: 560});

// The order things happened in: one mark per event, each arriving on its line, the newest lit.
export const TimelineScene: React.FC<Props> = ({scene, starts, lengths}) => {
  const frame = useCurrentFrame();
  const events = scene.events ?? [];
  const title = fit(scene.id, scene.title, [56, 48], LINE_W - 144, 1, headFace);
  const left = 110;
  const right = LINE_W - 110;
  const y = 330;
  const step = events.length > 1 ? (right - left) / (events.length - 1) : 0;
  const ats = events.map((_, i) => pointAt(starts, lengths, events.length, i));
  const reach = interpolate(frame, ats.map((a) => a + 4), events.map((_, i) => left + i * step), clamp);
  const lit = ats.reduce((last, a, i) => (frame >= a ? i : last), -1);
  return (
    <div style={{position: 'absolute', inset: 0}}>
      <div style={{...head, position: 'absolute', left: 72, top: 56, fontSize: title.size, lineHeight: 1.1, opacity: enter(frame, 6, 20)}}>{scene.title}</div>
      <div style={{position: 'absolute', left, top: y - 1, width: right - left, height: 2, background: t.panelBorder}} />
      <div style={{position: 'absolute', left, top: y - 2, width: Math.max(0, reach - left), height: 4, background: t.accent}} />
      {events.map((event, i) => {
        const x = left + i * step;
        const p = enter(frame, ats[i], 14);
        const label = fit(`${scene.id}-${i}`, event.label, [30, 27, 24], Math.max(180, step - 24), 2);
        const note = event.note ? fit(`${scene.id}-${i}n`, event.note, [24, 22], Math.max(180, step - 24), 3) : null;
        const color = i === lit ? t.accent : t.ink;
        // A label stays inside the frame: the first and last sit flush with the line's ends.
        const boxW = Math.max(180, step - 24);
        const boxL = Math.min(Math.max(24, x - boxW / 2), LINE_W - 24 - boxW);
        return (
          <div key={i} style={{opacity: p}}>
            <div style={{position: 'absolute', left: x - 12, top: y - 12, width: 24, height: 24, borderRadius: 24, background: i <= lit ? t.accent : t.panelSoft, border: `3px solid ${color}`, scale: String(0.6 + 0.4 * p)}} />
            <div style={{position: 'absolute', left: boxL, width: boxW, top: i % 2 ? y + 40 : y - 40 - label.lines * label.size * 1.15, textAlign: boxL === 24 ? 'left' : boxL === LINE_W - 24 - boxW ? 'right' : 'center', fontSize: label.size, fontWeight: 600, lineHeight: 1.15, color}}>{event.label}</div>
            {note ? <div style={{position: 'absolute', left: boxL, width: boxW, top: i % 2 ? y + 48 + label.lines * label.size * 1.15 : y + 40, textAlign: boxL === 24 ? 'left' : boxL === LINE_W - 24 - boxW ? 'right' : 'center', fontSize: note.size, lineHeight: 1.2, color: t.muted}}>{event.note}</div> : null}
          </div>
        );
      })}
    </div>
  );
};
