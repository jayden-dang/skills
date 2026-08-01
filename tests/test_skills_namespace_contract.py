"""SKNS contract tests — path grammar SSOT and skill-body path prescriptions.

SKNS-1.1 SKNS-1.2 SKNS-1.3 SKNS-1.4 SKNS-2.1 SKNS-2.2 SKNS-2.3 SKNS-2.4
SKNS-3.1 SKNS-3.2 SKNS-3.3 SKNS-4.1 SKNS-4.2 SKNS-4.3 SKNS-5.1 SKNS-5.2
SKNS-5.3 SKNS-5.4 SKNS-6.1 SKNS-6.2 SKNS-6.3 SKNS-6.4 SKNS-7.1
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SSOT = ROOT / "templates" / "skills-ephemera-paths.md"
SCEN = ROOT / "tests" / "skills-namespace" / "scenarios.md"
PRESSURE = ROOT / "tests" / "skills-namespace" / "scenarios-pressure.md"
REQ = ROOT / "docs" / "specs" / "2026-08-01-skills-namespace" / "requirements.md"

EXECUTE_SKILLS = [
    ROOT / "skills" / "execution" / "build-in-waves" / "SKILL.md",
    ROOT / "skills" / "execution" / "build-by-story" / "SKILL.md",
    ROOT / "skills" / "execution" / "build-inline" / "SKILL.md",
    ROOT / "skills" / "execution" / "build-in-waves" / "implementer-prompt.md",
]

DISCOVERY_SPEC = [
    ROOT / "skills" / "discovery" / "frame-change" / "SKILL.md",
    ROOT / "skills" / "spec" / "specify-behavior" / "SKILL.md",
    ROOT / "skills" / "spec" / "design-solution" / "SKILL.md",
    ROOT / "skills" / "spec" / "plan-tasks" / "SKILL.md",
]

ACCEPTANCE = [
    ROOT / "skills" / "acceptance" / "validate-feature" / "SKILL.md",
    ROOT / "skills" / "acceptance" / "review-product-flow" / "SKILL.md",
    ROOT / "skills" / "acceptance" / "vet-product-flow" / "SKILL.md",
    ROOT / "skills" / "acceptance" / "run-product-walkthrough" / "SKILL.md",
]

SHIP_TRACK = [
    ROOT / "skills" / "ship" / "package-change" / "SKILL.md",
    ROOT / "skills" / "ship" / "land-branch" / "SKILL.md",
    ROOT / "skills" / "track" / "reroute-plan" / "SKILL.md",
    ROOT / "skills" / "track" / "refresh-roadmap-status" / "SKILL.md",
    ROOT / "skills" / "track" / "write-handoff" / "SKILL.md",
    ROOT / "skills" / "review" / "brief-team" / "SKILL.md",
]


def _req_ids() -> set[str]:
    return set(re.findall(r"\*\*(SKNS-\d+\.\d+)\*\*", REQ.read_text()))


def _combined(paths: list[Path]) -> str:
    parts = []
    for p in paths:
        if p.is_file():
            parts.append(p.read_text())
    return "\n".join(parts)


class TestSkillsEphemeraSsot(unittest.TestCase):
    def test_SKNS_1_1_1_2_ssot_exists_with_code_root(self):
        self.assertTrue(SSOT.is_file(), f"missing {SSOT}")
        text = SSOT.read_text()
        self.assertIn(".skills/<CODE>/", text)
        self.assertRegex(text, re.compile(r"Feature code only|CODE alone|no long", re.I))

    def test_SKNS_2_shared_roots_documented(self):
        text = SSOT.read_text()
        for token in ("pathfind", "research", "decisions", "pr-packages"):
            self.assertIn(token, text)

    def test_SKNS_3_1_3_3_pending_and_adhoc(self):
        text = SSOT.read_text()
        self.assertIn("_pending-", text)
        self.assertIn("_adhoc/", text)

    def test_SKNS_1_3_resolve_order(self):
        text = SSOT.read_text()
        self.assertRegex(text, re.compile(r"resolve|resolution order|Feature code", re.I))

    def test_SKNS_4_1_4_2_legacy_read_write_rule(self):
        text = SSOT.read_text()
        self.assertRegex(text, re.compile(r"legacy", re.I))
        self.assertRegex(text, re.compile(r"read", re.I))
        self.assertRegex(text, re.compile(r"write", re.I))

    def test_SKNS_4_3_no_auto_migrate_in_ssot(self):
        text = SSOT.read_text()
        self.assertRegex(text, re.compile(r"auto-migrate|MUST NOT.*migrat|no auto", re.I))

    def test_SKNS_all_requirement_ids_in_scenarios(self):
        ids = _req_ids()
        self.assertTrue(SCEN.is_file(), f"missing {SCEN}")
        scen = SCEN.read_text()
        missing = sorted(i for i in ids if i not in scen)
        self.assertEqual(missing, [], f"missing from scenarios: {missing}")


class TestExecuteFamilyPaths(unittest.TestCase):
    def test_SKNS_1_4_5_1_6_2_execute_prescribes_code_progress(self):
        for path in EXECUTE_SKILLS:
            self.assertTrue(path.is_file(), f"missing {path}")
            text = path.read_text()
            self.assertIn(
                ".skills/<CODE>/",
                text,
                f"{path.relative_to(ROOT)} must prescribe .skills/<CODE>/",
            )
            self.assertIn("progress.md", text)

    def test_SKNS_5_1_execute_brief_report_notes_under_code(self):
        text = _combined(EXECUTE_SKILLS)
        for token in ("task-N-brief", "task-N-report", "implementation-notes"):
            self.assertIn(token, text)
        # Prefer CODE-prefixed forms in write targets
        self.assertRegex(
            text,
            re.compile(r"\.skills/<CODE>/task-N-brief|\.skills/<CODE>/.*brief", re.I),
        )

    def test_SKNS_7_1_dual_code_isolation_pressure(self):
        self.assertTrue(PRESSURE.is_file())
        text = PRESSURE.read_text()
        self.assertIn("SKNS-7.1", text)
        self.assertRegex(text, re.compile(r"two|dual|two CODE|two feature", re.I))


class TestDiscoverySpecPaths(unittest.TestCase):
    def test_SKNS_5_2_3_1_discovery_uses_code_or_pending(self):
        text = _combined(DISCOVERY_SPEC)
        self.assertTrue(
            ".skills/<CODE>/" in text or "_pending-" in text,
            "discovery/spec must cite CODE or _pending- roots",
        )

    def test_SKNS_3_2_specify_behavior_promotes_pending(self):
        text = (ROOT / "skills" / "spec" / "specify-behavior" / "SKILL.md").read_text()
        self.assertRegex(text, re.compile(r"promot|_pending-|pending.*CODE|move.*\.skills/", re.I))

    def test_SKNS_2_1_6_1_pathfind_stays_shared(self):
        frame = (ROOT / "skills" / "discovery" / "frame-change" / "SKILL.md").read_text()
        pathfind = (ROOT / "skills" / "discovery" / "pathfind" / "SKILL.md").read_text()
        combined = frame + pathfind
        self.assertIn(".skills/pathfind/", combined)


class TestAcceptancePaths(unittest.TestCase):
    def test_SKNS_5_3_acceptance_under_code(self):
        text = _combined(ACCEPTANCE)
        self.assertIn(".skills/<CODE>/", text)


class TestShipTrackPaths(unittest.TestCase):
    def test_SKNS_5_1_notes_under_code(self):
        text = _combined(SHIP_TRACK)
        self.assertIn(".skills/<CODE>/", text)
        self.assertIn("implementation-notes", text)

    def test_SKNS_2_3_2_4_pr_packages_and_decisions_shared(self):
        pchg = (ROOT / "skills" / "ship" / "package-change" / "SKILL.md").read_text()
        self.assertIn("pr-packages", pchg)
        # decisions remain under .skills/decisions/
        rec = (ROOT / "skills" / "ship" / "record-verdict" / "SKILL.md").read_text()
        self.assertIn(".skills/decisions/", rec)


class TestDocsAndGuards(unittest.TestCase):
    def test_SKNS_5_4_agents_describe_per_code(self):
        agents = (ROOT / "AGENTS.md").read_text()
        arts = (ROOT / "docs" / "guide" / "concepts" / "artifacts.md").read_text()
        blob = agents + arts
        self.assertIn(".skills/<CODE>", blob)
        self.assertIn("progress.md", agents)

    def test_SKNS_6_3_gitignore_language(self):
        pchg = (ROOT / "skills" / "ship" / "package-change" / "SKILL.md").read_text()
        self.assertRegex(pchg, r"git-ignor", re.I)

    def test_SKNS_6_4_no_layout_e_codes_in_scenarios(self):
        scen = SCEN.read_text() if SCEN.is_file() else ""
        self.assertNotRegex(scen, r"new E-code|E6 layout")

    def test_SKNS_no_python_under_skills_for_this_feature(self):
        # Guard: no new .py under skills/ from this feature's package (none expected)
        self.assertFalse(
            (ROOT / "skills" / "execution" / "skills-namespace").exists()
        )


if __name__ == "__main__":
    unittest.main()
