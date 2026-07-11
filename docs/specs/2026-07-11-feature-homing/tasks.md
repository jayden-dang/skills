# Tasks: Feature Homing Refinement & Facets

Feature code: MODHOME
Status: Implemented
Date: 2026-07-11
Requirements: ./requirements.md
Design: ./design.md

**Goal:** Make module homing legible — distinguish a feature that *spans* two or
more modules from one that is merely un-homed, attach a feature's cross-module
touched surface as *facets*, and let a `Module:` header line override the derived
home.

**Architecture:** All production code is in `scripts/check_graph.py`; all tests
in `scripts/check_graph_test.py` (Python `unittest`). A new pure classifier
`_home_feature` computes every piece of derived homing state from one
`resolve_module` walk; `harvest` calls it and carries the results on each feature
dict; `render_all` renders facets in the shard row; `_run_verify` formats the two
advisory warnings.

**Tech Stack:** Python 3, standard library only.

## Global Constraints

- **Stdlib only.** No third-party imports. No new top-level import side effects —
  every new symbol is a `def` or a module-level constant (MODHOME-4.5).
- **Re-stamp after every edit to `scripts/check_graph.py`.** Before committing a
  task that changed that file, run `python3 scripts/vendor_linters.py --stamp`
  and include the restamped file in the commit. Verify with
  `python3 scripts/vendor_linters.py --check` (must print `OK`).
- **All suites green before a task is done:**
  `python3 scripts/check_graph_test.py` (unittest),
  `python3 scripts/vendor_linters_test.py`,
  `python3 scripts/wiring_test.py`,
  `python3 evals/evals.py --strict`,
  `python3 scripts/check_trace.py`.
- **Traceability tags.** Every requirement ID must appear in a canonical
  `# covers MODHOME-N.M` comment (hyphen-dot form) inside the test that exercises
  it — Python method names use underscores, and `check_trace.py` scans for the
  canonical hyphen-dot ID, so the comment is what counts.
- **Commit trailer.** Each task's final commit ends with
  `Implements: MODHOME-N.M` (the IDs that task delivers). No other trailer.
- **Graceful degradation (MODHOME-4.1).** With no valid manifest, every feature
  must get `home None`, `facets []`, `homing {"spanned": [], "unknown_override":
  None}`, the flat `GRAPH.md` must stay byte-identical, and `--verify` must emit
  no homing warnings.

## File structure

| File | Change | Responsibility |
|---|---|---|
| `scripts/check_graph.py` | modify | Add `_home_feature` + `_MODULE_OVERRIDE_RE`; rewrite `_home_module` as a wrapper; wire `harvest`; extend `render_all`'s `shard()`; extend `_run_verify`. |
| `scripts/check_graph_test.py` | modify | Add `HomeFeatureTest`; extend `_spec_fixture` with a `module` key; add harvest, render_all, and `--verify` cases. |

All four tasks touch these same two files, so `execute-plan` will run them
serially regardless of the `Depends-on` edges below; the edges still record the
true data dependencies.

---

## Task 1 — `_home_feature` classifier + `_home_module` delegation

**Files:**
- Modify: `scripts/check_graph.py` — add `_home_feature` immediately after
  `resolve_module` (ends at `:158`) and before the current `_home_module`
  (`:161`); rewrite `_home_module`'s body (`:161-173`) as a one-line delegation.
- Test: `scripts/check_graph_test.py` — add a `HomeFeatureTest(unittest.TestCase)`
  class (place it right after the existing `HomeModuleTest`, ~`:576`).

**Interfaces:**
- Produces: `_home_feature(owned_paths, touched_paths, override_code,
  module_codes, modules) -> {"home": str|None, "facets": [str], "spanned":
  [str], "unknown_override": str|None}` — pure, no I/O.
- Produces: `_home_module(owned_paths, modules) -> str|None` (unchanged
  signature; now delegates to `_home_feature`).
- Consumes: `resolve_module(path, modules) -> [str]` (existing, `:139`).

**Depends-on:** none

