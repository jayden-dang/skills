"""The committed baseline resolves by pickaxe, against a real git history.

ASSESS-1.8 resolves the baseline as the full SHA of the single commit that introduced the
milestone's *current* `Committed` state, and ASSESS-1.10 withholds when it does not resolve.
Every other test in this feature reads markdown; this one drives the documented command
against a real repository, because the argument that makes it correct — given the line is
present at the candidate revision, the most recent change to its occurrence count must be
its addition — is a claim about git's behaviour, not about the skill's prose.

Promoted from the acceptance run recorded in `.skills/assess-milestone-acceptance.md`.
"""

import subprocess
import tempfile
import unittest
from pathlib import Path

FIXTURES = Path(__file__).resolve().parent / "milestone-assessment" / "fixtures"
COMMITTED = "**Commitment:** Committed 2026-03-01"


def git(repo, *args):
    return subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", *args],
        cwd=repo, capture_output=True, text=True, check=True,
    ).stdout.strip()


def build(tmp, roadmap_text):
    repo = Path(tmp)
    (repo / "docs" / "roadmap").mkdir(parents=True)
    (repo / "docs" / "roadmap" / "INDEX.md").write_text(roadmap_text)
    git(repo, "init", "-q", ".")
    return repo


def pickaxe(repo, line):
    """The documented pass 5, verbatim."""
    return git(repo, "log", "-1", "--format=%H", "-S", line, "--", "docs/roadmap/INDEX.md")


class CommittedBaseline(unittest.TestCase):
    def setUp(self):
        self.roadmap = (FIXTURES / "clean-close" / "roadmap-INDEX.md").read_text()
        self.assertIn(COMMITTED, self.roadmap, "fixture no longer carries the commitment line")

    def test_baseline_is_the_introducing_commit_not_head(self):
        """ASSESS-1.8 — later commits must not be mistaken for the baseline."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = build(tmp, self.roadmap)
            git(repo, "add", "-A")
            git(repo, "commit", "-q", "-m", "commit the milestone")
            introduced = git(repo, "rev-parse", "HEAD")
            for n in range(2):
                (repo / f"file{n}").write_text("x")
                git(repo, "add", "-A")
                git(repo, "commit", "-q", "-m", f"unrelated {n}")

            self.assertEqual(introduced, pickaxe(repo, COMMITTED))
            self.assertNotEqual(git(repo, "rev-parse", "HEAD"), pickaxe(repo, COMMITTED))

    def test_baseline_follows_a_recommitment(self):
        """ASSESS-1.8 — committed, backed out, re-committed resolves to the RE-commit."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = build(tmp, self.roadmap)
            git(repo, "add", "-A")
            git(repo, "commit", "-q", "-m", "commit the milestone")
            first = git(repo, "rev-parse", "HEAD")

            index = repo / "docs" / "roadmap" / "INDEX.md"
            index.write_text(self.roadmap.replace(COMMITTED, "**Commitment:** Planned"))
            git(repo, "add", "-A")
            git(repo, "commit", "-q", "-m", "back out the commitment")

            index.write_text(self.roadmap)
            git(repo, "add", "-A")
            git(repo, "commit", "-q", "-m", "re-commit the milestone")
            recommit = git(repo, "rev-parse", "HEAD")

            resolved = pickaxe(repo, COMMITTED)
            self.assertEqual(recommit, resolved, "resolved to a stale commitment")
            self.assertNotEqual(first, resolved)

    def test_untracked_roadmap_resolves_to_nothing(self):
        """ASSESS-1.10 — the line is present but absent from history, so the verdict withholds."""
        with tempfile.TemporaryDirectory() as tmp:
            repo = build(tmp, self.roadmap)
            (repo / "other").write_text("x")
            git(repo, "add", "other")
            git(repo, "commit", "-q", "-m", "init without the roadmap")

            self.assertIn(COMMITTED, (repo / "docs" / "roadmap" / "INDEX.md").read_text())
            self.assertEqual("", pickaxe(repo, COMMITTED))


if __name__ == "__main__":
    unittest.main()
