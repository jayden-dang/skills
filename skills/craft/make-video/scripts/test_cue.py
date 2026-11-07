#!/usr/bin/env python3
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "template", "manim"))
from cue import wait_for  # noqa: E402


class WaitFor(unittest.TestCase):
    def test_it_waits_for_a_word_ahead(self):
        self.assertAlmostEqual(wait_for(1.0, 2.5, "x"), 1.5)

    def test_under_a_frame_ahead_is_no_wait(self):
        self.assertEqual(wait_for(1.0, 1.02, "x"), 0)

    def test_a_frame_late_is_on_the_word(self):
        self.assertEqual(wait_for(1.10, 1.07, "x"), 0)

    def test_three_frames_late_is_still_on_the_word(self):
        self.assertEqual(wait_for(1.10, 1.0, "x"), 0)

    def test_more_than_a_tenth_late_stops_the_render_by_name(self):
        with self.assertRaisesRegex(ValueError, r'restrict: line 0 is spoken at 1.00s, but the animation before it runs to 1.20s. Shorten that animation by 0.20s.'):
            wait_for(1.20, 1.0, "restrict: line 0")


if __name__ == "__main__":
    unittest.main()
