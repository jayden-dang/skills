# Tasks: Sharded Module Graph

> **For agentic workers:** REQUIRED SUB-SKILL: use `execute-plan` to implement
> this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

Feature code: MODGRAPH
Status: Approved
Date: 2026-07-11
Requirements: ./requirements.md
Design: ./design.md

**Goal:** Reorganize the feature graph around M1's modules — home each feature,
render a top index plus per-module shards (or today's flat `GRAPH.md` when no
manifest), and bound the query with IDF ranking + a top-N cap.

**Architecture:** All production code extends `scripts/check_graph.py`; all tests
extend `scripts/check_graph_test.py` (`unittest`). One pure
`render_all(graph, cfg) → {relpath: content}` feeds both `--harvest` (write +
prune) and `--verify` (compare), so they never drift. Homing runs inside
`harvest` on the uncapped owned set.

**Tech Stack:** Python 3 standard library (`json`, `os`, `re`, `sys`), `unittest`.

## Global Constraints

- **Python standard library only.** No third-party imports.
- **No top-level side effects on import** — new symbols are `def`s or
  module-level constants only.
- **After editing `scripts/check_graph.py`, re-stamp:**
  `python3 scripts/vendor_linters.py --stamp`.
- **All green after every task:** `python3 scripts/check_graph_test.py`,
  `python3 scripts/vendor_linters_test.py`, `python3 scripts/wiring_test.py`,
  `python3 scripts/check_trace.py` (clean), `python3 evals/evals.py --strict`.
- **Test tagging:** every test method carries its requirement IDs as a
  `# covers MODGRAPH-N.M` comment on the first body line (canonical hyphen.dot
  form — `check-trace` scans for that, and Python method names can't contain
  `-`/`.`).
- **Preserve flat behavior:** with no valid manifest, `harvest`/`render`/`verify`
  must produce byte-identical output to today. `render_graph_md`, `load_config`,
  and the two existing `_run_verify` checks (registration, M1 boundary) stay
  intact.

## File Structure

| File | Responsibility |
|---|---|
| `scripts/check_graph.py` | MODIFY — `_home_module`, homing in `harvest`, `render_all` + shard renderers, `--harvest` write/prune, `query` IDF scoring, `--query` CLI envelope, `_first_sentence`, `queryCap` default, `_run_verify` shard-set check. |
| `scripts/check_graph_test.py` | MODIFY — unit + integration tests; update 3 existing `--query` CLI tests to the new envelope. |

> Both files are shared across all tasks, so `execute-plan` runs the tasks
> **serially** (the disjoint-surface check demotes them). `Depends-on` records
> the true logical graph.

---

### Task 1: Feature homing in `harvest`

**Files:**
- Modify: `scripts/check_graph.py` (add `_home_module` after `resolve_module` ~L157; load the manifest near the top of `harvest` ~L430 and add `"home"` to the `features.append` dict ~L466)
- Test: `scripts/check_graph_test.py`

**Interfaces:**
- Consumes: `resolve_module(path, modules)` and `load_manifest(cfg)` (M1).
- Produces: `_home_module(owned_paths, modules) -> str|None`; each harvested
  feature dict gains `"home"` (a module code or `None`).

**Depends-on:** none

- [ ] **Step 1: Write the failing test**

