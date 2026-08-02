"""VPF skill body contracts — isolation, map, non-claims, report, guide-gap,
author hand-off, walkthrough hard gate, product-defect isolation.

VPF-1.1 VPF-1.2 VPF-1.3 VPF-1.4 VPF-1.5 VPF-2.1 VPF-2.2 VPF-2.3 VPF-2.4
VPF-2.5 VPF-2.6 VPF-3.1 VPF-3.2 VPF-3.3 VPF-3.4 VPF-3.5 VPF-4.1 VPF-4.2
VPF-4.3 VPF-5.1 VPF-5.2 VPF-5.3 VPF-5.4 VPF-5.5 VPF-5.6 VPF-6.1 VPF-6.2
VPF-6.3 VPF-6.4 VPF-6.5 VPF-6.6 VPF-6.7 VPF-7.1 VPF-7.2 VPF-7.3 VPF-7.4
VPF-7.5 VPF-8.1
"""
from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "acceptance" / "vet-product-flow" / "SKILL.md"
RPF_SKILL = REPO / "skills" / "acceptance" / "review-product-flow" / "SKILL.md"
RPW_SKILL = (
    REPO / "skills" / "acceptance" / "run-product-walkthrough" / "SKILL.md"
)
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
        """VPF-1.3 — report path `.skills/<CODE>/vet-product-flow.md` + stamp fields."""
        self.assertIn(".skills/<CODE>/vet-product-flow.md", self.body)
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


class ReviewProductFlowAuthorHandoff(unittest.TestCase):
    """VPF-4.1–4.3 — review-product-flow §5 names vet; guards §1 + render SSOT."""

    def setUp(self):
        self.assertTrue(RPF_SKILL.exists(), f"missing {RPF_SKILL}")
        self.text = RPF_SKILL.read_text()
        self.body = _body(self.text)

    def _section5(self) -> str:
        """Extract Hand over / §5 through next ## or end."""
        m = re.search(
            r"(?is)##\s*5\.\s*Hand over\b(.*?)(?=\n##\s|\Z)",
            self.body,
        )
        self.assertIsNotNone(m, "§5 Hand over section missing")
        return m.group(0)

    def test_VPF_4_1_required_next_vet_before_dogfood(self):
        """VPF-4.1 — §5 names vet-product-flow as required next before agent dogfood."""
        sec5 = self._section5()
        self.assertIn("vet-product-flow", sec5)
        self.assertRegex(
            sec5,
            r"(?is)required next|next required",
        )
        self.assertRegex(
            sec5,
            r"(?is)(before|until).{0,80}(dogfood|run-product-walkthrough)|"
            r"(dogfood|run-product-walkthrough).{0,80}(after|only after|vet)",
        )
        # Ordered: walkthrough only after vet (not as immediate alternative)
        self.assertRegex(
            sec5,
            r"(?is)(only after|after).{0,60}(vet|clean|report)|"
            r"vet-product-flow.{0,200}run-product-walkthrough",
        )

    def test_VPF_4_2_coverage_gate_and_taxonomy_guard(self):
        """VPF-4.2 — §1 coverage gate and seven-kind taxonomy still present."""
        self.assertRegex(self.body, r"(?i)##\s*1\.\s*Scope|coverage gate")
        self.assertRegex(
            self.body,
            r"(?is)Coverage rules|Every user-facing requirement",
        )
        # Seven kinds in taxonomy
        for kind in (
            "happy",
            "edge",
            "error",
            "nonbehavior",
            "persist",
            "visual",
            "journey",
        ):
            self.assertIn(kind, self.body)
        # Coverage self-check remains (not removed by hand-off rewrite)
        self.assertRegex(
            self.body,
            r"(?i)Coverage self-check|count cases by `kind`",
        )

    def test_VPF_4_3_run_file_ssot_and_render_shell(self):
        """VPF-4.3 — run file SSOT and render shell path still present."""
        self.assertRegex(
            self.body,
            r"(?is)Authoring SSOT is the run file|run file.*SSOT|SSOT.*run file",
        )
        self.assertRegex(
            self.body,
            r"review-product-flow\s+render",
        )
        self.assertRegex(
            self.body,
            r"(?i)shell/guide\.html|checked-in shell",
        )
        self.assertRegex(
            self.body,
            r"(?is)(not|do not|never).{0,40}(craft-page|invent)",
        )

    def test_VPF_4_self_check_not_vet_rationalization(self):
        """VPF-4.1/4.2 — rationalization: coverage self-check ≠ vet."""
        self.assertRegex(self.body, r"(?i)\|\s*Thought\s*\|\s*Reality\s*\|")
        self.assertRegex(
            self.body,
            r"(?is)(self-?check|coverage self).{0,80}(not|≠|is not).{0,40}vet|"
            r"vet.{0,60}(not|≠|is not).{0,40}(self-?check|§\s*4|coverage)|"
            r"(self-?check).{0,40}(substitute|replacement).{0,40}vet|"
            r"not a substitute for vet",
        )


