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
import os
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


class RenderTests(unittest.TestCase):
    """`render` output. Note that data-* attributes are set by the shell's JS at
    runtime, so they are asserted against the shell source in
    tests/test_dogfood_guide_contract.py, not against rendered HTML."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = Path(self._tmp.name)

    def render(self, doc=None, shell: Path = None) -> str:
        path = write_doc(self.dir, doc if doc is not None else load_fixture())
        out = self.dir / "guide.html"
        run_cli("render", str(path), "-o", str(out), "--shell", str(shell or SHELL))
        return out.read_text(encoding="utf-8")

    @staticmethod
    def assignment(html: str) -> str:
        """The embedded JSON literal, taken from between the render markers."""
        block = html.split("/* __CASES_JSON__ */", 1)[1].split(
            "/* __END_CASES_JSON__ */", 1
        )[0]
        return block.split("window.__DOGFOOD__ = ", 1)[1].rstrip().rstrip(";")

    def embedded(self, html: str) -> dict:
        return json.loads(self.assignment(html).replace("<\\/", "</"))

    def test_render_embeds_each_cases_current_verdict(self):
        """DFSYNC-4.1 — the generated page carries case bodies and verdicts together."""
        doc = load_fixture()
        cases = list(iter_cases(doc))
        cases[0]["run"] = {
            "verdict": "pass", "saw": "seen it", "server": "probed", "notes": "",
        }
        cases[1]["human"]["checked"] = True
        payload = self.embedded(self.render(doc))
        rendered = {c["id"]: c for c in iter_cases(payload)}
        self.assertEqual("pass", rendered[cases[0]["id"]]["run"]["verdict"])
        self.assertEqual("seen it", rendered[cases[0]["id"]]["run"]["saw"])
        self.assertTrue(rendered[cases[1]["id"]]["human"]["checked"])

    def test_render_records_when_the_snapshot_was_taken(self):
        """DFSYNC-4.3 — the page carries the render timestamp it will show offline."""
        payload = self.embedded(self.render())
        self.assertIn("rendered_at", payload)
        self.assertRegex(payload["rendered_at"], r"^\d{4}-\d{2}-\d{2}T[\d:]{8}")

    def test_render_fails_loudly_without_the_markers(self):
        """DFSYNC-4.7 — a shell missing the marker pair exits non-zero."""
        bad_shell = self.dir / "no-markers.html"
        bad_shell.write_text("<html><body>nothing here</body></html>", encoding="utf-8")
        path = write_doc(self.dir, load_fixture(), "run2.json")
        cp = run_cli(
            "render", str(path), "-o", str(self.dir / "x.html"),
            "--shell", str(bad_shell), check=False,
        )
        self.assertNotEqual(0, cp.returncode)
        self.assertIn("__CASES_JSON__", cp.stderr)

    def test_render_preserves_two_character_newline_escapes(self):
        """DFSYNC-4.8 — a \\n inside a JSON string is not expanded into a real newline."""
        doc = load_fixture()
        first = next(iter_cases(doc))
        first["try"] = "line one\nline two"
        html = self.render(doc)
        assignment = self.assignment(html)
        self.assertIn("line one\\nline two", assignment)
        self.assertNotIn("line one\nline two", assignment)
        self.assertEqual(
            "line one\nline two",
            {c["id"]: c for c in iter_cases(self.embedded(html))}[first["id"]]["try"],
        )

    def test_render_escapes_closing_script_sequences(self):
        """DFSYNC-4.1 — embedded content cannot terminate the script element early."""
        doc = load_fixture()
        next(iter_cases(doc))["expect"] = "a </script> in the copy"
        html = self.render(doc)
        assignment = self.assignment(html)
        self.assertNotIn("</script>", assignment)


class VerdictCommandTests(unittest.TestCase):
    """init / next / status / mark / report, now reading and writing one run file."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = Path(self._tmp.name)

    def run_file(self, doc=None) -> Path:
        return write_doc(self.dir, doc if doc is not None else load_fixture())

    def read(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def pass_case(self, path: Path, case_id: str, server: str) -> subprocess.CompletedProcess:
        return run_cli(
            "mark", str(path), case_id, "pass", "--saw", "it showed up",
            "--server", server, check=False,
        )

    def test_init_seeds_pending_where_absent_and_preserves_pending_state(self):
        """DFSYNC-1.3 — init adds pending run state and leaves existing pending state alone.

        DFSYNC-1.4's trigger is a file that holds a *non-pending* verdict, so the
        state 1.3 protects here is a case already carrying pending run state with
        working notes on it — seeding must not blank that.
        """
        doc = bare_document()
        doc["sections"][0]["cases"].append(
            dict(doc["sections"][0]["cases"][0], id="CASE-2", req="BARE-1.2")
        )
        doc["sections"][0]["cases"][1]["run"] = {
            "verdict": "pending", "saw": "", "server": "", "notes": "seed data loaded",
        }
        path = self.run_file(doc)
        cp = run_cli("init", str(path))
        self.assertEqual(0, cp.returncode)
        written = self.read(path)
        self.assertEqual("pending", case_of(written, "CASE-1")["run"]["verdict"])
        self.assertFalse(case_of(written, "CASE-1")["human"]["checked"])
        self.assertEqual("pending", case_of(written, "CASE-2")["run"]["verdict"])
        self.assertEqual("seed data loaded", case_of(written, "CASE-2")["run"]["notes"])

    def test_init_refuses_when_any_verdict_is_recorded(self):
        """DFSYNC-1.4 — one recorded verdict anywhere in the file blocks a re-seed."""
        doc = bare_document()
        doc["sections"][0]["cases"].append(
            dict(doc["sections"][0]["cases"][0], id="CASE-2", req="BARE-1.2")
        )
        doc["sections"][0]["cases"][1]["run"] = {
            "verdict": "fail", "saw": "nope", "server": "500", "notes": "",
        }
        path = self.run_file(doc)
        before = path.read_text(encoding="utf-8")
        cp = run_cli("init", str(path), check=False)
        self.assertNotEqual(0, cp.returncode)
        self.assertIn("CASE-2", cp.stderr)
        self.assertEqual(before, path.read_text(encoding="utf-8"))

    def test_init_refuses_a_recorded_file_without_force(self):
        """DFSYNC-1.4 — a file already holding a non-pending verdict is not re-seeded."""
        doc = bare_document()
        doc["sections"][0]["cases"][0]["run"] = {
            "verdict": "pass", "saw": "seen", "server": "none — presentational", "notes": "",
        }
        path = self.run_file(doc)
        before = path.read_text(encoding="utf-8")
        cp = run_cli("init", str(path), check=False)
        self.assertNotEqual(0, cp.returncode)
        self.assertIn("--force", cp.stderr)
        self.assertEqual(before, path.read_text(encoding="utf-8"))

        forced = run_cli("init", str(path), "--force")
        self.assertEqual(0, forced.returncode)
        self.assertEqual("pending", case_of(self.read(path), "CASE-1")["run"]["verdict"])

    def test_next_ignores_human_ticks(self):
        """DFSYNC-2.3 — a human tick never advances next past an unproven case."""
        doc = load_fixture()
        for case in iter_cases(doc):
            case["human"] = {"checked": True, "at": "2026-07-31T00:00:00Z", "comment": "eyeballed"}
        path = self.run_file(doc)
        first = next(iter_cases(doc))["id"]
        self.assertEqual(first, run_cli("next", str(path)).stdout.strip())

    def test_next_is_silent_and_exits_1_when_every_case_passes(self):
        """DFSYNC-1.10 — no remaining case means no output and exit 1."""
        doc = load_fixture()
        for case in iter_cases(doc):
            case["run"] = {
                "verdict": "pass", "saw": "seen", "server": "probed", "notes": "",
            }
        cp = run_cli("next", str(self.run_file(doc)), check=False)
        self.assertEqual(1, cp.returncode)
        self.assertEqual("", cp.stdout.strip())

    def test_pass_requires_both_saw_and_server(self):
        """DFSYNC-1.11 — pass with an empty --saw or an empty --server is refused."""
        path = self.run_file()
        target = next(c for c in iter_cases(load_fixture()) if c["backend"] != "presentational")
        missing_server = run_cli(
            "mark", str(path), target["id"], "pass", "--saw", "it showed up", check=False
        )
        self.assertNotEqual(0, missing_server.returncode)
        self.assertIn("--server", missing_server.stderr)

        missing_saw = run_cli(
            "mark", str(path), target["id"], "pass", "--server", "GET /x 200", check=False
        )
        self.assertNotEqual(0, missing_saw.returncode)
        self.assertIn("--saw", missing_saw.stderr)
        self.assertEqual("pending", case_of(self.read(path), target["id"])["run"]["verdict"])

    def test_presentational_sentinel_is_enforced_in_both_directions(self):
        """DFSYNC-1.12 — the sentinel is required for presentational cases and refused elsewhere."""
        fixture = load_fixture()
        presentational = next(c for c in iter_cases(fixture) if c["backend"] == "presentational")
        probed = next(c for c in iter_cases(fixture) if c["backend"] != "presentational")
        path = self.run_file()

        wrong = self.pass_case(path, presentational["id"], "GET /api/notes 200")
        self.assertNotEqual(0, wrong.returncode)
        self.assertIn("presentational", wrong.stderr.lower())

        right = self.pass_case(path, presentational["id"], "none — presentational")
        self.assertEqual(0, right.returncode)

        laundered = self.pass_case(path, probed["id"], "none — presentational")
        self.assertNotEqual(0, laundered.returncode)
        self.assertIn("presentational", laundered.stderr.lower())

    def test_mark_writes_the_verdict_into_the_run_file(self):
        """DFSYNC-1.3 — a recorded verdict and its evidence land in the same file."""
        path = self.run_file()
        target = next(c for c in iter_cases(load_fixture()) if c["backend"] != "presentational")
        before = self.read(path)["rev"]
        cp = self.pass_case(path, target["id"], "GET /api/notes includes it")
        self.assertEqual(0, cp.returncode)
        after = self.read(path)
        case = case_of(after, target["id"])
        self.assertEqual("pass", case["run"]["verdict"])
        self.assertEqual("it showed up", case["run"]["saw"])
        self.assertEqual(before + 1, after["rev"])

    def test_status_reports_the_human_tally_separately(self):
        """DFSYNC-2.4 — the human count is its own line, not folded into the verdict counts."""
        doc = load_fixture()
        cases = list(iter_cases(doc))
        cases[0]["run"]["verdict"] = "pass"
        cases[1]["human"]["checked"] = True
        cases[2]["human"]["checked"] = True
        out = run_cli("status", str(self.run_file(doc))).stdout
        self.assertRegex(out, r"(?m)^total: 6$")
        self.assertRegex(out, r"(?m)^pass: 1$")
        self.assertRegex(out, r"(?m)^pending: 5$")
        self.assertRegex(out, r"(?m)^human: 2$")

    def test_report_gives_the_human_tick_its_own_column(self):
        """DFSYNC-2.5 — the report distinguishes a tick from a verdict."""
        doc = load_fixture()
        cases = list(iter_cases(doc))
        cases[0]["run"]["verdict"] = "pass"
        cases[1]["human"]["checked"] = True
        out = run_cli("report", str(self.run_file(doc))).stdout
        header = next(ln for ln in out.splitlines() if ln.startswith("| case"))
        self.assertIn("human", header)
        self.assertLess(header.index("verdict"), header.index("saw"))
        self.assertNotEqual(header.index("human"), header.index("verdict"))

    def test_report_has_one_row_per_case_and_escapes_pipes(self):
        """DFSYNC-1.13 — a markdown table, one row per case, with | escaped in cell text."""
        doc = load_fixture()
        first = next(iter_cases(doc))
        first["run"] = {
            "verdict": "fail", "saw": "saw a | pipe", "server": "probe | ran", "notes": "",
        }
        out = run_cli("report", str(self.run_file(doc))).stdout
        rows = [ln for ln in out.splitlines() if ln.startswith("| CASE-")]
        self.assertEqual(6, len(rows))
        self.assertIn(r"saw a \| pipe", out)

    def test_mark_opens_no_network_connection(self):
        """DFSYNC-3.5 — mark completes without creating a socket."""
        guard_dir = self.dir / "guard"
        guard_dir.mkdir()
        (guard_dir / "sitecustomize.py").write_text(
            "import socket\n"
            "def _forbidden(*a, **k):\n"
            "    raise AssertionError('dogfood mark opened a socket')\n"
            "socket.socket = _forbidden\n"
            "socket.create_connection = _forbidden\n",
            encoding="utf-8",
        )
        path = self.run_file()
        target = next(c for c in iter_cases(load_fixture()) if c["backend"] != "presentational")
        env = dict(os.environ, PYTHONPATH=str(guard_dir))
        cp = subprocess.run(
            [sys.executable, str(CLI), "mark", str(path), target["id"], "pass",
             "--saw", "it showed up", "--server", "GET /api/notes includes it"],
            capture_output=True, text=True, cwd=str(REPO), env=env,
        )
        self.assertEqual(0, cp.returncode, cp.stderr)
        self.assertNotIn("opened a socket", cp.stderr)
        self.assertEqual("pass", case_of(self.read(path), target["id"])["run"]["verdict"])

    def test_every_subcommand_runs_without_a_server(self):
        """DFSYNC-5.8 — the CLI is fully usable when no serve process exists (ARCH-2)."""
        path = self.run_file()
        first = next(iter_cases(load_fixture()))["id"]
        html = self.dir / "guide.html"
        report = self.dir / "report.md"
        for args in (
            ("list", str(path)),
            ("show", str(path), first),
            ("init", str(path), "--force"),
            ("next", str(path)),
            ("status", str(path)),
            ("report", str(path), "-o", str(report)),
            ("render", str(path), "-o", str(html), "--shell", str(SHELL)),
        ):
            with self.subTest(command=args[0]):
                self.assertEqual(0, run_cli(*args).returncode)

    def test_mark_takes_no_catalog_argument(self):
        """DFSYNC-1.2 — backend comes from the run file, so there is no second path to pass."""
        path = self.run_file()
        first = next(iter_cases(load_fixture()))["id"]
        cp = run_cli(
            "mark", str(path), first, "blocked", "--catalog", str(path), check=False
        )
        self.assertNotEqual(0, cp.returncode)
        self.assertIn("--catalog", cp.stderr)


if __name__ == "__main__":
    unittest.main()
