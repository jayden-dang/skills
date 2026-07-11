# Design: Python spec linters

Feature code: PYPORT
Status: Approved
Date: 2026-07-10

## Context

Three linters — `check-trace.mjs`, `check-graph.mjs`, `vendor-linters.mjs` — are vendored into
every consuming repo and run in its hooks and CI. Their runtime is therefore a tax on every
user of this skill set, and Claude Code is a native binary that puts no `node` on PATH. ADR
0001 records the decision and its evidence: on macOS `/usr/bin/python3` and `/usr/bin/git` are
byte-identical Command Line Tools shims, so anyone who can run this git-based skill set already
has Python 3; and Node ships no XML parser, which the next feature (COVER) needs.

This feature changes the runtime and **nothing else**. That constraint is what shapes the whole
design: the existing `.mjs` is not merely prior art, it is the *specification*. Every behavior
question — does `normalizePath` strip this token, does the reverse index sort this way — is
answered by running the oracle, never by reading the port. The `.mjs` files therefore stay
in-tree for the duration and are deleted only when a differential test proves every fixture
agrees on stdout, stderr, and exit code.

The obvious alternative — rewrite in Python and port the existing tests as the only check — is
rejected because those tests were written against the `.mjs`. A subtly different regex or sort
order passes a rewritten test while changing real output. The oracle is the point.

### Decisions

1. **Python 3.9.6 floor, stdlib only.** macOS CLT ships 3.9.6. No `match` statement, no
   `X | Y` runtime unions. Modules: `re`, `json`, `hashlib`, `pathlib`, `os`, `sys`,
   `argparse`, `subprocess`, `tempfile`, `shutil`, `difflib`, `unittest`. (`xml.etree` belongs
   to COVER, not here.)
2. **The `.mjs` is the specification.** Behavior is defined by the oracle, proven by the parity
   corpus, and the oracle is deleted only once the corpus is green.
