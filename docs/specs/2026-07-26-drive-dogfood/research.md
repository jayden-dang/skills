# Research — an agent-driven dogfood runner

**Status:** **shipped inventory (0.2.2)** — skill bodies, plugin/marketplace,
guide, AGENTS/README counts, CHANGELOG, RED/GREEN baselines. Optional next:
live multi-model trigger routing; full triad if product-specced beyond skill ship.
**Ceremony tier:** **2 — Feature.** A new skill plus an edit to a shipped one
(`dogfood`), touching `plugin.json`, the guide docs, the README/AGENTS.md
inventory, and `tests/`. Multi-task work, full triad required.
**Decisions:** §7 closed 2026-07-26 (user path A: decide → then RED).

---

## 1. The gap

`dogfood` produces a guide **for a human to drive**. Nothing in the set drives
it. The three neighbours each cover a different axis:

| Skill | Who drives | Deliverable | Durable? |
|---|---|---|---|
| `dogfood` | a human, later | the checkable HTML guide | the guide persists; the run does not |
| `acceptance-ui` | Playwright, headless | committed, ID-tagged specs | yes — joins the verify suite |
| `acceptance-api` | curl/http | committed API tests | yes |
| **the gap** | **the agent, in a real browser, now** | **an evidence-backed run verdict per case** | **no — it is a run, not an asset** |

The requested skill is the fourth row: take a guide that already exists, execute
every case in a real browser, prove the backend agrees with the screen, fix what
breaks through `debug`, re-drive, and finish with every case accounted for.

It is not a duplicate of `acceptance-ui`. `acceptance-ui` writes assets; this
executes a checklist and self-heals. It is closest in shape to `execute-plan` —
a ledger-driven loop with a review gate and a circuit breaker — but over cases
instead of tasks.

## 2. Split justification

`writing-skills` permits a split in exactly two cases. Both apply:

1. **Genuinely distinct trigger.** "Make me a test guide" and "run the test guide
   I already have" are different observable states — a guide file exists or it
   does not. Either can be reached without the other.
2. **Hiding post-completion steps.** Folding the drive loop into `dogfood` puts
   forty browser interactions in front of the author while it is still scoping
   cases, which is exactly the pull `writing-skills` says a split should hide.

Verdict: a new skill, not a mode on `dogfood`.

## 3. Skill identity

**Name (recommended):** `drive-dogfood` — verb-first, kebab-case, carries the
literal keyword a user types (`dogfood`).

