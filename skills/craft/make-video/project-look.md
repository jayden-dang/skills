# A film in the project's own look

Fill every value in `src/tokens.ts` from the repo's design tokens and name that file in its `Source:` comment. Find them through
`docs/standards/`, `docs/agents/`, then any theme or tokens file. A repo with none keeps the default look, and your report says so.
Set `cut` to `0` and `spectrum` to `[]`, so frames take the project's radius and border. Set `line` to the project's divider color,
`warn` to the closest token it has, and `onGroundAccent` to a token that reads on `ground`.

Replace `fontFiles` in `src/fonts.tsx` with every font the tokens name, its file copied into `public/fonts/`. A font the repo only
links from a service gets downloaded the same way. One run named a Google font and never loaded it: the film came out in Helvetica,
the check passed, and its report called it "Figtree-like". The render now stops on a font it cannot draw. With no file to be had,
take that name out of the tokens and say so in your report. A repo that allows only a system font stack leaves `fontFiles` empty.

*Done when: `Source:` names a file, or your report will say there is none.*
