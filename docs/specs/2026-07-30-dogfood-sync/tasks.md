# Tasks: Dogfood sync

> **For agentic workers:** pick the execute skill from `Execution-mode` and the
> run route — `execute-plan` (continuous + subagents), `execute-story`
> (story-unit + human review units), or `execute-inline` (controller implements,
> no implementer subagents). Steps use checkbox (`- [ ]`) syntax for tracking.

Feature code: DFSYNC
Status: Approved
Date: 2026-07-30
Execution-mode: continuous
Requirements: ./requirements.md
Design: ./design.md

**Goal:** Collapse a dogfood run's three disconnected files into one JSON artifact
that the agent and a person can both read and write, and add an optional loopback
server so the guide shows live state without ever letting a human tick become a
`pass`.

**Architecture:** `.skills/<slug>-dogfood.json` (`version: 2`) holds authored case
slots plus two disjoint per-case field spaces — `run` for the agent's
evidence-backed verdict and `human` for a person's tick — under a top-level `rev`.
All writes go through one store function that takes an `O_EXCL` lockfile, applies a
field-scoped patch, bumps `rev`, and lands via `os.replace`. `dogfood render` bakes
current verdicts into the guide so a `file://` page is correct with nothing running;
`dogfood serve` adds a loopback-only HTTP layer on top, whose shutdown terminates a
process only when `/whoami` returns the token recorded in its pidfile.

**Tech Stack:** Python 3 standard library only (`json`, `os`, `http.server`,
`secrets`, `signal`, `argparse`, `unittest`). Vanilla JS + CSS in a single HTML
shell, no build step, no bundler, no third-party runtime dependency.

## Global Constraints

Copied verbatim from `docs/agents/project.md` and `docs/architecture/INDEX.md`.

**Verify commands — run in this order; all must pass before any completion claim:**

| Check | Command |
|---|---|
| Typecheck | *(none)* |
| Lint | `python3 scripts/lint-skill-frontmatter.py && python3 scripts/lint-handoffs.py && python3 scripts/lint-context7.py` |
| Unit tests | `python3 -m unittest discover -s tests` |
| E2E / smoke | *(none)* |

Single test file: `python3 -m unittest tests.<module>`

**Test annotation convention** (from `docs/agents/project.md:118`): Requirement ID
in the test method name **or first-line docstring as greppable `CODE-N.M`**. This
plan uses the docstring form throughout, matching
`tests/test_prepare_change_wiring.py:16` — a method name like `test_DFSYNC_1_1`
does not contain the literal string `DFSYNC-1.1` and would be invisible to the
`trace` grep. **Every test in this plan opens with `"""DFSYNC-N.M — …"""`.**

**Architecture invariants** (verbatim, `docs/architecture/INDEX.md`):

- **ARCH-1** Trace and other vertical checks MUST be exact `grep`/`git`/file-read passes with fixed extraction rules and set differences — never an LLM judgment of whether a test "really" covers an ID.
- **ARCH-2** Optional project layers and config sections MUST no-op when absent: skills CONTINUES TO run without inventing vision, architecture invariants, team roster, or other standing facts that were never written.
- **ARCH-3** Consumer-repo adoption MUST require only the skills (plugin or npx) and markdown config — never mandate Python, vendored linters, CI jobs, or git-hook wiring for the full methodology; any hard headless gate is an optional documented add-on only.

**Forbidden in this feature:**

- Adding any third-party Python dependency. The CLI must import stdlib only — that
  is the ARCH-3 gain this feature exists to bank.
- Adding a `--host` flag, a bind address other than the literal `127.0.0.1`, or any
  auth/token layer on the HTTP surface. Deferred by requirements (Out of Scope).
- Any code path that writes `run.verdict` from an HTTP request, or that reads a
  `human` field when computing `next`. See ADR `docs/adr/0006-*`.
- Reading `.cases.yaml`, `.yml`, or `-run.md`. No migration path exists by decision.
- Adding a JS toolchain, bundler, or `package.json` to this repo.

**Workflow band:** Solo (`docs/agents/project.md:55`, headcount 1). Do not invent
reviewers or assignees.

**Known pre-existing failures — NOT caused by this work and NOT to be fixed here:**
`tests/test_plan_review_unit_contracts.py::test_story_unit_mode_and_preflight` and
`::test_unit_barrier_and_unit_review` have failed since commit `5d82820` split the
execute family. A full-suite run during this feature is green when it reports
exactly these two failures and no others. Do not claim green without saying so, and
do not fold a fix into this branch.

## File Structure

**Create:**

| Path | Responsibility |
|---|---|
| `tests/drive-dogfood/fixtures/notes-app/notes-dogfood.json` | The six-case notes fixture, converted to v2 with run state |
| `tests/test_dogfood_store.py` | The one new seam — locked, atomic, `rev`-checked commit |
| `tests/test_dogfood_serve.py` | Serve endpoints, bind address, pidfile, verified shutdown |
| `tests/test_dogfood_guide_contract.py` | Static contract assertions over `shell/guide.html` |

**Modify:**

| Path | Responsibility |
|---|---|
| `skills/acceptance/dogfood/scripts/dogfood` | v2 schema, store, command surface, `serve` |
| `skills/acceptance/dogfood/shell/guide.html` | Verdict badges, dual `file://` / `http://` mode |
| `skills/acceptance/dogfood/SKILL.md` | Authoring flow for v2; `serve` in the hand-over |
| `skills/acceptance/dogfood/references/cases-schema.md` | v2 schema reference |
| `skills/acceptance/drive-dogfood/SKILL.md` | Iron Law line, two rationalization rows, CLI recipe, ask-to-stop |
| `tests/test_dogfood_cli.py` | Rewritten against v2 |
| `tests/drive-dogfood/scenarios-cli.md` | CLI recipes updated to v2 paths |
| `docs/agents/project.md` | Trace-ignore paths; `Browser E2E` row |
| `docs/guide/skills/dogfood.md`, `docs/guide/skills/drive-dogfood.md` | Human docs |
| `CHANGELOG.md` | Release note |

