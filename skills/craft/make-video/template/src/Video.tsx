import {Audio} from '@remotion/media';
import {useState} from 'react';
import {AbsoluteFill, Easing, getStaticFiles, interpolate, Sequence, staticFile, useCurrentFrame} from 'remotion';
import {ASIDE_CLIP_W, CLIP_W, clipHeights, ClipScene, FULL, MOVE, MOVE_EASING} from './ClipScene';
import {fit} from './fit';
import {WithFonts} from './fonts';
import {clamp, enter, FlowScene, graphicSize, PointsScene, TitleScene} from './GraphicScenes';
import {Backdrop, cutShape, Decode, Edge, glide, rise, Roll, SweepLine} from './Look';
import {CodeScene, EarsScene, SequenceScene, SPEC_KINDS, specSize, TableScene} from './SpecScenes';
import {Beat, filmName, placed, planned, Scene, SoundEvent, totalFrames, TRANSITION, wordStarts, worldSteps} from './timing';
import {worldSize, WorldScene} from './WorldScene';
import {MANIM_SIZE, ManimScene} from './ManimScene';
import {CompareScene, compareSize, StatScene, statSize, TimelineScene, timelineSize} from './ChangeScenes';
import {t} from './tokens';

/* Two thin bands hold what the film is and where it stands. Between them, one window lives through the
   whole film and changes shape to fit each line. A world draws its own frames and needs no window. */

type Box = {x: number; y: number; w: number; h: number};
const TOP = 72;
const BOTTOM = 984;
const CENTER_Y = (TOP + BOTTOM) / 2;
const CELL_A = 324;
const CELL_B = 960;
const CELL_C = 1597;
const MONO = (size: number) => ({font: t.fontMono, weight: 400, tracking: 0.08, size});
const sizeOf = (scene: Scene) => (scene.kind === 'compare' ? compareSize() : scene.kind === 'stat' ? statSize(scene) : scene.kind === 'timeline' ? timelineSize() : scene.kind === 'manim' ? MANIM_SIZE : scene.kind === 'world' ? worldSize(scene) : SPEC_KINDS.includes(scene.kind) ? specSize(scene) : graphicSize(scene));
const centered = (w: number, h: number): Box => ({x: (1920 - w) / 2, y: CENTER_Y - h / 2, w, h});
// A scene with notes leaves them a column on the right; its picture centres in what is left, scaled down to fit.
const ASIDE_W = 400;
const MAIN_W = 1920 - ASIDE_W - 120;
const besideNotes = (w: number, h: number): Box => ({x: 40 + (MAIN_W - w) / 2, y: CENTER_Y - h / 2, w, h});
const asideScale = (scene: Scene) => (scene.aside?.length && scene.kind !== 'clip' ? Math.min(1, MAIN_W / sizeOf(scene).w) : 1);
// A scene change lands softly; a small change of shape takes less time than a large one, and always ends with the transition.
const LAND = Easing.bezier(0.22, 1, 0.36, 1);
const morphFrames = (a: Box, b: Box) => Math.round(12 + 12 * Math.min(1, Math.max(Math.abs(a.x - b.x), Math.abs(a.y - b.y), Math.abs(a.w - b.w), Math.abs(a.h - b.h)) / 600));

// Every shape the window takes, in order, with the frame it starts moving there. Measured text, so
// this runs inside WithFonts, once the project's fonts are in.
const shapesOf = () =>
  placed.flatMap(({scene, from, starts}) => {
    if (scene.kind !== 'clip') {
      const {w, h} = sizeOf(scene);
      const k = asideScale(scene);
      return [{at: from, box: scene.aside?.length ? besideNotes(w * k, h * k) : centered(w, h), bare: scene.kind === 'world' || scene.kind === 'manim' ? 1 : 0, cut: true}];
    }
    if (scene.full) return [{at: from, box: FULL, bare: 1, cut: true}];
    return clipHeights(scene).map((h, i) => ({at: i === 0 ? from : from + starts[i], box: scene.aside?.length ? besideNotes(ASIDE_CLIP_W, h) : centered(CLIP_W, h), bare: 0, cut: i === 0}));
  });

