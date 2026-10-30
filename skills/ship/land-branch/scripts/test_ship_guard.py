"""Behavior tests for ship-guard.sh's out-of-plan check (unittest, stdlib only)."""

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

GUARD = Path(__file__).resolve().parent / "ship-guard.sh"
PLAN_DIR = "docs/specs/2026-09-01-media"
FILES_PLAN = "# Tasks: MEDIA\n\n### Task 1: store\n\n**Files:**\n- Create: `api/media.txt`\n\n- [x] Step 1\n"
CATALOG = "# Lessons\n\n| Code | Feature | Spec | Status | Roadmap item |\n|---|---|---|---|---|\n| MEDIA | Media | [spec](../2026-09-01-media/) | {media} | — |\n| QUIZ | Quiz | [spec](../2026-08-01-quiz/) | {quiz} | — |\n"


class Repo:
    def __init__(self, root: Path):
        self.root = root
        self.git("init", "-q", "-b", "dev")

    def git(self, *args: str) -> str:
        return subprocess.run(["git", "-c", "user.email=t@e.st", "-c", "user.name=t", *args],
                              cwd=self.root, check=True, capture_output=True, text=True).stdout

    def write(self, rel: str, text: str) -> None:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)

    def commit(self, msg: str) -> None:
        self.git("add", "-A")
        self.git("commit", "-q", "-m", msg)

    def guard(self) -> subprocess.CompletedProcess:
        return subprocess.run(["bash", str(GUARD), "dev", f"{PLAN_DIR}/tasks.md"], cwd=self.root,
                              capture_output=True, text=True)


def seeded(t: str) -> Repo:
    r = Repo(Path(t))
    r.write(f"{PLAN_DIR}/requirements.md", "# Requirements\n\nFeature code: MEDIA\nStatus: In-progress\n")
    r.write("docs/specs/catalog/lessons.md", CATALOG.format(media="Approved", quiz="Approved"))
    r.write("docs/specs/INDEX.md", "# Spec Index\n\n| Domain | Scope | Surface roots | Feature catalog |\n|---|---|---|---|\n| lessons | Lessons | `api/` | [catalog](./catalog/lessons.md) |\n")
    r.commit("seed")
    r.git("checkout", "-q", "-b", "feat/media")
    return r


class TestOutOfPlan(unittest.TestCase):
    def test_a_plan_without_any_file_paths_skips_the_check_instead_of_dying(self):
        with tempfile.TemporaryDirectory() as t:
            r = seeded(t)
            r.write(f"{PLAN_DIR}/tasks.md", "# Tasks: MEDIA\n\n### Task 1: store\n\n- [x] Step 1\n")
            r.write("api/media.txt", "store\n")
            r.commit("feat")
            out = r.guard()
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("out-of-plan not checked", out.stdout)
        self.assertNotIn("out-of-plan\t", out.stdout)

    def test_a_plan_with_no_requirements_file_beside_it_still_runs(self):
        with tempfile.TemporaryDirectory() as t:
            r = Repo(Path(t))
            r.write("README.md", "seed\n")
            r.commit("seed")
            r.git("checkout", "-q", "-b", "feat/media")
            r.write(f"{PLAN_DIR}/tasks.md", FILES_PLAN)
            r.write("api/media.txt", "store\n")
            r.write("api/unrelated.txt", "drive-by\n")
            r.commit("feat")
            out = r.guard()
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("out-of-plan\tapi/unrelated.txt", out.stdout)

    def test_the_features_own_catalog_row_is_not_out_of_plan(self):
        with tempfile.TemporaryDirectory() as t:
            r = seeded(t)
            r.write(f"{PLAN_DIR}/tasks.md", FILES_PLAN)
            r.write("api/media.txt", "store\n")
            r.write("docs/specs/catalog/lessons.md", CATALOG.format(media="In-progress", quiz="Approved"))
            r.commit("feat")
            out = r.guard()
        self.assertEqual(out.returncode, 0, out.stderr)
        self.assertIn("# clean", out.stdout)

    def test_another_features_catalog_row_is_still_out_of_plan(self):
        with tempfile.TemporaryDirectory() as t:
            r = seeded(t)
            r.write(f"{PLAN_DIR}/tasks.md", FILES_PLAN)
            r.write("api/media.txt", "store\n")
            r.write("docs/specs/catalog/lessons.md", CATALOG.format(media="In-progress", quiz="Implemented"))
            r.commit("feat")
            out = r.guard()
        self.assertIn("out-of-plan\tdocs/specs/catalog/lessons.md", out.stdout)

    def test_an_unlisted_code_file_is_still_out_of_plan(self):
        with tempfile.TemporaryDirectory() as t:
            r = seeded(t)
            r.write(f"{PLAN_DIR}/tasks.md", FILES_PLAN)
            r.write("api/media.txt", "store\n")
            r.write("api/unrelated.txt", "drive-by\n")
            r.commit("feat")
            out = r.guard()
        self.assertIn("out-of-plan\tapi/unrelated.txt", out.stdout)
        self.assertNotIn("out-of-plan\tapi/media.txt", out.stdout)


if __name__ == "__main__":
    unittest.main()
