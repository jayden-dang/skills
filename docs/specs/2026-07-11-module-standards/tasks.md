# Tasks: Per-Module Standards Resolution

Feature code: MODSTD
Status: Implemented
Date: 2026-07-12
Requirements: ./requirements.md
Design: ./design.md

**Goal:** Add an inline standards layer (a project baseline + optional per-module
overrides) with an effective-standards resolver, a validity check, and a
`check-graph --standards <CODE>` emit mode.

**Architecture:** All production code is in `scripts/check_graph.py`; all tests
in `scripts/check_graph_test.py` (Python `unittest`). `load_manifest` carries a
new additive `standards` field; a pure `_standards_errors` validates baseline +
module standards (called unconditionally by `--verify`); a pure
`resolve_standards` merges baseline + a module's rules; a `--standards` branch in
`main` prints the resolved list.

**Tech Stack:** Python 3, standard library only.

## Global Constraints

- **Stdlib only.** No third-party imports. No new top-level import side effects —
  every new symbol is a `def` or a conditional inside `main` (MODSTD-4.4).
- **Re-stamp after every edit to `scripts/check_graph.py`.** Before committing a
  task that changed that file, run `python3 scripts/vendor_linters.py --stamp`
  and include the restamped file in the commit. Verify with
  `python3 scripts/vendor_linters.py --check` (must print `OK`).
- **All suites green before a task is done:**
  `python3 scripts/check_graph_test.py`,
  `python3 scripts/vendor_linters_test.py`,
  `python3 scripts/wiring_test.py`,
  `python3 evals/evals.py --strict`,
  `python3 scripts/check_trace.py`.
- **Traceability tags.** Every requirement ID must appear in a canonical
  `# covers MODSTD-N.M` comment (hyphen-dot form) inside the test that exercises
  it.
- **Commit trailer.** Each task's final commit ends with `Implements: MODSTD-N.M`
  (the IDs that task delivers). No other trailer.
- **A `standards` value is valid iff** it is absent (`None`) or a **list of
  non-empty strings**; an empty list `[]` is valid ("no standards"). This one
  rule governs both `_standards_errors` (reports a malformed value) and
  `resolve_standards` (skips malformed items).

## File structure

| File | Change | Responsibility |
|---|---|---|
| `scripts/check_graph.py` | modify | Carry `module["standards"]`; add `_standards_errors`, `resolve_standards`; call the validator in `_run_verify`; add a `--standards` branch to `main`. |
| `scripts/check_graph_test.py` | modify | Add a `LoadManifestTest` case; add `StandardsErrorsTest`, `ResolveStandardsTest`, `StandardsVerifyTest`, `StandardsCliTest`. |

All tasks touch these same two files, so `execute-plan` runs them serially
regardless of the `Depends-on` edges; the edges record the true data
dependencies.

---

## Task 1 — `load_manifest` carries `module["standards"]`

**Files:**
- Modify: `scripts/check_graph.py` — the module dict built in `load_manifest`
  (`:822-828`, after `"owner": entry.get("owner"),`).
- Test: `scripts/check_graph_test.py` — add a method to the existing
  `LoadManifestTest` class (`:1236`).

**Interfaces:**
- Produces: each loaded module dict gains `"standards": entry.get("standards")`
  (the raw value, carried verbatim; `None` when absent). Existing fields
  code/name/owns/layer/owner unchanged.

**Depends-on:** none

**Steps:**
- [ ] Add to `LoadManifestTest`:
  ```python
  def test_load_manifest_carries_standards_MODSTD_1_2_4_2(self):
      # covers MODSTD-1.2, MODSTD-4.2
      cfg = {"modules": [{"code": "AUTH", "name": "Auth", "owns": ["src/auth/**"],
                          "standards": ["Rule one"]}]}
      mods, errs = check_graph.load_manifest(cfg)
      self.assertEqual(errs, [])
      m = mods[0]
      self.assertEqual(m["standards"], ["Rule one"])          # 1.2 carried
      for key in ("code", "name", "owns", "layer", "owner"):  # 4.2 existing fields intact
          self.assertIn(key, m)
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k test_load_manifest_carries_standards`
  → expect failure: `KeyError: 'standards'`.
- [ ] In `load_manifest`'s built dict (after `"owner": entry.get("owner"),`), add:
  ```python
          "standards": entry.get("standards"),
  ```
- [ ] Run the same `-k` command → expect pass.
- [ ] Re-stamp (`--stamp` then `--check` → `OK`).
- [ ] Run the full suite → expect green.
- [ ] Commit: `feat(check-graph): carry per-module standards on the loaded manifest` +
  trailer `Implements: MODSTD-1.2, MODSTD-4.2`.

