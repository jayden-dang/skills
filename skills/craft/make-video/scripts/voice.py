#!/usr/bin/env python3
"""Speak every line of src/script.json through Vibi, level it, and record its length.

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
import time
import urllib.error
import urllib.request

API = "https://api.vibi.pro/v1"
# The owner chose these two voices from the trials in TESTS.md. Other languages go to ElevenLabs,
# whose flash model carries every language this set has used, at half the credits of v4.
SARAH = {"voice": "EXAVITQu4vr4xnSDxMaL", "model_id": "eleven_flash_v2_5"}
VOICES = {
    "en": {"voice": "273587280617674", "provider": "minimax", "model_id": "speech-2.8-hd", "language_code": "English"},
    "vi": {"voice": "362703657091265", "provider": "minimax", "model_id": "speech-2.8-hd", "language_code": "Vietnamese"},
}
TARGET_LUFS = -16.0
POLL_SECONDS = 2
POLL_LIMIT = 150  # Jobs took 5 to 20 seconds in the trial; this waits five minutes


def arg(argv, name, default):
    return argv[argv.index(name) + 1] if name in argv else default


def api_key():
    key = os.environ.get("VIBI_API")
    if not key:
        raise SystemExit("FAIL no VIBI_API in the environment")
    return key


def settings(language, voice):
    """What to ask for in this language: the fields of the request, and the voice for its path."""
    chosen = dict(VOICES.get(language) or {**SARAH, "language_code": language})
    path_voice = voice or chosen.pop("voice")
    chosen.pop("voice", None)
    return path_voice, chosen


def vendor_reason(error):
    """The vendor's own sentence: a 401 means a bad key or an unpaid invoice, and only this tells them apart."""
    try:
        body = json.loads(error.read())
    except ValueError:
        return "no reason given"
    detail = body.get("detail") if isinstance(body, dict) else None
    reason = detail.get("message") if isinstance(detail, dict) else detail
    return reason or (body.get("error") if isinstance(body, dict) else None) or "no reason given"


def call(key, path, body=None):
    req = urllib.request.Request(
        API + path,
        method="POST" if body is not None else "GET",
        headers={"xi-api-key": key, "Content-Type": "application/json", "User-Agent": "make-video"},
        data=json.dumps(body).encode() if body is not None else None,
    )
    try:
        return json.loads(urllib.request.urlopen(req, timeout=60).read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"FAIL Vibi answered {e.code}: {vendor_reason(e)}")


def speak(key, text, language, voice, out):
    path_voice, fields = settings(language, voice)
    job = call(key, f"/text-to-speech/{path_voice}", {"text": text, **fields})
    for _ in range(POLL_LIMIT):
        done = call(key, f"/history/{job['id']}")
        if done.get("status") == "failed":
            raise SystemExit(f"FAIL Vibi could not speak a line: {done.get('error') or 'no reason given'}")
        if done.get("status") == "completed":
            break
        time.sleep(POLL_SECONDS)
    else:
        raise SystemExit(f"FAIL Vibi job {job['id']} did not finish")
    url = done["result"]["audio_url"]
    # The key goes to Vibi alone, wherever the audio happens to be served from.
    headers = {"User-Agent": "make-video"}
    if url.startswith("https://api.vibi.pro/"):
        headers["xi-api-key"] = key
    data = urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=120).read()
    with open(out, "wb") as f:
        f.write(data)


def loudness(path):
    log = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", log)[-1])


def recording(cache, key, text, language, voice):
    """The levelled mp3 for these words, spoken now only if it is not already on disk."""
    path_voice, fields = settings(language, voice)
    name = hashlib.sha256("\0".join((text, language, path_voice, json.dumps(fields, sort_keys=True))).encode()).hexdigest()[:24]
    done = os.path.join(cache, f"{name}.mp3")
    if os.path.exists(done):
        return done, False
    raw = os.path.join(cache, f"{name}.raw.mp3")
    speak(key, text, language, voice, raw)
    gain = TARGET_LUFS - loudness(raw)
    subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-i", raw, "-af", f"volume={gain:.2f}dB,alimiter=limit=0.78:level=false", "-ar", "44100", "-b:a", "160k", done])
    os.remove(raw)
    return done, True


def spans_from(log, duration):
    """The stretches of speech between the pauses silencedetect logged."""
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    out = []
    at = 0.0
    for i, start in enumerate(starts):
        if start > at:
            out.append((at, start))
        at = ends[i] if i < len(ends) else duration
    if at < duration:
        out.append((at, duration))
    return out or [(0.0, duration)]


def word_starts(text, spans):
    """When each word starts: speech is shared among words by length, and a pause belongs to none of them."""
    words = text.split()
    weights = [len(w) + 1 for w in words]
    total = sum(weights)
    speech = sum(b - a for a, b in spans)
    out = []
    done = 0
    for weight in weights:
        left = speech * done / total
        for a, b in spans:
            if left < b - a:
                out.append(round(a + left, 3))
                break
            left -= b - a
        else:
            out.append(round(spans[-1][1], 3))
        done += weight
    return out


def speech_spans(path, duration):
    log = subprocess.run(["ffmpeg", "-hide_banner", "-i", path, "-af", "silencedetect=noise=-30dB:d=0.18", "-f", "null", "-"], capture_output=True, text=True).stderr
    return spans_from(log, duration)


def main(argv):
    if "--engine" in argv:
        raise SystemExit("FAIL --engine is gone: every line is spoken through Vibi")
    project = argv[1]
    key = api_key()
    script = json.load(open(os.path.join(project, "src", "script.json")))
    language = script.get("language", "en")
    voice = arg(argv, "--voice", None)
    folder = os.path.join(project, "public", "voice")
    cache = os.path.join(project, ".voice-cache")
    os.makedirs(folder, exist_ok=True)
    os.makedirs(cache, exist_ok=True)
    frames = {}
    words = {}
    paid = 0
    for scene in script["scenes"]:
        frames[scene["id"]] = []
        words[scene["id"]] = []
        for i, beat in enumerate(scene["beats"]):
            text = beat.get("spoken") or beat["text"]
            source, fresh = recording(cache, key, text, language, voice)
            paid += len(text) if fresh else 0
            out = os.path.join(folder, f"{scene['id']}-{i}.mp3")
            shutil.copyfile(source, out)
            seconds = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out]))
            frames[scene["id"]].append(int(seconds * 30) + 1)
            words[scene["id"]].append([int(at * 30) for at in word_starts(beat["text"], speech_spans(out, seconds))])
            print(f"{scene['id']}-{i} {seconds:.1f}s")
    json.dump(frames, open(os.path.join(project, "src", "voice.json"), "w"), indent=1)
    json.dump(words, open(os.path.join(project, "src", "words.json"), "w"))
    total = sum(sum(v) for v in frames.values()) / 30
    print(f"spoke {sum(len(v) for v in frames.values())} lines through Vibi: {total:.1f}s of speech, {paid} characters billed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
