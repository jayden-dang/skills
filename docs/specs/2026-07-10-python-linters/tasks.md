# Tasks: Python spec linters (PYPORT)

**Goal:** Move the three spec linters from Node `.mjs` to Python 3.9 stdlib without changing a single byte of their observable behavior.

**Architecture:** Each `.mjs` linter gets a `.py` twin. The `.mjs` is the specification, not merely prior art: a differential parity corpus (`scripts/parity_test.py`) runs a fixture repo through both implementations and asserts stdout, stderr, exit code, and the resulting filesystem are identical. The `.mjs` files are deleted only once that corpus is green.

**Tech stack:** CPython 3.9.6 (the macOS Command Line Tools floor), standard library only. Tests are `unittest`. No pytest, no third-party packages, no network.

## Global Constraints

Copied verbatim into every task brief. These apply to every task.

- **Python floor is 3.9.6.** No `match` statement. No PEP 604 (`X | Y`) unions evaluated at runtime. No `tomllib` (3.11). Nothing outside the standard library.
- **Behavior-identical is the whole feature.** If you are unsure what the port should do, run the `.mjs` and copy its output. Never infer behavior from the Python you just wrote.
- **Test suites (both must be green during the dual-run window):**
  - Node: `node --test scripts/*.test.mjs` — the **glob**, never `node --test scripts/`, which executes `check-trace.mjs` as a test file and it exits 1.
  - Python: `python3 -m unittest discover -s scripts -t scripts -p "*_test.py"`
- **Trace lint:** `node scripts/check-trace.mjs` (exit 0). **Graph lint:** `node scripts/check-graph.mjs --verify` (exit 0).
- **Test annotation convention:** the requirement ID goes in the test's **docstring**, in brackets: `"""[PYPORT-1.1] normalize_path strips a line locator."""` `check-trace` greps test-file text, so this registers as a Citation. Node tests keep the existing convention: `test('[PYPORT-1.1] ...', ...)`.
- **Python test files MUST be named `*_test.py`.** `check-trace`'s default `testFilePattern` is `(\.(test|spec)\.[cm]?[jt]sx?$)|([/\\]tests?[/\\])|([/\\]e2e[/\\])|(_test\.(rs|go|py)$)|(\.rs$)`, and this repo's `testGlobs` is `["scripts"]`. A file named `test_foo.py` would **not** be scanned.
- **Fixture requirement IDs must be assembled at runtime** — `"ALPHA" + "-1.1"`, never the literal. A literal ID inside a scanned test file is read as a Citation and fires a bogus E1. This is the Fixture ID vs Citation distinction in `CONTEXT.md`.
- **`argparse` is forbidden for the primary flag parse.** All three oracles hand-roll `args.indexOf(...)` and tolerate unknown flags silently. `argparse` prints usage and exits 2 on an unknown flag — a behavior change.
- **Commit trailer:** every commit ends `Implements: PYPORT-N.M` (or `Guards: PYPORT-N.M`).
- **Do not delete any `.mjs` file before Task 11.**

## File Structure

| File | Responsibility |
|---|---|
| `scripts/check_graph.py` | **Create.** Port of `check-graph.mjs`. Exports `DEFAULTS` + 11 functions. |
| `scripts/check_trace.py` | **Create.** Port of `check-trace.mjs`. No exports today; gains `main(argv) -> int`. |
| `scripts/vendor_linters.py` | **Create.** Port of `vendor-linters.mjs`, plus the `legacy` verdict and consented migration. |
| `scripts/check_graph_test.py` | **Create.** Unit tests for the pure functions + graph + CLI. Twin of `check-graph.test.mjs`. |
| `scripts/check_trace_test.py` | **Create.** Twin of `check-trace.test.mjs`. Fixture-bearing → added to `trace.json`'s `ignore`. |
| `scripts/vendor_linters_test.py` | **Create.** Twin of `vendor-linters.test.mjs`. |
| `scripts/wiring_test.py` | **Create.** Twin of `check-graph.wiring.test.mjs` (SKILL.md/template markers). |
| `scripts/parity_test.py` | **Create.** The differential oracle. Deleted-oracle-aware skip. |
| `scripts/floor_test.py` | **Create.** 3.9-floor AST scan + stdlib-only import check. |
| `scripts/handover_test.py` | **Create.** Meta-test: Python-cited ID set ⊇ `.mjs`-cited ID set. |
| `scripts/check-trace.mjs` | **Modify** (Task 1: drop `${e.message}`), then **delete** (Task 11). |
| `scripts/check-graph.mjs` | **Modify** (Task 1: drop `${e.message}`), then **delete** (Task 11). |
| `scripts/vendor-linters.mjs` | **Delete** (Task 11). |
| `scripts/*.test.mjs` (4 files) | **Delete** (Task 11), after their Python twins exist. |
| `docs/agents/trace.json` | **Modify.** `ignore` gains `check_trace_test.py`. |
| `templates/agents/project.md` | **Modify.** Trace + Graph rows name the interpreter. |
| `templates/githooks/pre-push` | **Modify.** Invoke the Python linters. |
| `skills/{setup/setup-repo,discovery/brainstorm,review/code-review,execution/verify}/SKILL.md` | **Modify.** Name the Python linters. |
| `README.md` | **Modify.** Add a Node-free install path. |
| `DESIGN.md` | **Modify.** Script inventory (line 44) + artifact model (lines 64–80, add `GRAPH.md`). |

