#!/usr/bin/env python3
"""Check a finished video and its script. Usage: check_video.py <project> <repo-root> <mp4> [--sheet <png>]

With --script in place of <mp4>, judge the script alone: run that before paying for a voice.
Exits 1 and prints one FAIL line per fault. Prints the numbers either way.
"""
import json
import os
import re
import subprocess
import sys

KINDS = ("feature", "pr", "release", "spec")
MAX_WORDS = 20
MAX_WORDS_BY_LANGUAGE = {"vi": 30}  # Vietnamese writes each syllable as a token
MAX_STILL = 6.0
MAX_SILENCE = 3.0
MIN_CLIP_WIDTH = 1600
SPEC_MAX = 120
WORLD_W = 1780
WORLD_H = 740
# Lines that say why. Walkthrough films measured 0 to 9% of their lines; explanations 42 to 64%.
REASON_WORDS = {
    "en": r"\b(so|because|but|if|since|otherwise)\b",
    "vi": r"(^|\s)(nên|vì|nhưng|nếu|vậy|muốn)(\s|$)",
}


def validate_script(s):
    faults = []
    if not s.get("language"):
        faults.append("language is missing")
    source = s.get("source") or {}
    if source.get("kind") not in KINDS:
        faults.append("source.kind must be feature, pr, release or spec")
    if source.get("kind") == "spec" and not source.get("spec"):
        faults.append("source.spec is missing")
    if not source.get("ref"):
        faults.append("source.ref is missing")
    for scene in s.get("scenes", []):
        sid = scene.get("id", "?")
        beats = scene.get("beats", [])
        if scene.get("kind") == "clip" and not any(b.get("clip") for b in beats) and not scene.get("clip"):
            faults.append(f"{sid}: clip scene names no clip")
        for i, beat in enumerate(beats):
            if not (beat.get("ref") or "").strip():
                faults.append(f"{sid}-{i}: no source")
            limit = MAX_WORDS_BY_LANGUAGE.get(s.get("language"), MAX_WORDS)
            if len((beat.get("text") or "").split()) > limit:
                faults.append(f"{sid}-{i}: over {limit} words")
    return faults


def live_ids(requirements):
    """The IDs requirements.md defines. A struck-through ID is retired and does not count."""
    return set(re.findall(r"(?<!~~)\*\*([A-Z][A-Z0-9]*-\d+\.\d+)\*\*", requirements))


def cited_ids(s):
    return {i for scene in s.get("scenes", []) for beat in scene.get("beats", []) for i in re.findall(r"[A-Z][A-Z0-9]*-\d+\.\d+", beat.get("ref", ""))}


def judge_spec(s, requirements):
    faults = []
    scenes = s.get("scenes", [])
    if not s.get("planned"):
        faults.append("planned label is missing")
    for i in sorted(cited_ids(s) - live_ids(requirements)):
        faults.append(f"{i} is not in requirements.md")
    kinds = [scene.get("kind") for scene in scenes]
    for scene in scenes:
        if scene.get("kind") == "clip":
            faults.append(f"{scene.get('id')}: a spec film shows no footage")
    if kinds.count("points") > 1:
        faults.append(f"{kinds.count('points')} points scenes: a spec film has at most 1")
    if "world" not in kinds:
        faults.append("no world scene")
    words = REASON_WORDS.get(s.get("language"))
    if words:
        lines = [beat.get("text", "") for scene in scenes for beat in scene.get("beats", [])]
        reasons = sum(1 for line in lines if re.search(words, line, re.I))
        if lines and reasons * 3 < len(lines):
            faults.append(f"{reasons} of {len(lines)} lines give a reason; an explanation needs a third")
    return faults


def uncited(s, requirements):
    """What the film leaves out, in the spec's order: the page lists it."""
    key = lambda i: [int(n) for n in re.findall(r"\d+", i)]
    return sorted(live_ids(requirements) - cited_ids(s), key=key)


def judge_length(duration):
    return [f"{duration:.1f}s is over the {SPEC_MAX}s limit"] if duration > SPEC_MAX else []