class VetProductFlowScenarios(unittest.TestCase):
    """Scenario markdown expanded for stories 1–3 + guide-gap + hand-off."""

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

    def test_VPF_4_scenarios_author_handoff_behavioral(self):
        """VPF-4.1–4.3 — Story 4 scenarios carry behavioral bullets."""
        s = SCENARIOS.read_text()
        for token in ("VPF-4.1", "VPF-4.2", "VPF-4.3"):
            self.assertIn(token, s)
        self.assertRegex(
            s,
            r"(?is)VPF-4\.1.{0,200}(required next|vet-product-flow|dogfood)",
        )
        self.assertRegex(
            s,
            r"(?is)VPF-4\.2.{0,200}(coverage|taxonomy|seven-?kind|§\s*1)",
        )
        self.assertRegex(
            s,
            r"(?is)VPF-4\.3.{0,200}(SSOT|run file|render|shell)",
        )

    def test_VPF_5_scenarios_walkthrough_gate_behavioral(self):
        """VPF-5.1–5.6 VPF-6.1 — Story 5 scenarios carry behavioral bullets."""
        s = SCENARIOS.read_text()
        for token in (
            "VPF-5.1",
            "VPF-5.2",
            "VPF-5.3",
            "VPF-5.4",
            "VPF-5.5",
            "VPF-5.6",
            "VPF-6.1",
        ):
            self.assertIn(token, s)
        self.assertRegex(
            s,
            r"(?is)VPF-5\.1.{0,250}(fresh|cases_fingerprint|run_file|rev)",
        )
        self.assertRegex(
            s,
            r"(?is)VPF-5\.3.{0,250}(names?|override|progress\.md|greppable)",
        )
        self.assertRegex(
            s,
            r"(?is)VPF-6\.1.{0,200}(block|open finding|severity)",
        )
        p = PRESSURE.read_text()
        self.assertRegex(
            p,
            r"(?is)((just go|demo in).{0,200}(stop|name|VPF-|override)|"
            r"P-GATE|walkthrough gate)",
        )


