import {Easing, interpolate, useCurrentFrame} from 'remotion';
import {fit, headFace, linesOf} from './fit';
import {clamp, enter, pointAt} from './GraphicScenes';
import {Scene} from './timing';
import {t} from './tokens';

/* The scenes a film of a spec is made of: what the spec says, on screen, in its own words. */

type Props = {scene: Scene; starts: number[]; lengths: number[]};

const W = 1640;
const PAD = 72;
const MAX_H = 840;
const INNER = W - PAD * 2;
const head = {fontFamily: t.fontHead, fontWeight: t.headWeight, letterSpacing: t.headTracking};
const MONO = {font: t.fontMono, weight: 500};
const plain = (text: string) => text.replace(/`/g, '');
const wash = (amount: number) => `color-mix(in srgb, ${t.accent} ${amount}%, transparent)`;

const titled = (scene: Scene) => {
  const title = fit(scene.id, scene.title, [64, 54], INNER, 1, headFace);
  return {title, top: 52 + title.size * 1.1 + 28};
};

const Title: React.FC<{scene: Scene; size: number}> = ({scene, size}) => {
  const frame = useCurrentFrame();
  return <div style={{...head, position: 'absolute', left: PAD, right: PAD, top: 52, fontSize: size, lineHeight: 1.1, whiteSpace: 'nowrap', opacity: enter(frame, 6, 20)}}>{scene.title}</div>;
};

// `code` in spec text is drawn in the mono face.
const Inline: React.FC<{text: string}> = ({text}) => (
  <>
    {text.split(/(`[^`]+`)/).map((part, i) =>
      part.startsWith('`') ? <span key={i} style={{fontFamily: t.fontMono, fontSize: '0.92em'}}>{plain(part)}</span> : part,
    )}
  </>
);

const EARS = /(WHEN|WHILE|WHERE|IF|THEN|THE SYSTEM SHALL CONTINUE TO|THE SYSTEM SHALL)/;
const Ears: React.FC<{text: string}> = ({text}) => (
  <>
    {text.split(EARS).map((part, i) =>
      i % 2 ? <span key={i} style={{color: t.accent, fontWeight: 700}}>{part}</span> : <Inline key={i} text={part} />,
    )}
  </>
);

const earsMetrics = (scene: Scene) => {
  const rules = scene.rules ?? [];
  const {title, top} = titled(scene);
  for (const size of [44, 38, 33, 29]) {
    const rows = rules.map((r) => linesOf(plain(r.text), size, INNER) * size * 1.26 + 66);
    const h = top + rows.reduce((a, b) => a + b, 0) + 44;
    if (rows.every(Number.isFinite) && h <= MAX_H) return {w: W, h, title, top, size, rows};
  }
  throw new Error(`${scene.id}: these rules do not fit. Use fewer in this scene.`);
};

