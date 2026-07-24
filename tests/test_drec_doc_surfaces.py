"""Doc-surface and skill-text structural checks for DREC.

DREC-9.1 DREC-9.2 DREC-9.4 DREC-9.8 DREC-9.9
DREC-6.4 DREC-6.12 DREC-6.13 DREC-6.14 DREC-9.3
DREC-7.1 DREC-7.2 DREC-7.3 DREC-7.4 DREC-7.5 DREC-7.6
DREC-11.10 DREC-11.20 DREC-11.21
DREC-10.1 DREC-10.2 DREC-10.3 DREC-10.4 DREC-10.5 DREC-10.6 DREC-10.7 DREC-10.8
DREC-12.1 DREC-12.2 DREC-12.3 DREC-12.4 DREC-12.5 DREC-12.6 DREC-12.7 DREC-12.8
DREC-12.9 DREC-12.10 DREC-12.11 DREC-12.12
DREC-3.15 DREC-3.16 DREC-13.1 DREC-13.2
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SKILL = REPO / "skills" / "ship" / "record-decision" / "SKILL.md"
RECORD = REPO / "skills" / "ship" / "record-decision" / "RECORD.md"
PLUGIN = REPO / ".claude-plugin" / "plugin.json"


class TestDRECRecordDecisionSkill(unittest.TestCase):
    def test_DREC_9_1_9_2_skill_and_record_siblings(self):
        """DREC-9.1 DREC-9.2"""
        self.assertTrue(SKILL.is_file())
        self.assertTrue(RECORD.is_file())
        body = SKILL.read_text(encoding="utf-8")
        self.assertIn("RECORD.md", body)
        self.assertNotIn("Payload-Digest-Algorithm:", body)

    def test_DREC_9_4_9_9_frontmatter(self):
        """DREC-9.4 DREC-9.9"""
        text = SKILL.read_text(encoding="utf-8")
        self.assertIn("name: record-decision", text)
        fm = text.split("---", 2)[1]
        self.assertNotIn("disable-model-invocation: true", fm)
        self.assertRegex(fm, r"finish-branch|release")
        self.assertNotRegex(fm.lower(), r"important decision|generic approval")

    def test_DREC_9_8_no_root_template(self):
        """DREC-9.8"""
        self.assertFalse((REPO / "RECORD.template.md").exists())
        self.assertFalse((REPO / "docs" / "decisions" / "TEMPLATE.md").exists())

    def test_DREC_plugin_lists_record_decision(self):
        data = json.loads(PLUGIN.read_text(encoding="utf-8"))
        skills = {s.removeprefix("./") for s in data["skills"]}
        self.assertIn("skills/ship/record-decision", skills)

    def test_DREC_15_and_caller_gate_doctrine(self):
        """DREC-9.5 DREC-9.6 DREC-15.1 DREC-4.3 DREC-3.4"""
        body = SKILL.read_text(encoding="utf-8")
        self.assertIn("HARD-GATE", body)
        self.assertIn("finish-branch", body)
        self.assertIn("release", body)
        self.assertIn("record-before-crossing", body.lower() + body)
        self.assertTrue(
            "Crossing executes only after" in body
            or "validator exits 0" in body
            or "only after the validator exits 0" in body
        )
        self.assertIn("Minimal is never published", body)
        self.assertIn("exact user-authored words", body)


class TestDRECFinishBranch(unittest.TestCase):
    def test_DREC_6_4_6_14_block_option_and_guards(self):
        """DREC-6.4 DREC-6.12 DREC-6.13 DREC-6.14 DREC-9.3"""
        text = (REPO / "skills/ship/finish-branch/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Block:", text)
        self.assertIn("REQUIRED SUB-SKILL: use `record-decision`", text)
        self.assertIn("discard", text)
        for phrase in ["Merge", "Pull Request", "Keep", "Discard"]:
            self.assertIn(phrase, text)
        self.assertTrue(
            "Do not offer merge or PR" in text
            or "withhold **merge** and **PR**" in text
            or "withhold merge and PR" in text.lower()
        )
        self.assertIn("literally type `discard`", text)


class TestDRECRelease(unittest.TestCase):
    def test_DREC_7_release_hooks(self):
        """DREC-7.1 DREC-7.2 DREC-7.3 DREC-7.4 DREC-7.5 DREC-7.6"""
        text = (REPO / "skills/ship/release/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("REQUIRED SUB-SKILL: use `record-decision`", text)
        self.assertIn("release-approve", text)
        self.assertIn("release-reject", text)
        self.assertIn("The stop rule", text)
        self.assertIn("Only after explicit user approval", text)


class TestDRECTrace(unittest.TestCase):
    def test_DREC_11_20_11_21_trace_guards(self):
        """DREC-11.20 DREC-11.21 DREC-11.10"""
        text = (REPO / "skills/execution/trace/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Decision-record passes", text)
        self.assertIn("docs/decisions/", text)
        self.assertIn("validate-records.sh", text)
        for code in ["E1", "E2", "E3", "W1", "W2", "E4", "E5", "W3"]:
            self.assertIn(code, text)
        self.assertIn("Coverage is textual presence", text)
        self.assertIsNotNone(
            re.search(r"crossing.without.record|without a (decision )?record", text, re.I)
        )


class TestDRECParticipantSurfaces(unittest.TestCase):
    def test_DREC_10_1_through_10_8(self):
        """DREC-10.1 DREC-10.2 DREC-10.3 DREC-10.4 DREC-10.5 DREC-10.6 DREC-10.7 DREC-10.8"""
        index = (REPO / "docs/architecture/INDEX.md").read_text(encoding="utf-8")
        artifacts = (REPO / "docs/architecture/artifacts.md").read_text(encoding="utf-8")
        agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
        using = (REPO / "skills/meta/using-skills/SKILL.md").read_text(encoding="utf-8")

        self.assertIn("**ARCH-6**", index)
        self.assertIsNotNone(re.search(r"mediat|never infer|CODEOWNERS|roster", index, re.I))

        for role in ["skill-mediated", "external contributor", "accountable reviewer"]:
            self.assertIsNotNone(re.search(role, artifacts, re.I), role)

        self.assertIn("Participant boundary", agents)
        self.assertIsNotNone(re.search(r"mediat", agents, re.I))
        self.assertIn("Four Iron Laws", agents)
        self.assertIn("Orchestration rule", agents)

        self.assertIsNotNone(re.search(r"mediat|never infer|supplied", using, re.I))
        self.assertIn("SUBAGENT-EXEMPT", using)
        self.assertIn("1% chance", using)


class TestDRECInterpret(unittest.TestCase):
    def test_DREC_12_interpret_doctrine(self):
        """DREC-12.1 DREC-12.2 DREC-12.3 DREC-12.4 DREC-12.5 DREC-12.6 DREC-12.7 DREC-12.8 DREC-12.9 DREC-12.10 DREC-12.11 DREC-12.12"""
        text = (REPO / "skills/discovery/interpret/SKILL.md").read_text(encoding="utf-8")
        for label in [
            "Source claim",
            "Verified fact",
            "Inference",
            "Recommendation",
            "User decision",
            "Open question",
        ]:
            self.assertIn(label, text)
        for label in [
            "User decisions",
            "Human rationale",
            "Verified evidence",
            "Interpret analysis",
            "Open questions",
            "Prepared reply",
            "Transport-adoption status",
        ]:
            self.assertIn(label, text)
        self.assertIn("Decided", text)
        self.assertIn("Human rationale: not supplied", text)
        self.assertRegex(text, r"never infer|Never.*infer", re.I)
        self.assertRegex(text, r"read-only|never commit", re.I)
        for n in [
            "1. Translate",
            "2. Simplify",
            "3. Feynman",
            "4. Independent analysis",
            "5. Prepare the reply",
        ]:
            self.assertIn(n, text)
        self.assertIn("companion", text.lower())


class TestDRECProjectDocs(unittest.TestCase):
    def test_DREC_3_15_3_16_pin_schema(self):
        """DREC-3.15 DREC-3.16"""
        tmpl = (REPO / "templates/agents/project.md").read_text(encoding="utf-8")
        self.assertIn("## Decision boundaries", tmpl)
        self.assertIn("Boundary-Type", tmpl)
        self.assertIn("Floor", tmpl)

    def test_DREC_13_1_13_2_discovery_convention(self):
        """DREC-13.1 DREC-13.2"""
        art = (REPO / "docs/architecture/artifacts.md").read_text(encoding="utf-8")
        self.assertIn("discovery.md", art)
        self.assertRegex(art, r"non-normative|never required")
        self.assertRegex(art, r"sole normative")


if __name__ == "__main__":
    unittest.main()
