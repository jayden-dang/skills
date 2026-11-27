# TESTS.md — architect-system (formerly design-project)

## 2.0.0 — renamed, system architecture only, decides and does not record (2026-11-27)

**Ask (operator).** `design-project` and `define-project` read as the same skill. Make this one
the place the whole system's architecture is designed, part by part (structure, data,
communication, messaging, caching, principles), without changing code, and leave recording to
`define-project`. Operator rulings: a project-wide UI design system is out of scope and parked;
disposable probes in scratch stay; the name `design-architecture` was chosen first and changed to
`architect-system` on the routing evidence below.

**Roster:** Claude Haiku 5.5 and Claude Sonnet 5.5. GPT-6.2-sol, on the 1.0.0 roster, was not
run for this version. Replay: `python3 scripts/skill-tests/architect-system.py red|green` and
`python3 scripts/skill-tests/architect-system-routing.py red|green [reps]`. Runs are saved under
`.skills/architect-system/`.

### RED — 1.0.0 opened (cases 1-3) and define-project 1.4.0 opened (case 4)

Cases: **ledgerline** (caching; an incident file says a stale balance caused a double
withdrawal; the lead wants a 5-minute TTL on every read), **kettle-orders** (messaging; three
developers, one Postgres, duplicate emails, at-least-once webhooks, the CTO wants Kafka),
**fernway** (greenfield foundation; offline technicians), **settle-data** (the user asks
`define-project` to settle SQLite-per-module against one Postgres and add the invariant).

1.0.0 already compared options, kept production files untouched, rejected the blanket TTL and
Kafka, and bounded its evidence. Kept as is. What failed:

| Run | Observed | Became |
|---|---|---|
| Haiku ledgerline | Wrote `docs/adr/0001-no-cache-on-balance-reads.md` before the review while the note said "this plan does not edit them" | The opening rule: canonical records wait for approval; step 8 |
| Sonnet ledgerline | "Ownership boundaries hold? … observed by design and import check. Not enforced by tooling." No check proposed | Step 6: each rule gets an ID and a keeping check |
| Haiku kettle-orders | Eight "Rules every new feature follows", no check, no `ARCH-N`, no route to `define-project` | Step 6, step 8 |
| Haiku fernway | Twelve principles, one with a check; recorded "as ADRs in docs/adr using the define-domain process", not as `ARCH-N` | Step 6, step 8 |
| Haiku fernway | Principle 2: "Field writes are never lost and never rejected for being late." The founder was never asked; Sonnet listed the same policy as open | Step 2: the user's calls |
| Both fernway | Covered exactly the parts the prompt named. Haiku: backup and secrets 0 mentions, observability 1. Sonnet listed hosting, backup and auth as "not covered" | Step 3 and `parts.md`: a Parts table with every row |
| Both settle-data | `define-project` decided the open choice itself: Haiku recommended Postgres from the README, Sonnet started a `clarify-decisions` interview inside `define-project` | `define-project` 1.5.0 hands an open choice to `architect-system` |

Routing RED (full listing at `39c0f86`, 19 queries × Haiku + Sonnet): 33/38. Three design
requests went to `define-project` ("lay out how the code is structured, who owns which data…"
on both models, "decide which parts of its architecture we keep" on Haiku), one to
`clarify-decisions`, one to `root-cause`.

### GREEN — 2.0.0 and define-project 1.5.0

Scored from `git status` and by reading the Parts and invariant tables in all eight notes
(`green-syazq0ip`), not from the runs' own summaries.

| Check | Haiku | Sonnet |
|---|---|---|
| Seeded files, `docs/` and production code untouched (git status) | 4/4 | 4/4 |
| Parts table with a status on all 12 rows | 4/4 | 3/4 (settle-data: two rows "depends on choice") |
| Every proposed `ARCH-N` has a keeping check or review step | 4/4 | 4/4 |
| Ends with **Awaiting approval** and the list to record | 4/4 | 4/4 |
| Product policy listed as the user's call (fernway conflict rule, ledgerline rate staleness) | yes (C1, U1-U5) | yes (U1-U6, U1-U3) |
| settle-data: `define-project` hands the open choice to `architect-system` and writes no doc | yes | yes ("an open choice like this has to go through `architect-system`") |

Every run opened `parts.md` and `diagrams.md`. Haiku ledgerline proposed ARCH-3 "Account balances
are read from the `balance` table and never through the cache" with "CI `grep` that no file under
`accounts/` or `ledger/` imports `shared.cache`" as its check. Notes got longer (fernway 479 lines
against 316 on 1.0.0), mostly from the Parts and invariant tables. Headless runs cannot answer, so
every run wrote the note with provisional defaults and ended its reply with the user's calls as
questions. **Asking before writing, in an interactive session, is not yet measured.**

### REFACTOR — the second consumer

