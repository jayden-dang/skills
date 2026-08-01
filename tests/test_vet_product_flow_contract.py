"""VPF skill body contracts — isolation, map, non-claims, report, guide-gap.

VPF-1.1 VPF-1.2 VPF-1.3 VPF-1.4 VPF-1.5 VPF-2.1 VPF-2.2 VPF-2.3 VPF-2.4
VPF-2.5 VPF-2.6 VPF-3.1 VPF-3.2 VPF-3.3 VPF-3.4 VPF-3.5 VPF-6.2 VPF-6.3
VPF-6.4 VPF-6.5 VPF-6.6 VPF-6.7 VPF-8.1
"""
from __future__ import annotations

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "acceptance" / "vet-product-flow" / "SKILL.md"
BRIEF = (
    REPO
    / "skills"
    / "acceptance"
    / "vet-product-flow"
    / "references"
    / "judgment-brief.md"
)
SCHEMA = (
    REPO
    / "skills"
    / "acceptance"
    / "vet-product-flow"
    / "references"
    / "report-schema.md"
)
SCENARIOS = REPO / "tests" / "vet-product-flow" / "scenarios.md"
PRESSURE = REPO / "tests" / "vet-product-flow" / "scenarios-pressure.md"


def _frontmatter(text: str) -> str:
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return ""
    return m.group(1)


def _body(text: str) -> str:
    parts = text.split("---", 2)
    return parts[2] if len(parts) > 2 else text


class VetProductFlowSkillExists(unittest.TestCase):
    """VPF-1.1 — model-invoked skill path and frontmatter."""

    def test_VPF_1_1_skill_path_and_name(self):
        """VPF-1.1 — SKILL.md exists; name: vet-product-flow; model-invoked."""
        self.assertTrue(SKILL.exists(), f"missing {SKILL}")
        text = SKILL.read_text()
        fm = _frontmatter(text)
        self.assertIn("name: vet-product-flow", fm)
        self.assertNotIn("disable-model-invocation", fm)

    def test_VPF_1_1_description_triggers_not_workflow(self):
        """VPF-1.1 — description triggers judgment/isolation/before dogfood; no step list."""
        text = SKILL.read_text()
        fm = _frontmatter(text)
        desc_m = re.search(
            r"description:\s*(.+?)(?=\n\w|\n---|\Z)", fm, re.DOTALL
        )
        self.assertIsNotNone(desc_m, "frontmatter description missing")
        d = desc_m.group(1).lower()
        # Trigger language
        self.assertTrue(
            any(
                t in d
                for t in (
                    "judgment",
                    "isolat",
                    "dogfood",
                    "missing-situation",
                    "before dogfood",
                    "vet",
                )
            ),
            f"description should trigger judgment/isolation/dogfood: {d!r}",
        )
        # Not a workflow summary
        self.assertNotRegex(d, r"step\s*1|1\.\s*load|then write the report")
        self.assertNotIn("surface map procedure", d)


class VetProductFlowIsolation(unittest.TestCase):
    """VPF-1.2 — fresh isolated pass; subagent or AUTHORING CLOSED fallback."""

    def setUp(self):
        self.assertTrue(SKILL.exists(), f"missing {SKILL}")
        self.body = _body(SKILL.read_text())

    def test_VPF_1_2_subagent_or_authoring_closed_fallback(self):
        """VPF-1.2 — subagent path and AUTHORING CLOSED inline fallback."""
        self.assertRegex(self.body, r"(?i)subagent")
        self.assertIn("AUTHORING CLOSED", self.body)
        self.assertRegex(
            self.body,
            r"(?i)isolat(ed|ion)|fresh isolat",
        )

    def test_VPF_1_2_forbids_same_session_section4_self_clear(self):
        """VPF-1.2 — forbids same-session §4 self-clear as substitute for isolation."""
        self.assertRegex(
            self.body,
            r"(?is)(same.?session|same agent).{0,80}(§\s*4|section\s*4|self-?check|self-?clear)|"
            r"(§\s*4|section\s*4).{0,80}(not|never|forbid|not a substitute)",
        )

    def test_VPF_1_2_judgment_brief_exists_with_paths(self):
        """VPF-1.2 — judgment-brief.md lists run path, triad, report, read-only."""
        self.assertTrue(BRIEF.exists(), f"missing {BRIEF}")
        b = BRIEF.read_text()
        self.assertRegex(b, r"(?i)run.?file|run path|run_file")
        self.assertRegex(b, r"(?i)triad|requirements\.md|design\.md|tasks\.md")
        self.assertRegex(b, r"(?i)report|vet-product-flow\.md")
        self.assertRegex(b, r"(?i)read-?only|do not (write|modify|patch)|unmodified")


