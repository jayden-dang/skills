# Tasks: Module Manifest & Boundary Linting

> **For agentic workers:** REQUIRED SUB-SKILL: use `execute-plan` to implement
> this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

Feature code: MODMAP
Status: Approved
Date: 2026-07-11
Requirements: ./requirements.md
Design: ./design.md

**Goal:** Add a module manifest (folder-glob → module) and a `--verify` boundary
check to `scripts/check_graph.py`, proving every source folder maps to exactly
one module, while staying purely additive.

**Architecture:** All production code lives in `scripts/check_graph.py` (stdlib
only), all tests in `scripts/check_graph_test.py` (`unittest`). New pure
functions (`load_manifest`, `_glob_to_re`, `resolve_module`, `enumerate_folders`,
`_verify_boundaries`) are wired into the existing `_run_verify`, which gains a
non-failing `warnings` channel. The manifest is read from a new `modules` key in
`docs/agents/trace.json`, which the unchanged `load_config` already passes
through.

**Tech Stack:** Python 3 standard library (`json`, `os`, `re`, `sys`), `unittest`.

## Global Constraints

- **Python standard library only** — no third-party imports, ever. Allowed:
  `json`, `os`, `re`, `sys` (already imported in `check_graph.py`).
- **No top-level side effects on import** — every new symbol is a `def`, a
  compiled regex, or a module-level dict/constant. No function runs at import
  time; the only entry point stays the guarded `if _invoked_as_script():` block.
- **After editing `scripts/check_graph.py`, re-stamp it:**
  `python3 scripts/vendor_linters.py --stamp` (the file carries a
  `# @skills-linter: check-graph sha256:…` line that must match its body, or
  `vendor_linters_test.py` fails).
- **All of these must stay green** after every task:
  `python3 scripts/check_graph_test.py`,
  `python3 scripts/vendor_linters_test.py`,
  `python3 scripts/wiring_test.py`,
  `python3 evals/evals.py --strict`.
- **Test tagging:** every test method name or docstring names the requirement
  IDs it covers as `MODMAP-N.M` (e.g. `def test_orphan_folder_is_error_MODMAP_3_2`).
- **Existing behavior is load-bearing:** do not change `harvest`, `query`,
  `render_graph_md`, `load_config`, or the two existing `_run_verify` checks
  (GRAPH.md freshness, INDEX.md registration). Only *append* to `_run_verify`.
- **The module-code shape is uppercase** `^[A-Z][A-Z0-9]{1,11}$` — the same
  namespace the harvest extractor and `check_trace.py` already use.

## File Structure

| File | Responsibility |
|---|---|
| `scripts/check_graph.py` | MODIFY — add the five new functions + a `warnings` channel in `_run_verify`. |
| `scripts/check_graph_test.py` | MODIFY — add unit + integration tests for each new function. |

> All five tasks modify these two files, so `execute-plan` runs them **serially**
> (its disjoint-surface check demotes them from any parallel wave). The
> `Depends-on` lines below still record the true logical graph.

---

### Task 1: Manifest loader + validation

**Files:**
- Modify: `scripts/check_graph.py` (add after the `load_config` function)
- Test: `scripts/check_graph_test.py`

**Interfaces:**
- Consumes: `cfg` dict from `load_config` (has `specsDir`, `graph`, and an
  optional pass-through `modules` list).
- Produces: `load_manifest(cfg) -> (modules, validity_errors)` where a **module**
  is `{"code": str, "name": str, "owns": [str], "layer": str|None, "owner": str|None}`
  and `validity_errors` is a `list[str]`. Also the constant
  `_MODULE_CODE_RE = re.compile(r"^[A-Z][A-Z0-9]{1,11}$")`.

**Depends-on:** none

- [ ] **Step 1: Write the failing test**

Add to `scripts/check_graph_test.py`:

