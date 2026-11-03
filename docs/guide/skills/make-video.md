# `make-video`

> A narrated 1080p film of a built feature, a branch, or a release, made from the real code and the running app.

|  |  |
|---|---|
| **Bucket** | craft |
| **Invocation** | `/make-video <feature, branch, or tag>` (user-invoked; `disable-model-invocation: true`) |
| **Reads** | the code at the pinned commit, the repo's design tokens, `docs/agents/verify.md` when it exists |
| **Writes** | `.skills/video/<slug>/` (git-ignored), and the finished MP4 at the path you name |
| **Calls** | nothing. Uses `agent-browser`, `ffmpeg`, `say`, and Remotion from npm |
| **Called by** | nobody — it is user-invoked |

## What it makes

| You name | Film shows | Made from |
|---|---|---|
| A feature | What the feature does today | `HEAD`, run from a temporary worktree |
| A branch or range | What changes for reviewers, with both sides when it helps | The branch head, and the base when compared |
| A version | What is new for people who use the product | The tag |

Narration and captions are English. Ask for another language by name, for example `/make-video v1.3.0 in Vietnamese`.

The voice is the machine's `say`, so no text leaves the machine. Asking for ElevenLabs sends the script to that vendor and needs `ELEVENLABS_API_KEY`. On a free plan, library voices are refused over the API and premade voices work. Vietnamese needs a model that lists it, which `voice.py` already picks.

## Why it is a template and a check

Seven runs without this skill got every fact right, including the traps a stale README and a reverted feature set for them. All seven still made slideshows: none reached 1080p, and five had no captions. So the skill holds no rule about reading the code. It carries what those runs lacked:

- **A Remotion project in `template/`.** The agent fills `src/script.json` and `src/tokens.ts`, and lists any font files in `src/fonts.tsx`.
- **One layout, in your project's look.** A single window changes shape to fit each line, with the narration under it. The layout belongs to the template. Fonts, colors, radii and shadows come from your repo's tokens. Text too long for the window stops the render and names the scene, and so does a font the machine cannot draw.
- **A camera on each line.** A `focus` rect on a beat moves the camera there, so the thing named fills the frame.
- **A source on each line.** Every spoken line carries a `file:line` or a run output, shown under the caption.
- **`check_video.py`.** It fails a film under 1920x1080, a still over 6 seconds, a silence over 3 seconds, a line with no source, and a `file:line` that does not exist at the pinned commit.

## Before you use it

- **Remotion's license.** It is free for individuals and for companies of up to three people. A larger company needs a [company license](https://www.remotion.pro/license).
- **Rendering.** The fonts follow the project's tokens. A font the project ships or links is loaded from a file. A system font stack renders correctly only on a machine that has those fonts.
- **Listening.** An agent cannot hear the film. It reports that, and the first listen is yours.

## Not this skill

- Slides for a meeting: use a deck, not a film.
- A feature with no code yet: there is nothing to film. A deeper film of a spec is planned as a separate source.
- Checking that a feature works: [`validate-feature`](validate-feature.md). A film shows a behavior; it does not prove one.
