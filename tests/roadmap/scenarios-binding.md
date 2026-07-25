# Scenarios — the `Roadmap item` binding column

Behavior coverage for `write-requirements` Step 1's binding write. Deterministic structure
is asserted by `tests/test_specs_index_binding.py`; these scenarios cover the judgment the
skill exercises at registration time. IDs are bare greppable tokens.

---

## S-BD-1 — Register a feature that implements a roadmap item

**Setup.** A repo with `docs/roadmap/INDEX.md` holding `ROAD-3 notes-search` under
`MILE-2`, and no spec yet for that item.

**Request.** Spec the work for `ROAD-3`.

**Expect.**
- A new row in `docs/specs/INDEX.md` whose **Roadmap item** cell reads `ROAD-3`. Covers
  RMAP-2.4.
- The `ROAD-N` is *cited*, never invented — the value matches an item already in the
  roadmap. Covers RMAP-2.4.
- `docs/roadmap/INDEX.md` is not modified by this step. Covers RMAP-2.4.

## S-BD-2 — Register with no roadmap layer present

**Setup.** A repo with no `docs/roadmap/INDEX.md`.

**Request.** Spec any new feature.

**Expect.**
- The row is registered with the **Roadmap item** cell reading `—`. Covers RMAP-2.5.
- Nothing else about registration changes, and no roadmap is created as a side effect.
  Covers RMAP-2.5.

## S-BD-3 — Registration ownership is unchanged

**Expect.**
- The feature code is still picked and registered in Step 1 of `write-requirements`, unique
  repo-wide, with the new row's status `Draft`. Covers RMAP-2.6.
- No other skill writes a cell in `docs/specs/INDEX.md` at registration time. `sync-spec`
  continues to own later `Status` realignment. Covers RMAP-2.6.

## S-BD-4 — Column position is not load-bearing

**Expect.**
- Consumers that read the registry — `brainstorm` step 1, the feature-overlap search,
  `sync-spec`, and `write-plan`'s status confirmation — read the `Status` cell semantically
  and keep working with the appended fifth column. Covers RMAP-2.6.
