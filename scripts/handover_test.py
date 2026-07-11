"""[PYPORT-2.7] handover: every FGRAPH/TRACE (and PYPORT) ID cited by the `.mjs`
test oracle must also be cited by a Python test, before Task 12 deletes the
`.mjs` files and the Python twins become the only covering tests left.

Reads docs/agents/trace.json's `ignore` array at runtime and applies it to BOTH
sides of the comparison. Without that, the `.mjs` side would read
check-trace.test.mjs's RET-coded Fixture IDs (test data, not claims of
coverage — see CONTEXT.md's Fixture ID vs Citation distinction) as Citations,
and demand check_trace_test.py reproduce them as literals — which would in turn
fire a bogus E1 from check-trace itself. (This file is itself scanned by
check-trace, so it must not spell those Fixture IDs as literals either — hence
this paragraph names them only as "RET-coded", never as a contiguous ID.)

ID extraction reuses check_trace.extract_ids — the exact function check_trace.py
itself uses to decide what a test file "cites" — so a Citation here means
exactly what check-trace would count as a Citation. No ID-shaped literal appears
in this file; the comparison operates on files, not on any single ID.
"""
import glob
import json
import os
import unittest

import check_trace

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_SCRIPTS_DIR)
_TRACE_JSON = os.path.join(_REPO_ROOT, "docs", "agents", "trace.json")


def _ignore_list():
    """Read docs/agents/trace.json's `ignore` array at runtime.

    Never hard-code the filenames it names — this is what lets the ignore list
    grow (e.g. when Task 12 removes files from it) without editing this test.
    """
    with open(_TRACE_JSON, "r", encoding="utf-8") as fh:
        cfg = json.load(fh)
    return set(cfg.get("ignore", []))


def _select_files(pattern, ignore):
    """Every scripts/ file matching glob `pattern`, minus basenames in `ignore`."""
    return sorted(
        p for p in glob.glob(os.path.join(_SCRIPTS_DIR, pattern))
        if os.path.basename(p) not in ignore
    )


def _ids_cited_by(paths):
    """The union of every requirement ID check_trace.extract_ids finds across paths."""
    ids = set()
    for p in paths:
        with open(p, "r", encoding="utf-8") as fh:
            text = fh.read()
        ids |= set(check_trace.extract_ids(text))
    return ids


# This file's job was to PROVE handover before Task 12 deleted the `.mjs`
# test files (its guards even assert `.mjs` files exist to compare against).
# Once they are gone, the comparison has nothing left to compare — skip
# cleanly rather than fail, mirroring parity_test.py's ORACLE_AVAILABLE
# pattern, so a future run on a machine that still has node does not read
# this as a regression.
_MJS_TEST_FILES_EXIST = bool(glob.glob(os.path.join(_SCRIPTS_DIR, "*.test.mjs")))


@unittest.skipUnless(_MJS_TEST_FILES_EXIST, "oracle unavailable: .mjs test files deleted")
class HandoverTest(unittest.TestCase):
    def test_python_tests_cite_every_id_the_mjs_tests_cite(self):
        """[PYPORT-2.7] no requirement loses its covering test when the .mjs go."""
        ignore = _ignore_list()

        mjs_files = _select_files("*.test.mjs", ignore)
        py_files = _select_files("*_test.py", ignore)
        self.assertTrue(mjs_files, "guard: at least one .mjs test file must exist to compare against")
        self.assertTrue(py_files, "guard: at least one .py test file must exist to compare against")

        mjs_ids = _ids_cited_by(mjs_files)
        py_ids = _ids_cited_by(py_files)

        self.assertLessEqual(mjs_ids, py_ids, f"orphaned: {sorted(mjs_ids - py_ids)}")

    def test_ignored_files_are_skipped_on_both_sides(self):
        """[PYPORT-2.7] guard: files named in trace.json's ignore list are excluded
        from the .mjs side AND the .py side of the comparison — not just one —
        so check-trace.test.mjs's Fixture IDs never leak into the requirement.
        """
        ignore = _ignore_list()
        self.assertTrue(ignore, "guard: ignore list must be non-empty for this test to discriminate anything")

        all_mjs = {os.path.basename(p) for p in glob.glob(os.path.join(_SCRIPTS_DIR, "*.test.mjs"))}
        all_py = {os.path.basename(p) for p in glob.glob(os.path.join(_SCRIPTS_DIR, "*_test.py"))}
        ignored_mjs = ignore & all_mjs
        ignored_py = ignore & all_py
        self.assertTrue(ignored_mjs, "guard: at least one ignored file must actually exist on the .mjs side")
        self.assertTrue(ignored_py, "guard: at least one ignored file must actually exist on the .py side")

        selected_mjs = {os.path.basename(p) for p in _select_files("*.test.mjs", ignore)}
        selected_py = {os.path.basename(p) for p in _select_files("*_test.py", ignore)}
        self.assertFalse(ignored_mjs & selected_mjs, "ignored .mjs file(s) must not appear in the compared set")
        self.assertFalse(ignored_py & selected_py, "ignored .py file(s) must not appear in the compared set")


if __name__ == "__main__":
    unittest.main()
