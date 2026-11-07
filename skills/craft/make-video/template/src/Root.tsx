import {Composition} from 'remotion';
import {beatFrames, FPS, restWindows, sceneIndex, sceneTiming, soundEvents, totalFrames} from './timing';
import {Film} from './Video';

export const RemotionRoot: React.FC = () => <Composition id="Film" component={Film} defaultProps={{beats: beatFrames(), scenes: sceneIndex(), events: soundEvents(), timing: sceneTiming(), rests: restWindows()}} durationInFrames={totalFrames()} fps={FPS} width={1920} height={1080} />;
