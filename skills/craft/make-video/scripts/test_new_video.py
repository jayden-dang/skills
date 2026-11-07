#!/usr/bin/env python3
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import new_video as nv  # noqa: E402


class LookFor(unittest.TestCase):
    def test_a_release_reads_as_paper(self):
        self.assertEqual(nv.look_for(["x", ".", "s", "--kind", "release"]), "paper")

    def test_a_concept_is_a_blueprint(self):
        self.assertEqual(nv.look_for(["x", ".", "s", "--kind", "concept"]), "blueprint")

    def test_other_kinds_take_the_default(self):
        for kind in ("feature", "pr", "spec"):
            self.assertEqual(nv.look_for(["x", ".", "s", "--kind", kind]), "night")

    def test_no_kind_takes_the_default(self):
        self.assertEqual(nv.look_for(["x", ".", "s"]), "night")

    def test_a_named_look_wins(self):
        self.assertEqual(nv.look_for(["x", ".", "s", "--kind", "release", "--look", "night"]), "night")


if __name__ == "__main__":
    unittest.main()