```python
class HomeModuleTest(unittest.TestCase):
    def test_all_paths_one_module_homes_there_MODGRAPH_1_2(self):
        # covers MODGRAPH-1.2
        mods = [{"code": "AUTH", "owns": ["src/auth/**"]}]
        self.assertEqual(
            check_graph._home_module(["src/auth/a.ts", "src/auth/b.ts"], mods), "AUTH")

    def test_spanning_is_unassigned_MODGRAPH_1_3(self):
        # covers MODGRAPH-1.3
        mods = [{"code": "AUTH", "owns": ["src/auth/**"]},
                {"code": "BILL", "owns": ["src/billing/**"]}]
        self.assertIsNone(check_graph._home_module(["src/auth/a.ts", "src/billing/b.ts"], mods))

    def test_orphan_and_empty_are_unassigned_MODGRAPH_1_3(self):
        # covers MODGRAPH-1.3
        mods = [{"code": "AUTH", "owns": ["src/auth/**"]}]
        self.assertIsNone(check_graph._home_module(["src/auth/a.ts", "src/x/c.ts"], mods))
        self.assertIsNone(check_graph._home_module([], mods))


class HarvestHomingTest(_FixtureTestCase):
    def test_harvest_homes_on_uncapped_owns_MODGRAPH_1_1(self):
        # covers MODGRAPH-1.1
        # 12 auth files + 1 billing file: capped owns (first 12) would look
        # all-AUTH; only the UNCAPPED set reveals the billing span -> unassigned.
        paths = [f"src/auth/f{i}.ts" for i in range(12)] + ["src/billing/x.ts"]
        tasks_body = "## Tasks\n\n**Files:**\n" + "\n".join(f"- Create: {p}" for p in paths)
        specs = self._spec_fixture([
            {"slug": "wide", "code": "WIDE", "name": "Wide", "tasks": tasks_body}])
        cfg = {"specsDir": "docs/specs",
               "graph": {"sourceRoots": ["src"], "sourceExts": ["ts"], "cardCap": 12},
               "modules": [{"code": "AUTH", "name": "A", "owns": ["src/auth/**"]},
                           {"code": "BILL", "name": "B", "owns": ["src/billing/**"]}]}
        graph = check_graph.harvest(specs, cfg)
        f = next(x for x in graph["features"] if x["code"] == "WIDE")
        self.assertIsNone(f["home"])
```

Run: `python3 scripts/check_graph_test.py -k "HomeModule or HarvestHoming"` — expect:
`AttributeError: module 'check_graph' has no attribute '_home_module'`.

- [ ] **Step 2: Implement** — add after `resolve_module` in `scripts/check_graph.py`:

```python
def _home_module(owned_paths, modules):
    """Home a feature by its owned paths: the single module code iff every owned
    path resolves to that one module; else None (orphan, double-mapped, spanning,
    or empty owns → unassigned)."""
    if not owned_paths:
        return None
    codes = set()
    for p in owned_paths:
        hits = resolve_module(p, modules)
        if len(hits) != 1:
            return None
        codes.add(hits[0])
    return next(iter(codes)) if len(codes) == 1 else None
```

Then in `harvest`, right after the missing-specs early return and before
`req_files = _walk(...)`, load the manifest once:

```python
    _manifest_modules, _manifest_errs = load_manifest(cfg)
    if _manifest_errs:
        _manifest_modules = []
```

And add `"home"` to the `features.append({...})` dict (the uncapped `owns` is the
local `owns` list here, before the later cap pass):

```python
                "oos": extract_out_of_scope(text),
                "home": _home_module(sorted(owns), _manifest_modules),
```

Run: `python3 scripts/check_graph_test.py -k "HomeModule or HarvestHoming"` — expect: pass.

- [ ] **Step 3: Re-stamp and commit**

`python3 scripts/vendor_linters.py --stamp`
`git commit -m "feat(check-graph): home features to modules in harvest # Implements: MODGRAPH-1.1"`

_Requirements: MODGRAPH-1.1, MODGRAPH-1.2, MODGRAPH-1.3_

---

### Task 2: `render_all` — flat, index, and shards

**Files:**
- Modify: `scripts/check_graph.py` (add after `render_graph_md` ~L545)
- Test: `scripts/check_graph_test.py`

**Interfaces:**
- Consumes: `graph` (features carry `home` from Task 1), `render_graph_md`,
  `load_manifest`.
- Produces: `render_all(graph, cfg) -> dict[str, str]` (specsDir-relative path →
  content); module-level `_GRAPH_BANNER`.

**Depends-on:** Task 1

- [ ] **Step 1: Write the failing test**

