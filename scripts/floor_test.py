"""floor_test.py — guards the Python 3.9 floor and the stdlib-only rule for
the linters.

Why this can't be `py_compile`: `py_compile` validates against the
**running** interpreter, so a `match` statement compiles clean on a 3.12
runner and a py_compile-only test passes green while asserting nothing.
The primary checks here are interpreter-independent: they walk the AST by
node-type NAME and a hand-rolled STDLIB_ALLOWLIST, never `ast.Match` or
`sys.stdlib_module_names` — both are 3.10+-only attributes that raise
AttributeError on the CPython 3.9 floor this file exists to guard. See each
test's docstring for the specific trap it avoids.
"""
import ast
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent

MODULES = ("check_graph.py", "check_trace.py", "vendor_linters.py")

# The PRIMARY stdlib-membership check. `sys.stdlib_module_names` (3.10+) is
# used to opportunistically widen this, never to replace it — referencing it
# by attribute unconditionally would crash this test on 3.9.
STDLIB_ALLOWLIST = {
    "ast",
    "argparse",
    "difflib",
    "hashlib",
    "json",
    "os",
    "pathlib",
    "re",
    "shutil",
    "subprocess",
    "sys",
    "tempfile",
    "typing",
    "unittest",
}


def _top_level_import_names(tree):
    """Yield the top-level module name of every `import x[.y]` / `from x[.y] import ...`
    in `tree`. A `from . import y` / `from .x import y` (relative import, level > 0)
    names no external module and is skipped."""
    for node in ast.walk(tree):
        kind = type(node).__name__
        if kind == "Import":
            for alias in node.names:
                yield alias.name.split(".")[0]
        elif kind == "ImportFrom":
            if getattr(node, "level", 0):
                continue  # relative import — not a third-party/stdlib name
            if node.module:
                yield node.module.split(".")[0]


def _annotation_slot_nodes(tree):
    """Yield every annotation-slot AST node in `tree`: an `arg`'s `.annotation`,
    a `FunctionDef`/`AsyncFunctionDef`'s `.returns`, and an `AnnAssign`'s
    `.annotation`. Checked independently (not `a or b`) because a node could in
    principle carry both slots, and `or` would silently skip a present-but-falsy
    one. A plain `Assign`/expression node has neither attribute, so a bitwise-or
    used as a *value* (`flags = re.A | re.M`, or the RHS of `x: int = A | B`)
    is never yielded here — only the annotation itself is."""
    for node in ast.walk(tree):
        ann = getattr(node, "annotation", None)
        if ann is not None:
            yield ann
        returns = getattr(node, "returns", None)
        if returns is not None:
            yield returns


def _find_pep604_unions(tree):
    """Return every BinOp/BitOr node found ANYWHERE inside an annotation
    subtree — not just sitting directly at the annotation's root. This catches
    a union nested inside a generic, e.g. `List[int | str]` or
    `Dict[str, int | None]`, which parses as a `Subscript` at the annotation
    root (not a bare `BinOp`) with the `BinOp`/`BitOr` one level down in the
    subscript's slice."""
    violations = []
    for ann in _annotation_slot_nodes(tree):
        for n in ast.walk(ann):
            if isinstance(n, ast.BinOp) and isinstance(n.op, ast.BitOr):
                violations.append(n)
    return violations


def scan_source(src, filename="<string>"):
    """Parse `src` and return a list of human-readable 3.10+-only-syntax
    violation messages: a `match` statement, or a PEP 604 `X | Y` union
    anywhere inside an annotation. Raises `SyntaxError` if `src` doesn't parse
    on this interpreter (e.g. a `match` statement on a pre-3.10 runner — the
    caller should treat that itself as the detection). Factored out so tests
    can feed it synthetic snippets directly instead of mutating real files."""
    tree = ast.parse(src, filename=filename)
    violations = []
    if any(type(n).__name__ == "Match" for n in ast.walk(tree)):
        violations.append(f"{filename} uses a match statement (3.10+)")
    if _find_pep604_unions(tree):
        violations.append(f"{filename} uses a PEP 604 `X | Y` annotation (3.10+)")
    return violations