const Window: React.FC<{children: React.ReactNode}> = ({children}) => {
  const frame = useCurrentFrame();
  const [shapes] = useState(shapesOf);
  const input: number[] = [];
  const boxes: Box[] = [];
  const bares: number[] = [];
  const eases: boolean[] = [];
  shapes.forEach(({at, box, bare, cut}, i) => {
    if (i === 0) return;
    const length = cut ? morphFrames(shapes[i - 1].box, box) : MOVE;
    const start = Math.max(cut ? at + TRANSITION - length : at, (input[input.length - 1] ?? -1) + 1);
    input.push(start, start + length);
    boxes.push(shapes[i - 1].box, box);
    bares.push(shapes[i - 1].bare, bare);
    eases.push(Boolean(cut));
  });
  // Each move eases on its own: a scene change lands softly, a camera move inside a clip keeps its own curve.
  const at = (key: keyof Box) => {
    if (!input.length) return shapes[0].box[key];
    for (let k = 0; k < input.length; k += 2) {
      if (frame < input[k]) return boxes[k][key];
      if (frame <= input[k + 1]) return interpolate(frame, [input[k], input[k + 1]], [boxes[k][key], boxes[k + 1][key]], {...clamp, easing: eases[k / 2] ? LAND : MOVE_EASING});
    }
    return boxes[boxes.length - 1][key];
  };
  const bare = input.length ? interpolate(frame, input, bares, clamp) : shapes[0].bare;
  const [w, h] = [at('w'), at('h')];
  const shape = t.cut > 0 ? cutShape(w, h) : undefined;
  return (
    <div style={{position: 'absolute', left: at('x'), top: at('y'), width: w, height: h, color: t.ink, opacity: enter(frame, 0, 12)}}>
      <div style={{position: 'absolute', inset: 0, background: t.panel, backdropFilter: t.panelBlur, boxShadow: t.shadow, clipPath: shape, borderRadius: t.cut > 0 ? 0 : t.radius, opacity: 1 - bare}} />
      <div style={{position: 'absolute', inset: 0, opacity: bare < 1 ? 1 : 0}}>
        <Edge id="window-edge" w={w} h={h} draw={Math.min(glide(frame, 0, 34), 1 - bare)} width={Math.max(t.borderWidth, 2)} />
      </div>
      {/* A window cuts what it holds; a world keeps the room its corner marks need. */}
      <div style={{position: 'absolute', inset: 0, clipPath: bare > 0.5 ? 'inset(-30px)' : (shape ?? `inset(0 round ${t.radius}px)`)}}>{children}</div>
    </div>
  );
};

// How one scene hands over to the next, chosen from what the two are, never by the script:
// the same kind in the same window pushes sideways like a page; anything else crosses in place.
type Hand = 'cross' | 'push';
const KIN = (scene: Scene) => (scene.kind === 'world' || scene.kind === 'manim' ? 'bare' : scene.kind === 'clip' && scene.full ? 'full' : scene.kind);
const handOf = (a: Scene | undefined, b: Scene | undefined): Hand => {
  if (!a || !b || KIN(a) !== KIN(b) || a.kind === 'clip' || a.kind === 'world' || a.kind === 'manim') return 'cross';
  const [x, y] = [sizeOf(a), sizeOf(b)];
  return Math.abs(x.w - y.w) < 80 && Math.abs(x.h - y.h) < 120 ? 'push' : 'cross';
};
// A new part of the film starts at a title or where the kind of picture changes; only there does the line sweep across.
const opensPart = (a: Scene, b: Scene) => b.kind === 'title' || KIN(a) !== KIN(b);

