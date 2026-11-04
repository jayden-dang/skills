#!/usr/bin/env python3
"""Speak every line of src/script.json with ElevenLabs, level it, and record its length.

A line already spoken with the same words, language and voice is reused, so a rerun pays only
for what changed.

Usage: voice.py <project> [--voice ID]
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request

ELEVEN_VOICE = "EXAVITQu4vr4xnSDxMaL"
# eleven_multilingual_v2 does not list Vietnamese; the flash model carries every language this set has used.
ELEVEN_MODEL = "eleven_flash_v2_5"
TARGET_LUFS = -16.0


def arg(argv, name, default):
    return argv[argv.index(name) + 1] if name in argv else default


def api_key():
    key = os.environ.get("ELEVENLABS_API_KEY") or os.environ.get("ELEVENLABS")
    if not key:
        raise SystemExit("FAIL no ELEVENLABS_API_KEY in the environment")
    return key


def vendor_reason(error):
    """The vendor's own sentence: a 401 means a bad key or an unpaid invoice, and only this tells them apart."""
    try:
        detail = json.loads(error.read()).get("detail")
    except ValueError:
        return "no reason given"
    return (detail.get("message") if isinstance(detail, dict) else detail) or "no reason given"


def eleven(key, text, language, voice, out):
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
        raise SystemExit(f"FAIL ElevenLabs answered {e.code}: {vendor_reason(e)}.{hint}")
    with open(out, "wb") as f:
        f.write(data)


def loudness(path):
    log = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", log)[-1])


def recording(cache, key, text, language, voice):
    """The levelled mp3 for these words, spoken now only if it is not already on disk."""
    name = hashlib.sha256("\0".join((text, language, voice, ELEVEN_MODEL)).encode()).hexdigest()[:24]
    done = os.path.join(cache, f"{name}.mp3")
    if os.path.exists(done):
        return done, False
    raw = os.path.join(cache, f"{name}.raw.mp3")
    eleven(key, text, language, voice, raw)
    gain = TARGET_LUFS - loudness(raw)
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", f"volume={gain:.2f}dB,alimiter=limit=0.84:level=false", "-ar", "44100", "-b:a", "160k", done])
    os.remove(raw)
    return done, True


def main(argv):
    if "--engine" in argv:
        raise SystemExit("FAIL --engine is gone: every line is spoken by ElevenLabs")
    project = argv[1]
    key = api_key()
    script = json.load(open(os.path.join(project, "src", "script.json")))
    language = script.get("language", "en")
    voice = arg(argv, "--voice", ELEVEN_VOICE)
    folder = os.path.join(project, "public", "voice")
    cache = os.path.join(project, ".voice-cache")
    os.makedirs(folder, exist_ok=True)
    os.makedirs(cache, exist_ok=True)
    frames = {}
    paid = 0
    for scene in script["scenes"]:
        frames[scene["id"]] = []
        for i, beat in enumerate(scene["beats"]):
            text = beat.get("spoken") or beat["text"]
            source, fresh = recording(cache, key, text, language, voice)
            paid += len(text) if fresh else 0
            out = os.path.join(folder, f"{scene['id']}-{i}.mp3")
            shutil.copyfile(source, out)
            seconds = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out]))
            frames[scene["id"]].append(int(seconds * 30) + 1)
            print(f"{scene['id']}-{i} {seconds:.1f}s")
    json.dump(frames, open(os.path.join(project, "src", "voice.json"), "w"), indent=1)
    total = sum(sum(v) for v in frames.values()) / 30
    print(f"spoke {sum(len(v) for v in frames.values())} lines with elevenlabs/{voice}: {total:.1f}s of speech, {paid} characters billed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
