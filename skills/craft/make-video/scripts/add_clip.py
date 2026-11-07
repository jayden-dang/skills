#!/usr/bin/env python3
"""Check a recording and add it to the film. Usage: add_clip.py <project> <name> <recording>"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_video import judge_clip  # noqa: E402


def main(argv):
    project, name, recording = argv[1:4]
    info = json.loads(subprocess.check_output(["ffprobe", "-v", "error", "-select_streams", "v", "-show_entries", "stream=width,height", "-show_entries", "format=duration", "-of", "json", recording]))
    width, height = info["streams"][0]["width"], info["streams"][0]["height"]
    fault = judge_clip(width, height)
    if fault:
        print(f"FAIL {fault}. Open the page first, set the viewport second, then record again.")
        return 1
    clips = os.path.join(project, "public", "clips")
    os.makedirs(clips, exist_ok=True)
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", recording, "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-an", os.path.join(clips, f"{name}.mp4")])
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-sseof", "-0.1", "-i", recording, "-frames:v", "1", "-update", "1", os.path.join(clips, f"{name}-last.png")])
    # The first frame stands in the window while the scene comes in, before the recording starts to play.
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", recording, "-frames:v", "1", "-update", "1", os.path.join(clips, f"{name}-first.png")])
    manifest = os.path.join(project, "src", "clips.json")
    data = json.load(open(manifest))
    data[name] = {"frames": round(float(info["format"]["duration"]) * 30), "width": width, "height": height}
    json.dump(data, open(manifest, "w"), indent=1)
    print(f"added {name}: {width}x{height}, {data[name]['frames']} frames")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