class VetProductFlowReportContract(unittest.TestCase):
    """VPF-1.3 VPF-1.4 VPF-1.5 VPF-8.1 — report path, ids, read-only."""

    def setUp(self):
        self.assertTrue(SKILL.exists(), f"missing {SKILL}")
        self.body = _body(SKILL.read_text())

    def test_VPF_1_3_report_path_and_schema_fields(self):
        """VPF-1.3 — report path `.skills/<slug>-vet-product-flow.md` + stamp fields."""
        self.assertIn(".skills/<slug>-vet-product-flow.md", self.body)
        for field in (
            "cases_fingerprint",
            "run_file",
            "pass_kind",
            "prior_report",
            "open_count",
            "stamped_at",
            "gate_hint",
        ):
            self.assertIn(
                field,
                self.body,
                f"skill body must name report field {field}",
            )
        # Schema still authoritative for shape
        self.assertTrue(SCHEMA.exists())
        schema = SCHEMA.read_text()
        self.assertIn("cases_fingerprint", schema)
        self.assertIn("surface_key", schema)

    def test_VPF_1_4_and_8_1_finding_ids_and_surface_key(self):
        """VPF-1.4 VPF-8.1 — finding ids VPF-N; surface_key reuse on re-check."""
        self.assertRegex(self.body, r"VPF-N")
        self.assertIn("surface_key", self.body)
        self.assertRegex(
            self.body,
            r"(?is)surface_key.{0,120}(reuse|re-?use|same|persist)|"
            r"(re-?check|recheck).{0,120}surface_key",
        )
        # Distinguish finding ids from criterion ids
        self.assertRegex(
            self.body,
            r"(?is)VPF-N\.M|criterion|integer",
        )

    def test_VPF_1_5_read_only_judgment(self):
        """VPF-1.5 — no product code / no run-file writes; report write allowed."""
        self.assertRegex(
            self.body,
            r"(?is)(read-?only|unmodified|do not (write|modify|patch|mutate)).{0,80}"
            r"(product|run.?file)|(product|run.?file).{0,80}"
            r"(unmodified|read-?only|do not (write|modify|patch))",
        )
        self.assertRegex(
            self.body,
            r"(?is)(report).{0,60}(write|allowed|may write)|(write).{0,40}(report)",
        )