**Steps:**
- [ ] Add the `HomeFeatureTest` class with these tests (complete code):
  ```python
  class HomeFeatureTest(unittest.TestCase):
      MODS = [{"code": "AUTH", "owns": ["src/auth/**"]},
              {"code": "BILL", "owns": ["src/billing/**"]}]

      def test_all_owned_one_module_homes_there_MODHOME_4_2(self):
          # covers MODHOME-4.2
          rec = check_graph._home_feature(
              ["src/auth/a.ts", "src/auth/b.ts"], [], None, {"AUTH", "BILL"}, self.MODS)
          self.assertEqual(rec["home"], "AUTH")
          self.assertEqual(rec["spanned"], [])
          # delegation: _home_module returns the same home
          self.assertEqual(
              check_graph._home_module(["src/auth/a.ts", "src/auth/b.ts"], self.MODS), "AUTH")

      def test_spanning_detected_MODHOME_1_1(self):
          # covers MODHOME-1.1
          rec = check_graph._home_feature(
              ["src/auth/a.ts", "src/billing/b.ts"], [], None, {"AUTH", "BILL"}, self.MODS)
          self.assertIsNone(rec["home"])
          self.assertEqual(rec["spanned"], ["AUTH", "BILL"])

      def test_orphan_owned_is_not_spanning_MODHOME_1_1(self):
          # covers MODHOME-1.1
          # an orphan owned path makes the feature UNRESOLVED, not spanning
          rec = check_graph._home_feature(
              ["src/auth/a.ts", "src/nowhere/x.ts"], [], None, {"AUTH", "BILL"}, self.MODS)
          self.assertIsNone(rec["home"])
          self.assertEqual(rec["spanned"], [])

      def test_facets_from_touched_modules_MODHOME_2_1(self):
          # covers MODHOME-2.1
          rec = check_graph._home_feature(
              ["src/auth/a.ts"], ["src/billing/b.ts"], None, {"AUTH", "BILL"}, self.MODS)
          self.assertEqual(rec["home"], "AUTH")
          self.assertEqual(rec["facets"], ["BILL"])

      def test_facets_exclude_home_MODHOME_2_2(self):
          # covers MODHOME-2.2
          rec = check_graph._home_feature(
              ["src/auth/a.ts"], ["src/auth/other.ts"], None, {"AUTH"},
              [{"code": "AUTH", "owns": ["src/auth/**"]}])
          self.assertEqual(rec["home"], "AUTH")
          self.assertEqual(rec["facets"], [])

      def test_facets_sorted_and_deduped_MODHOME_2_3(self):
          # covers MODHOME-2.3
          mods = [{"code": "AUTH", "owns": ["src/auth/**"]},
                  {"code": "BILL", "owns": ["src/billing/**"]},
                  {"code": "CORE", "owns": ["src/core/**"]}]
          rec = check_graph._home_feature(
              ["src/auth/a.ts"],
              ["src/core/x.ts", "src/billing/b.ts", "src/billing/c.ts"],
              None, {"AUTH", "BILL", "CORE"}, mods)
          self.assertEqual(rec["facets"], ["BILL", "CORE"])

      def test_touched_orphan_or_ambiguous_yields_no_facet_MODHOME_2_4(self):
          # covers MODHOME-2.4
          mods = [{"code": "AUTH", "owns": ["src/auth/**"]},
                  {"code": "DUP", "owns": ["src/shared/**"]},
                  {"code": "DUP2", "owns": ["src/shared/**"]}]
          rec = check_graph._home_feature(
              ["src/auth/a.ts"],
              ["src/nowhere/x.ts", "src/shared/s.ts"],  # orphan + double-mapped
              None, {"AUTH", "DUP", "DUP2"}, mods)
          self.assertEqual(rec["facets"], [])

      def test_valid_override_sets_home_MODHOME_3_1(self):
          # covers MODHOME-3.1
          rec = check_graph._home_feature(
              ["src/billing/b.ts"], [], "AUTH", {"AUTH", "BILL"}, self.MODS)
          self.assertEqual(rec["home"], "AUTH")

      def test_valid_override_suppresses_span_MODHOME_3_2(self):
          # covers MODHOME-3.2
          rec = check_graph._home_feature(
              ["src/auth/a.ts", "src/billing/b.ts"], [], "AUTH",
              {"AUTH", "BILL"}, self.MODS)
          self.assertEqual(rec["home"], "AUTH")
          self.assertEqual(rec["spanned"], [])

      def test_invalid_override_keeps_derived_and_flags_MODHOME_3_3(self):
          # covers MODHOME-3.3
          rec = check_graph._home_feature(
              ["src/auth/a.ts"], [], "NOPE", {"AUTH", "BILL"}, self.MODS)
          self.assertEqual(rec["home"], "AUTH")            # derived home retained
          self.assertEqual(rec["unknown_override"], "NOPE")

      def test_import_still_inert_with_homing_symbols_MODHOME_4_5(self):
          # covers MODHOME-4.5
          import importlib, io, contextlib
          out_buf, err_buf = io.StringIO(), io.StringIO()
          with contextlib.redirect_stdout(out_buf), contextlib.redirect_stderr(err_buf):
              mod = importlib.reload(check_graph)
          self.assertEqual(out_buf.getvalue(), "")
          self.assertEqual(err_buf.getvalue(), "")
          self.assertTrue(hasattr(mod, "_home_feature"))
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k HomeFeatureTest` → expect
  failure: `AttributeError: module 'check_graph' has no attribute '_home_feature'`.
