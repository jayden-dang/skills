# Tasks: Brownfield On-Ramp — Manifest Seed

Feature code: MODSEED
Status: Approved
Date: 2026-07-11
Requirements: ./requirements.md
Design: ./design.md

**Goal:** Add a `check-graph --seed` mode that drafts a module manifest from a
repo's directory tree and prints it as JSON for a human to paste into
`trace.json` — read-only, deterministic, and round-trip-valid.

**Architecture:** All production code is in `scripts/check_graph.py`; all tests
in `scripts/check_graph_test.py` (Python `unittest`). A pure normalizer
`_seed_code` turns a directory name into a valid module code; a pure `seed`
builder walks the source tree (reusing `enumerate_folders`) and returns
`{"modules": [...]}`; a thin `--seed` branch in `main` prints it.

**Tech Stack:** Python 3, standard library only.

## Global Constraints

- **Stdlib only.** No third-party imports. No new top-level import side effects —
  every new symbol is a `def` or a conditional inside `main` (MODSEED-4.4).
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
  `# covers MODSEED-N.M` comment (hyphen-dot form) inside the test that exercises
  it — Python method names use underscores, and `check_trace.py` scans for the
  canonical hyphen-dot ID.
- **Commit trailer.** Each task's final commit ends with `Implements: MODSEED-N.M`
  (the IDs that task delivers). No other trailer.
- **Test on a real `src/` tree, not this repo.** `--seed` against this repo emits
  `{"modules": []}` (none of the default source roots — `src`, `crates`, … —
  exist here). Every seed test MUST build a `_tmp_repo` with a real `src/…` tree.
- **macOS is case-insensitive.** Two directory names that differ only in case are
  the *same* directory on disk. To test a code collision, use two names that
  differ otherwise but normalize to the same code (e.g. `auth` and `au.th` both
  → `AUTH`) — never `auth`/`AUTH`.

## File structure

| File | Change | Responsibility |
|---|---|---|
| `scripts/check_graph.py` | modify | Add `_seed_code` and `seed`; add a `--seed` branch to `main`. |
| `scripts/check_graph_test.py` | modify | Add `SeedCodeTest`, `SeedTest`, `SeedCliTest` (+ a `_tree_snapshot` helper). |

All three tasks touch these same two files, so `execute-plan` runs them serially
regardless of the `Depends-on` edges; the edges still record the true data
dependencies.

---

## Task 1 — `_seed_code`: directory name → valid module code

**Files:**
- Modify: `scripts/check_graph.py` — add `_seed_code` immediately after
  `load_manifest` (which ends ~`:829`); it uses only string ops (the module
  regex `_MODULE_CODE_RE` at `:781` is referenced only by the tests here).
- Test: `scripts/check_graph_test.py` — add a `SeedCodeTest(unittest.TestCase)`
  class (place it after the existing `LoadManifestTest`).

**Interfaces:**
- Produces: `_seed_code(name: str) -> str` — pure; always returns a string
  matching `^[A-Z][A-Z0-9]{1,11}$` (2–12 chars, uppercase alnum, letter-first).

**Depends-on:** none

**Steps:**
- [ ] Add the `SeedCodeTest` class (complete code):
  ```python
  class SeedCodeTest(unittest.TestCase):
      CODE_RE = r"^[A-Z][A-Z0-9]{1,11}$"

      def test_normalizes_names_to_valid_codes_MODSEED_1_3(self):
          # covers MODSEED-1.3
          cases = {"auth": "AUTH", "my-service": "MYSERVICE",
                   "AUTHENTICATION": "AUTHENTICATI"}   # 14 chars -> first 12
          for name, code in cases.items():
              self.assertEqual(check_graph._seed_code(name), code)
              self.assertRegex(code, self.CODE_RE)

      def test_repairs_and_pads_to_valid_code_MODSEED_1_4(self):
          # covers MODSEED-1.4
          cases = {"2024": "M2024", "a": "A0", "___": "M0", "x": "X0", "": "M0"}
          for name, code in cases.items():
              self.assertEqual(check_graph._seed_code(name), code)
              self.assertRegex(code, self.CODE_RE)
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k SeedCodeTest` → expect failure:
  `AttributeError: module 'check_graph' has no attribute '_seed_code'`.
- [ ] Add `_seed_code` after `load_manifest`:
  ```python
  def _seed_code(name):
      """Normalize a directory name to a valid module code matching
      _MODULE_CODE_RE (2-12 chars, uppercase alnum, letter-first). Total and
      deterministic: defined for every string."""
      s = "".join(c for c in name.upper() if "A" <= c <= "Z" or "0" <= c <= "9")
      if not s or not s[0].isalpha():
          s = "M" + s               # ensure a leading letter (also covers empty)
      s = s[:12]                     # ensure <= 12 chars
      if len(s) < 2:
          s = s + "0"               # ensure >= 2 chars (single-letter / 'M'-only)
      return s
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k SeedCodeTest` → expect pass.
- [ ] Re-stamp: `python3 scripts/vendor_linters.py --stamp` then `--check` (`OK`).
- [ ] Run the full suite (all five commands) → expect green.
- [ ] Commit: `feat(check-graph): normalize directory names to module codes` +
  trailer `Implements: MODSEED-1.3, MODSEED-1.4`.

