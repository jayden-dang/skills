import {useCurrentFrame} from 'remotion';
import {fit, headFace} from './fit';
import {enter, pointAt} from './GraphicScenes';
import {Scene} from './timing';
import {t} from './tokens';

/* A tour's two plain-sight scenes: where the code lives, and the design system's own values drawn as what they are. */

type Props = {scene: Scene; starts: number[]; lengths: number[]};
const head = {fontFamily: t.fontHead, fontWeight: t.headWeight, letterSpacing: t.headTracking};
const W = 1640;
const ROW = 50;

type Row = {path: string; name: string; depth: number; folder: boolean; note?: string; listed: number};

// Every listed path with the folders above it, in tree order. Only listed rows arrive on a line; their parents come with them.
const rowsOf = (scene: Scene): Row[] => {
  const listed = scene.paths ?? [];
  const rows = new Map<string, Row>();
  listed.forEach((p, i) => {
    const parts = p.path.replace(/\/$/, '').split('/');
    parts.forEach((name, d) => {
      const path = parts.slice(0, d + 1).join('/') + (d < parts.length - 1 || p.path.endsWith('/') ? '/' : '');
      const own = d === parts.length - 1;
      const was = rows.get(path);
      rows.set(path, {path, name, depth: d, folder: path.endsWith('/'), note: own ? p.note : was?.note, listed: own ? i : Math.min(was?.listed ?? i, i)});
    });
  });
  return [...rows.values()].sort((a, b) => a.path.localeCompare(b.path));
};

export const treeSize = (scene: Scene) => {
  const title = fit(scene.id, scene.title, [56, 48], W - 144, 1, headFace);
  const rows = rowsOf(scene);
  const h = 112 + title.size * 1.1 + 28 + rows.length * ROW;
  if (h > 840) throw new Error(`${scene.id}: too many paths for one tree. Show the folders that matter.`);
  return {w: W, h, title};
};

export const TreeScene: React.FC<Props> = ({scene, starts, lengths}) => {
  const frame = useCurrentFrame();
  const {title} = treeSize(scene);
  const rows = rowsOf(scene);
  const count = (scene.paths ?? []).length;
  const at = (i: number) => (scene.paths?.[i]?.at !== undefined ? starts[Math.min(scene.paths[i].at as number, starts.length - 1)] : pointAt(starts, lengths, count, i));
  const lit = (scene.paths ?? []).reduce((last, _, i) => (frame >= at(i) ? i : last), -1);
  return (
    <div style={{position: 'absolute', inset: 0, padding: '56px 72px', boxSizing: 'border-box'}}>
      <div style={{...head, fontSize: title.size, lineHeight: 1.1, marginBottom: 28, opacity: enter(frame, 6, 20)}}>{scene.title}</div>
      {rows.map((row) => {
        const p = enter(frame, at(row.listed), 14);
        const own = (scene.paths ?? []).findIndex((x) => x.path.replace(/\/$/, '') === row.path.replace(/\/$/, ''));
        const on = own === lit;
        const note = row.note ? fit(`${scene.id}-${row.path}`, row.note, [30, 27, 24], 760, 1).size : 0;
        return (
          <div key={row.path} style={{display: 'flex', alignItems: 'center', height: ROW, opacity: 0.12 + 0.88 * p, translate: `${(1 - p) * 12}px 0px`}}>
            <div style={{width: 820, paddingLeft: row.depth * 38, display: 'flex', alignItems: 'center', gap: 14, fontFamily: t.fontMono, fontSize: 30, color: on ? t.accent : row.folder ? t.ink : t.muted, whiteSpace: 'nowrap'}}>
              <span style={{width: 18, height: 18, flexShrink: 0, borderRadius: row.folder ? 3 : 18, border: `2px solid ${on ? t.accent : t.panelBorder}`, background: row.folder ? (on ? t.accent : t.panelSoft) : 'transparent'}} />
              {row.name}
              {row.folder ? '/' : ''}
            </div>
            {row.note ? <div style={{fontSize: note, color: on ? t.ink : t.muted, opacity: own >= 0 ? 1 : 0.6}}>{row.note}</div> : null}
          </div>
        );
      })}
    </div>
  );
};