**Delete:**

| Path | Reason |
|---|---|
| `tests/drive-dogfood/fixtures/notes-app/notes-dogfood.cases.yaml` | Superseded by the `.json` fixture |
| `tests/drive-dogfood/fixtures/notes-app/dogfood-guide.html` | Regenerated from the v2 fixture |

---

### Task 1: v2 run-file schema and the hard cut from v1

**Files:**
- Modify: `skills/acceptance/dogfood/scripts/dogfood` — delete `load_cases_yaml` (:53-94), `load_cases_html` (:197-272), `extract_label_block` (:275-291), `extract_title` (:294-300), `extract_req` (:303-308), `strip_tags` (:311-315), `collapse_ws` (:318-320), and the `try: import yaml` block (:18-21); rewrite `load_catalog` (:37-50) and `catalog_from_dict` (:117-155)
- Create: `tests/drive-dogfood/fixtures/notes-app/notes-dogfood.json`
- Delete: `tests/drive-dogfood/fixtures/notes-app/notes-dogfood.cases.yaml`
- Test: `tests/test_dogfood_cli.py`

**Reuse:** existing — extends the eight-slot case shape already validated by `normalize_case` (`scripts/dogfood:97`) (rung 2)

**Interfaces:**
- Consumes: nothing
- Produces: `load_run_file(path: Path) -> dict` returning the parsed v2 document with a top-level `rev`, `version`, `slug`, `sections`; `normalize_case` unchanged in signature and rules; `all_cases(doc) -> list[dict]` and `find_case(doc, case_id) -> dict | None` unchanged in signature

**Depends-on:** none

- [ ] **Step 1: Write the failing tests**

Convert the fixture first (it is test data, not production code), then write:

```python
# tests/test_dogfood_cli.py — replacing the v1 fixture constant and adding these
RUN = REPO / "tests" / "drive-dogfood" / "fixtures" / "notes-app" / "notes-dogfood.json"

class SchemaV2Tests(unittest.TestCase):
    def test_single_path_argument_carries_cases_and_run_state(self):
        """DFSYNC-1.1, DFSYNC-1.2 — one file argument yields both case bodies and run state."""
        doc = json.loads(RUN.read_text())
        self.assertEqual(2, doc["version"])
        self.assertIn("rev", doc)
        case = doc["sections"][0]["cases"][0]
        for slot in ("id", "req", "kind", "title", "setup", "try", "expect", "backend"):
            self.assertIn(slot, case)
        self.assertIn("run", case)
        self.assertIn("human", case)

    def test_run_and_human_key_names_never_overlap(self):
        """DFSYNC-2.1 — the two field spaces share no key name."""
        doc = json.loads(RUN.read_text())
        for case in iter_cases(doc):
            self.assertFalse(set(case["run"]) & set(case["human"]))

    def test_top_level_rev_is_an_integer(self):
        """DFSYNC-3.1 — rev is a plain integer at the document root."""
        self.assertIsInstance(json.loads(RUN.read_text())["rev"], int)

    def test_rejects_wrong_version_duplicate_id_bad_kind_missing_slot(self):
        """DFSYNC-1.5 — each malformation exits non-zero naming case and field."""
        for mutate, needle in [
            (lambda d: d.update(version=1), "version"),
            (lambda d: d["sections"][0]["cases"].append(d["sections"][0]["cases"][0]), "CASE-1"),
            (lambda d: d["sections"][0]["cases"][0].update(kind="chaos"), "chaos"),
            (lambda d: d["sections"][0]["cases"][0].pop("backend"), "backend"),
        ]:
            with self.subTest(needle=needle):
                doc = json.loads(RUN.read_text())
                mutate(doc)
                with tempfile.TemporaryDirectory() as tmp:
                    bad = Path(tmp) / "bad.json"
                    bad.write_text(json.dumps(doc))
                    cp = run_cli("list", str(bad), check=False)
                    self.assertNotEqual(0, cp.returncode)
                    self.assertIn(needle, cp.stderr)

    def test_stdlib_only_no_yaml_import(self):
        """DFSYNC-1.6 — the CLI imports no third-party module."""
        src = CLI.read_text()
        self.assertNotIn("import yaml", src)
        self.assertNotIn("PyYAML", src)

    def test_v1_paths_are_named_errors_not_parse_attempts(self):
        """DFSYNC-1.7 — a .yaml/.yml/-run.md path exits non-zero naming the v2 format."""
        with tempfile.TemporaryDirectory() as tmp:
            for name in ("old.cases.yaml", "old.yml", "notes-dogfood-run.md"):
                stale = Path(tmp) / name
                stale.write_text("version: 1\n")
                cp = run_cli("list", str(stale), check=False)
                self.assertNotEqual(0, cp.returncode)
                self.assertIn("v2", cp.stderr.lower())

    def test_list_output_unchanged(self):
        """DFSYNC-1.8 — one tab-separated id/req/kind/title line per case, in file order."""
        doc = json.loads(RUN.read_text())
        expected = [
            "\t".join((c["id"], c["req"], c["kind"], c["title"])) for c in iter_cases(doc)
        ]
        lines = [ln for ln in run_cli("list", str(RUN)).stdout.splitlines() if ln]
        self.assertEqual(expected, lines)

    def test_show_prints_all_eight_slots(self):
        """DFSYNC-1.9 — show still prints every authored slot."""
        out = run_cli("show", str(RUN), "CASE-3").stdout
        for slot in ("id:", "req:", "kind:", "title:", "setup:", "try:", "expect:", "backend:"):
            self.assertIn(slot, out)
```