_Requirements: MODSTD-1.2, MODSTD-4.2_

---

## Task 2 — `_standards_errors`: validate baseline + module standards

**Files:**
- Modify: `scripts/check_graph.py` — add `_standards_errors` after `load_manifest`
  (ends `:829`).
- Test: `scripts/check_graph_test.py` — add a `StandardsErrorsTest(unittest.TestCase)`
  class after `LoadManifestTest`.

**Interfaces:**
- Produces: `_standards_errors(cfg) -> [error_str, ...]` — pure; empty when every
  `standards` value (baseline and each module entry) is valid; one error string
  per malformed value, labelled `baseline` or `module <code|#i>`. Never raises.

**Depends-on:** none

**Steps:**
- [ ] Add the `StandardsErrorsTest` class:
  ```python
  class StandardsErrorsTest(unittest.TestCase):
      def test_valid_and_absent_standards_no_error_MODSTD_1_5(self):
          # covers MODSTD-1.5
          cfg = {"standards": ["A", "B"],
                 "modules": [{"code": "AUTH", "standards": []},   # [] is valid
                             {"code": "BILL"}]}                    # omitted is valid
          self.assertEqual(check_graph._standards_errors(cfg), [])

      def test_malformed_baseline_flagged_MODSTD_1_4(self):
          # covers MODSTD-1.4
          for bad in ("nope", [""], [1], ["ok", ""]):
              errs = check_graph._standards_errors({"standards": bad})
              self.assertTrue(any("baseline" in e for e in errs), bad)

      def test_malformed_module_standards_flagged_MODSTD_1_3(self):
          # covers MODSTD-1.3
          cfg = {"modules": [{"code": "AUTH", "standards": "notalist"},
                             {"code": "BILL", "standards": [""]}]}
          errs = check_graph._standards_errors(cfg)
          self.assertTrue(any("AUTH" in e for e in errs))
          self.assertTrue(any("BILL" in e for e in errs))

      def test_never_raises_on_junk(self):
          # defensive: non-list modules / non-dict entries never crash
          self.assertIsInstance(check_graph._standards_errors({"modules": "x"}), list)
          self.assertIsInstance(check_graph._standards_errors({"modules": [1, "y"]}), list)
          self.assertIsInstance(check_graph._standards_errors({}), list)
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k StandardsErrorsTest` → expect
  failure: `AttributeError: module 'check_graph' has no attribute '_standards_errors'`.
- [ ] Add `_standards_errors` after `load_manifest`:
  ```python
  def _standards_errors(cfg):
      """Validate the baseline and per-module `standards` lists. Returns a list of
      error strings (empty when all valid); never raises. A `standards` value,
      when present, must be a list of non-empty strings ([] is valid)."""
      errors = []

      def bad(value):
          return value is not None and not (
              isinstance(value, list) and all(isinstance(s, str) and s for s in value))

      if bad(cfg.get("standards")):
          errors.append("E: baseline 'standards' must be a list of non-empty strings")
      raw = cfg.get("modules")
      if isinstance(raw, list):
          for i, entry in enumerate(raw):
              if not isinstance(entry, dict):
                  continue
              if bad(entry.get("standards")):
                  code = entry.get("code")
                  label = code if isinstance(code, str) and code else f"#{i + 1}"
                  errors.append(
                      f"E: module {label} 'standards' must be a list of non-empty strings")
      return errors
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k StandardsErrorsTest` → expect pass.
- [ ] Re-stamp (`--stamp` then `--check` → `OK`).
- [ ] Run the full suite → expect green.
- [ ] Commit: `feat(check-graph): validate baseline and per-module standards` +
  trailer `Implements: MODSTD-1.3, MODSTD-1.4, MODSTD-1.5`.

_Requirements: MODSTD-1.3, MODSTD-1.4, MODSTD-1.5_

---

## Task 3 — `resolve_standards`: effective standards for a module

**Files:**
- Modify: `scripts/check_graph.py` — add `resolve_standards` after
  `_standards_errors`.
- Test: `scripts/check_graph_test.py` — add a `ResolveStandardsTest(unittest.TestCase)`
  class after `StandardsErrorsTest`.

**Interfaces:**
- Produces: `resolve_standards(code, cfg) -> [rule_str, ...]` — pure, total,
  defensive; baseline rules then the module's rules, deduplicated keeping first
  occurrence; unknown code → baseline alone; malformed items skipped.

**Depends-on:** none

