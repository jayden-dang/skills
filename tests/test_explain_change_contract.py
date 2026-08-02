"""brief-team: packet substance, slug determinism, post-write verification.

Covers the 2026-07-30 tier-1 mini-spec (XPLN-2.10–2.14, 3.7–3.10, 5.8) plus the
deterministic delivery of XPLN-3.4's INDEX row, which the requirement already
demanded and the skill text under-specified.
"""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ROOT = REPO / "skills" / "review" / "brief-team"
SKILL = ROOT / "SKILL.md"
CONTRACT = ROOT / "references" / "section-contract.md"
SHELL = ROOT / "shell" / "packet.html"

SIX_SECTIONS = ("users", "decisions", "breaks", "prove-claim", "intuition", "seams")


class ExplainChangeIndexRow(unittest.TestCase):
    """XPLN-3.4 delivery: 'upsert exactly one INDEX row' is only deterministic
    if the row's shape is pinned. The requirement lists the fields; without a
    fixed column order and a stated match key, each run re-invents the table and
    'upsert' against a differently-shaped prior file is undefined."""

    def setUp(self):
        self.text = SKILL.read_text()

    def test_XPLN_3_4_index_row_has_a_fixed_column_order(self):
        """A fenced example pins the header row verbatim, so a later run can
        match the file it finds instead of guessing a layout."""
        self.assertIn("docs/explainers/INDEX.md", self.text)
        self.assertRegex(
            self.text,
            r"\|\s*Slug\s*\|\s*Title\s*\|\s*Path\s*\|\s*Range\s*\|\s*Generated\s*\|",
            msg="no fixed INDEX header row (| Slug | Title | Path | Range | Generated |)",
        )

    def test_XPLN_3_4_upsert_names_its_match_key(self):
        """Upsert is replace-or-append keyed on one cell. Unstated, the agent
        may append a duplicate row for a slug that already has one."""
        self.assertRegex(
            self.text,
            r"(?s)match(?:ing|es)?\s+on\s+the\s+`?Slug`?\s+cell",
            msg="INDEX upsert does not name the Slug cell as its match key",
        )


class ExplainChangeSlugDeterminism(unittest.TestCase):
    """XPLN-3.7 — the slug fallback must run on mechanical inputs only. XPLN-3.1
    already promised 'deterministically', but 'a short range summary' is a
    model-authored string: two runs over one range can produce two slugs, and
    the XPLN-3.2 overwrite-canonical contract silently becomes create-a-sibling."""

    def setUp(self):
        self.text = SKILL.read_text()
        start = self.text.find("## Slug resolver")
        self.assertNotEqual(start, -1, "## Slug resolver section heading not found")
        end = self.text.find("\n## ", start + 1)
        self.section = self.text[start:end if end != -1 else len(self.text)]

    def test_XPLN_3_7_ladder_rungs_are_ordered_and_mechanical(self):
        """Every rung reads a value off git or a registry file; none summarizes."""
        rungs = [
            "user-supplied",
            "feature code",
            "docs/specs/",
            "branch",
            "<base7>-<head7>",
        ]
        # Case-folded: rung labels open a list item, so they are capitalized.
        haystack = self.section.lower()
        positions = [haystack.find(r) for r in rungs]
        self.assertNotIn(-1, positions, f"missing slug rung among {rungs}")
        self.assertEqual(positions, sorted(positions), "slug ladder rungs out of order")

    def test_XPLN_3_7_model_authored_summary_is_forbidden(self):
        """The banned input is named, not merely omitted — the old text actively
        invited it ('a short range summary')."""
        # Bounded by the sentence (no `.`) rather than the line, so an 80-column
        # reflow between the negation and its object cannot break the assertion.
        self.assertRegex(
            self.section,
            r"(?i)(never|not|forbidden)[^.]{0,80}(summar|paraphras|invent)",
            msg="slug resolver does not forbid a model-authored summary",
        )

    def test_XPLN_3_7_sanitization_is_explicit(self):
        """A character allow-list plus a numeric length bound, matching the
        package-change stable-id convention — branch names legally carry shell
        metacharacters, so 'kebab-case' alone leaves the value ambiguous."""
        self.assertRegex(self.section, r"\[?a-z0-9-\]?", msg="no [a-z0-9-] allow-list")
        self.assertRegex(self.section, r"\b\d+ characters\b", msg="no numeric length bound")

    def test_XPLN_3_7_last_rung_always_resolves(self):
        """The ladder must terminate without asking: a commit-sha pair always
        exists for a resolved range, so no run falls off the end into a guess."""
        self.assertRegex(
            self.section,
            r"(?s)<base7>-<head7>[^\n]*\n?[^\n]*(always|never fails|terminat)",
            msg="final slug rung is not stated as total",
        )