---

## Task 1: Stop emitting runtime-authored text (prerequisite)

Both oracles interpolate their JSON parser's exception message. V8 says `Expected property name or '}' in JSON at position 2`; CPython says `Expecting property name enclosed in double quotes: line 1 column 3 (char 2)`. Byte-identical stderr is unreachable while a runtime writes part of the message, so the oracle changes **first** — before any parity fixture touches this path.

**Files:**
- Modify: `scripts/check-trace.mjs` (line 59), `scripts/check-graph.mjs` (line 389)
- Test: `scripts/check-graph.wiring.test.mjs`

**Interfaces:** none changed. Stderr text only.

- [x] **Step 1 (RED).** Add to `scripts/check-graph.wiring.test.mjs` — **not** `check-graph.test.mjs`, which never defines `repo` (only the wiring file does, at line 6):
  ```js
  test('[PYPORT-1.10] no linter leaks its runtime JSON-parser message', () => {
    for (const f of ['scripts/check-trace.mjs', 'scripts/check-graph.mjs']) {
      const src = read(f);
      assert.doesNotMatch(src, /\$\{e\.message\}/, `${f} must not interpolate a runtime error`);
      assert.match(src, /could not parse \$\{p\}: invalid JSON/, `${f} states its own wording`);
    }
  });
  ```
- [x] **Step 2.** Run `node --test scripts/check-graph.wiring.test.mjs`. Expect **fail**: `scripts/check-trace.mjs must not interpolate a runtime error`.
- [x] **Step 3 (GREEN).** In both files replace the `console.error` template's `${e.message}` with the literal `invalid JSON`:
  `console.error(\`check-trace: could not parse ${p}: invalid JSON\`);` (and `check-graph:` in the other).
- [x] **Step 4.** **Re-stamp first, then run the suite** — editing the bodies staled both `# @skills-linter` digests, so running the suite now would fail the stamp test and the three drift tests for the wrong reason:
  `node scripts/vendor-linters.mjs --stamp --from .` then `node --test scripts/*.test.mjs`. Expect **75 pass, 0 fail** (74 today, plus the one added above).
- [x] **Step 5.** Commit: `fix(linters): emit our own JSON-parse diagnostic, not the runtime's` with trailer `Implements: PYPORT-1.10`.

_Requirements: PYPORT-1.10_

---

## Task 2: `check_graph.py` — pure functions

**Files:**
- Create: `scripts/check_graph.py`, `scripts/check_graph_test.py`
- Reference (read, do not modify): `scripts/check-graph.mjs` lines 1–200, `scripts/check-graph.test.mjs`

**Interfaces — Produces:**
- `DEFAULTS: dict` — `{"specsDir": "docs/specs", "graph": {"sourceRoots": [...], "sourceExts": [...], "cardCap": 12}}`. Keys stay **camelCase**: they are read from `docs/agents/trace.json`, a wire format.
- `normalize_path(token: str) -> str`
- `is_source_path(token: str, cfg: dict) -> bool`
- `dedupe_by_fullest(paths: list) -> list`
- `classify_role(line: str, block_label) -> str` — returns `'owns'` or `'touches'`
- `cap_list(items: list, cap: int) -> list`
- `extract_out_of_scope(req_text: str) -> list`
- `extract_interfaces(bodies: list) -> list`

- [x] **Step 1 (RED).** Create `scripts/check_graph_test.py` with one test per pure function, expected values copied from `scripts/check-graph.test.mjs` (an independent source of truth — do **not** recompute them from your port). Example:
  ```python
  def test_normalize_path_strips_locator(self):
      """[PYPORT-1.1] normalize_path reduces a locator to a bare path."""
      self.assertEqual(check_graph.normalize_path("Editor.tsx:208"), "Editor.tsx")
      self.assertEqual(check_graph.normalize_path("Editor.tsx:208 (~208-221)"), "Editor.tsx")
  ```
