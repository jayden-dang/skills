# Requirements: Python spec linters

Feature code: PYPORT
Status: Approved
Date: 2026-07-10

<!--
Origin: brainstorm 2026-07-10. The linters are vendored into every consuming repo and run in
its hooks and CI, so their runtime is a tax on every user. Evidence: on macOS `/usr/bin/python3`
and `/usr/bin/git` are byte-identical Command Line Tools shims, so anyone who can run this
git-based skill set already has Python 3; Claude Code is a native binary and puts no `node` on
PATH. Node also ships no XML parser, and the next feature (COVER) must tolerantly parse JUnit
XML — a format with no formal specification — under a zero-dependency rule. Recorded in
docs/adr/0001-python3-stdlib-for-the-spec-linters.md.

Decomposition (brainstorm): PYPORT (this) -> COVER (check-trace reads JUnit reports, retires
the TRACE `ignore` capability) -> FGRAPH Story 12 (graph scale). Order is load-bearing: porting
a language and changing behavior in the same step destroys the only cheap oracle we have. Here
the existing `.mjs` IS the specification, and a differential test proves the port exact.

Vocabulary already settled in CONTEXT.md: Covered, Citation, Fixture ID.
-->

## 1. The linters run on Python 3.9 stdlib

**Story:** As a developer adopting this skill set in any language's repo, I want the linters to run on the Python that ships with my machine, so that using the spec system costs me no extra runtime install.

- **PYPORT-1.1** THE SYSTEM SHALL provide `check_trace.py`, `check_graph.py`, and `vendor_linters.py`, each implementing the behavior of its `.mjs` counterpart.
- **PYPORT-1.2** THE SYSTEM SHALL import only Python standard-library modules, requiring no third-party package and no network access.
- **PYPORT-1.3** WHEN a linter is executed by CPython 3.9.6, THE SYSTEM SHALL run to completion without a syntax or runtime error.
- **PYPORT-1.4** THE SYSTEM SHALL accept each linter's existing command-line flags and arguments unchanged.
- **PYPORT-1.5** WHEN a linter runs in a `--json` mode, THE SYSTEM SHALL emit JSON byte-identical to the `.mjs` implementation's output for the same input.
- **PYPORT-1.6** WHEN a linter file is invoked as a script from a path containing a symbolic link, THE SYSTEM SHALL execute its command-line entry point.
- **PYPORT-1.7** WHEN a linter module is imported rather than invoked as a script, THE SYSTEM SHALL NOT execute its command-line entry point.
- **PYPORT-1.8** WHEN an importable function encounters a fatal condition, THE SYSTEM SHALL raise an exception rather than terminate the interpreter.
- **PYPORT-1.9** WHEN a linter's command-line entry point catches a fatal condition raised by PYPORT-1.8, THE SYSTEM SHALL emit the same diagnostic message and exit with the same code as the `.mjs` implementation does for that condition. _(The `.mjs` `loadConfig` is exported and calls `process.exit(1)` on an unparseable `trace.json`; the port keeps that external behavior while making the function safe to import.)_
- **PYPORT-1.10** THE SYSTEM SHALL NOT include text authored by the language runtime — such as an interpreter's exception message — in any linter's stdout or stderr. _(Added during design: `check-trace.mjs:59` and `check-graph.mjs:389` interpolate `${e.message}` from the JSON parser. V8 says "Expected property name or '}' in JSON at position 2"; CPython says "Expecting property name enclosed in double quotes: line 1 column 3". Byte-identical stderr (PYPORT-2.3) is unreachable while a runtime writes part of the message, so both implementations emit their own wording instead. No test asserted the old text.)_

## 2. Differential parity against the `.mjs` oracle

**Story:** As the maintainer of a correctness gate, I want the port proven identical to the implementation it replaces, so that a subtly different regex or sort order cannot hide inside a rewrite.

- **PYPORT-2.1** WHEN the parity suite runs a fixture repository through both a `.mjs` linter and its `.py` counterpart, THE SYSTEM SHALL assert that the two exit codes are equal.
- **PYPORT-2.2** WHEN the parity suite runs a fixture repository through both implementations, THE SYSTEM SHALL assert that the two stdout streams are byte-identical.
- **PYPORT-2.3** WHEN the parity suite runs a fixture repository through both implementations, THE SYSTEM SHALL assert that the two stderr streams are byte-identical.
- **PYPORT-2.4** THE parity suite SHALL exercise, for every linter, at least one fixture per distinct exit code that linter can return, and at least one fixture per code path that writes to stderr — including an unparseable `docs/agents/trace.json` and an absent specs directory.
- **PYPORT-2.8** WHERE a behavior is introduced by this feature and has no `.mjs` counterpart — the `legacy` drift status of PYPORT-3.2 and the migration of PYPORT-3.3 through PYPORT-3.6 — THE SYSTEM SHALL exempt it from the differential parity assertions, which compare only behavior the oracle exhibits.
- **PYPORT-2.5** IF any fixture yields differing output or exit codes, THEN THE SYSTEM SHALL fail the parity suite and name the differing fixture and linter.
- **PYPORT-2.6** WHEN every fixture in the parity suite agrees, THE SYSTEM SHALL remove the `.mjs` linters from the repository.
- **PYPORT-2.7** (guard) WHEN the `.mjs` linters and their test files are removed, THE SYSTEM SHALL CONTINUE TO provide, for every requirement that a `.mjs` test previously covered, a Python test citing that requirement's ID.

