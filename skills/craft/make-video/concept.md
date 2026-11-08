# Teach a concept

A `concept` film teaches one idea to someone who wants to learn it: a protocol, an algorithm, a data structure, a
library's model. The topic needs no code in this repo. Both runs asked for one on 3.0.0 stopped instead, because the
film had nothing to cite.

## 1. Sources before lines

REQUIRED SUB-SKILL: use `research` to find the sources that own the topic: the paper, the RFC or spec, the official
docs, the library's source. In `src/script.json`:

```json
{"source": {"kind": "concept", "topic": "Raft leader election"},
 "sources": [{"id": "raft-5.2", "cite": "Ongaro and Ousterhout 2014, In Search of an Understandable Consensus Algorithm, section 5.2"}],
 ...}
```

Each line's `ref` names an `id` from `sources`, or a `file:line` when this repo holds the code. Add `source.ref`, the
commit, only when a line cites a file.

## 2. The story

Write it as `explainer.md` sections 1 and 2 say: the problem on a named example first, then the idea, then the example
moving forward with each complication as it happens. A third of the lines give a reason; the check counts them.

In each `manim` or `world` scene, set `"rest": true` on the one line that lands its key idea, such as "so two candidates cannot both win".
The picture stands 2.5 seconds after the words so the viewer can take it in, and that hold may run to 8 seconds. One
rested line a scene; the check fails a second, and a rest in any film but a concept.

## 3. Draw the idea in Manim

Before the script, run `python3 "$SKILL/scripts/render_manim.py" --check`. It finds a Python new enough, installs Manim
the first time (under a minute), and prints `manim ready`. Only a `FAIL` from it means a `world` instead: one run drew a
world because `python3 --version` said 3.9, while a newer Python sat on the path and Manim would have run. Another drew
worlds for a three-episode course because "Manim is not installed here": `--check` installs it.

The scene that carries the idea is `{"id": "elect", "kind": "manim", "title": ..., "beats": [...]}`: the lines only.
Its picture is `manim/elect.py` in the project, a class `Film` built on `FilmScene`, drawn with Manim Community Edition.
Put the scene in the script now, with its lines; write its picture after `voice.py`, because it times itself to the
voice. One run drew worlds instead because "Manim scenes need out/timing.json, which only exists after the voice step":
that file is for the picture, not the script.

```bash
(cd <project> && node preview.mjs)                       # writes out/timing.json
python3 "$SKILL/scripts/render_manim.py" <project>       # first run installs Manim, about a minute
```

```python
from manim import *
from film import FilmScene, INK, MUTED, ACCENT, WARN, BAD, FONT, MONO

class Film(FilmScene):
    def construct(self):
        pos = [LEFT * 5, UP * 1.2, RIGHT * 5]
        nodes = VGroup(*[Circle(radius=1, color=INK).move_to(p) for p in pos])
        self.play(Create(nodes), run_time=1)
        self.cue(0, "B's timer")          # waits for those words in line 0
        timer = Arc(radius=1.2, start_angle=PI / 2, angle=-TAU, color=WARN).move_to(pos[1])
        self.play(Create(timer), run_time=1.2, rate_func=linear)
        self.cue(1)                       # waits for line 1
        self.play(nodes[1].animate.set_stroke(ACCENT, 8), FadeOut(timer), run_time=0.5)
        self.finish()                     # holds to the scene's last frame
```

- Every line changes the picture, on the word that names the change, with no more than 9 words between changes. The
  film fails a hold over 4.5 seconds, as a spec film does.
- The frame is 1800 by 840 pixels, about 17 by 8 Manim units, on a transparent background over the film's ground. Use
  the film's colors and fonts as imported above, and `font_size` 36 or more.
- Change a label with `FadeTransform(old, new)`, never `Transform` or `ReplacementTransform` on text: both test films caught a label
  mid-morph as broken letters, "C·ndid·te" and "le·der?".
- `cue` stops the render by name when the animation before it runs past its words: shorten that animation.
- `render_manim.py` prints `rendered <id>: N frames` for each scene. Run `node preview.mjs` again, then go on to step 6.

## 4. Length and report

Up to 300 seconds: one idea, taught, with the complications that make it hard. Cut a complication before you shorten
every line. The report lists `sources` with their cites.
