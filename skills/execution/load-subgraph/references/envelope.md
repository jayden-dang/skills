# Result envelope

## Required fields (every run)

```text
advisory: true
owns_coverage:
  with_owns: <int>      # CODEs with non-empty OWNS after P1
  registered: <int>     # INDEX registry size
  ratio: <float>        # with_owns / registered (0 if registered=0)
p0:
  matched: <int>
  returned: <int>
  truncated: <bool>
notes: []               # non-fatal parse skips only
```

Plus exactly one query payload:

| Query | Payload |
|---|---|
| neighbors | `neighbors: [ { code, shared_paths, via: path\|term\|both }, … ]` length ≤ NEIGHBORS_MAX |
| ancestors | `ancestors: [ CODE, … ]` |
| descendants | `descendants: [ … ]` |
| blast_radius | `codes: [ … ]` |
| subgraph | `nodes: [ … ]`, `seeds: [ … ]`, optional `respects: [ … ]` |

## Banner (always print to the user)

> Advisory — not a hard gate. OWNS coverage W/R means the neighborhood is only as
> complete as Files blocks; thin is not “no features exist.”

## Forbidden in the envelope

- `depends_on` / `DEPENDS_ON` edges
- Claiming gate failure from empty or thin neighbors
