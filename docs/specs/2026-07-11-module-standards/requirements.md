# Requirements: Per-Module Standards Resolution

Feature code: MODSTD
Status: Approved
Date: 2026-07-11

Slice M5 of the enterprise context layer. Gives each module a **standards**
layer: a small project-wide baseline plus optional per-module overrides,
authored inline in `docs/agents/trace.json` and resolved into the effective
standards for any module. A new `check-graph --standards <CODE>` mode emits the
resolved list. This slice delivers the *model, the resolver, and the emit/query
surface only*; wiring the resolved standards into `code-review`'s conformance
axis and `execute-plan`'s task briefs is deferred to M6 (gate integration).
Depends on M1 (MODMAP) for `load_manifest` and the module model. Design context:
`scratchpad/ENTERPRISE-CONTEXT-DESIGN.md` (D6).

Vocabulary (to be formalized in CONTEXT.md at design time): **baseline
standards** are the project-wide rule list at the top-level `standards` key of
the config; **module standards** are a module's own `standards` list; the
**effective standards** for a module are the baseline followed by that module's
own rules, deduplicated.

## 1. Declare standards

**MODSTD-1.1** THE SYSTEM SHALL read an optional project-wide baseline standards
list from the top-level `standards` key of the loaded config.

**MODSTD-1.2** THE SYSTEM SHALL read an optional per-module standards list from
each module manifest entry's `standards` field and expose it on the loaded
module.

**MODSTD-1.3** IF a module entry's `standards` is present but is not a list of
non-empty strings, THEN THE SYSTEM SHALL report a manifest-validity error for
that module (and never raise).

**MODSTD-1.4** IF the baseline `standards` is present but is not a list of
non-empty strings, THEN THE SYSTEM SHALL report a validity error on the same
channel as manifest-validity errors (and never raise).

**MODSTD-1.5** WHEN a module entry or the config omits `standards`, THE SYSTEM
SHALL treat it as having no standards at that level (an empty list), not an
error.

## 2. Resolve effective standards

**MODSTD-2.1** THE SYSTEM SHALL resolve a module's effective standards as the
baseline standards followed by that module's own standards, preserving that
order.

**MODSTD-2.2** THE SYSTEM SHALL deduplicate the resolved list, keeping the first
occurrence of each rule, so a module rule identical to a baseline rule appears
once.

**MODSTD-2.3** WHEN resolving standards for a code that is not a declared
module, THE SYSTEM SHALL return the baseline standards alone.

**MODSTD-2.4** WHEN neither the baseline nor the module declares any standards,
THE SYSTEM SHALL resolve to an empty list.

## 3. Emit resolved standards

**MODSTD-3.1** WHEN `check-graph --standards <CODE>` runs and `<CODE>` is a
declared module, THE SYSTEM SHALL print to standard output a JSON object
`{"module": <CODE>, "standards": [ ... ]}` carrying the resolved effective
standards, and return exit code 0.

**MODSTD-3.2** IF `check-graph --standards <CODE>` names a code that is not a
declared module, THEN THE SYSTEM SHALL print an error message and return exit
code 1.

**MODSTD-3.3** IF `check-graph --standards` is given without a following code,
THEN THE SYSTEM SHALL print an error message and return exit code 1.

**MODSTD-3.4** THE SYSTEM SHALL print byte-identical `--standards` output across
repeated runs over an unchanged config.

## 4. Isolation and safety (guards)

**MODSTD-4.1** (guard) WHEN no standards are declared anywhere, THE SYSTEM SHALL
CONTINUE TO run `--harvest`, `--verify`, `--query`, and `--seed` exactly as
today.

**MODSTD-4.2** (guard) THE SYSTEM SHALL CONTINUE TO expose each loaded module's
existing fields — code, name, owns, layer, owner — with the `standards` field
added additively.

**MODSTD-4.3** (guard) WHILE running `--standards`, THE SYSTEM SHALL NOT create,
modify, or delete any file.

**MODSTD-4.4** (guard) THE SYSTEM SHALL CONTINUE TO run `check_graph.py` with no
top-level import side effects.

## Out of Scope

- **Consuming standards in `code-review` or `execute-plan`.** The conformance
  axis and task-brief injection are M6 (gate integration).
- **Auto-harvesting standards from code.** Inferring conventions by scanning a
  module's source is a separate, later problem.
- **External standards files (`standardsRef`) or per-file standards.** M5 stores
  rules inline as short strings; long-form prose files are out of scope.
- **Per-feature standards overrides.** Standards attach to the baseline and to
  modules only; a feature inherits its home module's effective standards (that
  inheritance is exercised in M6, not here).
- **Standards inheritance across a module hierarchy.** Modules do not nest;
  there is exactly one baseline level and one module level.