```python
class RenderAllTest(_FixtureTestCase):
    def _sharded(self):
        specs = self._spec_fixture([
            {"slug": "a", "code": "AA", "name": "Aye",
             "tasks": "**Files:**\n- Create: src/auth/a.ts\n- Modify: src/shared/util.ts"},
            {"slug": "b", "code": "BB", "name": "Bee",
             "tasks": "**Files:**\n- Create: src/billing/b.ts\n- Modify: src/shared/util.ts"}])
        cfg = {"specsDir": "docs/specs",
               "graph": {"sourceRoots": ["src"], "sourceExts": ["ts"], "cardCap": 12, "queryCap": 8},
               "modules": [{"code": "AUTH", "name": "Auth", "owns": ["src/auth/**", "src/shared/**"]},
                           {"code": "BILL", "name": "Bill", "owns": ["src/billing/**"]}]}
        return check_graph.harvest(specs, cfg), cfg

    def test_shards_by_module_MODGRAPH_2_1_2_2_2_3(self):
        # covers MODGRAPH-2.1, MODGRAPH-2.2, MODGRAPH-2.3
        graph, cfg = self._sharded()
        files = check_graph.render_all(graph, cfg)
        self.assertIn("modules/AUTH.md", files)
        self.assertIn("modules/BILL.md", files)
        self.assertIn("## Modules", files["GRAPH.md"])
        self.assertIn("src/shared/util.ts", files["GRAPH.md"])   # cross-module shared
        self.assertIn("| AA |", files["modules/AUTH.md"])

    def test_unassigned_shard_MODGRAPH_2_4(self):
        # covers MODGRAPH-2.4
        specs = self._spec_fixture([
            {"slug": "x", "code": "XX", "name": "Ex",
             "tasks": "**Files:**\n- Create: src/auth/a.ts\n- Create: src/billing/b.ts"}])
        cfg = {"specsDir": "docs/specs",
               "graph": {"sourceRoots": ["src"], "sourceExts": ["ts"], "cardCap": 12, "queryCap": 8},
               "modules": [{"code": "AUTH", "name": "A", "owns": ["src/auth/**"]},
                           {"code": "BILL", "name": "B", "owns": ["src/billing/**"]}]}
        files = check_graph.render_all(check_graph.harvest(specs, cfg), cfg)
        self.assertIn("modules/_unassigned.md", files)
        self.assertIn("| XX |", files["modules/_unassigned.md"])
        self.assertNotIn("modules/AUTH.md", files)               # AUTH has no homed feature

    def test_flat_when_no_manifest_MODGRAPH_4_2(self):
        # covers MODGRAPH-4.2
        specs = self._spec_fixture([
            {"slug": "a", "code": "AA", "name": "Aye", "tasks": "**Files:**\n- Create: src/auth/a.ts"}])
        cfg = {"specsDir": "docs/specs",
               "graph": {"sourceRoots": ["src"], "sourceExts": ["ts"], "cardCap": 12, "queryCap": 8}}
        graph = check_graph.harvest(specs, cfg)
        self.assertEqual(check_graph.render_all(graph, cfg),
                         {"GRAPH.md": check_graph.render_graph_md(graph)})

    def test_deterministic_and_banner_MODGRAPH_2_5_2_7(self):
        # covers MODGRAPH-2.5, MODGRAPH-2.7
        graph, cfg = self._sharded()
        f1 = check_graph.render_all(graph, cfg)
        self.assertEqual(f1, check_graph.render_all(graph, cfg))
        self.assertIn("Do not edit by hand", f1["GRAPH.md"])
        self.assertIn("Do not edit by hand", f1["modules/AUTH.md"])

    def test_import_has_no_side_effects_MODGRAPH_4_6(self):
        # covers MODGRAPH-4.6
        import importlib, io, contextlib
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            mod = importlib.reload(check_graph)
        self.assertEqual(buf.getvalue(), "")
        self.assertTrue(hasattr(mod, "render_all"))
```

