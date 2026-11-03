#!/usr/bin/env python3
"""Check a finished video and its script. Usage: check_video.py <project> <repo-root> <mp4> [--sheet <png>]

Exits 1 and prints one FAIL line per fault. Prints the numbers either way.
"""
import json
import os
import re
import subprocess
import sys

KINDS = ("feature", "pr", "release")
MAX_WORDS = 20
MAX_STILL = 6.0
MAX_SILENCE = 3.0
MIN_CLIP_WIDTH = 1600


def validate_script(s):
    faults = []
    if not s.get("language"):
        faults.append("language is missing")
    source = s.get("source") or {}
    if source.get("kind") not in KINDS:
        faults.append("source.kind must be feature, pr or release")
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
            if len((beat.get("text") or "").split()) > MAX_WORDS:
                faults.append(f"{sid}-{i}: over {MAX_WORDS} words")
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


def main(argv):
    project, repo, mp4 = argv[1:4]
    sheet = argv[argv.index("--sheet") + 1] if "--sheet" in argv else None
    s = json.load(open(os.path.join(project, "src", "script.json")))
    m = probe(mp4)
    print(json.dumps({k: m[k] for k in ("width", "height", "duration", "loudness", "peak", "freezes", "silences")}))
    faults = validate_script(s) + check_refs(s, repo) + judge_media(m)
    if sheet:
        contact_sheet(mp4, sheet, beat_frames(project), m["duration"])
        print(f"sheet: {sheet}")
    for f in faults:
        print(f"FAIL {f}")
    print("PASS" if not faults else f"{len(faults)} fault(s)")
    return 1 if faults else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