class FloorTest(unittest.TestCase):
    """the 3.9-floor / stdlib-only guard for the linters."""

    def test_no_310_only_syntax(self):
        """no module uses syntax newer than CPython 3.9."""
        for mod in MODULES:
            src = (SCRIPTS / mod).read_text(encoding="utf-8")
            try:
                violations = scan_source(src, filename=mod)
            except SyntaxError as e:
                # On 3.9 a `match` statement (or other 3.10+ grammar) raises
                # right here — this IS the detection on the floor interpreter.
                self.fail(f"{mod} is not parseable on this interpreter: {e}")
            # On 3.10+ `match` parses fine, so it must be caught by walking
            # the tree and comparing node-type NAME — never `ast.Match`,
            # which doesn't exist as an attribute on 3.9. PEP 604 (`X | Y`)
            # unions are syntactically ordinary BinOp/BitOr nodes on every
            # version — they parse fine even on 3.9 — but evaluating one as a
            # live annotation raises TypeError at def-time on 3.9
            # (`type.__or__` doesn't exist before 3.10). See `scan_source`.
            self.assertEqual(violations, [], "; ".join(violations))

    def test_detects_pep604_union_nested_in_parameter_annotation(self):
        """a PEP 604 union nested inside a subscripted parameter
        annotation (e.g. `List[int | str]`) is flagged, not just a bare
        top-level union."""
        src = "from typing import List\ndef f(x: List[int | str]):\n    pass\n"
        violations = scan_source(src, filename="synthetic_param.py")
        self.assertTrue(
            any("PEP 604" in v for v in violations),
            f"expected a PEP 604 violation for a nested union, got {violations}",
        )

    def test_detects_pep604_union_nested_in_variable_annotation(self):
        """a PEP 604 union nested inside a subscripted variable
        annotation (e.g. `Dict[str, int | None]`) is flagged, not just a bare
        top-level union."""
        src = "from typing import Dict\nx: Dict[str, int | None] = {}\n"
        violations = scan_source(src, filename="synthetic_var.py")
        self.assertTrue(
            any("PEP 604" in v for v in violations),
            f"expected a PEP 604 violation for a nested union, got {violations}",
        )

    def test_does_not_flag_bitwise_or_used_as_a_value(self):
        """a bitwise-or used as an ordinary expression VALUE
        (never an annotation) is not a PEP 604 union and must not be flagged."""
        src = (
            "import re\n"
            "flags = re.A | re.M\n"
            "x: int = A | B\n"  # the annotation is `int`; the union is on the value side
        )
        violations = scan_source(src, filename="synthetic_value.py")
        self.assertEqual(violations, [], f"unexpected violation(s): {violations}")

    def test_only_stdlib_imports(self):
        """the linters import nothing outside the standard library."""
        # sys.stdlib_module_names is 3.10+. STDLIB_ALLOWLIST is the PRIMARY
        # check; widen it opportunistically only when the richer set exists.
        known = getattr(sys, "stdlib_module_names", None) or STDLIB_ALLOWLIST
        for mod in MODULES:
            src = (SCRIPTS / mod).read_text(encoding="utf-8")
            tree = ast.parse(src, filename=mod)
            for name in _top_level_import_names(tree):
                self.assertIn(name, known, f"{mod} imports non-stdlib module {name!r}")

    def test_compiles_under_a_real_39_interpreter_if_present(self):
        """opportunistic: compile under python3.9 when discoverable."""
        interpreter = shutil.which("python3.9")
        if not interpreter:
            candidate = "/usr/bin/python3"
            try:
                probe = subprocess.run(
                    [candidate, "--version"],
                    capture_output=True,
                    text=True,
                    check=False,
                )
            except OSError:
                probe = None
            reported = (probe.stdout + probe.stderr) if probe else ""
            if probe is not None and probe.returncode == 0 and "Python 3.9" in reported:
                interpreter = candidate
        if not interpreter:
            self.skipTest("no python3.9 interpreter discoverable (checked PATH and /usr/bin/python3)")
        for mod in MODULES:
            result = subprocess.run(
                [interpreter, "-m", "py_compile", str(SCRIPTS / mod)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(
                result.returncode,
                0,
                f"{mod} failed to compile under {interpreter}: {result.stderr}",
            )


if __name__ == "__main__":
    unittest.main()