Run: `python3 scripts/check_graph_test.py -k RenderAll` — expect:
`AttributeError: module 'check_graph' has no attribute 'render_all'`.

- [ ] **Step 2: Implement** — add after `render_graph_md` in `scripts/check_graph.py`:

```python
_GRAPH_BANNER = "<!-- GENERATED by `check-graph --harvest`. Do not edit by hand; regenerated by sync-spec. -->"


def render_all(graph, cfg):
    """Render the graph to {specsDir-relative path: content}. Flat mode (no valid
    manifest) returns {"GRAPH.md": render_graph_md(graph)} unchanged. Manifest
    mode returns the module index at GRAPH.md plus one compact shard per module
    (and _unassigned) under modules/."""
    modules, errs = load_manifest(cfg)
    if errs or not modules:
        return {"GRAPH.md": render_graph_md(graph)}
    names = {m["code"]: m["name"] for m in modules}
    by_module = {}
    for f in graph["features"]:
        by_module.setdefault(f.get("home"), []).append(f)
    home_of = {f["code"]: f.get("home") for f in graph["features"]}

    idx = ["# Feature Graph", "", _GRAPH_BANNER, "", "## Modules", ""]
    for code in sorted(names):
        n = len(by_module.get(code, []))
        link = f" → modules/{code}.md" if n else ""
        idx.append(f"- {code} — {names[code]} ({n} features){link}")
    if by_module.get(None):
        idx.append(f"- (unassigned) — {len(by_module[None])} features → modules/_unassigned.md")
    idx += ["", "## Cross-module shared surface", "", "| Path | Modules |", "|---|---|"]
    for path in sorted(graph["reverse"]):
        homes = sorted({home_of.get(r["code"]) for r in graph["reverse"][path]
                        if home_of.get(r["code"]) is not None})
        if len(homes) >= 2:
            idx.append(f"| {path} | {', '.join(homes)} |")
    idx.append("")

    files = {"GRAPH.md": "\n".join(idx)}

    def shard(title, feats):
        rows = [f"# Module {title}", "", _GRAPH_BANNER, "", "| Feature | Name | Owns |", "|---|---|---|"]
        for f in sorted(feats, key=lambda x: x["code"]):
            rows.append(f"| {f['code']} | {f['name']} | {', '.join(f['owns']) or '—'} |")
        rows.append("")
        return "\n".join(rows)

    for code in sorted(k for k in by_module if k is not None):
        files[f"modules/{code}.md"] = shard(f"{code} — {names.get(code, code)}", by_module[code])
    if by_module.get(None):
        files["modules/_unassigned.md"] = shard("(unassigned)", by_module[None])
    return files
```

Run: `python3 scripts/check_graph_test.py -k RenderAll` — expect: pass.

- [ ] **Step 3: Re-stamp and commit**

`python3 scripts/vendor_linters.py --stamp`
`git commit -m "feat(check-graph): render sharded module graph # Implements: MODGRAPH-2.1"`

_Requirements: MODGRAPH-2.1, MODGRAPH-2.2, MODGRAPH-2.3, MODGRAPH-2.4, MODGRAPH-2.5, MODGRAPH-2.7, MODGRAPH-4.2, MODGRAPH-4.6_

---

### Task 3: `--harvest` writes shards and prunes stale ones

**Files:**
- Modify: `scripts/check_graph.py` (the default/`--harvest` block in `main`, ~L782-790)
- Test: `scripts/check_graph_test.py`

**Interfaces:**
- Consumes: `render_all(graph, cfg)` (Task 2).
- Produces: `--harvest` writes every rendered file and deletes any
  `modules/*.md` not in the rendered set.

**Depends-on:** Task 2

- [ ] **Step 1: Write the failing test**