const SceneFade: React.FC<{duration: number; first: boolean; last: boolean; inHand?: Hand; outHand?: Hand; children: React.ReactNode}> = ({duration, first, last, inHand = 'cross', outHand = 'cross', children}) => {
  const frame = useCurrentFrame();
  // The two scenes cross: the old one is still fading while the new one comes in, so the window is never empty.
  const inn = first ? 1 : interpolate(frame, [TRANSITION * 0.42, TRANSITION], [0, 1], clamp);
  const out = last ? 1 : interpolate(frame, [duration - TRANSITION, duration - TRANSITION * 0.42], [1, 0], clamp);
  const shift = (inHand === 'push' ? (1 - inn) * 90 : 0) - (outHand === 'push' ? (1 - out) * 90 : 0);
  return <AbsoluteFill style={{opacity: Math.min(inn, out), translate: `${shift}px 0px`}}>{children}</AbsoluteFill>;
};

const Cell: React.FC<{left: number; width?: number; top: number; height: number; children: React.ReactNode; gap?: number}> = ({left, width, top, height, children, gap = 0}) => (
  <div style={{position: 'absolute', left, width, top, height, display: 'flex', alignItems: 'center', gap}}>{children}</div>
);

const Bands: React.FC = () => {
  const frame = useCurrentFrame();
  const h = (y: number, d: number) => <div key={y} style={{position: 'absolute', top: y, left: 0, height: 1, width: `${glide(frame, d, 40) * 100}%`, background: t.line}} />;
  const up = (x: number, d: number) => <div key={`u${x}`} style={{position: 'absolute', left: x, top: 0, width: 1, height: TOP * glide(frame, d, 20), background: t.line}} />;
  const down = (x: number, d: number) => <div key={`d${x}`} style={{position: 'absolute', left: x, top: BOTTOM, width: 1, height: (1080 - BOTTOM) * glide(frame, d, 20), background: t.line}} />;
  const name = filmName?.toUpperCase();
  const nameSize = name ? fit('name', name, [22, 19, 16], CELL_A - 90, 1, MONO(22)).size : 22;
  return (
    <AbsoluteFill>
      {/* The bands cover whatever the camera carries past them. */}
      <div style={{position: 'absolute', left: 0, right: 0, top: 0, height: TOP, background: t.ground}} />
      <div style={{position: 'absolute', left: 0, right: 0, top: BOTTOM, bottom: 0, background: t.ground}} />
      {[h(TOP, 4), h(BOTTOM, 8), up(CELL_A, 12), up(CELL_B, 14), up(CELL_C, 16), down(CELL_A, 12), down(CELL_C, 16)]}
      {t.spectrum.length ? <div style={{position: 'absolute', left: CELL_A, top: 0, height: 3, width: (CELL_B - CELL_A) * glide(frame, 12, 30), background: `linear-gradient(90deg,${t.spectrum.join(',')})`}} /> : null}
      <Cell left={36} top={0} height={TOP} gap={7}>
        {[0, 1].map((n) => <div key={n} style={{width: 8, height: 8, borderRadius: 8, background: t.onGround, opacity: rise(frame, 10 + n * 4, 10)}} />)}
        {name ? <div style={{marginLeft: 10}}><Decode text={name} start={12} size={nameSize} color={t.onGround} /></div> : null}
      </Cell>
      {planned ? (
        <Cell left={CELL_C + 20} width={1920 - CELL_C - 40} top={0} height={TOP}>
          <div style={{position: 'relative', height: 42, width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', opacity: rise(frame, 20, 14)}}>
            <Edge id="planned-edge" w={1920 - CELL_C - 40} h={42} width={1.5} />
            <Decode text={planned.toUpperCase()} start={24} size={fit('planned', planned.toUpperCase(), [18, 16, 14, 12], 1920 - CELL_C - 64, 1, {font: t.fontMono, weight: 400, tracking: 0.04}).size} tracking="0.04em" color={t.onGround} />
          </div>
        </Cell>
      ) : null}
    </AbsoluteFill>
  );
};

// What this part of the film is about, in the band above it.
const Section: React.FC<{scene: Scene}> = ({scene}) => {
  if (scene.kind === 'title') return null;
  const text = scene.title.toUpperCase();
  const {size} = fit(scene.id, text, [22, 19, 16], CELL_B - CELL_A - 56, 1, MONO(22));
  return <Cell left={CELL_A + 32} top={0} height={TOP}><Decode text={text} start={10} size={size} color={t.onGround} /></Cell>;
};

// The numbers a world keeps, in the empty cell above it. A number rolls on the word that changes it.
const Stats: React.FC<{scene: Scene; starts: number[]; lengths: number[]}> = ({scene, starts, lengths}) => {
  const frame = useCurrentFrame();
  if (scene.kind !== 'world') return null;
  const seen: Record<string, {at: number; value: string}[]> = {};
  for (const {change, at} of worldSteps(scene, starts, lengths)) {
    for (const [label, value] of Object.entries(change.stats ?? {})) (seen[label] ??= []).push({at, value: String(value)});
  }
  // A number that runs into the next cell is unreadable, so it stops the render by name.
  const wide = Object.entries(seen).reduce((sum, [label, values]) => sum + label.length * 14 + 14 + Math.max(...values.map((v) => v.value.length)) * 24, 0) + 36 * Math.max(0, Object.keys(seen).length - 1);
  if (wide > CELL_C - CELL_B - 48) throw new Error(`${scene.id}: too many numbers for the top band. Keep the two that matter, or shorten their names.`);
  return (
    <Cell left={CELL_B + 32} width={CELL_C - CELL_B - 48} top={0} height={TOP} gap={36}>
      {Object.entries(seen).map(([label, values]) => {
        const i = values.reduce((last, v, k) => (frame >= v.at ? k : last), -1);
        if (i < 0) return null;
        const color = values[i].value === '0' ? t.bad : t.onGroundAccent;
        return (
          <span key={label} style={{display: 'flex', alignItems: 'center', gap: 14, opacity: rise(frame, values[0].at, 16)}}>
            <span style={{opacity: 0.6}}><Decode text={label.toUpperCase()} start={values[0].at} size={20} color={t.onGround} /></span>
            <Roll before={i > 0 ? values[i - 1].value : undefined} value={values[i].value} since={values[i].at} size={40} color={color} />
          </span>
        );
      })}
    </Cell>
  );
};

// A long path keeps its file and line: the folders are in the film's report.
const shortRef = (ref: string) => ref.split(/,\s*|\s{2,}/).map((part) => part.split('/').pop() ?? part);

const Caption: React.FC<{scene: Scene; beat: Beat; index: number; length: number}> = ({scene, beat, index, length}) => {
  const frame = useCurrentFrame();
  const words = beat.text.split(/\s+/);
  const times = wordStarts(scene, index, length);
  const {size} = fit(`${scene.id}-${index}`, beat.text, [32, 28, 25], CELL_C - CELL_A - 64, 2);
  const refs = shortRef(beat.ref);
  const refsShown = refs.slice(0, 2);
  const extra = refs.length - refsShown.length;
  return (
    <>
      <div style={{position: 'absolute', left: 36, width: CELL_A - 52, top: BOTTOM, height: 1080 - BOTTOM, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 4, overflow: 'hidden'}}>
        {refsShown.map((r, i) => <div key={r} style={{whiteSpace: 'nowrap'}}><Decode text={i === refsShown.length - 1 && extra ? `${r} +${extra}` : r} start={0} size={20} tracking="0.02em" color={t.onGroundAccent} /></div>)}
      </div>
      <div style={{position: 'absolute', left: CELL_A + 32, right: 1920 - CELL_C + 32, top: BOTTOM, height: 1080 - BOTTOM, display: 'flex', flexWrap: 'wrap', alignContent: 'center', fontSize: size, fontWeight: 400, lineHeight: 1.2, color: t.onGround, textShadow: t.onGroundShadow}}>
        {words.map((w, k) => (
          <span key={k} style={{marginRight: '0.26em', whiteSpace: 'pre', opacity: 0.16 + 0.84 * rise(frame, times[k] - 3, 10)}}>{w}</span>
        ))}
      </div>
    </>
  );
};

// Where the film stands: one segment per scene, sized by its length, the current one filling as its lines go by.
const Where: React.FC<{line: number; lines: number; scene: number; done: number}> = ({line, lines, scene, done}) => {
  const total = placed.reduce((sum, p) => sum + p.duration, 0);
  return (
    <Cell left={CELL_C + 28} top={BOTTOM} height={1080 - BOTTOM} gap={18}>
      <span style={{fontFamily: t.fontMono, fontSize: 20, letterSpacing: '0.08em', color: t.onGround, opacity: 0.6, whiteSpace: 'nowrap'}}>{`${String(line + 1).padStart(2, '0')}/${String(lines).padStart(2, '0')}`}</span>
      <div style={{width: 150, height: 4, display: 'flex', gap: 3}}>
        {placed.map((p, k) => (
          <div key={k} style={{flexGrow: p.duration / total, height: 4, background: t.line, position: 'relative', overflow: 'hidden'}}>
            <div style={{position: 'absolute', left: 0, top: 0, bottom: 0, width: `${k < scene ? 100 : k === scene ? done * 100 : 0}%`, background: t.onGroundAccent}} />
          </div>
        ))}
      </div>
    </Cell>
  );
};

// Notes beside the picture: each arrives on its line and stays, the newest lit, so the screen keeps what was said.
const Aside: React.FC<{scene: Scene; starts: number[]; lengths: number[]}> = ({scene, starts, lengths}) => {
  const frame = useCurrentFrame();
  const notes = scene.aside ?? [];
  const ats = notes.map((note, i) => starts[Math.min(note.at ?? i, starts.length - 1)] + (note.at === undefined && i >= starts.length ? Math.round(((i - starts.length + 1) * lengths[starts.length - 1]) / (notes.length - starts.length + 1)) : 0) + 6);
  const lit = ats.reduce((last, a, i) => (frame >= a ? i : last), -1);
  const x = 40 + MAIN_W + 40;
  return (
    <div style={{position: 'absolute', left: x, width: ASIDE_W, top: TOP + 40, bottom: 1080 - BOTTOM + (scene.staged ? 96 : 40), display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 18}}>
      {notes.map((note, i) => {
        const p = rise(frame, ats[i], 14);
        const size = fit(`${scene.id}-aside-${i}`, note.text, [30, 27, 24], ASIDE_W - 44, 3).size;
        return (
          <div key={i} style={{position: 'relative', padding: '16px 18px 16px 24px', background: t.panelSoft, border: `${t.borderWidth}px solid ${i === lit ? t.accent : t.panelBorder}`, borderRadius: t.radiusSmall, fontSize: size, lineHeight: 1.25, color: i === lit ? t.ink : t.muted, opacity: p, translate: `${(1 - p) * 24}px 0px`}}>
            <div style={{position: 'absolute', left: 0, top: 12, bottom: 12, width: 4, background: i === lit ? t.accent : t.panelBorder}} />
            {note.text}
          </div>
        );
      })}
    </div>
  );
};

const Staged: React.FC<{text: string}> = ({text}) => (
  <div style={{position: 'absolute', right: 40, bottom: 1080 - BOTTOM + 14, padding: '6px 18px', borderRadius: Math.max(t.radiusSmall, 0), background: t.panelSoft, border: `${t.borderWidth}px solid ${t.bad}`, color: t.bad, fontSize: 24, fontWeight: 500}}>{text}</div>
);

const Scenes: React.FC = () => {
  const lines = placed.reduce((sum, {scene}) => sum + scene.beats.length, 0);
  let line = 0;
  const hasSound = getStaticFiles().some((f) => f.name === 'sound.wav');
  return (
    <AbsoluteFill style={{background: t.ground, fontFamily: t.fontSans, overflow: 'hidden'}}>
      <Backdrop />
      {hasSound ? <Audio src={staticFile('sound.wav')} /> : null}
      <Window>
        {placed.map(({scene, from, duration, starts, lengths}, s) => {
          const props = {scene, starts, lengths};
          return (
            <Sequence key={scene.id} from={from} durationInFrames={duration} name={scene.title}>
              <SceneFade duration={duration} first={s === 0} last={s === placed.length - 1} inHand={handOf(placed[s - 1]?.scene, scene)} outHand={handOf(scene, placed[s + 1]?.scene)}>
                {scene.kind === 'clip' ? (
                  <ClipScene {...props} duration={duration} />
                ) : (
                  // Sized to the scene's own shape and held at the window's centre, so its text stays put while the window moves.
                  <div style={{position: 'absolute', left: '50%', top: '50%', translate: '-50% -50%', width: sizeOf(scene).w, height: sizeOf(scene).h, scale: String(asideScale(scene))}}>
                    {scene.kind === 'title' ? <TitleScene {...props} /> : null}
                    {scene.kind === 'points' ? <PointsScene {...props} /> : null}
                    {scene.kind === 'flow' ? <FlowScene {...props} /> : null}
                    {scene.kind === 'ears' ? <EarsScene {...props} /> : null}
                    {scene.kind === 'sequence' ? <SequenceScene {...props} /> : null}
                    {scene.kind === 'code' ? <CodeScene {...props} /> : null}
                    {scene.kind === 'table' ? <TableScene {...props} /> : null}
                    {scene.kind === 'world' ? <WorldScene {...props} /> : null}
                    {scene.kind === 'manim' ? <ManimScene scene={scene} /> : null}
                    {scene.kind === 'compare' ? <CompareScene {...props} /> : null}
                    {scene.kind === 'stat' ? <StatScene {...props} /> : null}
                    {scene.kind === 'timeline' ? <TimelineScene {...props} /> : null}
                  </div>
                )}
              </SceneFade>
            </Sequence>
          );
        })}
      </Window>
      <Bands />
      {placed.map(({scene, from, duration, starts, lengths}, s) => (
        <Sequence key={scene.id} from={from} durationInFrames={duration} name={`${scene.title}: narration`}>
          <SceneFade duration={duration} first={s === 0} last={s === placed.length - 1}>
            <Section scene={scene} />
            <Stats scene={scene} starts={starts} lengths={lengths} />
            {scene.beats.map((beat, i) => {
              const here = line++;
              return (
                <Sequence key={i} from={starts[i]} durationInFrames={(starts[i + 1] ?? duration) - starts[i]} layout="none" name={`line ${i + 1}`}>
                  <Audio src={staticFile(`voice/${scene.id}-${i}.mp3`)} />
                  <Caption scene={scene} beat={beat} index={i} length={lengths[i]} />
                  <Where line={here} lines={lines} scene={s} done={(i + 1) / scene.beats.length} />
                </Sequence>
              );
            })}
            {scene.aside?.length ? <Aside scene={scene} starts={starts} lengths={lengths} /> : null}
            {scene.staged ? <Staged text={scene.staged} /> : null}
          </SceneFade>
        </Sequence>
      ))}
      {placed.map(({from, scene}, s) => (s > 0 && opensPart(placed[s - 1].scene, scene) ? <SweepLine key={scene.id} start={from - 4} /> : null))}
      <SweepLine start={0} />
      <SweepLine start={totalFrames() - 30} />
    </AbsoluteFill>
  );
};

export const Film: React.FC<{beats: number[]; scenes: {id: string; title: string; seconds: number; refs: string}[]; events: SoundEvent[]; timing: Record<string, unknown>; rests: number[][]; cuts: number[]}> = () => (
  <WithFonts>
    <Scenes />
  </WithFonts>
);
