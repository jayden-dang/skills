#!/usr/bin/env python3
"""parity_test.py — the differential parity corpus.

Runs a fixture repo through both the `.mjs` oracle and its `.py` port and
asserts stdout, stderr, exit code, and the resulting filesystem are
byte-identical. This IS the proof that the ports are safe to ship: Task 12
deletes the `.mjs` files only once this corpus is green.

No literal requirement-ID-shaped fixture string appears in this file: every
Fixture ID a fixture's tree content needs is assembled at runtime (e.g.
`"GHOST" + "-1.1"`), never written as a contiguous literal — this file is
itself scanned by check-trace (testGlobs = ["scripts"], testFilePattern
matches `_test.py`), so a literal ID-shaped token here would read as a
Citation and fire a bogus E1. See CONTEXT.md's Fixture ID vs Citation
distinction. It therefore needs no entry in docs/agents/trace.json's `ignore`
list. The bracketed `[PYPORT-N.M]` tags in docstrings below are genuine
Citations for this porting task and are meant to be found.
"""
import difflib
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from vendor_linters import LINTERS

SCRIPTS = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS.parent

NODE = shutil.which("node")

# vendor_linters.LINTERS only carries the two linters IT vendors/drift-checks
# (check-graph, check-trace); this corpus also parity-tests vendor_linters.py's
# OWN CLI against vendor-linters.mjs, so that pair is added here rather than
# mutating the shipped LINTERS dict.
ALL_LINTERS = dict(LINTERS)
ALL_LINTERS["vendor-linters"] = ("vendor-linters.mjs", "vendor_linters.py")

# The brief's literal formula (guards on ORACLE_AVAILABLE, never `NODE is
# None`, so that after Task 12 deletes the .mjs files on a machine that still
# has node, this suite SKIPS instead of invoking a missing file and failing).
# Strengthened with an explicit vendor-linters.mjs check: LINTERS itself only
# covers the two linters vendor_linters.py vendors, not vendor-linters.mjs
# (which this corpus also runs as an oracle).
ORACLE_AVAILABLE = (
    NODE is not None
    and all((SCRIPTS / m).exists() for m, _ in LINTERS.values())
    and (SCRIPTS / "vendor-linters.mjs").exists()
)


def _first_diff_offset(a, b):
    """The index of the first character at which strings `a` and `b` differ,
    or min(len(a), len(b)) when one is a prefix of the other."""
    n = min(len(a), len(b))
    for i in range(n):
        if a[i] != b[i]:
            return i
    return n


class DiffOffsetTest(unittest.TestCase):
    def test_reports_the_index_of_the_first_differing_character(self):
        """[PYPORT-2.5] _first_diff_offset finds the first differing character."""
        self.assertEqual(_first_diff_offset("abcXdef", "abcYdef"), 3)

    def test_a_common_prefix_with_no_divergence_reports_the_shorter_length(self):
        """[PYPORT-2.5] a strict-prefix pair reports the shorter length, not a false index."""
        self.assertEqual(_first_diff_offset("abc", "abcdef"), 3)

    def test_identical_strings_report_the_full_length(self):
        """[PYPORT-2.5] identical strings report their (equal) length."""
        self.assertEqual(_first_diff_offset("same", "same"), 4)


def diagnose(fixture_id, linter, stream, oracle_val, port_val):
    """A parity-failure message naming the fixture, the linter, the stream,
    the first differing byte offset, and a difflib unified diff — so a
    mismatch never reads as bare "not equal". `""` when the two values
    already agree (an `assertEqual` that passes must never spend a message).
    """
    if oracle_val == port_val:
        return ""
    header = f"parity mismatch: fixture={fixture_id!r} linter={linter!r} stream={stream!r}"
    if isinstance(oracle_val, str) and isinstance(port_val, str):
        offset = _first_diff_offset(oracle_val, port_val)
        diff = "".join(
            difflib.unified_diff(
                oracle_val.splitlines(keepends=True),
                port_val.splitlines(keepends=True),
                fromfile=f"oracle:{stream}",
                tofile=f"port:{stream}",
            )
        )
        return f"{header}\nfirst differing byte offset: {offset}\n{diff}"
    return f"{header}\noracle={oracle_val!r}\nport={port_val!r}"