```python
class HarvestWriteTest(_FixtureTestCase):
    def _module_repo(self):
        return self._tmp_repo({
            "src/auth/a.ts": "x",
            "docs/agents/trace.json": json.dumps({"specsDir": "docs/specs",
                "modules": [{"code": "AUTH", "name": "Auth", "owns": ["src/auth/**"]}]}),
            "docs/specs/INDEX.md": "| AUTH1 |\n",
            "docs/specs/f/requirements.md":
                "# Requirements: F\nFeature code: AUTH1\nStatus: Approved\n\n## Out of Scope\n- none\n",
            "docs/specs/f/tasks.md": "## Tasks\n\n**Files:**\n- Create: src/auth/a.ts\n",
        })

    def test_harvest_writes_shards_and_prunes_MODGRAPH_2_6(self):
        # covers MODGRAPH-2.6
        root = self._module_repo()
        os.makedirs(os.path.join(root, "docs/specs/modules"))
        with open(os.path.join(root, "docs/specs/modules/OLD.md"), "w") as fh:
            fh.write("stale")
        check_graph.main(["--harvest", "--root", root])
        self.assertTrue(os.path.exists(os.path.join(root, "docs/specs/modules/AUTH.md")))
        self.assertFalse(os.path.exists(os.path.join(root, "docs/specs/modules/OLD.md")))
```

Run: `python3 scripts/check_graph_test.py -k HarvestWrite` — expect: fail
(`modules/AUTH.md` not written; `OLD.md` not pruned).

- [ ] **Step 2: Implement** — replace the default `--harvest` block in `main`
  (currently writing a single `GRAPH.md`) with:

```python
    # default: --harvest
    graph = harvest(specs_dir, cfg)
    if not os.path.exists(specs_dir):
        print(f"check-graph: no specs dir at {cfg['specsDir']}", file=sys.stderr)
        return 0
    files = render_all(graph, cfg)
    for relpath, content in files.items():
        dest = os.path.join(specs_dir, relpath)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(content)
    modules_dir = os.path.join(specs_dir, "modules")
    if os.path.isdir(modules_dir):
        for name in sorted(os.listdir(modules_dir)):
            if name.endswith(".md") and f"modules/{name}" not in files:
                os.remove(os.path.join(modules_dir, name))
    print(f"check-graph: wrote GRAPH.md — {len(graph['features'])} features, {len(graph['shared'])} shared paths.")
    return 0
```

Run: `python3 scripts/check_graph_test.py -k HarvestWrite` — expect: pass.

- [ ] **Step 3: Re-stamp and commit**

`python3 scripts/vendor_linters.py --stamp`
`git commit -m "feat(check-graph): harvest writes+prunes module shards # Implements: MODGRAPH-2.6"`

_Requirements: MODGRAPH-2.6_

---

### Task 4: IDF ranking in `query`

**Files:**
- Modify: `scripts/check_graph.py` (the result-build + sort in `query`, ~L575-586)
- Test: `scripts/check_graph_test.py`

**Interfaces:**
- Consumes: `graph["reverse"]` (per-path `{code, role}` lists — `len` = document
  frequency).
- Produces: each `query` result gains a numeric `score`; results ordered by
  `(-score, code)`; `code`/`name`/`card`/`overlapPaths` preserved.

**Depends-on:** none

- [ ] **Step 1: Write the failing test**

```python
class QueryIdfTest(unittest.TestCase):
    def test_rare_overlap_outranks_hub_MODGRAPH_3_1_3_2(self):
        # covers MODGRAPH-3.1, MODGRAPH-3.2
        def feats(*cs):
            return [{"code": c, "name": c, "owns": [], "touches": [],
                     "interfaces": [], "oos": []} for c in cs]
        graph = {
            "features": feats("HUB", "RARE", "X", "Y", "Z"),
            "reverse": {
                "hub.ts": [{"code": c, "role": "owns"} for c in ("HUB", "RARE", "X", "Y")],  # df=4
                "rare.ts": [{"code": c, "role": "owns"} for c in ("RARE", "Z")],             # df=2
            },
            "shared": [],
        }
        res = check_graph.query(graph, paths=["hub.ts", "rare.ts"])
        self.assertEqual(res[0]["code"], "RARE")               # 0.25 + 0.5 beats hub-only 0.25
        self.assertGreater(res[0]["score"], res[1]["score"])
        self.assertIn("card", res[0])                          # MODGRAPH-4.5 fields preserved

    def test_result_keeps_existing_fields_MODGRAPH_4_5(self):
        # covers MODGRAPH-4.5
        graph = {"features": [{"code": "A", "name": "A", "owns": [], "touches": [],
                               "interfaces": [], "oos": []}],
                 "reverse": {"p.ts": [{"code": "A", "role": "owns"}]}, "shared": []}
        r = check_graph.query(graph, paths=["p.ts"])[0]
        for k in ("code", "name", "card", "overlapPaths"):
            self.assertIn(k, r)
```