```python
class LoadManifestTest(unittest.TestCase):
    def test_absent_modules_key_disables_layer_MODMAP_1_1_4_1(self):
        mods, errs = check_graph.load_manifest({"specsDir": "docs/specs", "graph": {}})
        self.assertEqual(mods, [])
        self.assertEqual(errs, [])

    def test_valid_entry_parsed_with_optional_fields_MODMAP_1_1_1_2(self):
        cfg = {"modules": [
            {"code": "BILLING", "name": "Billing", "owns": ["src/billing/**"],
             "layer": "domain", "owner": "@team-pay"}]}
        mods, errs = check_graph.load_manifest(cfg)
        self.assertEqual(errs, [])
        self.assertEqual(len(mods), 1)
        self.assertEqual(mods[0]["code"], "BILLING")
        self.assertEqual(mods[0]["owns"], ["src/billing/**"])
        self.assertEqual(mods[0]["layer"], "domain")
        self.assertEqual(mods[0]["owner"], "@team-pay")

    def test_missing_required_fields_error_MODMAP_1_3(self):
        cfg = {"modules": [{"code": "A1", "owns": ["src/**"]},           # no name
                           {"code": "B1", "name": "B", "owns": []},      # empty owns
                           {"name": "C", "owns": ["src/c/**"]}]}         # no code
        mods, errs = check_graph.load_manifest(cfg)
        blob = "\n".join(errs)
        self.assertIn("A1", blob)
        self.assertIn("B1", blob)
        self.assertIn("missing", blob.lower())

    def test_duplicate_code_error_MODMAP_1_4(self):
        cfg = {"modules": [{"code": "DUP", "name": "One", "owns": ["src/a/**"]},
                           {"code": "DUP", "name": "Two", "owns": ["src/b/**"]}]}
        _, errs = check_graph.load_manifest(cfg)
        self.assertTrue(any("duplicate" in e.lower() and "DUP" in e for e in errs))

    def test_malformed_code_error_MODMAP_1_5(self):
        cfg = {"modules": [{"code": "lower", "name": "L", "owns": ["src/l/**"]}]}
        _, errs = check_graph.load_manifest(cfg)
        self.assertTrue(any("malformed" in e.lower() and "lower" in e for e in errs))

    def test_load_config_keeps_config_when_modules_present_MODMAP_4_4(self):
        import os, tempfile, shutil, json as _json
        root = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, root)
        os.makedirs(os.path.join(root, "docs/agents"))
        with open(os.path.join(root, "docs/agents/trace.json"), "w") as f:
            _json.dump({"specsDir": "docs/specs",
                        "modules": [{"code": "M1", "name": "M", "owns": ["src/**"]}]}, f)
        cfg = check_graph.load_config(root)
        self.assertEqual(cfg["specsDir"], "docs/specs")
        self.assertIn("sourceRoots", cfg["graph"])         # defaults still merged
        mods, errs = check_graph.load_manifest(cfg)
        self.assertEqual(errs, [])
        self.assertEqual(mods[0]["code"], "M1")
```

Run: `python3 scripts/check_graph_test.py` — expect: `AttributeError: module 'check_graph' has no attribute 'load_manifest'`.

- [ ] **Step 2: Implement** — add to `scripts/check_graph.py` after `load_config`:

```python
_MODULE_CODE_RE = re.compile(r"^[A-Z][A-Z0-9]{1,11}$")


def load_manifest(cfg):
    """Parse and validate the module manifest from cfg['modules'].

    Returns (modules, validity_errors). Absent/empty 'modules' -> ([], []). A
    module is {"code", "name", "owns":[str], "layer":str|None, "owner":str|None}.
    Validity errors are collected, never raised.
    """
    raw = cfg.get("modules")
    if not raw:
        return [], []
    modules = []
    errors = []
    seen = set()
    for i, entry in enumerate(raw):
        if not isinstance(entry, dict):
            errors.append(f"E: module entry #{i + 1} is not an object")
            continue
        code = entry.get("code")
        name = entry.get("name")
        owns = entry.get("owns")
        label = code if isinstance(code, str) and code else f"#{i + 1}"
        if not (isinstance(code, str) and code):
            errors.append(f"E: module entry {label} is missing 'code'")
        if not (isinstance(name, str) and name):
            errors.append(f"E: module {label} is missing 'name'")
        if not (isinstance(owns, list) and owns
                and all(isinstance(g, str) and g for g in owns)):
            errors.append(f"E: module {label} is missing a non-empty 'owns' list")
        if isinstance(code, str) and code:
            if not _MODULE_CODE_RE.match(code):
                errors.append(
                    f"E: module code {code} is malformed "
                    f"(need 2-12 chars, A-Z0-9, starting with a letter)")
            if code in seen:
                errors.append(f"E: duplicate module code {code}")
            seen.add(code)
        modules.append({
            "code": code,
            "name": name,
            "owns": owns if isinstance(owns, list) else [],
            "layer": entry.get("layer"),
            "owner": entry.get("owner"),
        })
    return modules, errors
```

