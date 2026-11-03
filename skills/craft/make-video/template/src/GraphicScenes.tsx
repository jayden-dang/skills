import {useGsapTimeline} from '@remotion/gsap';
import gsap from 'gsap';
import {DrawSVGPlugin} from 'gsap/DrawSVGPlugin';
import {AbsoluteFill} from 'remotion';
import {FPS, Scene} from './timing';
import {t} from './tokens';

gsap.registerPlugin(DrawSVGPlugin);

type Props = {scene: Scene; starts: number[]};

const sec = (f: number) => f / FPS;
const FRAME = {x: 96, y: 56, w: 1728, h: 850};
const deps = (starts: number[]) => ({dependencies: [starts.join()]});
const wordsIn = (timeline: gsap.core.Timeline, words: Element[]) =>
  timeline.fromTo(words, {opacity: 0, y: 18}, {opacity: 1, y: 0, duration: 0.5, stagger: 0.07, ease: 'power3.out'}, 0.08);

const Words: React.FC<{text: string; size: number; color?: string}> = ({text, size, color}) => (
  <div style={{fontSize: size, fontWeight: 700, letterSpacing: '-0.022em', lineHeight: 1.1, color}}>
    {text.split(' ').map((w, i) => (
      <span key={i} data-word="" style={{display: 'inline-block', marginRight: '0.24em', opacity: 0}}>
        {w}
      </span>
    ))}
  </div>
);

const Panel: React.FC<{children: React.ReactNode}> = ({children}) => (
  <div
    style={{
      position: 'absolute',
      left: FRAME.x,
      top: FRAME.y,
      width: FRAME.w,
      height: FRAME.h,
      boxSizing: 'border-box',
      padding: '56px 72px',
      borderRadius: t.radius,
      background: t.panel,
      backdropFilter: t.panelBlur,
      border: `1px solid ${t.panelBorder}`,
      boxShadow: t.shadow,
      color: t.ink,
    }}
  >
    {children}
  </div>
);

export const TitleScene: React.FC<Props> = ({scene, starts}) => {
  const scope = useGsapTimeline<HTMLDivElement>(({timeline, selector}) => {
    wordsIn(timeline, selector('[data-word]'));
    timeline.fromTo(selector('[data-sub]'), {opacity: 0, y: 14}, {opacity: 1, y: 0, duration: 0.5, ease: 'power3.out'}, 0.5);
  }, deps(starts));
  return (
    <AbsoluteFill ref={scope} style={{justifyContent: 'center', padding: '0 140px 150px', color: t.onGround, textAlign: 'center'}}>
      <Words text={scene.title} size={118} />
      {scene.subtitle ? (
        <div data-sub="" style={{fontSize: 44, fontWeight: 500, marginTop: 26, opacity: 0}}>
          {scene.subtitle}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

export const PointsScene: React.FC<Props> = ({scene, starts}) => {
  const points = scene.points ?? [];
  const scope = useGsapTimeline<HTMLDivElement>(({timeline, selector}) => {
    wordsIn(timeline, selector('[data-word]'));
    points.forEach((_, i) => {
      const at = sec(starts[Math.min(i, starts.length - 1)]) + (i >= starts.length ? (i - starts.length + 1) * 0.25 : 0);
      timeline.fromTo(selector(`#p${i}`), {opacity: 0, y: 18}, {opacity: 1, y: 0, duration: 0.4, ease: 'power3.out'}, at);
    });
  }, deps(starts));
  return (
    <AbsoluteFill ref={scope}>
      <Panel>
        <Words text={scene.title} size={84} />
        <div style={{display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: points.length > 3 ? 16 : 26, height: 590}}>
          {points.map((p, i) => (
            <div key={p} id={`p${i}`} style={{padding: points.length > 3 ? '20px 36px' : '34px 44px', borderRadius: t.radiusSmall, background: t.panelSoft, border: `1px solid ${t.panelBorder}`, fontSize: points.length > 3 ? 40 : 52, fontWeight: 600, lineHeight: 1.18, opacity: 0}}>
              {p}
            </div>
          ))}
        </div>
      </Panel>
    </AbsoluteFill>
  );
};

export const FlowScene: React.FC<Props> = ({scene, starts}) => {
  const sources = scene.sources ?? [];
  const gap = sources.length > 1 ? 470 / (sources.length - 1) : 0;
  const top = sources.length > 1 ? 340 : 575;
  const scope = useGsapTimeline<HTMLDivElement>(({timeline, selector}) => {
    wordsIn(timeline, selector('[data-word]'));
    sources.forEach((_, i) => {
      const at = sec(starts[Math.min(i, starts.length - 1)]) + (i >= starts.length ? (i - starts.length + 1) * 0.35 : 0);
      timeline.fromTo(selector(`#s${i}`), {opacity: 0, x: -30}, {opacity: 1, x: 0, duration: 0.38, ease: 'power3.out'}, at);
      timeline.fromTo(selector(`#l${i}`), {drawSVG: '0% 0%'}, {drawSVG: '0% 100%', duration: 0.5, ease: 'power1.in'}, at + 0.14);
    });
    timeline.fromTo(selector('#target'), {opacity: 0, scale: 0.7, transformOrigin: '50% 50%'}, {opacity: 1, scale: 1, duration: 0.5, ease: 'back.out(1.7)'}, sec(starts[0]) + 0.6);
    if (scene.note) timeline.fromTo(selector('#note'), {opacity: 0, y: 12}, {opacity: 1, y: 0, duration: 0.4, ease: 'power2.out'}, sec(starts[starts.length - 1]));
  }, deps(starts));
  return (
    <AbsoluteFill ref={scope}>
      <Panel>
        <Words text={scene.title} size={84} />
      </Panel>
      <svg viewBox="0 0 1920 1080" style={{position: 'absolute', inset: 0, width: 1920, height: 1080}}>
        {sources.map((_, i) => {
          const y = top + i * gap;
          return <path key={i} id={`l${i}`} d={`M800 ${y} C 940 ${y}, 980 575, 1130 575`} fill="none" stroke={t.accent} strokeWidth={5} strokeLinecap="round" />;
        })}
      </svg>
      {sources.map((s, i) => (
        <div key={s} id={`s${i}`} style={{position: 'absolute', left: 168, top: top + i * gap - 54, width: 632, height: 108, boxSizing: 'border-box', padding: '0 34px', display: 'flex', alignItems: 'center', borderRadius: t.radiusSmall, background: t.panelSoft, border: `1px solid ${t.panelBorder}`, color: t.ink, fontSize: 40, fontWeight: 600, opacity: 0}}>
          {s}
        </div>
      ))}
      <div id="target" style={{position: 'absolute', left: 1140, top: 450, width: 620, height: 250, display: 'flex', alignItems: 'center', justifyContent: 'center', textAlign: 'center', color: t.accent, fontSize: scene.target && scene.target.length < 8 ? 190 : 66, fontWeight: 700, letterSpacing: '-0.02em', lineHeight: 1.05, opacity: 0}}>
        {scene.target}
      </div>
      {scene.note ? (
        <div id="note" style={{position: 'absolute', left: 1140, top: 720, width: 620, textAlign: 'center', color: t.muted, fontSize: 36, fontWeight: 500, lineHeight: 1.2, opacity: 0}}>
          {scene.note}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};