_Requirements: MODSEED-1.3, MODSEED-1.4_

---

## Task 2 — `seed`: draft the manifest from the tree

**Files:**
- Modify: `scripts/check_graph.py` — add `seed` immediately after `_seed_code`.
- Test: `scripts/check_graph_test.py` — add a `SeedTest(_FixtureTestCase)` class
  (after `SeedCodeTest`).

**Interfaces:**
- Consumes: `_seed_code(name)` (Task 1); `enumerate_folders(root, cfg) ->
  (repo_folders, source_folders)` (existing, `:391`); `_MODULE_CODE_RE`
  (existing, `:781`).
- Produces: `seed(root, cfg) -> {"modules": [ {"code","name","owns"}, … ]}` —
  pure, read-only, deterministic; modules sorted by code, each `owns` sorted;
  never reads `cfg["modules"]`.

**Depends-on:** Task 1

**Steps:**
- [ ] Add the `SeedTest` class (complete code):
  ```python
  class SeedTest(_FixtureTestCase):
      def _cfg(self):
          return {"specsDir": "docs/specs",
                  "graph": {"sourceRoots": ["src"], "sourceExts": ["ts"],
                            "cardCap": 12, "queryCap": 8}}

      def test_drafts_one_module_per_child_dir_MODSEED_1_1_1_2_1_5(self):
          # covers MODSEED-1.1, MODSEED-1.2, MODSEED-1.5
          root = self._tmp_repo({"src/auth/a.ts": "x", "src/billing/b.ts": "x"})
          out = check_graph.seed(root, self._cfg())
          by_code = {m["code"]: m for m in out["modules"]}
          self.assertEqual(set(by_code), {"AUTH", "BILLING"})
          self.assertEqual(by_code["AUTH"]["owns"], ["src/auth/**"])   # 1.2
          self.assertEqual(by_code["AUTH"]["name"], "auth")            # 1.5

      def test_ignores_grandchildren_and_loose_files_MODSEED_1_1(self):
          # covers MODSEED-1.1
          root = self._tmp_repo({"src/auth/deep/c.ts": "x", "src/top.ts": "x"})
          out = check_graph.seed(root, self._cfg())
          # only the immediate child 'auth' becomes a module; 'deep' (grandchild)
          # and loose root files do not.
          self.assertEqual([m["code"] for m in out["modules"]], ["AUTH"])
          self.assertEqual(out["modules"][0]["owns"], ["src/auth/**"])

      def test_code_collision_gets_suffix_MODSEED_1_6(self):
          # covers MODSEED-1.6
          # 'auth' and 'au.th' are distinct dirs that both normalize to AUTH ->
          # one keeps AUTH, the other becomes AUTH2 (case-insensitive-FS safe).
          root = self._tmp_repo({"src/auth/a.ts": "x", "src/au.th/b.ts": "x"})
          out = check_graph.seed(root, self._cfg())
          self.assertEqual(sorted(m["code"] for m in out["modules"]),
                           ["AUTH", "AUTH2"])

      def test_output_is_deterministic_and_sorted_MODSEED_2_2(self):
          # covers MODSEED-2.2
          root = self._tmp_repo({"src/zebra/z.ts": "x", "src/alpha/a.ts": "x"})
          out1 = check_graph.seed(root, self._cfg())
          self.assertEqual(out1, check_graph.seed(root, self._cfg()))
          codes = [m["code"] for m in out1["modules"]]
          self.assertEqual(codes, sorted(codes))          # modules sorted by code

      def test_draft_round_trips_through_load_manifest_MODSEED_3_1_3_2(self):
          # covers MODSEED-3.1, MODSEED-3.2
          root = self._tmp_repo({"src/auth/a.ts": "x", "src/2fa/b.ts": "x",
                                 "src/x/c.ts": "x"})
          out = check_graph.seed(root, self._cfg())
          for m in out["modules"]:
              self.assertTrue(m["code"] and m["name"] and m["owns"])   # 3.2 non-empty
          mods, errs = check_graph.load_manifest({"modules": out["modules"]})
          self.assertEqual(errs, [])                                   # 3.1 zero errors

      def test_ignores_existing_manifest_MODSEED_4_2(self):
          # covers MODSEED-4.2
          cfg = dict(self._cfg(),
                     modules=[{"code": "OLD", "name": "Old", "owns": ["legacy/**"]}])
          root = self._tmp_repo({"src/auth/a.ts": "x"})
          out = check_graph.seed(root, cfg)
          self.assertEqual([m["code"] for m in out["modules"]], ["AUTH"])  # OLD ignored

      def test_import_still_inert_MODSEED_4_4(self):
          # covers MODSEED-4.4
          import importlib, io, contextlib
          out_buf, err_buf = io.StringIO(), io.StringIO()
          with contextlib.redirect_stdout(out_buf), contextlib.redirect_stderr(err_buf):
              mod = importlib.reload(check_graph)
          self.assertEqual(out_buf.getvalue(), "")
          self.assertEqual(err_buf.getvalue(), "")
          self.assertTrue(hasattr(mod, "seed"))
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k SeedTest` → expect failure:
  `AttributeError: module 'check_graph' has no attribute 'seed'`.
