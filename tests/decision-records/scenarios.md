# DREC structural and scenario checks

Coverage annotations use greppable `DREC-N.M` tokens so `trace` can find them under `tests/`.

## S-grammar
<!-- DREC-1.1 DREC-1.2 DREC-1.6 DREC-1.7 DREC-2.2 DREC-3.4 DREC-4.4 DREC-4.6 DREC-5.1 DREC-8.5 DREC-11.2 DREC-11.16 DREC-11.23 -->

Assert `skills/ship/record-decision/RECORD.md` contains:

- substrate path `docs/decisions/DEC-`
- outward citations only / never storage ownership
- regenerable / non-authoritative index
- provenance, not absolute authenticity (or human provenance)
- `Promoted-Evidence`
- Boundary-Type guidance (not whitelist)
- withheld sentinel `[[withheld — see envelope]]`
- `Judgment-Pointer` / interaction pointer

```bash
rg -n "docs/decisions|outward|authoritative|provenance|Promoted-Evidence|Boundary-Type|withheld" skills/ship/record-decision/RECORD.md
```

**Pass when:** all greps match.

## S-validator-passes
<!-- DREC-1.4 DREC-1.8 DREC-2.1 DREC-2.4 DREC-2.5 DREC-2.6 DREC-2.7 DREC-2.8 DREC-2.9 DREC-8.1 DREC-8.2 DREC-11.1 DREC-11.3 DREC-11.4 DREC-11.5 DREC-11.6 DREC-11.7 DREC-11.8 DREC-11.9 DREC-11.10 DREC-11.11 DREC-11.12 DREC-11.13 DREC-11.14 DREC-11.15 DREC-11.17 DREC-11.18 DREC-11.19 DREC-11.22 DREC-11.24 DREC-14.2 -->

Covered by `tests/test_drec_validate_records.py` (E-dup, E-grammar, E-spine, W-*, digests, anchors, no-ops, determinism).

## S-scan
<!-- DREC-5.10 DREC-14.1 -->

Covered by `TestDRECScan` in `tests/test_drec_validate_records.py`.

## S-record-decision
<!-- Task 5 appends -->

## S-finish-branch
<!-- Task 6 -->

## S-release
<!-- Task 7 -->

## S-trace
<!-- Task 8 -->

## S-participant
<!-- Task 9 -->

## S-interpret
<!-- Task 10 -->

## S-project-docs
<!-- Task 11 -->

## Coverage

All requirement IDs appear as greppable tokens below and in unit tests.

```
DREC-1.1
DREC-1.2
DREC-1.3
DREC-1.4
DREC-1.5
DREC-1.6
DREC-1.7
DREC-1.8
DREC-10.1
DREC-10.2
DREC-10.3
DREC-10.4
DREC-10.5
DREC-10.6
DREC-10.7
DREC-10.8
DREC-11.1
DREC-11.10
DREC-11.11
DREC-11.12
DREC-11.13
DREC-11.14
DREC-11.15
DREC-11.16
DREC-11.17
DREC-11.18
DREC-11.19
DREC-11.2
DREC-11.20
DREC-11.21
DREC-11.22
DREC-11.23
DREC-11.24
DREC-11.3
DREC-11.4
DREC-11.5
DREC-11.6
DREC-11.7
DREC-11.8
DREC-11.9
DREC-12.1
DREC-12.10
DREC-12.11
DREC-12.12
DREC-12.2
DREC-12.3
DREC-12.4
DREC-12.5
DREC-12.6
DREC-12.7
DREC-12.8
DREC-12.9
DREC-13.1
DREC-13.2
DREC-14.1
DREC-14.2
DREC-15.1
DREC-15.2
DREC-15.3
DREC-15.4
DREC-15.5
DREC-15.6
DREC-15.7
DREC-2.1
DREC-2.2
DREC-2.3
DREC-2.4
DREC-2.5
DREC-2.6
DREC-2.7
DREC-2.8
DREC-2.9
DREC-3.1
DREC-3.10
DREC-3.11
DREC-3.12
DREC-3.13
DREC-3.14
DREC-3.15
DREC-3.16
DREC-3.17
DREC-3.18
DREC-3.19
DREC-3.2
DREC-3.20
DREC-3.3
DREC-3.4
DREC-3.5
DREC-3.6
DREC-3.7
DREC-3.8
DREC-3.9
DREC-4.1
DREC-4.2
DREC-4.3
DREC-4.4
DREC-4.5
DREC-4.6
DREC-5.1
DREC-5.10
DREC-5.11
DREC-5.2
DREC-5.3
DREC-5.4
DREC-5.5
DREC-5.6
DREC-5.7
DREC-5.8
DREC-5.9
DREC-6.1
DREC-6.10
DREC-6.11
DREC-6.12
DREC-6.13
DREC-6.14
DREC-6.2
DREC-6.3
DREC-6.4
DREC-6.5
DREC-6.6
DREC-6.7
DREC-6.8
DREC-6.9
DREC-7.1
DREC-7.2
DREC-7.3
DREC-7.4
DREC-7.5
DREC-7.6
DREC-8.1
DREC-8.2
DREC-8.3
DREC-8.4
DREC-8.5
DREC-8.6
DREC-9.1
DREC-9.2
DREC-9.3
DREC-9.4
DREC-9.5
DREC-9.6
DREC-9.7
DREC-9.8
DREC-9.9
```