**Steps:**
- [ ] Add the `ResolveStandardsTest` class:
  ```python
  class ResolveStandardsTest(unittest.TestCase):
      def _cfg(self, baseline=None, module_standards=None):
          cfg = {"modules": [{"code": "AUTH", "name": "M", "owns": ["src/x/**"]}]}
          if baseline is not None:
              cfg["standards"] = baseline
          if module_standards is not None:
              cfg["modules"][0]["standards"] = module_standards
          return cfg

      def test_baseline_then_module_MODSTD_1_1_2_1(self):
          # covers MODSTD-1.1, MODSTD-2.1
          cfg = self._cfg(baseline=["A", "B"], module_standards=["C"])
          self.assertEqual(check_graph.resolve_standards("AUTH", cfg), ["A", "B", "C"])

      def test_dedupe_first_occurrence_MODSTD_2_2(self):
          # covers MODSTD-2.2
          cfg = self._cfg(baseline=["A"], module_standards=["A", "B"])
          self.assertEqual(check_graph.resolve_standards("AUTH", cfg), ["A", "B"])

      def test_unknown_code_baseline_only_MODSTD_2_3(self):
          # covers MODSTD-2.3
          cfg = self._cfg(baseline=["A"], module_standards=["C"])
          self.assertEqual(check_graph.resolve_standards("NOPE", cfg), ["A"])

      def test_nothing_declared_empty_MODSTD_2_4(self):
          # covers MODSTD-2.4
          self.assertEqual(check_graph.resolve_standards("AUTH", {"modules": []}), [])
          self.assertEqual(check_graph.resolve_standards("AUTH", {}), [])

      def test_malformed_values_skipped_not_crashing(self):
          # resolve is total/defensive (validity is a separate --verify concern)
          cfg = self._cfg(baseline="foo", module_standards=["", "ok", 1])
          self.assertEqual(check_graph.resolve_standards("AUTH", cfg), ["ok"])

      def test_import_still_inert_MODSTD_4_4(self):
          # covers MODSTD-4.4
          import importlib, io, contextlib
          out_buf, err_buf = io.StringIO(), io.StringIO()
          with contextlib.redirect_stdout(out_buf), contextlib.redirect_stderr(err_buf):
              mod = importlib.reload(check_graph)
          self.assertEqual(out_buf.getvalue(), "")
          self.assertEqual(err_buf.getvalue(), "")
          self.assertTrue(hasattr(mod, "resolve_standards"))
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k ResolveStandardsTest` → expect
  failure: `AttributeError: module 'check_graph' has no attribute 'resolve_standards'`.
- [ ] Add `resolve_standards` after `_standards_errors`:
  ```python
  def resolve_standards(code, cfg):
      """Resolve a module's effective standards: the baseline standards followed
      by that module's own standards, deduplicated (first occurrence kept). Total
      and defensive — non-list values and non-string/empty items are skipped, so a
      malformed config never crashes resolution (validity is a --verify concern).
      An unknown code yields the baseline alone."""
      def clean(value):
          if not isinstance(value, list):
              return []
          return [s for s in value if isinstance(s, str) and s]

      baseline = clean(cfg.get("standards"))
      module = []
      raw = cfg.get("modules")
      if isinstance(raw, list):
          for entry in raw:
              if isinstance(entry, dict) and entry.get("code") == code:
                  module = clean(entry.get("standards"))
                  break
      out, seen = [], set()
      for s in baseline + module:
          if s not in seen:
              seen.add(s)
              out.append(s)
      return out
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k ResolveStandardsTest` → expect pass.
- [ ] Re-stamp (`--stamp` then `--check` → `OK`).
- [ ] Run the full suite → expect green.
- [ ] Commit: `feat(check-graph): resolve effective standards for a module` +
  trailer `Implements: MODSTD-1.1, MODSTD-2.1, MODSTD-2.2, MODSTD-2.3, MODSTD-2.4, MODSTD-4.4`.

_Requirements: MODSTD-1.1, MODSTD-2.1, MODSTD-2.2, MODSTD-2.3, MODSTD-2.4, MODSTD-4.4_

---

## Task 4 — `--verify` runs the standards validator unconditionally

**Files:**
- Modify: `scripts/check_graph.py` — in `_run_verify`, after the boundary-check
  block (ends `:965`) and before `if as_json:` (`:967`).
- Test: `scripts/check_graph_test.py` — add a `StandardsVerifyTest(_FixtureTestCase)`
  class after `VerifyIntegrationTest`.

**Interfaces:**
- Consumes: `_standards_errors(cfg)` (Task 2); the existing `errors` list and
  `--json` output shape `{"errors": [...], "warnings": [...]}` in `_run_verify`.
