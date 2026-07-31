"""Mechanical tests for dogfood CLI (v2 run file, ledger, render, mark rules).

Requirement IDs travel in each test's first-line docstring, per the Test
annotation conventions in docs/agents/project.md.

Fixture requirement IDs (NOTE-x.y) are never hardcoded here: expected values are
derived from the fixture document itself. That is what keeps this module off the
trace-ignore list, so its DFSYNC tags count as coverage.
"""

from __future__ import annotations

import ast
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CLI = REPO / "skills" / "acceptance" / "dogfood" / "scripts" / "dogfood"
RUN = (
    REPO
    / "tests"
    / "drive-dogfood"
    / "fixtures"
    / "notes-app"
    / "notes-dogfood.json"
)
SHELL = REPO / "skills" / "acceptance" / "dogfood" / "shell" / "guide.html"

# The CLI's dependency budget: standard library only (ARCH-3). Widening this set
# is a deliberate act — `sys.stdlib_module_names` would be the obvious check but
# it needs Python 3.10, and this repo runs 3.9.
ALLOWED_IMPORTS = {
    "__future__",
    "argparse",
    "datetime",
    "http",
    "json",
    "os",
    "pathlib",
    "re",
    "secrets",
    "signal",
    "socket",
    "socketserver",
    "sys",
    "time",
    "typing",
    "urllib",
}


def cli_imports() -> set:
    """Top-level module names the CLI imports, parsed from its source."""
    tree = ast.parse(CLI.read_text(encoding="utf-8"))
    found = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            found.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            found.add(node.module.split(".")[0])
    return found


def run_cli(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    cmd = [sys.executable, str(CLI), *args]
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=check,
        cwd=str(REPO),
    )


def load_fixture() -> dict:
    return json.loads(RUN.read_text(encoding="utf-8"))


def iter_cases(doc: dict):
    for section in doc["sections"]:
        for case in section["cases"]:
            yield case


def case_of(doc: dict, case_id: str) -> dict:
    for case in iter_cases(doc):
        if case["id"] == case_id:
            return case
    raise KeyError(case_id)


