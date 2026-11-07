# `make-video`

> A narrated 1080p film of a built feature, a branch, or a release, made from the real code and the running app, a short film that explains a closed spec, or a film that teaches a concept, drawn in Manim.

|  |  |
|---|---|
| **Bucket** | craft |
| **Invocation** | `/make-video <feature, branch, tag, spec folder, or a topic to learn>`, or when you ask for a video |
| **Reads** | the code or spec at the pinned commit, `docs/agents/verify.md` when it exists, and the repo's design tokens only when you ask for the project's look |
| **Writes** | `.skills/video/<slug>/` (git-ignored), and the finished MP4 at the path you name |
| **Calls** | [`research`](research.md) for a concept film. Uses `agent-browser`, `ffmpeg`, Vibi, Remotion from npm, and Manim Community Edition for a concept film |
| **Called by** | [`shape`](shape.md) under `--auto --video` |

## What it makes

| You name | Film shows | Made from |
|---|---|---|
| A feature | What the feature does today | `HEAD`, run from a temporary worktree |
| A branch or range | What changes for reviewers, with both sides when it helps | The branch head, and the base when compared |
| A version | What is new for people who use the product | The tag |
| A spec folder | Why it is built this way: a problem, an idea, one example followed through what could go wrong | The commit holding the spec, with no app and no footage |
| A topic to learn | One idea taught: a protocol, an algorithm, a data structure, in this repo or not | The sources that own it, found by `research`, and Manim |

Narration and captions are English. Ask for another language by name, for example `/make-video v1.3.0 in Vietnamese`.

The voice comes through [Vibi](https://vibi.pro/docs), with no other engine, so the script goes to Vibi and the provider behind it, and the run needs `VIBI_API`; without a key it stops. English and Vietnamese are the MiniMax voices the owner chose, and other languages are ElevenLabs Flash. A rerun pays only for lines that changed, and `--voice` picks another voice from the same provider. Vibi keeps each job with its text in its history until you delete it, and the pages read state no retention period.

## A film of a spec

A spec film is what `/shape #N --auto --video` puts on its spec sheet, and you can ask for one directly. It runs 120 seconds at most. Every frame says it is planned and not built, and watching it approves nothing.

It explains and does not walk the spec. It opens on what goes wrong today, follows one named example, and takes each "but what if" to the rule that answers it. Films made by following the spec's files gave a reason in 0 to 9% of their lines; these give one in 42 to 64%. Everything happens in one `world` scene, where things stay on screen and change on the word that names the change, with a camera. `ears`, `code` and `table` scenes hold exact spec text when the point needs it.

`check_video.py` fails a film with no `world`, anything on screen cut by the camera, a line that changes nothing or runs more than 9 words (14 in Vietnamese) on one state, a hold over 4.5 seconds, fewer than a third of its lines giving a reason, an ID the spec does not define, a reworded rule or code line, footage, or more than one bullet scene. It does not require every requirement: it writes the ones the film leaves out to `out/uncited.json`, and the spec sheet says what each of them asks. The recipe is `explainer.md`. A built feature can use the same recipe, with real footage for what a person sees and a `world` for what no screen shows.

## A film that teaches a concept

Ask for a video that teaches you something, such as Raft leader election, and the film is a `concept`. The topic needs no
code in the repo. Every line cites a source the run found first (a paper section, an RFC, official docs, or a `file:line`),
listed with its full citation in the script. The idea is drawn in Manim, scene by scene, timed to the words of the voice,
and composited over the film's own look. It tells the story the way a spec film does, and may run 300 seconds.

`check_video.py` fails a concept film with no sources, a line citing none of them, no `manim` or `world` scene, fewer than
a third of its lines giving a reason, a hold over 4.5 seconds, or a Manim scene that was not rendered. The first Manim
scene installs Manim Community Edition into `~/.cache/make-video/manim`, which needs Python 3.11 or later. The recipe is
`concept.md`.

## Why it is a template and a check

Seven runs without this skill got every fact right, including the traps a stale README and a reverted feature set for them. All seven still made slideshows: none reached 1080p, and five had no captions. So the skill holds no rule about reading the code. It carries what those runs lacked:

- **A Remotion project in `template/`.** The agent fills `src/script.json`.
- **One layout, one look.** Two thin bands hold the subject, the scene, its numbers and the narration, and everything between them is content. Every film has the same look: near-black, hairlines, cut-corner frames with a moving spectrum edge, Space Grotesk and Roboto Mono, both under the Open Font License and shipped in the template with Vietnamese. Ask for "our own design system", or pass `--project-style` from `/shape`, and the fonts, colors, radii and shadows come from your repo's tokens instead. Text too long for its box stops the render and names the scene, and so does a font the machine cannot draw.
- **A quiet sound layer.** A low bed and a small hit on each change, synthesized by the template, under the voice.
- **A camera on each line.** A `focus` rect on a beat moves the camera there, so the thing named fills the frame.
- **A source on each line.** Every spoken line carries a `file:line` or a run output, shown beside the narration.
- **`check_video.py`.** It fails a film under 1920x1080, a hold over 6 seconds, a silence over 3 seconds, a line with no source, and a `file:line` that does not exist at the pinned commit.

## Before you use it

- **Remotion's license.** It is free for individuals and for companies of up to three people. A larger company needs a [company license](https://www.remotion.pro/license).
- **Rendering.** The default look's fonts ship with the template. In the project's own look, a font the project ships or links is loaded from a file, and a system font stack renders correctly only on a machine that has those fonts.
- **Listening.** An agent cannot hear the film. It reports that, and the first listen is yours.

## Not this skill

- Slides for a meeting: use a deck, not a film.
- A feature with no code and no spec: there is nothing to film.
- Checking that a feature works: [`validate-feature`](validate-feature.md). A film shows a behavior; it does not prove one.
