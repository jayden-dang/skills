# Requirements: Brownfield On-Ramp — Manifest Seed

Feature code: MODSEED
Status: Approved
Date: 2026-07-11

Slice M4 of the enterprise context layer. Gives a specs-less existing codebase
an on-ramp into module mode: a new `check-graph --seed` mode **drafts** a module
manifest from the repository's own directory structure and prints it for a human
to review and paste into `docs/agents/trace.json`. Once a manifest exists, the
already-shipped `--harvest` (M2) renders the macro map and per-module shards and
`--verify` (M1) checks boundaries — so the seed is the one missing piece between
"10k files, zero specs" and a working module graph. The seed is a *suggestion
tool*: it authors nothing durable, mutates no file, and generates no specs.
Depends on M1 (MODMAP) for `load_manifest`, `enumerate_folders`, and the module
code shape. Design context: `scratchpad/ENTERPRISE-CONTEXT-DESIGN.md` (D2, D5).

Vocabulary (to be formalized in CONTEXT.md at design time): a **draft module** is
a `{code, name, owns}` entry the seed proposes from one source directory; a
**source root** is a configured `graph.sourceRoots` directory that exists on
disk; the **seed** is the advisory draft manifest as a whole.

## 1. Draft modules from the source tree

**MODSEED-1.1** WHEN `check-graph --seed` runs, THE SYSTEM SHALL produce one
draft module for each immediate child directory of each source root that exists
on disk.

**MODSEED-1.2** THE SYSTEM SHALL set each draft module's `owns` to the single
glob `<root>/<child>/**`, where `<root>/<child>` is that child directory's
repo-relative path.

**MODSEED-1.3** THE SYSTEM SHALL derive each draft module's `code` from its child
directory name normalized to a valid module code: uppercased, restricted to the
characters `A-Z0-9`, truncated to at most 12 characters, and matching
`^[A-Z][A-Z0-9]{1,11}$`.

**MODSEED-1.4** IF a child directory name would normalize to a code that is empty
or does not begin with a letter, THEN THE SYSTEM SHALL repair it to a valid code
by prefixing the letter `M` before truncation.

**MODSEED-1.5** THE SYSTEM SHALL set each draft module's `name` to the child
directory's own name (its last path segment, unmodified).

**MODSEED-1.6** WHEN two or more child directories derive the same code, THE
SYSTEM SHALL keep every drafted code unique by appending the smallest integer
suffix (starting at `2`) that yields an unused, still-valid code.

## 2. Emit an advisory draft

**MODSEED-2.1** WHEN `check-graph --seed` runs, THE SYSTEM SHALL print to standard
output a single JSON object of the form `{"modules": [ ... ]}` containing the
drafted modules.

**MODSEED-2.2** THE SYSTEM SHALL order the drafted modules by `code` and order
each module's `owns` list, so that repeated runs over an unchanged tree print
byte-identical output.

**MODSEED-2.3** THE SYSTEM SHALL return exit code 0 from a `--seed` run whenever
it produced a draft, including when the draft contains no modules.

**MODSEED-2.4** WHEN no configured source root exists on disk, THE SYSTEM SHALL
print `{"modules": []}` and return exit code 0.

## 3. Round-trip validity

**MODSEED-3.1** THE SYSTEM SHALL emit a draft that, when supplied as the
`modules` value of a config, loads through `load_manifest` with zero validity
errors.

**MODSEED-3.2** THE SYSTEM SHALL give every drafted module a non-empty `code`, a
non-empty `name`, and a non-empty `owns` list.

## 4. Isolation and safety (guards)

**MODSEED-4.1** (guard) WHILE running `--seed`, THE SYSTEM SHALL NOT create,
modify, or delete `docs/agents/trace.json` or any other file.

**MODSEED-4.2** (guard) WHEN a `modules` manifest already exists in the loaded
config, THE SYSTEM SHALL still draft from the source tree and print its draft,
without reading or reusing the existing manifest.

**MODSEED-4.3** (guard) THE SYSTEM SHALL CONTINUE TO dispatch `--harvest`,
`--verify`, and `--query` exactly as today; `--seed` is a distinct mode that
changes none of them.

**MODSEED-4.4** (guard) THE SYSTEM SHALL CONTINUE TO run `check_graph.py` with no
top-level import side effects.

## Out of Scope

- **CODEOWNERS and workspace-config parsing.** M4 drafts only from top-level
  directories; richer sources (CODEOWNERS, pnpm/Cargo/go workspaces) are a later
  slice.
- **Writing to `trace.json`.** The seed only prints; a human pastes and refines.
- **Loose files directly under a source root.** Only child *directories* become
  modules; files sitting directly in a root are left for the human to place (the
  boundary linter will flag them as orphans if uncovered).
- **Generating specs, deepening module cards, or harvesting code interfaces.**
  Document-on-first-touch and per-module standards are M5/later.
- **Merging a drafted module into an existing manifest.** The seed emits a fresh
  draft; reconciliation with any existing `modules` is the human's job.