- [x] **Step 2.** Run `python3 -m unittest discover -s scripts -t scripts -p "*_test.py"`. Expect **fail**: `ModuleNotFoundError: No module named 'check_graph'`.
- [x] **Step 3 (GREEN).** Write `scripts/check_graph.py` with `DEFAULTS` and the eight symbols above. Every regex that relies on ASCII `\d`/`\w` semantics carries `re.ASCII`. `matchAll` → `re.finditer`; `.replace(re, '')` with `/g` → `re.sub`.
- [x] **Step 4.** Re-run the Python suite. Expect all pass. Cross-check three tokens against the oracle directly:
  `node -e "import('./scripts/check-graph.mjs').then(m=>console.log(m.normalizePath('Editor.tsx:127,172')))"` must equal the Python result.
- [x] **Step 5.** Commit with trailer `Implements: PYPORT-1.1`.

_Requirements: PYPORT-1.1_

---

## Task 3: `check_graph.py` — harvest, render, query, config

**Files:**
- Modify: `scripts/check_graph.py`, `scripts/check_graph_test.py`

**Interfaces — Consumes:** everything from Task 2.
**Interfaces — Produces:**
- `harvest(specs_dir: str, cfg: dict) -> dict` — `{"features": [...], "reverse": {...}, "shared": [...]}`
- `render_graph_md(graph: dict) -> str`
- `query(graph: dict, paths: list, keywords: list) -> list`
- `load_config(root: str) -> dict` — **raises `ConfigError`** on unparseable `trace.json`; never exits
- `class ConfigError(Exception)`

- [x] **Step 1 (RED).** Add to `check_graph_test.py`:
  ```python
  def test_load_config_raises_never_exits(self):
      """[PYPORT-1.8] load_config raises ConfigError instead of killing the process."""
      root = self._tmp_repo({"docs/agents/trace.json": "{ not json"})
      with self.assertRaises(check_graph.ConfigError):
          check_graph.load_config(root)
  ```
  plus harvest/render/query tests with expected values lifted from `check-graph.test.mjs`.
- [x] **Step 2.** Run the Python suite. Expect **fail**: `AttributeError: module 'check_graph' has no attribute 'ConfigError'`.
- [x] **Step 3 (GREEN).** Implement. Dict insertion order carries the reverse index's ordering, as JS object key order does. `sorted()` replaces `.sort()`; feature codes are `A-Z0-9`, where `localeCompare` and code-point order agree — the parity corpus is the arbiter, not this assumption.
- [x] **Step 4.** Run the Python suite (all pass), then `node --test scripts/*.test.mjs` (still green — you changed no `.mjs`).
- [x] **Step 5.** Commit with trailer `Implements: PYPORT-1.1, PYPORT-1.8`.

_Requirements: PYPORT-1.1, PYPORT-1.8_

---

## Task 4: `check_graph.py` — CLI, JSON fidelity, entry guard

**Files:**
- Modify: `scripts/check_graph.py`, `scripts/check_graph_test.py`

**Interfaces — Produces:**
- `main(argv: list) -> int` — returns an exit code, never calls `sys.exit`
- `_invoked_as_script() -> bool`

Flags: `--root R`, `--json`, `--query --path P --keyword K`, `--verify`, `--install`/`--check`/`--stamp` are **not** check-graph's. `--harvest` is **not parsed**: it is the fall-through default mode (`check-graph.mjs:435,441`). Unknown flags are ignored silently.

- [x] **Step 1 (RED).** Add CLI black-box tests using `subprocess`:
  ```python
  def test_json_is_byte_identical_to_node(self):
      """[PYPORT-1.5] --query --json output matches JSON.stringify(x, null, 2)."""
      # ensure_ascii=False is mandatory: the capList marker '…' and interface '—'
      # would otherwise be escaped to … / —.
  def test_runs_from_a_symlinked_path(self):
      """[PYPORT-1.6] a linter under a symlinked dir executes its CLI."""
  def test_import_does_not_run_main(self):
      """[PYPORT-1.7] importing the module executes no CLI."""
  def test_bad_trace_json_exits_1_with_our_wording(self):
      """[PYPORT-1.9][PYPORT-1.10] the CLI converts ConfigError to exit 1."""
  def test_verify_exits_zero_on_fresh_harvest(self):
      """[PYPORT-5.2] --verify exits 0 when GRAPH.md is fresh."""
  def test_flags_accepted_unchanged(self):
      """[PYPORT-1.4] every documented flag is accepted; unknown flags are ignored."""
  ```