Run: `python3 scripts/check_graph_test.py` — expect: pass.

- [ ] **Step 3: Re-stamp and commit**

`python3 scripts/vendor_linters.py --stamp`
`git commit -m "feat(check-graph): module manifest loader + validation # Implements: MODMAP-1.1"`

_Requirements: MODMAP-1.1, MODMAP-1.2, MODMAP-1.3, MODMAP-1.4, MODMAP-1.5, MODMAP-4.1, MODMAP-4.4_

---

### Task 2: Glob dialect + path→module resolution

**Files:**
- Modify: `scripts/check_graph.py` (add after `dedupe_by_fullest`)
- Test: `scripts/check_graph_test.py`

**Interfaces:**
- Consumes: a module list of `{"code", "owns":[str]}` dicts (the shape Task 1
  produces; tests build them inline).
- Produces: `_glob_to_re(pattern) -> compiled regex` and
  `resolve_module(path, modules) -> list[str]` (sorted matching module codes:
  `[]`=orphan, `[code]`=home, `[a, b, …]`=ambiguous/double-mapped).

**Depends-on:** none

- [ ] **Step 1: Write the failing test**

Add to `scripts/check_graph_test.py`:

```python
class GlobResolveTest(unittest.TestCase):
    def test_glob_subtree_and_segment_MODMAP_2_1(self):
        self.assertTrue(check_graph._glob_to_re("src/auth/**").match("src/auth"))
        self.assertTrue(check_graph._glob_to_re("src/auth/**").match("src/auth/login"))
        self.assertFalse(check_graph._glob_to_re("src/auth").match("src/auth/login"))
        self.assertTrue(check_graph._glob_to_re("packages/*").match("packages/api"))
        self.assertFalse(check_graph._glob_to_re("packages/*").match("packages/api/core"))

    def test_resolve_single_owner_MODMAP_2_1(self):
        mods = [{"code": "AUTH", "owns": ["src/auth/**"]},
                {"code": "BILL", "owns": ["src/billing/**"]}]
        self.assertEqual(check_graph.resolve_module("src/auth/login", mods), ["AUTH"])

    def test_resolve_double_mapped_MODMAP_2_2(self):
        mods = [{"code": "AAA", "owns": ["src/shared/**"]},
                {"code": "BBB", "owns": ["src/shared/**"]}]
        self.assertEqual(check_graph.resolve_module("src/shared/util", mods), ["AAA", "BBB"])

    def test_resolve_orphan_MODMAP_2_3(self):
        mods = [{"code": "AUTH", "owns": ["src/auth/**"]}]
        self.assertEqual(check_graph.resolve_module("src/unclaimed", mods), [])

    def test_resolve_preserves_digit_suffixed_folder_MODMAP_2_1(self):
        # guards against normalize_path stripping the trailing digit (store2->store)
        mods = [{"code": "STORE", "owns": ["src/store2/**"]}]
        self.assertEqual(check_graph.resolve_module("src/store2/db", mods), ["STORE"])
```

Run: `python3 scripts/check_graph_test.py` — expect:
`AttributeError: module 'check_graph' has no attribute '_glob_to_re'`.

- [ ] **Step 2: Implement** — add to `scripts/check_graph.py` after `dedupe_by_fullest`:

