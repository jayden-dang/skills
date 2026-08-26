# Deterministic passes (rfeat-1.0)

## Contents

- [Constants](#constants)
- [On-disk layout](#on-disk-layout)
- [Pass order](#pass-order)
- [Classification rules](#classification-rules)
- [Checkpoint advance](#checkpoint-advance)

## Constants

```text
FINDINGS_MAX = 12
EVIDENCE_MAX = 8
SURFACE_ROOTS_MAX_PER_CARD = 3
PATH_STOPWORDS = apps, app, src, lib, internal, routes, features, crates, packages,
                 backend, frontend, web, server, client, test, tests, __tests__,
                 node_modules, target, dist, build, vendor, generated, gen
GENERATED_PATH_GLOBS = **/node_modules/**, **/target/**, **/dist/**, **/build/**,
                       **/*.lock, **/pnpm-lock.yaml, **/Cargo.lock, **/package-lock.json,
                       **/generated/**, **/*.pb.go, **/__generated__/**
```

## On-disk layout

Only this tree (consuming repo, gitignored `.skills/`):

```text
.skills/reverse-features/
  state.json              # last_reconciled_sha, recipe_id, unresolved_finding_ids
  active/<domain>.md      # compact pending/reopened OBS cards only
  observations/OBS-*.json # evidence detail for active rows
  tombstones.jsonl        # dismissed/absorbed signatures; lookup only — never load into context
```

`<domain>` slug: prefer the catalog domain id when surface roots match a domain
router row; else the first non-stopword path segment of the dominant evidence
locator, lowercase kebab, max 32 chars. Never use a proto-CODE or a full crate
path (`mail_labels_service` is acceptable only when it is that segment; prefer
`mail` / `labels` when a shorter domain token is already in the router).

If `.skills/` is missing, not writable, or not ignored, run **stateless**: print
the envelope, write nothing, set `checkpoint.advanced_to: null`.

Forbidden alternate roots (baseline failures): `.skills/reconcile/`,
`.skills/observations/` (bare), `.skills/_pending-*/`, any path under `docs/`.

## Pass order

1. **Resolve range.** Read `.skills/reverse-features/state.json` when present.
   - Valid checkpoint ancestor of `HEAD` → `base = last_reconciled_sha`.
   - Missing/stale/non-ancestor → `full` or `brownfield-bootstrap`; for a just-pulled
     range prefer `ORIG_HEAD` / reflog pre-pull tip when the caller is post-pull.
2. **Rename-aware path inventory** (read full output):

```bash
git diff --name-status -z -M <base>..<head>
```

3. **Drop generated/vendor/lockfile paths** via `GENERATED_PATH_GLOBS`. Remaining
   paths are candidates.
4. **Load catalog ownership.** From live `docs/specs/` (tracked or local overlay):
   - INDEX / shard feature cards → CODE, surface roots when present
   - each feature `tasks.md` `**Files:**` / `Files:` Create|Modify|Test path tokens
   - compute `owns_coverage` like load-subgraph (with_owns / registered)
5. **Load active overlay.** Parse `active/*.md` OBS cards; tombstone-lookup
   evidence signatures before inventing a duplicate OBS.
6. **Classify each candidate path** (rules below). Cluster paths that share a
   non-stopword path prefix into one finding when they share change_class.
7. **Render envelope** per `envelope.md`. Cap at `FINDINGS_MAX`.
8. **Index then advance** (see Checkpoint advance).

No Graphify read in rfeat-1.0. No LLM-only finding without a locator from pass 2.

## Classification rules

Apply first match:

1. Path under `GENERATED_PATH_GLOBS` after filter → ignore (not a finding).
2. Exact/ancestor match to a Recognized Files token or surface root →
   `known-impact` on that CODE (confidence high for exact/ancestor; medium if
   only a stopword-stripped segment matched more than one CODE → prefer
   `uncertain`).
3. New behavior-bearing surface (added non-generated source, route, migration,
   schema, permission, public API) with no Recognized owner →
   `new-capability-candidate` + new `OBS-<6hex>` unless tombstoned.
4. Docs-only, comment-only, or internal rename within an owned surface with no
   contract file → `no-spec-impact` (still record briefly when the caller asked
   about that range).
5. Else → `uncertain`.

Never promote OBS → Feature CODE in this skill. Never absorb into a CODE without
explicit human disposition in the calling session.

## Checkpoint advance

After findings for the range are **indexed** into `active/<domain>.md` (and
per-OBS json for new/pending candidates):

1. Write/update `state.json`:
   - `last_reconciled_sha = head`
   - `recipe_id = "rfeat-1.0"`
   - `unresolved_finding_ids = [ pending/reopened OBS ids… ]`
2. Set envelope `checkpoint.advanced_to` to that sha.

Unresolved OBS **stay** in active shards. Advance does **not** require human
disposition. Do not refuse to advance solely because findings are pending —
that was a baseline rationalization that re-scans forever.

Promoted/absorbed/dismissed: remove from `active/`, append tombstone, keep
detail json only if useful for audit — default delete active card.