Run: `python3 -m unittest tests.test_dogfood_cli` — expect: import/attribute errors and
non-zero-exit assertion failures, because `load_catalog` still dispatches on `.yaml`
and the JSON fixture does not exist yet.

- [ ] **Step 2: Convert the fixture**

Translate all six cases from `notes-dogfood.cases.yaml` to `notes-dogfood.json`
keeping every authored string byte-identical. Add `"version": 2`, `"rev": 0`, and
per case `"run": {"verdict": "pending", "saw": "", "server": "", "notes": ""}` and
`"human": {"checked": false, "at": "", "comment": ""}`. Delete the `.yaml` file.

- [ ] **Step 3: Implement the loader**

Delete every function listed under Files. Replace `load_catalog` with:

```python
def load_run_file(path: Path) -> Dict[str, Any]:
    path = path.resolve()
    if path.suffix.lower() in {".yaml", ".yml"} or path.name.endswith("-run.md"):
        raise SystemExit(
            f"error: {path.name} is a v1 artifact; this CLI reads only the v2 JSON "
            "run file (.skills/<slug>-dogfood.json). Delete the v1 files and re-author."
        )
    if not path.is_file():
        raise SystemExit(f"error: run file not found: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"error: {path.name} is not valid JSON: {exc}")
    if not isinstance(data, dict):
        raise SystemExit("error: run file must be a JSON object at the top level")
    return normalize_run_doc(data, source=str(path))
```

`normalize_run_doc` replaces `catalog_from_dict`: reject `version != 2` naming the
field, walk sections, run the existing `normalize_case` on each case (unchanged
rules — required slots, `KINDS` membership, duplicate-`id` rejection), and default
`rev` to `0`, `run` to all-pending, and `human` to unchecked when absent. Keep
`extract_dogfood_json` (:158-194) — it stays useful now that the embedded blob is
the whole document.

Run: `python3 -m unittest tests.test_dogfood_cli` — expect: pass.

- [ ] **Step 4: Commit**

`git commit -m "feat(dogfood): v2 JSON run file, drop YAML and HTML scrapers"`
`# trailers: Implements: DFSYNC-1.1, DFSYNC-1.2, DFSYNC-1.5, DFSYNC-1.6, DFSYNC-1.7 | Guards: DFSYNC-1.8, DFSYNC-1.9`

_Requirements: DFSYNC-1.1, DFSYNC-1.2, DFSYNC-1.5, DFSYNC-1.6, DFSYNC-1.7, DFSYNC-1.8, DFSYNC-1.9, DFSYNC-2.1, DFSYNC-3.1_

---

### Task 2: The store — lockfile, atomic replace, `rev` patch

**Files:**
- Modify: `skills/acceptance/dogfood/scripts/dogfood` — delete the ledger block `default_run_path` (:345-348), `init_ledger` (:351-375), `parse_ledger` (:378-413), `write_ledger` (:416-437) and the `HEADER_RE`/`FIELD_RE` constants (:341-342); add the store
- Create: `tests/test_dogfood_store.py`

**Reuse:** stdlib — `json`, `os.replace`, `os.open(O_CREAT|O_EXCL)` (rung 3)

**Interfaces:**
- Consumes: `load_run_file` from Task 1
- Produces: `commit(path: Path, patch: Callable[[dict], None], scope: str) -> dict` where `scope` is `"run"` or `"human"`; `LOCK_STALE_SECONDS = 10.0`; `RETRY_LIMIT = 50`

**Depends-on:** Task 1

- [ ] **Step 1: Write the failing test**

```python
# tests/test_dogfood_store.py
class StoreTests(unittest.TestCase):
    def test_commit_bumps_rev_and_replaces_atomically(self):
        """DFSYNC-3.2 — a commit lands via a temp file and os.replace, bumping rev."""
        path = self.fresh_run_file()
        before = json.loads(path.read_text())["rev"]
        commit(path, lambda d: set_verdict(d, "CASE-1", "pass"), scope="run")
        self.assertEqual(before + 1, json.loads(path.read_text())["rev"])
        self.assertEqual([], list(path.parent.glob("*.tmp*")))

    def test_stale_base_rev_reapplies_onto_current_document(self):
        """DFSYNC-3.3 — a patch built on an old rev is re-applied to current state."""
        path = self.fresh_run_file()
        stale = json.loads(path.read_text())            # reader at rev 0
        commit(path, lambda d: set_verdict(d, "CASE-1", "pass"), scope="run")
        commit(path, lambda d: tick(d, "CASE-2"), scope="human")   # built from `stale`
        doc = json.loads(path.read_text())
        self.assertEqual("pass", case_of(doc, "CASE-1")["run"]["verdict"])
        self.assertTrue(case_of(doc, "CASE-2")["human"]["checked"])

    def test_human_patch_never_touches_verdict(self):
        """DFSYNC-2.2 — a human-scoped commit leaves every verdict unchanged."""
        path = self.fresh_run_file()
        commit(path, lambda d: set_verdict(d, "CASE-1", "pass"), scope="run")
        commit(path, lambda d: tick(d, "CASE-1"), scope="human")
        self.assertEqual("pass", case_of(json.loads(path.read_text()), "CASE-1")["run"]["verdict"])

    def test_interrupted_write_leaves_previous_file_parseable(self):
        """DFSYNC-7.4 — no partial file is ever observable at the target path."""
        path = self.fresh_run_file()
        with mock.patch("json.dumps", side_effect=RuntimeError("boom")):
            with self.assertRaises(RuntimeError):
                commit(path, lambda d: set_verdict(d, "CASE-1", "pass"), scope="run")
        json.loads(path.read_text())            # still parses
        self.assertEqual([], list(path.parent.glob("*.tmp*")))

    def test_two_processes_interleaving_lose_nothing(self):
        """DFSYNC-3.4, DFSYNC-7.3 — 50 writes from each of two processes all land."""
        path = self.fresh_run_file()
        a = subprocess.Popen([sys.executable, WRITER, str(path), "run", "50"])
        b = subprocess.Popen([sys.executable, WRITER, str(path), "human", "50"])
        a.wait(timeout=60); b.wait(timeout=60)
        self.assertEqual(0, a.returncode); self.assertEqual(0, b.returncode)
        doc = json.loads(path.read_text())
        self.assertEqual(100, doc["rev"])
        self.assertEqual(50, sum(1 for c in iter_cases(doc) if c["run"]["notes"]))
        self.assertEqual(50, sum(1 for c in iter_cases(doc) if c["human"]["comment"]))
```

