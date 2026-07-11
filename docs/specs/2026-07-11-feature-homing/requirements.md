# Requirements: Feature Homing Refinement & Facets

Feature code: MODHOME
Status: Approved
Date: 2026-07-11

Slice M3 of the enterprise context layer. Refines the **basic homing** M2
(MODGRAPH) shipped — where a feature is homed to a module only when every owned
path resolves to that one module, and every other case (orphan, double-mapped,
spanning, empty) collapses to `(unassigned)`. M3 makes homing legible: it
distinguishes a feature whose owned files genuinely **span** two or more real
modules (a structural smell worth surfacing) from a feature that is merely
un-homed; it attaches a feature's cross-module **touched** surface to the
feature as **facets** so a relationship to a non-home module is visible without a
second home; and it lets an author **override** the derived home with a
`Module:` line in the spec header. Depends on M1 (`load_manifest`,
`resolve_module`) and M2 (`harvest` homing, `render_all` shards). Design context:
`scratchpad/ENTERPRISE-CONTEXT-DESIGN.md` (decision D4).

Vocabulary (to be formalized in CONTEXT.md at design time): a feature **spans**
modules when its owned paths resolve to two or more distinct modules; a
**facet** is a module — other than the feature's home — that the feature relates
to through a touched (non-owned) path; a **home override** is an authored
`Module: CODE` line in a feature's `requirements.md` that fixes its home
regardless of what its owned files derive.

## 1. Surface the split signal

**MODHOME-1.1** WHEN a feature's owned paths resolve to two or more distinct
modules, THE SYSTEM SHALL classify that feature as **spanning**, distinct from a
feature that is un-homed because it has no owned paths, an orphan owned path, or
a double-mapped owned path.

**MODHOME-1.2** WHEN a feature is spanning and has no valid home override, THE
SYSTEM SHALL emit a `check-graph --verify` warning that names the feature code
and the distinct modules its owned paths fall in, and advises splitting the
feature per module or declaring a home.

**MODHOME-1.3** THE SYSTEM SHALL emit the split-signal warning on the
`--verify` warnings channel only, so that a spanning feature never changes the
`--verify` exit code.

**MODHOME-1.4** WHEN a feature is spanning, THE SYSTEM SHALL render it in the
`(unassigned)` shard, so no feature is dropped from the graph.

## 2. Attach cross-module facets

**MODHOME-2.1** WHEN a feature has a home module, THE SYSTEM SHALL record as that
feature's **facets** every module — other than its home — that is the single
resolved module of one of the feature's touched (non-owned) paths.

**MODHOME-2.2** THE SYSTEM SHALL exclude a feature's own home module from its
facet list.

**MODHOME-2.3** THE SYSTEM SHALL produce each feature's facet list sorted and
deduplicated, so a re-harvest of unchanged inputs yields identical facets.

**MODHOME-2.4** IF a feature's touched path resolves to no module or to more than
one module, THEN THE SYSTEM SHALL NOT derive a facet from that path.

**MODHOME-2.5** WHERE a feature homed to a module has one or more facets, THE
SYSTEM SHALL render those facets in that feature's row in its module shard, so
the cross-module relationship is visible in the sharded graph.

## 3. Honor the authored home override

**MODHOME-3.1** WHEN a feature's `requirements.md` header declares
`Module: CODE` and CODE is the code of a module in the manifest, THE SYSTEM
SHALL set that feature's home to CODE, overriding the home derived from its
owned paths.

**MODHOME-3.2** WHEN a valid `Module:` override sets a feature's home, THE
SYSTEM SHALL NOT emit the split-signal warning for that feature, because the
override resolves the ambiguity.

**MODHOME-3.3** IF a feature declares `Module: CODE` naming a code that is not in
the manifest, THEN THE SYSTEM SHALL ignore the override, retain the home derived
from the feature's owned paths, and emit a `--verify` warning naming the feature
and the unknown code.

**MODHOME-3.4** THE SYSTEM SHALL emit the invalid-override warning on the
`--verify` warnings channel only, so that an invalid override never changes the
`--verify` exit code.

## 4. Preserve today's behavior (guards)

**MODHOME-4.1** (guard) WHERE no valid manifest is present, THE SYSTEM SHALL
CONTINUE TO render and verify the flat `GRAPH.md` byte-for-byte as it does
today, performing no homing, facet derivation, split-signal, or override
processing.

**MODHOME-4.2** (guard) WHEN a manifest is present and every one of a feature's
owned paths resolves to the same single module, THE SYSTEM SHALL CONTINUE TO
home that feature to that module (the MODGRAPH-1.1 behavior).

**MODHOME-4.3** (guard) WHEN a manifest is present, THE SYSTEM SHALL CONTINUE TO
keep manifest-validity errors (`load_manifest`) and boundary errors (orphan and
double-mapped source folders) as `--verify` errors; only the split signal and
the invalid-override notice are advisory.

**MODHOME-4.4** (guard) THE SYSTEM SHALL CONTINUE TO expose each feature's
existing card fields — code, name, owns, touches, interfaces, oos, home — so the
added facet data is additive and the flat card render is unchanged.

**MODHOME-4.5** (guard) THE SYSTEM SHALL CONTINUE TO run `check_graph.py` with no
top-level import side effects.

## Out of Scope

- **Splitting a spanning feature automatically.** M3 only *flags* a span; it
  never edits specs or rewrites owned paths.
- **A second home.** A feature has at most one home; facets are edges, not
  additional homes. Multi-home modeling is not introduced.
- **Facets for un-homed features.** A spanning or orphan feature has no home, so
  no facets are derived for it; its cross-module spread is already visible in the
  index's cross-module shared-surface table (MODGRAPH-2.2).
- **Ranking or query changes.** Facets are rendered, not scored; the M2 IDF
  query ranking and cap are untouched.
- **Per-module standards, brownfield on-ramp, gate wiring.** Those are M4–M6.
- **A manifest schema field for facets.** Facets are derived from touched paths
  at harvest time, never authored in `trace.json`.
