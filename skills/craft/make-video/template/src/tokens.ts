// The film's look. It stays as it is unless the request asks for the project's own look.
// Source: make-video's default look
export const t = {
  fontSans: '"Space Grotesk", sans-serif',
  fontHead: '"Space Grotesk", sans-serif', // headings; the same as fontSans unless the project differs
  fontMono: '"Roboto Mono", monospace',
  headWeight: 300,
  headTracking: '-0.02em',
  ground: '#0a090f', // behind everything: any CSS background, so a gradient works
  onGround: '#efefe5', // the narration and the labels in the two bands
  onGroundShadow: 'none', // for a project whose text on its wallpaper carries one
  onGroundAccent: '#26f4d0', // the numbers and sources in the bands: must read on the ground
  line: '#353539', // the hairlines of the two bands
  panel: 'linear-gradient(187deg,#1c1b21f2,#121217f2 89%)', // the window; translucent when panelBlur is set
  panelSoft: '#17161c', // solid, for cards inside the window
  panelBorder: '#353539',
  panelBlur: 'none',
  borderWidth: 1,
  ink: '#efefe5', // text on the panel
  muted: '#a0a09a',
  accent: '#26f4d0', // must read on the panel
  warn: '#f8cf3e', // something held or waiting
  bad: '#fc6756',
  radius: 0,
  radiusSmall: 0,
  shadow: 'none',
  cut: 26, // the corner cut from a window and a card; 0 draws radius instead
  spectrum: ['#fc6756', '#f8cf3e', '#26f4d0', '#724ce8'], // the moving edge of a frame; [] draws panelBorder instead
};