`WRITER` is a tiny helper script the test writes into its temp dir that calls
`commit` in a loop; the fixture is expanded to 50 cases by `fresh_run_file`.

Run: `python3 -m unittest tests.test_dogfood_store` — expect: `ImportError`/`NameError`
on `commit`, which does not exist yet.

- [ ] **Step 2: Implement the store**

```python
LOCK_STALE_SECONDS = 10.0
RETRY_LIMIT = 50
WRITABLE_SCOPES = {"run", "human"}


def _acquire(lock: Path) -> int:
    deadline = time.monotonic() + LOCK_STALE_SECONDS * 2
    while True:
        try:
            return os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
        except FileExistsError:
            try:
                age = time.time() - lock.stat().st_mtime
            except FileNotFoundError:
                continue
            if age > LOCK_STALE_SECONDS:
                lock.unlink(missing_ok=True)
                continue
            if time.monotonic() > deadline:
                raise SystemExit(f"error: could not acquire {lock.name} after {age:.0f}s")
            time.sleep(0.01)


def commit(path: Path, patch, scope: str) -> Dict[str, Any]:
    """Apply `patch` to the current document under an exclusive lock.

    `patch` receives the freshly-read document and must mutate only fields inside
    `scope`. Reading a stale copy beforehand is safe: the patch is always applied
    to the document as it exists now, which is what makes concurrent run/human
    writes converge (the two scopes share no key names).
    """
    if scope not in WRITABLE_SCOPES:
        raise SystemExit(f"error: unknown write scope {scope!r}")
    lock = path.with_suffix(path.suffix + ".lock")
    fd = _acquire(lock)
    tmp = path.with_suffix(path.suffix + f".tmp.{os.getpid()}")
    try:
        doc = load_run_file(path)
        patch(doc)
        doc["rev"] = int(doc.get("rev", 0)) + 1
        tmp.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp, path)
        return doc
    finally:
        tmp.unlink(missing_ok=True)
        os.close(fd)
        lock.unlink(missing_ok=True)
```

Add `import os, time` and `from unittest import mock` where needed. `RETRY_LIMIT` is
consumed by `_acquire`'s deadline; keep it exported for the serve layer.

Run: `python3 -m unittest tests.test_dogfood_store` — expect: pass.

- [ ] **Step 3: Commit**

`git commit -m "feat(dogfood): locked, atomic, rev-checked store"`
`# trailers: Implements: DFSYNC-3.2, DFSYNC-3.3, DFSYNC-3.4, DFSYNC-7.3, DFSYNC-7.4 | Guards: DFSYNC-2.2`

_Requirements: DFSYNC-2.2, DFSYNC-3.2, DFSYNC-3.3, DFSYNC-3.4, DFSYNC-7.3, DFSYNC-7.4_

---

### Task 3: Verdict commands on the store

**Files:**
- Modify: `skills/acceptance/dogfood/scripts/dogfood` — `cmd_init` (:543-551), `cmd_status` (:554-568), `cmd_next` (:571-577), `cmd_mark` (:580-618), `cmd_report` (:635-668), `build_parser` (:671-731)
- Test: `tests/test_dogfood_cli.py`

**Reuse:** existing — keeps the argparse subcommand layout (`scripts/dogfood:671`) and `validate_mark` unchanged (`:447`) (rung 2)

**Interfaces:**
- Consumes: `load_run_file` (Task 1), `commit` (Task 2)
- Produces: no new symbols; every subcommand now takes exactly one positional path

**Depends-on:** Task 1, Task 2

- [ ] **Step 1: Write the failing tests**

```python
class VerdictCommandTests(unittest.TestCase):
    def test_init_seeds_pending_and_preserves_existing_run_state(self):
        """DFSYNC-1.3 — init adds pending where absent and leaves recorded state alone."""

    def test_init_refuses_non_pending_file_without_force(self):
        """DFSYNC-1.4 — a file holding a real verdict is not re-seeded without --force."""

    def test_next_ignores_human_and_exits_1_when_all_pass(self):
        """DFSYNC-1.10, DFSYNC-2.3 — next reads only run.verdict; silent exit 1 when done."""
        # tick every case, assert `next` still returns CASE-1
        # then pass every case, assert stdout == "" and returncode == 1

    def test_pass_requires_saw_and_server(self):
        """DFSYNC-1.11 — pass with an empty --saw or --server is rejected."""

    def test_presentational_sentinel_enforced_both_directions(self):
        """DFSYNC-1.12 — the sentinel is required for presentational and refused elsewhere."""

    def test_status_reports_human_count_on_its_own_line(self):
        """DFSYNC-2.4 — the human tally is separate from the verdict tallies."""

    def test_report_has_a_human_column_and_escapes_pipes(self):
        """DFSYNC-1.13, DFSYNC-2.5 — one row per case, human column present, | escaped."""

    def test_mark_opens_no_socket(self):
        """DFSYNC-3.5 — mark performs no network call."""
        # assert the CLI source contains no socket/urllib use inside cmd_mark's call graph,
        # and run mark with a SIGALRM-guarded no-network sitecustomize that raises on connect

    def test_every_subcommand_works_with_no_server_running(self):
        """DFSYNC-5.8 — list/show/init/next/status/mark/report/render need no serve."""
```

Fill each body following the existing style in `tests/test_dogfood_cli.py`.