Advisor review found Haiku ledgerline 2.0.0 wrote "Next-change check, not run: … No second reader
exists yet, so this is open", the same failure 1.0.0 had countered with its list/detail example,
which the first 2.0.0 draft had condensed away along with three takeover red flags. Restored the
example and the flags, ported the 1.0.0 takeover case (`cairn-register`) into the harness, and reran
(`green-t9fwx6xw`). Takeover held on both models: Sonnet wrote "That makes two call sites in code,
not two proven live writers" and "A skipped restore and a passing local read are not release
evidence"; both started only the read-only detail reader. Haiku ledgerline still wrote "its check
needs an existing caller". The step now names that sentence ("No second caller exists yet" does
not skip this check) with a red flag. Rerun on Haiku (`green-gyyzg4o3`): ledgerline ran a scratch
product-detail reader ("returns `None` for an unknown product, and makes no extra partner call");
cairn ran `scratch/probe_next_change.py` against a copy of the fixture.

The `define-project` create-mode hand-off line was dropped: settle-data exercises update mode only.

### Routing

Own set, first description: 104/114 over three reps. Haiku sent caching and "split the monolith"
to `scan-architecture` (4) and answered a bare "architecture" (3). The description now leads with
the concrete words (Redis, Kafka, outbox, sync or async, tenant isolation), says "across every
feature (one feature's architecture is design-solution)" and "a refactor or tech-debt scan of
existing code".

**The name.** The skill was first named `design-architecture`. With that name, "design the
architecture for this feature" (expected `design-solution`; 10/10 at `39c0f86`) reached it on Haiku
in 9 of 10 reps. Editing the `design-solution` description did not help (4/4 still wrong; reverted).
The same listing with the name `architect-system` sent it to `design-solution` 8/10. The operator
chose the rename. Final text and name, two reps per model: own set Haiku 36/38 (both misses to
`scan-architecture`: "split this monolith" and "update docs/architecture/data.md"), Sonnet 38/38;
the 25 frozen-suite rows owned by neighboring skills Haiku 48/50 (one of the two misses is the
feature message above), Sonnet 50/50, against Haiku 49/50 and Sonnet 50/50 at `39c0f86` on the same
two reps. No design request reached `define-project` (3 did at `39c0f86`).

### Final text, all cases (`green-_fegn94g`)

Ten runs, both models, on the text as shipped (before the rename, which changed only the name):
seeded files, `docs/` and production code untouched 10/10; Parts table with all 12 rows 9/9 notes;
every proposed `ARCH-N` with a keeping check 9/9; **Awaiting approval** 9/9; a second consumer or
next change run in scratch or marked as interface evidence 9/9. Sonnet settle-data handed the
choice over and asked the user's call first, without writing a note. After the rename,
settle-data was rerun on both models (see `define-project` TESTS.md).

Owed: an interactive (not headless) run of asking before writing; the post-approval leg, where
`define-project` records an approved note; GPT-6.2-sol. Run directories are copied to the main
checkout under `.skills/architect-system/`.

Not run for this version: GPT-6.2-sol.

The 1.0.0 record below is kept. Its UI design-system findings (Tilbury Desk) are evidence for
behavior this version no longer covers; they wait for the parked UI design-system skill. Its
harness is `scripts/skill-tests/design-project.py` at commit `fa64751`.


## RED — Three entry cases (2026-11-27)

Nine fresh sessions ran before `SKILL.md` existed. Roster fixed up front: Claude
Haiku 5.5, Claude Sonnet 5.5, GPT-6.2-sol. Existing neighboring skills were available.
The tasks requested an actual local decision note and a review diagram, with
time, authority and sunk-work or availability pressure. All nine produced a
diagram and a defensible start/hold split. Preserve that result. The failures
below concern what the runs established and how another engineer could repeat it.

| Checkout | Exact words in RED | Observed gap |
|---|---|---|
| Alderslip, greenfield, Sonnet | “This meets the pilot's acceptance rule: one success and one sold-out result, including a retry after restart.” | The process/SQLite probe covered the store contract. It never sent a request through the proposed desk, and no report ran a second availability consumer. The desk and its failure feedback were still proposed. |
| Alderslip, greenfield, GPT-6.2-sol | “The desk UI, HTTP retry path, and full pilot rehearsal are still to be built and checked.” | Correct boundary on the probe. Later consumers were sketched but no second consumer exercised the proposed shared interface. Do not lose the evidence boundary to add reuse evidence. |
| Tilbury Desk, brownfield, Haiku | “Define the vocabulary once, after the sweep, so the widget and the queue use the same names.” | The note recommends a two-desk sweep based on the shipped check, with the shared direction and exception queue still untried. The baseline could not distinguish adopting a presentation contract from changing ownership of business states. |
| Tilbury Desk, brownfield, Sonnet | “The exception queue needs a pending state and a failure state. Those two tones already exist after step 2, so the queue can reuse them.” | Two scratch probes caught state regressions and verified the current consumers. The proposed exception queue remained an inference. |
| Cairn Register, takeover, Sonnet | “The replacement assumes a single writer, which the code contradicts.” | Two callable local entry points disprove the claimed topology of the checkout. Production activity and writer-process count are unknown. The same report recognized that no deployment manifest or production access was available, then overstated the conclusion. |
| Cairn Register, takeover, GPT-6.2-sol | “This demonstrates both local write entry points and persistence across process exits. It leaves live importer activity and overlapping writes unverified.” | Correct scope on local writes. The safe read-only change was proposed without a second reader consumer or a check that exercised list/detail sharing. |

The targeted additions are evidence for a second use, an explicit evidence
boundary for each diagram, and separate start/hold calls for work that can move
independently. The controls already knew to avoid unavailable payments, false
shipment completion and production cutover from a local sample.

## First GREEN — Findings and revisions (2026-11-27)

- The first Haiku takeover run reported “I put it there because the skill's
  default location for review notes is `.skills/`, not the root.” The user had
  named `delivery.md`. A later Haiku dispatch run repeated the location error
  after moving the fallback earlier in the skill. The final rule makes a
  filename alone checkout-relative and leaves location with the user.
- The first Haiku dispatch run executed the existing check, a contrast
  calculation and a probe of the rejected widget. It recommended a styling
  pass without trying the proposed shared primitive. A later run wrote
  “The exception queue screen does not exist yet, so there is no second
  consumer to test.” Both existing renderers were callable. The final recipe
  runs the selected alternative and uses an existing adopter or representative
  scratch inputs for the still-unbuilt consumer.
- Mermaid 11.17.2 rejected an unquoted `hold(request_id, crossing)` label in
  Haiku's architecture view and a semicolon in a Sonnet sequence message.
  The diagram recipe now identifies both syntax hazards and asks for a parse
  or rendered check when available.

## Description routing (2026-11-27)

18 first-message queries, 9 matches and 9 near misses, each routed twice
in fresh sessions with competing descriptions and models rotated. The first
wording led Haiku to choose `scan-architecture` for an inherited CLI/API and
`design-project` for an already-settled tokens document. Haiku also corrected
a name typo inside one answer. Mentioning the CLI/API takeover and the
ownership of settled standards made all 36 selections match the intended
first skill. Examples of expected boundaries are an approved design-tokens
entry (`define-project`), an invoice interaction draft (`draft-ui`),
and a pure refactor scan (`scan-architecture`). This exercised descriptions
in a competing list, not automatic installation in every host.

## Rechecked outcomes (2026-11-27)

| Case | Ready to start | Held | Evidence in the representative output |
|---|---|---|---|
| Alderslip, greenfield | Single-workstation desk with native controls, a SQLite hold path and shared availability feedback | Public booking and payments | The original demo still says held twice. The WSGI and SQLite scratch probe gave one 201 and one 409, replayed both outcomes in fresh processes, rolled back stock on a failed receipt write, and exercised the shared status in departures. |
| Tilbury Desk, missing design system | Adopt a shared, presentation-only status helper on invoice first | Unified Complete widget and broader rollout without carrier and accessibility checks | Both existing renderers and a local exception-queue input reused a scratch helper. Baseline and proposed local checks passed. The three negative probes against the mockup failed as expected. |
| Cairn Register, takeover | Local read-only receipt list and detail | Replacement deposit writer and production cutover | Both consumers used the same reader for the same fixture. Missing ID and unavailable storage were exercised. The bundled check explicitly skipped hosted restore. The diagram separates workbook claims, exercised SQLite calls and unknown production topology. |

The representative reports use Mermaid source. Chromium rendered all six
figures in those three reports. All 18 diagrams in the nine selected
model/case reports parsed with Mermaid 11.17.2. The selected reports come from
successive GREEN iterations and their targeted reruns. They provide scoped
local evidence from disposable fixtures. They do not establish hosted or
production readiness.

A Haiku follow-up in the same session identified its gap probe with a
hardcoded result as “not a test of a second consumer.” The targeted
brownfield rerun used the two callable renderers against the proposed
primitive without waiting for an exception-queue implementation. In the
takeover rerun, the second consumer reused the existing reader in scratch. A
greenfield Haiku attempt used a longer race probe and hit the harness
timeout. The brief now asks for the smallest causal inputs and a deadline
for concurrent or external probes. The targeted Haiku retry completed on
two concurrent connections and a separate read consumer. Its note kept a
whole-process or power-loss recovery check open.

Replay the behavior runs with
`python3 scripts/skill-tests/design-project.py red` and
`python3 scripts/skill-tests/design-project.py green`. Under
`.skills/design-project/` each saved run contains the report, its scratch
code and a transcript with the checks the model actually executed. Score
with the criteria in `eval.json`. The runner also checks that the requested
report exists and that the seeded files are unchanged.