```python
_glob_cache = {}


def _glob_to_re(pattern):
    """Compile an owns-glob to an anchored regex matched against a repo-relative
    folder path. Dialect: a trailing '/**' owns the folder and every descendant;
    a bare '**' owns everything; '*' matches a single path segment; everything
    else is literal.
    """
    cached = _glob_cache.get(pattern)
    if cached is not None:
        return cached
    p = pattern.strip()
    if p.startswith("./"):
        p = p[2:]
    p = p.strip("/")
    if p == "**":
        _glob_cache[pattern] = re.compile("^.*$")
        return _glob_cache[pattern]
    trailing_subtree = p.endswith("/**")
    if trailing_subtree:
        p = p[:-3]
    out = ["^"]
    i, n = 0, len(p)
    while i < n:
        if p[i:i + 2] == "**":
            out.append(".*")
            i += 2
        elif p[i] == "*":
            out.append("[^/]*")
            i += 1
        else:
            out.append(re.escape(p[i]))
            i += 1
    if trailing_subtree:
        out.append("(?:/.*)?")
    out.append("$")
    regex = re.compile("".join(out))
    _glob_cache[pattern] = regex
    return regex


def resolve_module(path, modules):
    """Return the sorted list of module codes whose 'owns' globs match a
    repo-relative folder path: [] = orphan, [code] = home, [a, b, ...] =
    ambiguous (double-mapped). Neutral by design — callers decide severity.

    Normalize minimally (leading './' and trailing '/'): do NOT use
    normalize_path here — its locator-stripping rules would corrupt a
    digit-suffixed folder segment (e.g. 'src/store2' -> 'src/store').
    """
    folder = _LEADING_DOT_SLASH_RE.sub("", str(path)).strip("/")
    hits = set()
    for m in modules:
        code = m.get("code")
        if not code:
            continue
        for g in m.get("owns", []):
            if _glob_to_re(g).match(folder):
                hits.add(code)
                break
    return sorted(hits)
```

Run: `python3 scripts/check_graph_test.py` — expect: pass.

- [ ] **Step 3: Re-stamp and commit**

`python3 scripts/vendor_linters.py --stamp`
`git commit -m "feat(check-graph): owns-glob dialect + path resolution # Implements: MODMAP-2.1"`

_Requirements: MODMAP-2.1, MODMAP-2.2, MODMAP-2.3_

---

### Task 3: Source-tree folder enumeration

**Files:**
- Modify: `scripts/check_graph.py` (add after `_walk`)
- Test: `scripts/check_graph_test.py`

**Interfaces:**
- Consumes: `root` (absolute repo path), `cfg` (with `graph.sourceRoots`,
  `graph.sourceExts`), and the existing module-level `_SKIP_DIRS` set.
- Produces: `enumerate_folders(root, cfg) -> (repo_folders, source_folders)`,
  two sorted lists of repo-relative directory paths; `source_folders` are those
  directly containing a file whose extension is in `sourceExts`.

**Depends-on:** none

- [ ] **Step 1: Write the failing test**

Add to `scripts/check_graph_test.py` (reuses the existing `_FixtureTestCase._tmp_repo`
helper that writes a `{relpath: content}` tree):

```python
class EnumerateFoldersTest(_FixtureTestCase):
    def test_enumerates_repo_and_source_folders_MODMAP_3_1(self):
        root = self._tmp_repo({
            "src/auth/login.ts": "x",
            "src/auth/helpers/util.ts": "x",
            "src/assets/logo.png": "x",          # asset-only: repo folder, not source
            "src/container/inner/svc.ts": "x",   # 'container' has no direct source
            "node_modules/pkg/index.ts": "x",    # skipped
        })
        cfg = {"graph": {"sourceRoots": ["src"],
                         "sourceExts": ["ts"], "cardCap": 12}}
        repo, source = check_graph.enumerate_folders(root, cfg)
        self.assertIn("src/auth", source)
        self.assertIn("src/auth/helpers", source)
        self.assertIn("src/container/inner", source)
        self.assertNotIn("src/assets", source)       # no direct .ts
        self.assertNotIn("src/container", source)     # only subdirs have source
        self.assertIn("src/container", repo)          # but it IS a repo folder
        self.assertTrue(all("node_modules" not in f for f in repo))
```

