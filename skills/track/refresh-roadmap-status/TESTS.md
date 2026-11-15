# TESTS.md — refresh-roadmap-status

## 2026-11-15 — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). This skill is read-only and never
took its consent from being typed, so the body is unchanged. The description became trigger +
outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`.skills/fixtures/routing/listing.py`), 22 first messages (`cluster-a-messages.md`), one
subagent per model answering which one skill it loads first for each. Messages are batched in one
context, one rep per model, which is lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, 48 listed) — s | before — h | after (52 listed) — s | after — h |
|---|---|---|---|---|
| should fire here (3, 12; held out 19) | NONE on all | NONE, or `craft-page` for the dashboard asks | `refresh-roadmap-status` on all | `refresh-roadmap-status` on all |
| the other 9 near-miss messages | none routed here | none | none routed here | none |

Should-fire messages: where are we on the roadmap, and what should we pick up next? · which milestone are we in right now? · how far along is the plan overall, are we still on track for the second milestone?. Near misses that stayed with their owners: "what is ROAD-81 and can
we start it?" (`brief-road`), "move sharing ahead of search on the roadmap" and "put ROAD-12 on
hold" (`plan-milestones`), "review the billing branch before I merge it" (`inspect-change`),
"tell my manager in two lines what we shipped this week" (`speak-outer`), "build me a status page
for our public API uptime" (`craft-page` or none).

## 2026-10-14 — R11 covers S8 (1.1.0 → 1.2.0)

Template sync from plan-milestones 1.2.0: the roadmap gained the `After:` item-order
field and structural rule `S8` (a dangling or self `After:` target, or a cycle).
`R11` now names `S8`, so this check withholds its next action on a cyclic or
dangling `After:`. RED/GREEN evidence for the field itself is in plan-milestones'
TESTS.md (2026-10-14); nothing in this skill's own text changed except the rule
range `S1`–`S8`.

## 2026-10-19 — Notion drafts pass (1.2.0 → 1.3.0), plan T3c