Run: `python3 scripts/check_graph_test.py -k QueryIdf` — expect: fail
(`res[0]` has no `score`, order is by count).

- [ ] **Step 2: Implement** — in `query`, when building each result add a `score`
  and change the sort. Replace the results-build + sort tail so each result is:

```python
        score = sum(1.0 / len(graph["reverse"][p]) for p in entry["overlapPaths"]
                    if graph["reverse"].get(p))
        results.append(
            {
                "code": feature["code"],
                "name": feature["name"],
                "card": feature,
                "overlapPaths": sorted(entry["overlapPaths"]),
                "score": score,
            }
        )
    results.sort(key=lambda r: (-r["score"], r["code"]))
    return results
```

Then run the whole suite; if any existing `query` test asserted the old
`(-len(overlapPaths), code)` order, update its expected order to the score-based
order (note the change in the commit): `python3 scripts/check_graph_test.py`.

Run: `python3 scripts/check_graph_test.py -k QueryIdf` — expect: pass, and the
full suite green.

- [ ] **Step 3: Re-stamp and commit**

`python3 scripts/vendor_linters.py --stamp`
`git commit -m "feat(check-graph): IDF-weight query ranking # Implements: MODGRAPH-3.1"`

_Requirements: MODGRAPH-3.1, MODGRAPH-3.2, MODGRAPH-4.5_

---

### Task 5: `--query` CLI — cap, omitted count, out-of-scope truncation

**Files:**
- Modify: `scripts/check_graph.py` (`DEFAULTS["graph"]` ~L23-27 add `queryCap`;
  add `_first_sentence`; the `--query` block in `main` ~L770-777)
- Test: `scripts/check_graph_test.py` (add new tests; **update the 3 existing
  `--query` CLI tests** that assert a bare list)

**Interfaces:**
- Consumes: `query(...)` (Task 4), `cfg["graph"]["queryCap"]`.
- Produces: `_first_sentence(s) -> str`; `--query --json` emits
  `{"results": [...], "omitted": N}`; text mode prints capped `CODE (n)` lines +
  a `(+N more omitted)` trailer.

**Depends-on:** Task 4

- [ ] **Step 1: Write the failing test** — add new tests AND update the three
  existing ones:

```python
class FirstSentenceTest(unittest.TestCase):
    def test_first_sentence_MODGRAPH_3_5(self):
        # covers MODGRAPH-3.5
        self.assertEqual(check_graph._first_sentence("One thing. Two thing."), "One thing.")
        self.assertEqual(check_graph._first_sentence("no terminator"), "no terminator")


class QueryCliTest(_FixtureTestCase):
    def test_cap_and_omitted_and_oos_truncation_MODGRAPH_3_3_3_4_3_5(self):
        # covers MODGRAPH-3.3, MODGRAPH-3.4, MODGRAPH-3.5
        import io, contextlib
        feats = [{"slug": f"f{i}", "code": f"WID{i}", "name": "Widget maker",
                  "oos": ["First sentence. Second sentence."]} for i in range(4)]
        specs = self._spec_fixture(feats)
        root = os.path.dirname(os.path.dirname(specs))
        os.makedirs(os.path.join(root, "docs/agents"), exist_ok=True)
        with open(os.path.join(root, "docs/agents/trace.json"), "w") as fh:
            json.dump({"specsDir": "docs/specs", "graph": {"queryCap": 2}}, fh)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            check_graph.main(["--query", "--json", "--root", root, "--keyword", "widget"])
        parsed = json.loads(buf.getvalue())
        self.assertEqual(len(parsed["results"]), 2)          # capped
        self.assertEqual(parsed["omitted"], 2)               # 4 matched, 2 shown
        self.assertEqual(parsed["results"][0]["card"]["oos"], ["First sentence."])  # truncated
```