## 3. Vendoring migrates a consumer repo from `.mjs` to `.py`

**Story:** As a repo that already vendored `check-trace.mjs`, I want `setup-repo` to move me onto the Python linters without destroying a local change, so that upgrading is safe rather than lossy.

- **PYPORT-3.1** THE SYSTEM SHALL stamp each Python linter with a `# @skills-linter: <name> sha256:<digest>` line over its own body, the stamp line excluded from the digest.
- **PYPORT-3.2** WHEN the drift check runs against a repo whose vendored linter is a `.mjs` file, THE SYSTEM SHALL report that linter's status as `legacy`.
- **PYPORT-3.3** WHEN the install command runs, THE SYSTEM SHALL write the `.py` linters into the repo's configured scripts location.
- **PYPORT-3.4** IF a legacy `.mjs` linter is present when the install command runs, THEN THE SYSTEM SHALL offer to remove it.
- **PYPORT-3.5** THE SYSTEM SHALL NOT remove a legacy `.mjs` linter without the user's explicit consent.
- **PYPORT-3.6** IF a legacy `.mjs` linter's body does not match its own stamp, THEN THE SYSTEM SHALL warn that removing it discards a local modification.

## 4. Every consumer surface names the Python linters

**Story:** As an agent following a SKILL.md, I want the documented command to be the one that actually runs, so that a stale `.mjs` invocation never fails open the way the bare `check-graph` binary did.

- **PYPORT-4.1** WHEN `setup-repo` writes `docs/agents/project.md`, THE SYSTEM SHALL record the interpreter command for this machine (`python3`, `python`, or `py`) in the Trace and Graph rows.
- **PYPORT-4.2** THE `templates/githooks/pre-push` hook SHALL invoke the Python linters.
- **PYPORT-4.3** THE `setup-repo`, `brainstorm`, `code-review`, and `verify` skills SHALL name the Python linters in every command they instruct an agent to run.
- **PYPORT-4.4** THE `README.md` SHALL document an install path that requires no Node runtime.
- **PYPORT-4.5** THE `DESIGN.md` script inventory SHALL list the Python linters and the `GRAPH.md` artifact.
- **PYPORT-4.6** IF the configured interpreter cannot execute a linter at `setup-repo`'s proving gate, THEN THE SYSTEM SHALL classify it as a wiring failure and fix it before setup completes.

## 5. Guards — nothing else moves

**Story:** As a maintainer, I want the port to change the runtime and nothing else, so that a green suite after the port means the same thing it meant before.

- **PYPORT-5.1** (guard) WHEN `check_graph --harvest` runs over this repo's specs, THE SYSTEM SHALL CONTINUE TO produce a `GRAPH.md` byte-identical to the one the `.mjs` implementation produces.
- **PYPORT-5.2** (guard) WHEN `check_graph --verify` runs against a freshly harvested graph, THE SYSTEM SHALL CONTINUE TO exit zero.
- **PYPORT-5.3** (guard) WHERE `docs/agents/trace.json` provides an `ignore` array, THE SYSTEM SHALL CONTINUE TO exclude from the test-file scan any file whose repo-relative path contains any of the listed substrings.
- **PYPORT-5.4** (guard) WHEN a linter runs in a repository containing zero requirements, THE SYSTEM SHALL CONTINUE TO exit zero.
- **PYPORT-5.5** (guard) WHEN the port lands, THE SYSTEM SHALL CONTINUE TO require no new fields or annotations in `requirements.md`, `design.md`, or `tasks.md`.
- **PYPORT-5.6** (guard) WHEN the port lands, THE SYSTEM SHALL CONTINUE TO leave `task-brief`, `review-package`, `link-skills.sh`, and `session-start.sh` as dependency-free shell scripts.
- **PYPORT-5.7** (guard) IF the graph linter is absent or errors, THEN `brainstorm` and `code-review` SHALL CONTINUE TO complete without blocking.

## Out of Scope

- **Report-based coverage (the COVER feature).** `check_trace.py` ports the source-text scan exactly as it exists. Reading JUnit XML, deleting the source scan, and the `Covered`/`Fixture ID` semantics are the next spec, not this one.
- **Fixing TRACE.** The `ignore` capability is ported faithfully (PYPORT-5.3) even though COVER will delete it. TRACE stays `Approved` and structurally unshippable through this feature; that trap is COVER's to close.
- **Re-wording FGRAPH's criteria that name `.mjs` files.** FGRAPH-11.1, 11.4, 11.5, 11.6, 11.8 and 11.9 literally name `check-graph.mjs` / `check-trace.mjs`. A requirement should never have named an implementation filename; correcting that is a `sync-spec`/`amend` concern for FGRAPH, tracked separately.
- **Porting the shell scripts.** They are already runtime-free; rewriting them in Python would *add* the dependency this feature removes (PYPORT-5.6).
- **Type annotations, `mypy`, or a linter for the linters.** Stdlib and 3.9-compatible syntax only.
- **Publishing to PyPI or any package index.** The linters are vendored by file copy, exactly as they are today.
- **Windows interpreter auto-detection** beyond recording the command in `docs/agents/project.md`, which is already the indirection layer for every other repo command.
- **Performance work.** The port may be slower or faster; only behavior is specified.
- **FGRAPH Story 12** (graph scale: manifest/card split, IDF ranking, hub cutoff). Independent; sequenced last.