- [ ] Add `_home_feature` immediately after `resolve_module` (`:158`):
  ```python
  def _home_feature(owned_paths, touched_paths, override_code, module_codes, modules):
      """Classify a feature's module homing from its owned + touched paths and an
      optional authored `Module:` override. `module_codes` is the set of valid
      module codes, used only to validate the override. Pure — no I/O.

      Returns {home, facets, spanned, unknown_override}:
        home             module code or None
        facets           sorted modules (!= home) each the sole resolution of a
                         touched path; [] when home is None
        spanned          sorted modules the owned paths fall in, ONLY when every
                         owned path resolves to exactly one module, >=2 distinct
                         modules result, and no valid override applies; else []
        unknown_override the override code when one was declared but is not a
                         known module; else None
      """
      derived_home = None
      spanned = []
      if owned_paths:
          codes = []
          clean = True
          for p in owned_paths:
              hits = resolve_module(p, modules)
              if len(hits) != 1:
                  clean = False
                  break
              codes.append(hits[0])
          if clean:
              uniq = sorted(set(codes))
              if len(uniq) == 1:
                  derived_home = uniq[0]
              elif len(uniq) >= 2:
                  spanned = uniq
      home = derived_home
      unknown_override = None
      if override_code is not None:
          if override_code in module_codes:
              home = override_code
              spanned = []
          else:
              unknown_override = override_code
      facets = []
      if home is not None:
          fset = set()
          for p in touched_paths:
              hits = resolve_module(p, modules)
              if len(hits) == 1 and hits[0] != home:
                  fset.add(hits[0])
          facets = sorted(fset)
      return {"home": home, "facets": facets, "spanned": spanned,
              "unknown_override": unknown_override}
  ```
- [ ] Replace the body of `_home_module` (`:161-173`) with a delegation, keeping
  its name and signature:
  ```python
  def _home_module(owned_paths, modules):
      """Home a feature by its owned paths alone (no override, no touches): the
      single module code iff every owned path resolves to that one module; else
      None. Thin wrapper over _home_feature preserving the MODGRAPH-1.x contract."""
      return _home_feature(owned_paths, [], None, set(), modules)["home"]
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k HomeFeatureTest -k HomeModuleTest`
  (repeat `-k`; unittest has no `"A or B"` — a single quoted `or` pattern runs
  zero tests and still prints OK)
  → expect pass (new tests green AND the four existing `HomeModuleTest` guard
  assertions still green via delegation).
