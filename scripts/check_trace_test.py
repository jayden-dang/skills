"""Regression tests for check_trace.py — the requirements traceability linter.

Ported from scripts/check-trace.test.mjs (the oracle). Expected values are copied from the
oracle's expectations, never recomputed from the Python port under test.

This file is itself scanned by check-trace (testGlobs = ["scripts"], testFilePattern matches
`_test.py`), so it is a Fixture-ID-bearing file: it must be listed in docs/agents/trace.json's
`ignore` array (see CONTEXT.md's Fixture ID vs Citation distinction). The retirement fixture's
`RET`-coded IDs below are assembled at runtime — never written as a contiguous literal — so
the raw source text never contains a full ID-shaped match; other fixture IDs (`IGN`- and
`GHOST`-coded) are left as literals, matching the oracle's own test file, and are covered by
the `ignore` entry instead. The bracketed `[PYPORT-N.M]` tags in docstrings are genuine
Citations for this porting task and are meant to be found.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

import check_trace  # module-existence contract; the tests below exercise the CLI as a subprocess

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PY_CLI = os.path.join(_SCRIPTS_DIR, "check_trace.py")


class _FixtureTestCase(unittest.TestCase):
    """Shared fixture builder + CLI runner, mirroring check-trace.test.mjs's fixture()/run()."""

    def _fixture(self, requirements, files=None, trace_json=None):
        """Build a throwaway repo root with one spec file (and optional test files)."""
        root = tempfile.mkdtemp(prefix="check-trace-")
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        spec_dir = os.path.join(root, "docs", "specs", "feature")
        os.makedirs(spec_dir, exist_ok=True)
        with open(os.path.join(spec_dir, "requirements.md"), "w", encoding="utf-8") as fh:
            fh.write(requirements)
        for rel, body in (files or {}).items():
            p = os.path.join(root, rel)
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, "w", encoding="utf-8") as fh:
                fh.write(body)
        if trace_json is not None:
            agents_dir = os.path.join(root, "docs", "agents")
            os.makedirs(agents_dir, exist_ok=True)
            with open(os.path.join(agents_dir, "trace.json"), "w", encoding="utf-8") as fh:
                json.dump(trace_json, fh)
        return root

    def _run(self, root):
        """Run check_trace.py --json against root; return (code, summary)."""
        r = subprocess.run(
            [sys.executable, PY_CLI, "--root", root, "--json"],
            capture_output=True,
            text=True,
        )
        return r.returncode, json.loads(r.stdout)


class RetirementTest(_FixtureTestCase):
    def test_struck_through_requirement_is_retired_not_counted_cannot_fire_e2(self):
        """[PYPORT-1.1] a struck-through requirement is retired: not counted, cannot fire E2."""
        RET = "RET"
        requirements = "\n".join(
            [
                "# Requirements: retirement",
                f"Feature code: {RET}",
                "Status: Implemented",
                "",
                f"- **{RET}-1.1** THE SYSTEM SHALL do the live thing.",
                f"- ~~**{RET}-9.9**~~ superseded by {RET}-1.1 — retired, deliberately untested.",
                "",
            ]
        )
        # The live requirement has a covering test; the retired one has none.
        root = self._fixture(
            requirements,
            files={"src/cover.test.ts": f"it('[{RET}-1.1] covered', () => {{}})"},
        )
        code, summary = self._run(root)
        self.assertEqual(summary["requirements"], 1, f"only {RET}-1.1 is a definition; {RET}-9.9 is retired")
        self.assertEqual(summary["errors"], [], f"no E2 for the retired {RET}-9.9")
        self.assertEqual(code, 0, "clean exit")

    def test_bold_not_struck_id_still_fires_e2(self):
        """[PYPORT-1.1] the same ID left bold (not struck) still fires E2 — strip is strikethrough-specific."""
        RET = "RET"
        requirements = "\n".join(
            [
                "# Requirements: retirement",
                f"Feature code: {RET}",
                "Status: Implemented",
                "",
                f"- **{RET}-9.9** THE SYSTEM SHALL do a thing nobody tested.",
                "",
            ]
        )
        # No covering test anywhere.
        root = self._fixture(requirements)
        code, summary = self._run(root)
        self.assertEqual(summary["requirements"], 1, f"{RET}-9.9 counts as a definition when bold")
        self.assertEqual(len(summary["errors"]), 1, "exactly one error")
        self.assertRegex(summary["errors"][0], r"^E2 " + RET + r"-9\.9\b", "E2 still fires for a genuinely uncovered requirement")
        self.assertEqual(code, 1, "non-zero exit on error")


IGNORE_REQUIREMENTS = "\n".join(
    [
        "# Requirements: ignore",
        "Feature code: IGN",
        "Status: Approved",
        "",
        "- **IGN-1.1** THE SYSTEM SHALL do something unrelated to the fixture file.",
        "",
    ]
)


