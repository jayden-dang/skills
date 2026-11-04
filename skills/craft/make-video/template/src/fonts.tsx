import {loadFont} from '@remotion/fonts';
import {useEffect, useState} from 'react';
import {cancelRender, continueRender, delayRender, staticFile} from 'remotion';
import {t} from './tokens';

const LATIN = 'U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD';
const LATIN_EXT = 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF';
const VIETNAMESE = 'U+0102-0103,U+0110-0111,U+0128-0129,U+0168-0169,U+01A0-01A1,U+01AF-01B0,U+0300-0301,U+0303-0304,U+0308-0309,U+0323,U+0329,U+1EA0-1EF9,U+20AB';
const subsets = (family: string, stem: string, weight: string) =>
  ([['latin', LATIN], ['latin-ext', LATIN_EXT], ['vietnamese', VIETNAMESE]] as const).map(([name, unicodeRange]) => ({family, file: `${stem}-${name}-wght-normal.woff2`, weight, unicodeRange}));

// Every font file src/tokens.ts names, each in public/fonts/. A project's own look lists its own files here,
// one entry per weight, such as {family: 'Inter', file: 'Inter-Bold.woff2', weight: '700'}.
const fontFiles: {family: string; file: string; weight?: string; unicodeRange?: string}[] = [...subsets('Space Grotesk', 'space-grotesk', '300 700'), ...subsets('Roboto Mono', 'roboto-mono', '100 700')];

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
    Promise.all(fontFiles.map(({family, file, weight, unicodeRange}) => loadFont({family, url: staticFile(`fonts/${file}`), weight, unicodeRange})))
      .then(() => {
        requireFonts();
        setReady(true);
        continueRender(handle);
      })
      .catch(cancelRender);
  }, [handle]);
  return ready ? <>{children}</> : null;
};