Update these THREE existing tests to the `{results, omitted}` envelope:
- `test_valueless_keyword_flag_exits_zero_with_empty_result`: change
  `self.assertEqual(json.loads(stdout), [])` →
  `self.assertEqual(json.loads(stdout), {"results": [], "omitted": 0})`.
- `test_flags_accepted_unchanged`: change `parsed[0]["code"]` →
  `parsed["results"][0]["code"]`.
- `test_query_emits_fresh_json_to_stdout_without_a_prior_harvest`: change
  `parsed[0]["code"]` → `parsed["results"][0]["code"]`.

Run: `python3 scripts/check_graph_test.py -k "FirstSentence or QueryCli"` — expect:
`AttributeError: ... '_first_sentence'`.

- [ ] **Step 2: Implement**

Add `queryCap` to `DEFAULTS["graph"]` beside `cardCap`:

```python
        "cardCap": 12,
        "queryCap": 8,
```

Add near the other helpers:

```python
_SENTENCE_END_RE = re.compile(r"[.!?](?:\s|$)")


def _first_sentence(s):
    """Text up to and including the first sentence terminator, else the whole string."""
    m = _SENTENCE_END_RE.search(s)
    return s[:m.end()].strip() if m else s.strip()
```

Replace the `--query` block in `main` with:

```python
    if "--query" in argv:
        graph = harvest(specs_dir, cfg)
        res = query(graph, paths=_collect_flag(argv, "--path"), keywords=_collect_flag(argv, "--keyword"))
        cap = cfg["graph"]["queryCap"]
        kept, omitted = res[:cap], max(0, len(res) - cap)
        for r in kept:
            r["card"] = dict(r["card"], oos=[_first_sentence(x) for x in r["card"]["oos"]])
        if as_json:
            print(json.dumps({"results": kept, "omitted": omitted}, indent=2, ensure_ascii=False))
        else:
            print("\n".join(f"{r['code']} ({len(r['overlapPaths'])})" for r in kept))
            if omitted:
                print(f"(+{omitted} more omitted)")
        return 0
```

Run: `python3 scripts/check_graph_test.py` — expect: pass (new + updated tests).

- [ ] **Step 3: Re-stamp and commit**

`python3 scripts/vendor_linters.py --stamp`
`git commit -m "feat(check-graph): bound --query with cap+omitted+oos-trunc # Implements: MODGRAPH-3.3"`

_Requirements: MODGRAPH-3.3, MODGRAPH-3.4, MODGRAPH-3.5_

---

### Task 6: `--verify` checks the shard set + content

**Files:**
- Modify: `scripts/check_graph.py` (the freshness block in `_run_verify`, ~L712-719)
- Test: `scripts/check_graph_test.py`

**Interfaces:**
- Consumes: `render_all(graph, cfg)` (Task 2).
- Produces: `--verify` compares every rendered file to its committed copy and
  flags stale shard files; registration + M1 boundary checks unchanged.

**Depends-on:** Task 2

- [ ] **Step 1: Write the failing test**

