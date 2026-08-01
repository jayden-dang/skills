"""IMPN source contracts — classified mid-build implementation-notes.

IMPN-1.1 IMPN-1.2 IMPN-1.3 IMPN-1.4 IMPN-1.5 IMPN-1.6 IMPN-1.7
IMPN-2.1 IMPN-2.2 IMPN-2.3 IMPN-3.1 IMPN-3.2 IMPN-3.3
IMPN-4.1 IMPN-4.2 IMPN-4.3 IMPN-4.4 IMPN-5.1
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQ = ROOT / "docs" / "specs" / "2026-08-01-implementation-notes" / "requirements.md"
SCEN = ROOT / "tests" / "implementation-notes" / "scenarios.md"
PRESSURE = ROOT / "tests" / "implementation-notes" / "scenarios-pressure.md"
PROMPT = ROOT / "skills" / "execution" / "build-in-waves" / "implementer-prompt.md"
WAVES = ROOT / "skills" / "execution" / "build-in-waves" / "SKILL.md"
STORY = ROOT / "skills" / "execution" / "build-by-story" / "SKILL.md"
INLINE = ROOT / "skills" / "execution" / "build-inline" / "SKILL.md"
HANDOFF = ROOT / "skills" / "track" / "write-handoff" / "SKILL.md"
PCHG = ROOT / "skills" / "ship" / "package-change" / "SKILL.md"
LAND = ROOT / "skills" / "ship" / "land-branch" / "SKILL.md"
FRAME = ROOT / "skills" / "discovery" / "frame-change" / "SKILL.md"
EPHEMERA = ROOT / "templates" / "skills-ephemera-paths.md"

FIELDS = [
    "Task",
    "Unknown class",
    "Map said",
    "Territory showed",
    "Deviation",
    "Cause",
    "Choice",
    "Map impact",
    "Revisit",
]

UNKNOWN_CLASSES = [
    "known-unknown",
    "unknown-known",
    "unknown-unknown",
    "assumption-break",
    "blindspot",
]

MAP_IMPACTS = ["none", "revisit-only", "reroute-plan", "realign-spec"]


def _req_ids() -> set[str]:
    return set(re.findall(r"\*\*(IMPN-\d+\.\d+)\*\*", REQ.read_text()))


class TestImplementerPromptSchema(unittest.TestCase):
    def test_IMPN_1_2_1_3_1_4_nine_fields_and_enums(self):
        text = PROMPT.read_text()
        for f in FIELDS:
            self.assertIn(f, text, f"missing field {f}")
        for u in UNKNOWN_CLASSES:
            self.assertIn(u, text)
        for m in MAP_IMPACTS:
            self.assertIn(m, text)

    def test_IMPN_1_1_1_5_2_3_4_4_path_and_conservative(self):
        text = PROMPT.read_text()
        self.assertIn(".skills/<CODE>/implementation-notes.md", text)
        self.assertRegex(text, re.compile(r"conservative", re.I))
        self.assertRegex(text, re.compile(r"BEFORE you finish|before finishing", re.I))

    def test_IMPN_2_1_prompt_is_deviations_ssot(self):
        text = PROMPT.read_text()
        self.assertIn("## Deviations", text)
        self.assertIn("Unknown class", text)

    def test_IMPN_all_ids_in_scenarios(self):
        self.assertTrue(SCEN.is_file())
        scen = SCEN.read_text()
        missing = sorted(i for i in _req_ids() if i not in scen)
        self.assertEqual(missing, [], f"missing: {missing}")

    def test_IMPN_5_1_pressure_append(self):
        self.assertTrue(PRESSURE.is_file())
        p = PRESSURE.read_text()
        self.assertIn("IMPN-5.1", p)
        self.assertRegex(p, re.compile(r"two|append|second entr", re.I))

    def test_IMPN_pressure_five_field_and_silent_stretch(self):
        p = PRESSURE.read_text()
        self.assertIn("IMPN-1.7", p)
        self.assertIn("IMPN-1.6", p)


class TestExecuteRoutes(unittest.TestCase):
    def test_IMPN_2_2_inline_full_fields(self):
        text = INLINE.read_text()
        for f in ("Unknown class", "Map said", "Territory showed", "Map impact", "Revisit"):
            self.assertIn(f, text)

    def test_IMPN_1_6_1_7_waves_and_story(self):
        for path in (WAVES, STORY):
            text = path.read_text()
            self.assertIn("implementation-notes.md", text)
            self.assertRegex(
                text,
                re.compile(r"incomplete|Missing notes|notes path", re.I),
            )
            self.assertIn("reroute-plan", text)

    def test_IMPN_4_2_4_3_no_silent_map_rewrite_and_tdd(self):
        text = INLINE.read_text() + WAVES.read_text()
        self.assertRegex(text, re.compile(r"reroute-plan|do not stretch|falsif", re.I))
        self.assertIn("test-first", text)


class TestPostBuildSurface(unittest.TestCase):
    def test_IMPN_3_1_write_handoff(self):
        text = HANDOFF.read_text()
        self.assertIn("implementation-notes.md", text)
        self.assertRegex(text, re.compile(r"Map impact|non-none|≠ none|not `none`|not none", re.I))

    def test_IMPN_3_2_package_change(self):
        text = PCHG.read_text()
        self.assertIn("implementation-notes.md", text)

    def test_IMPN_3_3_land_branch(self):
        text = LAND.read_text()
        self.assertIn("implementation-notes.md", text)
        self.assertRegex(text, re.compile(r"reroute-plan|realign-spec", re.I))

    def test_IMPN_4_1_discovery_still_owns_knowns(self):
        frame = FRAME.read_text()
        self.assertIn("Known unknowns", frame)
        self.assertIn("Unknown knowns", frame)
        prompt = PROMPT.read_text()
        self.assertNotRegex(
            prompt,
            re.compile(r"replace.*knowns inventory|replaces frame-change knowns", re.I),
        )


if __name__ == "__main__":
    unittest.main()