type Kind = 'color' | 'radius' | 'shadow' | 'font' | 'value';
const kindOf = (name: string, value: string): Kind => {
  if (/shadow/i.test(name)) return 'shadow';
  if (/radius|round/i.test(name)) return 'radius';
  if (/font|face|family/i.test(name)) return 'font';
  if (/^(#|rgb|hsl|oklch)/i.test(value.trim())) return 'color';
  return 'value';
};

const CARD_W = 340;
const CARD_H = 250;
export const tokensSize = (scene: Scene) => {
  const title = fit(scene.id, scene.title, [56, 48], W - 144, 1, headFace);
  const n = (scene.tokens ?? []).length;
  const cols = Math.min(4, Math.max(1, n));
  const rows = Math.ceil(n / cols);
  const h = 112 + title.size * 1.1 + 28 + rows * (CARD_H + 24);
  if (h > 840) throw new Error(`${scene.id}: too many tokens for one scene. Show eight at most.`);
  return {w: W, h, title, cols};
};

// Each token drawn as what it is: a colour as a swatch, a radius on a corner, a shadow under a card, a face as type.
export const TokensScene: React.FC<Props> = ({scene, starts, lengths}) => {
  const frame = useCurrentFrame();
  const {title, cols} = tokensSize(scene);
  const tokens = scene.tokens ?? [];
  return (
    <div style={{position: 'absolute', inset: 0, padding: '56px 72px', boxSizing: 'border-box'}}>
      <div style={{...head, fontSize: title.size, lineHeight: 1.1, marginBottom: 28, opacity: enter(frame, 6, 20)}}>
        {scene.title}
        <span style={{fontFamily: t.fontMono, fontSize: 24, color: t.muted, marginLeft: 24, letterSpacing: 0}}>{scene.file}</span>
      </div>
      <div style={{display: 'grid', gridTemplateColumns: `repeat(${cols}, ${CARD_W}px)`, gap: 24}}>
        {tokens.map((tok, i) => {
          const p = enter(frame, tok.at !== undefined ? starts[Math.min(tok.at, starts.length - 1)] : pointAt(starts, lengths, tokens.length, i), 16);
          const kind = kindOf(tok.name, tok.value);
          const sample = (() => {
            if (kind === 'color') return <div style={{height: 110, borderRadius: t.radiusSmall, background: tok.value, border: `1px solid ${t.panelBorder}`}} />;
            if (kind === 'radius') return <div style={{height: 110, display: 'flex', alignItems: 'center', justifyContent: 'center'}}><div style={{width: 150, height: 90, borderRadius: tok.value, border: `3px solid ${t.accent}`}} /></div>;
            if (kind === 'shadow') return <div style={{height: 110, display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#e9eeec', borderRadius: t.radiusSmall}}><div style={{width: 170, height: 70, borderRadius: 10, background: '#ffffff', boxShadow: tok.value}} /></div>;
            if (kind === 'font') return <div style={{height: 110, display: 'flex', alignItems: 'center', fontFamily: tok.value, fontSize: 46, color: t.ink, overflow: 'hidden', whiteSpace: 'nowrap'}}>Aa Delay 0123</div>;
            return <div style={{height: 110, display: 'flex', alignItems: 'center', fontFamily: t.fontMono, fontSize: 40, color: t.ink}}>{tok.value}</div>;
          })();
          return (
            <div key={tok.name} style={{height: CARD_H, boxSizing: 'border-box', padding: 18, background: t.panelSoft, border: `${t.borderWidth}px solid ${t.panelBorder}`, borderRadius: t.radiusSmall, opacity: p, translate: `0px ${(1 - p) * 16}px`}}>
              {sample}
              <div style={{fontFamily: t.fontMono, fontSize: 22, color: t.accent, marginTop: 14, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>{tok.name}</div>
              <div style={{fontFamily: t.fontMono, fontSize: 20, color: t.muted, marginTop: 4, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>{tok.value}</div>
              {tok.role ? <div style={{fontSize: 22, color: t.ink, marginTop: 6, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis'}}>{tok.role}</div> : null}
            </div>
          );
        })}
      </div>
    </div>
  );
};