```python
class VerifyShardsTest(_FixtureTestCase):
    def _built_module_repo(self):
        root = self._tmp_repo({
            "src/auth/a.ts": "x",
            "docs/agents/trace.json": json.dumps({"specsDir": "docs/specs",
                "modules": [{"code": "AUTH", "name": "Auth", "owns": ["src/auth/**"]}]}),
            "docs/specs/INDEX.md": "| AUTH1 |\n",
            "docs/specs/f/requirements.md":
                "# Requirements: F\nFeature code: AUTH1\nStatus: Approved\n\n## Out of Scope\n- none\n",
            "docs/specs/f/tasks.md": "## Tasks\n\n**Files:**\n- Create: src/auth/a.ts\n",
        })
        check_graph.main(["--harvest", "--root", root])   # write index + shards
        return root

    def test_clean_after_harvest_MODGRAPH_4_1(self):
        # covers MODGRAPH-4.1
        root = self._built_module_repo()
        self.assertEqual(check_graph.main(["--verify", "--root", root]), 0)

    def test_edited_shard_is_stale_MODGRAPH_4_1(self):
        # covers MODGRAPH-4.1
        root = self._built_module_repo()
        with open(os.path.join(root, "docs/specs/modules/AUTH.md"), "w") as fh:
            fh.write("tampered")
        self.assertEqual(check_graph.main(["--verify", "--root", root]), 1)

    def test_extra_shard_is_stale_MODGRAPH_4_1(self):
        # covers MODGRAPH-4.1
        root = self._built_module_repo()
        with open(os.path.join(root, "docs/specs/modules/GHOST.md"), "w") as fh:
            fh.write("leftover")
        self.assertEqual(check_graph.main(["--verify", "--root", root]), 1)

    def test_boundary_and_registration_still_run_MODGRAPH_4_3_4_4(self):
        # covers MODGRAPH-4.3, MODGRAPH-4.4
        import io, contextlib
        root = self._built_module_repo()
        # orphan a source folder (M1 boundary error) + drop the INDEX registration
        os.makedirs(os.path.join(root, "src/orphan"))
        with open(os.path.join(root, "src/orphan/z.ts"), "w") as fh:
            fh.write("x")
        with open(os.path.join(root, "docs/specs/INDEX.md"), "w") as fh:
            fh.write("(empty)\n")
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = check_graph.main(["--verify", "--root", root])
        out = buf.getvalue()
        self.assertEqual(rc, 1)
        self.assertIn("orphan", out.lower())                 # M1 boundary still runs (4.3)
        self.assertIn("not registered in INDEX.md", out)     # registration still runs (4.4)
```

Run: `python3 scripts/check_graph_test.py -k VerifyShards` — expect: the edited/extra
shard cases FAIL (verify only checks GRAPH.md today).

- [ ] **Step 2: Implement** — in `_run_verify`, replace the single-`GRAPH.md`
  freshness block (build `graph_md_path`, read `committed`, compare to
  `render_graph_md(graph)`) with a render_all set+content check:

```python
    files = render_all(graph, cfg)
    for relpath, content in files.items():
        p = os.path.join(specs_dir, relpath)
        committed = None
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as fh:
                committed = fh.read()
        if committed != content:
            errors.append(f"{relpath} is stale — run `check-graph --harvest` and commit the result.")
    modules_dir = os.path.join(specs_dir, "modules")
    if os.path.isdir(modules_dir):
        for name in sorted(os.listdir(modules_dir)):
            if name.endswith(".md") and f"modules/{name}" not in files:
                errors.append(f"E: stale shard modules/{name} — run `check-graph --harvest`.")
```

(The registration check and the M1 `_verify_boundaries` block below stay exactly
as they are.)

Run: `python3 scripts/check_graph_test.py` — expect: pass, full suite green.

- [ ] **Step 3: Full green + re-stamp + commit**

`python3 scripts/vendor_linters.py --stamp`
`python3 scripts/check_graph_test.py && python3 scripts/vendor_linters_test.py && python3 scripts/wiring_test.py && python3 scripts/check_trace.py && python3 evals/evals.py --strict`
`git commit -m "feat(check-graph): verify the shard set + content # Implements: MODGRAPH-4.1"`

_Requirements: MODGRAPH-4.1, MODGRAPH-4.3, MODGRAPH-4.4_
