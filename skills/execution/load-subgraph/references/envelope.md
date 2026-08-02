# Result envelope

## Required fields (every run)

```text
advisory: true
schema_version: "1.1"
recipe_id: "fsubr-1.1"
owns_coverage:
  with_owns: <int>      # CODEs with non-empty OWNS after P1
  registered: <int>     # INDEX registry size
  ratio: <float>        # with_owns / registered (0 if registered=0)
p0:
  matched: <int>
  returned: <int>
  truncated: <bool>
notes: []               # non-fatal reliability notes (no silent count cap)
```

Plus exactly one query payload:

| Query | Payload |
|---|---|
| neighbors | `neighbors: [ NeighborRow, … ]` length ≤ NEIGHBORS_MAX — see below |
| ancestors | `ancestors: [ CODE, … ]` |
| descendants | `descendants: [ … ]` |
| blast_radius | `codes: [ … ]` |
| subgraph | `nodes: [ … ]`, `seeds: [ … ]`, optional `respects: [ … ]` |
| cluster | cluster card — see **Cluster payload** below |

## Neighbor row (schema 1.1)

Each element of `neighbors`:

```text
code: CODE
shared_paths: <int>          # |meaningful(OWNS_focus) ∩ meaningful(OWNS_code)| — ranking field
via: path | term | both      # exactly one
path_evidence:
  items: [ path, … ]         # shared meaningful paths, lex ascending, length ≤ PATH_EVIDENCE_MAX (5)
  truncated: <bool>          # true iff more shared meaningful paths exist than items
term_evidence:
  items: [ term, … ]         # matched seed terms for this feature; casefold-deduped;
                             # keep first original form; seed order; length ≤ TERM_EVIDENCE_MAX (5)
  truncated: <bool>          # true iff more matching seeds than items
via_traces:                  # always exactly these two kinds, in this order (Wave A)
  - kind: path_overlap
    items: [ path, … ]       # same list as path_evidence.items
    truncated: <bool>        # same as path_evidence.truncated
  - kind: term_match
    items: [ term, … ]       # same list as term_evidence.items
    truncated: <bool>        # same as term_evidence.truncated
```

**Consumers:** ignore unknown future `via_traces` kinds; continue to consume
`schema_version`, `shared_paths`, `via`, `path_evidence`, `term_evidence`,
`owns_coverage`, and the advisory banner.

## Cluster payload (schema 1.1)

Exactly one focus CODE. Reject zero or many focus values (note
`cluster_focus_invalid`); do **not** ship a global `communities()` partition.

```text
focus: CODE
members: [ MemberRow, … ]   # length ≤ CLUSTER_MEMBERS_MAX (8); focus first
members_truncated: <bool>    # true iff (1 + eligible_non_focus_count) > CLUSTER_MEMBERS_MAX
out_of_scope: [ OosItem, … ] # length ≤ OOS_ITEM_MAX (6); total display code points ≤ OOS_TEXT_CEILING (1200)
oos_truncated: <bool>         # true iff item cap or text ceiling dropped content
```

### Member row

```text
code: CODE
# focus row: code only (no path_evidence)
# non-focus row:
weight: <int>                # meaningful OVERLAPS |intersection| with focus (≥ CLUSTER_K)
path_evidence:
  items: [ path, … ]         # shared meaningful paths, lex ascending, ≤ PATH_EVIDENCE_MAX (5)
  truncated: <bool>          # true iff more shared meaningful paths than listed
```

### OOS item

```text
text: <string>               # first original display form seen (member order × bullet order)
sources: [ CODE, … ]         # attribution; CODE ascending
```

**Dedupe key (not emitted):** collapse whitespace + casefold of `text`. No LLM
similarity. Walk returned members in list order; first display form wins; later
members append to `sources`.

**Eligibility:** non-focus eligible iff weight ≥ `CLUSTER_K` (1). Rank non-focus
by weight desc, CODE asc; cap includes focus.

## Banner (always print to the user)

> Advisory — not a hard gate. OWNS coverage W/R means the neighborhood is only as
> complete as Files blocks; thin is not “no features exist.”

## Forbidden in the envelope

- `depends_on` / `DEPENDS_ON` edges
- Untyped `provenance` or `edge_extensions` bags
- P6 / work-graph adapter trace kinds in Wave A (`via_traces` only
  `path_overlap` and `term_match`)
- Claiming gate failure from empty or thin neighbors