class RunProductWalkthroughHardGate(unittest.TestCase):
    """VPF-5.1–5.6 VPF-6.1 — hard gate before any product case drive."""

    def setUp(self):
        self.assertTrue(RPW_SKILL.exists(), f"missing {RPW_SKILL}")
        self.text = RPW_SKILL.read_text()
        self.body = _body(self.text)

    def test_VPF_5_1_require_fresh_vet_report_before_drive(self):
        """VPF-5.1 — fresh .skills/<CODE>/vet-product-flow.md before drive."""
        self.assertIn(".skills/<CODE>/vet-product-flow.md", self.body)
        self.assertRegex(
            self.body,
            r"(?is)vet-product-flow",
        )
        self.assertRegex(
            self.body,
            r"(?is)(before|prior to).{0,80}(drive|product (case|click))|"
            r"(no product|not drive).{0,80}(until|before).{0,40}(gate|vet|report)",
        )
        # Freshness = run_file + cases_fingerprint, not whole-file rev
        self.assertIn("cases_fingerprint", self.body)
        self.assertIn("run_file", self.body)
        self.assertRegex(
            self.body,
            r"(?is)(not|≠|!=).{0,40}\brev\b|"
            r"\brev\b.{0,60}(not|does not|never).{0,40}(fresh|freshness)|"
            r"fingerprint.{0,40}(not|≠).{0,40}\brev\b|"
            r"not whole-file.?`?rev`?",
        )

    def test_VPF_5_2_5_3_open_findings_named_override_trail(self):
        """VPF-5.2 VPF-5.3 — open findings block unless yes names each VPF-N; trail."""
        self.assertRegex(
            self.body,
            r"(?is)open finding",
        )
        self.assertRegex(
            self.body,
            r"(?is)(names?|naming).{0,40}(each|every|all).{0,40}(open )?(VPF-N|finding)|"
            r"(each|every).{0,40}open.{0,40}(VPF-N|finding).{0,40}(name|yes)",
        )
        self.assertRegex(
            self.body,
            r"(?is)\.skills/progress\.md|progress\.md",
        )
        self.assertRegex(
            self.body,
            r"(?is)(override|VPF override)",
        )
        # Bare "just go" is not enough
        self.assertRegex(
            self.body,
            r"(?is)just go|bare.{0,20}(yes|go)|silent skip",
        )

    def test_VPF_5_4_6_1_every_open_blocks_severity_does_not_soften(self):
        """VPF-5.4 VPF-6.1 — every open finding blocks; severity never softens gate."""
        self.assertRegex(
            self.body,
            r"(?is)(every|all).{0,40}open.{0,40}(finding|block)|"
            r"(severity|does not|never).{0,40}(soften|drop|reintroduce|critical.?only)",
        )
        self.assertRegex(
            self.body,
            r"(?is)severity.{0,80}(not|never|does not).{0,60}(gate|block|soften|drop)|"
            r"(gate|block).{0,80}severity.{0,40}(not|never|orders? fix)",
        )

    def test_VPF_5_5_origin_consent_guard(self):
        """VPF-5.5 — origin consent still required before product click."""
        self.assertRegex(
            self.body,
            r"(?is)(origin|non-local).{0,80}(consent|explicit yes|naming)",
        )
        self.assertRegex(
            self.body,
            r"(?is)(before|prior).{0,40}(first product click|product click)|"
            r"product click",
        )

    def test_VPF_5_6_iron_law_mark_evidence_guard(self):
        """VPF-5.6 — Iron Law mark requires non-empty --saw and --server."""
        self.assertRegex(self.body, r"(?i)Iron Law")
        self.assertRegex(
            self.body,
            r"(?is)--saw|--server|`saw`|`server`",
        )
        self.assertRegex(
            self.body,
            r"(?is)presentational",
        )
        self.assertRegex(
            self.body,
            r"(?is)(refuses? empty|non-empty|both).{0,40}(saw|server)|"
            r"empty `--saw`|empty `--server`",
        )

    def test_VPF_5_init_may_seed_no_product_click_until_gate(self):
        """VPF-5.1 — init may seed pending; no product click / driven mark until gate."""
        self.assertRegex(
            self.body,
            r"(?is)init.{0,120}(seed|pending)|"
            r"(seed|pending).{0,80}init",
        )
        self.assertRegex(
            self.body,
            r"(?is)(no product click|not.{0,20}product click|"
            r"no `mark` of a driven).{0,80}(until|before).{0,40}gate|"
            r"gate.{0,80}(before|until).{0,40}(product click|drive)",
        )

    def test_VPF_5_stop_points_to_guide_gap_loop(self):
        """VPF-5.2 — on stop, cross-link guide-gap loop."""
        self.assertRegex(
            self.body,
            r"(?is)guide-gap|guide gap",
        )


