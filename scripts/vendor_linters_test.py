"""Regression tests for scripts/vendor_linters.py — the Python port of vendor-linters.mjs.

Ported from scripts/vendor-linters.test.mjs (the oracle). Expected digests are computed
independently here via hashlib, never by calling compute_stamp — a test that asserts
compute_stamp(x) == compute_stamp(x) proves nothing.

No literal requirement-ID-shaped fixture string appears in this file: the one fixture
requirement ID this file needs is assembled at runtime (`"GUARD" + "-1.1"`), so this file
carries no Fixture IDs for check-trace to misread as Citations, and needs no entry in
docs/agents/trace.json's `ignore` list. The bracketed `[PYPORT-N.M]` tags in docstrings below
are genuine Citations for this porting task and are meant to be found.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

import vendor_linters
from vendor_linters import LINTERS, compute_stamp, read_stamp, restamp, install, check_drift

_SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.dirname(_SCRIPTS_DIR)
PY_CLI = os.path.join(_SCRIPTS_DIR, "vendor_linters.py")

STAMP_LINE_PREFIX = "# @skills-linter:"


def _read(rel):
    with open(os.path.join(_REPO_ROOT, rel), "r", encoding="utf-8") as fh:
        return fh.read()


def _expected_stamp(src):
    """Independent source of truth: hash the body with any stamp line removed."""
    body = "\n".join(l for l in src.split("\n") if not l.startswith(STAMP_LINE_PREFIX))
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]


class _ScratchTestCase(unittest.TestCase):
    """A scratch skill-set root (real ported linters) plus an empty scratch consumer repo."""

    def _scratch(self):
        root = tempfile.mkdtemp(prefix="vendor-")
        self.addCleanup(shutil.rmtree, root, ignore_errors=True)
        src_root = os.path.join(root, "skills")
        dest_root = os.path.join(root, "consumer")
        os.makedirs(os.path.join(src_root, "scripts"), exist_ok=True)
        os.makedirs(dest_root, exist_ok=True)
        for _, (_, port_filename) in LINTERS.items():
            shutil.copyfile(
                os.path.join(_SCRIPTS_DIR, port_filename),
                os.path.join(src_root, "scripts", port_filename),
            )
        return src_root, dest_root

    def _vendored(self, dest_root, port_filename):
        return os.path.join(dest_root, "scripts", port_filename)


class StampTest(_ScratchTestCase):
    def test_every_shipped_linter_carries_a_stamp(self):
        """[PYPORT-3.1][FGRAPH-11.2] every shipped Python linter carries a content-hash stamp naming itself."""
        for name, (_, port_filename) in LINTERS.items():
            src = _read(f"scripts/{port_filename}")
            stamp = read_stamp(src)
            self.assertIsNotNone(stamp, f"scripts/{port_filename} must carry a '{STAMP_LINE_PREFIX} <name> sha256:<12hex>' line")
            self.assertEqual(stamp["name"], name, f"scripts/{port_filename} stamp must name the linter it belongs to")

    def test_stamp_matches_body_hash(self):
        """[PYPORT-3.1][FGRAPH-11.2] each linter's stamp is the sha256 of its own body."""
        for name, (_, port_filename) in LINTERS.items():
            src = _read(f"scripts/{port_filename}")
            stamp = read_stamp(src)
            self.assertIsNotNone(stamp, f"scripts/{port_filename} must carry a stamp")
            self.assertEqual(stamp["digest"], _expected_stamp(src), f"scripts/{port_filename} stamp is stale — recompute it")

    def test_compute_stamp_excludes_stamp_line_so_stamping_reaches_a_fixpoint(self):
        """[PYPORT-3.1][FGRAPH-11.2] compute_stamp excludes the stamp line, so re-stamping a stamped file is a no-op."""
        src = _read("scripts/check_graph.py")
        tampered = "\n".join(
            "# @skills-linter: check-graph sha256:000000000000" if l.startswith(STAMP_LINE_PREFIX) else l
            for l in src.split("\n")
        )
        self.assertNotEqual(src, tampered, "guard: the tamper must actually change the file")
        self.assertEqual(compute_stamp(tampered), compute_stamp(src), "the stamp line must not feed its own hash")
        self.assertEqual(compute_stamp(src), _expected_stamp(src), "compute_stamp agrees with an independent sha256")

    def test_restamp_is_idempotent(self):
        """[PYPORT-3.1] restamp(restamp(src)) == restamp(src) — stamping reaches a fixpoint."""
        src = _read("scripts/check_graph.py")
        once = restamp(src, "check-graph")
        twice = restamp(once, "check-graph")
        self.assertEqual(once, twice)
        stamp = read_stamp(once)
        self.assertEqual(stamp["digest"], _expected_stamp(once))


