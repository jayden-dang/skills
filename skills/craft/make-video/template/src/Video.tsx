import {Audio} from '@remotion/media';
import {linearTiming, TransitionSeries} from '@remotion/transitions';
import type {TransitionPresentation, TransitionPresentationComponentProps} from '@remotion/transitions';
import {AbsoluteFill, Sequence, staticFile} from 'remotion';
import {ClipScene} from './ClipScene';
import {FlowScene, PointsScene, TitleScene} from './GraphicScenes';
import {Beat, layout, scenes, TRANSITION} from './timing';
import {t} from './tokens';

const Through: React.FC<TransitionPresentationComponentProps<Record<string, never>>> = ({children, presentationDirection, presentationProgress}) => (
  <AbsoluteFill style={{opacity: presentationDirection === 'exiting' ? Math.max(0, 1 - presentationProgress * 2) : Math.max(0, presentationProgress * 2 - 1)}}>{children}</AbsoluteFill>
);
const through = (): TransitionPresentation<Record<string, never>> => ({component: Through, props: {}});

const Caption: React.FC<{beat: Beat}> = ({beat}) => (
  <>
    <div style={{position: 'absolute', left: 34, right: 34, top: 12, fontSize: 38, fontWeight: 500, lineHeight: 1.18, textWrap: 'balance'}}>{beat.text}</div>
    <div style={{position: 'absolute', left: 34, bottom: 9, fontFamily: t.fontMono, fontSize: 20, color: t.muted}}>{beat.ref}</div>
  </>
);

const Staged: React.FC<{text: string}> = ({text}) => (
  <div style={{position: 'absolute', right: 96, top: 26, padding: '8px 20px', borderRadius: 999, background: t.panel, border: `2px solid ${t.bad}`, color: t.bad, fontSize: 28, fontWeight: 600}}>{text}</div>
);

export const Film: React.FC = () => (
  <AbsoluteFill style={{background: t.ground, fontFamily: t.fontSans, color: t.ink}}>
    <TransitionSeries>
      {scenes.flatMap((scene, s) => {
        const {starts, lengths, duration} = layout(scene);
        const parts = [
          <TransitionSeries.Sequence key={scene.id} name={scene.title} durationInFrames={duration}>
            {scene.kind === 'clip' ? <ClipScene scene={scene} starts={starts} lengths={lengths} duration={duration} /> : null}
            {scene.kind === 'title' ? <TitleScene scene={scene} starts={starts} /> : null}
            {scene.kind === 'points' ? <PointsScene scene={scene} starts={starts} /> : null}
            {scene.kind === 'flow' ? <FlowScene scene={scene} starts={starts} /> : null}
            {scene.staged ? <Staged text={scene.staged} /> : null}
            <div style={{position: 'absolute', left: 96, top: 922, width: 1728, height: 138, boxSizing: 'border-box', borderRadius: t.radiusSmall, background: t.panel, backdropFilter: t.panelBlur, border: `1px solid ${t.panelBorder}`, color: t.ink}}>
              {scene.beats.map((beat, i) => (
                <Sequence key={`${scene.id}-${i}`} from={starts[i]} durationInFrames={i === scene.beats.length - 1 ? duration - starts[i] : starts[i + 1] - starts[i]} layout="none" name={`line ${i + 1}`}>
                  <Audio src={staticFile(`voice/${scene.id}-${i}.mp3`)} />
                  <Caption beat={beat} />
                </Sequence>
              ))}
            </div>
          </TransitionSeries.Sequence>,
        ];
        if (s < scenes.length - 1) parts.push(<TransitionSeries.Transition key={`${scene.id}-t`} presentation={through()} timing={linearTiming({durationInFrames: TRANSITION})} />);
        return parts;
      })}
    </TransitionSeries>
  </AbsoluteFill>
);