**Never hardcode a fixture requirement ID** (`NOTE-1.1` and friends) in any test.
Derive expected values from the fixture document, as `test_list_output_unchanged`
does in Task 1. This is why `tests/test_dogfood_cli.py` can leave the trace-ignore
list in Task 8 — see *Trace-ignore* under the coverage check.

Run: `python3 -m unittest tests.test_dogfood_cli` — expect: failures on the human
column, the human count line, and the `--catalog` argument still being required.

- [ ] **Step 2: Implement**

Rewrite the six commands against `load_run_file` + `commit`:

- `cmd_init` — `commit(..., scope="run")` seeding `verdict: pending` where the case
  has none; abort non-zero when any case holds a non-`pending` verdict and
  `--force` is absent.
- `cmd_next` — read `run.verdict` only; never touch `human`.
- `cmd_status` — existing verdict tallies plus `human: <n>`.
- `cmd_mark` — resolve `backend` from the same document (delete the `--catalog`
  argument and the `meta["source"]` fallback at :591-606), call `validate_mark`
  **unchanged**, then `commit(..., scope="run")`.
- `cmd_report` — add a `human` column between `verdict` and `saw`; keep `cell()`.
- `build_parser` — drop `--catalog`; every subcommand takes one positional path.

Run: `python3 -m unittest tests.test_dogfood_cli` — expect: pass.

- [ ] **Step 3: Commit**

`git commit -m "feat(dogfood): verdict commands read and write the v2 run file"`
`# trailers: Implements: DFSYNC-1.3, DFSYNC-1.4, DFSYNC-2.3, DFSYNC-2.4, DFSYNC-2.5, DFSYNC-3.5 | Guards: DFSYNC-1.10, DFSYNC-1.11, DFSYNC-1.12, DFSYNC-1.13, DFSYNC-5.8`

_Requirements: DFSYNC-1.3, DFSYNC-1.4, DFSYNC-1.10, DFSYNC-1.11, DFSYNC-1.12, DFSYNC-1.13, DFSYNC-2.3, DFSYNC-2.4, DFSYNC-2.5, DFSYNC-3.5, DFSYNC-5.8_

---

### Task 4: Render bakes verdicts; the guide is honest offline

**Files:**
- Modify: `skills/acceptance/dogfood/scripts/dogfood` — `render_html` (:484-513), `cmd_render` (:621-632)
- Modify: `skills/acceptance/dogfood/shell/guide.html` — CSS (:8-137), `renderCase` (:230-257), the IIFE head (:172-208)
- Create: `tests/test_dogfood_guide_contract.py`
- Test: `tests/test_dogfood_cli.py`
- Delete: `tests/drive-dogfood/fixtures/notes-app/dogfood-guide.html` (regenerated)

**Reuse:** existing — extends the `__CASES_JSON__` marker protocol (`scripts/dogfood:484`) and the guide's render IIFE (`shell/guide.html:172`) (rung 2)

**Interfaces:**
- Consumes: `load_run_file` (Task 1)
- Produces: rendered HTML whose embedded `window.__DOGFOOD__` is the whole v2 document plus `"rendered_at"`; `window.__DOGFOOD__.rendered_at` is what the offline banner prints

**Depends-on:** Task 1

- [ ] **Step 1: Write the failing tests**

```python
# tests/test_dogfood_cli.py
def test_render_embeds_verdicts_and_render_time(self):
    """DFSYNC-4.1 — the generated page carries each case's current verdict."""

def test_render_states_the_snapshot_is_not_live(self):
    """DFSYNC-4.3 — the page says verdicts are the render-time snapshot, with a timestamp."""

def test_render_keeps_the_five_data_attributes(self):
    """DFSYNC-4.5 — data-case/req/kind/backend/setup survive on each case element."""

def test_render_fails_without_markers(self):
    """DFSYNC-4.7 — a shell missing the marker pair exits non-zero."""

def test_render_preserves_two_character_newline_escapes(self):
    """DFSYNC-4.8 — \\n inside JSON strings is not expanded into a real newline."""

# tests/test_dogfood_guide_contract.py — static assertions over the shell source
def test_file_protocol_path_makes_no_network_call(self):
    """DFSYNC-4.2 — the offline branch contains no fetch/XHR/WebSocket."""

def test_every_interpolation_goes_through_an_escaper(self):
    """DFSYNC-4.4 — no case-supplied value reaches innerHTML unescaped."""

def test_localstorage_ticks_and_reset_survive(self):
    """DFSYNC-4.6 — the offline tick path still reads/writes localStorage and resets."""

def test_kind_chip_and_both_colour_schemes_survive(self):
    """DFSYNC-4.9 — the kind chip class and prefers-color-scheme block are intact."""

def test_verdict_badge_is_text_plus_colour_with_visible_focus(self):
    """DFSYNC-7.5 — verdict is never colour-only and ticks carry a focus indicator."""
```

Run: `python3 -m unittest tests.test_dogfood_cli tests.test_dogfood_guide_contract` —
expect: the badge, banner, and focus assertions fail; the guard assertions pass.

- [ ] **Step 2: Implement**

`render_html` embeds the whole document plus `rendered_at` (ISO-8601, UTC) — keep
the marker regex and the **callable** `_inject` exactly as they are, since that
callable is the reason `\n` survives. In the shell: add a `LIVE` constant
(`location.protocol === "http:" || location.protocol === "https:"`), a verdict badge
span per case reusing the `.chip` pattern with new `--pass/--fail/--blocked/--pending`
custom properties, an offline banner rendered only when `!LIVE`, and
`input[type=checkbox]:focus-visible { outline: 2px solid var(--accent); }`. Leave the
`localStorage` path untouched — it is the `!LIVE` branch.

