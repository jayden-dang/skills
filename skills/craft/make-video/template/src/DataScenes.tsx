import {interpolate, useCurrentFrame} from 'remotion';
import data from './data.json';
import {fit, headFace} from './fit';
import {clamp, enter, pointAt} from './GraphicScenes';
import terminals from './terminals.json';
import {Scene} from './timing';
import {t} from './tokens';

/* Two scenes whose content is recorded, never typed into the script: a terminal session and a chart of measured numbers. */

type Props = {scene: Scene; starts: number[]; lengths: number[]};
const head = {fontFamily: t.fontHead, fontWeight: t.headWeight, letterSpacing: t.headTracking};
const W = 1640;
const H = 760;
export const dataSceneSize = () => ({w: W, h: H});

type Run = {command: string; lines: {t: number; text: string}[]; more: number; exit: number};
const recorded = terminals as unknown as Record<string, Run>;

const LINE = 40;
const ROWS = Math.floor((H - 150) / LINE);

// Each line with a `run` types its command, then prints what the command really printed; earlier runs stay above.
export const TerminalScene: React.FC<Props> = ({scene, starts}) => {
  const frame = useCurrentFrame();
  const rows: {text: string; kind: 'prompt' | 'out' | 'note'}[] = [];
  scene.beats.forEach((beat, i) => {
    const run = beat.run ? recorded[beat.run] : undefined;
    if (!run) return;
    const begin = starts[i] + 4;
    if (frame < begin) return;
    const typing = Math.min(30, run.command.length * 1.4);
    const typed = Math.floor(interpolate(frame, [begin, begin + typing], [0, run.command.length], clamp));
    rows.push({text: `$ ${run.command.slice(0, typed)}${typed < run.command.length && Math.floor(frame / 8) % 2 === 0 ? '▍' : ''}`, kind: 'prompt'});
    if (typed < run.command.length) return;
    // The real timing, squeezed into at most 24 frames, so a slow command does not hold the picture still.
    const last = run.lines.length ? Math.max(0.001, run.lines[run.lines.length - 1].t) : 1;
    const spread = Math.min(24, run.lines.length * 2);
    run.lines.forEach((line) => {
      if (frame >= begin + typing + 4 + (line.t / last) * spread) rows.push({text: line.text, kind: 'out'});
    });
    if (run.more && frame >= begin + typing + 4 + spread) rows.push({text: `… ${run.more} more lines`, kind: 'note'});
  });
  const shown = rows.slice(-ROWS);
  return (
    <div style={{position: 'absolute', inset: 0, padding: '40px 56px', boxSizing: 'border-box'}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 10, marginBottom: 26, opacity: enter(frame, 4, 16)}}>
        {['#fc6756', '#f8cf3e', '#26c96f'].map((c) => <span key={c} style={{width: 14, height: 14, borderRadius: 14, background: c, opacity: 0.85}} />)}
        <span style={{...head, fontSize: 34, marginLeft: 18}}>{scene.title}</span>
      </div>
      <div style={{fontFamily: t.fontMono, fontSize: 28, lineHeight: `${LINE}px`, whiteSpace: 'pre'}}>
        {shown.map((row, k) => (
          <div key={k} style={{color: row.kind === 'prompt' ? t.accent : row.kind === 'note' ? t.muted : t.ink, overflow: 'hidden', textOverflow: 'ellipsis'}}>{row.text || ' '}</div>
        ))}
      </div>
    </div>
  );
};

// Categorical slots validated against each look's surface (dataviz validator); a project's own tokens fall back to night's.
const FALLBACK = ['#3987e5', '#d95926', '#199e70', '#c98500'];
const palette = () => ((t as {chart?: string[]}).chart?.length ? (t as {chart?: string[]}).chart! : FALLBACK);
const values = data as unknown as Record<string, number[][]>;

const label = (v: number) => (Math.abs(v) >= 100 ? v.toFixed(0) : Math.abs(v) >= 10 ? v.toFixed(1) : v.toFixed(2));

// Grouped bars from zero, one axis, a legend for two or more series and the value on each bar, in ink.
export const ChartScene: React.FC<Props> = ({scene, starts, lengths}) => {
  const frame = useCurrentFrame();
  const groups = scene.groups ?? [];
  const series = scene.series ?? [];
  const got = values[scene.id] ?? groups.map((g) => g.values.map(() => 0));
  const max = Math.max(1e-9, ...got.flat()) * 1.18;
  const title = fit(scene.id, scene.title, [52, 44], W - 112, 1, headFace);
  const colors = palette();
  const plotTop = 210;
  const plotH = H - plotTop - 110;
  const bar = Math.min(110, (W - 260) / Math.max(1, groups.length) / Math.max(1, series.length) - 30);
  const groupW = series.length * (bar + 2) + 90;
  const left = (W - groups.length * groupW) / 2 + 45;
  return (
    <div style={{position: 'absolute', inset: 0}}>
      <div style={{...head, position: 'absolute', left: 56, top: 44, fontSize: title.size, opacity: enter(frame, 4, 18)}}>{scene.title}</div>
      {series.length > 1 ? (
        <div style={{position: 'absolute', left: 56, top: 44 + title.size * 1.25, display: 'flex', gap: 34, fontSize: 26, color: t.ink, opacity: enter(frame, 8, 18)}}>
          {series.map((name, k) => (
            <span key={name} style={{display: 'flex', alignItems: 'center', gap: 12}}>
              <span style={{width: 18, height: 18, borderRadius: 4, background: colors[k % colors.length]}} />
              {name}
            </span>
          ))}
        </div>
      ) : null}
      {scene.unit ? <div style={{position: 'absolute', left: 56, top: plotTop - 6, fontFamily: t.fontMono, fontSize: 22, color: t.muted}}>{scene.unit}</div> : null}
      <div style={{position: 'absolute', left: 56, right: 56, top: plotTop + plotH, height: 2, background: t.panelBorder}} />
      {groups.map((g, gi) => {
        const at = pointAt(starts, lengths, groups.length, gi);
        const grow = interpolate(frame, [at, at + 22], [0, 1], {...clamp, easing: (x) => 1 - (1 - x) ** 3});
        return (
          <div key={g.label}>
            {series.map((_, si) => {
              const v = got[gi]?.[si] ?? 0;
              const h = (v / max) * plotH * grow;
              const x = left + gi * groupW + si * (bar + 2);
              return (
                <div key={si}>
                  <div style={{position: 'absolute', left: x, top: plotTop + plotH - h, width: bar, height: h, background: colors[si % colors.length], borderRadius: '4px 4px 0 0'}} />
                  <div style={{position: 'absolute', left: x - 20, width: bar + 40, top: plotTop + plotH - h - 40, textAlign: 'center', fontFamily: t.fontMono, fontSize: 24, color: t.ink, opacity: grow}}>{label(v * grow)}</div>
                </div>
              );
            })}
            <div style={{position: 'absolute', left: left + gi * groupW - 20, width: series.length * (bar + 2) + 40, top: plotTop + plotH + 18, textAlign: 'center', fontSize: 28, color: t.ink, opacity: enter(frame, at, 14)}}>{g.label}</div>
          </div>
        );
      })}
      <div style={{position: 'absolute', right: 56, bottom: 28, fontFamily: t.fontMono, fontSize: 20, color: t.muted}}>{scene.data}</div>
    </div>
  );
};
