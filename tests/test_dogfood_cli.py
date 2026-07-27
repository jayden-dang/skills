"""Mechanical tests for dogfood CLI (cases, ledger, render, mark rules)."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CLI = REPO / "skills" / "acceptance" / "dogfood" / "scripts" / "dogfood"
CASES = (
    REPO
    / "tests"
    / "drive-dogfood"
    / "fixtures"
    / "notes-app"
    / "notes-dogfood.cases.yaml"
)
SHELL = REPO / "skills" / "acceptance" / "dogfood" / "shell" / "guide.html"


def run_cli(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(CLI), *args]
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=check,
        cwd=str(REPO),
    )


class DogfoodCliTests(unittest.TestCase):
    def test_cli_exists_and_executable_help(self):
        self.assertTrue(CLI.is_file())
        self.assertTrue(SHELL.is_file())
        self.assertTrue(CASES.is_file())
        cp = run_cli("--help", check=False)
        self.assertEqual(cp.returncode, 0)
        self.assertIn("list", cp.stdout)

    def test_list_fixture_cases(self):
        cp = run_cli("list", str(CASES))
        lines = [ln for ln in cp.stdout.strip().splitlines() if ln]
        self.assertEqual(6, len(lines))
        self.assertTrue(lines[0].startswith("CASE-1\tNOTE-1.1\thappy\t"))

    def test_show_case(self):
        cp = run_cli("show", str(CASES), "CASE-3")
        self.assertIn("kind: error", cp.stdout)
        self.assertIn("Title is required", cp.stdout)
        self.assertIn("backend:", cp.stdout)

    def test_init_status_next_mark_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_path = Path(tmp) / "run.md"
            cp = run_cli("init", str(CASES), "-o", str(run_path))
            self.assertEqual(str(run_path), cp.stdout.strip())
            text = run_path.read_text()
            self.assertIn("## CASE-1", text)
            self.assertIn("verdict: pending", text)

            st = run_cli("status", str(run_path))
            self.assertIn("total: 6", st.stdout)
            self.assertIn("pending: 6", st.stdout)
            self.assertIn("next: CASE-1", st.stdout)

            nxt = run_cli("next", str(run_path))
            self.assertEqual("CASE-1", nxt.stdout.strip())

            # pass without server → fail
            bad = run_cli(
                "mark",
                str(run_path),
                "CASE-1",
                "pass",
                "--saw",
                'list shows "Alpha"',
                "--catalog",
                str(CASES),
                check=False,
            )
            self.assertNotEqual(0, bad.returncode)
            self.assertIn("requires non-empty --server", bad.stderr)

            good = run_cli(
                "mark",
                str(run_path),
                "CASE-1",
                "pass",
                "--saw",
                'list shows "Alpha"',
                "--server",
                "GET /api/notes includes Alpha",
                "--catalog",
                str(CASES),
            )
            self.assertIn("CASE-1: pass", good.stdout)

            st2 = run_cli("status", str(run_path))
            self.assertIn("pass: 1", st2.stdout)
            self.assertIn("pending: 5", st2.stdout)
            self.assertIn("next: CASE-2", st2.stdout)

            # presentational pass requires special server string
            run_cli(
                "mark",
                str(run_path),
                "CASE-6",
                "pass",
                "--saw",
                "empty state copy visible",
                "--server",
                "none — presentational",
                "--catalog",
                str(CASES),
            )

            # wrong presentational mark
            run_cli(
                "mark",
                str(run_path),
                "CASE-2",
                "pass",
                "--saw",
                "still there",
                "--server",
                "GET ok",
                "--catalog",
                str(CASES),
            )
            bad_pres = run_cli(
                "mark",
                str(run_path),
                "CASE-6",
                "pass",
                "--saw",
                "x",
                "--server",
                "GET /api/notes",
                "--catalog",
                str(CASES),
                check=False,
            )
            # CASE-6 already pass; re-mark with wrong server should fail validation
            self.assertNotEqual(0, bad_pres.returncode)

            report = Path(tmp) / "report.md"
            run_cli("report", str(run_path), "-o", str(report))
            body = report.read_text()
            self.assertIn("| CASE-1 |", body)
            self.assertIn("pass", body)

    def test_render_embeds_cases_and_roundtrips(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "guide.html"
            run_cli("render", str(CASES), "-o", str(out), "--shell", str(SHELL))
            html = out.read_text()
            self.assertIn("window.__DOGFOOD__", html)
            self.assertIn("CASE-1", html)
            self.assertIn("NOTE-1.1", html)
            self.assertIn("localStorage", html)
            # list from rendered HTML
            cp = run_cli("list", str(out))
            self.assertEqual(6, len(cp.stdout.strip().splitlines()))

    def test_mark_presentational_rejects_probe_string(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_path = Path(tmp) / "run.md"
            run_cli("init", str(CASES), "-o", str(run_path))
            bad = run_cli(
                "mark",
                str(run_path),
                "CASE-6",
                "pass",
                "--saw",
                "empty state",
                "--server",
                "GET /api/notes []",
                "--catalog",
                str(CASES),
                check=False,
            )
            self.assertNotEqual(0, bad.returncode)
            self.assertIn("presentational", bad.stderr.lower())


if __name__ == "__main__":
    unittest.main()
