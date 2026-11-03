import {Composition} from 'remotion';
import {beatFrames, FPS, totalFrames} from './timing';
import {Film} from './Video';

export const RemotionRoot: React.FC = () => <Composition id="Film" component={Film} defaultProps={{beats: beatFrames()}} durationInFrames={totalFrames()} fps={FPS} width={1920} height={1080} />;