- [ ] Re-stamp: `python3 scripts/vendor_linters.py --stamp` then
  `python3 scripts/vendor_linters.py --check` (expect `OK`).
- [ ] Run the full suite (all five commands in Global Constraints) → expect green.
- [ ] Commit: `feat(check-graph): classify feature homing with spans, facets, override` +
  trailer `Implements: MODHOME-1.1, MODHOME-2.1, MODHOME-2.2, MODHOME-2.3, MODHOME-2.4, MODHOME-3.1, MODHOME-3.2, MODHOME-3.3, MODHOME-4.2, MODHOME-4.5`.

_Requirements: MODHOME-1.1, MODHOME-2.1, MODHOME-2.2, MODHOME-2.3, MODHOME-2.4, MODHOME-3.1, MODHOME-3.2, MODHOME-3.3, MODHOME-4.2, MODHOME-4.5_

---

## Task 2 — `harvest` parses the override and carries the diagnostics

**Files:**
- Modify: `scripts/check_graph.py` — add `_MODULE_OVERRIDE_RE` beside
  `_FEATURE_CODE_RE` (`:450`); in `harvest` compute `_module_codes` once (after
  the manifest load at `:459-461`) and replace the feature-dict `"home":
  _home_module(...)` entry (`:502`) with the `_home_feature` call plus the new
  `facets` and `homing` keys.
- Test: `scripts/check_graph_test.py` — extend `_spec_fixture` (the helper at
  ~`:40`) with an optional `module` key; add cases to `HarvestHomingTest`
  (`:578`).

**Interfaces:**
- Consumes: `_home_feature(...)` (Task 1); `load_manifest(cfg) -> (modules,
  errors)` (existing, `:721`); each feature's `requirements.md` text `text`
  (in scope in `harvest` at `:464`).
- Produces: every harvested feature dict now additionally carries
  `"facets": [str]` and `"homing": {"spanned": [str], "unknown_override":
  str|None}`; `"home"` keeps its meaning.
- Produces: `_spec_fixture` accepts `module` (str) → writes a `Module: <code>`
  header line into that feature's `requirements.md`.

**Depends-on:** Task 1

**Steps:**
- [ ] Extend `_spec_fixture` so a `module` key injects the header line. Change the
  `req_text` builder to:
  ```python
  module_line = f"Module: {f['module']}\n" if f.get("module") else ""
  req_text = (
      f"# Requirements: {f['name']}\n"
      f"Feature code: {f['code']}\n"
      f"{module_line}"
      "Status: Approved\n\n"
      "## Out of Scope\n"
      f"{oos_bullets}\n"
  )
  ```
- [ ] Add these tests to `HarvestHomingTest`:
  ```python
  def _cfg(self):
      return {"specsDir": "docs/specs",
              "graph": {"sourceRoots": ["src"], "sourceExts": ["ts"], "cardCap": 12},
              "modules": [{"code": "AUTH", "name": "A", "owns": ["src/auth/**"]},
                          {"code": "BILL", "name": "B", "owns": ["src/billing/**"]}]}

  def test_module_override_wins_over_derivation_MODHOME_3_1(self):
      # covers MODHOME-3.1
      specs = self._spec_fixture([
          {"slug": "ov", "code": "OV", "name": "Override", "module": "AUTH",
           "tasks": "**Files:**\n- Create: src/billing/b.ts"}])
      graph = check_graph.harvest(specs, self._cfg())
      f = next(x for x in graph["features"] if x["code"] == "OV")
      self.assertEqual(f["home"], "AUTH")   # derived would be BILL; override wins

  def test_harvest_adds_facets_and_homing_fields_MODHOME_4_4(self):
      # covers MODHOME-4.4
      specs = self._spec_fixture([
          {"slug": "aa", "code": "AA", "name": "Aye",
           "tasks": "**Files:**\n- Create: src/auth/a.ts\n- Modify: src/billing/b.ts"}])
      f = next(x for x in check_graph.harvest(specs, self._cfg())["features"]
               if x["code"] == "AA")
      self.assertEqual(f["home"], "AUTH")
      self.assertEqual(f["facets"], ["BILL"])
      self.assertEqual(f["homing"], {"spanned": [], "unknown_override": None})
      for key in ("code", "name", "owns", "touches", "interfaces", "oos", "home"):
          self.assertIn(key, f)             # existing card fields preserved

  def test_no_manifest_degrades_homing_MODHOME_4_1(self):
      # covers MODHOME-4.1
      specs = self._spec_fixture([
          {"slug": "aa", "code": "AA", "name": "Aye", "module": "AUTH",
           "tasks": "**Files:**\n- Create: src/auth/a.ts"}])
      cfg = {"specsDir": "docs/specs",
             "graph": {"sourceRoots": ["src"], "sourceExts": ["ts"], "cardCap": 12}}
      f = next(x for x in check_graph.harvest(specs, cfg)["features"]
               if x["code"] == "AA")
      self.assertIsNone(f["home"])
      self.assertEqual(f["facets"], [])
      self.assertEqual(f["homing"], {"spanned": [], "unknown_override": None})
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k HarvestHomingTest` → expect
  failure: `KeyError: 'facets'` (and the override test failing on `home`).