Run: `python3 scripts/check_graph_test.py` — expect:
`AttributeError: module 'check_graph' has no attribute 'enumerate_folders'`.

- [ ] **Step 2: Implement** — add to `scripts/check_graph.py` after `_walk`:

```python
def enumerate_folders(root, cfg):
    """Walk each existing sourceRoot under `root`; return (repo_folders,
    source_folders) as sorted repo-relative directory paths. source_folders
    directly contain a file whose extension is in graph.sourceExts. Uses the
    same dotfile/_SKIP_DIRS exclusions as _walk. Never called at import time.
    """
    graph = cfg["graph"]
    exts = tuple("." + e for e in graph["sourceExts"])
    repo_folders = set()
    source_folders = set()

    def walk(abs_dir, rel_dir):
        try:
            entries = list(os.scandir(abs_dir))
        except OSError:
            return
        has_source = False
        for e in entries:
            if e.name.startswith("."):
                continue
            if e.is_dir(follow_symlinks=False):
                if e.name in _SKIP_DIRS:
                    continue
                child_rel = e.name if not rel_dir else rel_dir + "/" + e.name
                repo_folders.add(child_rel)
                walk(e.path, child_rel)
            elif e.is_file(follow_symlinks=False) and e.name.endswith(exts):
                has_source = True
        if rel_dir and has_source:
            source_folders.add(rel_dir)

    for r in graph["sourceRoots"]:
        abs_r = os.path.join(root, r)
        if os.path.isdir(abs_r):
            repo_folders.add(r)
            walk(abs_r, r)
    return sorted(repo_folders), sorted(source_folders)
```

Run: `python3 scripts/check_graph_test.py` — expect: pass.

- [ ] **Step 3: Re-stamp and commit**

`python3 scripts/vendor_linters.py --stamp`
`git commit -m "feat(check-graph): source-tree folder enumeration # Implements: MODMAP-3.1"`

_Requirements: MODMAP-3.1_

---

### Task 4: Boundary verification sub-check

**Files:**
- Modify: `scripts/check_graph.py` (add just before `_run_verify`)
- Test: `scripts/check_graph_test.py`

**Interfaces:**
- Consumes: `enumerate_folders` (Task 3), `resolve_module` (Task 2), and a
  validated `modules` list (Task 1 shape).
- Produces: `_verify_boundaries(root, cfg, modules) -> (errors, warnings)`, both
  `list[str]`; error strings prefixed `E:`, warnings `W:`.

**Depends-on:** Task 1, Task 2, Task 3

- [ ] **Step 1: Write the failing test**

Add to `scripts/check_graph_test.py`:

```python
class VerifyBoundariesTest(_FixtureTestCase):
    def _cfg(self):
        return {"graph": {"sourceRoots": ["src"], "sourceExts": ["ts"], "cardCap": 12}}

    def test_orphan_folder_is_error_MODMAP_3_2(self):
        root = self._tmp_repo({"src/auth/a.ts": "x", "src/lonely/b.ts": "x"})
        mods = [{"code": "AUTH", "name": "A", "owns": ["src/auth/**"]}]
        errs, warns = check_graph._verify_boundaries(root, self._cfg(), mods)
        self.assertTrue(any("src/lonely" in e and "orphan" in e.lower() for e in errs))

    def test_double_mapped_folder_is_error_MODMAP_3_3(self):
        root = self._tmp_repo({"src/shared/a.ts": "x"})
        mods = [{"code": "AAA", "name": "A", "owns": ["src/shared/**"]},
                {"code": "BBB", "name": "B", "owns": ["src/**"]}]
        errs, _ = check_graph._verify_boundaries(root, self._cfg(), mods)
        self.assertTrue(any("src/shared" in e and "AAA" in e and "BBB" in e for e in errs))

    def test_stale_glob_is_warning_not_error_MODMAP_3_4(self):
        root = self._tmp_repo({"src/auth/a.ts": "x"})
        mods = [{"code": "AUTH", "name": "A", "owns": ["src/auth/**", "src/ghost/**"]}]
        errs, warns = check_graph._verify_boundaries(root, self._cfg(), mods)
        self.assertEqual(errs, [])                                   # full coverage
        self.assertTrue(any("src/ghost" in w and "AUTH" in w for w in warns))

    def test_full_coverage_is_clean_MODMAP_3_5(self):
        root = self._tmp_repo({"src/auth/a.ts": "x", "src/auth/sub/b.ts": "x"})
        mods = [{"code": "AUTH", "name": "A", "owns": ["src/auth/**"]}]
        errs, warns = check_graph._verify_boundaries(root, self._cfg(), mods)
        self.assertEqual(errs, [])
        self.assertEqual(warns, [])
```