class DiagnoseTest(unittest.TestCase):
    def test_equal_values_produce_no_message(self):
        """[PYPORT-2.5] diagnose returns "" when the two streams already agree — a passing
        assertion must never spend a message."""
        self.assertEqual(diagnose("fx", "check-trace", "stdout", "same", "same"), "")

    def test_a_stdout_mismatch_names_the_fixture_linter_stream_and_offset(self):
        """[PYPORT-2.5] on mismatch, diagnose names the fixture, the linter, the stream,
        and the first differing byte offset."""
        msg = diagnose("clean-repo", "check-trace", "stdout", "abcXdef", "abcYdef")
        self.assertIn("clean-repo", msg)
        self.assertIn("check-trace", msg)
        self.assertIn("stdout", msg)
        self.assertIn("3", msg, "must name the first differing offset (index 3)")

    def test_a_stdout_mismatch_includes_a_difflib_unified_diff(self):
        """[PYPORT-2.5] on mismatch, diagnose includes a difflib unified diff of the two streams."""
        msg = diagnose("fx", "check-graph", "stdout", "line one\nline two\n", "line one\nCHANGED\n")
        self.assertIn("-line two", msg)
        self.assertIn("+CHANGED", msg)

    def test_an_exit_code_mismatch_names_both_codes_without_crashing_on_non_string_input(self):
        """[PYPORT-2.5] diagnose handles non-string values (exit codes) without raising."""
        msg = diagnose("fx", "check-graph", "exit code", 0, 1)
        self.assertIn("0", msg)
        self.assertIn("1", msg)


def fresh(work, tree):
    """Wipe `work` back to empty, then materialize `tree` ({relpath: content})
    underneath it. The SAME `work` path is reused for both the oracle run and
    the port run of a fixture (and across fixtures) — re-materialized between
    them, never diffed across two different directories — so a path that
    leaks into stdout/stderr is identical either way and can never itself be
    the source of a mismatch.
    """
    for entry in os.listdir(work):
        full = os.path.join(work, entry)
        if os.path.isdir(full) and not os.path.islink(full):
            shutil.rmtree(full)
        else:
            os.remove(full)
    for rel, content in tree.items():
        full = os.path.join(work, rel)
        parent = os.path.dirname(full)
        if parent:
            os.makedirs(parent, exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(content)


def snapshot(work):
    """A deterministic {relpath: content} map of every file under `work`,
    used to diff a run's filesystem side effects byte-for-byte."""
    out = {}
    for dirpath, dirnames, filenames in os.walk(work):
        dirnames.sort()
        for name in sorted(filenames):
            full = Path(dirpath) / name
            rel = full.relative_to(work).as_posix()
            try:
                out[rel] = full.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError) as exc:
                out[rel] = f"<<unreadable: {exc}>>"
    return out


class FreshSnapshotTest(unittest.TestCase):
    """[PYPORT-2.1] fresh()/snapshot() are the harness's re-materialize/capture
    primitives: ONE working directory, wiped and rebuilt between runs, never
    two directories whose distinct paths could themselves leak into output."""

    def setUp(self):
        self.work = tempfile.mkdtemp(prefix="parity-helper-test-")
        self.addCleanup(shutil.rmtree, self.work, ignore_errors=True)

    def test_fresh_materializes_every_file_in_the_tree(self):
        """[PYPORT-2.1] fresh() writes every {path: content} entry, creating parent dirs."""
        fresh(self.work, {"a.txt": "hello", "nested/b.txt": "world"})
        self.assertEqual(Path(self.work, "a.txt").read_text(), "hello")
        self.assertEqual(Path(self.work, "nested/b.txt").read_text(), "world")

    def test_fresh_wipes_prior_content_not_named_in_the_new_tree(self):
        """[PYPORT-2.1] re-materializing must be a WIPE, not an overlay — a file a previous
        fixture (or a linter's own writes) left behind must not survive into the next fixture."""
        fresh(self.work, {"stale.txt": "leftover", "keep/dir/deep.txt": "x"})
        self.assertTrue(Path(self.work, "keep").is_dir())
        fresh(self.work, {"fresh.txt": "new"})
        self.assertFalse(Path(self.work, "stale.txt").exists())
        self.assertFalse(Path(self.work, "keep").exists())
        self.assertTrue(Path(self.work, "fresh.txt").exists())

    def test_snapshot_round_trips_the_materialized_tree(self):
        """[PYPORT-2.1] snapshot() reads back exactly what fresh() wrote."""
        tree = {"a.txt": "hello", "nested/b.txt": "world"}
        fresh(self.work, tree)
        self.assertEqual(snapshot(self.work), tree)

    def test_snapshot_reflects_files_a_run_wrote_after_fresh(self):
        """[PYPORT-2.1] snapshot() captures filesystem EFFECTS of a run, not just the
        original tree — the harvest-writes fixture depends on this."""
        fresh(self.work, {"in.txt": "seed"})
        Path(self.work, "written-by-run.txt").write_text("output")
        snap = snapshot(self.work)
        self.assertEqual(snap["in.txt"], "seed")
        self.assertEqual(snap["written-by-run.txt"], "output")


