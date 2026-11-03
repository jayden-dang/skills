#!/usr/bin/env python3
"""Run with: python3 -m unittest discover -s skills/craft/make-video/scripts"""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import check_video as cv  # noqa: E402


def script(**over):
    base = {
        "language": "en",
        "source": {"kind": "feature", "ref": "abc123"},
        "scenes": [
            {"id": "a", "kind": "points", "title": "T", "points": ["p"], "beats": [{"text": "One line.", "ref": "alerts.js:3"}]}
        ],
    }
    base.update(over)
    return base


class ValidateScript(unittest.TestCase):
    def test_a_complete_script_has_no_faults(self):
        self.assertEqual(cv.validate_script(script()), [])

    def test_a_sentence_without_a_source_is_a_fault(self):
        s = script()
        s["scenes"][0]["beats"][0]["ref"] = ""
        self.assertIn("a-0: no source", cv.validate_script(s))

    def test_a_sentence_over_twenty_words_is_a_fault(self):
        s = script()
        s["scenes"][0]["beats"][0]["text"] = " ".join(["word"] * 21)
        self.assertIn("a-0: over 20 words", cv.validate_script(s))

    def test_an_unknown_source_kind_is_a_fault(self):
        self.assertIn("source.kind must be feature, pr or release", cv.validate_script(script(source={"kind": "spec", "ref": "x"})))

    def test_a_missing_language_is_a_fault(self):
        s = script()
        del s["language"]
        self.assertIn("language is missing", cv.validate_script(s))

    def test_a_clip_scene_with_no_clip_is_a_fault(self):
        s = script()
        s["scenes"][0] = {"id": "c", "kind": "clip", "title": "T", "beats": [{"text": "Hi.", "ref": "a.js:1"}]}
        self.assertIn("c: clip scene names no clip", cv.validate_script(s))


class JudgeClip(unittest.TestCase):
    def test_sixteen_by_nine_at_1600_passes(self):
        self.assertIsNone(cv.judge_clip(1600, 900))

    def test_the_default_recorded_viewport_fails(self):
        self.assertIn("1280x578", cv.judge_clip(1280, 578))

    def test_small_sixteen_by_nine_fails(self):
        self.assertIn("1280x720", cv.judge_clip(1280, 720))


class JudgeMedia(unittest.TestCase):
    def clean(self, **over):
        m = {"width": 1920, "height": 1080, "has_audio": True, "duration": 60.0, "peak": -2.0, "loudness": -16.0, "freezes": [], "silences": []}
        m.update(over)
        return m

    def test_a_clean_render_has_no_faults(self):
        self.assertEqual(cv.judge_media(self.clean()), [])

    def test_720p_fails(self):
        self.assertTrue(any("1920x1080" in f for f in cv.judge_media(self.clean(width=1280, height=720))))

    def test_no_audio_fails(self):
        self.assertIn("no audio stream", cv.judge_media(self.clean(has_audio=False)))

    def test_a_long_still_mid_video_fails(self):
        faults = cv.judge_media(self.clean(freezes=[(10.0, 8.0)]))
        self.assertTrue(any("still for 8.0s at 10.0s" in f for f in faults))

    def test_a_still_closing_card_passes(self):
        self.assertEqual(cv.judge_media(self.clean(freezes=[(52.0, 8.0)])), [])

    def test_a_long_silence_mid_video_fails(self):
        faults = cv.judge_media(self.clean(silences=[(20.0, 3.5)]))
        self.assertTrue(any("silent for 3.5s at 20.0s" in f for f in faults))

    def test_a_clipping_peak_fails(self):
        self.assertTrue(any("peak" in f for f in cv.judge_media(self.clean(peak=-0.3))))


class FileRefs(unittest.TestCase):
    def test_finds_path_and_line(self):
        self.assertEqual(cv.file_refs("alerts.js:3, docs/a.md:12 and a request"), [("alerts.js", 3), ("docs/a.md", 12)])

    def test_ignores_text_without_a_line(self):
        self.assertEqual(cv.file_refs("recorded run, GET /health"), [])


if __name__ == "__main__":
    unittest.main()