class VetProductFlowSurfaceMap(unittest.TestCase):
    """VPF-2.1–2.6 — implementation-surface map claim."""

    def setUp(self):
        self.assertTrue(SKILL.exists(), f"missing {SKILL}")
        self.body = _body(SKILL.read_text())

    def test_VPF_2_1_2_2_user_observable_map(self):
        """VPF-2.1 VPF-2.2 — user-observable map; missing-situation findings."""
        self.assertRegex(self.body, r"(?i)user-?observable")
        self.assertRegex(
            self.body,
            r"(?i)(surface map|implementation-surface|map).{0,40}|"
            r"routes|primary actions|empty",
        )
        self.assertRegex(self.body, r"(?i)missing-?situation")

    def test_VPF_2_3_2_4_evidence_and_no_uninspected(self):
        """VPF-2.3 VPF-2.4 — evidence (file/symbol/route); no uninspected assert."""
        self.assertRegex(
            self.body,
            r"(?i)(evidence|file|symbol|route).{0,40}(open|inspect|pointer)|"
            r"(opened|inspected).{0,40}(code|file|route)",
        )
        self.assertRegex(
            self.body,
            r"(?is)(not inspected|uninspected|never inspected|was not inspected)"
            r".{0,80}(not|shall not|do not|must not|skip)|"
            r"(do not|must not|shall not).{0,80}"
            r"(not inspected|uninspected|never inspected)",
        )

    def test_VPF_2_5_severity_orders_fix_not_gate(self):
        """VPF-2.5 — Critical/Important/Minor order fix only; does not soften gate."""
        for sev in ("Critical", "Important", "Minor"):
            self.assertIn(sev, self.body)
        self.assertRegex(
            self.body,
            r"(?is)severity.{0,80}(order|fix).{0,80}(not|never|does not).{0,40}(gate|soften)|"
            r"(not|never|does not).{0,40}(soften|clear).{0,40}(gate|severity)|"
            r"(severity).{0,60}(does not|shall not|must not).{0,40}(soften|clear|drop)",
        )

    def test_VPF_2_6_hygiene_not_product_claim(self):
        """VPF-2.6 — hygiene not product claim; forbid complete-for-real-users sell."""
        self.assertRegex(
            self.body,
            r"(?i)hygiene|schema.?kind|§\s*1|section\s*1",
        )
        self.assertRegex(
            self.body,
            r"(?is)(not|never|shall not).{0,40}complete for real users|"
            r"complete for real users.{0,40}(not|never|forbid)",
        )


class VetProductFlowNonClaims(unittest.TestCase):
    """VPF-3.1–3.5 — explicit non-claims."""

    def setUp(self):
        self.assertTrue(SKILL.exists(), f"missing {SKILL}")
        self.body = _body(SKILL.read_text())

    def test_VPF_3_1_no_novelty_feel_polish(self):
        """VPF-3.1 — no novelty/feel/polish taste as pass/fail."""
        self.assertRegex(
            self.body,
            r"(?i)novelty|feel|polish",
        )
        self.assertRegex(
            self.body,
            r"(?is)(shall not|must not|do not|never|not).{0,60}"
            r"(novelty|feel|polish|taste)",
        )

    def test_VPF_3_2_no_chaos_load_race_fuzz(self):
        """VPF-3.2 — no chaos/load/race/fuzz requirement."""
        for term in ("chaos", "load", "race", "fuzz"):
            self.assertRegex(
                self.body,
                rf"(?i){term}",
                f"non-claim must mention {term}",
            )

    def test_VPF_3_3_no_speculative_users_will_want(self):
        """VPF-3.3 — no speculative users-will-want findings."""
        self.assertRegex(
            self.body,
            r"(?i)users will want|speculative|should do",
        )

    def test_VPF_3_4_no_global_stamps(self):
        """VPF-3.4 — no good UX / ready to ship / complete for real users stamps."""
        self.assertRegex(
            self.body,
            r"(?i)good UX|ready to ship|complete for real users",
        )

    def test_VPF_3_5_no_drive_or_fe_be_ownership(self):
        """VPF-3.5 — does not replace dogfood; no drive / FE+BE ownership."""
        self.assertRegex(
            self.body,
            r"(?is)(not|never|shall not|do not).{0,40}(replace dogfood|drive)|"
            r"(no drive|does not replace dogfood)",
        )
        self.assertRegex(
            self.body,
            r"(?i)FE\+BE|FE.?BE|front.?end.{0,20}back.?end|saw|server",
        )