- Produces: standards validity errors surfaced by `--verify`, affecting its exit
  code, whether or not any module is declared.

**Depends-on:** Task 2

**Steps:**
- [ ] Add the `StandardsVerifyTest` class:
  ```python
  class StandardsVerifyTest(_FixtureTestCase):
      def _verify(self, trace):
          import io, contextlib
          root = self._tmp_repo({"docs/agents/trace.json": json.dumps(trace)})
          os.makedirs(os.path.join(root, "docs/specs"), exist_ok=True)
          open(os.path.join(root, "docs/specs/INDEX.md"), "w").close()
          check_graph.main(["--harvest", "--root", root])   # non-stale GRAPH.md
          buf = io.StringIO()
          with contextlib.redirect_stdout(buf):
              rc = check_graph.main(["--verify", "--root", root, "--json"])
          return rc, json.loads(buf.getvalue())

      def test_no_standards_verify_unchanged_MODSTD_4_1(self):
          # covers MODSTD-4.1
          rc, payload = self._verify({"specsDir": "docs/specs"})
          self.assertEqual(rc, 0)
          self.assertEqual(payload["errors"], [])

      def test_malformed_baseline_fails_verify_without_modules_MODSTD_1_4(self):
          # covers MODSTD-1.4 (end-to-end: reported even with NO modules declared)
          rc, payload = self._verify({"specsDir": "docs/specs", "standards": "notalist"})
          self.assertEqual(rc, 1)
          self.assertTrue(any("baseline" in e for e in payload["errors"]))
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k StandardsVerifyTest` → expect
  the malformed-baseline test to fail (rc 0, no error) — the validator is not wired
  in yet.
- [ ] In `_run_verify`, immediately after the boundary block (after the
  `elif modules:` body ending at `:965`) and before `if as_json:`, add at the
  top level of the function body:
  ```python
      errors.extend(_standards_errors(cfg))
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k StandardsVerifyTest` → expect pass.
- [ ] Re-stamp (`--stamp` then `--check` → `OK`).
- [ ] Run the full suite → expect green.
- [ ] Commit: `feat(check-graph): report standards validity from --verify` +
  trailer `Implements: MODSTD-1.4, MODSTD-4.1`.

_Requirements: MODSTD-1.4, MODSTD-4.1_

---

## Task 5 — `--standards`: the CLI emit branch

**Files:**
- Modify: `scripts/check_graph.py` — in `main`, insert a `--standards` branch
  after the `--seed` branch (`:1015-1017`) and before the `# default: --harvest`
  comment (`:1019`).
- Test: `scripts/check_graph_test.py` — add a `StandardsCliTest(_FixtureTestCase)`
  class after `SeedCliTest`.

**Interfaces:**
- Consumes: `resolve_standards(code, cfg)` (Task 3); `load_manifest(cfg)`
  (existing) for the declared module codes; `_collect_flag(argv, name)` (existing,
  `:879-885`) — returns `[None]` when the flag is the last token.
- Produces: `check-graph --standards <CODE>` prints
  `{"module": <CODE>, "standards": [...]}` and returns 0 for a declared module;
  errors to stderr and returns 1 for a missing or unknown code.

**Depends-on:** Task 3

