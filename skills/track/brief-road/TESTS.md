# brief-road — test evidence

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