- [x] **Step 2.** Run the Python suite. Expect **fail** on all six.
- [x] **Step 3 (GREEN).** Implement `main(argv) -> int`. Serialize with `json.dumps(obj, indent=2, ensure_ascii=False)` and `print(...)` (which appends the newline `console.log` does). Entry point:
  ```python
  def _invoked_as_script():
      argv0 = sys.argv[0] if sys.argv else None
      if not argv0:
          return False
      try:
          return os.path.realpath(argv0) == os.path.realpath(__file__)
      except OSError:
          return False

  if _invoked_as_script():
      sys.exit(main(sys.argv[1:]))
  ```
  Comparing `realpath` on both sides is what makes a copy under `/tmp` (a symlink to `/private/tmp` on macOS) actually run.
- [x] **Step 4.** Run both suites. Expect green. Then prove byte-identity by hand:
  `diff <(node scripts/check-graph.mjs --query --json --keyword graph) <(python3 scripts/check_graph.py --query --json --keyword graph)` → **no output**.
- [x] **Step 5.** Commit with trailer `Implements: PYPORT-1.4, PYPORT-1.5, PYPORT-1.6, PYPORT-1.7, PYPORT-1.9` and `Guards: PYPORT-5.2`.

_Requirements: PYPORT-1.4, PYPORT-1.5, PYPORT-1.6, PYPORT-1.7, PYPORT-1.9, PYPORT-5.2_

---

## Task 5: `check_trace.py`

`check-trace.mjs` exports nothing and exits at top level in three places. The port grows a `main(argv) -> int`.

**Files:**
- Create: `scripts/check_trace.py`, `scripts/check_trace_test.py`
- Modify: `docs/agents/trace.json` (add `check_trace_test.py` to `ignore`)

**Interfaces — Produces:** `main(argv: list) -> int`. Flags: `--strict`, `--json`, `--root R`.

- [x] **Step 1 (RED).** Create `scripts/check_trace_test.py`, porting `check-trace.test.mjs`. Its fixture IDs (`RET-1.1`, `RET-9.9`) must be **assembled at runtime**: `RET = "RET"; f"- **{RET}-1.1** ..."`. Add:
  ```python
  def test_ignore_excludes_a_fixture_bearing_file(self):
      """[PYPORT-5.3] the ignore substring list still excludes test files."""
  def test_zero_requirements_exits_zero(self):
      """[PYPORT-5.4] a repo with no requirements is a clean state."""
  ```
- [x] **Step 2.** Run the Python suite. Expect **fail**: `ModuleNotFoundError: No module named 'check_trace'`.
- [x] **Step 3 (GREEN).** Port `check-trace.mjs`. Keep the E1/E2/E3/W1/W2 codes, the ID grammar, strikethrough retirement, and the `ignore` substring filter (`rel.includes(s)` → `s in rel`) byte-for-byte in their messages.
- [x] **Step 4.** Add `"check_trace_test.py"` to `ignore` in `docs/agents/trace.json`. Without this, its Fixture IDs fire E1. Run `node scripts/check-trace.mjs` → exit 0.
- [x] **Step 5.** Run both suites; then `diff <(node scripts/check-trace.mjs --json) <(python3 scripts/check_trace.py --json)` → **no output**. This diff is necessary but weak: on a clean repo `errors` and `warnings` are both `[]`, so it never exercises array traversal order. A fixture with **several** E1/E2 errors belongs in Task 8's corpus, where ordering divergence would actually show.
- [x] **Step 6.** Commit with trailer `Implements: PYPORT-1.1` and `Guards: PYPORT-5.3, PYPORT-5.4`.

_Requirements: PYPORT-1.1, PYPORT-5.3, PYPORT-5.4_

---

## Task 6: `vendor_linters.py` — port

**Files:**
- Create: `scripts/vendor_linters.py`, `scripts/vendor_linters_test.py`

**Interfaces — Produces:**
- `LINTERS: dict` — name → `(oracle_filename, port_filename)`
- `compute_stamp(src: str) -> str` — 12-hex sha256 of the body, **stamp lines excluded**
- `read_stamp(src: str) -> dict | None` (use `typing.Optional[dict]`, not `dict | None`, on 3.9)
- `restamp(src: str, name: str) -> str` — idempotent
- `install(src_root, dest_root, scripts_dir="scripts") -> list`
- `check_drift(src_root, dest_root, scripts_dir="scripts") -> list`

The stamp comment becomes `# @skills-linter: <name> sha256:<12hex>`.

- [x] **Step 1 (RED).** Port `vendor-linters.test.mjs`. Expected digests come from `hashlib` computed independently in the test, never from `compute_stamp`.
  ```python
  def test_stamp_matches_body_hash(self):
      """[PYPORT-3.1] each linter's stamp is the sha256 of its own body."""
  ```
