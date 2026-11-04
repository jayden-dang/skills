#!/usr/bin/env python3
"""Run with: python3 -m unittest discover -s skills/craft/make-video/scripts"""
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(__file__))
import voice  # noqa: E402


def tone():
    """A real mp3, because voice.py levels what it receives with ffmpeg."""
    with tempfile.TemporaryDirectory() as d:
        out = os.path.join(d, "t.mp3")
        subprocess.check_call(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "sine=frequency=330:duration=0.5", out])
        return open(out, "rb").read()


TONE = tone()
AUDIO = "https://api.vibi.pro/audio/job.mp3"


class Speak(unittest.TestCase):
    """The HTTP calls are the system boundary, so they are the only thing replaced."""

    def setUp(self):
        self.project = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.project, "src"))
        self.posts = []
        self.requests = []
        self.polls = [{"status": "completed", "result": {"audio_url": AUDIO}}]
        self.real_open = urllib.request.urlopen
        urllib.request.urlopen = self.answer
        self.addCleanup(setattr, urllib.request, "urlopen", self.real_open)
        self.saved = {k: os.environ.pop(k, None) for k in ("VIBI_API", "ELEVENLABS_API_KEY", "ELEVENLABS")}
        os.environ["VIBI_API"] = "test-key"
        self.addCleanup(self.restore)
        self.addCleanup(setattr, voice, "POLL_SECONDS", voice.POLL_SECONDS)
        voice.POLL_SECONDS = 0
        quiet = contextlib.redirect_stdout(io.StringIO())
        quiet.__enter__()
        self.addCleanup(quiet.__exit__, None, None, None)

    def restore(self):
        os.environ.pop("VIBI_API", None)
        for k, v in self.saved.items():
            if v:
                os.environ[k] = v

    def answer(self, req, timeout=None):
        self.requests.append(req)
        if req.get_method() == "POST":
            self.posts.append((req.full_url, json.loads(req.data)))
            return io.BytesIO(json.dumps({"id": "job", "status": "pending"}).encode())
        if "/history/" in req.full_url:
            step = self.polls.pop(0) if len(self.polls) > 1 else self.polls[0]
            return io.BytesIO(json.dumps(step).encode())
        return io.BytesIO(TONE)

    def write(self, beats, language="en"):
        script = {"language": language, "scenes": [{"id": "a", "kind": "title", "title": "T", "beats": beats}]}
        json.dump(script, open(os.path.join(self.project, "src", "script.json"), "w"))

    def line(self, text="Hello.", **more):
        return {"text": text, "ref": "x", **more}

    def test_vietnamese_is_the_chosen_minimax_narrator(self):
        self.write([self.line("Xin chào.")], language="vi")
        self.assertEqual(voice.main(["voice.py", self.project]), 0)
        url, body = self.posts[0]
        self.assertTrue(url.endswith("/v1/text-to-speech/362703657091265"))
        self.assertEqual(body["provider"], "minimax")
        self.assertEqual(body["model_id"], "speech-2.8-hd")
        self.assertEqual(body["language_code"], "Vietnamese")
        self.assertEqual(body["text"], "Xin chào.")

    def test_english_is_the_chosen_minimax_speaker(self):
        self.write([self.line()])
        voice.main(["voice.py", self.project])
        url, body = self.posts[0]
        self.assertTrue(url.startswith("https://api.vibi.pro/v1/text-to-speech/273587280617674"))
        self.assertEqual(body["provider"], "minimax")
        self.assertEqual(body["model_id"], "speech-2.8-hd")
        self.assertEqual(body["language_code"], "English")

    def test_another_language_goes_to_elevenlabs_with_its_code(self):
        self.write([self.line("Hallo.")], language="de")
        voice.main(["voice.py", self.project])
        self.assertEqual(self.posts[0][1]["language_code"], "de")
        self.assertEqual(self.posts[0][1]["model_id"], "eleven_flash_v2_5")

    def test_the_voice_flag_replaces_the_voice_and_keeps_the_provider(self):
        self.write([self.line("Xin chào.")], language="vi")
        voice.main(["voice.py", self.project, "--voice", "123"])
        self.assertTrue(self.posts[0][0].endswith("/text-to-speech/123"))
        self.assertEqual(self.posts[0][1]["provider"], "minimax")

    def test_it_waits_for_the_job_and_saves_the_audio(self):
        self.polls = [{"status": "pending"}, {"status": "processing"}, {"status": "completed", "result": {"audio_url": AUDIO}}]
        self.write([self.line()])
        voice.main(["voice.py", self.project])
        self.assertTrue(os.path.exists(os.path.join(self.project, "public", "voice", "a-0.mp3")))
        self.assertEqual(sum("/history/job" in r.full_url for r in self.requests), 3)

    def test_a_failed_job_says_why_and_leaves_no_file(self):
        self.polls = [{"status": "failed", "error": "Voice not available"}]
        self.write([self.line()])
        with self.assertRaises(SystemExit) as stop:
            voice.main(["voice.py", self.project])
        self.assertIn("Voice not available", str(stop.exception))
        self.assertFalse(os.path.exists(os.path.join(self.project, "public", "voice", "a-0.mp3")))

    def test_a_job_that_never_ends_stops_with_its_id(self):
        self.polls = [{"status": "processing"}]
        self.write([self.line()])
        original, voice.POLL_LIMIT = voice.POLL_LIMIT, 3
        self.addCleanup(setattr, voice, "POLL_LIMIT", original)
        with self.assertRaises(SystemExit) as stop:
            voice.main(["voice.py", self.project])
        self.assertIn("job", str(stop.exception))

    def test_no_key_stops_before_any_call(self):
        del os.environ["VIBI_API"]
        self.write([self.line()])
        with self.assertRaises(SystemExit) as stop:
            voice.main(["voice.py", self.project])
        self.assertIn("VIBI_API", str(stop.exception))
        self.assertEqual(self.requests, [])

    def test_the_old_elevenlabs_key_is_not_used(self):
        del os.environ["VIBI_API"]
        os.environ["ELEVENLABS_API_KEY"] = "old"
        self.addCleanup(os.environ.pop, "ELEVENLABS_API_KEY", None)
        self.write([self.line()])
        with self.assertRaises(SystemExit):
            voice.main(["voice.py", self.project])
        self.assertEqual(self.requests, [])

    def test_the_old_engine_flag_is_gone(self):
        self.write([self.line()])
        with self.assertRaises(SystemExit) as stop:
            voice.main(["voice.py", self.project, "--engine", "say"])
        self.assertIn("--engine", str(stop.exception))
        self.assertEqual(self.requests, [])

    def test_a_refusal_says_why_in_the_vendors_words(self):
        def refuse(req, timeout=None):
            raise urllib.error.HTTPError(req.full_url, 401, "no", {}, io.BytesIO(b'{"error":"missing or invalid authentication credentials"}'))

        urllib.request.urlopen = refuse
        self.write([self.line()])
        with self.assertRaises(SystemExit) as stop:
            voice.main(["voice.py", self.project])
        self.assertIn("401", str(stop.exception))
        self.assertIn("missing or invalid", str(stop.exception))
        self.assertFalse(os.path.exists(os.path.join(self.project, "public", "voice", "a-0.mp3")))

    def test_the_key_goes_only_to_the_vendor(self):
        self.polls = [{"status": "completed", "result": {"audio_url": "https://cdn.example.com/a.mp3"}}]
        self.write([self.line()])
        voice.main(["voice.py", self.project])
        download = next(r for r in self.requests if "cdn.example.com" in r.full_url)
        self.assertIsNone(download.get_header("Xi-api-key"))
        self.assertEqual(self.requests[0].get_header("Xi-api-key"), "test-key")

    def test_spoken_replaces_what_is_said_and_text_stays_on_screen(self):
        self.write([self.line("POST /api/offers answers 409.", spoken="The offers route answers four oh nine.")])
        voice.main(["voice.py", self.project])
        self.assertEqual(self.posts[0][1]["text"], "The offers route answers four oh nine.")

    def test_a_second_run_pays_only_for_the_line_that_changed(self):
        self.write([self.line("One."), self.line("Two.")])
        voice.main(["voice.py", self.project])
        self.assertEqual(len(self.posts), 2)
        self.posts.clear()
        self.write([self.line("One."), self.line("Three.")])
        voice.main(["voice.py", self.project])
        self.assertEqual([b["text"] for _, b in self.posts], ["Three."])
        lengths = json.load(open(os.path.join(self.project, "src", "voice.json")))
        self.assertEqual(len(lengths["a"]), 2)

    def test_a_new_language_is_not_served_from_the_old_recording(self):
        self.write([self.line("One.")])
        voice.main(["voice.py", self.project])
        self.posts.clear()
        self.write([self.line("One.")], language="vi")
        voice.main(["voice.py", self.project])
        self.assertEqual(len(self.posts), 1)


class WordTimes(unittest.TestCase):
    def test_words_share_the_speech_by_length(self):
        self.assertEqual(voice.word_starts("aaa bbb", [(0.0, 2.0)]), [0.0, 1.0])

    def test_a_pause_is_skipped_not_shared(self):
        # Two words spoken either side of a one-second pause.
        self.assertEqual(voice.word_starts("aaa bbb", [(0.0, 1.0), (2.0, 3.0)]), [0.0, 2.0])

    def test_a_longer_word_takes_longer(self):
        starts = voice.word_starts("a bbbbbbb c", [(0.0, 3.0)])
        self.assertLess(starts[1], 1.0)
        self.assertGreater(starts[2], 2.0)

    def test_speech_spans_come_from_the_gaps(self):
        log = "silence_start: 0\nsilence_end: 0.3 | silence_duration: 0.3\nsilence_start: 1.2\nsilence_end: 1.6 | silence_duration: 0.4\nsilence_start: 2.5\n"
        self.assertEqual(voice.spans_from(log, 2.7), [(0.3, 1.2), (1.6, 2.5)])

    def test_no_gap_is_one_span(self):
        self.assertEqual(voice.spans_from("", 2.0), [(0.0, 2.0)])


if __name__ == "__main__":
    unittest.main()
