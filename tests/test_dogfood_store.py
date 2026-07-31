"""The dogfood store: exclusive lock, atomic replace, rev-checked patches.

This is the one new seam DFSYNC introduces (design.md, Seams for testing). The
store is exercised in-process for single-writer behavior and through real
subprocesses for the concurrency guarantee — a threaded stand-in would test the
GIL rather than the lockfile.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
CLI = REPO / "skills" / "acceptance" / "dogfood" / "scripts" / "dogfood"

WRITER_SOURCE = '''
import importlib.machinery, importlib.util, sys
spec = importlib.util.spec_from_loader(
    "dogfood_cli", importlib.machinery.SourceFileLoader("dogfood_cli", sys.argv[1])
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

path, scope, count = sys.argv[2], sys.argv[3], int(sys.argv[4])
for i in range(count):
    case_id = "CASE-%d" % (i + 1)

    def patch(doc, case_id=case_id, scope=scope):
        for section in doc["sections"]:
            for case in section["cases"]:
                if case["id"] == case_id:
                    if scope == "run":
                        case["run"]["notes"] = "touched"
                    else:
                        case["human"]["comment"] = "touched"
                    return
        raise SystemExit("writer: no such case " + case_id)

    mod.commit(path, patch, scope=scope)
'''


def load_dogfood_module():
    spec = importlib.util.spec_from_loader(
        "dogfood_cli", importlib.machinery.SourceFileLoader("dogfood_cli", str(CLI))
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def document(case_count: int = 3) -> dict:
    return {
        "version": 2,
        "rev": 0,
        "slug": "store",
        "sections": [
            {
                "name": "Cases",
                "cases": [
                    {
                        "id": f"CASE-{n}",
                        "req": f"STORE-1.{n}",
                        "kind": "happy",
                        "title": f"Case {n}",
                        "setup": "none",
                        "try": "do it",
                        "expect": "it happened",
                        "backend": "presentational",
                    }
                    for n in range(1, case_count + 1)
                ],
            }
        ],
    }


def iter_cases(doc: dict):
    for section in doc["sections"]:
        for case in section["cases"]:
            yield case


def case_of(doc: dict, case_id: str) -> dict:
    for case in iter_cases(doc):
        if case["id"] == case_id:
            return case
    raise KeyError(case_id)


def set_verdict(doc: dict, case_id: str, verdict: str) -> None:
    case_of(doc, case_id)["run"]["verdict"] = verdict


def tick(doc: dict, case_id: str) -> None:
    case_of(doc, case_id)["human"]["checked"] = True


class StoreTests(unittest.TestCase):
    def setUp(self):
        self.mod = load_dogfood_module()
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.dir = Path(self._tmp.name)

    def fresh_run_file(self, case_count: int = 3) -> Path:
        path = self.dir / "run.json"
        path.write_text(json.dumps(document(case_count), indent=2), encoding="utf-8")
        return path

    def read(self, path: Path) -> dict:
        return json.loads(path.read_text(encoding="utf-8"))

    def test_commit_bumps_rev_and_leaves_no_temp_file(self):
        """DFSYNC-3.2 — a commit lands atomically and increments rev by one."""
        path = self.fresh_run_file()
        before = self.read(path)["rev"]
        self.mod.commit(path, lambda d: set_verdict(d, "CASE-1", "pass"), scope="run")
        after = self.read(path)
        self.assertEqual(before + 1, after["rev"])
        self.assertEqual("pass", case_of(after, "CASE-1")["run"]["verdict"])
        self.assertEqual([], sorted(self.dir.glob("*.tmp*")))
        self.assertEqual([], sorted(self.dir.glob("*.lock")))

    def test_patch_built_on_a_stale_read_lands_on_current_state(self):
        """DFSYNC-3.3 — a patch authored against an old rev applies to the current document."""
        path = self.fresh_run_file()
        stale = self.read(path)
        self.assertEqual(0, stale["rev"])

        self.mod.commit(path, lambda d: set_verdict(d, "CASE-1", "pass"), scope="run")

        # Authored while holding `stale`, committed after the document moved on.
        self.mod.commit(path, lambda d: tick(d, "CASE-2"), scope="human")

        final = self.read(path)
        self.assertEqual(2, final["rev"])
        self.assertEqual("pass", case_of(final, "CASE-1")["run"]["verdict"])
        self.assertTrue(case_of(final, "CASE-2")["human"]["checked"])

    def test_human_scoped_commit_never_changes_a_verdict(self):
        """DFSYNC-2.2 — a human tick leaves the case's verdict untouched."""
        path = self.fresh_run_file()
        self.mod.commit(path, lambda d: set_verdict(d, "CASE-1", "pass"), scope="run")
        self.mod.commit(path, lambda d: tick(d, "CASE-1"), scope="human")
        case = case_of(self.read(path), "CASE-1")
        self.assertEqual("pass", case["run"]["verdict"])
        self.assertTrue(case["human"]["checked"])

    def test_unknown_scope_is_refused(self):
        """DFSYNC-2.2 — a write outside the two known field spaces is refused."""
        path = self.fresh_run_file()
        with self.assertRaises(SystemExit):
            self.mod.commit(path, lambda d: None, scope="verdict")

    def test_scope_is_enforced_not_merely_declared(self):
        """DFSYNC-2.2 — a patch cannot reach outside the field space it declared.

        The whole disjointness argument — and ADR 0006's promise that a tick never
        becomes a verdict — rests on this. A docstring asking politely is not an
        enforcement mechanism, so the store restores the other space after every
        patch.
        """
        path = self.fresh_run_file()

        def run_scoped_patch_reaching_into_human(doc):
            case_of(doc, "CASE-1")["run"]["verdict"] = "pass"
            case_of(doc, "CASE-1")["human"]["checked"] = True   # out of bounds

        self.mod.commit(path, run_scoped_patch_reaching_into_human, scope="run")
        case = case_of(self.read(path), "CASE-1")
        self.assertEqual("pass", case["run"]["verdict"], "the in-scope write must land")
        self.assertFalse(case["human"]["checked"], "the out-of-scope write must not")

    def test_a_human_patch_cannot_forge_a_verdict(self):
        """DFSYNC-2.2 — the same guard in the direction that actually matters."""
        path = self.fresh_run_file()

        def human_scoped_patch_forging_a_pass(doc):
            case_of(doc, "CASE-1")["human"]["checked"] = True
            case_of(doc, "CASE-1")["run"]["verdict"] = "pass"   # out of bounds

        self.mod.commit(path, human_scoped_patch_forging_a_pass, scope="human")
        case = case_of(self.read(path), "CASE-1")
        self.assertTrue(case["human"]["checked"])
        self.assertEqual("pending", case["run"]["verdict"], "a tick must not forge a pass")

    def test_interrupted_write_leaves_the_previous_file_intact(self):
        """DFSYNC-7.4 — a failure mid-write never leaves a partial file at the target path."""
        path = self.fresh_run_file()
        self.mod.commit(path, lambda d: set_verdict(d, "CASE-1", "pass"), scope="run")
        before = path.read_text(encoding="utf-8")

        with mock.patch.object(self.mod.json, "dumps", side_effect=RuntimeError("boom")):
            with self.assertRaises(RuntimeError):
                self.mod.commit(
                    path, lambda d: set_verdict(d, "CASE-2", "fail"), scope="run"
                )

        self.assertEqual(before, path.read_text(encoding="utf-8"))
        json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual([], sorted(self.dir.glob("*.tmp*")))
        self.assertEqual([], sorted(self.dir.glob("*.lock")))

    def test_two_processes_interleaving_lose_no_writes(self):
        """DFSYNC-3.4, DFSYNC-7.3 — 50 writes from each of two processes all survive."""
        path = self.fresh_run_file(case_count=50)
        writer = self.dir / "writer.py"
        writer.write_text(WRITER_SOURCE, encoding="utf-8")

        procs = [
            subprocess.Popen(
                [sys.executable, str(writer), str(CLI), str(path), scope, "50"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            for scope in ("run", "human")
        ]
        for proc in procs:
            out, err = proc.communicate(timeout=120)
            self.assertEqual(0, proc.returncode, f"writer failed: {err or out}")

        doc = self.read(path)
        self.assertEqual(100, doc["rev"], "every commit must bump rev exactly once")
        self.assertEqual(
            50, sum(1 for c in iter_cases(doc) if c["run"]["notes"] == "touched")
        )
        self.assertEqual(
            50, sum(1 for c in iter_cases(doc) if c["human"]["comment"] == "touched")
        )


if __name__ == "__main__":
    unittest.main()