- [x] **Step 2.** Run the Python suite. Expect **fail**: no module `vendor_linters`.
- [x] **Step 3 (GREEN).** Implement. `check_drift` order matters: check `modified` (body ≠ its own stamp) **before** `outdated`, or a hand-edit that leaves the stamp line alone masquerades as `ok`.
- [x] **Step 4.** Run `python3 scripts/vendor_linters.py --stamp --from .` then the Python suite. Expect green.
- [x] **Step 5.** Commit with trailer `Implements: PYPORT-1.1, PYPORT-3.1`.

_Requirements: PYPORT-1.1, PYPORT-3.1_

---

## Task 7: The 3.9 floor and the stdlib-only rule

`py_compile` validates against the **running** interpreter, so a `match` statement compiles clean on a 3.12 runner and the test passes green while asserting nothing. The check must be interpreter-independent.

**Files:**
- Create: `scripts/floor_test.py`

**Two APIs the obvious implementation would reach for do not exist on 3.9.** Verified on 3.9.6:
`ast.Match` → `AttributeError`, and `sys.stdlib_module_names` → `AttributeError`. Referencing
either by attribute makes this test **crash on the exact interpreter it guards**, while passing
green on a 3.12 runner. Note also that a `match` statement is not parseable on 3.9 at all —
`ast.parse` raises `SyntaxError`, which *is* the detection there; the node-type walk only earns
its keep on a 3.10+ runner.

- [x] **Step 1 (RED).**
  ```python
  STDLIB_ALLOWLIST = {"ast","argparse","difflib","hashlib","json","os","pathlib","re",
                      "shutil","subprocess","sys","tempfile","typing","unittest"}

  def test_no_310_only_syntax(self):
      """[PYPORT-1.3] no module uses syntax newer than CPython 3.9."""
      for mod in ("check_graph.py", "check_trace.py", "vendor_linters.py"):
          src = (SCRIPTS / mod).read_text()
          try:
              tree = ast.parse(src)          # on 3.9 a `match` stmt raises here
          except SyntaxError as e:
              self.fail(f"{mod} is not parseable on this interpreter: {e}")
          # On 3.10+ `match` parses; compare by node-type NAME, never `ast.Match`.
          bad = [n for n in ast.walk(tree) if type(n).__name__ == "Match"]
          self.assertEqual(bad, [], f"{mod} uses a match statement (3.10+)")
          # PEP 604: a BinOp with BitOr used as an annotation (def-time TypeError on 3.9)
          for n in ast.walk(tree):
              ann = getattr(n, "annotation", None) or getattr(n, "returns", None)
              if isinstance(ann, ast.BinOp) and isinstance(ann.op, ast.BitOr):
                  self.fail(f"{mod} uses a PEP 604 `X | Y` annotation (3.10+)")

  def test_only_stdlib_imports(self):
      """[PYPORT-1.2] the linters import nothing outside the standard library."""
      # sys.stdlib_module_names is 3.10+. The allowlist is the PRIMARY check;
      # widen it opportunistically when the richer set exists.
      known = getattr(sys, "stdlib_module_names", None) or STDLIB_ALLOWLIST

  def test_compiles_under_a_real_39_interpreter_if_present(self):
      """[PYPORT-1.3] opportunistic: compile under python3.9 when discoverable."""
      # shutil.which("python3.9"), else /usr/bin/python3 if it reports 3.9; else skipTest
  ```
- [x] **Step 2.** Run the Python suite. Expect **fail**: `AssertionError` naming a module, not `AttributeError`. If you see `AttributeError: module 'ast' has no attribute 'Match'`, you wrote `isinstance(n, ast.Match)` — that is the bug this task exists to avoid.
- [x] **Step 3 (GREEN).** Make it pass by fixing any 3.10+ syntax in Tasks 2–6's output. Prove the scan discriminates: temporarily add `def f() -> dict | None: pass` to `check_graph.py`, re-run under `/usr/bin/python3`, watch it **fail**, then remove it.
- [x] **Step 4.** Commit with trailer `Implements: PYPORT-1.2, PYPORT-1.3`.

_Requirements: PYPORT-1.2, PYPORT-1.3_

---

## Task 8: The differential parity corpus

**Files:**
- Create: `scripts/parity_test.py`

**Interfaces — Produces:** `CORPUS: list[dict]` — each `{"id", "linter", "argv", "tree", "writes"}`.

