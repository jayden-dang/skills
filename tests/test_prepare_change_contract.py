"""package-change base resolution: declared, asked, never inferred from topology."""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILL = REPO / "skills" / "ship" / "package-change" / "SKILL.md"
TICKETS = REPO / "skills" / "ship" / "package-change" / "tickets.md"
CONV = REPO / "skills" / "ship" / "package-change" / "conventions.md"


class PrepareChangeBase(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text()

    def test_PCHG_2_1_2_2_2_3_2_4_ladder_in_order(self):
        """PCHG-2.1 PCHG-2.2 PCHG-2.3 PCHG-2.4 — four rungs, in order, ending in ask."""
        rungs = ["explicit base", "existing PR", "Default PR base:", "ask the user"]
        positions = [self.text.find(r) for r in rungs]
        self.assertNotIn(-1, positions, f"missing rung among {rungs}")
        self.assertEqual(positions, sorted(positions), "base ladder rungs out of order")

    def test_PCHG_2_6_no_topology_fallback(self):
        """PCHG-2.6 — origin/HEAD, main, master, and fork-point are named as forbidden."""
        self.assertRegex(
            self.text,
            r"(?s)NEVER[^\n]*origin/HEAD|SHALL NOT[^\n]*origin/HEAD|never[^\n]*origin/HEAD",
            msg="package-change does not forbid topology-based base selection",
        )
        for token in ("fork-point", "`main`", "`master`"):
            self.assertIn(token, self.text)

    def test_PCHG_2_7_writes_no_project_config(self):
        """PCHG-2.7 — the skill never writes docs/agents/project.md."""
        self.assertRegex(self.text, r"never writes? .{0,40}project\.md|writes no project configuration")

    def test_PCHG_2_5_head_equals_default_asks(self):
        """PCHG-2.5 — head == configured default always asks, invocation-scoped."""
        self.assertIn("head branch is the configured", self.text)
        self.assertIn("this invocation only", self.text)

    def test_PCHG_2_8_names_setup_repo_when_absent(self):
        """PCHG-2.8 — absent config continues session-only and names /configure-repo."""
        self.assertIn("/configure-repo", self.text)

    def test_PCHG_2_9_2_10_memoized_and_revalidated(self):
        """PCHG-2.9 PCHG-2.10 — memoized for the session; re-asked when it stops resolving."""
        self.assertIn("memoize", self.text.lower())
        self.assertIn("no longer resolves", self.text)

    def test_PCHG_2_9_manifest_field_distinct_from_config_field(self):
        """PCHG-2.9 — the manifest records the resolved value under `Base:`,
        never under the config field name `Default PR base:`, since the
        resolved value is a per-invocation value that may differ from the
        configured default."""
        self.assertRegex(self.text, r"manifest\s+as\s+`Base:`")
        self.assertNotRegex(self.text, r"manifest\s+as\s+`Default PR base:`")
        self.assertRegex(
            self.text,
            r"(?s)`Base:`.{0,120}resolved base for this invocation.{0,120}may differ from any configured `Default PR base:`",
        )


class PrepareChangeContext(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text()

    def test_PCHG_3_1_3_2_two_authorities(self):
        """PCHG-3.1 PCHG-3.2 — diff owns what changed; specs/ADRs/records own why."""
        self.assertIn("diff", self.text)
        self.assertRegex(self.text, r"(?s)what changed.{0,400}why")
        for src in ("docs/adr", "implementation-notes.md", "decision record"):
            self.assertIn(src, self.text)

    def test_PCHG_3_3_absent_context_omits_never_invents(self):
        """PCHG-3.3 — a missing why-source shortens the narrative, never fills it."""
        self.assertRegex(self.text, r"(?i)never invent")
        self.assertIn("omit", self.text.lower())

    def test_PCHG_3_4_loads_passive_data_contract_by_path(self):
        """PCHG-3.4 — passive-data contract is loaded from a sibling file, not
        restated, and not path-coupled into another skill's folder."""
        self.assertIn("passive-data-safety.md", self.text)
        self.assertNotIn(
            "skills/review/brief-team/references/passive-data-safety.md",
            self.text,
        )
        passive = REPO / "skills" / "ship" / "package-change" / "passive-data-safety.md"
        self.assertTrue(passive.exists(), "passive-data-safety.md missing beside SKILL.md")

    def test_PCHG_3_4_passive_data_rule_is_a_hard_gate(self):
        """PCHG-3.4 — the passive-data rule is wrapped in its own <HARD-GATE>
        block (or shares one with the REQUIRED-load directive), matching its
        neighbours (PCHG-3.3 omit-never-invent, PCHG-3.5 redaction), not left
        as bare prose next to the directive."""
        self.assertRegex(
            self.text,
            r"(?s)<HARD-GATE>((?!</HARD-GATE>).)*passive data((?!</HARD-GATE>).)*</HARD-GATE>",
            msg="passive-data rule is not wrapped in a <HARD-GATE> block",
        )

    def test_PCHG_3_5_secrets_redacted_by_class(self):
        """PCHG-3.5 — secrets become class-named placeholders."""
        self.assertIn("[redacted:", self.text)

    def test_PCHG_3_6_3_7_locator_rule(self):
        """PCHG-3.6 PCHG-3.7 — only reachable paths are linked; the rest is inlined."""
        self.assertIn("tracked and reachable", self.text)
        self.assertRegex(self.text, r"(?s)promote.{0,60}inline")
        self.assertIn(".skills/", self.text)


class PrepareChangeTickets(unittest.TestCase):
    def setUp(self):
        self.assertTrue(TICKETS.exists(), "tickets.md missing")
        self.text = TICKETS.read_text()

    def test_PCHG_5_1_5_2_reads_configured_tracker_and_hierarchy(self):
        """PCHG-5.1 PCHG-5.2 — tracker comes from config; branch IDs resolve hierarchy."""
        self.assertIn("docs/agents/issue-tracker.md", self.text)
        self.assertIn("sub-issue", self.text)
        self.assertIn("parent", self.text)

    def test_PCHG_5_3_5_4_5_5_completion_classification(self):
        """PCHG-5.3 PCHG-5.4 PCHG-5.5 — classify, then close only what is complete."""
        for token in ("fully completed", "partial", "related"):
            self.assertIn(token, self.text)
        self.assertRegex(self.text, r"(?s)partial.{0,200}without closing linkage")

    def test_PCHG_5_6_linkage_syntax_is_backend_specific(self):
        """PCHG-5.6 — no linkage syntax is assumed across backends."""
        self.assertRegex(self.text, r"(?i)never assume.{0,60}syntax|syntax of the configured backend")

    def test_PCHG_5_7_no_tracker_is_a_normal_state(self):
        """PCHG-5.7 — an unconfigured tracker yields an empty set, not a failure."""
        self.assertIn("empty ticket set", self.text)

    def test_PCHG_5_7_configured_tracker_with_no_resolvable_item(self):
        """PCHG-5.7 — a configured tracker that resolves to nothing (the
        branch name carries no tracker identifier, or the identifier it
        carries resolves to no item) is documented as a normal state that
        also yields an empty ticket set, distinct from the absent/
        unconfigured-tracker HARD-GATE pinned above. Scoped to the
        branch-resolution section rather than asserted whole-file, because
        'empty ticket set' already occurs once in the earlier
        absent-tracker gate — an unscoped assertIn would pass without this
        case ever being documented."""
        start = self.text.find("## Resolve the branch's items and their hierarchy")
        end = self.text.find("## Classify each resolved item against the diff")
        self.assertNotEqual(start, -1, "branch-resolution heading not found")
        self.assertNotEqual(end, -1, "classify heading not found")
        section = self.text[start:end]
        self.assertIn(
            "empty ticket set", section,
            "configured-tracker-but-unresolved case not documented in the "
            "branch-resolution section",
        )

    def test_PCHG_5_8_tracker_never_structures_the_body(self):
        """PCHG-5.8 — tracker content is bounded to four uses."""
        self.assertRegex(self.text, r"(?i)never structure.{0,60}body|not structured around")

    def test_PCHG_5_8_no_ticket_section_phrase(self):
        """PCHG-5.8 — tickets.md never dictates PR-body structure; PR-body
        placement is package-contract.md's domain, not this file's. The
        partial/related reference must not be pinned to a 'ticket section'
        of the PR body, which would contradict the HARD-GATE above that
        forbids structuring the PR body around tracker items."""
        self.assertNotIn("ticket section", self.text)


class PrepareChangeConventionGrading(unittest.TestCase):
    def setUp(self):
        self.assertTrue(CONV.exists(), "conventions.md missing")
        self.text = CONV.read_text()

    def test_PCHG_4_6_two_conventions_carry_two_independent_grades(self):
        """PCHG-4.6 — commit_subject_form and pr_structure resolve on two
        separate ladders (the commit-history ladder vs. the PR-template/
        guidance rule) and can land on different grades in the same
        session — e.g. commit convention `inferred` from a bounded sample
        while PR structure falls to the neutral `declared` fallback. One
        shared `grade` field cannot hold both outcomes, so the record must
        carry commit_subject_grade and pr_structure_grade independently.
        Scoped to the record-shape block at the top of the file (before the
        commit-ladder heading) so this doesn't pass merely because the word
        'grade' recurs throughout the rest of the file."""
        start = self.text.find("# Resolve conventions")
        end = self.text.find("## Commit convention: the three-rung ladder")
        self.assertNotEqual(start, -1, "conventions.md title heading not found")
        self.assertNotEqual(end, -1, "commit-ladder heading not found")
        section = self.text[start:end]
        for field in (
            "commit_subject_form",
            "commit_subject_grade",
            "pr_structure",
            "pr_structure_grade",
        ):
            self.assertIn(
                field, section,
                f"'{field}' missing from the record-shape block",
            )
        self.assertNotRegex(
            section,
            r"\{\s*commit_subject_form,\s*pr_structure,\s*grade\s*\}",
            msg="record literal still declares a single shared `grade` field",
        )


class PrepareChangeCommits(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text()

    def test_PCHG_1_1_1_2_group_then_size_down(self):
        """PCHG-1.1 PCHG-1.2 — group before committing; one coherent change stays one commit."""
        self.assertRegex(self.text, r"(?s)group.{0,200}before creating any commit")
        self.assertRegex(self.text, r"(?s)single coherent change.{0,120}one commit")

    def test_PCHG_1_3_six_validation_axes(self):
        """PCHG-1.3 — validation covers axes before each commit (DOSP: no ID trailers)."""
        start = self.text.find("5. **Author commits**")
        end = self.text.find("6. **Write package**")
        self.assertNotEqual(start, -1, "phase 5 (Author commits) heading not found")
        self.assertNotEqual(end, -1, "phase 6 (Write package) heading not found")
        phase5 = self.text[start:end]
        for axis in ("file scope", "subject", "body", "secret", "staging boundary"):
            self.assertIn(axis, phase5, f"'{axis}' axis missing from phase 5 (Author commits)")

    def test_PCHG_1_4_1_5_autonomous_with_five_exceptions(self):
        """PCHG-1.4 PCHG-1.5 — commits without plan approval; five stop conditions."""
        self.assertRegex(self.text, r"(?i)without requesting approval")
        for trigger in ("unrelated", "ownership", "partial-staging", "secret-risk", "mismatch"):
            self.assertIn(trigger, self.text)

    def test_PCHG_1_6_1_7_prose_leads_no_id_primary(self):
        """PCHG-1.6 PCHG-1.7 — subject explains change; IDs never primary (DOSP: no trailers)."""
        self.assertNotIn("`Implements:` / `Guards:` trailer\n   lines the commit carries, if any", self.text)
        self.assertRegex(self.text, r"(?i)never .{0,80}primary explanation")

    def test_PCHG_1_8_empty_tree_creates_nothing(self):
        """PCHG-1.8 — an empty working tree is valid and creates no commit."""
        self.assertRegex(self.text, r"(?s)no uncommitted tracked changes.{0,200}create no commit")

    def test_PCHG_1_9_untracked_excluded_by_default(self):
        """PCHG-1.9 — untracked files are excluded unless named this invocation."""
        self.assertIn("untracked", self.text)

    def test_PCHG_9_2_9_3_9_4_execute_plan_continuation(self):
        """PCHG-9.2 PCHG-9.3 PCHG-9.4 — task commits untouched; residue grouped; no extra approval."""
        self.assertIn("residue", self.text)
        self.assertRegex(self.text, r"(?s)implementer.{0,120}unmodified|task commits.{0,80}unmodified")


PKG = REPO / "skills" / "ship" / "package-change" / "package-contract.md"


class PrepareChangePackage(unittest.TestCase):
    def setUp(self):
        self.assertTrue(PKG.exists(), "package-contract.md missing")
        self.text = PKG.read_text()

    def test_PCHG_6_1_6_4_three_file_layout(self):
        """PCHG-6.1 PCHG-6.4 — manifest.md, title.txt, and body.md, with body.md reviewer-facing only."""
        self.assertIn(".skills/pr-packages/", self.text)
        self.assertIn("manifest.md", self.text)
        self.assertIn("title.txt", self.text)
        self.assertIn("body.md", self.text)
        self.assertRegex(self.text, r"(?s)body\.md.{0,200}reviewer-facing")

    def test_PCHG_6_2_stable_id_is_sanitized(self):
        """PCHG-6.2 — a raw branch name never reaches the path."""
        self.assertIn("stable-id", self.text)
        self.assertRegex(self.text, r"(?i)never .{0,60}raw branch name")

    def test_PCHG_6_3_manifest_field_list_complete(self):
        """PCHG-6.3 — every manifest field is named in the manifest field-list section."""
        start = self.text.find("## manifest.md field list")
        end = self.text.find("## body.md holds reviewer-facing content only")
        self.assertNotEqual(start, -1, "manifest field-list section heading not found")
        self.assertNotEqual(end, -1, "body.md section heading not found")
        fields = self.text[start:end].lower()
        for field in ("package version", "title", "base", "head", "ticket",
                      "commits", "advisory commit map", "findings",
                      "validation results", "digest"):
            self.assertIn(field, fields, f"'{field}' field missing from manifest field list")

    def test_PCHG_6_3_digest_uses_git_hash_object(self):
        """PCHG-6.3 — the digest is computed with git plumbing, not a shipped script."""
        self.assertIn("git hash-object", self.text)

    def test_PCHG_6_3_digest_recipe_uses_qualified_body_path(self):
        """PCHG-6.3 — the digest recipe's code block reads body.md by its
        fully qualified package path, never a bare relative filename. A
        bare `cat body.md` only resolves from inside the package directory;
        run from the repo root (the normal working directory) it fails on
        stderr while printf's bytes still reach git hash-object, silently
        hashing the title alone and printing a plausible-looking wrong
        digest. Scoped to the fenced code block itself (not surrounding
        prose) so a prose mention of the old anti-pattern, used to explain
        the bug, can't make this assertion vacuous."""
        start = self.text.find("## `Content-digest:`")
        end = self.text.find("## Package files never enter a commit plan")
        self.assertNotEqual(start, -1, "Content-digest section heading not found")
        self.assertNotEqual(end, -1, "next section heading not found")
        section = self.text[start:end]
        code_match = re.search(r"```\n(.*?)```", section, re.S)
        self.assertIsNotNone(code_match, "no fenced code block in digest section")
        code = code_match.group(1)
        self.assertRegex(
            code,
            r'cat\s+"\.skills/pr-packages/<stable-id>/body\.md"',
            msg="digest recipe code does not cat the fully qualified body.md path",
        )
        self.assertNotRegex(
            code,
            r"cat\s+body\.md\b",
            msg="digest recipe code still contains a bare `cat body.md`",
        )

    def test_PCHG_6_3_digest_recipe_guards_unreadable_body_before_pipe(self):
        """PCHG-6.3 — the qualified path alone does not fix the
        silent-corruption bug: a qualified-but-missing body.md still lets
        `cat` fail on stderr while `printf`'s bytes flow on through the
        pipe, so `git hash-object` hashes the title alone and prints a
        plausible-looking wrong SHA. The actual fix is a readability guard
        that aborts — with a nonzero exit — before the pipe runs. Pins the
        guard mechanism itself (a `test -r` check on the qualified path,
        wired to a nonzero exit, positioned before the `git hash-object`
        pipe), not just prose describing it, so a variant that keeps the
        qualified `cat` but drops the guard still fails this test."""
        start = self.text.find("## `Content-digest:`")
        end = self.text.find("## Package files never enter a commit plan")
        self.assertNotEqual(start, -1, "Content-digest section heading not found")
        self.assertNotEqual(end, -1, "next section heading not found")
        section = self.text[start:end]
        code_match = re.search(r"```\n(.*?)```", section, re.S)
        self.assertIsNotNone(code_match, "no fenced code block in digest section")
        code = code_match.group(1)

        guard_match = re.search(
            r'test\s+-r\s+"\.skills/pr-packages/<stable-id>/body\.md"'
            r"(?:[^\n]*\n)*?[^\n]*\bexit\s+[1-9]\d*\b",
            code,
        )
        self.assertIsNotNone(
            guard_match,
            "digest recipe code has no `test -r "
            '".skills/pr-packages/<stable-id>/body.md" || { ...; exit <nonzero>; }` '
            "readability guard on the qualified body.md path",
        )

        pipe_match = re.search(r"\|\s*git hash-object", code)
        self.assertIsNotNone(
            pipe_match, "digest recipe code has no pipe into git hash-object"
        )
        self.assertLess(
            guard_match.start(),
            pipe_match.start(),
            "readability guard must abort before the pipe into git hash-object, not after",
        )

    def test_PCHG_6_2_stable_id_sanitization_is_an_explicit_rule(self):
        """PCHG-6.2 — sanitization is an explicit character allow-list plus a
        numeric length bound, not a qualitative description. `git
        check-ref-format --branch` legally permits shell metacharacters in
        branch names, so a vague rule like 'separators replaced' leaves the
        stable-id field land-branch rederives to ambiguous."""
        self.assertRegex(
            self.text,
            r"\[?a-z0-9-\]?",
            msg="no explicit [a-z0-9-] allow-list found",
        )
        self.assertRegex(
            self.text,
            r"\b\d+ characters\b",
            msg="no numeric length bound found",
        )

    def test_PCHG_6_5_proves_skills_is_ignored_first(self):
        """PCHG-6.5 — nothing is written until .skills/ is proven git-ignored."""
        self.assertRegex(self.text, r"(?s)git-ignored.{0,200}before")

    def test_PCHG_6_6_6_7_never_committed_never_linked(self):
        """PCHG-6.6 PCHG-6.7 — package files never enter a commit plan or a reviewer link."""
        self.assertRegex(self.text, r"(?i)never .{0,60}commit plan")
        self.assertRegex(self.text, r"(?i)never .{0,80}reviewer-facing locator")


class PrepareChangeAdvisory(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text()

    def test_PCHG_7_1_no_rewriting_verbs(self):
        """PCHG-7.1 — every rewrite verb is named as forbidden. Scoped to the
        advisory-commit-map section itself: `rewrite`, `amend`, `squash`, and
        `reorder` each already appear elsewhere in the file for unrelated
        reasons (phase 1's "never rewrites the project default", phase 5's
        "never amend, squash, or reorder" about session-created commits), so
        an unscoped assertIn would still pass if one of those six verbs were
        dropped from this section alone."""
        start = self.text.find("## Advisory commit map and findings grading")
        end = self.text.find("## Red flags")
        self.assertNotEqual(start, -1, "advisory commit map section heading not found")
        self.assertNotEqual(end, -1, "Red flags heading not found")
        section = self.text[start:end]
        for verb in ("rewrite", "amend", "squash", "reorder", "rebase", "force-push"):
            self.assertIn(verb, section, f"'{verb}' verb missing from advisory commit map section")
        self.assertRegex(section, r"(?s)(NEVER|never|SHALL NOT).{0,200}rebase")

    def test_PCHG_7_2_map_carries_five_parts(self):
        """PCHG-7.2 — the advisory map names groups, order, subjects, bodies,
        rationale, trailers as the six-part bullet list itself, not merely as
        bare words anywhere in the section. `groups`, `order`, and `subjects`
        each recur in this section's own prose for unrelated reasons ("the
        order those groups would appear in"; "real order"; "real subjects"),
        so a plain assertIn on the word would still pass if the bullet naming
        that part were deleted. Match each part by its own `- **name**`
        bullet marker instead, and require exactly six such bullets, so
        deleting any one bullet fails regardless of what the surrounding
        prose happens to say."""
        start = self.text.find("## Advisory commit map and findings grading")
        end = self.text.find("## Red flags")
        self.assertNotEqual(start, -1, "advisory commit map section heading not found")
        self.assertNotEqual(end, -1, "Red flags heading not found")
        section = self.text[start:end]
        list_start = section.find("parts:")
        list_end = section.find("`manifest.md`'s")
        self.assertNotEqual(list_start, -1, "'parts:' lead-in to the six-part bullet list not found")
        self.assertNotEqual(list_end, -1, "'`manifest.md`'s' lead-out after the bullet list not found")
        bullet_block = section[list_start:list_end]
        bullet_parts = re.findall(r"^- \*\*([a-z]+)\*\*", bullet_block, re.MULTILINE)
        self.assertEqual(
            len(bullet_parts), 6,
            f"expected exactly six map-part bullets, found {bullet_parts}",
        )
        self.assertEqual(
            set(bullet_parts),
            {"groups", "order", "subjects", "bodies", "rationale", "trailers"},
            f"map bullets do not match the six expected parts: {bullet_parts}",
        )

    def test_PCHG_7_3_no_runnable_rewrite_commands(self):
        """PCHG-7.3 — no runnable reset/rebase/force-push command is emitted by default."""
        self.assertRegex(self.text, r"(?i)no runnable .{0,60}command")

    def test_PCHG_7_4_body_describes_the_real_branch(self):
        """PCHG-7.4 — the PR body never describes the map as applied."""
        self.assertRegex(self.text, r"(?s)as it actually exists|never .{0,60}as though")

    def test_PCHG_7_5_7_6_four_grades(self):
        """PCHG-7.5 PCHG-7.6 — four grades; machine-enforced failures ride the prove-claim path."""
        for grade in ("advisory", "reported", "not run"):
            self.assertIn(grade, self.text)
        self.assertRegex(self.text, r"(?s)verify.{0,120}(failure path|withhold)")
        self.assertRegex(self.text, r"(?i)no (additional|new) gate")

    def test_PCHG_7_7_findings_travel_in_the_package(self):
        """PCHG-7.7 — findings and grades reach the package."""
        self.assertRegex(self.text, r"(?s)findings.{0,120}package")

    def test_PCHG_4_6_findings_grading_names_both_convention_grades(self):
        """PCHG-4.6 — commit_subject_form and pr_structure resolve on
        separate ladders in conventions.md and can land on different
        grades in the same session, so the cross-cutting findings-grading
        section here must key a finding's grade off whichever specific
        convention it was raised against (commit_subject_grade or
        pr_structure_grade), never off one shared `grade`. Scoped to the
        'Advisory commit map and findings grading' section, since the word
        'grade' recurs throughout SKILL.md for unrelated reasons (phase 5's
        subject-axis validation, the rationalization table)."""
        start = self.text.find("## Advisory commit map and findings grading")
        end = self.text.find("## Red flags")
        self.assertNotEqual(start, -1, "advisory commit map section heading not found")
        self.assertNotEqual(end, -1, "Red flags heading not found")
        section = self.text[start:end]
        self.assertIn(
            "commit_subject_grade", section,
            "findings-grading section does not name commit_subject_grade",
        )
        self.assertIn(
            "pr_structure_grade", section,
            "findings-grading section does not name pr_structure_grade",
        )


class PrepareChangeWritingSkillsForm(unittest.TestCase):
    """author-skills ship checklist: red flags, Done when, no plan-task leaks,
    digest recipe single-home match with land-branch."""

    def setUp(self):
        self.skill = SKILL.read_text()
        self.pkg = PKG.read_text()

    def test_red_flags_section_lists_gate_symptoms(self):
        """Gate skills carry ## Red flags as the symptom list beside the table."""
        start = self.skill.find("## Red flags")
        self.assertNotEqual(start, -1, "## Red flags heading missing")
        section = self.skill[start:self.skill.find("## Rationalizations")]
        for needle in ("origin/HEAD", "pre-existing", "git-ignored", "five ask"):
            self.assertIn(needle, section, f"red-flag symptom missing: {needle}")

    def test_each_phase_has_done_when(self):
        """Every phase ends on a checkable Done when bound."""
        # Six phase titles, each followed by a Done when before the next phase
        # or the advisory section.
        phases = [
            "1. **Resolve base**",
            "2. **Resolve conventions**",
            "3. **Gather context**",
            "4. **Resolve tickets**",
            "5. **Author commits**",
            "6. **Write package**",
        ]
        for i, phase in enumerate(phases):
            p = self.skill.find(phase)
            self.assertNotEqual(p, -1, f"phase missing: {phase}")
            end = (
                self.skill.find(phases[i + 1])
                if i + 1 < len(phases)
                else self.skill.find("## Advisory commit map")
            )
            chunk = self.skill[p:end]
            self.assertIn(
                "**Done when:**", chunk,
                f"{phase} lacks **Done when:**",
            )

    def test_no_plan_task_number_leaks_in_prepare_change_files(self):
        """Skill bodies name consumers by role, not ephemeral plan Task N."""
        root = REPO / "skills" / "ship" / "package-change"
        for path in root.glob("*.md"):
            text = path.read_text()
            self.assertIsNone(
                re.search(r"\bTasks?\s+\d+\b", text),
                f"plan task-number leak in {path.name}",
            )

    def test_package_contract_has_toc(self):
        """References over ~100 lines carry a table of contents."""
        self.assertRegex(self.pkg, r"(?m)^## Contents\s*$")
        self.assertIn("[Layout]", self.pkg)

    def test_digest_recipe_block_matches_finish_branch(self):
        """Single-home digest: land-branch's fenced recipe equals package-contract's."""
        finish = (REPO / "skills" / "ship" / "land-branch" / "SKILL.md").read_text()

        def extract_digest_code(text: str) -> str:
            # Prefer the Content-digest section when present; else first block
            # that pipes into git hash-object (land-branch embeds it inline).
            start = text.find("## `Content-digest:`")
            region = text[start:] if start != -1 else text
            for m in re.finditer(r"```(?:bash)?\n(.*?)```", region, re.S):
                block = m.group(1).strip()
                if "git hash-object" in block and "title.txt" in block:
                    return block
            self.fail("no digest recipe code block found")

        self.assertEqual(
            extract_digest_code(self.pkg),
            extract_digest_code(finish),
            "land-branch digest block drifted from package-contract.md home",
        )


class PrepareChangeRationalizations(unittest.TestCase):
    def setUp(self):
        self.text = SKILL.read_text()

    def test_important_3_rationalizations_table_has_content_rows(self):
        """docs/product/guidelines.md:16 requires a populated rationalization
        table (`| Thought | Reality |` form) in skill bodies. SKILL.md shipped
        with the header and zero rows; count real content rows (lines under
        the `|---|---|` separator that still open with `| "`) so the table
        can't silently regress back to that empty state."""
        start = self.text.find("## Rationalizations")
        self.assertNotEqual(start, -1, "Rationalizations heading not found")
        section = self.text[start:]
        sep = "|---|---|"
        header_end = section.find(sep)
        self.assertNotEqual(header_end, -1, "rationalization table header separator not found")
        rows_text = section[header_end + len(sep):]
        rows = [
            line for line in rows_text.splitlines()
            if line.strip().startswith('| "')
        ]
        self.assertGreaterEqual(
            len(rows), 4,
            f"expected at least 4 rationalization content rows, found {len(rows)}",
        )


if __name__ == "__main__":
    unittest.main()
