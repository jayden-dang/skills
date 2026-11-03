#!/usr/bin/env python3
"""Speak every line of src/script.json, level it, and record its length.

Usage: voice.py <project> [--engine say|elevenlabs] [--voice NAME]
"""
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

SAY_VOICE = {"en": "Samantha", "vi": "Linh"}
ELEVEN_VOICE = "EXAVITQu4vr4xnSDxMaL"
# eleven_multilingual_v2 does not list Vietnamese; the flash model carries every language this set has used.
ELEVEN_MODEL = "eleven_flash_v2_5"
TARGET_LUFS = -16.0


def arg(argv, name, default):
    return argv[argv.index(name) + 1] if name in argv else default


def eleven(text, language, voice, out):
    key = os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("ELEVENLABS")
    if not key:
        raise SystemExit("FAIL no ELEVENLABS_API_KEY in the environment")
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format=mp3_44100_128",
        method="POST",
        headers={"xi-api-key": key, "Content-Type": "application/json"},
        data=json.dumps({"text": text, "model_id": ELEVEN_MODEL, "language_code": language}).encode(),
    )
    try:
        data = urllib.request.urlopen(req).read()
    except urllib.error.HTTPError as e:
        hint = " A free plan cannot use library voices over the API; use a premade voice." if e.code == 402 else ""
        raise SystemExit(f"FAIL ElevenLabs answered {e.code}.{hint}")
    with open(out, "wb") as f:
        f.write(data)


def say(text, voice, out):
    subprocess.check_call(["say", "-v", voice, "-o", out, text])


def loudness(path):
    log = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", log)[-1])


def main(argv):
    project = argv[1]
    engine = arg(argv, "--engine", "say")
    script = json.load(open(os.path.join(project, "src", "script.json")))
    language = script.get("language", "en")
    voice = arg(argv, "--voice", ELEVEN_VOICE if engine == "elevenlabs" else SAY_VOICE.get(language))
    if not voice:
        raise SystemExit(f"FAIL no default say voice for {language}; pass --voice")
    folder = os.path.join(project, "public", "voice")
    os.makedirs(folder, exist_ok=True)
    frames = {}
    for scene in script["scenes"]:
        frames[scene["id"]] = []
        for i, beat in enumerate(scene["beats"]):
            raw = os.path.join(folder, f"{scene['id']}-{i}.raw" + (".mp3" if engine == "elevenlabs" else ".aiff"))
            out = os.path.join(folder, f"{scene['id']}-{i}.mp3")
            if engine == "elevenlabs":
                eleven(beat["text"], language, voice, raw)
            else:
                say(beat["text"], voice, raw)
            gain = TARGET_LUFS - loudness(raw)
            subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", f"volume={gain:.2f}dB,alimiter=limit=0.84:level=false", "-ar", "44100", "-b:a", "160k", out])
            os.remove(raw)
            seconds = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out]))
            frames[scene["id"]].append(int(seconds * 30) + 1)
            print(f"{scene['id']}-{i} {seconds:.1f}s")
    json.dump(frames, open(os.path.join(project, "src", "voice.json"), "w"), indent=1)
    total = sum(sum(v) for v in frames.values()) / 30
    print(f"spoke {sum(len(v) for v in frames.values())} lines with {engine}/{voice}: {total:.1f}s of speech")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
