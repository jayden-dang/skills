import {Audio} from '@remotion/media';
import {useState} from 'react';
import {AbsoluteFill, interpolate, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {CLIP_W, clipHeights, ClipScene, MOVE, MOVE_EASING} from './ClipScene';
import {WithFonts} from './fonts';
import {clamp, enter, FlowScene, graphicSize, PointsScene, TitleScene} from './GraphicScenes';
import {CodeScene, EarsScene, SequenceScene, SPEC_KINDS, specSize, TableScene} from './SpecScenes';
import {Beat, placed, planned, Scene, TRANSITION} from './timing';
import {worldSize, WorldScene} from './WorldScene';
import {t} from './tokens';

/* One window lives through the whole film and changes shape to fit each line. The narration sits under it. */

type Box = {x: number; y: number; w: number; h: number};
const CENTER_Y = 412;
const sizeOf = (scene: Scene) => (scene.kind === 'world' ? worldSize(scene) : SPEC_KINDS.includes(scene.kind) ? specSize(scene) : graphicSize(scene));
const centered = (w: number, h: number): Box => ({x: (1920 - w) / 2, y: CENTER_Y - h / 2, w, h});

// Every shape the window takes, in order, with the frame it starts moving there. Measured text, so
// this runs inside WithFonts, once the project's fonts are in.
const shapesOf = () =>
  placed.flatMap(({scene, from, starts}) => {
    if (scene.kind !== 'clip') {
      const {w, h} = sizeOf(scene);
      return [{at: from, box: centered(w, h)}];
    }
    return clipHeights(scene).map((h, i) => ({at: i === 0 ? from : from + starts[i], box: centered(CLIP_W, h)}));
  });

const Window: React.FC<{children: React.ReactNode}> = ({children}) => {
  const frame = useCurrentFrame();
  const [shapes] = useState(shapesOf);
  const input: number[] = [];
  const boxes: Box[] = [];
  shapes.forEach(({at, box}, i) => {
    if (i === 0) return;
    const start = Math.max(at, (input[input.length - 1] ?? -1) + 1);
    input.push(start, start + MOVE);
    boxes.push(shapes[i - 1].box, box);
  });
  const at = (key: keyof Box) => (input.length ? interpolate(frame, input, boxes.map((b) => b[key]), {...clamp, easing: MOVE_EASING}) : shapes[0].box[key]);
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
    <div style={{position: 'absolute', left: 140, right: 140, top: 826, textAlign: 'center', opacity: p, translate: `0px ${(1 - p) * 8}px`}}>
      <div style={{fontSize: 50, fontWeight: 550, lineHeight: 1.18, letterSpacing: '-0.012em', color: t.onGround, textShadow: t.onGroundShadow, textWrap: 'balance'}}>{beat.text}</div>
      <div style={{fontFamily: t.fontMono, fontSize: 24, color: t.onGround, textShadow: t.onGroundShadow, opacity: 0.72, marginTop: 10}}>{beat.ref}</div>
    </div>
  );
};

const Staged: React.FC<{text: string}> = ({text}) => (
  <div style={{position: 'absolute', right: 40, bottom: 20, padding: '6px 18px', borderRadius: Math.max(t.radiusSmall, 6), background: t.panelSoft, border: `${t.borderWidth}px solid ${t.bad}`, color: t.bad, fontSize: 26, fontWeight: 600}}>{text}</div>
);

// A film of a spec says so on every frame: nothing it shows exists yet.
const Planned: React.FC<{text: string}> = ({text}) => (
  <div style={{position: 'absolute', right: 40, bottom: 20, padding: '6px 18px', borderRadius: Math.max(t.radiusSmall, 6), background: t.panelSoft, border: `${t.borderWidth}px solid ${t.accent}`, color: t.accent, fontSize: 26, fontWeight: 600}}>{text}</div>
);

const Scenes: React.FC = () => (
  <AbsoluteFill style={{background: t.ground, fontFamily: t.fontSans}}>
    <Window>
      {placed.map(({scene, from, duration, starts, lengths}, s) => {
        const props = {scene, starts, lengths};
        return (
          <Sequence key={scene.id} from={from} durationInFrames={duration} name={scene.title}>
            <SceneFade duration={duration} first={s === 0} last={s === placed.length - 1}>
              {scene.kind === 'clip' ? (
                <ClipScene {...props} duration={duration} />
              ) : (
                // Sized to the scene's own shape, so its text holds still while the window moves.
                <div style={{position: 'absolute', left: 0, top: 0, width: sizeOf(scene).w, height: sizeOf(scene).h}}>
                  {scene.kind === 'title' ? <TitleScene {...props} /> : null}
                  {scene.kind === 'points' ? <PointsScene {...props} /> : null}
                  {scene.kind === 'flow' ? <FlowScene {...props} /> : null}
                  {scene.kind === 'ears' ? <EarsScene {...props} /> : null}
                  {scene.kind === 'sequence' ? <SequenceScene {...props} /> : null}
                  {scene.kind === 'code' ? <CodeScene {...props} /> : null}
                  {scene.kind === 'table' ? <TableScene {...props} /> : null}
                  {scene.kind === 'world' ? <WorldScene {...props} /> : null}
                </div>
              )}
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
    {planned ? <Planned text={planned} /> : null}
  </AbsoluteFill>
);

export const Film: React.FC<{beats: number[]; scenes: {id: string; title: string; seconds: number; refs: string}[]}> = () => (
  <WithFonts>
    <Scenes />
  </WithFonts>
);
