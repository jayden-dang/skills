"""What a Manim scene in this film builds on. render_manim.py puts this folder on the path and renders
manim/<id>.py, whose class Film(FilmScene) draws the scene with that id.

    class Film(FilmScene):
        def construct(self):
            a = Circle(color=INK)
            self.play(Create(a))
            self.cue(0, "times out")   # wait for the words "times out" in line 0
            self.play(a.animate.set_color(ACCENT))
            self.cue(1)                # wait for line 1
            ...
            self.finish()              # hold to the scene's last frame

cue() stops the render by name when the animation before it runs past the words, so shorten it.
"""
import json
import os
import re

from manim import Scene

FPS = 30
HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)


def _tokens():
    text = open(os.path.join(PROJECT, "src", "tokens.ts")).read()
    return dict(re.findall(r"^\s*(\w+):\s*'([^']*)'", text, re.M))


_t = _tokens()
INK, MUTED, ACCENT, WARN, BAD = (_t[k] for k in ("ink", "muted", "accent", "warn", "bad"))
FONT = os.environ.get("FILM_FONT", "Space Grotesk Light")
MONO = os.environ.get("FILM_MONO", "Roboto Mono")


class FilmScene(Scene):
    def setup(self):
        self.film_id = os.environ["FILM_SCENE"]
        self.timing = json.load(open(os.path.join(PROJECT, "out", "timing.json")))[self.film_id]

    def moment(self, line, phrase=None):
        """Seconds from the scene's start to line `line`, or to the word `phrase` starts on in it."""
        start = self.timing["starts"][line]
        if phrase is None:
            return start / FPS
        norm = lambda t: [re.sub(r"^\W+|\W+$", "", w).lower() for w in t.split()]
        text = self.film_lines[line]
        words, wanted = norm(text), norm(phrase)
        for i in range(len(words) - len(wanted) + 1):
            if wanted and words[i : i + len(wanted)] == wanted:
                return (start + self.timing["words"][line][i]) / FPS
        raise ValueError(f'{self.film_id}-{line}: "{phrase}" is not in the line "{text}"')

    @property
    def film_lines(self):
        script = json.load(open(os.path.join(PROJECT, "src", "script.json")))
        scene = next(s for s in script["scenes"] if s["id"] == self.film_id)
        return [b["text"] for b in scene["beats"]]

    def cue(self, line, phrase=None):
        """Wait until line `line` (or the word `phrase` in it) is spoken."""
        target = self.moment(line, phrase)
        late = self.time - target
        if late > 1 / FPS:
            where = f'"{phrase}" in line {line}' if phrase else f"line {line}"
            raise ValueError(f"{self.film_id}: {where} is spoken at {target:.2f}s, but the animation before it runs to {self.time:.2f}s. Shorten that animation by {late:.2f}s.")
        if target - self.time >= 1 / FPS:
            self.wait(target - self.time)

    def finish(self):
        """Hold the last picture to the scene's end, so the clip is exactly as long as the scene."""
        end = self.timing["duration"] / FPS
        if self.time - end > 1 / FPS:
            raise ValueError(f"{self.film_id}: the animation runs to {self.time:.2f}s; the scene ends at {end:.2f}s.")
        if end - self.time >= 1 / FPS:
            self.wait(end - self.time)