Alternatives considered: `run-dogfood` (collides with `/run`, which launches an
app), `execute-guide` (loses the `dogfood` keyword), `walk-cases` (coined, no
pretrained anchor). `drive` is the leading word already used across the
acceptance bucket ("drive the running system", "drive the app in a real
browser"), so it recruits an established prior.

**Bucket:** `skills/acceptance/drive-dogfood/`.
**Invocation:** model-invocable (no `disable-model-invocation`).

**Draft description** — trigger + outcome noun only, no workflow steps:

> Use when a dogfood test guide already exists and its cases must be executed
> rather than handed to a human — the agent-driven pass over every case in the
> guide against the running app in a real browser, judging both what the screen
> shows and what the backend actually stored. Produces an evidence-backed run
> ledger carrying a pass / fail / blocked verdict per case ID, and a guide left
> fully accounted for. Triggers on running or resuming a half-finished test
> guide, working a dogfood file end to end, or testing every case in the browser
> and fixing what breaks. Not for authoring the guide (`dogfood`) or writing
> committed e2e specs (`acceptance-ui`).

The outcome noun is *the run ledger with a per-case verdict*. Naming the
neighbours inline follows the precedent in `write-roadmap` and `amend`.

**Highest routing risk:** `dogfood` and `drive-dogfood` share a token, so the
description must be trigger-tested as a *pair* per `pressure-testing.md` — a
description earns its keep only when exactly one of a colliding pair fires. The
disambiguating predicate is observable and belongs in both descriptions: **does
a guide already exist?**

## 4. Predicted baseline failures → RED scenarios

These are **hypotheses, not findings.** Each must be confirmed by a control run
without the skill before a single line of skill text is written. If a control
complies, that row is deleted and nothing is written for it.

Roster: opus / sonnet / haiku. The bar is haiku.

| # | Predicted failure | Pressure stack for the RED scenario | Form that would fix it |
|---|---|---|---|
| F1 | Ticks a case on screen evidence alone; never checks that the server stored anything | time + volume (40 cases) + pragmatic ("the UI updated, that *is* the proof") | conditional on an observable predicate + a REQUIRED evidence slot in the ledger row |
| F2 | Spot-checks 3 representative cases, declares the remaining 37 "the same pattern" | exhaustion + economic (token cost) + social proof | positive recipe: the ledger row contract — no row, not run |
| F3 | On a failure, patches inline without `debug` and without a failing test first | time + sunk cost + authority ("just make it green") | hard prohibition + rationalization table (this is a gate: Iron Laws 2 and 3) |
| F4 | After a fix, re-drives only the failed case; never re-checks what the fix could regress | time + pragmatic ("the other cases already passed") | deterministic recipe over a named input — the changed files' requirement IDs |
| F5 | Loses the run to compaction; restarts at case 1 or claims completion from memory | context pressure | ledger-as-source-of-truth, mirroring `execute-plan`'s `progress.md` |
| F6 | Reports "all cases pass" with no per-case evidence | end-of-run exhaustion | REQUIRED slot + completion criterion (Iron Law 4) |
| F7 | Drives whatever tab is already open, against real or staging data | convenience | a precondition gate keyed to an observable (the target origin) |

F3 is the load-bearing one: the user's request ("nếu có lỗi, fix qua debug rồi
test lại") is precisely an invitation to bypass Gates 2 and 3 under time
pressure. That scenario gets the full three-pressure stack plus authority.

**Non-gate axis.** F1/F2/F4/F5/F6 are recipe/shape failures, not compliance
failures, so per `pressure-testing.md` they are tested with technique scenarios —
a fresh agent, an *unseen* guide, does the output take the right shape — not
pressure runs. Only F3 and F7 need pressure scenarios.

## 5. Proposed body — the load-bearing rules

Sketch only; the final text is written *after* RED, against the recorded
transcripts, and only for the failures that actually occurred.

### 5.1 The Iron Law candidate

```
NO CASE IS TICKED ON THE SCREEN ALONE
```

Paired evidence, gated on an observable predicate rather than an exemption
clause:

- The case's **Expect** touches state the server owns → the ledger row carries
  **both** the front-end observation **and** a server-side probe, or the case is
  not ticked.
- The case is purely presentational (layout, color, copy, empty state) → the
  front-end observation is the whole evidence, and the row records
  `backend: none — presentational`.

Probe ladder, strongest first: the request/response the UI actually made
(network read) → a read-back through the app's own API → a direct store peek
(DB / file / cache) → reload or restart to prove durability. A red console error
or a 5xx on the wire fails the case even when the screen looks right.

### 5.2 The ledger contract (recipe, addresses F2/F5/F6)

`.skills/<slug>-dogfood-run.md`, one row per case ID from the guide, written
**before** the case is driven, updated as it resolves:

| field | content |
|---|---|
| `case` | the guide's stable case ID |
| `req` | the requirement ID the case exercises |
| `verdict` | `pending` \| `pass` \| `fail` \| `blocked` |
| `saw` | what was actually on screen — quoted, not paraphrased |
| `server` | the probe run and its result, or `none — presentational` |
| `notes` | fix attempts, the `debug` hand-off, the re-drive |

The ledger is the source of truth across compaction; on re-entry, read it and
resume at the first non-`pass` row. A todo is created per case so the loop is
visible to the user (the `acceptance-check` convention).

### 5.3 Failure routing (addresses F3/F4)

Triage before any fix — re-drive the failed case once from a clean state and
classify by an observable, the shape `acceptance-ui` already proves:

- **Deterministic failure on a real Expect** → product defect. `REQUIRED
  SUB-SKILL: use debug`. Hand it a red-capable loop, not a click sequence: the
  captured request/response, the console output, and the minimal steps, so
  `debug` Phase 1 has something to build from.
- **Non-deterministic, or the guide is wrong** (a stale label, a missing
  precondition, a case that assumes seed data) → defect in the *guide*. Fix the
  guide, re-drive. Never route a guide bug to `debug`.
- **Precondition failure** (login broken, server down, seed missing) → shared
  dependency: stop the run. Everything downstream is untested, not passing.

After `debug` reports fixed: restart the app, re-drive the failed case from a
clean state, **and** re-drive every already-`pass` case whose requirement ID
appears in the fix's changed files. That sweep is the deterministic answer to
F4 — a named pass over a named input, not "consider re-checking".

**Circuit breaker:** a case still failing after 3 distinct fixes stops the whole
run and escalates, matching Gate 3 and `execute-plan`'s breaker.

### 5.4 Safety preconditions (addresses F7)

Confirm the target origin is the local dev app before the first click; a
non-local origin stops the run pending explicit user consent. Drive in a
dedicated tab, never a tab the user is working in. Avoid any control that raises
a native `alert`/`confirm` — a modal dialog freezes the browser bridge and kills
the run; where a case requires one, warn the user first.

### 5.5 Browser driver

Default to the Chrome extension tools when present (real session, real
extensions, real cookies — the point of the exercise). Fall back to a headed
Playwright/Chromium session when they are not, so the skill degrades in a
consuming repo rather than dead-ending. Do **not** hard-depend on the
`claude-in-chrome` skill: it ships outside this package.

## 6. The `dogfood` upgrade

`dogfood` already produces everything the driver needs — for a human. Four
REQUIRED slots in its existing artifact contract make the same guide machine
drivable at no cost to the human reader (all four are invisible `data-*`
attributes or a file path):

1. `data-case="CASE-N"` — a **stable case ID** per row. Today a row is
   identified only by its prose; a driver needs a key to write a verdict against
   and to resume on.
2. `data-req="CODE-N.M"` — the requirement ID as an attribute, not only as
   rendered text, so the regression sweep in §5.3 can be a `grep`, not a parse.
3. `data-backend="…"` — **the server-side assertion for this case**, or the
   literal `presentational`. This is the genuinely new authoring work, and the
   most valuable: it forces the guide's author to say what the server should
   have stored, which today the guide never states. It improves the human guide
   too — a human dogfooder also cannot verify persistence from the screen.
4. `data-setup="…"` — the precondition or reset that lets the case be driven
   **independently**, so a case can be re-driven after a fix without replaying
   the whole guide. Ordered guides are fine for humans and fatal for a resumable
   loop.

Plus one contract change: **always write the page to a file** (a known path)
before publishing it with the Artifact tool. Today the file is only the fallback
when artifact tooling is absent; a driver needs a path to read.

Form check: this is `writing-skills`'s "omits an element from something it
already produces" row → **REQUIRED slots in the template it already fills in**,
not prose reminders near the contract.

**This edit needs its own RED.** "It's a tiny edit" is the second row of the
`writing-skills` rationalization table — baseline the current `dogfood` against a
scenario that needs a machine-readable guide and record what it omits.

## 7. Decisions closed (2026-07-26)

User chose path A: close decisions first, then RED. Decisions below are
**binding for the skill body** once RED confirms the related failures.

### D1 — Where "done" is marked

**Decision: (a) ledger authoritative + (c) run-report at the end.**

| Role | Artifact |
|---|---|
| Source of truth during the run | `.skills/<slug>-dogfood-run.md` (verdict per case) |
| Session glanceable progress | one todo per case, marked done when the ledger row is `pass` |
| End-of-run handoff | regenerate or append a run report (statuses + `saw`/`server` evidence baked in) next to the guide path |

**(b) ticking the guide HTML checkbox** is a **nicety only** while the guide tab
is open — never authoritative, never required for a case to count as done.
Rationale: localStorage is per-browser and a mis-click corrupts the human
record; the ledger survives compaction and is greppable.

### D2 — Fix-in-place vs batch

**Decision: fix-in-place, with hard caps.**

- On a deterministic product failure: stop that case → `debug` → re-drive failed
  case + regression sweep (§5.3) → continue the ledger.
- Precondition failure (server/login/seed): **stop the whole run** (unchanged).
- **Per-case circuit breaker:** 3 distinct fix attempts on the same case → stop
  and escalate (Gate 3 / `execute-plan` precedent).
- **Per-run cap:** 5 distinct product-defect fix cycles across the whole run.
  Hitting the cap stops the run with a partial ledger — remaining cases stay
  `pending` / `blocked`, never silently `pass`. Rationale: one cascading bug
  must not turn a dogfood pass into an unbounded debug session.

### D3 — Durable asset after the run

**Decision: the run itself is not durable; failures leave durable assets.**

- Passing cases: evidence lives in the run ledger / end report only. They do
  **not** auto-promote to Playwright/API specs (that is `acceptance-ui` /
  `acceptance-api` territory).
- Failing product cases fixed via `debug`: the regression test `debug` already
  requires under TDD **is** the durable asset. The skill must not invent a
  second promotion path.
- Optional later (out of v1 scope): user may explicitly ask to promote a green
  case into a committed e2e — that is a hand-off *to* `acceptance-ui`, not a
  silent side effect of `drive-dogfood`.

## 8. Ship checklist for this repo

Beyond the `writing-skills` deployment checklist:

- [x] `skills/acceptance/drive-dogfood/SKILL.md` (≤300 lines preferred)
- [x] `dogfood/SKILL.md` edited with the four REQUIRED slots + the file-path rule
- [x] `.claude-plugin/plugin.json` — add `./skills/acceptance/drive-dogfood`
- [x] `docs/guide/skills/drive-dogfood.md` + `See also` links added to
      `dogfood.md`, `acceptance-ui.md`, `acceptance-check.md`
- [x] `docs/guide/skills/README.md` index row
- [x] `AGENTS.md` §11 — acceptance row + skill count (→ **47**; header matched)
- [x] `README.md` inventory
- [x] `CHANGELOG.md` (0.2.2)
- [x] `tests/drive-dogfood/red-baselines.md` + `scenarios-*.md`
- [x] `tests/trigger/drive-dogfood-routing.md` — query set for the colliding triple
      (live multi-model routing still outstanding)

## 9. RED outcome → GREEN scope (2026-07-26)

Full transcripts: `tests/drive-dogfood/red-baselines.md`. Model: **grok-4.5**
only (multi-model roster not available on this harness).

| Prediction | Observed | GREEN action |
|---|---|---|
| F1 screen-only tick | **RED 2/2** | Iron Law + REQUIRED `saw`/`server` slots; counter *"dogfood = screen only"* |
| F2 spot-check | **RED 1/2** (variance) | Ledger recipe binds full set; counter *"same pattern"* |
| F3 skip debug | **COMPLY 2/2** | Thin `REQUIRED SUB-SKILL: use debug` only — no Gate-2/3 clone |
| F4 no regression sweep | **COMPLY** | One-liner named-input recipe |
| F5 bad resume | **COMPLY** | One-liner ledger resume |
| F6 empty completion | **COMPLY** | Fold into F1 evidence slots |
| F7 staging / partial | **RED on hard reframe (C)** | Origin + consent gate; counter *"whatever is fastest"* |
| dogfood machine slots | **RED** slots 1–4 missing | REQUIRED `data-case/req/backend/setup` |

### Next

- [x] Research + skill identity + proposed body sketch
- [x] Open decisions closed (§7)
- [x] RED control runs + dogfood-upgrade RED
- [x] GREEN skill text for RED rows (+ D1–D3 recipe contracts)
- [x] GREEN re-run P-F7 + T-F1 + T-F2 + dogfood slots (grok-4.5 hold)
- [x] Ship checklist (§8): plugin, marketplace, guide docs, AGENTS/README counts, CHANGELOG, trigger query set
- [ ] Optional: live multi-model description routing; multi-model GREEN; full triad if product-specced