class ExplainChangePostWriteVerification(unittest.TestCase):
    """XPLN-3.8 — the shell renders whatever it is handed. A failed injection
    produced a plausible-looking page, and the pipeline ended at 'report the
    path' with nothing between writing and claiming success."""

    def setUp(self):
        self.text = SKILL.read_text()

    def test_XPLN_3_8_verification_step_exists_before_handoff(self):
        """The check sits between Write and Write Handoff, not after the claim."""
        write = self.text.find("**Write**")
        verify = self.text.find("**Verify the written file**")
        handoff = self.text.find("**Write Handoff**")
        self.assertNotEqual(write, -1, "Write phase not found")
        self.assertNotEqual(verify, -1, "no 'Verify the written file' phase")
        self.assertNotEqual(handoff, -1, "Write Handoff phase not found")
        self.assertLess(write, verify, "verification precedes the write")
        self.assertLess(verify, handoff, "verification runs after the write-handoff claim")

    def test_XPLN_3_8_verification_is_a_grep_recipe_not_prose(self):
        """author-skills:41 — a check that must never be misjudged is a fixed
        pass over a named input plus a fixed rule on its output. 'Confirm the
        packet looks complete' invites interpretation; a grep does not."""
        start = self.text.find("**Verify the written file**")
        end = self.text.find("**Write Handoff**")
        section = self.text[start:end]
        self.assertIn("grep", section, "verification names no grep pass")
        self.assertIn("__PACKET_DATA__", section, "injection marker not checked")
        # The recipe is a grep pattern, so the dot is backslash-escaped there.
        # Accept either form rather than pinning the escaping style.
        self.assertRegex(
            section,
            r"window\\?\.__PACKET__",
            msg="verification does not confirm the packet assignment landed",
        )

    def test_XPLN_2_11_verification_covers_all_six_section_bodies(self):
        """A packet can carry the real title and still leave a section empty;
        XPLN-2.11 makes that unfilled, so the pass must reach every section."""
        start = self.text.find("**Verify the written file**")
        end = self.text.find("**Write Handoff**")
        section = self.text[start:end]
        for name in SIX_SECTIONS:
            self.assertIn(
                name, section,
                f"section '{name}' not covered by the post-write verification",
            )

    def test_XPLN_3_9_orphan_html_is_named_in_the_failure_report(self):
        """XPLN-3.9 — XPLN-3.6 forbade presenting a partial path as success but
        said nothing about the file already on disk: HTML written, INDEX upsert
        failed, and the residue went unmentioned."""
        self.assertRegex(
            self.text,
            r"(?s)(orphan|incomplete output)",
            msg="write residue is never named",
        )
        self.assertRegex(
            self.text,
            r"(?s)INDEX[^\n]{0,120}fail[^.]{0,200}name[^.]{0,120}(path|file)",
            msg="INDEX-failure path does not require naming the written file",
        )

    def test_XPLN_3_9_write_order_is_pinned_html_then_index(self):
        """XPLN-3.9 — the residue rule only makes sense against a fixed order.
        Writing INDEX first would trade an orphan file for an INDEX row pointing
        at a path that does not exist, which is the worse of the two states
        because the registry is what a teammate reads first."""
        self.assertRegex(
            self.text,
            r"(?s)HTML first, then INDEX",
            msg="write order is not pinned",
        )

    def test_XPLN_3_10_overwrite_canonical_guard_survives(self):
        """XPLN-3.10 (guard) — the slug ladder is new machinery in front of the
        overwrite contract, so the contract itself must stay stated: a re-run
        lands on the same file, and history stays in git rather than in
        date-prefixed siblings."""
        self.assertRegex(
            self.text,
            r"(?i)OVERWRITE the canonical",
            msg="the overwrite-canonical rule is no longer a hard gate",
        )
        self.assertRegex(
            self.text,
            r"(?i)no date-prefixed tree",
            msg="the no-date-tree rule vanished",
        )
        start = self.text.find("## Slug resolver")
        end = self.text.find("\n## ", start + 1)
        section = self.text[start:end if end != -1 else len(self.text)]
        self.assertRegex(
            section,
            r"(?i)same (work|range)[^.]{0,80}same rung|re-run",
            msg="the slug resolver does not tie itself to re-run stability",
        )


