# `make-video`

> A narrated 1080p film of a built feature, a branch, or a release, made from the real code and the running app, or a short film that explains a closed spec.

|  |  |
|---|---|
| **Bucket** | craft |
| **Invocation** | `/make-video <feature, branch, tag, or spec folder>`, or when you ask for a video |
| **Reads** | the code or spec at the pinned commit, the repo's design tokens, `docs/agents/verify.md` when it exists |
| **Writes** | `.skills/video/<slug>/` (git-ignored), and the finished MP4 at the path you name |
| **Calls** | nothing. Uses `agent-browser`, `ffmpeg`, Vibi, and Remotion from npm |
| **Called by** | [`shape`](shape.md) under `--auto --video` |

## What it makes

| You name | Film shows | Made from |
|---|---|---|
| A feature | What the feature does today | `HEAD`, run from a temporary worktree |
| A branch or range | What changes for reviewers, with both sides when it helps | The branch head, and the base when compared |
| A version | What is new for people who use the product | The tag |
| A spec folder | Why it is built this way: a problem, an idea, one example followed through what could go wrong | The commit holding the spec, with no app and no footage |

Narration and captions are English. Ask for another language by name, for example `/make-video v1.3.0 in Vietnamese`.

The voice comes through [Vibi](https://vibi.pro/docs), with no other engine, so the script goes to Vibi and the provider behind it, and the run needs `VIBI_API`; without a key it stops. English and Vietnamese are the MiniMax voices the owner chose, and other languages are ElevenLabs Flash. A rerun pays only for lines that changed, and `--voice` picks another voice from the same provider. Vibi keeps each job with its text in its history until you delete it, and the pages read state no retention period.

## A film of a spec

A spec film is what `/shape #N --auto --video` makes in place of most of the review page, and you can ask for one directly. It runs 120 seconds at most. Every frame says it is planned and not built, and watching it approves nothing.

It explains and does not walk the spec. It opens on what goes wrong today, follows one named example, and takes each "but what if" to the rule that answers it. Films made by following the spec's files gave a reason in 0 to 9% of their lines; these give one in 42 to 64%. Everything happens in one `world` scene, where things stay on screen and change, with a camera. `ears`, `code` and `table` scenes hold exact spec text when the point needs it.

`check_video.py` fails a film with no `world`, anything on screen cut by the camera, fewer than a third of its lines giving a reason, an ID the spec does not define, a reworded rule or code line, footage, or more than one bullet scene. It does not require every requirement: it writes the ones the film leaves out to `out/uncited.json`, and the review page lists them. The recipe is `explainer.md`. A built feature can use the same recipe, with real footage for what a person sees and a `world` for what no screen shows.

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
- A feature with no code and no spec: there is nothing to film.
- Checking that a feature works: [`validate-feature`](validate-feature.md). A film shows a behavior; it does not prove one.