- [ ] Add `seed` after `_seed_code`:
  ```python
  def seed(root, cfg):
      """Draft a module manifest from the repo's source tree. Pure and
      read-only: returns {"modules": [...]} sorted by code (each 'owns' sorted);
      writes nothing; ignores any existing cfg['modules']."""
      repo_folders, _ = enumerate_folders(root, cfg)
      folderset = set(repo_folders)
      existing_roots = [r for r in cfg["graph"]["sourceRoots"] if r in folderset]
      drafts = []  # (code, {code,name,owns})
      for f in repo_folders:
          for r in existing_roots:
              if f.startswith(r + "/") and "/" not in f[len(r) + 1:]:
                  name = f.rsplit("/", 1)[-1]
                  drafts.append((_seed_code(name),
                                 {"name": name, "owns": [f + "/**"]}))
                  break
      # deterministic collision suffixing over sorted drafts
      drafts.sort(key=lambda d: (d[0], d[1]["owns"]))
      used = set()
      modules = []
      for code, mod in drafts:
          if code in used:
              n = 2
              while True:
                  suffix = str(n)
                  cand = code[:12 - len(suffix)] + suffix
                  if cand not in used and _MODULE_CODE_RE.match(cand):
                      break
                  n += 1
              code = cand
          used.add(code)
          modules.append({"code": code, "name": mod["name"],
                          "owns": sorted(mod["owns"])})
      modules.sort(key=lambda m: m["code"])
      return {"modules": modules}
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k SeedTest` → expect pass.
- [ ] Re-stamp (`--stamp` then `--check` → `OK`).
- [ ] Run the full suite → expect green.
- [ ] Commit: `feat(check-graph): draft a module manifest from the source tree` +
  trailer `Implements: MODSEED-1.1, MODSEED-1.2, MODSEED-1.5, MODSEED-1.6, MODSEED-2.2, MODSEED-3.1, MODSEED-3.2, MODSEED-4.2, MODSEED-4.4`.

_Requirements: MODSEED-1.1, MODSEED-1.2, MODSEED-1.5, MODSEED-1.6, MODSEED-2.2, MODSEED-3.1, MODSEED-3.2, MODSEED-4.2, MODSEED-4.4_

---

## Task 3 — `--seed`: the CLI branch

**Files:**
- Modify: `scripts/check_graph.py` — in `main`, insert a `--seed` branch after
  the `--verify` branch (`:965-966`) and before the `# default: --harvest`
  comment (`:968`).
- Test: `scripts/check_graph_test.py` — add a module-level `_tree_snapshot`
  helper and a `SeedCliTest(_FixtureTestCase)` class (after `VerifyIntegrationTest`).

**Interfaces:**
- Consumes: `seed(root, cfg)` (Task 2); `main(argv) -> int` (existing, `:931`);
  `root` and `cfg` already bound in `main` at `:939`/`:943`.
- Produces: `check-graph --seed` prints one `{"modules": [...]}` JSON object to
  stdout and returns 0.

**Depends-on:** Task 2

**Steps:**
- [ ] Add a module-level helper near the top of `check_graph_test.py` (after the
  imports), used by the isolation test:
  ```python
  def _tree_snapshot(root):
      """Map every file under `root` to its bytes — for asserting nothing changed."""
      snap = {}
      for dirpath, _dirs, filenames in os.walk(root):
          for fn in filenames:
              p = os.path.join(dirpath, fn)
              with open(p, "rb") as fh:
                  snap[os.path.relpath(p, root)] = fh.read()
      return snap
  ```
