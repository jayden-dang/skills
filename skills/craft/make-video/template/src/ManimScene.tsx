import {getStaticFiles, OffthreadVideo, staticFile} from 'remotion';
import {Scene} from './timing';
import {WORLD_H, WORLD_W} from './WorldScene';
import {t} from './tokens';

// A scene drawn by Manim: manim/<id>.py, rendered by render_manim.py to public/manim/<id>.webm with a
// transparent background, exactly as long as the scene. Until then the frame says what is missing.
export const MANIM_SIZE = {w: WORLD_W, h: WORLD_H};

export const ManimScene: React.FC<{scene: Scene}> = ({scene}) => {
  const name = `manim/${scene.id}.webm`;
  if (!getStaticFiles().some((f) => f.name === name)) {
    return <div style={{...MANIM_SIZE, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: t.fontMono, fontSize: 30, color: t.warn}}>{`${name} is not rendered yet`}</div>;
  }
  return <OffthreadVideo src={staticFile(name)} transparent muted style={{...MANIM_SIZE, display: 'block'}} />;
};
