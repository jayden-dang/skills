// Fill every value from the project's design tokens and name that file on the next line.
// Source: <path to the project's tokens>
export const t = {
  fontSans: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
  fontHead: '-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif', // headings; the same as fontSans unless the project differs
  fontMono: 'ui-monospace, Menlo, monospace',
  headWeight: 650,
  headTracking: '-0.02em',
  ground: '#eceef2', // behind everything: any CSS background, so a gradient works
  onGround: '#15181e', // the narration, on the ground
  panel: '#ffffff', // the window; translucent when panelBlur is set
  panelSoft: '#ffffff', // solid, for cards inside the window
  panelBorder: 'rgba(20, 24, 31, 0.1)',
  panelBlur: 'none',
  borderWidth: 1,
  ink: '#15181e', // text on the panel
  muted: '#5b6573',
  accent: '#2c5be0', // must read on the panel
  bad: '#c02a4a',
  radius: 22,
  radiusSmall: 12,
  shadow: '0 24px 60px rgba(20, 24, 31, 0.14)',
};
