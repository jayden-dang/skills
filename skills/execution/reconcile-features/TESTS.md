# `reconcile-features` — freeze reverse-track recipe (v1.0.0)

**Roster:** grok-4.6 (primary), grok-4.5 (weaker).
**Type:** technique / recipe (gate A/B/C/D controls all chose ethics-compliant A under AGENTS.md alone — those are not the failure this skill fixes).
**Scenarios:** `.skills/_pending-reconcile/red-rf-t{1,2,3}-*.md`.

## Failure class

**Complies on ethics, invents incompatible recipes.** Without a skill, both
models refuse to mint CODEs, write Approved SHALLs, or add consuming-repo CI —
AGENTS.md already carries those gates. They still diverge on durable shape:
overlay path, OBS id grammar, checkpoint advance, and envelope schema. A caller
cannot query a stable overlay; the next session cannot find what the last one
wrote.

Form: positive recipe / contract (envelope + on-disk layout + deterministic
passes) + hard prohibitions only for the remaining mint/CI/graph traps.

### RED (no skill)

| Scenario | Model | Shape verdict |
|---|---|---|
| T1 produce envelope | grok-4.6 | Overlay `.skills/reverse-features/` + `OBS-LABL` (proto-CODE id) + `state.json` advanced with unresolved findings |
| T1 produce envelope | grok-4.5 | Overlay `.skills/reconcile/` + `OBS-20260826-01` + freeform `disposition-*.md` — **different root and id grammar** |
| T2 frame after pull | grok-4.6 | `.skills/reverse-features/envelope.yaml`; also said **do not advance checkpoint past unresolved** — conflicts with locked advance-after-index policy |
| T2 frame after pull | grok-4.5 | `.skills/reconcile/disposition-<range>.md` — third spelling of the same artifact |
| T3 brownfield | grok-4.6 | Ad-hoc `.skills/_pending-rate-limit-auth-mail/observations.md` |
| T3 brownfield | grok-4.5 | Ad-hoc `.skills/observations/OBS-rate-limit-auth-mail.md` |

Verbatim shape failures:

- (4.5 T1) "Create `/tmp/mailgate-checkout/.skills/reconcile/checkpoint`" / "`disposition-c0c4e479..58104524.md`"
- (4.6 T2) "Do not advance the checkpoint past unresolved findings."
- (4.6 T3) "Write one read-only OBS candidate under `.skills/_pending-rate-limit-auth-mail/observations.md`"
- (4.5 T3) "`/tmp/opentickly-checkout/.skills/observations/OBS-rate-limit-auth-mail.md`"

Ethics held without the skill (not counted as RED wins for authoring): no CODE
mint, no `docs/specs/**` writes, no CI. Those stay in the skill as Red Flags so
a weaker future model cannot regress, but they are not the reason the skill
exists.

### Locked decisions feeding the recipe (2026-08-26)

1. Overlay root: `.skills/reverse-features/`
2. Checkpoint advances after findings are indexed into active overlay
3. Graphify adapter: deferred entirely for v1

### GREEN (v1.0.0 skill present)

Compliant = overlay root + schema/recipe ids + `OBS-<6hex>` + index-then-advance
+ no CODE/specs/CI.

| Scenario | Model | Choice / shape |
|---|---|---|
| T1 | grok-4.6 | `.skills/reverse-features/`; envelope 1 / rfeat-1.0; `OBS-5682de`; `advanced_to: 58104524`; no CODE/specs/CI |
| T1 | grok-4.5 | same `OBS-5682de` (identical locator hash); same root/schema/advance; `active/labels.md` |
| T2 | grok-4.6 | only `.skills/reverse-features/`; index then advance; no refuse-on-pending |
| T2 | grok-4.5 | same; NEXT_ARTIFACT points at reverse-features tree |

Meta (4.5 T1): hex rule + forbidden proto-CODE row made `OBS-LABL` unavailable;
index-then-advance row blocked the RED checkpoint refusal.

