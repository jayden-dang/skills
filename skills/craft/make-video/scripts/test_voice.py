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


class Speak(unittest.TestCase):
    """The HTTP call is the system boundary, so it is the only thing replaced."""

    def setUp(self):
        self.project = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.project, "src"))
        self.sent = []
        self.real_open = urllib.request.urlopen
        urllib.request.urlopen = self.answer
        self.addCleanup(setattr, urllib.request, "urlopen", self.real_open)
        self.key = os.environ.pop("ELEVENLABS_API_KEY", None)
        self.old = os.environ.pop("ELEVENLABS", None)
        os.environ["ELEVENLABS_API_KEY"] = "test"
        self.addCleanup(self.restore)
        quiet = contextlib.redirect_stdout(io.StringIO())
        quiet.__enter__()
        self.addCleanup(quiet.__exit__, None, None, None)

    def restore(self):
        os.environ.pop("ELEVENLABS_API_KEY", None)
        if self.key:
            os.environ["ELEVENLABS_API_KEY"] = self.key
        if self.old:
            os.environ["ELEVENLABS"] = self.old

    def answer(self, req):
        self.sent.append(json.loads(req.data))
        return io.BytesIO(TONE)

    def write(self, beats, language="en"):
        script = {"language": language, "scenes": [{"id": "a", "kind": "title", "title": "T", "beats": beats}]}
        json.dump(script, open(os.path.join(self.project, "src", "script.json"), "w"))

    def test_every_line_goes_to_elevenlabs_in_the_script_language(self):
        self.write([{"text": "Xin chào.", "ref": "x"}], language="vi")
        self.assertEqual(voice.main(["voice.py", self.project]), 0)
        self.assertEqual(self.sent[0]["language_code"], "vi")
        self.assertEqual(self.sent[0]["text"], "Xin chào.")
        self.assertTrue(os.path.exists(os.path.join(self.project, "public", "voice", "a-0.mp3")))

    def test_no_key_stops_before_any_call(self):
        del os.environ["ELEVENLABS_API_KEY"]
        self.write([{"text": "Hello.", "ref": "x"}])
        with self.assertRaises(SystemExit) as stop:
            voice.main(["voice.py", self.project])
        self.assertIn("ELEVENLABS_API_KEY", str(stop.exception))
        self.assertEqual(self.sent, [])

    def test_the_old_engine_flag_is_gone(self):
        self.write([{"text": "Hello.", "ref": "x"}])
        with self.assertRaises(SystemExit) as stop:
            voice.main(["voice.py", self.project, "--engine", "say"])
        self.assertIn("--engine", str(stop.exception))
        self.assertEqual(self.sent, [])

    def test_a_refused_call_names_the_code_and_leaves_no_file(self):
        def refuse(req):
            raise urllib.error.HTTPError(req.full_url, 429, "busy", {}, io.BytesIO(b""))

        urllib.request.urlopen = refuse
        self.write([{"text": "Hello.", "ref": "x"}])
        with self.assertRaises(SystemExit) as stop:
            voice.main(["voice.py", self.project])
        self.assertIn("429", str(stop.exception))
        self.assertFalse(os.path.exists(os.path.join(self.project, "public", "voice", "a-0.mp3")))

    def test_a_refusal_says_why_in_the_vendors_words(self):
        body = b'{"detail":{"status":"payment_issue","message":"Complete the latest invoice to continue usage."}}'

        def refuse(req):
            raise urllib.error.HTTPError(req.full_url, 401, "no", {}, io.BytesIO(body))

        urllib.request.urlopen = refuse
        self.write([{"text": "Hello.", "ref": "x"}])
        with self.assertRaises(SystemExit) as stop:
            voice.main(["voice.py", self.project])
        self.assertIn("401", str(stop.exception))
        self.assertIn("Complete the latest invoice", str(stop.exception))

    def test_spoken_replaces_what_is_said_and_text_stays_on_screen(self):
        self.write([{"text": "POST /api/offers answers 409.", "spoken": "The offers route answers four oh nine.", "ref": "x"}])
        voice.main(["voice.py", self.project])
        self.assertEqual(self.sent[0]["text"], "The offers route answers four oh nine.")

    def test_a_second_run_pays_only_for_the_line_that_changed(self):
        self.write([{"text": "One.", "ref": "x"}, {"text": "Two.", "ref": "x"}])
        voice.main(["voice.py", self.project])
        self.assertEqual(len(self.sent), 2)
        self.sent.clear()
        self.write([{"text": "One.", "ref": "x"}, {"text": "Three.", "ref": "x"}])
        voice.main(["voice.py", self.project])
        self.assertEqual([b["text"] for b in self.sent], ["Three."])
        lengths = json.load(open(os.path.join(self.project, "src", "voice.json")))
        self.assertEqual(len(lengths["a"]), 2)

    def test_a_new_language_is_not_served_from_the_old_recording(self):
        self.write([{"text": "One.", "ref": "x"}])
        voice.main(["voice.py", self.project])
        self.sent.clear()
        self.write([{"text": "One.", "ref": "x"}], language="vi")
        voice.main(["voice.py", self.project])
        self.assertEqual(len(self.sent), 1)


if __name__ == "__main__":
    unittest.main()