class RunProductWalkthroughProductDefectIsolation(unittest.TestCase):
    """VPF-7.1–7.5 — product-defect isolation during dogfood (§4 Failure routing)."""

    def setUp(self):
        self.assertTrue(RPW_SKILL.exists(), f"missing {RPW_SKILL}")
        self.body = _body(RPW_SKILL.read_text())
        # Scope asserts to §4 Failure routing when possible
        m = re.search(
            r"(?is)##\s*4\.\s*Failure routing(.+?)(?=\n##\s+\d|\Z)",
            self.body,
        )
        self.section4 = m.group(1) if m else self.body

    def test_VPF_7_1_master_owns_selection_evidence_mark_retest(self):
        """VPF-7.1 — master owns case selection, evidence, mark, re-test."""
        s = self.section4
        self.assertRegex(
            s,
            r"(?is)\bmaster\b.{0,80}(own|mark|re-?test|select|evidence)|"
            r"(own|keep).{0,40}\bmaster\b",
        )
        # Master marks fail with evidence (not subagent)
        self.assertRegex(
            s,
            r"(?is)master.{0,80}(mark|evidence)|"
            r"mark.{0,40}fail.{0,40}evidence",
        )
        self.assertRegex(
            s,
            r"(?is)re-?test|re-?drive",
        )

    def test_VPF_7_2_subagent_brief_red_capable_not_full_history(self):
        """VPF-7.2 — subagent brief: repro, saw/server, case id, req — not full history."""
        s = self.section4
        self.assertRegex(s, r"(?is)subagent")
        self.assertRegex(
            s,
            r"(?is)brief",
        )
        # Red-capable brief contents
        for token in (r"repro", r"case id|case.?id|`?id`?", r"\breq\b"):
            self.assertRegex(s, rf"(?is){token}")
        self.assertRegex(
            s,
            r"(?is)saw|server",
        )
        # Not full session history
        self.assertRegex(
            s,
            r"(?is)(not|without|never).{0,60}(full|whole|entire).{0,40}"
            r"(session|history|context)|"
            r"(not|without).{0,40}(session history|full history|"
            r"whole session|long dogfood)",
        )

    def test_VPF_7_3_master_redrives_failed_and_related_pass_on_done(self):
        """VPF-7.3 — on DONE master re-drives failed + already-pass whose req fix touched."""
        s = self.section4
        self.assertRegex(
            s,
            r"(?is)(DONE|done|fixed|reports? fixed).{0,120}(re-?drive|master)|"
            r"(re-?drive|master).{0,120}(DONE|done|fixed)",
        )
        self.assertRegex(
            s,
            r"(?is)(failed case|re-?drive the failed)",
        )
        self.assertRegex(
            s,
            r"(?is)already-?`?pass`?.{0,80}(req|fix)|"
            r"(req|fix).{0,80}already-?`?pass`?",
        )

    def test_VPF_7_4_subagent_still_root_cause_and_test_first(self):
        """VPF-7.4 — subagent still uses root-cause (+ test-first); isolation ≠ free patch."""
        s = self.section4
        self.assertRegex(
            s,
            r"(?is)root-cause|`root-cause`",
        )
        self.assertRegex(
            s,
            r"(?is)test-first|TDD",
        )
        self.assertRegex(
            s,
            r"(?is)(subagent|isolation).{0,100}(root-cause|test-first)|"
            r"root-cause.{0,80}(subagent|isolat)|"
            r"(not|≠|!=|never).{0,40}(free|skip).{0,40}(patch|root-cause)|"
            r"isolation.{0,60}(not|≠).{0,40}(free|patch)",
        )

    def test_VPF_7_5_guide_gap_loop_separate_from_product_defect(self):
        """VPF-7.5 — guide-gap loop separate from product-defect dogfood loop."""
        s = self.section4
        self.assertRegex(
            s,
            r"(?is)guide-gap|guide gap",
        )
        self.assertRegex(
            s,
            r"(?is)(separate|not routed|do not absorb|not.{0,40}product defect)|"
            r"(product defect).{0,80}(not|never).{0,60}(guide-gap|guide gap)|"
            r"(guide-gap|guide gap).{0,80}(separate|not).{0,60}"
            r"(product.?defect|this loop|routed here)",
        )

    def test_VPF_7_preserve_flaky_guide_wrong_and_precondition_rows(self):
        """Guards — flaky/guide-wrong and precondition-stop rows remain."""
        s = self.section4
        self.assertRegex(
            s,
            r"(?is)flaky|guide wrong|guide-wrong",
        )
        self.assertRegex(
            s,
            r"(?is)(run file|authored).{0,60}(fix|edit)|"
            r"fix.{0,40}(run file|authored)",
        )
        self.assertRegex(
            s,
            r"(?is)precondition|server down|login",
        )
        self.assertRegex(
            s,
            r"(?is)stop the run|leave remaining|pending|blocked",
        )


