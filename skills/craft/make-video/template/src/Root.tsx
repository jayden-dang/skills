import {Composition} from 'remotion';
import {FPS, totalFrames} from './timing';
import {Film} from './Video';

export const RemotionRoot: React.FC = () => <Composition id="Film" component={Film} durationInFrames={totalFrames()} fps={FPS} width={1920} height={1080} />;