class Result:
    """(exit code, stdout, stderr) of one CLI invocation."""

    __slots__ = ("code", "out", "err")

    def __init__(self, code, out, err):
        self.code = code
        self.out = out
        self.err = err


def run(cmd, work):
    """Run `cmd` with cwd=work, capturing (code, stdout, stderr) as text."""
    r = subprocess.run(cmd, cwd=work, capture_output=True, text=True)
    return Result(r.returncode, r.stdout, r.stderr)


class RunTest(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.mkdtemp(prefix="parity-run-test-")
        self.addCleanup(shutil.rmtree, self.work, ignore_errors=True)

    def test_run_captures_exit_code_stdout_and_stderr(self):
        """[PYPORT-2.1] run() executes a command in `work` and captures (code, stdout, stderr)."""
        code = "import sys; print('out-line'); print('err-line', file=sys.stderr); sys.exit(7)"
        result = run([sys.executable, "-c", code], self.work)
        self.assertEqual(result.code, 7)
        self.assertEqual(result.out, "out-line\n")
        self.assertEqual(result.err, "err-line\n")

    def test_run_executes_with_the_given_working_directory(self):
        """[PYPORT-2.1] run() executes the command with cwd=work, matching os.getcwd()."""
        result = run([sys.executable, "-c", "import os; print(os.getcwd())"], self.work)
        self.assertEqual(result.out.strip(), os.path.realpath(self.work))


def _rid(code, n, m):
    """Assemble a requirement-ID-shaped string (`CODE-N.M`) at runtime. Never
    write the concatenated form as a literal in this file: it is scanned by
    check-trace as a test file, and a literal ID-shaped token here would be
    misread as a Citation (see module docstring)."""
    return f"{code}-{n}.{m}"


def oracle_cmd_for(fixture, work):
    oracle_file, _ = ALL_LINTERS[fixture["linter"]]
    return [NODE, str(SCRIPTS / oracle_file), "--root", work] + fixture["argv"]


def port_cmd_for(fixture, work):
    _, port_file = ALL_LINTERS[fixture["linter"]]
    return [sys.executable, str(SCRIPTS / port_file), "--root", work] + fixture["argv"]


# ---------------------------------------------------------------- fixtures

def _tree_clean_repo():
    """check-trace, default mode: one Draft requirement (no E2/W1 possible for
    Draft status) — zero errors, zero warnings. Exit 0, both streams empty of
    diagnostics."""
    code = "CLEAN"
    return {
        "docs/specs/thing/requirements.md": (
            "# Requirements: Thing\n"
            f"Feature code: {code}\n"
            "Status: Draft\n\n"
            "## 1. Thing\n\n"
            f"- **{_rid(code, 1, 1)}** THE SYSTEM SHALL do a thing.\n"
        ),
    }


def _tree_trace_errors():
    """check-trace, default mode: no requirements are ever defined, so a test
    file citing an ID fires E1 ("cites unknown requirement"). TWO candidate
    test files sit in the SAME directory, created in NON-alphabetical order
    ("one" before "aaa") and both cite the SAME unknown ID: this is the exact
    shape of Task 5's real parity bug — the E1 message names only the FIRST
    file found (`uniq[0]`), and "first" depends on directory walk order.
    Node's fs.readdirSync always yields alphabetical order (libuv is
    scandir(3) + alphasort); an os.scandir() that is not explicitly
    re-sorted would not, and could name a different file than the oracle.
    """
    ghost = _rid("GHOST", 1, 1)
    return {
        "docs/specs/.gitkeep": "",
        "tests/one.test.js": f"test('[{ghost}] first', () => {{}});\n",
        "tests/aaa.test.js": f"test('[{ghost}] second', () => {{}});\n",
    }


def _tree_strict_warnings():
    """check-trace: one Approved requirement, cited by no task -> W1. A W1-only
    repo exits 0 by default and 1 under --strict."""
    code = "WARNX"
    return {
        "docs/specs/warn/requirements.md": (
            "# Requirements: Warn\n"
            f"Feature code: {code}\n"
            "Status: Approved\n\n"
            "## 1. Warn\n\n"
            f"- **{_rid(code, 1, 1)}** THE SYSTEM SHALL do warn.\n"
        ),
    }


def _tree_stale_graph():
    """check-graph --verify: a committed GRAPH.md that can never match a fresh
    render -> the "GRAPH.md is stale" error. INDEX.md registers the feature
    code so the registration check does NOT also fire, isolating one error."""
    code = "STALEG"
    return {
        "docs/specs/staleg/requirements.md": (
            "# Requirements: Stale Graph\n"
            f"Feature code: {code}\n"
            "Status: Draft\n\n"
            "## Out of Scope\n"
            "- nothing\n"
        ),
        "docs/specs/GRAPH.md": "# Feature Graph\n\nstale placeholder content — never matches a fresh render.\n",
        "docs/specs/INDEX.md": f"# Index\n\n{code}\n",
    }


def _tree_bad_trace_json():
    """check-trace: an unparseable docs/agents/trace.json -> ConfigError,
    stderr, exit 1. PYPORT-2.4's explicitly-named stderr path."""
    return {"docs/agents/trace.json": "{ this is not valid json"}


def _tree_harvest():
    """check-graph, default (--harvest) mode: one Draft requirement, no
    committed GRAPH.md yet -> the run WRITES docs/specs/GRAPH.md. Exit 0,
    filesystem effect."""
    code = "HARVQ"
    return {
        "docs/specs/harvq/requirements.md": (
            "# Requirements: Harvest Writes\n"
            f"Feature code: {code}\n"
            "Status: Draft\n\n"
            "## Out of Scope\n"
            "- nothing\n"
        ),
    }


# ---- vendor-linters fixtures (review pass: Finding 1b) --------------------
#
# vendor_linters.py's `main()` can return exit 0 (`--check` clean, `--install`,
# `--stamp`), 1 (`--check` with drift), or 2 (no mode). Before this pass only
# exit 2 had a fixture (`vendor-no-mode`) — PYPORT-2.4 requires a fixture per
# distinct exit code per linter, and this hole let a genuine parity bug
# (Finding 1a: REMEDY's "missing"/"outdated" strings said `vendor_linters
# --install` where the oracle says `vendor-linters --install`) ship
# undetected, because `--check`'s drift-listing branch — the only place
# REMEDY strings are printed — was never exercised by the corpus.
#
# `vendor_linters.py` vendors `.py` files (check_graph.py/check_trace.py);
# `vendor-linters.mjs` vendors `.mjs` files (check-graph.mjs/check-trace.mjs)
# — by design (see the "oracle_filename vs port_filename" comment above
# vendor_linters.LINTERS). A `--check` fixture's skill-set (`--from`) tree
# therefore needs BOTH extensions present, so neither CLI's read of its own
# source file ever 404s — an uncaught FileNotFoundError/ENOENT on either side
# would produce a traceback that can never be byte-identical across runtimes,
# forbidden by this task's binding ruling on valueless-flag-style crashes.
#
# `--install`/`--stamp` are deliberately NOT covered by a fixture: they WRITE
# files under different names per implementation (`check-graph.mjs` vs
# `check_graph.py`), so the harness's blanket `assertEqual(o_files, p_files)`
# filesystem-snapshot check could never pass for either mode — for a reason
# structurally unrelated to correctness, not a bug to catch. `--check` is
# read-only and already reaches exit 0/1 without that trap.


def _stamp_digest(body):
    """The stamp digest of a body — sha256, first 12 hex chars — computed
    independently of vendor_linters.compute_stamp, so building fixture content
    never depends on the very code path a fixture exists to exercise."""
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:12]