- [x] **Step 1 (RED).** Write the harness. **One** working directory, re-materialized between the two runs:
  ```python
  ORACLE_AVAILABLE = NODE is not None and all((SCRIPTS / m).exists() for m, _ in LINTERS.values())

  @unittest.skipUnless(ORACLE_AVAILABLE, "oracle unavailable: node absent or .mjs deleted")
  class Parity(unittest.TestCase):
      def test_corpus(self):
          """[PYPORT-2.1][PYPORT-2.2][PYPORT-2.3][PYPORT-2.4][PYPORT-2.5][PYPORT-2.8][PYPORT-5.1]"""
          for fx in CORPUS:
              with self.subTest(fixture=fx["id"], linter=fx["linter"]):
                  fresh(work); o = run(oracle_cmd, work); o_files = snapshot(work)
                  fresh(work); p = run(port_cmd,   work); p_files = snapshot(work)
                  self.assertEqual(o.code, p.code, diagnose(...))
                  self.assertEqual(o.out,  p.out,  diagnose(...))
                  self.assertEqual(o.err,  p.err,  diagnose(...))
                  self.assertEqual(o_files, p_files, diagnose(...))
  ```
  Guard on **`ORACLE_AVAILABLE`**, not `NODE is None`: after Task 11 deletes the `.mjs` on a machine that still has node, the corpus must skip, not invoke a missing file and fail.
- [x] **Step 2.** Populate `CORPUS` covering every exit code and both stderr paths: clean repo (0); trace errors (1); `--strict` with warnings (1); stale `GRAPH.md` (1); `vendor-linters` with no mode (2); **unparseable `trace.json`** (1, stderr); **absent specs dir** (0, stderr); `--harvest` writing `GRAPH.md` (0, filesystem); and the real repo itself. Fixture IDs assembled at runtime.
- [x] **Step 3.** Run `python3 -m unittest discover -s scripts -t scripts -p "*_test.py"`. Every fixture must pass. Any mismatch prints the fixture, linter, stream, first differing byte offset, and a `difflib` unified diff.
- [x] **Step 4.** Prove the harness discriminates: temporarily change `check_graph.py`'s `cap_list` marker from `…` to `...`, re-run, watch the `real-repo` fixture **fail** on stdout, then revert.
- [x] **Step 5.** Commit with trailer `Implements: PYPORT-2.1, PYPORT-2.2, PYPORT-2.3, PYPORT-2.4, PYPORT-2.5, PYPORT-2.8` and `Guards: PYPORT-5.1`.

_Requirements: PYPORT-2.1, PYPORT-2.2, PYPORT-2.3, PYPORT-2.4, PYPORT-2.5, PYPORT-2.8, PYPORT-5.1_

---

## Task 9: Coverage handover before the oracle dies

The four `.mjs` test files are today the **only** covering tests for every FGRAPH-1.x…11.x and TRACE-1.x requirement. Deleting them without their twins turns `check-trace` red with dozens of E2 errors.

**Files:**
- Create: `scripts/wiring_test.py`, `scripts/handover_test.py`
- Modify: `scripts/check_graph_test.py`, `scripts/check_trace_test.py`, `scripts/vendor_linters_test.py`

- [x] **Step 1 (RED).** Write `scripts/handover_test.py`:
  ```python
  def test_python_tests_cite_every_id_the_mjs_tests_cite(self):
      """[PYPORT-2.7] no requirement loses its covering test when the .mjs go."""
      # Extract IDs from .mjs tests and .py tests. SKIP the files named in
      # docs/agents/trace.json's `ignore` on BOTH sides — otherwise the check
      # reads check-trace.test.mjs's Fixture IDs (RET-1.1, RET-9.9) as Citations
      # and forces check_trace_test.py to reproduce them.
      self.assertTrue(mjs_ids <= py_ids, f"orphaned: {sorted(mjs_ids - py_ids)}")
  ```
- [x] **Step 2.** Run it. Expect **fail**, listing every FGRAPH ID not yet cited by a Python test.
- [x] **Step 3 (GREEN).** Port `check-graph.wiring.test.mjs` → `scripts/wiring_test.py` (SKILL.md + template markers), and finish porting the remaining assertions of the other three suites, until `handover_test.py` is green.
- [x] **Step 4.** Run `node scripts/check-trace.mjs`. Expect exit 0 with no new E2.
- [x] **Step 5.** Commit with trailer `Guards: PYPORT-2.7`.

_Requirements: PYPORT-2.7_

---

## Task 10: `vendor_linters.py` — legacy verdict and consented migration

New behavior with **no oracle**; exempt from parity (PYPORT-2.8).

**Files:**
- Modify: `scripts/vendor_linters.py`, `scripts/vendor_linters_test.py`

**Interfaces — Produces:** `check_drift` gains the verdict `"legacy"`. `install(..., remove_legacy: bool = False)`.