Roster: haiku and sonnet, headless (`skill-fixtures/run-headless.sh` with `FIXTURE_MCP`).
`mcp/fake-mcp.py` serves Notion and Linear with the hosted tool names, and
`scenarios/notion-world.py` seeds two Notion workspaces. `notion-saltgrass`
(Saltgrass Marina) holds `Harbor Ledger / Roadmap drafts`, which is this repo's, and
`Harbor Portal / Roadmap drafts`, which is Thu's. `notion-klynt` (Klynt Labs) holds
`Ledger / Roadmap drafts`. Linear has teams `LED` and `POR`. The fixture is `harbor-ledger`
with overlays `roadmap-draft` and `notion-linear`, plus `notion-bound` (the binding a
baseline setup wrote) or `notion-bound2` (the template's fields). Scored by
`scenarios/notion-score.py` from the server state files and `mcp-calls.jsonl`, never from
the reply. Full record: `docs/design/2026-10-19-notion-draft-surface.md`.

**RED (1.2.0), variant `inreview`.** MILE-2 is `In review`. Quang's comment on the page
says: "Drop that phrase or split refunds out, then I'll sign." The prompt asks which drafts
are waiting on Quang and whether anything is holding them up.
- **Unbound repo:** 0/2 runs opened Notion at all.
- **Bound repo:** 6/7 runs fetched the table and never read a comment. The 7 are the
  baseline binding 1/3 and the template binding 0/4. Verbatim (haiku): "Not in the repo.
  … The only thing holding it is Quang's review."

**GREEN (1.3.0).** Pass 7 runs only when Draft surface is `notion`. It fetches the data
source, reads `notion-get-comments` on every row not yet signed off, and writes one `draft`
line per row with the sign-off role's newest comment quoted verbatim.

| | haiku | sonnet |
|---|---|---|
| `notion-get-comments` on MILE-2 | 3/3 | 1/1 |
| Quang's comment quoted | 3/3 | 1/1 |
| Harbor Portal's `In review` row reported | 0/3 | 0/1 |

## 1.3.1 — template copy follows plan-milestones 1.7.0 (2026-11-05)

The roadmap template copy drops the table's Outcome column. Table order, which S4 reads, is unchanged.

---

# Merged from `brief-road` — now `brief.md` beside this skill

## 2026-10-23 — 1.0.0

Asked for (2026-10-23): a small user-invoked skill to understand one roadmap item before
`frame-change`, because a real roadmap grows past a person's reading budget. Fixture: the
real klynt repo, read-only (`docs/roadmap/INDEX.md`: 890 lines, ~50 milestones, 200 ROAD
entries, median 157 words, longest 755). Model roster: **Sonnet only** (standing
directive), the `skill-tester` agent, fresh context per run, no nested agents. Criteria
and per-item ground truth were written before each round
(`.skills/road-brief/baseline-criteria.md`; run notes in `.skills/road-brief/runs/`).

Prompt for RED, terse and realistic: *"Trước khi frame-change, giúp tôi hiểu ROAD-N trong
roadmap: nó là gì, giải quyết gì, liên quan tới những gì."* ("Before frame-change, help me
understand ROAD-N: what it is, what it solves, what it relates to.") GREEN prompt: the
slash command `/brief-road ROAD-N` with SKILL.md loaded.

### RED — no skill (A) and `understand` 1.0.0 (B)

Items: ROAD-81 (582 words, unbuilt, restated twice; truth: blocked only by ROAD-44, the
eight members above it all Implemented) and ROAD-170 (97 words, unframed; truth: behind
ROAD-49/50/169, none bound).

| Criterion | A-81 | A-170 | B-81 | B-170 |
|---|---|---|---|---|
| S1 plain opener (who can do what) | no | partial | partial | yes |
| S3 exclusions with destination | yes | yes | yes | yes |
| **S4 readiness verdict from predecessor status** | no | no | no | no |
| S5 binding stated | partial | partial | partial | partial |
| **S6 existing code at file:line** | n/a | no | n/a | no |
| **S7 decided vs open** | partial | partial | no | no |
| **S8 terms defined** | no | no | no | no |
| S10 one check question | no | no | yes | yes |
| S11 nothing written | yes | yes | yes | yes |

Verbatim: A-81, after listing ROAD-80 → … → ROAD-44 → ROAD-81, *"Tôi chưa kiểm tra trạng
thái đó"* ("I have not checked that status"), about ROAD-44. A-81 ran to ~900 words, a
near-verbatim reformat of the entry, opening *"mục thứ 10 trong 11 mục"* ("item 10 of
11"). B-170: *"Tôi cũng chưa mở các consumer của `currentRow`"* ("I did not open the
`currentRow` consumers") though the entry requires that audit. Both B runs skipped
`understand`'s page: "a roadmap item is a document, not a code path through 3+ files".

Supplementary RED, A-179 (an Implemented item, CBUILD): found the catalog row and the spec,
and routed further work to `amend-feature` — **Built detection is a no-op**, so the skill
carries only a verdict row for it, no branch.

Form, per the failure table: S4 is a check that must never be misjudged → fixed `grep`
passes with a rule on their output (the verdict table). S1/S6/S7/S8 are omissions from a
brief the agent already writes → REQUIRED slots in a fixed order.

### GREEN round 1 — draft

| | G-81 | G-170 | G-139 (holdout) |
|---|---|---|---|
| S4 verdict matches truth | yes — Blocked by ROAD-44, 9 rows | yes — Blocked by 49/50/169 | yes — Ready (136/137/138 Implemented) |
| S7 decided / open | **no** — "nothing recorded"; entry cites ADR-0031, ADR-0006 | yes — K16/C1/S2, U5b/C4 | yes — lock 5 with file:line |
| S6 / S8 / S10 | yes | yes | yes |
| ≤40 lines | **no** (~65: Scope now copied five groups of acceptance criteria) | no (~55) | no (~45) |

Fixes: ADRs the entry cites are decisions (pass 5, slot 6); Scope now capped at five
one-line deliverables, never their acceptance criteria.

### GREEN round 2

G2-81: ADR-0031/0006/0032 under Decided; Scope now five bullets plus dated history. Still
~50 lines, ten of them slot 5's rows → the cap excludes slot 5's rows.
G2-170: **regression** — "Decided: nothing recorded". The entry cites no `.skills/` path and
the item has no CODE; round 1 had found `.skills/CCOL/decisions.md` by inference.
`grep -rlE 'ROAD-170\b' .skills/` returns `CCOL/roadmap-proposal.md`, the frame-change
that inserted it → added to pass 5 with that case as its counter. ROAD-170 is now named in
the skill text, so it stops being a test; ROAD-172 replaces it.

### GREEN round 3 — holdout ROAD-172

Blocked by ROAD-49/50/169/170/171 (truth); Decided C13 (`decisions.md:68`) and K19 (`:31`)
reached through the new grep; Open U10b (`:146`) and U11b (`:147`); code at
`CourseBrowserList.tsx:50` and `FolderTree.tsx:130-131`, spot-checked. One misread: K19's
"closes" column taken as its state.

### No-op sweep

Deleted, each with a 4/4 RED pass behind it: the read-only sentence and its red flag (no
run wrote a file), the "choosing which item is `/board`" line (no run ranked items), and
the Links pass (every run found the neighbours unaided). Kept: the stop path for a missing
or retired item (house rule), slot 3 (the output contract must list every slot), the
In-flight verdict row (the table must be total).

### Final text — holdout ROAD-44

Run on the swept text. Ready (truth): all eight members above it Implemented, one row
each. The `.skills/` grep returned 12+ files (research notes, GRADER); the brief kept the
two that hold locks about ROAD-44 — `CAPGW/decisions.md:107`, `PUBL/decisions.md` — and
reported `.skills/_pending-road127/close.md`, which the entry cites, as absent. Code today:
`capability_wiring.rs:153` (`IndeterminatePublicationStateReader`), `capability.rs:80,182`,
spot-checked. Scope now five bullets plus a dated history line; exclusions with owners
(MILE-32, MILE-17, ROAD-98, ROAD-157).

### Remaining branches (same day, asked for by the user)

Truth written before each run (`baseline-criteria.md`, "Remaining-branch round").

| Run | Model | Item | Result |
|---|---|---|---|
| R1 | Sonnet | ROAD-72, struck as *delivered* | **fail** — headline "đã bị loại bỏ" ("removed") above a quote saying delivered. The skill's own words ("say it is retired") put it there |
| R1b | Sonnet | ROAD-73, struck as delivered | pass — "đã giao (delivered), không phải bị bỏ", quoted, stopped |
| R1b | Sonnet | ROAD-69, struck as absorbed by ROAD-52 | pass — "bỏ (retired)", quoted, pointed at `/brief-road ROAD-52` |
| R2 | Sonnet | bot ROAD-4 — no `docs/specs/catalog/`, Roadmap-item column mid-row | pass — Ready, ROAD-3 = SEAL Implemented; ARCH-17 (`INDEX.md:96`) cited |
| R3 | Sonnet | copy of bot, ROAD-12 given `After: MILE-2` | pass — Blocked by ROAD-4/5/6/7, ROAD-11 (above it in MILE-4) correctly not a predecessor; flagged `After: MILE-2` against the milestone's `Depends-on: MILE-3` as open |
| R4 | Haiku | ROAD-172 | partial — verdict, K19/C13, U10b/U11b right; called `apps/library/` absent (it is `frontend/src/apps/library/`) and never opened the course browser |
| R4b | Haiku | ROAD-172 | partial — no false "absent"; course browser still unresolved, because it searched the path, not the words |
| R4c | Haiku | ROAD-214 holdout — Surfaces in words only, `After: ROAD-179` | pass — Ready (CBUILD Implemented); reached `course_build_service/slot_step.rs:223` and `evals/widget_selection/` (eval set: new); CPLAN lock 15 at `decisions.md:302`, spot-checked |

Fixes: the stop path says delivered or dropped from the reason (R1 → R1b); pass 5 searches
before calling a Surface absent — a non-resolving path by `find -path`, a Surface named in
words by its nouns as a `find -iname` pattern, build output excluded (R4 → R4b → R4c).
ROAD-72 and ROAD-172 are named in the skill text after these fixes, so neither is a clean
test any more.

Roster after this round: Sonnet and Haiku.

### Verdict rows not yet run, and length

| Run | Model | Item | Result |
|---|---|---|---|
| R5 | Sonnet | ROAD-177 (CREV, In-progress) | pass — "In flight as CREV (In-progress)"; ~55 lines |
| R6 | Sonnet | ROAD-179 (CBUILD, Implemented) | pass — "Built as CBUILD"; ~52 lines |

No run on the final text had met the 40-line target: briefs ran 45–55 lines, swollen in
slots 3, 4, 6 and 7. The overall cap became per-slot limits (≤5 exclusions, ≤6 terms, ≤5
locks + the file holding the rest, ≤5 open questions, ≤5 code bullets), the form that had
already worked for Scope now.

| R5b | Sonnet | ROAD-177 | every slot within its limit; ~48 lines; `config.rs:16,85` spot-checked |
| R4d | Haiku | ROAD-214 | every slot within its limit; Ready; but cited `self-check.tsx:37` copied from a decision's text — line 37 is `useTranslation()` |

Fix: the red flag for unopened paths now covers every `file:line` in the brief.
| R4e | Haiku | ROAD-214 | pass — every `file:line` cited is one it opened or grepped (`slot_step.rs:223`, `requirements.md:173` CBUILD-3.5, spot-checked); every slot within its limit; Ready |

## 2026-11-03 — 1.1.0: model-invoked

Asked for by the operator, so that `/shape --auto` can check a road's readiness. Fixture: a generated marina
CLI repo with this set installed under `.claude/skills/`.

**RED.** `/shape #4 --auto` with no readiness step, Sonnet 1. `ROAD-4`'s `After: ROAD-3` is `In-progress` in the
catalog. The conductor opened a worktree, wrote "ROAD-4 follows ROAD-3" as a Lock and started two sessions.
It never looked up ROAD-3.

**Trigger test.** `claude -p --model claude-sonnet-5-5 --max-turns 1`, 16 queries, 2 reps each.
Should fire: 16/16 called `brief-road` ("What is ROAD-4?", "can we start ROAD-4 yet", "is ROAD-4 blocked?",
"ROAD-4 ready to frame?", "what's left out of ROAD-4", "what does road 4 actually deliver", a plain "explain"
request, and one query in another language).
Should not fire: 0/16. "let's build ROAD-4" went to `frame-change`; "drop it", "add a roadmap item" and "reorder the
milestones" went to `plan-milestones`; "write the requirements" to `specify-behavior`; "how does quay list work"
and "where does the whole roadmap stand" read the repo directly, and "explain how bookings are stored" to `understand` or the repo.

Not covered: the body is unchanged, so the 1.0.0 brief evidence stands for Sonnet and Haiku. The trigger test ran on Sonnet only.

## 1.2.0 — "Ready" is not ready for an unattended run (2026-11-05)

RED, 1.1.0, Sonnet: asked "Can ROAD-4 go through /shape --auto --go tonight? Nobody will be at the keyboard", on a road that is a slug and
Surfaces only: "Short answer: yes, ROAD-4 is ready to go through `/shape --auto --go` tonight." GREEN, 1.2.0, Sonnet and Haiku: both
answered no, gave the card row as missing, and said the card decides an unattended run.

---

# Merged from `chart-progress` — now `chart.md` beside this skill

## 2026-11-15 — model-invocable (description routing)

`disable-model-invocation` removed on the owner's word (2026-11-15: agents start skills on their
own; approving, answering and merging stay with the operator). This skill is read-only and never
took its consent from being typed, so the body is unchanged. The description became trigger +
outcome with its neighbours named.

Routing check: the full listing of model-invocable skills as a session sees it
(`.skills/fixtures/routing/listing.py`), 22 first messages (`cluster-a-messages.md`), one
subagent per model answering which one skill it loads first for each. Messages are batched in one
context, one rep per model, which is lighter than `pressure-testing.md`'s fresh context per query.

| | before (flagged, 48 listed) — s | before — h | after (52 listed) — s | after — h |
|---|---|---|---|---|
| should fire here (4, 14; held out 20) | NONE on all | NONE, or `craft-page` for the dashboard asks | `chart-progress` on all | `chart-progress` on all |
| the other 9 near-miss messages | none routed here | none | none routed here | none |

Should-fire messages: make this week's progress dashboard · generate the weekly progress page with the roadmap graph · I want the usual Friday chart for the team. Near misses that stayed with their owners: "what is ROAD-81 and can
we start it?" (`brief-road`), "move sharing ahead of search on the roadmap" and "put ROAD-12 on
hold" (`plan-milestones`), "review the billing branch before I merge it" (`inspect-change`),
"tell my manager in two lines what we shipped this week" (`speak-outer`), "build me a status page
for our public API uptime" (`craft-page` or none).

## 2026-10-14 — 1.0.0

Roster: Sonnet (`skill-tester`), as the user named. Fixture: a clone of the klynt repo at
`1be5268ad` (dev) with its `.skills/**/*.md` ephemera, `--today 2026-10-14`. Same prompt in
every run: "Generate my weekly dashboard: one self-contained HTML file … what got done in the
last week and the last month, what is in progress, the roadmap as a dependency graph with what
can run in parallel next week and what's ready to start now, each catalog domain, and the
architecture", then report the numbers and how each was derived.

### RED — no skill, 2 runs

| | run 1 | run 2 |
|---|---|---|
| finished, 7 days | 7 | 14 |
| finished, 30 days | 30 | 30 |
| in progress | AWID, AWKIND, CCOL | AWID, AWKIND, CCOL |
| ready to start | 30 items | 16 items |
| time / tokens | 6.6 min / 137k | 6.9 min / 146k |

Both wrote a generator of their own (run 2: `/tmp/dashgen/gen.py` plus four helpers, left
outside the repo). Verbatim:

- run 1, ready: "This is my own rule, not a roadmap field … I hand-applied a few readings from
  Blockers text: 110 waits on MILE-39, 74 waits on 72 and 73, 73 is independent, and 190 can
  start now."
- run 1, dates: re-dated a catch-up commit's features "from the merge-to-dev date …
  ASSET's date is approximate".
- run 2, ready: "The item-level Needs come from parsing prose, so they are heuristic."
- run 2, dates: "A first attempt with `--first-parent` was wrong … so I dropped it."

Failure class: a check that must not vary run to run → a recipe of deterministic primitives
(`scripts/extract.py`, `scripts/render.py`) plus one Iron Law: the agent never re-derives a
number. Counters carry the recorded 7-vs-14 and 30-vs-16.

Taken from the baselines into the extractor, because both runs were right to look:
the catch-up batch (`88ad16e50` moved 11 features to Implemented on 10-10; run 1 and run 2 both
caught it) → flagged as a batch, not re-dated; 13 milestones with every member done but not
Closed (run 2) → `graph.closable`; MILE-27 table Planned vs block Closed (run 2) → `S7`
finding; six duplicate ADR numbers (run 2) → `ADR` finding; the 7-day window as 7 calendar
days including today (both runs).

### GREEN — skill installed at `.claude/skills/chart-progress/`, 2 runs

Both runs: 15 finished in 7 days (11 flagged as batch `88ad16e50`), 31 in 30 days, in
progress CCOL / AWID / AWKIND, the same 21 ready items, the same 13 closable milestones; no
generator of their own; nothing written outside `.skills/dashboard/`; every ID in the notes
present in the snapshot. Both stated the `After:` coverage (0 of 181) in the summary and
recommended the backfill. 37 s / 42k and 30 s / 44k tokens.

Found by diffing the two runs' artifacts, not by their reports:

- the snapshots differed in byte order — `graph.unlocks` was built by iterating a `set`, so
  key order followed `PYTHONHASHSEED`. Fixed; covered by a three-process byte-equality test
  (render has the same test, after `hash()` in SVG ids failed it).
- run 2 recommended "AWID has 0 of 31 tasks recorded complete": AWID has no ledger, and the
  page printed `0/31`. The cell now reads "31 tasks, no ledger".

### Scripts

`scripts/test_extract.py` and `scripts/test_render.py` (unittest, stdlib only), each test
watched failing first. Run: `cd scripts && python3 -m unittest`.

## 2026-10-14 — 1.1.0: a page for a person

**RED — user review of 1.0.0.** "It is still more machine-readable than human-readable." On the
klynt page: IDs and kebab-case slugs led every row (`ROAD-107 · ai-quota-campaigns · MILE-26`),
states were internal words (`unspecced`, `specced`, `framing`), the critical path was a string
of IDs, overlaps were a list of raw paths, dates were ISO. The notes from both 1.0.0 GREEN runs
— the first paragraph on the page — carried snapshot vocabulary verbatim: "coverage.with_after
is 0", "are in graph.closable", "frontend/src/widgets/assistant/", "S7".

Failure class: wrong shape → a positive recipe. The page (render.py) became a weekly briefing:
names first with the ID as a small tag, plain states from one `STATE` table, human dates
("Sat 10 Oct"), finished work grouped by day, an 8-week trend, build age, ready items grouped
under their milestone's name and outcome, overlaps as "Shares code with <name> (<state>) —
<area>", finished milestones left off the map. Each property has a render test, watched
failing first (8 failed on 1.0.0). The readability tests caught a real bug the old page hid:
feature names parsed as `[spec]` (the spec column, not the name column).

The notes section became a recipe with one worked example from an unrelated project (not
klynt, so the GREEN fixture could not be copied from it).

**GREEN — 2 runs on klynt.** Both notes files: zero field names, paths, rule codes, hashes or
bare IDs (`grep` over the written files); features, items and milestones named the way the
page names them; the missing-`After:` caveat in plain words naming plan-milestones. One loose
claim survived in run 1 ("three assistant features" while one of the three is a Library
feature) — prose accuracy, not vocabulary; not addressed.

## 2026-10-30 — lanes, delivery proof, migration slot (1.1.0 → 1.2.0)

Source: the klynt frame-change on roadmap Focus and parallel lanes. klynt maintained its
parallel lanes by hand in `docs/specs/INDEX.md`; that table was refreshed 5 times in 6 days
and carried dated status columns.

**Code, test-first.** `test_delivery.py` (17) and `test_lanes.py` (7) were written first and
watched fail: `KeyError: 'integration'`, `'focus'`, `'slots'`, and `'done' != 'in-review'`.
The render test failed on `KeyError: 'in-review'`. The fixture squash-merges PRs onto `dev`,
like klynt does: 3/3 recent klynt PR heads are not ancestors of `origin/dev`, and PR #279 has
7 commits but its integration commit has 1 parent. Suite: 68 tests green.

**klynt measurement** (origin/dev d48c1aa89, proof switched on in a scratch run only). Of 99
Implemented or Shipped CODEs, 13 have exactly one candidate integration commit naming them, 42
have several, and 44 have none. Turning `Delivery proof: required` on before backfill would put
nearly every item in review. That is why the switch is opt-in, and why candidates are proposed
in `delivery_candidates`, never written.

**SKILL text, shape check.** 1.1.0 never mentions `lanes.md`, so no run on it can produce the
file; that is the baseline. GREEN on 1.2.0 (sonnet 1, haiku 1) ran `/chart-progress` on an
`academy` fixture with a Focus slot and no git remote. Both runs wrote `docs/roadmap/lanes.md`
with `Source: origin/dev@<sha>` and dropped `--issues` after `gh` failed, so the file reads
"Tracker read: not read". Neither run hand-edited the file, and both notes named BUILD as in
review and blocking Desktop foundation. One haiku run left a stray `gh.err` in
`.skills/dashboard/`, which is inside the allowed directory and was not countered.

Not covered: a run with real tracker issues (only unit-tested through `claims_from_issues`),
and the leaf-level overlap rule. Shared-path detection is unchanged.

## 2026-10-30 — an item amended by several features (1.2.0 → 1.2.1)

Found while backfilling klynt. ROAD-219 was delivered by changing both CPLAN and CBUILD: each
tasks.md carries a `## ROAD-219 amendment` group. The extractor kept only the first host
(`setdefault`), so ROAD-219 read as done from CPLAN's group whatever CBUILD's said. The shared
`roadmap-findings.md` R6 also called two `amends` lists naming one item an error. That rule
was added during authoring; the owner's decision D never stated it.

Test-first: `test_an_item_amended_by_two_features_waits_for_every_group` (PLAN's group ticked
and delivered, BUILD's with an open box) failed with `'done' != 'building'`. Now every host's
group must exist (else specced), any open box means building, and done needs every group
delivered (else in-review). R6 now judges primary binds only. 69 tests green. klynt after the
backfill (`ROAD-127 amends ROAD-219`, `ROAD-179 amends ROAD-219, ROAD-220`): ROAD-219 and
ROAD-220 read done instead of ready.

## 1.3.0 — the lean milestone table (2026-11-05)

`extract.py` reads a four-column table (`| ID | Milestone | Depends-on | Commitment |`) and takes each outcome from the
block's `**Outcome:**` line; a five-column table reads as before. Unit test: the same roadmap in both forms parses to
identical milestones and items. 24 extract tests pass.

## 1.4.0 — the snapshot and the lanes file come from refresh-lanes (2026-11-13)

`extract.py` and `lanes.py` moved to the model-invocable `refresh-lanes`, so the skills that
write a roadmap-moving record can regenerate `lanes.md` themselves; a model-invoked skill
may not invoke this one or reach into its folder. Behavior-preserving move: 70 tests green
before and after; state labels now travel in the snapshot. `test_render.py` imports the
extractor from the sibling folder in this repo. Evidence: `skills/track/refresh-lanes/TESTS.md`.
