# B14 — create-mode scan step: dispatch, inline fallback, failure→blocker; mode guards

Covers: `[PROJDOC-1.6]` `[PROJDOC-1.10]` `[PROJDOC-2.4]` `[PROJDOC-2.5]` `[PROJDOC-9.7]`
`[PROJDOC-9.8]` `[PROJDOC-9.9]` `[PROJDOC-9.10]` `[PROJDOC-9.11]`

**Scenario:** (fixtures described in-scenario, not committed as real repos, per B04's
convention)

- **(a) Brownfield fixture, scan-subagent capability available.** A repo with
  `src/app.py` beneath a detected `src/` root (satisfies the brownfield source
  predicate) and a live subagent-dispatch capability. Running `establish-project` in
  create mode: Step 1 detects brownfield, dispatches a scan subagent per
  `brownfield-scan.md`, and the digest `.skills/<slug>-scan.md` exists, complete,
  *before* Step 2's `grilling` interview begins. `[PROJDOC-1.6]`
- **(b) Greenfield fixture.** An empty repo (or one with only `README.md` and
  `.git/` — no regular file beneath any named or manifest-declared source root).
  Running `establish-project` in create mode: Step 1 detects greenfield, dispatches
  no scan, and proceeds straight to the Step 2 interview. `[PROJDOC-1.10]`
- **(c) No-subagent harness, same brownfield fixture as (a).** The predicate is
  satisfied but the running harness has no subagent-dispatch capability. Step 1
  still detects brownfield, and — per the inline-fallback sentence — runs the same
  `brownfield-scan.md` recipe by hand (not a different, lesser recipe), producing the
  same digest contract at `.skills/<slug>-scan.md` before Step 2. `[PROJDOC-9.7]`
- **(d) Failure-injection fixture.** Same brownfield fixture as (a), but the
  dispatched (or inline) scan errors out, times out, or the digest it produces is
  missing a required section/header field (an incomplete `.skills/<slug>-scan.md`).
  Step 1 reports the failure as a blocker `[PROJDOC-9.8]`; the create workflow stops
  before the Step 2 interview runs `[PROJDOC-9.9]`; the repo is NOT reclassified or
  treated as greenfield (Step 1 does not fall through to the greenfield branch)
  `[PROJDOC-9.10]`; no vision/spine/guidelines file or any other durable artifact is
  written from this run `[PROJDOC-9.11]`.
- **(e) Update run and validate run, same brownfield fixture as (a).** The layer
  already exists (`docs/product/vision.md`, `docs/architecture/INDEX.md` present).
  Running `establish-project` in update mode, and separately in validate mode, on
  this brownfield fixture: neither mode dispatches (or runs inline) the create-mode
  brownfield scan — Step 1 and `brownfield-scan.md` are never invoked outside create.
  `[PROJDOC-2.4]` `[PROJDOC-2.5]`

**Walk (verify):** — executed against the edited `SKILL.md` Create Step 1 / Update /
Validate sections:

- **(a)** Step 1's detect clause matches `src/app.py` under root `src/` against the
  source predicate → brownfield branch. The brownfield clause reads "dispatch a
  **scan subagent** per `brownfield-scan.md` (beside this file) ... writing
  `.skills/<slug>-scan.md` — before Step 2's interview begins." With subagent
  capability available, dispatch happens and the digest is complete before Step 2.
  Expected = observed. `[PROJDOC-1.6]` **PASS.**
- **(b)** Step 1's detect clause finds no file beneath any named/declared source root
  in the fixture → greenfield branch: "**Greenfield** — skip the scan, proceed
  straight to Step 2." No scan clause is reached; Step 2 runs next. Expected =
  observed. `[PROJDOC-1.10]` **PASS.**
- **(c)** Step 1's brownfield clause carries the parenthetical "(No subagents? Run
  the same scan inline under the `brownfield-scan.md` contract.)" — same fixture as
  (a), same predicate match, same target file and contract, only the dispatch
  mechanism differs (inline vs. subagent); the recipe itself is not restated or
  altered. Expected = observed. `[PROJDOC-9.7]` **PASS.**
- **(d)** Step 1's failure clause reads: "**Failure → blocker:** if the scan fails,
  times out, or cannot write a complete digest, report it as a blocker and STOP here
  — do not proceed to Step 2, do not classify the repo as greenfield, and write
  nothing durable." This is a single control-flow branch off the same Step 1 dispatch
  (not a separate gate elsewhere), so all four sub-checks are satisfied by one
  sentence: reported as blocker (`9.8`), STOP before Step 2 (`9.9`), no greenfield
  reclassification (`9.10` — the sentence is a third branch off detection, not a
  fallthrough to the greenfield branch), nothing durable written (`9.11` — STOP fires
  before Steps 3–6, which are the only steps that write durable files). Expected =
  observed. `[PROJDOC-9.8]` `[PROJDOC-9.9]` `[PROJDOC-9.10]` `[PROJDOC-9.11]` **PASS.**
- **(e)** The Update section's new guard bullet ("Update mode CONTINUES TO avoid
  dispatching the create-mode brownfield scan — Step 1 is create-only.") and the
  Validate section's new guard bullet ("Validate mode CONTINUES TO avoid dispatching
  the create-mode brownfield scan — Step 1 is create-only.") each state explicitly
  that Step 1 and its scan dispatch never run outside create mode, regardless of
  whether the repo is brownfield. Everything else in both sections is byte-identical
  to before this task (ARCH-2). Expected = observed. `[PROJDOC-2.4]` `[PROJDOC-2.5]`
  **PASS.**

**Result:** PASS — all 5 sub-scenarios verified by direct reading of the edited
`skills/project/establish-project/SKILL.md` Create Step 1, Update, and Validate
sections; all 9 requirement IDs covered.