Run: `python3 scripts/check_graph_test.py` — expect:
`AttributeError: module 'check_graph' has no attribute '_verify_boundaries'`.

- [ ] **Step 2: Implement** — add to `scripts/check_graph.py` just before `_run_verify`:

```python
def _verify_boundaries(root, cfg, modules):
    """Check module coverage of the source tree. Returns (errors, warnings).

    Orphan and double-mapped SOURCE folders are errors; a module 'owns' pattern
    matching no REPO folder is a warning (aligns with 'no folder in the repo').
    """
    errors = []
    warnings = []
    repo_folders, source_folders = enumerate_folders(root, cfg)
    for folder in source_folders:
        hits = resolve_module(folder, modules)
        if not hits:
            errors.append(f"E: source folder {folder} maps to no module (orphan)")
        elif len(hits) > 1:
            errors.append(
                f"E: source folder {folder} is double-mapped to modules "
                f"{', '.join(hits)}")
    for m in modules:
        code = m.get("code")
        for g in m.get("owns", []):
            rx = _glob_to_re(g)
            if not any(rx.match(f) for f in repo_folders):
                warnings.append(
                    f"W: module {code} owns '{g}' which matches no folder in the repo")
    return errors, warnings
```

Run: `python3 scripts/check_graph_test.py` — expect: pass.

- [ ] **Step 3: Re-stamp and commit**

`python3 scripts/vendor_linters.py --stamp`
`git commit -m "feat(check-graph): boundary coverage sub-check # Implements: MODMAP-3.2"`

_Requirements: MODMAP-3.2, MODMAP-3.3, MODMAP-3.4, MODMAP-3.5_

---

### Task 5: Wire boundary check into `--verify` with a warnings channel

**Files:**
- Modify: `scripts/check_graph.py` (the `_run_verify` function only)
- Test: `scripts/check_graph_test.py`

**Interfaces:**
- Consumes: `load_manifest` (Task 1), `_verify_boundaries` (Task 4), and the
  existing `_run_verify(root, cfg, specs_dir, as_json)` body.
- Produces: an extended `_run_verify` that appends validity/boundary findings,
  prints a `warnings` section, adds a `"warnings"` key to JSON output, and keeps
  `return 1 if errors else 0`.

**Depends-on:** Task 1, Task 4

- [ ] **Step 1: Write the failing test**

Add to `scripts/check_graph_test.py`. These build a full temp repo and call
`main(["--verify", "--root", root])`, capturing the exit code:

