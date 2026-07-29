"""finish-branch checkpoint: ticket question, content approval, and every prior gate."""
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
FINISH = REPO / "skills" / "ship" / "finish-branch" / "SKILL.md"


class FinishBranchCheckpoint(unittest.TestCase):
    def setUp(self):
        self.text = FINISH.read_text()

    def test_PCHG_8_1_8_2_ticket_question_always_asked(self):
        """PCHG-8.1 PCHG-8.2 — the ticket set is shown and the question asked, tracker or not."""
        self.assertIn("resolved ticket set", self.text)
        self.assertRegex(self.text, r"(?s)no tracker.{0,200}still ask")

    def test_PCHG_8_3_file_issues_named_never_invoked(self):
        """PCHG-8.3 — /file-issues is named and the crossing pauses (ARCH-5)."""
        self.assertIn("/file-issues", self.text)
        self.assertRegex(self.text, r"(?i)never invoke|named, never")

    def test_PCHG_8_4_8_5_content_approval_and_edit_loop(self):
        """PCHG-8.4 PCHG-8.5 — approve/edit/cancel, with edits forcing fresh approval."""
        for token in ("approve", "request edits", "cancel"):
            self.assertIn(token, self.text.lower())
        self.assertRegex(self.text, r"(?s)edit.{0,200}fresh approval")

    def test_PCHG_8_6_8_7_12_3_revalidate_before_submit(self):
        """PCHG-8.6 PCHG-8.7 PCHG-12.3 — SHAs and digest rechecked; mismatch invalidates."""
        self.assertRegex(self.text, r"(?s)immediately before submission")
        self.assertIn("Content-digest:", self.text)
        self.assertRegex(self.text, r"(?i)invalidate")

    def test_PCHG_8_8_submits_approved_bytes(self):
        """PCHG-8.8 — the adapter receives the approved values without re-authoring."""
        self.assertIn("--body-file", self.text)
        self.assertRegex(self.text, r"(?i)without re-authoring")

    def test_PCHG_8_9_digest_inline_not_a_path(self):
        """PCHG-8.9 — the digest is inline evidence; the .skills/ path is never cited."""
        self.assertRegex(self.text, r"(?s)digest.{0,200}inline")

    def test_PCHG_8_10_fresh_record_after_invalidated_approval(self):
        """PCHG-8.10 — an invalidating mismatch after publication forces a fresh
        record-decision publish, carrying the reapproved values, before retry."""
        start = self.text.find("**Option 2 — push + PR.**")
        end = self.text.find("**Option 3 — keep.**")
        self.assertNotEqual(start, -1, "Option 2 section heading not found")
        self.assertNotEqual(end, -1, "Option 3 section heading not found")
        section = self.text[start:end]
        self.assertRegex(
            section,
            r"(?s)invalidat.{0,300}fresh\s+`record-decision`\s+publish.{0,200}"
            r"before submission is retried",
        )
        self.assertRegex(section, r"(?i)carrying the reapproved values")

    def test_important_1_pr_create_passes_approved_title(self):
        """Real break: `gh pr create` errors outright in a non-interactive
        agent session when neither --title nor --fill is given, so the PR
        path breaks on first real use unless the approved title is passed.
        Pinned to the exact `gh pr create` invocation line (not just anywhere
        in the Option 2 section) and reading from title.txt (Minor 5's fix
        for the same shell-quoting hazard), so a stray --title elsewhere in
        the file, or a --title whose value is still interpolated inline,
        can't make this vacuously pass."""
        start = self.text.find("**Option 2 — push + PR.**")
        end = self.text.find("**Option 3 — keep.**")
        self.assertNotEqual(start, -1, "Option 2 section heading not found")
        self.assertNotEqual(end, -1, "Option 3 section heading not found")
        section = self.text[start:end]
        create_match = re.search(r"^gh pr create.*$", section, re.MULTILINE)
        self.assertIsNotNone(create_match, "gh pr create invocation not found in Option 2")
        line = create_match.group(0)
        self.assertIn("--title", line)
        self.assertIn("title.txt", line)

    def test_important_2_option_1_prefers_package_base_over_topology(self):
        """finish-branch's Option 1 (local merge) must use the PR package's
        resolved `Base:` — the branch prepare-change actually authored the
        commits and narrative against — over Step 2's origin/HEAD-derived
        topology detection, when a package exists for this session. Without
        this, `Default PR base: dev` with `origin/HEAD` at `main` merges
        silently against the wrong branch. Step 2's own detection logic is
        untouched; it stays the fallback for the no-package case. Scoped to
        the Option 1 section so this can't match Step 2's own prose instead."""
        start = self.text.find("**Option 1 — merge locally.**")
        end = self.text.find("**Option 2 — push + PR.**")
        self.assertNotEqual(start, -1, "Option 1 section heading not found")
        self.assertNotEqual(end, -1, "Option 2 section heading not found")
        section = self.text[start:end]
        self.assertRegex(section, r"(?i)package exists")
        self.assertRegex(section, r"`Base:`")
        self.assertRegex(section, r"(?i)fallback")

    def test_PCHG_11_1_red_gate_still_withholds(self):
        """PCHG-11.1 — merge and PR stay withheld while any check fails."""
        self.assertRegex(self.text, r"withhold \*\*merge\*\* and \*\*PR\*\*")

    def test_PCHG_11_2_five_options_verbatim(self):
        """PCHG-11.2 — the five-option menu is unchanged and the checkpoint follows it."""
        self.assertIn("Present exactly these five options, verbatim", self.text)
        for option in ("1. Merge back to", "2. Push and create a Pull Request",
                       "3. Keep the branch as-is", "4. Discard this work",
                       "5. Block: reject this work"):
            self.assertIn(option, self.text)

    def test_PCHG_11_3_record_before_crossing(self):
        """PCHG-11.3 — record-decision still publishes before any crossing."""
        self.assertIn("record-decision", self.text)
        self.assertRegex(self.text, r"(?s)before.{0,80}(git/gh side effect|the crossing)")

    def test_PCHG_11_4_typed_discard(self):
        """PCHG-11.4 — discard still requires the typed word."""
        self.assertIn("literally type `discard`", self.text)

    def test_PCHG_11_5_optional_skills_still_named(self):
        """PCHG-11.5 — both optional human skills are still named."""
        self.assertIn("/comprehend-change", self.text)
        self.assertIn("/explain-change", self.text)

    def test_PCHG_11_6_no_self_initiated_force_push(self):
        """PCHG-11.6 — force-push remains user-request-only."""
        self.assertRegex(self.text, r"Force-push on your own initiative")


if __name__ == "__main__":
    unittest.main()