class IgnoreListTest(_FixtureTestCase):
    """Ports check-trace.test.mjs's TRACE-1.x-labeled tests. TRACE stays uncovered/Out of Scope
    per docs/specs/2026-07-10-python-linters/design.md; these tests exist to guard PYPORT-5.3
    (the port carries the `ignore` behavior forward), not to cite TRACE requirement IDs.
    """

    def test_ignore_excludes_matching_test_files_so_fixture_ids_never_fire_e1(self):
        """[PYPORT-5.3] docs/agents/trace.json ignore excludes matching test files, so their fixture IDs never fire E1."""
        root = self._fixture(
            IGNORE_REQUIREMENTS,
            files={"src/x.test.ts": "it('[GHOST-9.9] x', () => {})"},
            trace_json={"ignore": ["x.test.ts"]},
        )
        code, summary = self._run(root)
        self.assertEqual(summary["errors"], [], "the ignored file contributes no reference to GHOST-9.9, so no E1 fires")
        self.assertEqual(code, 0, "clean exit")

    def test_empty_ignore_array_scans_every_test_file_unknown_id_still_fires_e1(self):
        """[PYPORT-5.3] an empty ignore array scans every test file — unknown ID still fires E1."""
        root = self._fixture(
            IGNORE_REQUIREMENTS,
            files={"src/x.test.ts": "it('[GHOST-9.9] x', () => {})"},
            trace_json={"ignore": []},
        )
        code, summary = self._run(root)
        self.assertEqual(len(summary["errors"]), 1, "exactly one error")
        self.assertRegex(summary["errors"][0], r"^E1 test cites unknown requirement GHOST-9\.9", "E1 fires — ignore is off by default")
        self.assertEqual(code, 1, "non-zero exit on error")

    def test_no_trace_json_at_all_unknown_id_test_file_fires_e1_as_before(self):
        """[PYPORT-5.3] with no trace.json at all, an unknown-ID test file fires E1 exactly as before this change."""
        root = self._fixture(
            IGNORE_REQUIREMENTS,
            files={"src/x.test.ts": "it('[GHOST-9.9] x', () => {})"},
            # no trace_json — docs/agents/trace.json does not exist
        )
        code, summary = self._run(root)
        self.assertEqual(
            summary["errors"],
            ["E1 test cites unknown requirement GHOST-9.9 (src/x.test.ts)"],
            "byte-identical error text to pre-ignore behavior",
        )
        self.assertEqual(summary["testFilesScanned"], 1, "the file is still scanned")
        self.assertEqual(code, 1, "non-zero exit on error")

    def test_blank_ignore_entry_does_not_exclude_every_test_file(self):
        """[PYPORT-5.3] a blank ignore entry ("") does not exclude every test file."""
        requirements = "\n".join(
            [
                "# Requirements: ignore blank entries",
                "Feature code: IGN",
                "Status: Implemented",
                "",
                "- **IGN-2.1** THE SYSTEM SHALL do something unrelated to the fixture file.",
                "",
            ]
        )
        # A stray/blank entry in `ignore` must be a no-op, not `s in rel` (always true for "").
        root = self._fixture(
            requirements,
            files={"src/good.test.ts": "it('[IGN-2.1] covered', () => {})"},
            trace_json={"ignore": [""]},
        )
        code, summary = self._run(root)
        self.assertGreaterEqual(summary["testFilesScanned"], 1, "the real test file is still scanned; an empty ignore entry must not match every path")
        self.assertEqual(summary["testedRequirements"], 1, "IGN-2.1 is still discovered as covered, not silently excluded")
        self.assertEqual(summary["errors"], [], "Implemented IGN-2.1 has a covering test, so no E2 fires")
        self.assertEqual(code, 0, "clean exit")

    def test_ignore_only_adds_exclusion_non_ignored_files_still_selected_and_covered(self):
        """[PYPORT-5.3] ignore only adds an exclusion — testGlobs/testFilePattern selection and coverage still work for non-ignored files."""
        root = self._fixture(
            IGNORE_REQUIREMENTS,
            files={
                "src/good.test.ts": "it('[IGN-1.1] covered', () => {})",
                "src/x.test.ts": "it('[GHOST-9.9] x', () => {})",
            },
            trace_json={"ignore": ["x.test.ts"]},
        )
        code, summary = self._run(root)
        self.assertEqual(summary["testedRequirements"], 1, "IGN-1.1 is still discovered and counted as tested via normal testGlobs/testFilePattern selection")
        self.assertEqual(summary["errors"], [], "the ignored file still contributes nothing, and the non-ignored file cites a known ID")
        self.assertEqual(code, 0, "clean exit")


