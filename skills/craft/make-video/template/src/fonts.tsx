import {loadFont} from '@remotion/fonts';
import {useEffect, useState} from 'react';
import {cancelRender, continueRender, delayRender, staticFile} from 'remotion';
import {t} from './tokens';

// Every font file the project ships that src/tokens.ts names. Copy each into public/fonts/ and list it here,
// one entry per weight, such as {family: 'Inter', file: 'Inter-Bold.woff2', weight: '700'}.
const fontFiles: {family: string; file: string; weight?: string}[] = [];

// Keywords, plus Apple's system faces: a browser reaches those through a keyword, never by name.
const BUILT_IN = ['serif', 'sans-serif', 'monospace', 'cursive', 'fantasy', 'system-ui', 'ui-serif', 'ui-sans-serif', 'ui-monospace', 'ui-rounded', '-apple-system', 'blinkmacsystemfont', 'sf mono', 'sf pro', 'sf pro text', 'sf pro display'];

const canDraw = (family: string) => {
  const context = document.createElement('canvas').getContext('2d');
  if (!context) throw new Error('no canvas to check fonts with');
  const sample = 'Delay alerts 0123456789';
  return ['serif', 'monospace'].some((fallback) => {
    context.font = `48px ${fallback}`;
    const without = context.measureText(sample).width;
    context.font = `48px "${family}", ${fallback}`;
    return context.measureText(sample).width !== without;
  });
};

// A browser swaps a font it cannot find without a word, and the film comes out in the wrong typeface.
const requireFonts = () => {
  for (const stack of [t.fontSans, t.fontHead, t.fontMono]) {
    const first = stack.split(',')[0].trim().replace(/^['"]|['"]$/g, '');
    if (!BUILT_IN.includes(first.toLowerCase()) && !canDraw(first)) {
      throw new Error(`src/tokens.ts names the font "${first}", and this machine cannot draw it. Copy its file into public/fonts/ and list it in src/fonts.tsx.`);
    }
  }
};

export const WithFonts: React.FC<{children: React.ReactNode}> = ({children}) => {
  const [handle] = useState(() => delayRender('Loading the project fonts'));
  const [ready, setReady] = useState(false);
  useEffect(() => {
    Promise.all(fontFiles.map(({family, file, weight}) => loadFont({family, url: staticFile(`fonts/${file}`), weight})))
      .then(() => {
        requireFonts();
        setReady(true);
        continueRender(handle);
      })
      .catch(cancelRender);
  }, [handle]);
  return ready ? <>{children}</> : null;
};