def _stamped(body, name, comment):
    """A source body carrying a self-consistent stamp line, `comment`-prefixed
    (`#` for the `.py` port's own files, `//` for the `.mjs` oracle's)."""
    return f"{comment} @skills-linter: {name} sha256:{_stamp_digest(body)}\n{body}"


_VL_GRAPH_BODY_V1 = "def harvest():\n    return {'v': 1}\n"
_VL_GRAPH_BODY_V2 = "def harvest():\n    return {'v': 2}\n"
_VL_TRACE_BODY_V1 = "def analyze():\n    return {'v': 1}\n"


def _tree_vendor_check_missing():
    """--check, exit 1: the skill set has both linters (both extensions); the
    destination has neither vendored yet. Exercises REMEDY["missing"] for both
    linters — the exact path where Finding 1a's underscore/hyphen bug hid,
    because no fixture ever ran `--check` against a missing linter before."""
    return {
        "skillset/scripts/check_graph.py": _stamped(_VL_GRAPH_BODY_V1, "check-graph", "#"),
        "skillset/scripts/check_trace.py": _stamped(_VL_TRACE_BODY_V1, "check-trace", "#"),
        "skillset/scripts/check-graph.mjs": _stamped(_VL_GRAPH_BODY_V1, "check-graph", "//"),
        "skillset/scripts/check-trace.mjs": _stamped(_VL_TRACE_BODY_V1, "check-trace", "//"),
    }