def write_doc(directory: Path, doc: dict, name: str = "run.json") -> Path:
    path = Path(directory) / name
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def load_dogfood_module():
    """Import the extension-less CLI script as a module for in-process tests."""
    spec = importlib.util.spec_from_loader(
        "dogfood_cli", importlib.machinery.SourceFileLoader("dogfood_cli", str(CLI))
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def bare_document() -> dict:
    """A minimal authored document: eight slots per case, no run state, no rev."""
    return {
        "version": 2,
        "slug": "bare",
        "sections": [
            {
                "name": "Only section",
                "cases": [
                    {
                        "id": "CASE-1",
                        "req": "BARE-1.1",
                        "kind": "happy",
                        "title": "A bare case",
                        "setup": "nothing",
                        "try": "do the thing",
                        "expect": "the thing happened",
                        "backend": "presentational",
                    }
                ],
            }
        ],
    }


class SchemaV2Tests(unittest.TestCase):
    """Behavior of the loader, exercised on documents the loader must normalize.

    These assert what `load_run_file` guarantees, never what the checked-in
    fixture happens to contain — a test that reads the fixture and asserts the
    fixture's own shape passes by construction and proves nothing.
    """

    def test_loader_supplies_run_state_for_an_authored_document(self):
        """DFSYNC-1.1, DFSYNC-1.2 — one path yields case bodies and run state together."""
        mod = load_dogfood_module()
        with tempfile.TemporaryDirectory() as tmp:
            path = write_doc(Path(tmp), bare_document())
            doc = mod.load_run_file(path)
            case = doc["sections"][0]["cases"][0]
            self.assertEqual("do the thing", case["try"])
            self.assertEqual("pending", case["run"]["verdict"])
            self.assertFalse(case["human"]["checked"])

    def test_loader_defaults_run_and_human_to_disjoint_key_sets(self):
        """DFSYNC-2.1 — the run and human field spaces the loader creates share no key name."""
        mod = load_dogfood_module()
        with tempfile.TemporaryDirectory() as tmp:
            path = write_doc(Path(tmp), bare_document())
            case = mod.load_run_file(path)["sections"][0]["cases"][0]
        overlap = set(case["run"]) & set(case["human"])
        self.assertEqual(set(), overlap, f"run/human share keys: {overlap}")
        self.assertEqual({"verdict", "saw", "server", "notes"}, set(case["run"]))
        self.assertEqual({"checked", "at", "comment"}, set(case["human"]))

    def test_loader_defaults_rev_to_integer_zero(self):
        """DFSYNC-3.1 — a document with no rev loads with an integer rev of 0."""
        mod = load_dogfood_module()
        with tempfile.TemporaryDirectory() as tmp:
            path = write_doc(Path(tmp), bare_document())
            rev = mod.load_run_file(path)["rev"]
        self.assertIsInstance(rev, int)
        self.assertNotIsInstance(rev, bool)
        self.assertEqual(0, rev)

    def test_loader_preserves_recorded_run_state(self):
        """DFSYNC-1.1 — run state already on disk is loaded, not reset to pending."""
        mod = load_dogfood_module()
        doc = bare_document()
        doc["rev"] = 7
        doc["sections"][0]["cases"][0]["run"] = {
            "verdict": "pass",
            "saw": "the thing happened",
            "server": "none — presentational",
            "notes": "",
        }
        with tempfile.TemporaryDirectory() as tmp:
            loaded = mod.load_run_file(write_doc(Path(tmp), doc))
        self.assertEqual(7, loaded["rev"])
        self.assertEqual("pass", loaded["sections"][0]["cases"][0]["run"]["verdict"])

    def test_malformed_documents_are_named_errors(self):
        """DFSYNC-1.5 — wrong version, duplicate id, bad kind, missing slot each exit non-zero."""
        first_id = next(iter_cases(load_fixture()))["id"]
        cases = [
            ("version", lambda d: d.update(version=1)),
            (
                first_id,
                lambda d: d["sections"][0]["cases"].append(
                    dict(d["sections"][0]["cases"][0])
                ),
            ),
            ("chaos", lambda d: d["sections"][0]["cases"][0].update(kind="chaos")),
            ("backend", lambda d: d["sections"][0]["cases"][0].pop("backend")),
        ]
        with tempfile.TemporaryDirectory() as tmp:
            for needle, mutate in cases:
                with self.subTest(needle=needle):
                    doc = load_fixture()
                    mutate(doc)
                    bad = write_doc(Path(tmp), doc, f"bad-{needle}.json")
                    cp = run_cli("list", str(bad), check=False)
                    self.assertNotEqual(0, cp.returncode)
                    self.assertIn(needle, cp.stderr)

    def test_invalid_json_is_a_named_error(self):
        """DFSYNC-1.5 — a file that is not JSON exits non-zero saying so."""
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text("{not json", encoding="utf-8")
            cp = run_cli("list", str(bad), check=False)
            self.assertNotEqual(0, cp.returncode)
            self.assertIn("JSON", cp.stderr)

    def test_stdlib_only_no_third_party_import(self):
        """DFSYNC-1.6 — the CLI imports only from its sanctioned standard-library budget."""
        imported = cli_imports()
        unsanctioned = imported - ALLOWED_IMPORTS
        self.assertEqual(
            set(),
            unsanctioned,
            f"CLI imports outside its stdlib budget: {sorted(unsanctioned)}. "
            "A new import is a deliberate decision — widen ALLOWED_IMPORTS only "
            "for a standard-library module.",
        )
        self.assertNotIn("yaml", imported)

    def test_v1_paths_are_named_errors_not_parse_attempts(self):
        """DFSYNC-1.7 — a .yaml/.yml/-run.md path exits non-zero naming the v2 format."""
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("old.cases.yaml", "old.yml", "notes-dogfood-run.md"):
                with self.subTest(name=name):
                    stale = Path(tmp) / name
                    stale.write_text("version: 1\n", encoding="utf-8")
                    cp = run_cli("list", str(stale), check=False)
                    self.assertNotEqual(0, cp.returncode)
                    self.assertIn("v2", cp.stderr.lower())

    def test_missing_file_is_a_named_error(self):
        """DFSYNC-1.7 — a path that does not exist exits non-zero naming the file."""
        cp = run_cli("list", "/nonexistent/nope.json", check=False)
        self.assertNotEqual(0, cp.returncode)
        self.assertIn("nope.json", cp.stderr)


class CatalogReadTests(unittest.TestCase):
    def test_list_output_unchanged(self):
        """DFSYNC-1.8 — one tab-separated id/req/kind/title line per case, in file order."""
        doc = load_fixture()
        expected = [
            "\t".join((c["id"], c["req"], c["kind"], c["title"])) for c in iter_cases(doc)
        ]
        lines = [ln for ln in run_cli("list", str(RUN)).stdout.splitlines() if ln]
        self.assertEqual(expected, lines)

    def test_show_prints_all_eight_slots(self):
        """DFSYNC-1.9 — show still prints every authored slot for the named case."""
        doc = load_fixture()
        target = next(c for c in iter_cases(doc) if c["kind"] == "error")
        out = run_cli("show", str(RUN), target["id"]).stdout
        for slot in (
            "id:",
            "req:",
            "kind:",
            "title:",
            "setup:",
            "try:",
            "expect:",
            "backend:",
        ):
            self.assertIn(slot, out)
        self.assertIn(target["title"], out)
        self.assertIn(target["req"], out)

    def test_show_unknown_case_is_a_named_error(self):
        """DFSYNC-1.9 — asking for a case that does not exist exits non-zero."""
        cp = run_cli("show", str(RUN), "CASE-999", check=False)
        self.assertNotEqual(0, cp.returncode)
        self.assertIn("CASE-999", cp.stderr)

    def test_cli_help_lists_subcommands(self):
        """DFSYNC-1.2 — the CLI exposes its subcommands and the fixture files exist."""
        self.assertTrue(CLI.is_file())
        self.assertTrue(SHELL.is_file())
        self.assertTrue(RUN.is_file())
        cp = run_cli("--help", check=False)
        self.assertEqual(0, cp.returncode)
        for sub in ("list", "show", "render"):
            self.assertIn(sub, cp.stdout)


if __name__ == "__main__":
    unittest.main()