Run: same two modules — expect: pass. Then regenerate the fixture guide:
`python3 skills/acceptance/dogfood/scripts/dogfood render tests/drive-dogfood/fixtures/notes-app/notes-dogfood.json -o tests/drive-dogfood/fixtures/notes-app/dogfood-guide.html`

- [ ] **Step 3: Commit**

`git commit -m "feat(dogfood): render bakes verdicts; guide declares its snapshot"`
`# trailers: Implements: DFSYNC-4.1, DFSYNC-4.3, DFSYNC-7.5 | Guards: DFSYNC-4.2, DFSYNC-4.4, DFSYNC-4.5, DFSYNC-4.6, DFSYNC-4.7, DFSYNC-4.8, DFSYNC-4.9`

_Requirements: DFSYNC-4.1, DFSYNC-4.2, DFSYNC-4.3, DFSYNC-4.4, DFSYNC-4.5, DFSYNC-4.6, DFSYNC-4.7, DFSYNC-4.8, DFSYNC-4.9, DFSYNC-7.5_

---

### Task 5: `dogfood serve` — the loopback layer

**Files:**
- Modify: `skills/acceptance/dogfood/scripts/dogfood` — add `cmd_serve` and the handler; register the subparser in `build_parser`
- Create: `tests/test_dogfood_serve.py`

**Reuse:** stdlib — `http.server.HTTPServer` + `secrets.token_hex` (rung 3)

**Interfaces:**
- Consumes: `commit` (Task 2), `render_html` (Task 4)
- Produces: `DEFAULT_PORT = 8787`; `bind_server(path: Path, token: str) -> HTTPServer`; routes `GET /`, `GET /state`, `POST /human/<case-id>`, `GET /whoami`

**Depends-on:** Task 2, Task 4

- [ ] **Step 1: Write the failing test**

```python
class ServeTests(unittest.TestCase):
    def test_binds_loopback_only(self):
        """DFSYNC-5.1, DFSYNC-7.2 — the listening socket is 127.0.0.1 and off-host is refused."""
        srv = bind_server(self.path, token="t")
        self.assertEqual("127.0.0.1", srv.server_address[0])

    def test_default_port_with_fallback_and_prints_actual_url(self):
        """DFSYNC-5.2 — 8787 by default, next free port when busy, real URL reported."""

    def test_one_process_serves_guide_and_state(self):
        """DFSYNC-5.3 — GET / returns the guide; GET /state returns verdicts and ticks."""

    def test_post_human_persists_a_tick(self):
        """DFSYNC-5.5 — a POST to /human/<id> lands in the run file's human field."""

    def test_post_rejects_verdict_bearing_keys(self):
        """DFSYNC-2.6 — any attempt to write verdict/saw/server/notes is 4xx and a no-op."""
        for key in ("verdict", "saw", "server", "notes"):
            status, _ = self.post(f"/human/CASE-1", {key: "x", "checked": True})
            self.assertEqual(400, status)
            self.assertEqual("pending", self.verdict_of("CASE-1"))

    def test_marked_verdict_visible_within_three_seconds(self):
        """DFSYNC-7.1 — a verdict written by mark shows up in /state inside the budget."""
```

Run: `python3 -m unittest tests.test_dogfood_serve` — expect: `NameError: bind_server`.

- [ ] **Step 2: Implement**

`bind_server` walks ports from `DEFAULT_PORT` upward on `OSError`, binding
`("127.0.0.1", port)` — the host is a literal, never a parameter. The handler:
`GET /` renders live via `render_html`; `GET /state` returns
`{"rev": …, "cases": {id: {"verdict": …, "human": {…}}}}`; `POST /human/<id>` reads a
JSON body, rejects with 400 unless its keys are a subset of
`{"checked", "comment", "base_rev"}`, then `commit(..., scope="human")`;
`GET /whoami` returns `{"token", "slug", "pid"}`. No route writes a verdict.

Run: `python3 -m unittest tests.test_dogfood_serve` — expect: pass.

- [ ] **Step 3: Commit**

`git commit -m "feat(dogfood): loopback serve layer with human-scoped writes"`
`# trailers: Implements: DFSYNC-2.6, DFSYNC-5.1, DFSYNC-5.2, DFSYNC-5.3, DFSYNC-5.5, DFSYNC-7.1, DFSYNC-7.2`

_Requirements: DFSYNC-2.6, DFSYNC-5.1, DFSYNC-5.2, DFSYNC-5.3, DFSYNC-5.5, DFSYNC-7.1, DFSYNC-7.2_

---

### Task 6: Pidfile identity and shutdown that requires proof

**Files:**
- Modify: `skills/acceptance/dogfood/scripts/dogfood` — `cmd_serve` gains pidfile write and `--stop`
- Test: `tests/test_dogfood_serve.py`

**Reuse:** stdlib — `os.kill`, `signal`, `json` (rung 3)

**Interfaces:**
- Consumes: `bind_server`, `DEFAULT_PORT` (Task 5)
- Produces: `pidfile_path(run_path: Path) -> Path`; `verify_live(pidfile: dict) -> bool`

**Depends-on:** Task 5

- [ ] **Step 1: Write the failing test**

```python
def test_pidfile_carries_pid_port_and_token(self):
    """DFSYNC-5.6 — the pidfile records the process id, the bound port, and an instance token."""

def test_background_launch_returns_control(self):
    """DFSYNC-5.7 — the documented launch backgrounds the server and the caller continues."""

def test_stop_kills_only_on_token_match(self):
    """DFSYNC-6.1 — --stop terminates the process when /whoami returns the pidfile token."""

def test_stop_on_recycled_pid_kills_nothing(self):
    """DFSYNC-6.2 — a pidfile pointing at a live unrelated process is cleaned, not killed."""
    victim = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
    self.write_pidfile(pid=victim.pid, port=self.free_port(), token="stale")
    cp = run_cli("serve", str(self.path), "--stop", check=False)
    self.assertIsNone(victim.poll())          # still alive
    self.assertFalse(self.pidfile.exists())
    victim.kill()

def test_serve_cleans_a_stale_pidfile_without_signalling(self):
    """DFSYNC-6.3 — startup applies the same verification to an existing pidfile."""

def test_no_termination_path_other_than_explicit_stop(self):
    """DFSYNC-6.5 — os.kill appears only in the --stop branch."""

def test_mark_result_identical_with_and_without_server(self):
    """DFSYNC-3.6 — mark produces the same run file whether or not serve is running."""
    # mark CASE-1 with no server; snapshot the document
    # reset, start serve, mark CASE-1 identically; assert the two documents match
    # except for rev, and that mark's stdout is byte-identical in both runs
```