- [x] **Step 1 (RED).** E2E tests against a scratch repo holding a vendored `check-trace.mjs`:
  ```python
  def test_vendored_mjs_reports_legacy(self):
      """[PYPORT-3.2] a .mjs where a .py is expected is `legacy`."""
  def test_install_writes_the_py_linters(self):
      """[PYPORT-3.3] install lands check_trace.py and check_graph.py."""
  def test_install_offers_to_remove_legacy(self):
      """[PYPORT-3.4] the legacy .mjs removal is offered."""
  def test_install_never_removes_without_consent(self):
      """[PYPORT-3.5] remove_legacy defaults False; the .mjs survives."""
  def test_modified_legacy_warns_before_removal(self):
      """[PYPORT-3.6] a hand-edited legacy copy warns that removal discards it."""
  ```
- [x] **Step 2.** Run the Python suite. Expect **fail** on all five.
- [x] **Step 3 (GREEN).** Implement. `remove_legacy` defaults to `False`; the CLI prompts and passes the answer through. A legacy file whose body does not hash to its own stamp is reported `modified` **and** `legacy`.
- [x] **Step 4.** Run `python3 scripts/vendor_linters.py --check --to ../bot` (read-only). Expect it to report `check-trace.mjs: legacy` and `check_graph.py: missing`. Confirm `git -C ../bot status --short scripts/` is empty.
- [x] **Step 5.** Commit with trailer `Implements: PYPORT-3.2, PYPORT-3.3, PYPORT-3.4, PYPORT-3.5, PYPORT-3.6`.

_Requirements: PYPORT-3.2, PYPORT-3.3, PYPORT-3.4, PYPORT-3.5, PYPORT-3.6_

---

## Task 11: Consumer surfaces

**Files:**
- Modify: `templates/agents/project.md`, `templates/githooks/pre-push`, `skills/setup/setup-repo/SKILL.md`, `skills/discovery/brainstorm/SKILL.md`, `skills/review/code-review/SKILL.md`, `skills/execution/verify/SKILL.md`, `README.md`, `DESIGN.md`
- Modify: `scripts/wiring_test.py`

- [x] **Step 1 (RED).** Extend `scripts/wiring_test.py`:
  ```python
  def test_project_md_template_names_the_interpreter(self):
      """[PYPORT-4.1] the Trace and Graph rows invoke the Python linters."""
  def test_pre_push_runs_both_python_linters(self):
      """[PYPORT-4.2] the hook template runs check_trace.py and check_graph.py --verify."""
  def test_skills_name_the_python_linters(self):
      """[PYPORT-4.3] setup-repo, brainstorm, code-review, verify all name the .py linters."""
  def test_readme_has_a_node_free_install(self):
      """[PYPORT-4.4] README documents git clone + link-skills.sh or the plugin."""
  def test_design_md_inventory_lists_the_linters_and_graph_md(self):
      """[PYPORT-4.5] DESIGN.md's script inventory and artifact model are current."""
  def test_setup_repo_treats_a_dead_interpreter_as_a_wiring_failure(self):
      """[PYPORT-4.6] the proving gate classifies an unrunnable linter as wiring."""
  def test_spec_templates_demand_no_new_fields(self):
      """[PYPORT-5.5] no graph/linter annotation is required in the spec triad."""
  def test_shell_scripts_stay_dependency_free(self):
      """[PYPORT-5.6] task-brief, review-package, link-skills.sh, session-start.sh are bash."""
  def test_graph_query_still_fails_open(self):
      """[PYPORT-5.7] brainstorm and code-review continue when the graph linter is absent."""
  ```
- [x] **Step 2.** Run the Python suite. Expect **fail** on all nine.
- [x] **Step 3 (GREEN).** Make each edit. `DESIGN.md:44` gains the Python linters; the artifact model at `DESIGN.md:64-80` gains `docs/specs/GRAPH.md`, which it has never listed.
- [x] **Step 4.** Mutation-check every marker: delete it in a scratch copy, confirm the mapped test fails, restore.
- [x] **Step 5.** Commit with trailer `Implements: PYPORT-4.1, PYPORT-4.2, PYPORT-4.3, PYPORT-4.4, PYPORT-4.5, PYPORT-4.6` and `Guards: PYPORT-5.5, PYPORT-5.6, PYPORT-5.7`.

_Requirements: PYPORT-4.1, PYPORT-4.2, PYPORT-4.3, PYPORT-4.4, PYPORT-4.5, PYPORT-4.6, PYPORT-5.5, PYPORT-5.6, PYPORT-5.7_

---

## Task 12: Retire the oracle

Do **not** start this task until Task 8's corpus is green and Task 9's handover test passes. That ordering *is* the gate for PYPORT-2.6 — the tripwire below asserts a committed-file fact, not the requirement's trigger.