export const EarsScene: React.FC<Props> = ({scene, starts, lengths}) => {
  const frame = useCurrentFrame();
  const {title, top, size, rows} = earsMetrics(scene);
  const rules = scene.rules ?? [];
  return (
    <div style={{position: 'absolute', inset: 0}}>
      <Title scene={scene} size={title.size} />
      <div style={{position: 'absolute', left: PAD, right: PAD, top}}>
        {rules.map((r, i) => {
          const shown = enter(frame, pointAt(starts, lengths, rules.length, i), 16);
          return (
            <div key={r.id} style={{height: rows[i], opacity: 0.14 + 0.86 * shown, translate: `${(shown - 1) * 14}px 0px`}}>
              <div style={{fontFamily: t.fontMono, fontSize: 28, fontWeight: 600, color: t.muted, marginBottom: 8}}>{r.id}</div>
              <div style={{fontSize: size, fontWeight: 500, lineHeight: 1.26}}><Ears text={r.text} /></div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

const sequenceMetrics = (scene: Scene) => {
  const actors = scene.actors ?? [];
  const steps = scene.steps ?? [];
  if (actors.length < 2 || steps.length === 0) throw new Error(`${scene.id}: a sequence needs two actors and a step.`);
  const {title, top} = titled(scene);
  const headH = 64;
  const rowH = Math.min(92, (MAX_H - top - headH - 60) / steps.length);
  if (rowH < 58) throw new Error(`${scene.id}: too many steps for one scene. Split it.`);
  const spread = INNER / actors.length;
  const actorSize = fit(scene.id, actors.reduce((a, b) => (a.length > b.length ? a : b)), [34, 30, 26], spread - 36, 1, MONO).size;
  return {w: W, h: top + headH + steps.length * rowH + 60, title, top, headH, rowH, spread, actorSize};
};

export const SequenceScene: React.FC<Props> = ({scene, starts, lengths}) => {
  const frame = useCurrentFrame();
  const {h, title, top, headH, rowH, spread, actorSize} = sequenceMetrics(scene);
  const actors = scene.actors ?? [];
  const steps = scene.steps ?? [];
  const x = (name: string) => {
    const at = actors.indexOf(name);
    if (at < 0) throw new Error(`${scene.id}: "${name}" is not one of the actors.`);
    return PAD + spread * (at + 0.5);
  };
  const arrives = steps.map((_, i) => pointAt(starts, lengths, steps.length, i));
  const current = arrives.reduce((last, at, i) => (frame >= at ? i : last), -1);
  const y0 = top + headH + 8;
  return (
    <div style={{position: 'absolute', inset: 0}}>
      <Title scene={scene} size={title.size} />
      {actors.map((name) => (
        <div key={name} style={{position: 'absolute', left: x(name) - spread / 2 + 10, width: spread - 20, top, height: headH - 12, display: 'flex', alignItems: 'center', justifyContent: 'center', boxSizing: 'border-box', borderRadius: t.radiusSmall, background: t.panelSoft, border: `${t.borderWidth}px solid ${t.panelBorder}`, fontFamily: t.fontMono, fontSize: actorSize, fontWeight: 600, opacity: enter(frame, 8, 18)}}>
          {name}
        </div>
      ))}
      <svg width={W} height={h} style={{position: 'absolute', left: 0, top: 0}}>
        {actors.map((name) => (
          <line key={name} x1={x(name)} x2={x(name)} y1={top + headH - 12} y2={h - 32} stroke={t.panelBorder} strokeWidth={2} strokeDasharray="6 8" opacity={enter(frame, 8, 18)} />
        ))}
        {steps.map((step, i) => {
          const p = interpolate(frame, [arrives[i], arrives[i] + 16], [0, 1], {...clamp, easing: Easing.bezier(0.45, 0, 0.3, 1)});
          if (p === 0) return null;
          const y = y0 + rowH * (i + 0.72);
          const [a, b] = [x(step.from), x(step.to)];
          const color = i === current ? t.accent : t.muted;
          if (a === b) {
            return <path key={i} d={`M${a} ${y - 22} h 56 v 22 h -46 m 12 -9 l -12 9 l 12 9`} fill="none" stroke={color} strokeWidth={4} strokeLinejoin="round" strokeLinecap="round" opacity={p} />;
          }
          const dir = b > a ? 1 : -1;
          const end = a + (b - a) * p;
          return (
            <g key={i}>
              <line x1={a} x2={end} y1={y} y2={y} stroke={color} strokeWidth={4} strokeLinecap="round" />
              {p === 1 ? <path d={`M${b - dir * 15} ${y - 10} L${b} ${y} L${b - dir * 15} ${y + 10}`} fill="none" stroke={color} strokeWidth={4} strokeLinecap="round" strokeLinejoin="round" /> : null}
            </g>
          );
        })}
      </svg>
      {steps.map((step, i) => {
        const shown = enter(frame, arrives[i] + 4, 14);
        const [a, b] = [x(step.from), x(step.to)];
        const self = a === b;
        const size = fit(scene.id, plain(step.label), [30, 27, 24], self ? spread * 1.2 : Math.max(Math.abs(b - a) - 24, 620), 1, MONO).size;
        const width = self ? INNER : Math.max(Math.abs(b - a) - 24, 620);
        const center = (a + b) / 2;
        const left = self ? a + 72 : Math.min(Math.max(PAD, center - width / 2), W - PAD - width);
        return (
          <div key={i} style={{position: 'absolute', left, width: self ? W - PAD - left : width, top: y0 + rowH * (i + 0.72) - (self ? 34 : size * 1.28 + 8), fontFamily: t.fontMono, fontSize: size, fontWeight: i === current ? 650 : 500, lineHeight: 1.28, textAlign: self ? 'left' : 'center', whiteSpace: 'nowrap', color: i === current ? t.ink : t.muted, opacity: shown}}>
            {plain(step.label)}
          </div>
        );
      })}
    </div>
  );
};

const codeMetrics = (scene: Scene) => {
  const lines = scene.lines ?? [];
  const {title, top} = titled(scene);
  const inner = INNER - 56;
  for (const size of [34, 30, 27, 24]) {
    const fits = lines.every((l) => linesOf(l.replace(/ /g, ' ') || 'x', size, inner, MONO) === 1);
    const blockH = lines.length * size * 1.42 + 44;
    const h = top + 44 + blockH + 44;
    if (fits && h <= MAX_H) return {w: W, h, title, top, size, blockH};
  }
  throw new Error(`${scene.id}: this code does not fit. Quote fewer or shorter lines.`);
};

export const CodeScene: React.FC<Props> = ({scene, starts}) => {
  const frame = useCurrentFrame();
  const {title, top, size, blockH} = codeMetrics(scene);
  const lines = scene.lines ?? [];
  const beat = scene.beats.reduce((last, _, i) => (frame >= starts[i] ? i : last), 0);
  const marked = scene.beats[beat]?.mark ?? [];
  const move = enter(frame, starts[beat], 12);
  return (
    <div style={{position: 'absolute', inset: 0}}>
      <Title scene={scene} size={title.size} />
      <div style={{position: 'absolute', left: PAD, right: PAD, top, fontFamily: t.fontMono, fontSize: 26, color: t.muted, opacity: enter(frame, 8, 18)}}>{scene.file}</div>
      <div style={{position: 'absolute', left: PAD, right: PAD, top: top + 44, height: blockH, boxSizing: 'border-box', padding: '22px 28px', borderRadius: t.radiusSmall, background: t.panelSoft, border: `${t.borderWidth}px solid ${t.panelBorder}`, fontFamily: t.fontMono, fontSize: size, lineHeight: 1.42, opacity: enter(frame, 10, 18)}}>
        {lines.map((line, i) => {
          const on = marked.includes(i + 1);
          return (
            <div key={i} style={{whiteSpace: 'pre', margin: '0 -12px', padding: '0 12px', borderRadius: 6, background: on ? wash(16 * move) : 'transparent', opacity: marked.length && !on ? 1 - 0.5 * move : 1}}>
              {line || ' '}
            </div>
          );
        })}
      </div>
    </div>
  );
};

const tableMetrics = (scene: Scene) => {
  const columns = scene.columns ?? [];
  const rows = scene.rows ?? [];
  const {title, top} = titled(scene);
  const longest = columns.map((c, at) => Math.max(c.length, ...rows.map((r) => plain(r[at] ?? '').length)));
  const weights = longest.map((n) => Math.min(Math.max(n, 12), 60));
  const total = weights.reduce((a, b) => a + b, 0);
  const widths = weights.map((n) => (INNER * n) / total);
  for (const size of [36, 32, 28, 25]) {
    const lineCounts = rows.map((r) => Math.max(...r.map((cell, at) => linesOf(plain(cell), size, widths[at] - 28))));
    const heights = lineCounts.map((n) => n * size * 1.22 + 26);
    const h = top + 50 + heights.reduce((a, b) => a + b, 0) + 40;
    if (lineCounts.every(Number.isFinite) && h <= MAX_H) return {w: W, h, title, top, size, widths, heights};
  }
  throw new Error(`${scene.id}: this table does not fit. Use fewer rows or shorter cells.`);
};

export const TableScene: React.FC<Props> = ({scene, starts, lengths}) => {
  const frame = useCurrentFrame();
  const {title, top, size, widths, heights} = tableMetrics(scene);
  const rows = scene.rows ?? [];
  const arrives = rows.map((_, i) => pointAt(starts, lengths, rows.length, i));
  const current = arrives.reduce((last, at, i) => (frame >= at ? i : last), -1);
  return (
    <div style={{position: 'absolute', inset: 0}}>
      <Title scene={scene} size={title.size} />
      <div style={{position: 'absolute', left: PAD, right: PAD, top}}>
        <div style={{display: 'flex', height: 50, alignItems: 'center', borderBottom: `2px solid ${t.panelBorder}`, opacity: enter(frame, 8, 18)}}>
          {(scene.columns ?? []).map((c, i) => (
            <div key={c} style={{width: widths[i], paddingLeft: 14, boxSizing: 'border-box', fontSize: 27, fontWeight: 650, color: t.muted}}>{c}</div>
          ))}
        </div>
        {rows.map((row, r) => {
          const shown = enter(frame, arrives[r], 14);
          return (
            <div key={r} style={{display: 'flex', alignItems: 'center', height: heights[r], borderRadius: t.radiusSmall, background: r === current ? wash(10 * shown) : 'transparent', opacity: 0.12 + 0.88 * shown}}>
              {row.map((cell, i) => (
                <div key={i} style={{width: widths[i], paddingLeft: 14, boxSizing: 'border-box', fontSize: size, fontWeight: 500, lineHeight: 1.22}}><Inline text={cell} /></div>
              ))}
            </div>
          );
        })}
      </div>
    </div>
  );
};

// A decision beside what it rejected: the options arrive through the first line, the verdict lands on the second.
const CHOICE_GAP = 32;
export const choiceMetrics = (scene: Scene) => {
  const {title, top} = titled(scene);
  const options = scene.options ?? [];
  const n = Math.max(1, options.length);
  const cardW = (INNER - CHOICE_GAP * (n - 1)) / n;
  for (const [size, why] of [[44, 30], [40, 28], [36, 26], [32, 24]]) {
    const labels = options.map((o) => linesOf(o.label, size, cardW - 64, headFace));
    const whys = options.map((o) => linesOf(o.why, why, cardW - 64));
    if (![...labels, ...whys].every(Number.isFinite) || Math.max(...labels) > 2 || Math.max(...whys) > 3) continue;
    const cardH = 40 + 44 + 18 + Math.max(...labels) * size * 1.12 + 18 + Math.max(...whys) * why * 1.28 + 40;
    const cost = scene.cost ? fit(`${scene.id}-cost`, scene.cost, [30, 28, 26], INNER - 48, 2) : null;
    const costH = cost ? 28 + cost.lines * cost.size * 1.28 + 32 : 0;
    const h = top + cardH + costH + 56;
    if (h > MAX_H) continue;
    const cards = options.map((_, i) => ({x: PAD + i * (cardW + CHOICE_GAP), y: top, w: cardW, h: cardH}));
    return {w: W, h, title, top, size, why, cards, cost, costTop: top + cardH + 28};
  }
  throw new Error(`${scene.id}: these options do not fit. Shorten their labels or reasons.`);
};

export const ChoiceScene: React.FC<Props> = ({scene, starts, lengths}) => {
  const frame = useCurrentFrame();
  const {title, size, why, cards, cost, costTop} = choiceMetrics(scene);
  const options = scene.options ?? [];
  const verdict = enter(frame, (starts[1] ?? starts[0] + lengths[0]) + 4, 18);
  const costAt = enter(frame, (starts[2] ?? starts[1] ?? 0) + 10, 18);
  return (
    <div style={{position: 'absolute', inset: 0}}>
      <Title scene={scene} size={title.size} />
      {options.map((o, i) => {
        const box = cards[i];
        const shown = enter(frame, starts[0] + Math.round((lengths[0] * i) / options.length), 16);
        const lit = o.chosen ? verdict : 0;
        const out = o.chosen ? 0 : verdict;
        return (
          <div key={i} style={{position: 'absolute', left: box.x, top: box.y, width: box.w, height: box.h, boxSizing: 'border-box', padding: '40px 32px', borderRadius: t.radiusSmall, background: t.panelSoft, border: `${Math.max(t.borderWidth, 1) + lit}px solid ${lit > 0.5 ? t.accent : t.panelBorder}`, opacity: shown * (1 - 0.55 * out), translate: `0px ${(1 - shown) * 24}px`}}>
            <div style={{height: 44, display: 'flex', alignItems: 'center'}}>
              <div style={{width: 40, height: 40, borderRadius: 40, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: t.fontMono, fontSize: 24, fontWeight: 600, border: `2px solid ${lit > 0.5 ? t.accent : t.muted}`, color: lit > 0.5 ? t.accent : t.muted, background: lit > 0.5 ? wash(18) : 'transparent'}}>
                {verdict < 0.5 ? String.fromCharCode(65 + i) : o.chosen ? '✓' : '✕'}
              </div>
            </div>
            <div style={{...head, marginTop: 18, fontSize: size, lineHeight: 1.12, color: t.ink}}>
              <span style={{position: 'relative'}}>
                {o.label}
                {!o.chosen ? <span style={{position: 'absolute', left: 0, top: '55%', height: 3, width: `${out * 100}%`, background: t.muted}} /> : null}
              </span>
            </div>
            <div style={{marginTop: 18, fontSize: why, lineHeight: 1.28, color: t.muted}}>{o.why}</div>
          </div>
        );
      })}
      {cost ? (
        <div style={{position: 'absolute', left: PAD, right: PAD, top: costTop, padding: '14px 24px', boxSizing: 'border-box', borderLeft: `4px solid ${t.warn}`, background: t.panelSoft, fontSize: cost.size, lineHeight: 1.28, color: t.ink, opacity: costAt, translate: `${(1 - costAt) * 20}px 0px`}}>{scene.cost}</div>
      ) : null}
    </div>
  );
};

export const SPEC_KINDS = ['ears', 'sequence', 'code', 'table', 'choice'];

export const specSize = (scene: Scene) => {
  if (scene.kind === 'ears') return earsMetrics(scene);
  if (scene.kind === 'sequence') return sequenceMetrics(scene);
  if (scene.kind === 'code') return codeMetrics(scene);
  if (scene.kind === 'choice') return choiceMetrics(scene);
  return tableMetrics(scene);
};