class InstallTest(_ScratchTestCase):
    def test_install_copies_every_linter_stamp_intact(self):
        """[PYPORT-1.1][FGRAPH-11.1] install copies every Python linter into the consumer repo, stamp intact."""
        src_root, dest_root = self._scratch()
        result = install(src_root, dest_root)
        self.assertEqual(sorted(r["name"] for r in result), sorted(LINTERS.keys()))
        for name, (_, port_filename) in LINTERS.items():
            dest = self._vendored(dest_root, port_filename)
            self.assertTrue(os.path.exists(dest), f"{name} landed in the consumer repo")
            with open(dest, "r", encoding="utf-8") as fh:
                dest_body = fh.read()
            self.assertEqual(dest_body, _read(f"scripts/{port_filename}"), "byte-identical to source")
            self.assertEqual(read_stamp(dest_body)["name"], name, "vendored copy carries its stamp")

    def test_a_vendored_linter_actually_runs_from_the_consumer_repo(self):
        """[PYPORT-1.1][FGRAPH-11.1] a vendored linter actually runs, as a subprocess, from the consumer repo."""
        src_root, dest_root = self._scratch()
        install(src_root, dest_root)
        vendored_graph = self._vendored(dest_root, LINTERS["check-graph"][1])
        r = subprocess.run(
            [sys.executable, vendored_graph, "--query", "--json"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, f"vendored check_graph.py should run: {r.stderr}")
        json.loads(r.stdout)  # must not raise

    def _read_vendored(self, dest_root, port_filename):
        with open(self._vendored(dest_root, port_filename), "r", encoding="utf-8") as fh:
            return fh.read()

    def test_check_drift_never_mutates_the_consumer_repo(self):
        """[PYPORT-1.1][FGRAPH-11.3] check_drift is read-only — it never writes into the consumer repo."""
        src_root, dest_root = self._scratch()
        install(src_root, dest_root)
        before = [self._read_vendored(dest_root, pf) for _, (_, pf) in LINTERS.items()]
        check_drift(src_root, dest_root)
        after = [self._read_vendored(dest_root, pf) for _, (_, pf) in LINTERS.items()]
        self.assertEqual(before, after)


class CheckDriftTest(_ScratchTestCase):
    def test_a_fresh_install_reports_no_drift(self):
        """[PYPORT-3.1][FGRAPH-11.3] a fresh install reports no drift."""
        src_root, dest_root = self._scratch()
        install(src_root, dest_root)
        drift = [d for d in check_drift(src_root, dest_root) if d["status"] != "ok"]
        self.assertEqual(drift, [])

    def test_a_never_installed_linter_reports_missing(self):
        """[PYPORT-3.1][FGRAPH-11.3] a never-installed linter reports missing."""
        src_root, dest_root = self._scratch()
        drift = check_drift(src_root, dest_root)
        self.assertEqual([d["status"] for d in drift], ["missing", "missing"])

    def test_a_stale_vendored_copy_reports_outdated(self):
        """[PYPORT-3.1][FGRAPH-11.3] a stale vendored copy (untouched locally, source moved on) reports outdated."""
        src_root, dest_root = self._scratch()
        install(src_root, dest_root)
        # The skill set moves on: check-trace.py gains a capability and is re-stamped.
        src_path = os.path.join(src_root, "scripts", LINTERS["check-trace"][1])
        with open(src_path, "r", encoding="utf-8") as fh:
            evolved = fh.read() + "\n# a new capability, e.g. the ignore list\n"
        restamped = restamp(evolved, "check-trace")
        with open(src_path, "w", encoding="utf-8") as fh:
            fh.write(restamped)

        drift = [d for d in check_drift(src_root, dest_root) if d["status"] != "ok"]
        self.assertEqual(len(drift), 1, "exactly one linter drifted")
        self.assertEqual(drift[0]["name"], "check-trace")
        self.assertEqual(drift[0]["status"], "outdated")

    def test_a_hand_edited_vendored_copy_reports_modified_even_with_an_untouched_stamp(self):
        """[PYPORT-3.1][FGRAPH-11.3] a hand-edited vendored copy reports modified before outdated is even considered — the ordering trap."""
        src_root, dest_root = self._scratch()
        install(src_root, dest_root)

        # The source ALSO moves on (declared != expected becomes true too), so a
        # check_drift that tests `outdated` before `modified` would see the stale
        # declared digest, conclude "outdated", and never notice the local hand
        # edit at all — the two conditions must be allowed to coexist, with
        # `modified` winning, for this test to actually discriminate the order.
        src_path = os.path.join(src_root, "scripts", LINTERS["check-graph"][1])
        with open(src_path, "r", encoding="utf-8") as fh:
            evolved = fh.read() + "\n# a new capability\n"
        with open(src_path, "w", encoding="utf-8") as fh:
            fh.write(restamp(evolved, "check-graph"))

        dest = self._vendored(dest_root, LINTERS["check-graph"][1])
        # Body changes; the stamp line is left alone — checking `outdated` first
        # would find declared != expected (source moved on) and misreport
        # `outdated`, silently discarding the fact the local copy was also hand-edited.
        with open(dest, "r", encoding="utf-8") as fh:
            body = fh.read()
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(body + "\n# local hack\n")

        drift = [d for d in check_drift(src_root, dest_root) if d["status"] != "ok"]
        self.assertEqual(len(drift), 1)
        self.assertEqual(drift[0]["name"], "check-graph")
        self.assertEqual(drift[0]["status"], "modified", "modified must win over outdated when both conditions hold")


FIXTURE_ID = "GUARD" + "-1.1"


class GuardTest(_ScratchTestCase):
    def _fixture_repo(self):
        """A consumer repo that drives check-trace's full pipeline: one Implemented requirement
        with a covering test. An empty repo is useless here — check_trace.py early-exits with
        "no specs directory", so both copies would trivially agree.
        """
        d = tempfile.mkdtemp(prefix="consumer-repo-")
        self.addCleanup(shutil.rmtree, d, ignore_errors=True)
        os.makedirs(os.path.join(d, "docs/specs/thing"), exist_ok=True)
        os.makedirs(os.path.join(d, "tests"), exist_ok=True)
        with open(os.path.join(d, "docs/specs/thing/requirements.md"), "w", encoding="utf-8") as fh:
            fh.write(
                "# Requirements: Thing\n\nFeature code: GUARD\nStatus: Implemented\n\n"
                f"## 1. Thing\n\n- **{FIXTURE_ID}** THE SYSTEM SHALL do a thing.\n"
            )
        with open(os.path.join(d, "tests/thing_test.py"), "w", encoding="utf-8") as fh:
            fh.write(f'def test_covered():\n    """[{FIXTURE_ID}] covered."""\n')
        return d

    def test_the_vendored_check_trace_behaves_exactly_like_the_source_copy(self):
        """[PYPORT-1.1][FGRAPH-11.14] (guard) the vendored check_trace.py behaves exactly like the source copy."""
        src_root, dest_root = self._scratch()
        install(src_root, dest_root)
        fixture = self._fixture_repo()

        def run(linter):
            return subprocess.run([sys.executable, linter], cwd=fixture, capture_output=True, text=True)

        source = run(os.path.join(src_root, "scripts", LINTERS["check-trace"][1]))
        copy = run(self._vendored(dest_root, LINTERS["check-trace"][1]))

        self.assertEqual(source.returncode, 0, "guard: the fixture reaches a clean, fully-traced state")
        self.assertIn("1 requirement", source.stdout, "guard: the full pipeline ran, not an early exit")
        self.assertEqual(copy.returncode, source.returncode, "exit code unchanged")
        self.assertEqual(copy.stdout, source.stdout, "stdout unchanged")
        self.assertEqual(copy.stderr, source.stderr, "stderr unchanged")


class CliTest(_ScratchTestCase):
    def test_stamp_mode_restamps_in_place(self):
        """[PYPORT-1.1] --stamp restamps each linter under --from in place."""
        src_root, _ = self._scratch()
        r = subprocess.run(
            [sys.executable, PY_CLI, "--stamp", "--from", src_root],
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        for name, (_, port_filename) in LINTERS.items():
            self.assertIn(f"stamped {name} ->", r.stdout)
            with open(os.path.join(src_root, "scripts", port_filename), "r", encoding="utf-8") as fh:
                stamped = fh.read()
            stamp = read_stamp(stamped)
            self.assertEqual(stamp["digest"], _expected_stamp(stamped))

    def test_install_mode_writes_the_consumer_repo(self):
        """[PYPORT-1.1] --install writes every linter into --to."""
        src_root, dest_root = self._scratch()
        r = subprocess.run(
            [sys.executable, PY_CLI, "--install", "--from", src_root, "--to", dest_root],
            capture_output=True,
            text=True,
        )
        self.assertEqual(r.returncode, 0, r.stderr)
        for _, (_, port_filename) in LINTERS.items():
            self.assertTrue(os.path.exists(os.path.join(dest_root, "scripts", port_filename)))

    def test_check_mode_exits_1_on_drift_and_0_when_clean(self):
        """[PYPORT-1.1] --check exits 1 when a linter is missing, 0 once installed."""
        src_root, dest_root = self._scratch()
        before = subprocess.run(
            [sys.executable, PY_CLI, "--check", "--from", src_root, "--to", dest_root],
            capture_output=True,
            text=True,
        )
        self.assertEqual(before.returncode, 1)
        self.assertIn("missing", before.stdout)

        subprocess.run(
            [sys.executable, PY_CLI, "--install", "--from", src_root, "--to", dest_root],
            capture_output=True,
            text=True,
        )
        after = subprocess.run(
            [sys.executable, PY_CLI, "--check", "--from", src_root, "--to", dest_root],
            capture_output=True,
            text=True,
        )
        self.assertEqual(after.returncode, 0, after.stdout + after.stderr)
        self.assertIn("OK", after.stdout)

    def test_no_mode_prints_usage_and_exits_2(self):
        """[PYPORT-1.1] no mode flag prints usage to stderr and exits 2, matching the oracle."""
        r = subprocess.run([sys.executable, PY_CLI], capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)
        self.assertIn("usage:", r.stderr)


class LegacyTest(_ScratchTestCase):
    """[PYPORT-3.2][PYPORT-3.3][PYPORT-3.4][PYPORT-3.5][PYPORT-3.6] the `legacy`
    verdict and consented migration — new behavior with no `.mjs` oracle
    (PYPORT-2.8 exempts it from the parity corpus). A scratch consumer repo
    holds only a vendored `check-trace.mjs` (as if installed before the
    Python port existed) and no `check_trace.py` at all.
    """

    def _legacy_dest(self):
        """A scratch consumer repo holding a vendored `check-trace.mjs`,
        stamped via the .mjs oracle's own `// @skills-linter:` convention,
        with no `check_trace.py` installed yet. Returns (dest_root, oracle_filename).
        """
        dest_root = tempfile.mkdtemp(prefix="vendor-legacy-dest-")
        self.addCleanup(shutil.rmtree, dest_root, ignore_errors=True)
        os.makedirs(os.path.join(dest_root, "scripts"), exist_ok=True)
        oracle_filename = LINTERS["check-trace"][0]
        body = "// a legacy check-trace body, predating the Python port\nconsole.log('legacy');\n"
        digest = hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]
        stamped = f"// @skills-linter: check-trace sha256:{digest}\n{body}"
        with open(os.path.join(dest_root, "scripts", oracle_filename), "w", encoding="utf-8") as fh:
            fh.write(stamped)
        return dest_root, oracle_filename

    def test_vendored_mjs_reports_legacy(self):
        """[PYPORT-3.2] a .mjs where a .py is expected is `legacy`."""
        src_root, _ = self._scratch()
        dest_root, oracle_filename = self._legacy_dest()
        legacy_path = os.path.join(dest_root, "scripts", oracle_filename)
        self.assertTrue(os.path.exists(legacy_path), "guard: the legacy .mjs fixture is actually on disk")

        drift = {d["name"]: d for d in check_drift(src_root, dest_root)}
        self.assertEqual(
            drift["check-trace"]["status"], "legacy",
            "an untouched vendored .mjs, with the .py port absent, must report legacy — not missing",
        )
        self.assertEqual(
            drift["check-graph"]["status"], "missing",
            "guard: a linter with neither .py nor .mjs present stays missing",
        )

    def test_install_writes_the_py_linters(self):
        """[PYPORT-3.3] install lands check_trace.py and check_graph.py."""
        src_root, _ = self._scratch()
        dest_root, oracle_filename = self._legacy_dest()

        # Spelling out the documented default pins install()'s new signature:
        # PYPORT-3.3 is that installing the .py port must succeed exactly the
        # same whether or not a legacy .mjs sits alongside it.
        install(src_root, dest_root, remove_legacy=False)

        for _, (_, port_filename) in LINTERS.items():
            dest = os.path.join(dest_root, "scripts", port_filename)
            self.assertTrue(os.path.exists(dest), f"{port_filename} must be installed even beside a legacy .mjs")
        with open(os.path.join(dest_root, "scripts", "check_trace.py"), "r", encoding="utf-8") as fh:
            self.assertEqual(fh.read(), _read("scripts/check_trace.py"), "byte-identical to the skill set's copy")

    def test_install_offers_to_remove_legacy(self):
        """[PYPORT-3.4] the legacy .mjs removal is offered."""
        src_root, _ = self._scratch()
        dest_root, oracle_filename = self._legacy_dest()
        legacy_path = os.path.join(dest_root, "scripts", oracle_filename)

        results = install(src_root, dest_root, remove_legacy=True)

        self.assertFalse(os.path.exists(legacy_path), "explicit consent (remove_legacy=True) removes the untouched legacy .mjs")
        record = next(r for r in results if r["name"] == "check-trace")
        self.assertEqual(record.get("legacy_removed"), legacy_path, "install reports what it removed")

    def test_install_never_removes_without_consent(self):
        """[PYPORT-3.5] remove_legacy defaults False; the .mjs survives."""
        src_root, _ = self._scratch()
        dest_root, oracle_filename = self._legacy_dest()
        legacy_path = os.path.join(dest_root, "scripts", oracle_filename)

        # Pin the default explicitly first (proves the parameter exists and
        # defaults to False)...
        install(src_root, dest_root, remove_legacy=False)
        self.assertTrue(os.path.exists(legacy_path), "explicit remove_legacy=False must leave the .mjs in place")

        # ...then prove omitting it entirely behaves identically.
        install(src_root, dest_root)
        self.assertTrue(os.path.exists(legacy_path), "omitted remove_legacy defaults False -> the .mjs still survives")

    def test_install_rejects_non_boolean_consent(self):
        """[PYPORT-3.5] remove_legacy defaults False; the .mjs survives.

        install() guards a real os.remove, and is a public function a future
        caller could invoke with a naively-parsed value instead of a genuine
        bool. Only the literal True the CLI itself produces may delete —
        every other value, truthy (the string "false", the int 1) or not,
        must fail closed and leave the legacy .mjs on disk.
        """
        src_root, _ = self._scratch()
        dest_root, oracle_filename = self._legacy_dest()
        legacy_path = os.path.join(dest_root, "scripts", oracle_filename)

        # The string "false" is truthy in Python — `elif remove_legacy:`
        # would delete here. It must not.
        install(src_root, dest_root, remove_legacy="false")
        self.assertTrue(
            os.path.exists(legacy_path),
            'remove_legacy="false" (a truthy string) must NOT be treated as consent',
        )

        # 1 == True but is not the same object/type as True; it must not be
        # accepted either, so both a truthy string and a truthy non-bool
        # number fail the same way (fail closed, not "whichever happens to
        # pass an `==` check").
        install(src_root, dest_root, remove_legacy=1)
        self.assertTrue(
            os.path.exists(legacy_path),
            "remove_legacy=1 (truthy, but not True) must NOT be treated as consent",
        )

    def test_modified_legacy_warns_before_removal(self):
        """[PYPORT-3.6] a hand-edited legacy copy warns that removal discards it."""
        src_root, _ = self._scratch()
        dest_root, oracle_filename = self._legacy_dest()
        legacy_path = os.path.join(dest_root, "scripts", oracle_filename)
        with open(legacy_path, "a", encoding="utf-8") as fh:
            fh.write("// a local hand-edit made after vendoring, stamp line left untouched\n")

        drift = {d["name"]: d for d in check_drift(src_root, dest_root)}
        self.assertEqual(drift["check-trace"]["status"], "modified", "a hand-edited legacy file is modified...")
        self.assertTrue(drift["check-trace"].get("legacy"), "...AND legacy — both facts must be reported together")

        results = install(src_root, dest_root, remove_legacy=True)

        self.assertTrue(
            os.path.exists(legacy_path),
            "a hand-edited legacy file may hold unsaved work — consent alone must not delete it",
        )
        record = next(r for r in results if r["name"] == "check-trace")
        self.assertTrue(record.get("legacy_warning"), "install must surface a warning instead of silently keeping quiet")
        self.assertIsNone(record.get("legacy_removed"), "a warned-about file must not also be reported removed")


if __name__ == "__main__":
    unittest.main()