- [ ] Add `_MODULE_OVERRIDE_RE` beside `_FEATURE_CODE_RE` (after `:450`):
  ```python
  _MODULE_OVERRIDE_RE = re.compile(r"^Module:\s*([A-Z][A-Z0-9]{1,11})", re.MULTILINE)
  ```
- [ ] In `harvest`, immediately after the manifest-load block (`:459-461`), add:
  ```python
  _module_codes = {m["code"] for m in _manifest_modules if m.get("code")}
  ```
- [ ] Replace the feature-dict tail. The current `features.append({...})`
  (`:494-504`) ends with `"home": _home_module(sorted(owns), _manifest_modules),`.
  Just before the `features.append(`, compute:
  ```python
  override_code = None
  if _manifest_modules:
      om = _MODULE_OVERRIDE_RE.search(text)
      override_code = om.group(1) if om else None
  _hom = _home_feature(sorted(owns), sorted(touches), override_code,
                       _module_codes, _manifest_modules)
  ```
  and change the dict's last entry from the single `"home": _home_module(...)`
  line to:
  ```python
          "home": _hom["home"],
          "facets": _hom["facets"],
          "homing": {"spanned": _hom["spanned"],
                     "unknown_override": _hom["unknown_override"]},
  ```
  (Leave the `:536-541` card-cap pass untouched — it caps only
  owns/touches/interfaces/oos, never `facets`.)
- [ ] Run `python3 scripts/check_graph_test.py -k HarvestHomingTest -k HomeModuleTest -k RenderAllTest`
  (repeat `-k` per class)
  → expect pass (new fields present; existing homing + render_all tests still
  green because they read `home`/`owns`, which are unchanged).
- [ ] Re-stamp (`--stamp` then `--check` → `OK`).
- [ ] Run the full suite → expect green.
- [ ] Commit: `feat(check-graph): harvest carries facets, spans, and Module override` +
  trailer `Implements: MODHOME-3.1, MODHOME-4.1, MODHOME-4.4`.

_Requirements: MODHOME-3.1, MODHOME-4.1, MODHOME-4.4_

---

## Task 3 — `render_all` shows facets in the shard row

**Files:**
- Modify: `scripts/check_graph.py` — the nested `shard()` helper inside
  `render_all` (`:611-616`): add a `Facets` column.
- Test: `scripts/check_graph_test.py` — add cases to `RenderAllTest` (`:658`).

**Interfaces:**
- Consumes: harvested features carrying `home`, `facets` (Task 2);
  `render_all(graph, cfg) -> {relpath: content}` (existing, `:580`).
- Produces: per-module shard rows now read `| Feature | Name | Owns | Facets |`.

**Depends-on:** Task 2

