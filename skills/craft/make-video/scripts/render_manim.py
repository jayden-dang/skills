#!/usr/bin/env python3
"""Render every `manim` scene of src/script.json to public/manim/<id>.webm. Usage: render_manim.py <project>

Each scene is manim/<id>.py with `class Film(FilmScene)`. It times itself to out/timing.json, which
`node preview.mjs` writes, so run that after voice.py and before this. The first run installs Manim
Community Edition into ~/.cache/make-video/manim.
"""
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

VENV = os.path.expanduser("~/.cache/make-video/manim")
W, H, FPS = 1800, 840, 30


def python311():
    for name in ("python3.13", "python3.12", "python3.11", "python3"):
        path = shutil.which(name)
        if path and subprocess.run([path, "-c", "import sys; sys.exit(sys.version_info < (3, 11))"]).returncode == 0:
            return path
    return None


def venv():
    py = os.path.join(VENV, "bin", "python")
    if os.path.exists(os.path.join(VENV, "bin", "manim")):
        return py
    base = python311()
    if not base:
        raise SystemExit("FAIL Manim needs Python 3.11 or later, and none is on PATH. Draw this scene as a world instead.")
    subprocess.check_call([base, "-m", "venv", VENV])
    subprocess.check_call([py, "-m", "pip", "install", "-q", "manim", "fonttools", "brotli"])
    return py


def fonts(py, project):
    """Pango cannot read woff2: the film's own fonts go to TTF once, beside the scenes."""
    out = os.path.join(project, "manim", "fonts")
    os.makedirs(out, exist_ok=True)
    code = (
        "import sys,os\nfrom fontTools.ttLib import TTFont\n"
        "for f in sys.argv[2:]:\n"
        "  t=TTFont(f); t.flavor=None; t.save(os.path.join(sys.argv[1], os.path.basename(f).rsplit('.',1)[0]+'.ttf'))\n"
    )
    files = glob.glob(os.path.join(project, "public", "fonts", "*.woff2"))
    if files:
        subprocess.check_call([py, "-c", code, out, *files])
    return out


def frames(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", path], text=True)
    return int(out.strip())


def main(argv):
    project = os.path.abspath(argv[1])
    script = json.load(open(os.path.join(project, "src", "script.json")))
    scenes = [s for s in script["scenes"] if s.get("kind") == "manim"]
    if not scenes:
        print("no manim scenes")
        return 0
    timing_path = os.path.join(project, "out", "timing.json")
    if not os.path.exists(timing_path):
        print("FAIL out/timing.json is missing: run `node preview.mjs` first")
        return 1
    timing = json.load(open(timing_path))
    py = venv()
    font_dir = fonts(py, project)
    os.makedirs(os.path.join(project, "public", "manim"), exist_ok=True)
    failed = 0
    for scene in scenes:
        sid = scene["id"]
        source = os.path.join(project, "manim", f"{sid}.py")
        if not os.path.exists(source):
            print(f"FAIL {sid}: manim/{sid}.py is missing")
            failed += 1
            continue
        if sid not in timing:
            print(f"FAIL {sid}: not in out/timing.json; run `node preview.mjs` again")
            failed += 1
            continue
        media = tempfile.mkdtemp()
        # Fonts are registered through a sitecustomize, so Text() finds them in any scene file.
        boot = os.path.join(media, "sitecustomize.py")
        open(boot, "w").write(f"import glob, manimpango\nfor f in glob.glob({font_dir!r} + '/*.ttf'): manimpango.register_font(f)\n")
        env = {**os.environ, "FILM_SCENE": sid, "PYTHONPATH": os.pathsep.join([media, os.path.join(project, "manim")])}
        cmd = [os.path.join(VENV, "bin", "manim"), "render", source, "Film", "--fps", str(FPS), "-r", f"{W},{H}", "-t", "--format", "webm", "--disable_caching", "--media_dir", media, "-o", sid]
        done = subprocess.run(cmd, env=env, capture_output=True, text=True)
        found = glob.glob(os.path.join(media, "videos", "**", f"{sid}.webm"), recursive=True)
        if done.returncode != 0 or not found:
            tail = [l for l in (done.stderr or done.stdout).splitlines() if l.strip()][-6:]
            print(f"FAIL {sid}: manim stopped\n  " + "\n  ".join(tail))
            failed += 1
            continue
        target = os.path.join(project, "public", "manim", f"{sid}.webm")
        shutil.copy(found[0], target)
        got, want = frames(target), timing[sid]["duration"]
        if abs(got - want) > 1:
            print(f"FAIL {sid}: {got} frames, the scene is {want}. End construct() with self.finish().")
            failed += 1
            continue
        print(f"rendered {sid}: {got} frames")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