3. **The parity harness uses ONE working directory, reset between runs** — not two side-by-side
   copies. Verified: `check-trace.mjs:59` and `check-graph.mjs:389` print the **absolute** root
   path. Two copies at two paths would force the harness to normalize absolute paths before
   comparing, and normalization blinds it to exactly the divergences a port introduces (a wrong
   separator, a differently-realpath'd root). Same directory ⇒ identical path bytes ⇒ no
   normalization ⇒ no blind spot.
4. **JSON is byte-identical via `json.dumps(obj, indent=2, ensure_ascii=False)`** plus the
   newline `console.log` appends. Verified against both real outputs. The default
   `ensure_ascii=True` **differs**: it escapes the `…` elision marker of `capList` and the
   `—`/`→` in harvested interfaces to `…` etc.
5. **No runtime-authored text in output** (PYPORT-1.10). Both linters interpolate `${e.message}`
   from their JSON parser (`check-trace.mjs:59`, `check-graph.mjs:389`). V8 and CPython word
   that differently, making byte-identical stderr unreachable. **Prerequisite step:** before any
   parity fixture can exercise the bad-`trace.json` path, both oracles must first be amended to
   emit `could not parse <path>: invalid JSON`, and the ports must match. This edits the oracle
   deliberately; no test asserted the old text, so nothing else moves.
6. **Importable functions raise; only the CLI exits.** `check-graph.mjs` exports `loadConfig`,
   which calls `process.exit(1)` — importing it kills the caller's process.
7. **Entry-point guard compares real paths.** The `.mjs` compared `import.meta.url` against
   `pathToFileURL(process.argv[1])`, which is false under any symlinked path (macOS
   `/var` → `/private/var`), so a vendored linter under `/tmp` printed nothing and exited **0**.
8. **Python test files are named `*_test.py`** so `check-trace`'s existing default
   `testFilePattern` (`_test\.(rs|go|py)$`) scans them with no config change.
9. **`vendor_linters` gains a `legacy` drift verdict** for a vendored `.mjs`. It has no oracle
   and is exempt from parity (PYPORT-2.8).

## Architecture

### Module layout and the port strategy

Satisfies: PYPORT-1.1, PYPORT-1.2, PYPORT-1.3, PYPORT-1.4

Three modules, one per oracle, snake_case because the tests must `import` them (a hyphen is not
a legal Python module name):

| Oracle | Port | Public functions (snake_case of the `.mjs` exports) |
|---|---|---|
| `check-trace.mjs` | `check_trace.py` | no exports today; `main(argv)` plus internal helpers |
| `check-graph.mjs` | `check_graph.py` | `DEFAULTS` (data), `normalize_path`, `is_source_path`, `dedupe_by_fullest`, `classify_role`, `cap_list`, `extract_out_of_scope`, `extract_interfaces`, `harvest`, `render_graph_md`, `query`, `load_config` |
| `vendor-linters.mjs` | `vendor_linters.py` | `compute_stamp`, `read_stamp`, `restamp`, `install`, `check_drift`, `LINTERS` |

CLI flags are reproduced exactly (PYPORT-1.4) — `--root`, `--json`, `--strict`,
`--query --path P --keyword K`, `--verify`, `--install`, `--check`, `--stamp`, `--from`, `--to`,
`--scripts-dir`. `--harvest` is **not parsed at all**: `check-graph`'s `main()` never tests for
it (`check-graph.mjs:435,441`), it is the fall-through default mode, and the port must keep that
exact shape. `argparse` is **not** used for the primary parse: the oracles hand-roll
`args.indexOf(...)` and `collectFlag`, and tolerate unknown flags silently. `argparse` would
print a usage string and exit 2 on an unknown flag — a behavior change. The port keeps the
hand-rolled scan. (`vendor-linters`' exit 2 is for an **absent mode**, not an unknown flag.)

**A bounded code-shape deviation.** `check-graph.mjs` calls `process.exit` from five places and
`check-trace.mjs` exits at top level; the ports instead have `main()` **return** an int, with a
single `sys.exit` at the entry point. This is required by PYPORT-1.8 (importable functions must
not kill the caller) and is the one place the port's internal shape differs from the oracle's.
External behavior — exit codes, stdout, stderr — is unchanged, and the parity corpus is what
proves it.

### Output fidelity: JSON, sorting, and regex semantics

Satisfies: PYPORT-1.5

Three portability hazards, each resolved by construction and then checked by the oracle:

- **JSON.** `json.dumps(obj, indent=2, ensure_ascii=False)` + `"\n"` reproduces
  `JSON.stringify(obj, null, 2)` + `console.log`'s newline. Python's `indent` separators default
  to `(',', ': ')`, matching. Verified byte-identical on real `check-trace --json` and
  `check-graph --query --json` output.
- **Sorting.** The oracles use two orderings: plain `Array.prototype.sort()` (UTF-16 code-unit
  order) on paths, and `a.code.localeCompare(b.code)` on feature codes. Python's `sorted()` is
  code-point order. These agree for the BMP, and feature codes are `A-Z0-9` where
  `localeCompare` also agrees. This design **asserts nothing** about that: the parity corpus is
  the arbiter, and a fixture with mixed-case and digit-bearing codes exists to press it.
- **Regex.** JS `\d`/`\w` are ASCII; Python's are Unicode by default. Every ported pattern that
  relies on the ASCII reading carries `re.ASCII`. `matchAll` → `re.finditer`;
  `.replace(re, '')` with `/g` → `re.sub`. The risky ports are `normalize_path`'s fixpoint loop
  and the requirement-ID grammar.

### Entry point and process boundaries

Satisfies: PYPORT-1.6, PYPORT-1.7, PYPORT-1.8, PYPORT-1.9, PYPORT-1.10

```python
def _invoked_as_script():
    argv0 = sys.argv[0] if sys.argv else None
    if not argv0:
        return False                      # `python -c`, embedders
    try:
        return os.path.realpath(argv0) == os.path.realpath(__file__)
    except OSError:
        return False

if _invoked_as_script():
    sys.exit(main(sys.argv[1:]))
```

Comparing `realpath` on both sides is what makes a linter vendored under a symlinked path run
(PYPORT-1.6); the `argv[0]` guard covers `python -c` (PYPORT-1.7).

`load_config` **raises** `ConfigError` on unparseable `trace.json` (PYPORT-1.8). Only `main()`
catches it, prints `check-<tool>: could not parse <abs path>: invalid JSON` to stderr, and
returns 1 — the same exit code and, after decision 5, the same bytes as the amended oracle
(PYPORT-1.9, PYPORT-1.10). `main()` **returns** an int; `sys.exit` appears exactly once per
module, at the entry point.

### The parity oracle

Satisfies: PYPORT-2.1, PYPORT-2.2, PYPORT-2.3, PYPORT-2.4, PYPORT-2.5, PYPORT-2.6, PYPORT-2.8, PYPORT-5.1

Designed twice. **Rejected:** two side-by-side fixture copies (one per implementation) with a
minimal `Case` record. It has the smaller interface, but because both linters echo the absolute
root in their config-parse error, it must fold absolute paths to a `<ROOT>` sentinel before
comparing — and that fold hides any divergence *inside* a path. **Chosen:** a single working
directory, re-materialized between the two runs.

```python
# scripts/parity_test.py
CORPUS = [ {"id": ..., "linter": ..., "argv": [...], "tree": {...} | REAL_REPO, "writes": [...]} ]

for fx in CORPUS:
    with self.subTest(fixture=fx["id"], linter=fx["linter"]):     # PYPORT-2.5
        fresh(work);  o = run(oracle_cmd, work);  o_files = snapshot(work)
        fresh(work);  p = run(port_cmd,   work);  p_files = snapshot(work)
        assertEqual(o.code, p.code)      # 2.1
        assertEqual(o.out,  p.out)       # 2.2   bytes, never text
        assertEqual(o.err,  p.err)       # 2.3
        assertEqual(o_files, p_files)    # 5.1   GRAPH.md included
```

`fresh()` (rmtree + re-materialize) between the runs is what stops `--harvest`'s written
`GRAPH.md` from becoming the port's input. Snapshotting the tree after each run turns
"`GRAPH.md` is byte-identical" (PYPORT-5.1) into an assertion rather than a hope. Diagnostics
name the fixture, the linter, the stream, and the first differing byte offset with a
`difflib.unified_diff` (PYPORT-2.5).

The corpus is skipped when **the oracle is unavailable**, which is two distinct conditions —
`node` is not installed, *or* the `.mjs` files are gone:

```python
ORACLE_AVAILABLE = NODE is not None and all((SCRIPTS / m).exists() for m, _ in LINTERS.values())

@unittest.skipUnless(ORACLE_AVAILABLE, "oracle unavailable: node absent or .mjs deleted")
class Parity(unittest.TestCase): ...
```

Guarding on `NODE is None` alone would be wrong: after PYPORT-2.6 deletes the `.mjs` on a
machine that still has node, the corpus would invoke `node scripts/check-graph.mjs` against a
missing file and fail rather than skip.

The corpus covers every exit code and both stderr paths (PYPORT-2.4): a clean repo (0), trace
errors (1), `--strict` with warnings (1), a stale `GRAPH.md` (1), `vendor-linters` with no mode
(2), an **unparseable `trace.json`** (1, stderr), an **absent specs directory** (0, stderr), and
the real repo itself as the most realistic input. `vendor_linters`' `legacy` verdict and its
migration prompts are excluded from the corpus (PYPORT-2.8) — they have no oracle.

**Fixture IDs must be assembled at runtime.** `parity_test.py` lives under `scripts/`, a
configured `testGlob`, so a literal `ALPHA-1.1` in a fixture tree would be scanned as a citation
and fire a bogus E1 — the Fixture-ID/Citation confusion in `CONTEXT.md`. Build them as
`"ALPHA" + "-1.1"`.

### Coverage handover when the `.mjs` are deleted

Satisfies: PYPORT-2.7

`check-graph.test.mjs`, `check-graph.wiring.test.mjs`, `check-trace.test.mjs` and
`vendor-linters.test.mjs` are today the **only** covering tests for every FGRAPH-1.x…11.x and
TRACE-1.x requirement. Deleting them with the `.mjs` would turn `check-trace` red with dozens of
E2s at the exact moment the port claims success.

Each is ported to its `*_test.py` twin, and a **meta-test** guards the handover: it extracts the
requirement-ID set cited by the `.mjs` tests and the set cited by the `.py` tests, and asserts
the Python set is a superset. It runs while both exist; deletion is permitted only when it is
green.

The extraction on **both** sides must skip the files named in `docs/agents/trace.json`'s `ignore`
list, exactly as `check-trace` does. Otherwise the superset check reads `check-trace.test.mjs`'s
Fixture IDs (`RET-1.1`, `RET-9.9`) as citations and forces `check_trace_test.py` to reproduce
them — turning a coverage guard into a Fixture-ID propagator, the very confusion `CONTEXT.md`
defines away. `check_trace_test.py` inherits its twin's fixture-bearing status, so the `ignore`
list gains it alongside the existing entry. TRACE's five requirements stay uncovered exactly as
they are today (Out of Scope).

### `vendor_linters`: stamp, legacy verdict, consented migration

Satisfies: PYPORT-3.1, PYPORT-3.2, PYPORT-3.3, PYPORT-3.4, PYPORT-3.5, PYPORT-3.6

The stamp comment changes to `# @skills-linter: <name> sha256:<12hex>`, still computed over the
body with stamp lines filtered out, so stamping stays idempotent (PYPORT-3.1). `check_drift`
grows a fifth verdict: a consumer repo holding `check-trace.mjs` where a `.py` is expected
reports `legacy` (PYPORT-3.2). `install` writes the `.py` files (PYPORT-3.3); when a legacy
`.mjs` is present it **offers** removal and never removes without explicit consent
(PYPORT-3.4, PYPORT-3.5). If the legacy file's body does not hash to its own stamp it is a
`modified` copy carrying a local change, and the offer says so (PYPORT-3.6).

### Consumer surfaces and the interpreter indirection

Satisfies: PYPORT-4.1, PYPORT-4.2, PYPORT-4.3, PYPORT-4.4, PYPORT-4.5, PYPORT-4.6

`docs/agents/project.md` is already the layer where every repo command is recorded, so the
interpreter (`python3`, `python`, or `py`) lands in its Trace and Graph rows (PYPORT-4.1) —
which is how Windows is handled without auto-detection. `templates/githooks/pre-push`
(PYPORT-4.2) and the four SKILL.md files (PYPORT-4.3) name the Python linters. `README.md` gains
a Node-free install path — `git clone` + `link-skills.sh`, or the Claude Code plugin
(PYPORT-4.4). `DESIGN.md:44`'s script inventory currently reads
`check-trace.mjs, task-brief, review-package`; it gains the Python linters, and the artifact
model at `DESIGN.md:64-80` gains `GRAPH.md`, which it has never listed (PYPORT-4.5).
`setup-repo`'s proving gate treats an interpreter that cannot execute a linter as a **wiring
failure** (PYPORT-4.6), exactly as it already treats a missing `node`.

### Guards

Satisfies: PYPORT-5.2, PYPORT-5.3, PYPORT-5.4, PYPORT-5.5, PYPORT-5.6, PYPORT-5.7

`--verify` still exits zero on a fresh harvest (5.2). The `ignore` substring filter is ported
verbatim (5.3) even though COVER deletes it. A repo with zero requirements still exits zero
(5.4) — `setup-repo`'s proving gate depends on it. No new field appears in any spec artifact
(5.5). `task-brief`, `review-package`, `link-skills.sh` and `session-start.sh` remain
dependency-free bash (5.6). `brainstorm` and `code-review` still complete when the graph linter
is absent or errors (5.7).

## Seams for testing

Unit seams are the exported pure functions. The integration seam is the CLI black box
(temp-repo fixture + `subprocess` + `--json`), exactly as `check-trace.test.mjs` works today.
The differential seam is new and is the heart of this feature.

| Seam | Kind | Covers |
|---|---|---|
| `check_graph` pure functions (`normalize_path`, `is_source_path`, `dedupe_by_fullest`, `classify_role`, `cap_list`, `extract_out_of_scope`, `extract_interfaces`, `harvest`, `render_graph_md`, `query`) | unit | PYPORT-1.1, 1.2, 1.3 |
| `check_graph.load_config` (raises, never exits) | unit | PYPORT-1.8 |
| `vendor_linters` (`compute_stamp`, `read_stamp`, `restamp`, `install`, `check_drift`) | unit | PYPORT-1.1, 3.1, 3.2, 3.3, 3.6 |
| CLI black box via `subprocess` (`--json`, `--root`, all modes) | integration | PYPORT-1.4, 1.5, 1.9, 1.10, 5.2, 5.4 |
| CLI invoked through a symlinked path; and via `python -c` import | integration | PYPORT-1.6, 1.7 |
| **Differential parity corpus** (oracle vs port; stdout, stderr, exit, filesystem) | differential integration | PYPORT-2.1, 2.2, 2.3, 2.4, 2.5, 2.8, 5.1, 5.3 |
| Repo-state tripwire: no `scripts/*.mjs` remains, and the parity corpus **skips** cleanly | integration | PYPORT-2.6 |
| Meta-test: ID set cited by `.py` tests ⊇ ID set cited by `.mjs` tests | unit | PYPORT-2.7 |
| `vendor_linters` install into a scratch repo holding a legacy `.mjs` (consent required) | integration (E2E) | PYPORT-3.4, 3.5 |
| `templates/` file contents | unit | PYPORT-4.2 |
| SKILL.md / README.md / DESIGN.md durable markers | wiring regression | PYPORT-4.1, 4.3, 4.4, 4.5, 4.6, 5.5, 5.7 |
| Shell scripts' shebangs and absence of node/python invocations | unit | PYPORT-5.6 |
| Interpreter floor: AST scan rejecting 3.10+-only constructs by node-type **name**, **plus** `compile()` under a discovered 3.9 interpreter when one exists | unit | PYPORT-1.3 |

Two rows carry a caveat the reviewer surfaced, recorded rather than hidden.

**PYPORT-1.3 cannot be observed by `py_compile` alone.** `compile()` validates against the
*running* interpreter, so on a 3.12 CI runner a `match` statement — exactly what decision 1
forbids — compiles clean and the test passes green while asserting nothing. The seam is
therefore an `ast` walk rejecting 3.10+ constructs, *plus* an opportunistic `compile()` under a
real 3.9 binary when `shutil.which("python3.9")` or a 3.9-reporting `/usr/bin/python3` is found.

The walk must match node types **by name** (`type(n).__name__ == "Match"`), never by attribute:
verified on 3.9.6, `ast.Match` raises `AttributeError` and `sys.stdlib_module_names` does too.
Referencing either would crash the floor test on the very interpreter it guards while passing
green on a newer one. On 3.9 a `match` statement is not parseable at all, so `ast.parse`'s
`SyntaxError` *is* the detection; the node-type walk earns its keep only on 3.10+.

**PYPORT-2.6's seam is a tripwire, not coverage.** "No `.mjs` remains" asserts a committed-file
fact; it passes trivially once the files are deleted and can never fail meaningfully. The
substantive gate for 2.6 is that PYPORT-2.1–2.5 are green *before* deletion — enforced by task
ordering in `tasks.md`, not by an assertion. Stated plainly so nobody later mistakes the
tripwire for proof.

## Coverage check

Every PYPORT ID 1.1–5.7 appears in exactly one `Satisfies:` line. Cross-check: 1.1–1.4 → module
layout; 1.5 → output fidelity; 1.6–1.10 → entry point and process boundaries; 2.1–2.6, 2.8 +
5.1 → the parity oracle; 2.7 → coverage handover; 3.x → vendor_linters; 4.x → consumer surfaces;
5.2–5.7 → guards. No deliberately unmapped requirements.

**Requirement changed during design.** PYPORT-1.10 was added (a new ID under Story 1; nothing
renumbered). Designing the parity corpus proved PYPORT-2.3 unsatisfiable as approved: both
oracles interpolate the runtime's JSON-parser message, and V8's wording differs from CPython's.
Rather than reinterpret 2.3, the linters stop emitting runtime-authored text — in both
implementations — so 2.3 and 2.4 stand exactly as approved.