```python
class VerifyIntegrationTest(_FixtureTestCase):
    def _repo_with_specs(self, extra, trace):
        # a valid, non-stale spec repo so the two existing checks pass
        files = dict(extra)
        root = self._tmp_repo(files)
        import os as _os, json as _json
        _os.makedirs(_os.path.join(root, "docs/agents"), exist_ok=True)
        with open(_os.path.join(root, "docs/agents/trace.json"), "w") as f:
            _json.dump(trace, f)
        _os.makedirs(_os.path.join(root, "docs/specs"), exist_ok=True)
        open(_os.path.join(root, "docs/specs/INDEX.md"), "w").close()
        # generate a non-stale GRAPH.md through the real harvest path so the two
        # existing --verify checks pass (no features -> empty, self-consistent).
        check_graph.main(["--harvest", "--root", root])
        return root

    def test_warnings_do_not_fail_the_gate_MODMAP_3_4_3_7(self):
        root = self._repo_with_specs(
            {"src/auth/a.ts": "x"},
            {"specsDir": "docs/specs",
             "modules": [{"code": "AUTH", "name": "A",
                          "owns": ["src/auth/**", "src/ghost/**"]}]})
        rc = check_graph.main(["--verify", "--root", root])
        self.assertEqual(rc, 0)                       # stale-glob is warning only

    def test_orphan_fails_the_gate_MODMAP_3_6(self):
        root = self._repo_with_specs(
            {"src/auth/a.ts": "x", "src/orphan/b.ts": "x"},
            {"specsDir": "docs/specs",
             "modules": [{"code": "AUTH", "name": "A", "owns": ["src/auth/**"]}]})
        rc = check_graph.main(["--verify", "--root", root])
        self.assertEqual(rc, 1)

    def test_no_manifest_behaves_as_before_MODMAP_4_2(self):
        root = self._repo_with_specs(
            {"src/whatever/a.ts": "x"}, {"specsDir": "docs/specs"})
        rc = check_graph.main(["--verify", "--root", root])
        self.assertEqual(rc, 0)                       # no modules key -> no boundary errors

    def test_existing_checks_still_run_with_manifest_MODMAP_4_3(self):
        root = self._repo_with_specs(
            {"src/auth/a.ts": "x"},
            {"specsDir": "docs/specs",
             "modules": [{"code": "AUTH", "name": "A", "owns": ["src/auth/**"]}]})
        import os as _os
        with open(_os.path.join(root, "docs/specs/GRAPH.md"), "w") as f:
            f.write("stale content")                  # break the freshness check
        rc = check_graph.main(["--verify", "--root", root])
        self.assertEqual(rc, 1)                       # existing freshness check still fires

    def test_import_has_no_side_effects_MODMAP_4_5(self):
        import importlib
        mod = importlib.reload(check_graph)            # re-import triggers no CLI/IO
        self.assertTrue(hasattr(mod, "_run_verify"))
```

Run: `python3 scripts/check_graph_test.py` — expect: the new `VerifyIntegrationTest`
cases FAIL (boundary errors not yet wired; e.g. `test_orphan_fails_the_gate`
returns 0 instead of 1).

- [ ] **Step 2: Implement** — modify only `_run_verify` in `scripts/check_graph.py`.
  Keep both existing checks exactly as they are; add a `warnings = []` list next
  to `errors = []`, then insert the boundary block after the registration check
  and before the output block, and update the output block:

```python
    # (existing) errors = []  ->  add:
    warnings = []

    # ... unchanged freshness check ...
    # ... unchanged registration check ...

    # boundary verification (MODMAP)
    modules, validity_errors = load_manifest(cfg)
    if validity_errors:
        errors.extend(validity_errors)
    elif modules:
        berrors, bwarnings = _verify_boundaries(root, cfg, modules)
        errors.extend(berrors)
        warnings.extend(bwarnings)

    if as_json:
        print(json.dumps({"errors": errors, "warnings": warnings},
                         indent=2, ensure_ascii=False))
    else:
        print(f"check-graph --verify: {'FAIL' if errors else 'OK'}")
        for e in errors:
            print(f"  {e}")
        for w in warnings:
            print(f"  {w}")
    return 1 if errors else 0
```

Run: `python3 scripts/check_graph_test.py` — expect: pass.

- [ ] **Step 3: Full green + re-stamp + commit**

`python3 scripts/vendor_linters.py --stamp`
`python3 scripts/check_graph_test.py && python3 scripts/vendor_linters_test.py && python3 scripts/wiring_test.py && python3 evals/evals.py --strict`
`git commit -m "feat(check-graph): wire boundary check into --verify # Implements: MODMAP-3.6"`

_Requirements: MODMAP-3.6, MODMAP-3.7, MODMAP-4.2, MODMAP-4.3, MODMAP-4.5_