This is the first point in the plan where both the store and the server exist, so
`DFSYNC-3.6` is proved here rather than in Task 3.

`test_stop_on_recycled_pid_kills_nothing` is the load-bearing one: it is the exact
scenario ADR 0007 exists for, and it fails loudly against a `kill -0` implementation.

Run: `python3 -m unittest tests.test_dogfood_serve` — expect: `NameError: pidfile_path`.

- [ ] **Step 2: Implement**

On start write `{"pid", "port", "token", "slug"}` to
`.skills/<slug>-dogfood-serve.pid` with `secrets.token_hex(16)`. `verify_live` GETs
`http://127.0.0.1:<port>/whoami` with a 1 s timeout and compares tokens. `--stop`:
verify → `os.kill(pid, signal.SIGTERM)` and remove the pidfile on match; on no
answer or mismatch remove the pidfile, print that the server is already gone, and
signal nothing. Startup runs the same check: a live matching server means print its
URL and exit 0 without starting a second.

Run: `python3 -m unittest tests.test_dogfood_serve` — expect: pass.

- [ ] **Step 3: Commit**

`git commit -m "feat(dogfood): token-verified server shutdown"`
`# trailers: Implements: DFSYNC-5.6, DFSYNC-5.7, DFSYNC-6.1, DFSYNC-6.2, DFSYNC-6.3, DFSYNC-6.5 | Guards: DFSYNC-3.6`

_Requirements: DFSYNC-3.6, DFSYNC-5.6, DFSYNC-5.7, DFSYNC-6.1, DFSYNC-6.2, DFSYNC-6.3, DFSYNC-6.5_

---

### Task 7: The guide goes live over HTTP

**Files:**
- Modify: `skills/acceptance/dogfood/shell/guide.html` — the IIFE gains the polling branch
- Test: `tests/test_dogfood_guide_contract.py`, `tests/test_dogfood_serve.py`

**Reuse:** existing — extends the guide render IIFE added in Task 4 (`shell/guide.html:172`) (rung 2)

**Interfaces:**
- Consumes: `GET /state`, `POST /human/<id>` (Task 5)
- Produces: nothing consumed downstream

**Depends-on:** Task 4, Task 5

- [ ] **Step 1: Write the failing test**

```python
# tests/test_dogfood_guide_contract.py
def test_live_branch_polls_state_and_posts_ticks(self):
    """DFSYNC-5.4 — the LIVE branch polls /state on an interval and repaints on rev change."""

def test_live_tick_posts_instead_of_writing_localstorage(self):
    """DFSYNC-5.5 — under http the tick handler POSTs and does not write localStorage."""

# tests/test_dogfood_serve.py
def test_served_page_carries_the_live_client(self):
    """DFSYNC-5.4 — the page served over http ships the polling client."""
```

Run: `python3 -m unittest tests.test_dogfood_guide_contract tests.test_dogfood_serve`
— expect: the polling assertions fail.

- [ ] **Step 2: Implement**

Under `LIVE`, `setInterval(poll, 1000)` fetching `/state`; when the returned `rev`
differs from the last seen, repaint each case's verdict badge and tick state. The
tick handler branches on `LIVE`: POST `{checked, comment, base_rev}` to
`/human/<id>` when live, write `localStorage` when not. The offline branch is
untouched, so Task 4's guards keep holding.

Run: same two modules — expect: pass.

- [ ] **Step 3: Commit**

`git commit -m "feat(dogfood): live polling and tick POST in the served guide"`
`# trailers: Implements: DFSYNC-5.4`

_Requirements: DFSYNC-5.4_

---

### Task 8: Skill bodies, docs, and the ask-to-stop step

**Files:**
- Modify: `skills/acceptance/drive-dogfood/SKILL.md` — Iron Law second line (:26), CLI recipe (:47-67), failure routing reference to cases YAML (:137), §5 close (:155-163), rationalization rows (:170-171), red flags (:180-185)
- Modify: `skills/acceptance/dogfood/SKILL.md` — §4 authoring (:82-113), §5 hand-over (:115-125), red flags (:141-145)
- Modify: `skills/acceptance/dogfood/references/cases-schema.md` — full rewrite for v2
- Modify: `tests/drive-dogfood/scenarios-cli.md`, `docs/agents/project.md`, `docs/guide/skills/dogfood.md`, `docs/guide/skills/drive-dogfood.md`, `CHANGELOG.md`
- Test: `tests/test_dogfood_cli.py` (skill-body contract assertions, matching the style of `tests/test_prepare_change_wiring.py`)

**Reuse:** existing — extends `drive-dogfood` §5 *Close the run* and `dogfood` §5 *Hand over* (rung 2)

**Interfaces:**
- Consumes: the command surface from Tasks 3, 6
- Produces: nothing

**Depends-on:** Task 3, Task 6, Task 7

- [ ] **Step 1: Write the failing test**

```python
def test_drive_dogfood_asks_before_stopping_the_server(self):
    """DFSYNC-6.4 — §5 requires asking the person whether to stop a server the agent started."""
    text = (REPO / "skills" / "acceptance" / "drive-dogfood" / "SKILL.md").read_text()
    self.assertRegex(text, r"ask .*whether to stop|serve --stop")
    self.assertNotIn("PROGRESS LIVES IN THE LEDGER", text)   # the ledger is gone
    self.assertIn("NO CASE IS TICKED ON THE SCREEN ALONE", text)  # the substance survives
```