T3 not re-run in GREEN — ethics already held in RED; shape contract covered by T1/T2.

### Description trigger (v1.0.0)

10 queries × grok-4.5 / grok-4.6 — should-fire Q1–Q5 all `reconcile-features`;
should-not-fire Q6–Q10 → `audit-trace`, `load-subgraph`, `map-features`,
`realign-spec`, `root-cause` respectively. No misses either direction on this
held-out set.

## Edit — catalog-query ownership load (v1.1.0)

Pass 4 points at `catalog-query.md` for flat/sharded detect and context caps.
RED evidence for unbounded INDEX dump lives on `frame-change` v1.2.0 TESTS;
this bump keeps reconcile aligned with the same contract.

## Quality pass (v1.1.1) — author-skills wording sweep

Pointer-only procedure; disposition this-run = pending; envelope no-spec-impact
aligned to classification rule 4; rationalization/red-flag parity; Done when
checkable. No new behavior.

## Precision — OWNS extract + cluster (scripts/, post-1.1.1)

**RED command:**
`cd skills/execution/reconcile-features/scripts && python3 -m unittest test_owns.TestCluster.test_cluster_groups_by_two_meaningful_segments -v`

**RED output (verbatim shape):**
`AssertionError: 'enclave/src' not found in {'enclave/a.rs': [...], 'enclave/b.rs': [...], 'labels/x.ts': [...], 'labels/y.ts': [...]}`

**Root cause:** `cluster_unowned_paths` joined the first two `meaningful_segments`,
which after stopword strip were often `[domain, filename]` (`enclave` + `a.rs`).
`web` was also a PATH_STOPWORD, so `apps/web/.../labels/x.ts` collapsed to
`labels/x.ts` instead of `web/labels`.

**GREEN fix:** `cluster_key` strips the trailing filename, takes the first two
meaningful directory segments, or one meaningful + the next raw segment
(`crates/enclave/src/a.rs` → `enclave/src`). `web` removed from PATH_STOPWORDS
(monorepo package name). Shared `owns.py` stays index-first (CODE → spec dir from
INDEX; no `Feature code:` requirement) + fence-aware Files + File Structure.

**GREEN command (whole script suite):**
`cd skills/execution/reconcile-features/scripts && python3 -m unittest test_owns.py -v`
→ 7 tests OK.

**Mailgate dogfood** (`/Users/jayden/Developer/work/CommandOss/mailgate`,
`HEAD~12..HEAD` @ `705ac437`):

| Metric | Value |
|---|---|
| OWNS coverage | 4/25 (`AAEF`,`AGNT`,`ATCH`,`GIDS`); 20 INDEX dirs missing on disk; 1 dir no `tasks.md` |
| Window paths | 386 total; 276 owned; 110 unowned |
| Unowned clusters | 43 directory keys (e.g. `base/testkit`, `mail_labels_service/src`, `auth_service/oauth`) — no filename keys |
| Labels surface | `crates/mail_labels_service/src/service.rs` correctly unowned (`—`) → new-capability candidate |
| Catalog skew | `ATCH` Files lists `crates/enclave` → ancestor-owns most enclave paths (authoring breadth, not extractor miss) |

## Bundled runner — `scripts/reconcile.py` (v1.2.0)

**RED:** `ModuleNotFoundError: No module named 'reconcile'` from
`test_reconcile.py`; then
`test_new_capability_survives_cap_ahead_of_known_impact` failed when
CODE-tuple known-impact rows filled all 12 slots before OBS candidates.

**GREEN:** runner classifies + emits envelope; known-impact is one row per CODE;
cap priority is new-capability → uncertain → known-impact → no-spec-impact.

**Suite:** `python3 -m unittest test_owns.py test_reconcile.py -v` → 16 OK.