**Steps:**
- [ ] Add the `StandardsCliTest` class:
  ```python
  class StandardsCliTest(_FixtureTestCase):
      def _repo(self, standards=None, module_standards=None):
          trace = {"specsDir": "docs/specs",
                   "graph": {"sourceRoots": ["src"], "sourceExts": ["ts"]},
                   "modules": [{"code": "AUTH", "name": "Auth", "owns": ["src/auth/**"]}]}
          if standards is not None:
              trace["standards"] = standards
          if module_standards is not None:
              trace["modules"][0]["standards"] = module_standards
          return self._tmp_repo({"docs/agents/trace.json": json.dumps(trace)})

      def test_standards_emits_resolved_json_MODSTD_3_1(self):
          # covers MODSTD-3.1
          import io, contextlib
          root = self._repo(standards=["No default exports"],
                            module_standards=["Auth behind AuthGuard"])
          buf = io.StringIO()
          with contextlib.redirect_stdout(buf):
              rc = check_graph.main(["--standards", "AUTH", "--root", root])
          self.assertEqual(rc, 0)
          self.assertEqual(json.loads(buf.getvalue()),
                           {"module": "AUTH",
                            "standards": ["No default exports", "Auth behind AuthGuard"]})

      def test_unknown_code_errors_MODSTD_3_2(self):
          # covers MODSTD-3.2
          import io, contextlib
          root = self._repo()
          out, err = io.StringIO(), io.StringIO()
          with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
              rc = check_graph.main(["--standards", "NOPE", "--root", root])
          self.assertEqual(rc, 1)
          self.assertEqual(out.getvalue(), "")           # nothing on stdout
          self.assertIn("NOPE", err.getvalue())

      def test_missing_code_errors_MODSTD_3_3(self):
          # covers MODSTD-3.3
          # --standards is the LAST token, so _collect_flag yields [None]
          import io, contextlib
          root = self._repo()
          err = io.StringIO()
          with contextlib.redirect_stderr(err):
              rc = check_graph.main(["--root", root, "--standards"])
          self.assertEqual(rc, 1)
          self.assertTrue(err.getvalue())

      def test_output_deterministic_MODSTD_3_4(self):
          # covers MODSTD-3.4
          import io, contextlib
          root = self._repo(standards=["A", "B"], module_standards=["C"])
          def run():
              buf = io.StringIO()
              with contextlib.redirect_stdout(buf):
                  check_graph.main(["--standards", "AUTH", "--root", root])
              return buf.getvalue()
          self.assertEqual(run(), run())

      def test_standards_writes_nothing_MODSTD_4_3(self):
          # covers MODSTD-4.3
          import io, contextlib
          root = self._repo(standards=["A"])
          before = _tree_snapshot(root)
          with contextlib.redirect_stdout(io.StringIO()):
              check_graph.main(["--standards", "AUTH", "--root", root])
          self.assertEqual(_tree_snapshot(root), before)
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k StandardsCliTest` → expect
  failure (no `--standards` branch: JSON parse of empty stdout / rc mismatch).
- [ ] In `main`, insert between the `--seed` branch and the `# default: --harvest`
  comment:
  ```python
      if "--standards" in argv:
          values = _collect_flag(argv, "--standards")
          code = values[0] if values else None
          if not code:
              print("check-graph: --standards requires a module code", file=sys.stderr)
              return 1
          modules, _errs = load_manifest(cfg)
          known = {m["code"] for m in modules if m.get("code")}
          if code not in known:
              print(f"check-graph: unknown module code {code}", file=sys.stderr)
              return 1
          print(json.dumps({"module": code, "standards": resolve_standards(code, cfg)},
                           indent=2, ensure_ascii=False))
          return 0
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k StandardsCliTest` → expect pass.
- [ ] Re-stamp (`--stamp` then `--check` → `OK`).
- [ ] Run the full suite → expect green.
- [ ] Commit: `feat(check-graph): add --standards mode that prints resolved standards` +
  trailer `Implements: MODSTD-3.1, MODSTD-3.2, MODSTD-3.3, MODSTD-3.4, MODSTD-4.3`.

_Requirements: MODSTD-3.1, MODSTD-3.2, MODSTD-3.3, MODSTD-3.4, MODSTD-4.3_

---

## Coverage map

| Requirement | Task | Tagged test |
|---|---|---|
| MODSTD-1.1 | 3 | `test_baseline_then_module` |
| MODSTD-1.2 | 1 | `test_load_manifest_carries_standards` |
| MODSTD-1.3 | 2 | `test_malformed_module_standards_flagged` |
| MODSTD-1.4 | 2, 4 | `test_malformed_baseline_flagged`, `test_malformed_baseline_fails_verify_without_modules` |
| MODSTD-1.5 | 2 | `test_valid_and_absent_standards_no_error` |
| MODSTD-2.1 | 3 | `test_baseline_then_module` |
| MODSTD-2.2 | 3 | `test_dedupe_first_occurrence` |
| MODSTD-2.3 | 3 | `test_unknown_code_baseline_only` |
| MODSTD-2.4 | 3 | `test_nothing_declared_empty` |
| MODSTD-3.1 | 5 | `test_standards_emits_resolved_json` |
| MODSTD-3.2 | 5 | `test_unknown_code_errors` |
| MODSTD-3.3 | 5 | `test_missing_code_errors` |
| MODSTD-3.4 | 5 | `test_output_deterministic` |
| MODSTD-4.1 | 4 | `test_no_standards_verify_unchanged` |
| MODSTD-4.2 | 1 | `test_load_manifest_carries_standards` |
| MODSTD-4.3 | 5 | `test_standards_writes_nothing` |
| MODSTD-4.4 | 3 | `test_import_still_inert` |

Build order: {Task 1, Task 2, Task 3} → Task 4 (needs Task 2) and Task 5 (needs
Task 3). All tasks share `scripts/check_graph.py` + `scripts/check_graph_test.py`,
so `execute-plan` serializes them into one worker regardless.