class ExplainChangeVerificationIsNotAGate(unittest.TestCase):
    """XPLN-5.8 — adding a verification step to a skill whose Iron Law is
    'never a ship gate' opens the exact door TESTS.md recorded a baseline agent
    walking through ('You were explicit: block until it exists')."""

    def setUp(self):
        self.text = SKILL.read_text()

    def test_XPLN_5_8_hard_gate_names_the_non_gate_rule(self):
        self.assertRegex(
            self.text,
            r"(?s)(verification|verify)[^\n]{0,60}fail[^\n]{0,80}(NEVER|never)[^\n]{0,80}"
            r"(merge|PR|menu)|(NEVER|never)[^\n]{0,80}withhold[^\n]{0,80}"
            r"(verification|verify)",
            msg="no rule stating a failed verification still leaves merge/PR available",
        )

    def test_XPLN_5_8_rationalization_row_exists(self):
        """The prescribed counter-form for a rule an agent breaks under
        pressure — a row, verbatim in the thought's own voice."""
        start = self.text.find("## Rationalizations")
        end = self.text.find("## Red flags")
        self.assertNotEqual(start, -1, "Rationalizations heading not found")
        table = self.text[start:end]
        self.assertRegex(
            table,
            r'(?s)\|\s*"[^"]*(verif|placeholder|incomplete)[^"]*"',
            msg="no rationalization row covering a failed/partial packet",
        )

    def test_XPLN_5_8_red_flag_lists_the_symptom(self):
        start = self.text.find("## Red flags")
        end = self.text.find("## Pipeline")
        flags = self.text[start:end]
        self.assertRegex(
            flags,
            r"(?i)(gate|withhold|block|condition)",
            msg="red flags do not name gating as a symptom",
        )


class ExplainChangeSectionSubstance(unittest.TestCase):
    """XPLN-2.10 / XPLN-2.11 — six headings with one hollow line each satisfied
    the old contract by letter. The RED evidence in TESTS.md shows time pressure
    degrading the packet's form; a slot list with no substance bar leaves the
    same pressure a legal output."""

    def setUp(self):
        self.assertTrue(CONTRACT.exists(), "section-contract.md missing")
        self.text = CONTRACT.read_text()

    def test_XPLN_2_10_substance_bar_is_stated_per_slot(self):
        """Each section must carry specifics traceable to the range, not prose
        that would read the same for any change."""
        self.assertRegex(
            self.text,
            r"(?i)(substance|specific|concrete)",
            msg="no substance bar in the section contract",
        )
        self.assertRegex(
            self.text,
            r"(?s)(path|command|ID|commit)[^\n]{0,120}(cite|name|from the range)",
            msg="substance bar does not require range-derived specifics",
        )

    def test_XPLN_2_11_heading_restatement_is_forbidden(self):
        """The cheapest way to fill six slots under time pressure is to restate
        the heading; name that output as unfilled."""
        self.assertRegex(
            self.text,
            r"(?i)(restat|echo|repeat)[^\n]{0,80}heading|heading[^\n]{0,80}(restat|echo)",
            msg="heading-restatement is not named as an unfilled section",
        )

    def test_XPLN_2_11_unfilled_blocks_the_success_report(self):
        self.assertRegex(
            self.text,
            r"(?i)unfilled",
            msg="the contract never uses the unfilled verdict XPLN-2.11 defines",
        )

    def test_XPLN_2_12_six_slots_still_required_in_order(self):
        """XPLN-2.12 (guard) — tightening the contract must not disturb XPLN-2.4's
        slots or their order."""
        positions = [self.text.find(f"`{name}`") for name in SIX_SECTIONS]
        self.assertNotIn(-1, positions, "a required slot name vanished from the contract")
        self.assertEqual(positions, sorted(positions), "slot order changed")