class VetProductFlowStory7Scenarios(unittest.TestCase):
    """VPF-7.1–7.5 — Story 7 scenarios carry behavioral bullets."""

    def test_VPF_7_scenarios_product_defect_isolation_behavioral(self):
        """VPF-7.1–7.5 — Story 7 scenarios expand isolation bullets."""
        s = SCENARIOS.read_text()
        for token in (
            "VPF-7.1",
            "VPF-7.2",
            "VPF-7.3",
            "VPF-7.4",
            "VPF-7.5",
        ):
            self.assertIn(token, s)
        self.assertRegex(
            s,
            r"(?is)VPF-7\.1.{0,200}(master|selection|evidence|mark|re-?test)",
        )
        self.assertRegex(
            s,
            r"(?is)VPF-7\.2.{0,200}(subagent|brief|repro|not.{0,40}(full|session))",
        )
        self.assertRegex(
            s,
            r"(?is)VPF-7\.3.{0,200}(re-?drive|DONE|already-?pass|req)",
        )
        self.assertRegex(
            s,
            r"(?is)VPF-7\.4.{0,200}(root-cause|test-first)",
        )
        self.assertRegex(
            s,
            r"(?is)VPF-7\.5.{0,200}(separate|guide-gap|product.?defect)",
        )


# --- Task 7: inventory + human guide + trigger routing (VPF-1.1 packaging) ---

AGENTS = REPO / "AGENTS.md"
README = REPO / "README.md"
PLUGIN = REPO / ".claude-plugin" / "plugin.json"
MARKET = REPO / ".claude-plugin" / "marketplace.json"
SKILLS_DOC = REPO / "docs" / "architecture" / "skills.md"
SYSTEM_DOC = REPO / "docs" / "architecture" / "system.md"
WORKFLOWS_DOC = REPO / "docs" / "architecture" / "workflows.md"
GUIDE = REPO / "docs" / "guide" / "skills" / "vet-product-flow.md"
TRIGGER = REPO / "tests" / "trigger" / "vet-product-flow-routing.md"
TRIPLE_TRIGGER = REPO / "tests" / "trigger" / "run-product-walkthrough-routing.md"
PROJECT_MD = REPO / "docs" / "agents" / "project.md"