**Steps:**
- [ ] Add these tests to `RenderAllTest`:
  ```python
  def test_facets_render_in_shard_row_MODHOME_2_5(self):
      # covers MODHOME-2.5
      specs = self._spec_fixture([
          {"slug": "aa", "code": "AA", "name": "Aye",
           "tasks": "**Files:**\n- Create: src/auth/a.ts\n- Modify: src/billing/b.ts"}])
      cfg = {"specsDir": "docs/specs",
             "graph": {"sourceRoots": ["src"], "sourceExts": ["ts"], "cardCap": 12, "queryCap": 8},
             "modules": [{"code": "AUTH", "name": "Auth", "owns": ["src/auth/**"]},
                         {"code": "BILL", "name": "Bill", "owns": ["src/billing/**"]}]}
      files = check_graph.render_all(check_graph.harvest(specs, cfg), cfg)
      self.assertIn("Facets", files["modules/AUTH.md"])
      # AA's row carries its BILL facet
      auth_rows = [ln for ln in files["modules/AUTH.md"].splitlines() if ln.startswith("| AA ")]
      self.assertTrue(auth_rows and "BILL" in auth_rows[0])

  def test_spanning_feature_renders_in_unassigned_MODHOME_1_4(self):
      # covers MODHOME-1.4
      specs = self._spec_fixture([
          {"slug": "sp", "code": "SP", "name": "Span",
           "tasks": "**Files:**\n- Create: src/auth/a.ts\n- Create: src/billing/b.ts"}])
      cfg = {"specsDir": "docs/specs",
             "graph": {"sourceRoots": ["src"], "sourceExts": ["ts"], "cardCap": 12, "queryCap": 8},
             "modules": [{"code": "AUTH", "name": "Auth", "owns": ["src/auth/**"]},
                         {"code": "BILL", "name": "Bill", "owns": ["src/billing/**"]}]}
      files = check_graph.render_all(check_graph.harvest(specs, cfg), cfg)
      self.assertIn("modules/_unassigned.md", files)
      self.assertIn("| SP |", files["modules/_unassigned.md"])

  def test_flat_render_byte_identical_with_new_fields_MODHOME_4_1(self):
      # covers MODHOME-4.1
      specs = self._spec_fixture([
          {"slug": "aa", "code": "AA", "name": "Aye", "tasks": "**Files:**\n- Create: src/auth/a.ts"}])
      cfg = {"specsDir": "docs/specs",
             "graph": {"sourceRoots": ["src"], "sourceExts": ["ts"], "cardCap": 12, "queryCap": 8}}
      graph = check_graph.harvest(specs, cfg)   # no manifest -> facets/home degraded
      self.assertEqual(
          check_graph.render_all(graph, cfg),
          {"GRAPH.md": check_graph.render_graph_md(graph)})
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k RenderAllTest` → expect the
  facets test to fail (`Facets` not in shard) while the others pass.
- [ ] In `render_all`'s `shard()` (`:611-616`), change the header row and the
  per-feature row:
  ```python
  def shard(title, feats):
      rows = [f"# Module {title}", "", _GRAPH_BANNER, "",
              "| Feature | Name | Owns | Facets |", "|---|---|---|---|"]
      for f in sorted(feats, key=lambda x: x["code"]):
          facets = ", ".join(f.get("facets") or []) or "—"
          rows.append(f"| {f['code']} | {f['name']} | {', '.join(f['owns']) or '—'} | {facets} |")
      rows.append("")
      return "\n".join(rows)
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k RenderAllTest` → expect pass
  (existing `| AA |` / `| XX |` substring assertions still hold with the extra
  column).
- [ ] Re-stamp (`--stamp` then `--check` → `OK`).
- [ ] Run the full suite → expect green.
- [ ] Commit: `feat(check-graph): render feature facets in module shard rows` +
  trailer `Implements: MODHOME-1.4, MODHOME-2.5`.

_Requirements: MODHOME-1.4, MODHOME-2.5, MODHOME-4.1_

---

## Task 4 — `--verify` emits the split-signal and invalid-override warnings