def judge_quotes(s, read):
    """A rule or a code block on screen is the source's own words. read(path) gives a file at the pinned commit, or None."""
    faults = []
    folder = (s.get("source") or {}).get("spec", "")
    requirements = read(f"{folder}/requirements.md") or ""
    for scene in s.get("scenes", []):
        sid = scene.get("id")
        for rule in scene.get("rules", []):
            line = next((l for l in requirements.splitlines() if f"**{rule.get('id')}**" in l), "")
            if not rule.get("text") or rule["text"] not in line:
                faults.append(f"{sid}: {rule.get('id')} is not in the spec's words")
        if scene.get("kind") == "code":
            text = read(scene.get("file", ""))
            if text is None:
                faults.append(f"{sid}: {scene.get('file')} is not at the pinned commit")
                continue
            held = text.splitlines()
            for i, line in enumerate(scene.get("lines", [])):
                if line.strip() and line not in held:
                    faults.append(f"{sid}: line {i + 1} is not in {scene.get('file')}")
    return faults


def judge_world(s):
    """Nothing on screen is cut by the frame. A thing the frame sits wholly inside is its background."""
    faults = []
    for scene in s.get("scenes", []):
        if scene.get("kind") != "world":
            continue
        objects = {o["id"]: {"hidden": True, **o} for o in scene.get("objects", [])}
        camera = {"x": 0, "y": 0, "w": WORLD_W, "h": WORLD_H}
        told = set()
        for i, beat in enumerate(scene.get("beats", [])):
            change = beat.get("world") or {}
            for step in (change, change.get("then") or {}):
                for oid, values in (step.get("set") or {}).items():
                    if oid in objects:
                        objects[oid] = {**objects[oid], "hidden": False, **values}
                camera = step.get("camera") or camera
                # The template fits the box to the frame, so the frame may show more than the box.
                zoom = min(WORLD_W / camera["w"], WORLD_H / camera["h"])
                left = camera["x"] + camera["w"] / 2 - WORLD_W / zoom / 2
                top = camera["y"] + camera["h"] / 2 - WORLD_H / zoom / 2
                right, bottom = left + WORLD_W / zoom, top + WORLD_H / zoom
                view = (left, top, right, bottom)
                for oid, o in objects.items():
                    if o.get("hidden"):
                        continue
                    x, y, r, b = o["x"], o["y"], o["x"] + o["w"], o["y"] + o["h"]
                    apart = r <= left or x >= right or b <= top or y >= bottom
                    inside = x >= left - 1 and y >= top - 1 and r <= right + 1 and b <= bottom + 1
                    behind = x <= left and y <= top and r >= right and b >= bottom
                    if not (apart or inside or behind) and (oid, view) not in told:
                        told.add((oid, view))
                        faults.append(f"{scene.get('id')}-{i}: {oid} is cut by the camera")
    return faults


def judge_clip(width, height):
    if width < MIN_CLIP_WIDTH or width * 9 != height * 16:
        return f"clip is {width}x{height}; it needs 16:9 at {MIN_CLIP_WIDTH} wide or more"
    return None


def judge_media(m):
    faults = []
    if (m["width"], m["height"]) != (1920, 1080):
        faults.append(f"video is {m['width']}x{m['height']}, not 1920x1080")
    if not m["has_audio"]:
        faults.append("no audio stream")
    if m["peak"] is not None and m["peak"] > -1.0:
        faults.append(f"peak {m['peak']} dBFS is above -1")
    for start, length in m["freezes"]:
        if start + length < m["duration"] - 0.5 and length > MAX_STILL:
            faults.append(f"still for {length:.1f}s at {start:.1f}s")
    for start, length in m["silences"]:
        if start + length < m["duration"] - 0.5 and length > MAX_SILENCE:
            faults.append(f"silent for {length:.1f}s at {start:.1f}s")
    return faults


def file_refs(ref):
    return [(p, int(n)) for p, n in re.findall(r"([\w./-]+\.[A-Za-z0-9]+):(\d+)", ref)]