**Mailgate dogfood (same window, post-cap fix):** balanced envelope shows
~7 largest OBS clusters + 1 uncertain + 4 known-impact CODEs
(`ATCH`,`AGNT`,`AAEF`,`GIDS`); `findings_truncated: true`.
`crates/mail_labels_service/src/service.rs` is correctly **unowned** but
cluster-rank ~30/38 (singleton) so it falls outside the capped 12 — gold-label
corpus must assert it on the uncapped classify set / Critical-miss rule, not
only on the truncated envelope.

## Judgment corpus (v1.2.0)

Fixtures under `scripts/testdata/corpus/`:

| Case | Critical rule |
|---|---|
| `mailgate-labels` | `crates/mail_labels_service/src/service.rs` → `new-capability-candidate` with OBS id; never AGNT/ATCH; capped envelope still shows AGNT+ATCH known-impact; OBS id stable |
| `klynt-authz` | 0 OWNS snapshot → ≥1 new-capability; no proto-CODE OBS substrings |

**Command:** `python3 -m unittest test_corpus.py -v` → 3 OK.
**Full scripts suite:** `python3 -m unittest discover -v` in `scripts/` → 20 OK.

## Sharded INDEX (optional) — owns.py

**RED:** sharded fixture registered 0 CODEs / wrong `catalog/2026-…` path because
`str.lstrip("./")` ate `../` and Spec links lived outside cell 2.

**GREEN:** Domain-router detect + shard card parse; preserve `..` when resolving
spec dirs against the shard file. Fixture `testdata/specs-sharded/` → `SHRD`
owns `crates/mail/src/labels.rs`.

## Overlay index-then-advance (v1.3.0)

**RED:** `ModuleNotFoundError: overlay`; `reconcile_repo(..., write_overlay=True)`
left `checkpoint.advanced_to` null.

**GREEN:** `scripts/overlay.py` — `can_write_overlay` requires `.skills/` in
`.gitignore` + writable; `index_overlay` writes `state.json`, `active/<domain>.md`,
`observations/OBS-*.json`, skips tombstoned ids, still advances checkpoint.
CLI: `--write-overlay`.

## Precision ≥90 pass (v1.4.0) — breadth + novelty boost

**RED:** `crates/enclave` (2-seg, no trailing `/`) owned deep bootstrap paths as
ATCH; novel singleton `mail_labels_service` lost to larger bulk clusters under
`FINDINGS_MAX`.

**GREEN:**
- Ancestor OWNS only if token ends with `/` or has ≥3 segments
- Novel size-1 clusters (first meaningful segment absent from OWNS vocab) sort
  ahead of larger generic unowned clusters
- Corpus `must_appear_in_capped` for `crates/mail_labels_service/src/service.rs`

**Suite:** `python3 -m unittest discover -v` in `scripts/` → 27 OK.

**Mailgate re-dogfood:** `mail_labels_service` appears in capped envelope +
active overlay; ATCH hits drop from whole-enclave to attachment-specific paths;
known-impact still lists AGNT/AAEF/GIDS/ATCH.

## Cross-repo dogfood + INDEX Path column (v1.4.x)

**RED (klynt/bot):** Index Path cells used backticks / bare `docs/specs/…`
paths; parser took Name parentheticals (`(course and bootcamp)`) → OWNS 0/2
or 0/0.

**GREEN:** Prefer backtick / `docs/specs/` / dated-dir candidates over Name
`(prose)`; normalize to dirs relative to `docs/specs/`.

**Re-dogfood:**
| Repo | Window | OWNS | Envelope shape |
|---|---|---|---|
| klynt | HEAD~12 | **28/29** | 4 OBS + 8 known (AUTHZ/OFR/…) |
| bot | HEAD~8 | **1/1 SEAL** | known SEAL + uncertain + no-spec-impact |
| skills | HEAD~15 | 0/0 (no consumer INDEX) | pack-change OBS under `scripts` |
