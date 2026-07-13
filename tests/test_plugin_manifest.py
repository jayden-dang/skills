"""The plugin manifest must list every skill, and only real skills.

A skill missing from `.claude-plugin/plugin.json` exists in the repo, passes
every linter, and still does not install — the failure is silent at exactly the
moment it matters. This is the same drift that left two guide docs listing 8 of
10 user-invoked skills.

Run: python3 -m unittest discover -s tests
"""

import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def manifest_skills() -> set[str]:
    data = json.loads((REPO / ".claude-plugin" / "plugin.json").read_text())
    return {s.removeprefix("./") for s in data["skills"]}


def repo_skills() -> set[str]:
    return {
        str(p.parent.relative_to(REPO)) for p in REPO.glob("skills/*/*/SKILL.md")
    }


class TestPluginManifest(unittest.TestCase):
    def test_every_skill_in_the_repo_is_listed_in_the_manifest(self):
        missing = repo_skills() - manifest_skills()
        self.assertEqual(
            missing, set(), f"skill(s) exist but would not install: {sorted(missing)}"
        )

    def test_every_manifest_entry_points_at_a_real_skill(self):
        stale = manifest_skills() - repo_skills()
        self.assertEqual(
            stale, set(), f"manifest lists skill(s) that do not exist: {sorted(stale)}"
        )


if __name__ == "__main__":
    unittest.main()