**Files:**
- Modify: `scripts/check_graph.py` — `_run_verify`, inside the existing
  `elif modules:` branch (`:841-844`), after the boundary check.
- Test: `scripts/check_graph_test.py` — add cases to `VerifyIntegrationTest`
  (`:1196`).

**Interfaces:**
- Consumes: `graph["features"]` each carrying `homing = {"spanned", "unknown_override"}`
  (Task 2); the existing `warnings` list and `--json` output shape
  `{"errors": [...], "warnings": [...]}` (`:846-847`).
- Produces: new advisory warning strings on the `warnings` channel; no exit-code
  change (exit stays `1 if errors else 0`).

**Depends-on:** Task 2

**Steps:**
- [ ] Add these tests to `VerifyIntegrationTest` (they build their own repo
  because the split/override features must be registered in `INDEX.md`):
  ```python
  def _homing_repo(self, req_extra, files):
      import io, contextlib
      root = self._tmp_repo(files)
      os.makedirs(os.path.join(root, "docs/agents"), exist_ok=True)
      with open(os.path.join(root, "docs/agents/trace.json"), "w") as fh:
          json.dump({"specsDir": "docs/specs",
                     "graph": {"sourceRoots": ["src"], "sourceExts": ["ts"]},
                     "modules": [{"code": "AUTH", "name": "A", "owns": ["src/auth/**"]},
                                 {"code": "BILL", "name": "B", "owns": ["src/billing/**"]}]},
                    fh)
      check_graph.main(["--harvest", "--root", root])   # write non-stale shards
      buf = io.StringIO()
      with contextlib.redirect_stdout(buf):
          rc = check_graph.main(["--verify", "--root", root, "--json"])
      return rc, json.loads(buf.getvalue())

  def test_split_signal_is_advisory_MODHOME_1_2_1_3(self):
      # covers MODHOME-1.2, MODHOME-1.3
      rc, payload = self._homing_repo(None, {
          "docs/specs/INDEX.md": "| SPAN | Span | ./span/ | Approved |\n",
          "docs/specs/span/requirements.md":
              "# Requirements: Span\nFeature code: SPAN\nStatus: Approved\n\n## Out of Scope\n",
          "docs/specs/span/tasks.md":
              "**Files:**\n- Create: src/auth/a.ts\n- Create: src/billing/b.ts\n",
          "src/auth/a.ts": "x", "src/billing/b.ts": "x"})
      self.assertEqual(rc, 0)                           # advisory, no gate change (1.3)
      self.assertEqual(payload["errors"], [])
      self.assertTrue(any("SPAN" in w and "AUTH" in w and "BILL" in w
                          for w in payload["warnings"]))   # (1.2)

  def test_invalid_override_is_advisory_MODHOME_3_3_3_4(self):
      # covers MODHOME-3.3, MODHOME-3.4
      rc, payload = self._homing_repo(None, {
          "docs/specs/INDEX.md": "| OV | Ov | ./ov/ | Approved |\n",
          "docs/specs/ov/requirements.md":
              "# Requirements: Ov\nFeature code: OV\nModule: NOPE\nStatus: Approved\n\n## Out of Scope\n",
          "docs/specs/ov/tasks.md": "**Files:**\n- Create: src/auth/a.ts\n",
          "src/auth/a.ts": "x"})
      self.assertEqual(rc, 0)                           # advisory (3.4)
      self.assertEqual(payload["errors"], [])
      self.assertTrue(any("OV" in w and "NOPE" in w for w in payload["warnings"]))  # (3.3)

  def test_boundary_error_still_fails_with_span_present_MODHOME_4_3(self):
      # covers MODHOME-4.3
      rc, payload = self._homing_repo(None, {
          "docs/specs/INDEX.md": "| SPAN | Span | ./span/ | Approved |\n",
          "docs/specs/span/requirements.md":
              "# Requirements: Span\nFeature code: SPAN\nStatus: Approved\n\n## Out of Scope\n",
          "docs/specs/span/tasks.md":
              "**Files:**\n- Create: src/auth/a.ts\n- Create: src/billing/b.ts\n",
          "src/auth/a.ts": "x", "src/billing/b.ts": "x",
          "src/orphan/z.ts": "x"})                       # orphan source folder -> error
      self.assertEqual(rc, 1)                            # boundary error still fails the gate
      self.assertTrue(any("orphan" in e for e in payload["errors"]))
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k test_split_signal_is_advisory -k test_invalid_override_is_advisory`
  (repeat `-k` per test)
  → expect failure (warnings list lacks the new strings).
