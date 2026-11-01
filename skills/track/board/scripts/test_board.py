"""Behavior test for board.py's Shaping column (unittest, stdlib only)."""

from __future__ import annotations

import json
import os
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


LABELS_READY = """| Canonical role | Label |
|---|---|
| ready-for-agent | ready-for-agent |
| bug | bug |
| enhancement | enhancement |
"""


def ticket(number, title="A ticket", labels=("ready-for-agent", "enhancement"), body="", **extra):
    return dict(number=number, title=title, labels=[dict(name=l) for l in labels], assignees=[], comments=[], body=body, **extra)


def repo(root, approved=(), requirements=None, records=None):
    """A repo holding the label map, an approved feature per code, and `.skills/<dir>/tickets.md` per record."""
    (root / "docs/agents").mkdir(parents=True)
    (root / "docs/agents/triage-labels.md").write_text(LABELS_READY)
    (root / "docs/specs/catalog").mkdir(parents=True)
    rows = "| Code | Spec |\n|---|---|\n"
    for code in approved:
        d = root / "docs/specs" / code.lower()
        d.mkdir()
        for f in ("requirements", "design", "tasks"):
            (d / f"{f}.md").write_text("Status: Approved\n")
        rows += f"| {code} | ../{code.lower()}/ |\n"
    (root / "docs/specs/catalog/core.md").write_text(rows)
    if requirements:
        (root / "docs/specs/fixes.md").write_text(requirements)
    for name, text in (records or {}).items():
        (root / ".skills" / name).mkdir(parents=True)
        (root / ".skills" / name / "tickets.md").write_text(text)


def board(root, issues):
    (root / "issues.json").write_text(json.dumps(issues))
    (root / "prs.json").write_text("[]")
    return subprocess.run([sys.executable, str(BOARD), "--issues", "issues.json", "--prs", "prs.json", "--me", "me"],
                          cwd=root, capture_output=True, text=True, check=True).stdout


def line_for(out, number):
    return next(l for l in out.splitlines() if l.startswith(f"- #{number} ") and ("eligible" in l.lower()))


FIX = "- **QUOTA-4.1** WHEN a quota is exceeded THE SYSTEM SHALL refuse the call.\n- **QUOTA-4.2** (guard) WHEN a quota is not exceeded THE SYSTEM SHALL CONTINUE TO serve the call.\n"


class TestBlocking(unittest.TestCase):
    def run_board(self, *issues):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            repo(root)
            return board(root, list(issues))

    def test_an_open_native_edge_shows_the_ticket_as_blocked(self):
        out = self.run_board(ticket(1), ticket(2, blockedBy=dict(nodes=[dict(number=1)], totalCount=1)))
        self.assertIn("blocked by #1", line_for(out, 2))

    def test_a_closed_native_blocker_does_not_block(self):
        out = self.run_board(ticket(2, blockedBy=dict(nodes=[dict(number=1)], totalCount=1)))
        self.assertNotIn("blocked by", line_for(out, 2))

    def test_a_blocked_by_line_still_shows_the_ticket_as_blocked(self):
        out = self.run_board(ticket(1), ticket(2, body="Blocked by: #1"))
        self.assertIn("blocked by #1", line_for(out, 2))

    def test_an_issues_file_with_no_native_edges_prints_every_section(self):
        out = self.run_board(ticket(1))
        for section in ("### Ready", "## Board and repo disagree"):
            self.assertIn(section, out)


class TestPrivateRecords(unittest.TestCase):
    def test_a_private_ticket_resolves_its_feature_from_the_record(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            repo(root, approved=["QUOTA"], records={"QUOTA": "#7 covers: QUOTA-1.1\n"})
            out = board(root, [ticket(7, title="Owners see their quota")])
        self.assertIn("eligible", line_for(out, 7))
        self.assertNotIn("NOT eligible", line_for(out, 7))
        self.assertNotIn("spec is missing", out)

    def test_a_private_bug_with_a_covered_fix_and_guard_is_a_tier_one_fix(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            repo(root, requirements=FIX, records={"QUOTA": "ZR-9 covers: QUOTA-4.1, QUOTA-4.2\n"})
            out = board(root, [ticket("ZR-9", title="Calls over quota are served", labels=("ready-for-agent", "bug"))])
        self.assertIn("eligible, tier-1 fix", out)

    def test_a_shared_bug_is_still_a_tier_one_fix_from_its_body(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            repo(root, requirements=FIX)
            out = board(root, [ticket(9, labels=("ready-for-agent", "bug"), body="Requirements covered: QUOTA-4.1, QUOTA-4.2")])
        self.assertIn("eligible, tier-1 fix", line_for(out, 9))

    def test_a_pending_record_resolves_no_feature(self):
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            repo(root, approved=["QUOTA"], records={"_pending-quota": "#7 road: ROAD-6\n"})
            out = board(root, [ticket(7)])
        self.assertIn("NOT eligible", line_for(out, 7))


class TestGhFallback(unittest.TestCase):
    def test_a_gh_that_rejects_blocked_by_still_lists_the_tickets(self):
        stub = """#!/usr/bin/env python3
import json, os, sys
s = " ".join(sys.argv[1:])
if "blockedBy" in s:
    print('Unknown JSON field: "blockedBy"', file=sys.stderr); sys.exit(1)
if sys.argv[1:3] == ["issue", "list"]:
    print(json.dumps([dict(number=5, title="Still listed", labels=[dict(name="ready-for-agent")], assignees=[], comments=[], body="")]))
elif sys.argv[1:3] == ["pr", "list"]:
    print("[]")
else:
    print("{}")
"""
        with tempfile.TemporaryDirectory() as t:
            root = Path(t)
            repo(root)
            (root / "bin").mkdir()
            (root / "bin/gh").write_text(stub)
            (root / "bin/gh").chmod(0o755)
            env = dict(os.environ, PATH=f"{root / 'bin'}{os.pathsep}{os.environ['PATH']}")
            out = subprocess.run([sys.executable, str(BOARD), "--me", "me"], cwd=root, env=env,
                                 capture_output=True, text=True, check=True).stdout
        self.assertIn("#5 Still listed", out)


if __name__ == "__main__":
    unittest.main()