def _tree_vendor_check_ok():
    """--check, exit 0: the destination is byte-identical to the skill set for
    both linters (both extensions) -> both report `ok`."""
    tree = _tree_vendor_check_missing()
    tree["dest/scripts/check_graph.py"] = tree["skillset/scripts/check_graph.py"]
    tree["dest/scripts/check_trace.py"] = tree["skillset/scripts/check_trace.py"]
    tree["dest/scripts/check-graph.mjs"] = tree["skillset/scripts/check-graph.mjs"]
    tree["dest/scripts/check-trace.mjs"] = tree["skillset/scripts/check-trace.mjs"]
    return tree


def _tree_vendor_check_drifted():
    """--check, exit 1: check-graph is `outdated` (destination untouched but
    self-consistent, from an OLDER skill-set body); check-trace is `modified`
    (destination's stamp no longer matches its own body — hand-edited after
    vendoring). Exercises REMEDY["outdated"] and REMEDY["modified"], the two
    REMEDY entries `vendor-check-missing` cannot reach."""
    tree = {
        "skillset/scripts/check_graph.py": _stamped(_VL_GRAPH_BODY_V2, "check-graph", "#"),
        "skillset/scripts/check-graph.mjs": _stamped(_VL_GRAPH_BODY_V2, "check-graph", "//"),
        "dest/scripts/check_graph.py": _stamped(_VL_GRAPH_BODY_V1, "check-graph", "#"),
        "dest/scripts/check-graph.mjs": _stamped(_VL_GRAPH_BODY_V1, "check-graph", "//"),
        "skillset/scripts/check_trace.py": _stamped(_VL_TRACE_BODY_V1, "check-trace", "#"),
        "skillset/scripts/check-trace.mjs": _stamped(_VL_TRACE_BODY_V1, "check-trace", "//"),
    }
    tree["dest/scripts/check_trace.py"] = _stamped(_VL_TRACE_BODY_V1, "check-trace", "#") + "hand-edited-line\n"
    tree["dest/scripts/check-trace.mjs"] = _stamped(_VL_TRACE_BODY_V1, "check-trace", "//") + "hand-edited-line\n"
    return tree


# The "real repo" fixtures: this repo's OWN current working-tree state (every
# file on disk right now, including uncommitted changes), read into a
# {relative_posix_path: content} dict ONCE at import time. Both the oracle
# run and the port run of a real-repo fixture replay this SAME captured dict
# via fresh() — so a file someone edits between the two runs can never be the
# source of a spurious mismatch, and the copy is deterministic across the
# whole test run.
_REAL_REPO_SKIP_DIRS = {
    "__pycache__", "node_modules", "dist", "build", "target", "coverage", ".next",
    ".git", ".skills",  # .skills is gitignored scratch output; irrelevant to the linters
}


def _read_repo_tree():
    tree = {}
    for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [d for d in dirnames if d not in _REAL_REPO_SKIP_DIRS]
        for name in filenames:
            full = Path(dirpath) / name
            rel = full.relative_to(REPO_ROOT).as_posix()
            try:
                tree[rel] = full.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue  # non-text/unreadable — none of the linters need it
    return tree


REAL_REPO_TREE = _read_repo_tree()