**Files:**
- Delete: `scripts/check-trace.mjs`, `scripts/check-graph.mjs`, `scripts/vendor-linters.mjs`, `scripts/check-trace.test.mjs`, `scripts/check-graph.test.mjs`, `scripts/check-graph.wiring.test.mjs`, `scripts/vendor-linters.test.mjs`
- Modify: `docs/agents/trace.json` (drop `check-trace.test.mjs` from `ignore`), `scripts/parity_test.py`

- [x] **Step 1.** Re-run everything. `python3 -m unittest discover -s scripts -t scripts -p "*_test.py"` green; `node --test scripts/*.test.mjs` green; `node scripts/check-trace.mjs` exit 0; `node scripts/check-graph.mjs --verify` exit 0. If any is red, **stop** — the oracle stays.
- [x] **Step 2 (RED).** Add to `scripts/parity_test.py`:
  ```python
  def test_no_mjs_linters_remain(self):
      """[PYPORT-2.6] the oracle is retired once parity is proven."""
      self.assertEqual(sorted(p.name for p in SCRIPTS.glob("*.mjs")), [])
  ```
  Run it. Expect **fail**, listing seven `.mjs` files.
- [x] **Step 3 (GREEN).** `git rm` the seven files. Remove `check-trace.test.mjs` from `trace.json`'s `ignore` (the file is gone; a stale entry is a silent no-op that would hide a future file of the same name).
- [x] **Step 4.** Run the Python suite. `Parity` must now report **skipped** (`oracle unavailable: node absent or .mjs deleted`), not failed. `test_no_mjs_linters_remain` passes. `node scripts/check-trace.mjs` no longer exists — use `python3 scripts/check_trace.py`; expect exit 0.
- [x] **Step 5.** Regenerate the graph: `python3 scripts/check_graph.py --harvest`, then `--verify` → exit 0. Commit with trailer `Implements: PYPORT-2.6`.
- [x] **Step 6.** REQUIRED SUB-SKILL: use `sync-spec` to mark PYPORT `Implemented` and realign `INDEX.md`.

_Requirements: PYPORT-2.6_

---

## Coverage check

Every requirement is cited by a task footer **and** tagged on a real test.

| Req | Task | Tagged test |
|---|---|---|
| 1.1 | 2, 3, 5, 6 | `[PYPORT-1.1]` unit tests per module |
| 1.2 | 7 | `[PYPORT-1.2]` stdlib-only import scan |
| 1.3 | 7 | `[PYPORT-1.3]` AST scan + opportunistic 3.9 compile |
| 1.4 | 4 | `[PYPORT-1.4]` flags accepted; unknown ignored |
| 1.5 | 4 | `[PYPORT-1.5]` JSON byte-identity |
| 1.6 | 4 | `[PYPORT-1.6]` symlinked-path invocation |
| 1.7 | 4 | `[PYPORT-1.7]` import runs no CLI |
| 1.8 | 3 | `[PYPORT-1.8]` `load_config` raises `ConfigError` |
| 1.9 | 4 | `[PYPORT-1.9]` CLI converts the raise to exit 1 |
| 1.10 | 1 | `[PYPORT-1.10]` no `${e.message}`; also Task 4's CLI test |
| 2.1–2.5, 2.8 | 8 | `[PYPORT-2.1…2.5][PYPORT-2.8]` the parity corpus |
| 2.6 | 12 | `[PYPORT-2.6]` no `.mjs` remain (tripwire; the real gate is task order) |
| 2.7 | 9 | `[PYPORT-2.7]` handover superset meta-test |
| 3.1 | 6 | `[PYPORT-3.1]` stamp = sha256 of body |
| 3.2–3.6 | 10 | `[PYPORT-3.2…3.6]` legacy verdict + consented migration |
| 4.1–4.6 | 11 | `[PYPORT-4.1…4.6]` wiring markers |
| 5.1 | 8 | `[PYPORT-5.1]` filesystem snapshot diff (GRAPH.md) |
| 5.2 | 4 | `[PYPORT-5.2]` `--verify` exits 0 |
| 5.3 | 5 | `[PYPORT-5.3]` `ignore` substring filter |
| 5.4 | 5 | `[PYPORT-5.4]` zero requirements exits 0 |
| 5.5–5.7 | 11 | `[PYPORT-5.5…5.7]` guards |

**Reconciliation with the design's seam table:** every seam row is exercised. Two carry the caveats `design.md` records: PYPORT-1.3's seam is an interpreter-independent AST scan (a `py_compile` check would pass green on a 3.12 runner while asserting nothing), and PYPORT-2.6's seam is a tripwire — its substantive gate is that Tasks 8 and 9 are green before Task 12 runs. No requirement is left untagged; none was found wrong or infeasible, so no upstream sync-back was needed beyond PYPORT-1.10, which was added during design.