- [ ] Add the `SeedCliTest` class:
  ```python
  class SeedCliTest(_FixtureTestCase):
      def test_seed_emits_modules_json_MODSEED_2_1_2_3(self):
          # covers MODSEED-2.1, MODSEED-2.3
          import io, contextlib
          root = self._tmp_repo({"src/auth/a.ts": "x"})
          buf = io.StringIO()
          with contextlib.redirect_stdout(buf):
              rc = check_graph.main(["--seed", "--root", root])
          self.assertEqual(rc, 0)                                     # 2.3
          payload = json.loads(buf.getvalue())                        # 2.1 one JSON object
          self.assertEqual(payload["modules"][0]["code"], "AUTH")

      def test_seed_empty_when_no_source_root_MODSEED_2_4(self):
          # covers MODSEED-2.4
          import io, contextlib
          root = self._tmp_repo({"docs/readme.md": "x"})              # no src/ etc.
          buf = io.StringIO()
          with contextlib.redirect_stdout(buf):
              rc = check_graph.main(["--seed", "--root", root])
          self.assertEqual(rc, 0)
          self.assertEqual(json.loads(buf.getvalue()), {"modules": []})

      def test_seed_writes_nothing_MODSEED_4_1(self):
          # covers MODSEED-4.1
          import io, contextlib
          root = self._tmp_repo({"src/auth/a.ts": "x"})
          before = _tree_snapshot(root)
          with contextlib.redirect_stdout(io.StringIO()):
              check_graph.main(["--seed", "--root", root])
          self.assertEqual(_tree_snapshot(root), before)              # nothing created/changed

      def test_seed_short_circuits_before_harvest_MODSEED_4_3(self):
          # covers MODSEED-4.3
          import io, contextlib
          root = self._tmp_repo({"src/auth/a.ts": "x", "docs/specs/INDEX.md": ""})
          with contextlib.redirect_stdout(io.StringIO()):
              rc = check_graph.main(["--seed", "--root", root])
          self.assertEqual(rc, 0)
          # --seed must not fall through to --harvest: no GRAPH.md written
          self.assertFalse(os.path.exists(os.path.join(root, "docs/specs/GRAPH.md")))
          # and --harvest itself still works, unchanged, when invoked directly
          with contextlib.redirect_stdout(io.StringIO()):
              check_graph.main(["--harvest", "--root", root])
          self.assertTrue(os.path.exists(os.path.join(root, "docs/specs/GRAPH.md")))
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k SeedCliTest` → expect failure
  (no `--seed` branch yet: `test_seed_emits_modules_json` fails to parse an empty
  stdout as JSON, and `test_seed_short_circuits` finds GRAPH.md was written).
- [ ] In `main`, insert between the `--verify` branch and the `# default:
  --harvest` comment:
  ```python
      if "--seed" in argv:
          print(json.dumps(seed(root, cfg), indent=2, ensure_ascii=False))
          return 0
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k SeedCliTest` → expect pass.
- [ ] Re-stamp (`--stamp` then `--check` → `OK`).
- [ ] Run the full suite → expect green.
- [ ] Commit: `feat(check-graph): add --seed mode that prints a drafted manifest` +
  trailer `Implements: MODSEED-2.1, MODSEED-2.3, MODSEED-2.4, MODSEED-4.1, MODSEED-4.3`.

_Requirements: MODSEED-2.1, MODSEED-2.3, MODSEED-2.4, MODSEED-4.1, MODSEED-4.3_

---

## Coverage map

| Requirement | Task | Tagged test |
|---|---|---|
| MODSEED-1.1 | 2 | `test_drafts_one_module_per_child_dir`, `test_ignores_grandchildren_and_loose_files` |
| MODSEED-1.2 | 2 | `test_drafts_one_module_per_child_dir` |
| MODSEED-1.3 | 1 | `test_normalizes_names_to_valid_codes` |
| MODSEED-1.4 | 1 | `test_repairs_and_pads_to_valid_code` |
| MODSEED-1.5 | 2 | `test_drafts_one_module_per_child_dir` |
| MODSEED-1.6 | 2 | `test_code_collision_gets_suffix` |
| MODSEED-2.1 | 3 | `test_seed_emits_modules_json` |
| MODSEED-2.2 | 2 | `test_output_is_deterministic_and_sorted` |
| MODSEED-2.3 | 3 | `test_seed_emits_modules_json` |
| MODSEED-2.4 | 3 | `test_seed_empty_when_no_source_root` |
| MODSEED-3.1 | 2 | `test_draft_round_trips_through_load_manifest` |
| MODSEED-3.2 | 2 | `test_draft_round_trips_through_load_manifest` |
| MODSEED-4.1 | 3 | `test_seed_writes_nothing` |
| MODSEED-4.2 | 2 | `test_ignores_existing_manifest` |
| MODSEED-4.3 | 3 | `test_seed_short_circuits_before_harvest` |
| MODSEED-4.4 | 2 | `test_import_still_inert` |

Build order: Task 1 → Task 2 → Task 3. All three share `scripts/check_graph.py`
+ `scripts/check_graph_test.py`, so `execute-plan` serializes them into one
worker regardless.