class ExplainChangeShell(unittest.TestCase):
    """The shell is the last line of defence: it renders whatever it is handed,
    so a failed injection must look broken rather than plausible."""

    def setUp(self):
        self.text = SHELL.read_text()

    def test_XPLN_3_8_shell_carries_no_plausible_sample_packet(self):
        """The old fallback object supplied a real-looking title and six
        placeholder bodies, so a forgotten injection rendered a complete-looking
        explainer. No sample content may survive in the shipped shell."""
        self.assertNotIn(
            "Sample explainer", self.text,
            "shell still ships a sample packet that masks a failed injection",
        )
        self.assertNotRegex(
            self.text,
            r"(?i)placeholder\.?\"",
            msg="shell still ships placeholder section bodies",
        )

    def test_XPLN_3_8_shell_renders_an_incomplete_banner_without_data(self):
        """Absent packet data is a visible failure state, not an empty page that
        reads as a thin-but-real explainer."""
        self.assertRegex(
            self.text,
            r"(?s)if\s*\(\s*!\s*(window\.__PACKET__|PACKET)\s*\)",
            msg="shell has no missing-data branch",
        )
        self.assertRegex(
            self.text,
            r"(?i)incomplete output",
            msg="shell missing-data branch does not label the file incomplete output",
        )

    def test_XPLN_2_13_light_theme_media_query_is_reachable(self):
        """XPLN-2.13 (guard) — the shipped shell hardcoded data-theme="dark" on <html>, so the
        prefers-color-scheme block — whose selector requires the attribute to be
        absent — could never match. Dark stays the default through :root; the
        media query must be live for a light-preferring viewer."""
        self.assertRegex(
            self.text,
            r"<html[^>]*>",
            msg="no <html> tag found",
        )
        html_tag = re.search(r"<html[^>]*>", self.text).group(0)
        self.assertNotIn(
            'data-theme="dark"', html_tag,
            "hardcoded data-theme on <html> makes the light media query dead code",
        )
        self.assertIn("prefers-color-scheme: light", self.text)

    def test_XPLN_2_13_shell_makes_no_external_requests(self):
        """XPLN-2.13 (guard) — the packet must open offline. No remote origin may appear in
        the shell — not a font, not a stylesheet, not an image."""
        for needle in ("http://", "https://", "//fonts.", "cdn."):
            self.assertNotIn(needle, self.text, f"external reference '{needle}' in shell")

    def test_XPLN_2_12_shell_renders_all_six_sections(self):
        """XPLN-2.12 (guard) — every required slot still has a mount point."""
        for name in SIX_SECTIONS:
            self.assertIn(f'id="{name}"', self.text, f"section #{name} missing from shell")


class ExplainChangeSeparationDuplication(unittest.TestCase):
    """author-skills:62 duplication sweep — one home per rule. The no-quiz and
    non-gate rules each had four homes (Iron Law, hard gates, a rationalization
    row, plus a Separation table and a Neighbors paragraph). Rationalization rows
    and red flags are the exempt gate form; the two prose restatements are not."""

    def setUp(self):
        self.text = SKILL.read_text()

    def test_separation_table_removed(self):
        self.assertNotIn(
            "## Separation", self.text,
            "the Separation table restates rules already owned by the Iron Law "
            "and hard gates",
        )

    def test_XPLN_2_14_no_quiz_rule_survives_the_removal(self):
        """XPLN-2.14 (guard) — the deletion must not take the load-bearing rule
        with it."""
        self.assertRegex(
            self.text,
            r"(?i)NO QUIZ|no quiz",
            msg="the no-quiz rule disappeared along with the separation prose",
        )
        start = self.text.find("## Rationalizations")
        end = self.text.find("## Red flags")
        self.assertRegex(
            self.text[start:end],
            r"(?i)quiz",
            msg="no rationalization row counters the quiz temptation",
        )

    def test_neighbor_predicate_is_not_restated(self):
        """land-branch owns the naming predicate (multi_task / risk_hit /
        architecture_affecting). Mirroring it here creates two homes that drift."""
        self.assertNotRegex(
            self.text,
            r"(?s)multi-task[^\n]{0,80}risk glob[^\n]{0,120}architecture-affecting",
            msg="the land-branch naming predicate is restated in this skill",
        )


class ExplainChangeWritingSkillsForm(unittest.TestCase):
    """Ship checklist: line budget, phase completion criteria, reference depth."""

    def setUp(self):
        self.text = SKILL.read_text()

    def test_body_within_line_budget(self):
        lines = self.text.splitlines()
        self.assertLess(
            len(lines), 300,
            f"SKILL.md is {len(lines)} lines; 300 is the preferred ceiling",
        )

    def test_every_pipeline_phase_has_a_done_when(self):
        """author-skills:60 — a step without a checkable bound lets attention
        slip to being done. The shipped pipeline bounded only 4 of 11 steps."""
        start = self.text.find("## Pipeline")
        end = self.text.find("## Range resolver")
        self.assertNotEqual(start, -1, "## Pipeline heading not found")
        self.assertNotEqual(end, -1, "## Range resolver heading not found")
        pipeline = self.text[start:end]
        steps = re.findall(r"(?m)^\d+\.\s+\*\*", pipeline)
        dones = re.findall(r"\*\*Done when:\*\*", pipeline)
        self.assertGreaterEqual(
            len(dones), len(steps),
            f"{len(steps)} pipeline steps but only {len(dones)} 'Done when' bounds",
        )

    def test_references_are_one_level_deep(self):
        """A file reached only through another file gets skimmed, not read."""
        for ref in ROOT.glob("references/*.md"):
            self.assertIn(
                ref.name, self.text,
                f"{ref.name} is not pointed at from SKILL.md",
            )


if __name__ == "__main__":
    unittest.main()
