// Measures text so the window can hug it. A text that fits at no size stops the render by name.
import {t} from './tokens';

type Face = {font?: string; weight?: number; tracking?: number};

let context: CanvasRenderingContext2D | null = null;

const widthOf = (text: string, size: number, face: Face) => {
  context = context ?? document.createElement('canvas').getContext('2d');
  if (!context) throw new Error('no canvas to measure text with');
  context.font = `${face.weight ?? 500} ${size}px ${face.font ?? t.fontSans}`;
  context.letterSpacing = `${(face.tracking ?? 0) * size}px`;
  return context.measureText(text).width;
};

export const linesOf = (text: string, size: number, width: number, face: Face = {}) => {
  let lines = 1;
  let line = '';
  for (const word of text.split(' ')) {
    const next = line ? `${line} ${word}` : word;
    if (widthOf(next, size, face) * 1.02 <= width) {
      line = next;
    } else {
      if (widthOf(word, size, face) * 1.02 > width) return Infinity;
      lines += 1;
      line = word;
    }
  }
  return lines;
};

// The lines a text breaks into at this size, the same way linesOf counts them.
export const wrap = (text: string, size: number, width: number, face: Face = {}) => {
  const out: string[] = [];
  let line = '';
  for (const word of text.split(' ')) {
    const next = line ? `${line} ${word}` : word;
    if (!line || widthOf(next, size, face) * 1.02 <= width) line = next;
    else {
      out.push(line);
      line = word;
    }
  }
  return line ? [...out, line] : out;
};

export const fit = (owner: string, text: string, sizes: number[], width: number, maxLines: number, face: Face = {}) => {
  for (const size of sizes) {
    const lines = linesOf(text, size, width, face);
    if (lines <= maxLines) return {size, lines};
  }
  throw new Error(`${owner}: "${text}" does not fit. Shorten it.`);
};

export const headFace = {font: t.fontHead, weight: t.headWeight, tracking: parseFloat(t.headTracking)};
