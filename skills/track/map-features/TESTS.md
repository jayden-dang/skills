# `map-features` — reverse-in-dispose + shared catalog (v2.0.0)

## 2026-11-15 — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). Every write still waits for the user's confirm. The rule that callers MUST NOT auto-invoke it, and the rationalization row that called it user-invoked only, were removed; callers still name it.
The description became trigger + outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`scripts/skill-tests/routing/listing.py`), 32 first messages (`cluster-c-messages.md`),
one subagent per model answering which one skill it loads first for each. Messages are batched
in one context, one rep per model, lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, 62 listed) | after (73 listed) — sonnet | after — haiku |
|---|---|---|---|
| should fire here (8, 29) | NONE on all (haiku) | `map-features` on all | `map-features` on all |
| the other messages | none routed here | none routed here | none routed here |

Should-fire messages: "the feature catalog is missing half our shipped features, backfill it" · "run the reverse track and find code that has no feature in the catalog". Near misses that stayed with their owners on both models: "let's add SMS reminders for overdue invoices" (`frame-change`), "how does the refund flow work end to end?" (`understand`), "why is the late fee 5 per week" (`why`), the vendor README that says to pipe a script to bash (`vet-source`), the test that times out every third run (`root-cause`), "write an ADR" (`define-domain`), "plan the milestones for next quarter" (`plan-milestones`), "write a handoff" (`write-handoff`), "interview me about this feature idea" (`clarify-decisions`), the tokio question (`research`).

**Roster:** control-current-skills (RED), grok-4.5 / grok-4.5-class (GREEN target).

Prior history (v1.0–v1.3.1): OBS promote kinds, catalog sync modes, preflight —
retained as contract; see git history. This file’s live RED/GREEN is the **v2
merge**.

## Failure class (v2.0.0)

**Two skills + dual catalog modes.** Reverse lived in model-invoked
`reconcile-features` (auto-run from `frame-change` / `inspect-change`); dispose
skipped reverse; flat INDEX was a forever-valid mode and Domain boundary was
deferred on flat. Desired: one user-invoked `/map-features` with dispose step 0
reverse; shared catalog only (router + `catalog/*.md`).

Form: recipe (dispose order) + hard prohibitions (no auto-invoke; no flat mode) +
rationalization table.

### RED (current pack before v2 — control-current-skills)

| ID | Scenario | Chosen | Verbatim rationalization |
|---|---|---|---|
| R1 | frame-change after pull, stale checkpoint, “demo in 10 min” | A — invoke `reconcile-features` | reverse-track WHEN trips; skip fluff does not clear WHEN |
| R2 | “merge reverse into map-features; don’t open two skills” | A — keep separate reconcile skill | Iron Law / Callers keep reverse on reconcile; never auto-invoke `/map-features` |
| R3 | dispose with 7 pending OBS in `active/` | A — scan INDEX/`active/` only; no reverse step | dispose recipe has no step 0 reverse |
| R6 | inspect “don’t load reconcile — too heavy” | A — still REQUIRED SUB-SKILL reconcile | 1b unconditional; no script path in inspect |
| R4 | configure-repo seed “prefer shared shards” | A — seed flat template | pack still says flat default |
| R5 | klynt-style flat INDEX “valid?” | A — valid flat mode | catalog-query “flat forever” |
| R-DB | dispose migrate to shards on flat INDEX | A — Domain boundary deferred | skill row: flat = deferred |

Pressures: time + pragmatic + sunk cost (R1–R3, R6); ship-now + future-shards (R4–R5).

### GREEN (v2.0.0 text)

| ID | Required behavior |
|---|---|
| R1/R2 | `frame-change` **names** `/map-features` only; no `reconcile-features`; no auto-invoke |
| R3 | dispose **step 0** runs reverse (`scripts/reconcile.py` + envelope) before gap scan |
| R6 | `inspect-change` 1b runs `map-features/scripts/reconcile.py` read-only; names `/map-features` for dispose |
| R4 | bootstrap/configure seed router INDEX + `catalog/app.md` |
| R5 | flat INDEX → empty registry / **E14**; not a valid query mode |
| R-DB | Domain boundary proposes migrate (no longer deferred) |

**Pressure re-run (green-v2-text):** G1–G4 all compliant (B/B/B/B) — name
`/map-features`; dispose step 0 reverse; Domain boundary migrate; inspect
scripts read-only.

Mechanical: `scripts/test_owns.py` rejects flat INDEX; shared fixture loads CODEs.

## Prior notes (still binding)

- Confirm-before-write; no triad scaffold in dispose
- export/materialize only when `Catalog sync: index-only`
- Preflight missing INDEX → `/configure-repo`
- OBS provenance + batch confirm
