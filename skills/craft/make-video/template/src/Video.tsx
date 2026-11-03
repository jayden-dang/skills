import {Audio} from '@remotion/media';
import {AbsoluteFill, Easing, interpolate, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {ClipScene} from './ClipScene';
import {clamp, enter, FlowScene, graphicSize, PointsScene, TitleScene} from './GraphicScenes';
import {Beat, placed, Scene, TRANSITION} from './timing';
import {t} from './tokens';

/* One window lives through the whole film and changes shape to fit each scene. The narration sits under it. */

type Box = {x: number; y: number; w: number; h: number};
const CLIP_WIDTH = 1440;
const CENTER_Y = 452;

const boxFor = (scene: Scene): Box => {
  if (scene.kind === 'clip') return {x: (1920 - CLIP_WIDTH) / 2, y: 26, w: CLIP_WIDTH, h: (CLIP_WIDTH * 9) / 16};
  const {w, h} = graphicSize(scene);
  return {x: (1920 - w) / 2, y: CENTER_Y - h / 2, w, h};
};

const Window: React.FC<{children: React.ReactNode}> = ({children}) => {
  const frame = useCurrentFrame();
  const input: number[] = [];
  const boxes: Box[] = [];
  placed.forEach(({scene, from}, i) => {
    if (i === 0) return;
    input.push(from, from + 24);
    boxes.push(boxFor(placed[i - 1].scene), boxFor(scene));
  });
  const first = boxFor(placed[0].scene);
  const at = (key: keyof Box) => (input.length ? interpolate(frame, input, boxes.map((b) => b[key]), {...clamp, easing: Easing.bezier(0.5, 0, 0.1, 1)}) : first[key]);
  return (
    <div style={{position: 'absolute', left: at('x'), top: at('y'), width: at('w'), height: at('h'), boxSizing: 'border-box', borderRadius: t.radius, background: t.panel, backdropFilter: t.panelBlur, border: `${t.borderWidth}px solid ${t.panelBorder}`, boxShadow: t.shadow, overflow: 'hidden', color: t.ink, scale: String(0.96 + 0.04 * enter(frame, 0, 24)), opacity: enter(frame, 0, 12)}}>
      {children}
    </div>
  );
};

const SceneFade: React.FC<{duration: number; first: boolean; last: boolean; children: React.ReactNode}> = ({duration, first, last, children}) => {
  const frame = useCurrentFrame();
  const inn = first ? 1 : interpolate(frame, [TRANSITION / 2, TRANSITION], [0, 1], clamp);
  const out = last ? 1 : interpolate(frame, [duration - TRANSITION, duration - TRANSITION / 2], [1, 0], clamp);
  return <AbsoluteFill style={{opacity: Math.min(inn, out)}}>{children}</AbsoluteFill>;
};

const Caption: React.FC<{beat: Beat}> = ({beat}) => {
  const frame = useCurrentFrame();
  const p = enter(frame, 0, 10);
  return (
    <div style={{position: 'absolute', left: 200, right: 200, top: 866, textAlign: 'center', opacity: p, translate: `0px ${(1 - p) * 8}px`}}>
      <div style={{fontSize: 42, fontWeight: 550, lineHeight: 1.2, letterSpacing: '-0.01em', color: t.onGround, textWrap: 'balance'}}>{beat.text}</div>
      <div style={{fontFamily: t.fontMono, fontSize: 21, color: t.onGround, opacity: 0.72, marginTop: 10}}>{beat.ref}</div>
    </div>
  );
};

const Staged: React.FC<{text: string}> = ({text}) => (
  <div style={{position: 'absolute', right: 36, bottom: 18, padding: '7px 18px', borderRadius: Math.max(t.radiusSmall, 6), background: t.panelSoft, border: `${t.borderWidth}px solid ${t.bad}`, color: t.bad, fontSize: 24, fontWeight: 600}}>{text}</div>
);

export const Film: React.FC = () => (
  <AbsoluteFill style={{background: t.ground, fontFamily: t.fontSans}}>
    <Window>
      {placed.map(({scene, from, duration, starts, lengths}, s) => {
        const box = boxFor(scene);
        const props = {scene, starts, lengths};
        return (
          <Sequence key={scene.id} from={from} durationInFrames={duration} name={scene.title}>
            <SceneFade duration={duration} first={s === 0} last={s === placed.length - 1}>
              <div style={{position: 'absolute', left: 0, top: 0, width: box.w, height: box.h}}>
                {scene.kind === 'title' ? <TitleScene {...props} /> : null}
                {scene.kind === 'points' ? <PointsScene {...props} /> : null}
                {scene.kind === 'flow' ? <FlowScene {...props} /> : null}
                {scene.kind === 'clip' ? <ClipScene {...props} duration={duration} width={CLIP_WIDTH} /> : null}
              </div>
            </SceneFade>
          </Sequence>
        );
      })}
    </Window>
    {placed.map(({scene, from, duration, starts}, s) => (
      <Sequence key={scene.id} from={from} durationInFrames={duration} name={`${scene.title}: narration`}>
        <SceneFade duration={duration} first={s === 0} last={s === placed.length - 1}>
          {scene.beats.map((beat, i) => (
            <Sequence key={i} from={starts[i]} durationInFrames={(starts[i + 1] ?? duration) - starts[i]} layout="none" name={`line ${i + 1}`}>
              <Audio src={staticFile(`voice/${scene.id}-${i}.mp3`)} />
              <Caption beat={beat} />
            </Sequence>
          ))}
          {scene.staged ? <Staged text={scene.staged} /> : null}
        </SceneFade>
      </Sequence>
    ))}
  </AbsoluteFill>
);
