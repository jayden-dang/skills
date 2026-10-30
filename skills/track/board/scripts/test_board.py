"""Behavior test for board.py's Shaping column (unittest, stdlib only)."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

BOARD = Path(__file__).resolve().parent / "board.py"
LABELS = """# Triage labels

| Role | Label |
|---|---|
| needs-triage | `needs-triage` |
| shaping | `shaping` |
| ready-for-agent | `ready-for-agent` |
"""
ISSUES = [
    {"number": 301, "title": "ROAD-6 desktop foundation", "labels": [{"name": "shaping"}],
     "assignees": [{"login": "alice"}], "comments": [], "body": ""},
    {"number": 302, "title": "ROAD-9 secrets rotation", "labels": [{"name": "shaping"}],
     "assignees": [], "comments": [], "body": ""},
]


class TestShapingColumn(unittest.TestCase):
    def test_a_shaping_ticket_shows_who_is_framing_it(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            (root / "docs/agents").mkdir(parents=True)
            (root / "docs/agents/triage-labels.md").write_text(LABELS)
            (root / "issues.json").write_text(json.dumps(ISSUES))
            (root / "prs.json").write_text("[]")
            out = subprocess.run([sys.executable, str(BOARD), "--issues", "issues.json", "--prs", "prs.json", "--me", "jayden"],
                                 cwd=root, capture_output=True, text=True, check=True).stdout
        shaping = out.split("### Shaping", 1)[1].split("\n### ", 1)[0]
        line_301 = next(l for l in shaping.splitlines() if l.startswith("- #301"))
        line_302 = next(l for l in shaping.splitlines() if l.startswith("- #302"))
        self.assertIn("alice", line_301)
        self.assertIn("unassigned", line_302)


if __name__ == "__main__":
    unittest.main()