CORPUS = [
    {"id": "clean-repo", "linter": "check-trace", "argv": [], "tree": _tree_clean_repo(), "writes": False},
    {"id": "trace-errors", "linter": "check-trace", "argv": [], "tree": _tree_trace_errors(), "writes": False},
    {
        "id": "strict-warnings",
        "linter": "check-trace",
        "argv": ["--strict"],
        "tree": _tree_strict_warnings(),
        "writes": False,
    },
    {"id": "stale-graph", "linter": "check-graph", "argv": ["--verify"], "tree": _tree_stale_graph(), "writes": False},
    {"id": "vendor-no-mode", "linter": "vendor-linters", "argv": [], "tree": {}, "writes": False},
    {
        "id": "vendor-check-missing",
        "linter": "vendor-linters",
        "argv": ["--check", "--from", "skillset", "--to", "dest"],
        "tree": _tree_vendor_check_missing(),
        "writes": False,
    },
    {
        "id": "vendor-check-ok",
        "linter": "vendor-linters",
        "argv": ["--check", "--from", "skillset", "--to", "dest"],
        "tree": _tree_vendor_check_ok(),
        "writes": False,
    },
    {
        "id": "vendor-check-drifted",
        "linter": "vendor-linters",
        "argv": ["--check", "--from", "skillset", "--to", "dest"],
        "tree": _tree_vendor_check_drifted(),
        "writes": False,
    },
    {
        "id": "unparseable-trace-json",
        "linter": "check-trace",
        "argv": [],
        "tree": _tree_bad_trace_json(),
        "writes": False,
    },
    {"id": "absent-specs-dir", "linter": "check-trace", "argv": [], "tree": {}, "writes": False},
    {
        "id": "harvest-writes",
        "linter": "check-graph",
        "argv": [],
        "tree": _tree_harvest(),
        "writes": "docs/specs/GRAPH.md",
    },
    # Step 4's discrimination proof targets THIS fixture by id: --verify's
    # stdout line ("OK" vs "FAIL — GRAPH.md is stale ...") is directly
    # sensitive to check_graph.py's cap_list elision marker whenever a real
    # Summary card list exceeds cardCap (this repo's committed GRAPH.md
    # already has two "…(+N more)" cards, so it does).
    {"id": "real-repo", "linter": "check-graph", "argv": ["--verify"], "tree": REAL_REPO_TREE, "writes": False},
    # PYPORT-5.1, literally: check_graph --harvest run over THIS repo's own
    # specs must write a byte-identical GRAPH.md to the oracle's.
    {
        "id": "real-repo-harvest",
        "linter": "check-graph",
        "argv": [],
        "tree": REAL_REPO_TREE,
        "writes": "docs/specs/GRAPH.md",
    },
    # Bonus coverage: the full check-trace pipeline at real-world complexity
    # (many requirement/task/test files, several per directory, in whatever
    # order the real filesystem happens to hold them) — the strongest
    # available regression net for the Task-5 walk-order bug class.
    {"id": "real-repo-trace", "linter": "check-trace", "argv": [], "tree": REAL_REPO_TREE, "writes": False},
]


class OracleRetiredTest(unittest.TestCase):
    """Deliberately NOT gated on ORACLE_AVAILABLE: this is the tripwire that
    must actually RUN (and pass) once the `.mjs` files are gone, not skip
    alongside `Parity`."""

    def test_no_mjs_linters_remain(self):
        """[PYPORT-2.6] the oracle is retired once parity is proven."""
        self.assertEqual(sorted(p.name for p in SCRIPTS.glob("*.mjs")), [])


@unittest.skipUnless(ORACLE_AVAILABLE, "oracle unavailable: node absent or .mjs deleted")
class Parity(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.mkdtemp(prefix="parity-")
        self.addCleanup(shutil.rmtree, self.work, ignore_errors=True)

    def test_corpus(self):
        """[PYPORT-2.1][PYPORT-2.2][PYPORT-2.3][PYPORT-2.4][PYPORT-2.5][PYPORT-2.8][PYPORT-5.1]"""
        for fx in CORPUS:
            with self.subTest(fixture=fx["id"], linter=fx["linter"]):
                fresh(self.work, fx["tree"])
                o = run(oracle_cmd_for(fx, self.work), self.work)
                o_files = snapshot(self.work)

                fresh(self.work, fx["tree"])
                p = run(port_cmd_for(fx, self.work), self.work)
                p_files = snapshot(self.work)

                self.assertEqual(o.code, p.code, diagnose(fx["id"], fx["linter"], "exit code", o.code, p.code))
                self.assertEqual(o.out, p.out, diagnose(fx["id"], fx["linter"], "stdout", o.out, p.out))
                self.assertEqual(o.err, p.err, diagnose(fx["id"], fx["linter"], "stderr", o.err, p.err))
                self.assertEqual(
                    o_files, p_files, diagnose(fx["id"], fx["linter"], "filesystem", repr(o_files), repr(p_files))
                )
                target = fx.get("writes")
                if target:
                    self.assertIn(target, o_files, f"{fx['id']}: expected {target!r} to exist after the run")
                    self.assertIn(target, p_files, f"{fx['id']}: expected {target!r} to exist after the run")


if __name__ == "__main__":
    unittest.main()