class VetProductFlowRationalization(unittest.TestCase):
    """VPF-1.2 VPF-2.6 — rationalization counters same-agent / CLI false confidence."""

    def setUp(self):
        self.assertTrue(SKILL.exists(), f"missing {SKILL}")
        self.body = _body(SKILL.read_text())

    def test_VPF_rationalization_table_same_agent_and_cli(self):
        """VPF-1.2 VPF-2.6 — rationalization table for same-agent and CLI completeness."""
        self.assertRegex(self.body, r"(?i)\|\s*Thought\s*\|\s*Reality\s*\|")
        self.assertRegex(
            self.body,
            r"(?is)same.?agent|same.?session|self-?check|rubber.?stamp",
        )
        self.assertRegex(
            self.body,
            r"(?is)CLI|schema.?kind|mechanical|false confidence|complete for real",
        )


class VetProductFlowGuideGapLoop(unittest.TestCase):
    """VPF-6.2–6.7 — guide-gap fix / re-check loop protocol (Task 3)."""

    def setUp(self):
        self.assertTrue(SKILL.exists(), f"missing {SKILL}")
        self.body = _body(SKILL.read_text())

    def test_VPF_6_2_severity_order_run_file_only_no_product(self):
        """VPF-6.2 — order by severity; patch run file only + re-render; no product."""
        self.assertRegex(
            self.body,
            r"(?i)Guide-gap fix loop|guide-gap fix",
        )
        self.assertRegex(
            self.body,
            r"(?is)order.{0,40}severity|severity.{0,40}order",
        )
        self.assertRegex(
            self.body,
            r"(?is)(run.?file|cases).{0,80}(only|patch)|"
            r"patch.{0,60}(run.?file|only)",
        )
        self.assertRegex(
            self.body,
            r"(?i)re-?render|render",
        )
        self.assertRegex(
            self.body,
            r"(?is)(not|never|no).{0,40}(product|app).{0,40}(patch|code|mutat)|"
            r"(product|app).{0,40}(code|patches?).{0,40}(not|never|out)",
        )

    def test_VPF_6_3_reinvoke_fresh_gate_new_report(self):
        """VPF-6.3 — re-invoke fresh isolated vet; gate uses new report only."""
        self.assertRegex(
            self.body,
            r"(?is)re-?invoke.{0,40}vet-product-flow|"
            r"vet-product-flow.{0,40}(fresh|re-?check|re-?invoke)",
        )
        self.assertRegex(
            self.body,
            r"(?is)fresh.{0,40}isolat|isolat.{0,40}(fresh|re-?check|re-?invoke)",
        )
        self.assertRegex(
            self.body,
            r"(?is)(gate|dogfood).{0,80}(new report|new open)|"
            r"(new report|only against the new).{0,60}(gate|dogfood|re-?evaluat)",
        )

    def test_VPF_6_4_clear_only_absent_or_named_override(self):
        """VPF-6.4 — clear only when gone from open list or named override."""
        self.assertRegex(
            self.body,
            r"(?is)(clear|cleared).{0,100}(open list|absent|no longer)|"
            r"(absent|no longer).{0,80}(open|finding)",
        )
        self.assertRegex(
            self.body,
            r"(?i)named override|explicit override",
        )
        self.assertRegex(
            self.body,
            r"(?is)(never|not|forbid).{0,60}(self-?declar|self-?clear)|"
            r"(self-?declar|self-?clear).{0,60}(never|not|forbid)",
        )

    def test_VPF_6_5_escalate_fixer_threshold_and_brief(self):
        """VPF-6.5 — fixer when ≥5 findings or ≥2 ability areas; brief findings+path."""
        self.assertRegex(
            self.body,
            r"(?is)fixer subagent|isolated fixer",
        )
        self.assertRegex(
            self.body,
            r"(?is)(≥\s*5|>=\s*5|at least 5|≥5).{0,80}(finding|open)|"
            r"(finding|open).{0,40}(≥\s*5|>=\s*5|≥5)",
        )
        self.assertRegex(
            self.body,
            r"(?is)(≥\s*2|>=\s*2|≥2).{0,40}(ability|area)|"
            r"(ability area|multi-?section).{0,40}(≥\s*2|>=\s*2|2)",
        )
        self.assertRegex(
            self.body,
            r"(?is)(brief|vpf-fix-brief).{0,80}(finding|run.?path|run.?file)|"
            r"(finding).{0,40}(run.?path|run.?file).{0,40}(brief)?",
        )

    def test_VPF_6_6_cap_two_rejudgment_cycles(self):
        """VPF-6.6 — cap 2 re-judgment cycles then stop for human."""
        self.assertRegex(
            self.body,
            r"(?is)(2|two).{0,40}(re-?judgment|re-?vet|re-?check|cycle)",
        )
        self.assertRegex(
            self.body,
            r"(?is)(stop|halt).{0,40}(human|user)|"
            r"(human|user).{0,40}(stop|halt|rather than thrash)",
        )

    def test_VPF_6_7_non_code_grounded_taste_not_loop(self):
        """VPF-6.7 — non-code-grounded / taste items do not keep the loop alive."""
        self.assertRegex(
            self.body,
            r"(?is)(non-?code-?grounded|not code-?grounded|taste).{0,100}"
            r"(loop|fix loop|keep)|"
            r"(loop|fix loop).{0,80}(non-?code|taste|outside the skill claim)",
        )

    def test_VPF_1_5_reassert_no_run_file_write_during_judgment(self):
        """VPF-1.5 reassert — judgment does not write the run file (guide-gap is separate)."""
        self.assertRegex(
            self.body,
            r"(?is)(judgment|vet pass|during judgment).{0,100}"
            r"(read-?only|unmodified|do not (write|modify|patch|mutate)).{0,40}"
            r"(run.?file)|"
            r"(run.?file).{0,60}(unmodified|read-?only).{0,80}"
            r"(judgment|vet)",
        )