def run(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def probe(mp4):
    streams = json.loads(run("ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", mp4).stdout)
    video = next(s for s in streams["streams"] if s["codec_type"] == "video")
    has_audio = any(s["codec_type"] == "audio" for s in streams["streams"])
    duration = float(streams["format"]["duration"])
    loud = run("ffmpeg", "-hide_banner", "-i", mp4, "-af", "ebur128=peak=true", "-vn", "-f", "null", "-").stderr
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", loud)
    peak = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", loud)
    freeze = run("ffmpeg", "-hide_banner", "-i", mp4, "-vf", "freezedetect=n=0.001:d=4", "-an", "-f", "null", "-").stderr
    silence = run("ffmpeg", "-hide_banner", "-i", mp4, "-af", "silencedetect=noise=-40dB:d=1.5", "-vn", "-f", "null", "-").stderr
    return {
        "width": video["width"],
        "height": video["height"],
        "has_audio": has_audio,
        "duration": duration,
        "loudness": float(i[-1]) if i else None,
        "peak": float(peak[-1]) if peak else None,
        "freezes": spans(freeze, "freeze_start", "freeze_end", duration),
        "silences": spans(silence, "silence_start", "silence_end", duration),
    }


def spans(log, start_key, end_key, duration):
    starts = [float(x) for x in re.findall(rf"{start_key}: ([\d.]+)", log)]
    ends = [float(x) for x in re.findall(rf"{end_key}: ([\d.]+)", log)]
    return [(s, (ends[i] if i < len(ends) else duration) - s) for i, s in enumerate(starts)]


def check_refs(s, repo):
    faults = []
    ref = (s.get("source") or {}).get("ref", "HEAD")
    for scene in s.get("scenes", []):
        for i, beat in enumerate(scene.get("beats", [])):
            for path, line in file_refs(beat.get("ref", "")):
                shown = run("git", "-C", repo, "show", f"{ref}:{path}")
                if shown.returncode != 0:
                    faults.append(f"{scene.get('id')}-{i}: {path} is not in {ref}")
                elif line > len(shown.stdout.splitlines()):
                    faults.append(f"{scene.get('id')}-{i}: {path}:{line} is past the end of the file at {ref}")
    return faults


def sheet_filter(frames, duration):
    if frames:
        picks = "+".join(rf"eq(n\,{f})" for f in frames)
        rows = (len(frames) + 3) // 4
        return f"select='{picks}',scale=480:-1,tile=4x{rows}"
    return f"fps=1/{max(1.5, duration / 16)},scale=480:-1,tile=4x4"


def beat_frames(project):
    """The frames preview.mjs chose: the last moment of each line. Empty when it has not run."""
    path = os.path.join(project, "out", "beats.json")
    return json.load(open(path)) if os.path.exists(path) else None


def contact_sheet(mp4, out, frames, duration):
    run("ffmpeg", "-v", "error", "-y", "-i", mp4, "-vf", sheet_filter(frames, duration), "-frames:v", "1", out)


def spec_text(s, repo):
    source = s.get("source") or {}
    if source.get("kind") != "spec" or not source.get("spec"):
        return None
    shown = run("git", "-C", repo, "show", f"{source.get('ref')}:{source['spec']}/requirements.md")
    return shown.stdout if shown.returncode == 0 else None


def script_faults(s, repo):
    """Everything that can be judged before a voice or a render exists."""
    faults = validate_script(s) + check_refs(s, repo) + judge_world(s)
    source = s.get("source") or {}
    if source.get("kind") == "spec" and source.get("spec"):
        text = spec_text(s, repo)
        if text is None:
            faults.append(f"{source['spec']}/requirements.md is not in {source.get('ref')}")
        else:
            def read(path):
                held = run("git", "-C", repo, "show", f"{source.get('ref')}:{path}")
                return held.stdout if held.returncode == 0 else None

            faults += judge_spec(s, text) + judge_quotes(s, read)
    return faults


def main(argv):
    project, repo = argv[1:3]
    only_script = "--script" in argv
    mp4 = None if only_script else argv[3]
    sheet = argv[argv.index("--sheet") + 1] if "--sheet" in argv else None
    s = json.load(open(os.path.join(project, "src", "script.json")))
    faults = script_faults(s, repo)
    text = spec_text(s, repo)
    if not only_script:
        m = probe(mp4)
        print(json.dumps({k: m[k] for k in ("width", "height", "duration", "loudness", "peak", "freezes", "silences")}))
        faults += judge_media(m)
        if text is not None:
            faults += judge_length(m["duration"])
        if sheet:
            contact_sheet(mp4, sheet, beat_frames(project), m["duration"])
            print(f"sheet: {sheet}")
    if text is not None:
        left_out = uncited(s, text)
        print(f"not in the film: {len(left_out)} of {len(live_ids(text))} IDs, in out/uncited.json")
        os.makedirs(os.path.join(project, "out"), exist_ok=True)
        json.dump(left_out, open(os.path.join(project, "out", "uncited.json"), "w"))
    for f in faults:
        print(f"FAIL {f}")
    print("PASS" if not faults else f"{len(faults)} fault(s)")
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