Run: `python3 -m unittest tests.test_dogfood_cli` — expect: the ask assertion fails and
the stale Iron Law line is still present.

- [ ] **Step 2: Implement**

Rewrite the Iron Law's second line so it names the run file rather than a ledger,
keeping the first line verbatim. Replace the two localStorage rationalization rows
with rows that match the new model (a tick is recorded, never a verdict). Update the
CLI recipe to the single-path v2 commands. Add the §5 ask-to-stop step. Rewrite
`cases-schema.md` for v2. Record the browser-coverage decision in the `Browser E2E`
row of `docs/agents/project.md:132`.

**Trace-ignore — do this exactly.** In the ignore list at
`docs/agents/project.md:112`, **remove** `tests/test_dogfood_cli.py` and **do not
add** `tests/test_dogfood_store.py`, `tests/test_dogfood_serve.py`, or
`tests/test_dogfood_guide_contract.py`. Keep `tests/drive-dogfood/fixtures/` and
`tests/drive-dogfood/scenarios-cli.md` ignored — those still carry fixture IDs as
data. Then prove it:

```python
def test_dfsync_tests_are_visible_to_trace(self):
    """DFSYNC-6.4 — no module carrying a DFSYNC tag sits on the trace-ignore list."""
    ignore = (REPO / "docs" / "agents" / "project.md").read_text()
    for mod in ("test_dogfood_cli.py", "test_dogfood_store.py",
                "test_dogfood_serve.py", "test_dogfood_guide_contract.py"):
        self.assertNotIn(f"tests/{mod}", ignore)
```

Run: `python3 -m unittest discover -s tests` and the three lint scripts — expect:
pass, with exactly the two known pre-existing failures named in Global Constraints.

- [ ] **Step 3: Commit**

`git commit -m "docs(dogfood): skill bodies and references for the v2 run file"`
`# trailers: Implements: DFSYNC-6.4`

_Requirements: DFSYNC-6.4_

---

## Coverage check

| Story | IDs | Tasks |
|---|---|---|
| 1 — one artifact | 1.1–1.13 | T1 (1.1, 1.2, 1.5–1.9), T3 (1.3, 1.4, 1.10–1.13) |
| 2 — human channel | 2.1–2.6 | T1 (2.1), T2 (2.2), T3 (2.3–2.5), T5 (2.6) |
| 3 — two writers | 3.1–3.6 | T1 (3.1), T2 (3.2–3.4), T3 (3.5) — **3.6 see below** |
| 4 — guide alone | 4.1–4.9 | T4 (all) |
| 5 — live guide | 5.1–5.8 | T3 (5.8), T5 (5.1–5.3, 5.5), T6 (5.6, 5.7), T7 (5.4) |
| 6 — safe shutdown | 6.1–6.5 | T6 (6.1–6.3, 6.5), T8 (6.4) |
| 7 — quality | 7.1–7.5 | T2 (7.3, 7.4), T4 (7.5), T5 (7.1, 7.2) |

**DFSYNC-3.6** (`mark` behaves identically with and without a server running) needs
both the store and the server, so it is tagged on a test in **Task 6**, added there
as `test_mark_result_identical_with_and_without_server` — the first point in the
plan where both halves exist.

Every ID appears in exactly one task footer and on at least one docstring-tagged
test.

### Trace-ignore — the landmine this plan defuses

`tests/test_dogfood_cli.py` is currently on the trace-ignore list
(`docs/agents/project.md:112`), and `trace`'s NON-NEGOTIABLE section drops ignored
files **wholesale, never ID-by-ID**. Tagging `DFSYNC-N.M` inside an ignored module
would therefore read as *zero coverage* — every such ID would fire **E2** the moment
this feature's `Status:` reaches `Implemented`, long after the tests were written
and passing.

The file was ignored for a good reason: it hardcoded the notes fixture's fake
`NOTE-1.1`, which no requirements file defines, so leaving it visible would fire
**E1**. This plan removes the cause instead of living with the symptom — tests
derive expected values from the fixture document (Task 1, Task 3) — and Task 8 then
takes the file off the ignore list with a test that keeps it off.

### Browser coverage — what these tests do and do not prove

`design.md` flagged six IDs whose natural seam is a browser, against a repo that
records `Browser E2E (Playwright, Chromium): *(none)*`
(`docs/agents/project.md:132`) and whose test stack is `python3 -m unittest`. This
plan does **not** add a JS toolchain — that would put node, a bundler, and a browser
download into a repo whose vision constrains it to "Python linters only for *this*
repo's skill-set quality", and it is the user's call, not a side effect of a plan.

Those IDs are instead covered by **static contract tests** over `shell/guide.html`
(`tests/test_dogfood_guide_contract.py`), in the same style as the repo's existing
`tests/test_prepare_change_wiring.py` — deterministic file-read assertions, which is
what **ARCH-1** asks vertical checks to be. Server-side halves of DFSYNC-5.4 and
5.5 are covered behaviorally in `tests/test_dogfood_serve.py`.

State plainly what that buys: a static test proves the offline branch contains no
`fetch`, that every interpolation passes through an escaper, and that the polling
client ships — it does **not** prove a checkbox click fires a POST in a real
browser. That behavioral half belongs to `acceptance-ui`, which owns harness setup,
and Task 8 records the gap in the `Browser E2E` row rather than leaving it
undiscovered.

**Decided at the approval gate (2026-07-30):** static contract tests now, browser
behavior to `acceptance-ui` later — no Playwright harness in this branch. Tracker
publishing was also declined; `tasks.md` is the single source of truth for this
feature's work breakdown, with no GitHub issues mirroring it.