class VetProductFlowScenarios(unittest.TestCase):
    """Scenario markdown expanded for stories 1–3 + guide-gap (Tasks 2–3)."""

    def test_scenarios_and_pressure_exist(self):
        """Stories 1–3 behavioral coverage files present."""
        self.assertTrue(SCENARIOS.exists())
        self.assertTrue(PRESSURE.exists())
        s = SCENARIOS.read_text()
        p = PRESSURE.read_text()
        for token in (
            "VPF-1.1",
            "VPF-1.2",
            "VPF-1.5",
            "VPF-2.1",
            "VPF-2.6",
            "VPF-3.1",
            "VPF-3.5",
        ):
            self.assertIn(token, s)
        # Pressure scenarios mention same-agent / mechanical / chaos pressures
        self.assertRegex(p, r"(?i)same.?agent|rubber.?stamp")
        self.assertRegex(p, r"(?i)mechanical|complete for real|false confidence")
        self.assertRegex(p, r"(?i)chaos|load|race|fuzz")

    def test_VPF_6_scenarios_guide_gap_behavioral(self):
        """VPF-6.2–6.7 — Story 6 scenarios carry behavioral bullets."""
        s = SCENARIOS.read_text()
        for token in (
            "VPF-6.2",
            "VPF-6.3",
            "VPF-6.4",
            "VPF-6.5",
            "VPF-6.6",
            "VPF-6.7",
        ):
            self.assertIn(token, s)
        self.assertRegex(
            s,
            r"(?is)VPF-6\.2.{0,200}(severity|run file|re-?render)",
        )
        self.assertRegex(
            s,
            r"(?is)VPF-6\.5.{0,200}(≥\s*5|>=\s*5|fixer|ability)",
        )
        self.assertRegex(
            s,
            r"(?is)VPF-6\.6.{0,200}(2|two).{0,40}(cycle|re-?judgment|re-?vet)",
        )


if __name__ == "__main__":
    unittest.main()
