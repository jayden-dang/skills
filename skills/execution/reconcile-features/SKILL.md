---
name: reconcile-features
version: 1.2.0
description: >
  Use when external commits, a pull/merge, brownfield code, or a missing feature
  owner must be mapped onto the capability catalog (reverse tracking,
  changes-since-checkpoint, OBS overlay) — produces one advisory reconciliation
  envelope plus a local `.skills/reverse-features/` index. Not for writing
  requirements (specify-behavior), confirmed registry backfill (/map-features),
  docs-only ID audit (audit-trace), or ask-time neighbors (load-subgraph).
---

# Reconcile Features

Reverse track from git/code evidence onto the capability catalog (no specs/CI
writes; overlay only under `.skills/reverse-features/` when permitted). Sibling
of `load-subgraph` (horizontal neighbors) and `audit-trace` (vertical IDs): this
skill answers **what changed out there, and which Recognized features or
observations own it?**

## The Iron Law

```
NO FEATURE CODE MINT. NO SPECS WRITE. NO CONSUMING-REPO CI.
ONE OVERLAY ROOT. INDEX THEN ADVANCE. ENVELOPE.md IS THE SHAPE.
```

## What you produce

Print **exactly one** envelope shaped by `references/envelope.md`. When
`.skills/` is writable and ignored, index per `references/passes.md`.

## Procedure

1. Resolve the consuming repo root and mode per `references/passes.md` Pass 1
   (`changes-since-checkpoint`, `full`, or `brownfield-bootstrap`).
2. Load **`references/passes.md`** and run **every** pass in that file’s Pass
   order, including Pass 2. Do not substitute a remembered path list.
   Prefer the bundled runner when a mechanical inventory is enough:
   `scripts/reconcile.py --repo <root> --base <sha> --head <sha> --mode <mode>`
   (uses `scripts/owns.py` + `scripts/cluster.py`; prints the envelope; default
   `checkpoint.advanced_to: null` until overlay write is explicitly enabled).
3. Load **`references/envelope.md`** and print exactly one envelope in that
   shape (banner included). This run sets `disposition: pending` for new/reopened
   OBS and for unresolved findings — do not emit `absorbed` / `dismissed` /
   `attested-no-impact` here.
4. Index-then-advance **only** as `references/passes.md` § Checkpoint advance
   specifies, including the stateless `advanced_to: null` case.
5. Return the envelope to the caller. Unresolved `pending` findings must be
   surfaced before `frame-change` / `realign-spec` decisions on those surfaces.
   Name `/map-features` for confirm-then-write backfill; never auto-invoke it.

## Callers

| Skill | When |
|---|---|
| `frame-change` | After pull/merge or when INDEX may miss external work — before tier/requirements |
| `inspect-change` | Step 1b on the pinned review range |
| `realign-spec` | Optional pre-check: which CODEs the range actually touched |
| standalone | User asks to reverse-track, reconcile since checkpoint, or bootstrap OBS from code |

## Rationalization

| Thought | Reality |
|---|---|
| "Mint LABL — the crate is obviously that feature" | CODE only after human disposition via frame-change /map-features; this skill emits OBS ids |
| "Lead said sync specs to the code" | Code is evidence; Approved SHALLs need specify-behavior approval |
| "Add a CI drift workflow so teammates comply" | Zero-footprint: no consuming-repo automation |
| "Write `.skills/reconcile/` — close enough" | Only `.skills/reverse-features/`; other roots are recipe bugs |
| "Use OBS-LABL so promotion is obvious" | OBS id is `OBS-<6hex>` from evidence locators, never a proto-CODE |
| "Don't advance checkpoint while OBS pending" | Advance after active-shard index; pending stays queryable in active/ |
| "No specs dir — invent Approved requirements for the audit" | Brownfield bootstrap writes OBS only; configure-repo / frame-change come next |
| "GRAPH.md will help the PM browse" | No committed graph; catalog + local overlay only |
| "uncertain is basically no-spec-impact" | uncertain stays unresolved; never silent-clean |
| "Skip git diff — I already know the paths" | Pass 2 is mandatory; locators come from rename-aware inventory |
| "Paste the whole INDEX so ownership is obvious" | Catalog-query caps apply to the reply; Pass R may enumerate on disk |
| "I'll just invoke map-features and write the INDEX rows" | Name `/map-features` for the user; never auto-invoke |

## Red Flags

- Creating Feature CODE / INDEX rows / requirements from this skill
- Writing under any overlay root other than `.skills/reverse-features/`
- OBS ids shaped like Feature CODEs (`OBS-LABL`, `OBS-DRFT`, …)
- Refusing checkpoint advance solely because findings are pending
- Adding `.github/workflows/**`, git hooks, or tracked reconciler scripts to the target
- Writing `GRAPH.md` or treating Graphify as required (deferred in rfeat-1.0)
- Calling the range clean while any finding is `uncertain` or `pending`
- Auto-invoking `/map-features` or `/configure-repo`
- Skipping Pass 2 `git diff` or classifying from memory
- Pasting the full INDEX/catalog into the envelope or chat
- Printing a freeform note instead of the `references/envelope.md` envelope

## Done when

Exactly one `references/envelope.md` envelope is printed (advisory banner
included); every finding’s `change_class` follows `references/passes.md`
Classification rules; overlay written under `.skills/reverse-features/` **or**
stateless with `checkpoint.advanced_to: null`; unresolved `pending` rows are in
the envelope returned to the caller; `/map-features` named only, not invoked.