class WalkOrderTest(_FixtureTestCase):
    """Guards PYPORT-1.1: check_trace.py's directory walk must visit entries in the
    same order the oracle does. check-trace.mjs walks via fs.readdirSync, which
    libuv implements as scandir(3) + alphasort — Node always yields directory
    entries alphabetically. Python's os.scandir makes no such promise and, on
    this filesystem, returns raw (non-alphabetical) order once a directory holds
    enough entries. When two candidate files in the same directory both cite the
    same unknown ID, which one becomes the E1's example filename — and the order
    of the errors array itself — depends entirely on this.
    """

    def test_walk_visits_entries_in_the_same_alphabetical_order_as_the_oracle(self):
        """[PYPORT-1.1] the E1 example file for an unknown ID cited by two candidate
        files must be the alphabetically-first one, matching fs.readdirSync — not
        whichever file os.scandir happens to yield first."""
        ZED = "ZED"
        cite = f"it('[{ZED}-3.3] x')"
        candidate_words = (
            "apple", "mango", "zebra", "kiwi", "lemon",
            "grape", "peach", "plum", "berry", "melon",
        )
        files = {}
        # A pile of filler files pushes this directory past whatever small/inline
        # format the filesystem uses for a handful of entries and into a format
        # (verified empirically on this repo's filesystem) whose raw scandir
        # order is no longer alphabetical.
        for i in range(1, 51):
            files[f"src/filler_{i:03d}.txt"] = ""
        for w in candidate_words:
            files[f"src/{w}_test.py"] = "no citation here"
        files["src/apple_test.py"] = cite
        files["src/lemon_test.py"] = cite
        root = self._fixture(
            "\n".join(["# Requirements: walk order", "Feature code: WLK", "Status: Approved", ""]),
            files=files,
        )
        src = os.path.join(root, "src")

        # Sanity check: the fixture must actually diverge from alphabetical order
        # on this machine, or the assertion below wouldn't discriminate the bug
        # at all — it would pass whether or not check_trace.py sorts.
        raw_names = [e.name for e in os.scandir(src)]
        raw_target_order = [n for n in raw_names if n in ("apple_test.py", "lemon_test.py")]
        self.assertNotEqual(
            raw_target_order,
            sorted(raw_target_order),
            "fixture's raw os.scandir order coincidentally matches alphabetical order on this "
            "filesystem, so it can't exercise PYPORT-1.1 — adjust the filler/target file names",
        )

        code, summary = self._run(root)
        zed_errors = [e for e in summary["errors"] if f"{ZED}-3.3" in e]
        expected_first = sorted(["apple_test.py", "lemon_test.py"])[0]
        self.assertEqual(
            zed_errors,
            [f"E1 test cites unknown requirement {ZED}-3.3 (src/{expected_first}, +1 more)"],
            "the cited example file must be the alphabetically-first candidate, matching "
            "fs.readdirSync's alphasort order, regardless of raw scandir order",
        )


class GuardTest(_FixtureTestCase):
    """New tests required by Task 5's brief, beyond the ported oracle suite."""

    def test_ignore_excludes_a_fixture_bearing_file(self):
        """[PYPORT-5.3] the ignore substring list still excludes test files."""
        root = self._fixture(
            IGNORE_REQUIREMENTS,
            files={"src/fixture.test.ts": "it('[GHOST-1.1] uses a fixture id', () => {})"},
            trace_json={"ignore": ["fixture.test.ts"]},
        )
        code, summary = self._run(root)
        self.assertEqual(summary["testFilesScanned"], 0, "the ignored file is excluded from the scan entirely")
        self.assertEqual(summary["errors"], [], "the excluded fixture id never becomes a citation")
        self.assertEqual(code, 0, "clean exit")

    def test_zero_requirements_exits_zero(self):
        """[PYPORT-5.4] a repo with no requirements is a clean state."""
        root = tempfile.mkdtemp(prefix="check-trace-")
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        os.makedirs(os.path.join(root, "docs", "specs"), exist_ok=True)
        code, summary = self._run(root)
        self.assertEqual(summary["requirements"], 0, "an empty specs tree defines nothing")
        self.assertEqual(summary["errors"], [], "no requirements means nothing can fire E1/E2/E3")
        self.assertEqual(summary["warnings"], [])
        self.assertEqual(code, 0, "clean exit")

    def test_no_specs_directory_at_all_exits_zero(self):
        """[PYPORT-5.4] a repo with no docs/specs directory at all also exits zero."""
        root = tempfile.mkdtemp(prefix="check-trace-")
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        result = subprocess.run(
            [sys.executable, PY_CLI, "--root", root],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("no specs directory", result.stderr)
        self.assertEqual(result.stdout, "", "the early-exit path prints no summary")


if __name__ == "__main__":
    unittest.main()