- [ ] In `_run_verify`, extend the `elif modules:` branch (`:841-844`). After the
  existing `warnings.extend(bwarnings)` line, add:
  ```python
          for f in graph["features"]:
              hom = f.get("homing") or {}
              if hom.get("spanned"):
                  warnings.append(
                      f"W: feature {f['code']} owns files spanning modules "
                      f"{', '.join(hom['spanned'])} — split it per module or "
                      f"declare a home with a `Module:` header line")
              if hom.get("unknown_override"):
                  warnings.append(
                      f"W: feature {f['code']} declares Module: {hom['unknown_override']} "
                      f"which is not a known module — override ignored")
  ```
- [ ] Run `python3 scripts/check_graph_test.py -k VerifyIntegrationTest` → expect
  pass (new advisories present; the three MODMAP boundary/registration tests
  still green).
- [ ] Re-stamp (`--stamp` then `--check` → `OK`).
- [ ] Run the full suite → expect green.
- [ ] Commit: `feat(check-graph): warn on module spans and unknown Module overrides` +
  trailer `Implements: MODHOME-1.2, MODHOME-1.3, MODHOME-3.3, MODHOME-3.4, MODHOME-4.3`.

_Requirements: MODHOME-1.2, MODHOME-1.3, MODHOME-3.3, MODHOME-3.4, MODHOME-4.3_

---

## Coverage map

| Requirement | Task | Tagged test |
|---|---|---|
| MODHOME-1.1 | 1 | `test_spanning_detected`, `test_orphan_owned_is_not_spanning` |
| MODHOME-1.2 | 4 | `test_split_signal_is_advisory` |
| MODHOME-1.3 | 4 | `test_split_signal_is_advisory` |
| MODHOME-1.4 | 3 | `test_spanning_feature_renders_in_unassigned` |
| MODHOME-2.1 | 1 | `test_facets_from_touched_modules` |
| MODHOME-2.2 | 1 | `test_facets_exclude_home` |
| MODHOME-2.3 | 1 | `test_facets_sorted_and_deduped` |
| MODHOME-2.4 | 1 | `test_touched_orphan_or_ambiguous_yields_no_facet` |
| MODHOME-2.5 | 3 | `test_facets_render_in_shard_row` |
| MODHOME-3.1 | 1, 2 | `test_valid_override_sets_home`, `test_module_override_wins_over_derivation` |
| MODHOME-3.2 | 1 | `test_valid_override_suppresses_span` |
| MODHOME-3.3 | 1, 4 | `test_invalid_override_keeps_derived_and_flags`, `test_invalid_override_is_advisory` |
| MODHOME-3.4 | 4 | `test_invalid_override_is_advisory` |
| MODHOME-4.1 | 2, 3 | `test_no_manifest_degrades_homing`, `test_flat_render_byte_identical_with_new_fields` |
| MODHOME-4.2 | 1 | `test_all_owned_one_module_homes_there` |
| MODHOME-4.3 | 4 | `test_boundary_error_still_fails_with_span_present` |
| MODHOME-4.4 | 2 | `test_harvest_adds_facets_and_homing_fields` |
| MODHOME-4.5 | 1 | `test_import_still_inert_with_homing_symbols` |

Build order: Task 1 → Task 2 → {Task 3, Task 4}. All four share
`scripts/check_graph.py` + `scripts/check_graph_test.py`, so `execute-plan`
serializes them into one worker regardless.