class VetProductFlowWiring(unittest.TestCase):
    """VPF-1.1 — discoverability: inventory, guide, triggers, plugin."""

    def test_VPF_1_1_agents_acceptance_lists_model_invoked(self):
        """VPF-1.1 — AGENTS.md acceptance row lists vet-product-flow (m)."""
        agents = AGENTS.read_text()
        self.assertRegex(
            agents,
            r"(?is)acceptance.*vet-product-flow|vet-product-flow.*\(m\)",
        )
        # Explicit model-invoked mark near the name in the acceptance inventory
        self.assertRegex(
            agents,
            r"`vet-product-flow`\s*\(m\)",
        )
        # Skill count header stays accurate (engineering dirs include this skill)
        m = re.search(r"(\d+)\s+skills across", agents)
        self.assertIsNotNone(m, "AGENTS.md skill count banner missing")
        eng = [
            p
            for p in (REPO / "skills").glob("*/*/SKILL.md")
            if "personal" not in p.parts
        ]
        self.assertEqual(
            int(m.group(1)),
            len(eng),
            f"AGENTS.md says {m.group(1)} skills but engineering dirs={len(eng)}",
        )

    def test_VPF_1_1_architecture_skills_and_system(self):
        """VPF-1.1 — docs/architecture skills.md + system.md inventory."""
        self.assertIn("vet-product-flow", SKILLS_DOC.read_text())
        self.assertIn("vet-product-flow", SYSTEM_DOC.read_text())
        self.assertRegex(
            SYSTEM_DOC.read_text(),
            r"acceptance/.*vet-product-flow",
        )

    def test_VPF_1_1_workflows_author_vet_walkthrough(self):
        """VPF-1.1 — workflows.md chains author → vet → walkthrough when dogfooding."""
        w = WORKFLOWS_DOC.read_text()
        self.assertIn("vet-product-flow", w)
        self.assertRegex(
            w,
            r"(?is)review-product-flow.{0,120}vet-product-flow|"
            r"author.{0,40}vet.{0,40}walkthrough|"
            r"vet-product-flow.{0,120}run-product-walkthrough",
        )

    def test_VPF_1_1_readme_acceptance_roster(self):
        """VPF-1.1 — README.md acceptance roster names vet-product-flow."""
        self.assertIn("vet-product-flow", README.read_text())

    def test_VPF_1_1_plugin_manifests_register_skill(self):
        """VPF-1.1 — plugin.json and marketplace.json list the skill path."""
        for manifest in (PLUGIN, MARKET):
            body = manifest.read_text()
            self.assertIn(
                "./skills/acceptance/vet-product-flow",
                body,
                f"{manifest.name} missing vet-product-flow",
            )
            json.loads(body)  # valid JSON

    def test_VPF_1_1_human_guide_exists(self):
        """VPF-1.1 — docs/guide/skills/vet-product-flow.md present."""
        self.assertTrue(GUIDE.exists(), f"missing {GUIDE}")
        g = GUIDE.read_text()
        self.assertIn("vet-product-flow", g)
        self.assertRegex(g, r"(?i)model-invoc")

    def test_VPF_1_1_trigger_routing_should_fire_and_not(self):
        """VPF-1.1 — trigger file: should-fire vet; not author/drive/Playwright."""
        self.assertTrue(TRIGGER.exists(), f"missing {TRIGGER}")
        t = TRIGGER.read_text()
        self.assertRegex(t, r"(?i)should-?fire")
        self.assertIn("vet-product-flow", t)
        # Peer disambiguators
        self.assertIn("review-product-flow", t)
        self.assertIn("run-product-walkthrough", t)
        self.assertIn("validate-ui", t)
        # Should-fire cues for vet (finished guide / missing situations / before dogfood)
        self.assertRegex(
            t,
            r"(?is)(missing.?situation|before dogfood|vet the guide|"
            r"complete for the implementation|isolat)",
        )
        # Should-not / prefer author, drive, Playwright
        self.assertRegex(
            t,
            r"(?is)(should-?not|must not|prefer|→\s*`?review-product-flow)",
        )
        self.assertRegex(
            t,
            r"(?is)(author|produce|write).{0,80}(guide|cases)|"
            r"review-product-flow",
        )
        self.assertRegex(
            t,
            r"(?is)(drive|execute|walkthrough)|run-product-walkthrough",
        )
        self.assertRegex(
            t,
            r"(?is)(Playwright|e2e)|validate-ui",
        )

    def test_VPF_1_1_triple_routing_names_vet_disambiguator(self):
        """VPF-1.1 — run-product-walkthrough-routing.md mentions vet-product-flow."""
        self.assertTrue(TRIPLE_TRIGGER.exists())
        text = TRIPLE_TRIGGER.read_text()
        self.assertIn("vet-product-flow", text)

    def test_VPF_1_1_audit_trace_docs_only_or_legacy_ignore(self):
        """VPF-1.1 — docs-only audit-trace (DOSP) or legacy ignore list for fixtures."""
        p = PROJECT_MD.read_text()
        docs_only = "docs-only" in p.lower() and "does not grep" in p.lower()
        legacy = (
            "tests/vet-product-flow/fixtures/" in p
            and "tests/trigger/vet-product-flow-routing.md" in p
            and "tests/vet-product-flow/scenarios-pressure.md" in p
        )
        self.assertTrue(
            docs_only or legacy,
            "project.md must document docs-only audit-trace or list VPF fixture ignores",
        )


# --- Task 8: full-suite close — every approved VPF-N.M in scenarios.md ---

REQUIREMENTS = (
    REPO / "docs" / "specs" / "2026-08-01-vet-product-flow" / "requirements.md"
)


class VetProductFlowScenarioCompleteness(unittest.TestCase):
    """Suite close — every bold VPF-N.M from requirements appears in scenarios."""

    def test_VPF_all_requirement_ids_appear_in_scenarios(self):
        """All VPF-N.M — every bold ID in requirements.md appears in scenarios.md."""
        self.assertTrue(REQUIREMENTS.exists(), f"missing {REQUIREMENTS}")
        self.assertTrue(SCENARIOS.exists(), f"missing {SCENARIOS}")
        req = REQUIREMENTS.read_text()
        scenarios = SCENARIOS.read_text()
        # Bold EARS markers only: **VPF-N.M** (not bare mentions in prose)
        ids = sorted(set(re.findall(r"\*\*(VPF-\d+\.\d+)\*\*", req)))
        self.assertGreaterEqual(
            len(ids),
            30,
            f"expected full VPF set from requirements.md, found {len(ids)}: {ids}",
        )
        missing = [rid for rid in ids if rid not in scenarios]
        self.assertEqual(
            missing,
            [],
            f"scenarios.md missing requirement IDs: {missing}",
        )


if __name__ == "__main__":
    unittest.main()
