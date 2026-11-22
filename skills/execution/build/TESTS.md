# TESTS.md — build

## v1.2.0: every dispatch takes its model and effort from `model-routing.md` (2026-11-22, Sonnet + Haiku + Codex `gpt-6.2-sol`)

Scenario: a wave controller with five tasks (a migration, a 7-file refactor, a one-file rename, a browser
page checked from screenshots, a webhook signature check), then the whole-branch review and acceptance.
Asked for each dispatch's model and effort, and whether it asks the operator.

**RED, the Cheap / Mid / Top tiers.**
- Sonnet controller: `opus` for the T2 implementer, the T2 and T5 reviewers, the whole-branch review and the
  fixer, five dispatches above itself. "I would not ask for any of these." No effort passed.
- Codex controller, `gpt-6.2-sol` medium: `gpt-6.2-astra` high for the T5 implementer, its reviewer and the
  whole-branch review, "the model guidance specifies no separate approval gate for choosing a tier above the
  controller". Acceptance ran on `gpt-6.2-sol`.

**GREEN, `model-routing.md`.**
- Sonnet and Haiku: 0 `opus`; T3 `haiku` low; the migration and signature reviews plus the whole-branch
  review `sonnet` high; nothing asked; "Opus here would be a raise, so I would not use it unasked."
- Codex: 0 `gpt-6.2-astra`; T3 `gpt-6-luna` low; acceptance `gpt-6.1-terra` medium; both values passed on
  every dispatch.

The BLOCKED row's "ceiling → stronger model" now needs the operator's word, the same rule.

**Rerun with the real `Agent` tool (effort, `subagent_type`, no `model`), Sonnet and Haiku.** The first
Launching row said `Agent` takes a model and no effort, the reverse of this harness. With the row fixed,
both passed `effort` and chose the model through `subagent_type` (`reviewer-sonnet`, `worker-haiku`), 0 Opus,
nothing asked.

Not covered: a real build dispatching on these rows; the raise list reaching a PR's decision section.


## v1.1.0: Close step 4 tells acceptance that a product walk is queued (2026-11-17)

The hand-off in step 4 now tells `validate-feature` whenever step 4b's predicate holds, so it
leaves the browser to the walk. The evidence is in `validate-feature`'s TESTS.md, v1.5.0:
- RED: 2 of 2 drove the UI before the walk.
- GREEN: 2 of 2 skipped it.
- Reverse case: a standalone run still drove the UI.

**Full close, steps 4 and 4b, with no hand-off line in the prompt.** The build session was told
only to run steps 4 and 4b of `common.md`, on harbourline `VARIANT=ui` with build, validate-feature,
write-dogfood and run-dogfood installed. Scored on the ledger line, on `validate-feature.md`, and on
`dogfood status`.
- Sonnet: step 4 wrote "UI: the product walk drives it next" itself and skipped `ui.md`. Step 4b
  then wrote an 11-case guide, reviewed it in context, and drove it in `agent-browser`: 11 pass.
- Haiku: step 4 skipped the UI the same way, but step 4b stopped at `run-dogfood`'s review gate.
  The harness has no subagent tool, and the classifier refused the self-written review. So no
  case got a verdict and nothing drove `/book`. That is the failure the skip opens.

**Fallback, added to 4b.** When the walk stops before any case in its run file has a verdict,
run `validate-feature` again on the UI items, telling it no walk follows, before step 5. Haiku
was re-run on a fresh fixture. The walk stopped at the same gate, and the run then drove `/book`
in `agent-browser` and quoted every result in `validate-feature.md`: "Booked B-1: 2 seat(s),
24k VND", "Could not book: only 0 seats left", and persistence after a restart.

**Not covered.**
- A real `/go` in which the build controller has subagents. There, the review gate would normally
  open, so this harness overstates how often the walk stalls.
- `go.md` and the receipt's own accounting of a walk that stopped.

## 2026-11-15 — absorbed build-in-waves, build-by-story, build-inline, execute-common as mode file(s)

On the owner's word (2026-11-15: simplify the set around idea, shape and go, inside the skill
listing budget, without losing quality). Moved whole, not rewritten: build-in-waves → `waves.md`; build-by-story → `story.md`; build-inline → `inline.md`; execute-common → `common.md`.
`SKILL.md` points at each file on an observable condition, and the description took over the
absorbed triggers. The absorbed skills' own records are appended at the end of this file.

Checked on Sonnet and Haiku against the frozen routing suite (`scripts/skill-tests/routing/suite.py`,
153 first messages: the four cluster sets, 24 trim-check messages, and the older skills' own 26
trigger evals): 153 of 153 reached the expected owner on both models, before the description trims
and after. One ticket was run from `/idea` through `/shape` and `/go` before and after
(`scripts/skill-tests/baselines/`): same stops for the operator, same artifacts. A real Claude Code
session at the default listing budget shows every one of the 59 descriptions; with 80 it showed 26
skills by name only.

Not covered: each mode file was not re-run on its own scenario. The absorbed skills' contract
evals, which cited headings of a `SKILL.md` that no longer exists, were dropped.

## 2026-11-15 — 1.0.0 (one skill, three mode files)

`build-in-waves`, `build-by-story`, `build-inline` and `execute-common` became one skill on the
owner's word (2026-11-15). Their bodies moved whole into `waves.md`, `story.md`, `inline.md` and
`common.md`; only the names by which they refer to each other changed. The evidence for this
move is the end-to-end run recorded at the bottom of this section. The four skills' own records
follow below, unedited.

**The router is new text, so it was run.** Four small repos, each holding only this skill and an
approved `docs/specs/pay/tasks.md`; the operator writes "The PAY plan … is approved. Build it." and
the run stops at the router's Done-when. Haiku, one run each (2026-11-15):

| `Execution-mode:` line | Session can dispatch subagents | File opened |
|---|---|---|
| `continuous` | yes | `waves.md` |
| `story-unit` | yes | `story.md` |
| `continuous` | no | `inline.md` ("the first row applies … it overrides whatever `Execution-mode:` line is in tasks.md") |
| none | yes | `waves.md` |

The first draft of the table listed the wave row first, which left `story-unit` with no subagents
ambiguous; the rows are now checked in order, inline first. Not run: `waves.md` and `story.md`
end to end after the move. The test agents cannot dispatch subagents, so every end-to-end run
here went through `inline.md` and `common.md`.

---

# Merged from `build-in-waves` — now `waves.md` beside this skill

## Verify tiers (v2.2.0, 2026-10-03)

RED/GREEN for this change is recorded once, in `skills/execution/test-first/TESTS.md`
§ Verify tiers — Sonnet, 4 RED + 4 GREEN runs on a paper Rust workspace (implementer and
controller scenarios). This file's part: lane worktrees reused across ready sets, wave gate after a
parallel merge. Both are shape-only so far: the fixture's shared test database made both
controllers serialize.


## Length pass — cross-file duplication with execute-common (v2.1.2, 2026-09-07)

**Goal:** SKILL.md was 211 lines (87 atoms, 2.4 lines/atom — densest file in the
set). Bring it to ≤195 without losing behavior. `execute-common` and
`task-lifecycle.md` (both REQUIRED SUB-SKILL loads from this file) already own
several of the rules this file restated; those restatements were the only
slack in an otherwise wall-to-wall rule file.

**Before / after:** 211 → 192 lines (87 → 71 atoms). No new sibling file was
created — everything removed had a surviving home either in this same file's
own Gate section or in `execute-common`/`task-lifecycle.md`, which this file
already loads as REQUIRED SUB-SKILL for exactly these steps.

**Moved:** nothing — no conditional block qualified for extraction; every
removal below is either a no-op deletion or a duplicate with a named
surviving home.

**Deleted as duplicates (surviving home confirmed by grep):**

| Removed from `SKILL.md` | Surviving home |
|---|---|
| `**Not this skill:**` table (both rows) | story-unit row → `## Mode ownership` table + Thought/Reality row + Red Flags; inline row → `## Inline route` section + Red Flags |
| Reviewer-Prompt Hygiene: "Never pre-judge findings (...)" | Red Flags: "Tell a reviewer what not to flag, or pre-rate severity in the dispatch" (same file, Gate — kept) |
| Durable Progress: "On start, read `.skills/<CODE>/progress.md`; resume after the last complete task." | `execute-common/SKILL.md` § Ledger check: "Read `.skills/<CODE>/progress.md` if it exists. Every task ... it marks complete IS complete — resume at the first item it does not list." |
| Durable Progress: "Never re-dispatch a task the ledger marks complete." | Red Flags: "Re-dispatch a task the ledger marks complete" (same file, Gate — kept) |
| Red Flags: "Skip the tracker-sync, occupancy, or workspace preflight" | `execute-common/SKILL.md` Red flags — never, identical line |
| Red Flags: "Invent a tracker or ticket set when config is absent or the user declined sync" | `execute-common/SKILL.md` Red flags — never: "Invent a tracker or ticket set when config is absent or the user declined" |
| Red Flags: "Use `HEAD~1` as a review base" | `execute-common/task-lifecycle.md` step 4: "Never use `HEAD~1` as base." |
| Red Flags: "Dispatch the first task before the todo list exists (tasks **and** Close branch)" | `execute-common/SKILL.md` Red flags — never, identical line |
| Red Flags: "Skip the close sequence, silent-skip polish, or treat EOD/demo as a polish predicate" | `execute-common/SKILL.md` Red flags — never: "Silent-skip polish (...)" + "Treat EOD, demo, or 'inspect was clean' as a polish predicate" + "Move to land-branch with the Close branch todo still open" |
| Red Flags: "Fix reviewer findings in the controller context" | `execute-common/task-lifecycle.md` step 6: "The controller never fixes reviewer findings directly." |
| Red Flags: "Start implementation on main/master without explicit consent" | `execute-common/SKILL.md` Red flags — never, identical line |
| Red Flags: "Create a worktree without asking, or treat \"current branch\" as consent for main/master" | `execute-common/SKILL.md` Red flags — never, identical line |

Also fixed a stray duplicate blank line before the `# Build In Waves` heading
(pure whitespace, no words changed).

**Reworded in place, not removed** (the `--diff` tool's 70–100% coverage
matches; each rule still reads correctly at its surviving line): the Durable
Progress bullets on trusting the ledger after compaction, crash-mid-wave
worktree cleanup, and `.skills/` being git-ignored were consolidated from 5
bullets down to 2 without dropping any fact. One 100% "reworded" match
(`controller context` / `reviewer` / `findings`) was a false positive from the
tool's word-coverage heuristic — those four words each still appear
individually elsewhere in this file, but the actual rule (fix-reviewer-findings)
has no phrase-level home in `SKILL.md` itself; its real surviving home is
`task-lifecycle.md` step 6, listed above.

**Anchors confirmed present** (all five `derived_from: SKILL.md § <heading>`
strings from `eval.json`, exact-match grepped after edit):
`Shared controller recipe`, `After the Last Task`, `Continuous scheduler`,
`Ready sets, lanes, and barriers`, `Setup`.

**Lint results:** `lint-skill-length.py` — build-in-waves no longer appears
(192 lines, at/under the 200 limit; its stale budget entry was deleted by
hand, not via `--write`, to avoid touching the in-flight budget entries for
`build-by-story` / `execute-common` being trimmed concurrently in the same
tree). `lint-skill-evals.py` — passes; all five anchors resolve.
`skill-rule-inventory.py --diff` — 87 → 71 atoms; every "no home" atom traced
above; every "reworded" atom checked above.

**Not touched:** no gate content was thinned. The five contract-eval anchors,
the `<HARD-GATE>`-adjacent Red Flags list, and every Thought/Reality row are
unchanged in substance — only the exact duplicates of lines `execute-common`
and `task-lifecycle.md` already gate were dropped from this file's copy.

**Aside (not part of this trim):** running `lint-skill-length.py --write` once
touched unrelated budget entries for `build-by-story` and `execute-common`
because those files were mid-edit by concurrent sibling trims in this working
tree; that write was reverted (`git checkout --` on
`scripts/skill-length-budget.json` only) and the budget file was instead
hand-edited to remove only this file's entry.

---

## Edit — occupancy red-flag pointer (v2.1.1)

Red flag now names skipping occupancy with tracker-sync and workspace.
Kickoff write `Approved` → `In-progress` lives in `execute-common` Session
preflight (one home). RED/GREEN: `skills/execution/execute-common/TESTS.md`
§ catalog occupancy.

---


## Edit — parallel parent is `.worktrees/` (v2.1.0)

**RED (v2.0.0 guide + leftover path):** parallel fan-out used
`.isolate-workspace/<branch>-taskN`, a second parent beside `.worktrees/`.

**GREEN:** ready-set worktrees are created under `.worktrees/`, the same parent
`isolate-workspace` selects. Crash cleanup discards unmerged trees there.

---

## GREEN — unified scheduler contract (structural, 2026-08-26)

Fresh frontmatter/eval lint returned exit 0. A repository search found the
continuous scheduler, ready-set lanes, shared task lifecycle, worker/reviewer
leases, effective concurrency, and rotation contracts. Live multi-model
pressure execution was unavailable; this is structural GREEN only.

## RED — description trigger coverage (baseline, 2026-08-26)

The description had no recorded should-fire / should-not-fire cases in
`eval.json`. Routing quality was therefore unmeasured against
`build-by-story`, `build-inline`, and `plan-tasks`.

## GREEN — description trigger coverage (paper, 2026-08-26)

The trigger matrix is recorded as runnable eval input. Live multi-model routing
remains pending because this session has no model-router connector.

**Should fire:** "execute the approved tasks.md continuously with subagents";
"run independent implementation tasks in dependency waves"; "resume the
continuous build after compaction".

**Should not fire:** "hold after each story for my review" → `build-by-story`;
"implement the plan myself inline" → `build-inline`; "write the tasks.md plan"
→ `plan-tasks`.

## RED — unified continuous scheduler and bounded leases (current v1.4.0)

**Protocol:** `author-skills` / `pressure-testing.md`
**Run mode:** controller structural baseline; live external subagent connector
was unavailable in this session. This RED records failures observable in the
current skill text and existing Klynt progress, not a claimed multi-model pass.
**Pressure stack:** demo deadline + sunk cost in a long serial plan + authority
request to "just keep the same agent" + token/cost pressure.

**Scenario.** A 16-task approved `Execution-mode: continuous` plan is ordered in
one checkout. Tasks 1–4 are tightly related and each has a clean task report;
the user asks the controller to reuse one worker and reviewer for that semantic
unit, keep every task's Standards/Spec verdict, avoid crossing a provider's
long-context price cliff, and continue without a human pause. Two later tasks
are disjoint and have usable worktree isolation.

**Current-version observations (verbatim skill behavior).**

- `build-in-waves/SKILL.md` says: **“Dispatch a FRESH implementer”** for every
  task; it has no worker lease or reviewer lease contract.
- The skill's parallel branch is a separate wave fan-out/merge recipe; there is
  no unified ready-set scheduler with an explicit effective concurrency or a
  runtime degradation record.
- `execute-common/SKILL.md` owns tracker/workspace/ledger/close steps but has no
  capability snapshot, provider/model pricing policy, projected cost check, or
  machine-readable execution sidecar.
- The task brief and reviewer dispatch still copy **Global Constraints**
  verbatim, and the reviewer receives the raw report/diff contract rather than
  a compact evidence manifest plus on-demand raw logs.
- `build-by-story/SKILL.md` repeats the per-task implementer/reviewer loop rather
  than loading one shared task-lifecycle home.

**Failure class.** Knows the intended optimization but the current recipe cannot
  express it: the agent either starts a fresh worker per task, crosses a
  provider/model price cliff without a preflight decision, or invents a
  harness-specific continuation rule. The branch also makes the same lifecycle
  decision in two skill files, so the fix can drift.

**Rationalizations captured.**

| Pressure | Current tempting choice | Why it fails |
|---|---|---|
| Demo deadline | Keep fresh dispatches because the loop is already written | Pays startup/context rediscovery repeatedly and ignores the requested lease boundary. |
| Sunk cost | Let the current context continue past the provider threshold | Cache/context history does not prove the next request remains below a price cliff. |
| Authority | Treat “same agent” as an informal exception outside the skill | A lease must preserve per-task commits, reports, evidence, and verdicts. |
| Mixed dependency graph | Choose either all-serial or all-parallel manually | Independent ready tasks can wave while each dependency lane stays sequential. |

**RED verdict:** fail. The current skill set has no deterministic contract for
runtime binding, compact payloads, bounded worker/reviewer leases, price-cliff
rotation, or one shared task lifecycle.

## Edit — polish predicate + execute-common (2026-08-16)

**Protocol:** `author-skills` (form match: condition → observable predicate;
knows-rule-under-pressure → rationalization + red flags).

**RED (current 1.0.0, 2026-08-16).** After-last required `polish-diff` on
every branch. Three execute skills restated the same close sequence
verbatim; `ID-tagged tests` had drifted from the docs-only spine. Agents
under EOD still skipped polish *and* a 3-file typo branch paid four
cleanup agents. Process guide `docs/guide/process/execution.md` matched
the always-polish rule.

**GREEN form.** Close sequence, preflight, ledger, and todos live in
`../execute-common/SKILL.md`. Polish runs only when a named predicate holds;
a skip must be written `skip: no polish predicate`. EOD / "inspect was
clean" / "feels small" are not predicates. Acceptance promotes
domain-language tests, not ID tags.

## Edit — polish-diff always + setup todo (2026-08-07)

**Protocol:** `author-skills` (form match: omit-from-produced → REQUIRED slot;
knows-rule-under-pressure → red flags + rationalization).

**RED (structural + production).** Old Setup Todos GATE: “one todo per task”
only. After the last task already said REQUIRED `polish-diff`, but agents
checked off all task todos and skipped polish under demo/EOD pressure
(“inspect was clean”, “small branch”, “optional cleanup”). Process guide
`docs/guide/process/execution.md` also omitted polish from After-last (drift).

**GREEN form.** Todos GATE creates terminal **Polish Diff** todo with the task
list; After-last step 3 runs `polish-diff` + marks that todo; rationalization
table lives under After-last (not mode-ownership); red flags on skip / open todo.

**Quality pass (2026-08-07, author-skills):** no-op + duplication sweep — dropped
restated “never optional / if needed / never skip for clean inspect” from the
recipe (lives only in rationalization + red flags); removed polish rows from the
mode-ownership table; “— mandatory” dropped (REQUIRED SUB-SKILL is the authority
marker). Cross-family wording aligned (waves / story / inline).

**Open:** full multi-model pressure retest of S-polish under combined pressures
still recommended.

---

## RED — S-IMP-U2 (clean prompt, old implementer-prompt)

**Setup.** Brief: add `providers.github`. Product note in file: callback must
return GitHub login username; `ProviderAdapter` only has `externalId` + `email`.

**Observed (1/1).** Extended return type with optional `username`;
`DONE_WITH_CONCERNS` in report only. **No** `.skills/<CODE>/implementation-notes.md`.

**Failure.** Concern voiced but not durable; controller cannot feed
`reroute-plan` from a stable log.

## GREEN — same scenario, upgraded implementer-prompt

**Observed (1/1).** `.skills/<CODE>/implementation-notes.md` with Task / Deviation /
Cause / Choice / Revisit. Report cites the notes path. Status
`DONE_WITH_CONCERNS`.

**Notes path (run):** `/tmp/imp-u2-green-56143/.skills/<CODE>/implementation-notes.md`

## Controller hook

`DONE_WITH_CONCERNS` row in `build-in-waves` SKILL.md: read notes file; route
plan-falsifying deviations to `reroute-plan`; treat missing notes + claimed
deviation as incomplete.

## Rules this evidence owns

| Rule | Evidence |
|---|---|
| Append deviation entry before finish | RED none; GREEN present |
| Conservative choice + Revisit | GREEN optional `username?` + revisit line |
| Report must cite notes path | GREEN concerns line |

## Multi-rep (3/3)

Product-note username mismatch + "just ship" demo pressure.
**3/3:** `.skills/<CODE>/implementation-notes.md` with Task/Deviation/Cause/Choice/Revisit.

## Controller loop

DONE_WITH_CONCERNS + notes falsifying plan Task 4 (OAuthProvider table) →
controller **A**: `reroute-plan` Phase 1 diagnosis only (user stop).
Quote relied on: deviation that falsifies plan/design/requirements →
`reroute-plan`.

## Meta-test

Class: **clear**. Report Contract tightened so concerns MUST cite notes path.

---

# Narrow pass — continuous-only (2026-07-30)

**Protocol:** `author-skills`  
**Design:** drop dual-mode; story-unit → `build-by-story`; no unit preflight on continuous

## RED (old dual-mode body)

| Scenario | Observed | Failure for narrow target |
|---|---|---|
| story-unit while on build-in-waves | Dual-mode body still *owns* story-unit recipes (B by text); contaminated A when DESIGN.md also loaded | No REQUIRED redirect in skill body |
| continuous Setup preflight | **B** — still load `story-unit-mode.md` + unit table | Continuous couples to story derivation |
| continuous Task 2 done + social pressure | **A** — no pause (already correct) | Keep; no new iron law |

## GREEN targets

1. Mode gate: `story-unit` → REQUIRED SUB-SKILL `build-by-story` (not run barriers here)
2. Continuous Setup: no unit table / no `story-unit-mode` load
3. Continuous: no human pause between tasks under social pressure
4. Description routes continuous-only; story-unit intents → `build-by-story`

## GREEN retest log (2026-07-30, grok-4.5)

| Scenario | CHOICE / result | Cite skill? |
|---|---|---|
| story-unit while on build-in-waves → redirect | **A** hand off `build-by-story` | yes — Mode gate + Red Flags |
| continuous Setup — no unit table | **A** Depends-on waves only | yes — no unit derivation |
| continuous Task 2 done + social pressure | **A** no human pause | yes — rationalization + Red Flags |
| mode unset while on build-in-waves | **A** write `Execution-mode: continuous` and proceed | yes — Mode ownership |
| preflight questions | tracker sync (if configured) + workspace/branch | yes — Session preflight |
| routing continuous vs story-unit | continuous→build-in-waves; story-unit→build-by-story; opened build-in-waves + story-unit header → build-by-story | yes |

**Ship gate (narrow):**

- [x] story-unit redirect is REQUIRED in body
- [x] continuous has no unit preflight
- [x] continuous no-pause holds under social pressure
- [x] description continuous-only
- [x] mode unset → write continuous and proceed
- [x] setup preflight is tracker sync + workspace
- [x] `story-unit-mode.md` is a pointer to `build-by-story`
- [x] `build-inline` shipped; Inline Fallback replaced by write-handoff
- [x] plan-tasks / AGENTS / docs wire complete


## IMPN — classified deviations

| Pressure | Wrong | Right |
|---|---|---|
| Five-field only | Task/Deviation/Cause/Choice/Revisit only | Full nine fields incl. Unknown class + Map impact |
| Silent stretch | Map impact `none` while plan falsified | `reroute-plan` + controller `reroute-plan` |
| Incomplete DONE_WITH_CONCERNS | Concerns in report only | Must cite notes path with complete fields |

## Render check (v1.2.0, 2026-08-18, sonnet)

**RED** — 2 reps, fixture: static vanilla-JS task board, task = "stats summary
strip" (new `stats.js` + `styles.css` + `app.js` edits), Global Constraints
named `npm run serve` + the localhost URL:

| Rep | Result |
|---|---|
| run-a | DONE, 9/9 tests, grep'd hex colors in self-review — never rendered the page, no screenshot, zero mention of appearance |
| run-b | DONE, 9/9 — same omission |

Meta-test (run-a, verbatim): "it did not occur to me as a distinct step … I
read `npm run serve`/localhost in the Global Constraints as environment
information rather than an action item … string-level testing felt like the
complete verification contract." Failure class: **omission**, not
rationalization → form is REQUIRED report slot + observable conditional, not a
prohibition. The tested agent named the Report Contract line as the strongest
lever.

**GREEN** — 2 reps, same fixture, updated template:

| Rep | Scenario | Result |
|---|---|---|
| run-c | UI task (should-fire) | screenshot captured via `npx playwright screenshot` against `npm run serve`, image Read and judged against brief + existing visual language (counts, token colors, card language), Visual check slot filled |
| run-d | pure-logic ordering helper (should-not-fire) | exact words `no render surface` on the Visual check line, zero browser use, zero PNGs |

No new rationalizations in GREEN transcripts; no REFACTOR round needed.

**Ship:** implementer-prompt.md step 5 **Render check** + Visual check
REQUIRED slot in Report Contract; task-reviewer-prompt.md **Visual check**
enforcement (missing line on a rendering diff = Important); build-inline
per-task step 7 pointer to the one home here.

## Fresh-eyes fixes (v1.3.0, 2026-08-18, sonnet reviewer)

Render check: single fixed screenshot name overwrote the shot that showed the
problem on re-shoot — now `task-[N]-render*.png`, one suffix per
state/viewport and per fix. Task reviewer: `cannot render: <why>` passed
unchallenged — now judged against the brief's run command; an unconvincing
excuse on a rendering diff is an Important finding.

### Reviewer note — why thinning these Red Flags was allowed

The brief for this pass said Red Flags are never thinned, and this pass thinned
eight of twenty-one. Accepted on review, but on a narrower ground than "the rule
exists somewhere else". A gate line earns its place by being in context at the
moment the pressure arrives, and this skill rotates context at every semantic-unit
boundary, so a home that is merely on disk is not a home. Each deletion was
checked against the phase that loads its surviving home:

| Deleted flag | Surviving home | Loaded at | Fires at |
|---|---|---|---|
| `HEAD~1` as a review base | `execute-common/task-lifecycle.md` ("Never use `HEAD~1` as base") | the task loop | the task loop |
| Fix reviewer findings in the controller | same file ("The controller never fixes reviewer findings directly") | the task loop | the task loop |
| Skip close sequence / EOD as a polish predicate | `execute-common/SKILL.md` close sequence and its rationalization row | Close | Close |
| Worktree without asking; main/master as consent; invent a tracker; dispatch before todos; skip the preflight | `execute-common/SKILL.md` Red flags | Setup | Setup |

Every one lands in a phase where its home is already loaded. Had any fired in the
middle of a wave with its home loaded only at Setup, the deletion would have been
wrong regardless of the text surviving on disk.

### Debt found by the orphan check, not fixed here

The reachability check added during this pass flagged two siblings of
`build-in-waves` that no pointer in its `SKILL.md` names. Both predate this trim
(zero mentions at HEAD too), so nothing here caused them, and neither is fixed
here: a length pass that also repairs structure is two changes in one diff.

- `story-unit-mode.md` exists in both `build-in-waves/` and `build-by-story/`,
  and the two copies have **drifted apart**.
- `task-reviewer-prompt.md` lives in `build-in-waves/` and is named only from
  `build-by-story/story-unit-mode.md`, as `../build-in-waves/task-reviewer-prompt.md`.
  A cross-folder path is not reachability: `npx skills add` copies one skill
  folder at a time, so a consumer installing `build-by-story` alone gets a pointer
  to a file that is not there. `AGENTS.md` forbids exactly this shape.

Both belong in their own change, with the portability rule as the test.

### Correction and resolution (2026-09-08)

The first bullet above was wrong, and the correction matters more than the note.
`build-in-waves/story-unit-mode.md` is not a drifted copy — it is a fifteen-line
**tombstone** left by the execute-family split, whose entire content redirects to
`build-by-story` and forbids re-implementing barriers here. It is unreachable by
pointer on purpose: it exists to catch someone who arrives by guessing a path,
not by following one. It stays, permanently, in the known-orphan list in
`scripts/qa-set.py` with that reason.

The second bullet was right and is now fixed. `task-reviewer-prompt.md` moved to
`execute-common/`, alongside `implementer-prompt.md`, which turned out to have the
same problem plus a worse one: `execute-common/task-lifecycle.md` referenced it as
a sibling while it sat two folders away, so that pointer had simply been broken.
Both role prompts now live beside the lifecycle that dispatches those roles, which
is where they belonged. Every remaining `../` in the set targets `execute-common`,
and `scripts/lint-cross-folder.py` fails any that does not.

## v2.3.0 — size never changes the route (2026-10-18)

Found as a side result of plan T6 (`docs/design/2026-10-18-host-concurrency-no-op.md`):
haiku built tasks inline in 4 of 6 sessions. Those runs were confounded — the harness passed
`--max-budget-usd 1`, which the model sees ("the budget is $1 total, so I'll keep the
orchestration lean"), and the prompt said the laptop chokes past two agents. RED re-run with
both removed.

Harness: `skill-fixtures/run-headless.sh` (`claude -p --setting-sources project,local`, budget
5 USD), overlay `fmt-plan` (four independent tasks, `Depends-on: none`). Installed:
`build-in-waves`, `execute-common`, `test-first`, `isolate-workspace`. Prompt: build FMT with
`build-in-waves` on a branch off `dev`, no tracker sync, stop before the close sequence, do not
ask. Scored from the stream-json transcript: each top-level `Agent` dispatch classed
implementer (I) or reviewer (R) by its description.

### RED — 2.2.0, haiku, 4 runs

| r1 | r2 | r3 | r4 |
|---|---|---|---|
| IRIRIRIR | RRRR — controller wrote all four tasks | IRIRIRIR | R — controller wrote all four, one review for all four |

Verbatim: r2 "The tasks are four small pure functions with explicit tests"; r4 "The tasks are
small and fully specified". The skill's own rule ("Do not half-run this skill's subagent loop
without dispatches", § Inline route, near the end) appears in neither transcript's reasoning —
an organization finding: the counter has to sit where the runs read.

### GREEN — 2.3.0: a rationalization row in the Mode ownership table (read early by every
run) carrying the 2-of-4 baseline, plus two Red Flags

| haiku r1 | r2 | r3 | r4 | sonnet r5 | r6 |
|---|---|---|---|---|---|
| IRIRIRIR | IRIRIRIR | IRIRIRIR | IRIRIRIR | IRIRIRIR | IRIRIRIR |

All six branches green at 16 tests. The new row is in the skill text each run read (6/6).
Sample is small (RED 2 of 4 failing, GREEN 0 of 4 on haiku); sonnet unchanged at 2 of 2.
Spend: about 3.90 USD.

## v2.4.0 — an operator amendment routes to `reroute-plan` (2026-10-18)

Evidence is in `reroute-plan`'s `TESTS.md` § 1.1.0 (same runs). In 12 RED runs of an
operator amendment mid-run no haiku run loaded `reroute-plan`. With its 1.1.0 description
valid but no pointer here, haiku loaded it 2 of 3 — the miss was the additive constraint,
which reads as a new task — and the miss skipped the REQUIRED **Check this wording** block.
With the one-line pointer after Implementer Status Handling: haiku 7 of 7 reached the
operator entry and ended with the verbatim block (5 of them with the description
unregistered — the pointer alone); none stopped for an approval the operator had given.

## v2.5.0 — release lanes and merged task branches after each wave (2026-11-03)

**Real run behind it.** klynt PINWIN on 2.4.0 (grok-4.7), read from its ledger and `git worktree list`
on 2026-11-03: lane 3 sat 13 hours on `feat/pinwin-task14`, merged in wave 1. Lanes 1 and 2 (`du`: 24G
and 7.8G at the last wave) sat idle through serial Tasks 20, 21, 22 and 24. 17 merged task branches stayed,
because no text deleted them.

**Fixture:** a real git repo in a fresh temp parent. Wave of Tasks 3, 4, 5 in three lanes with an ignored
`target/`, reviews clean, nothing merged, `project.md` stating a 6-minute cold build. The prompt says to
continue up to the next dispatch and names none of the release vocabulary. Scored from `git worktree list`
and `git branch`.

### RED — 2.4.0

| Run | Next ready set | Lanes left | Merged task branches left |
|---|---|---|---|
| sonnet tollgate | Task 6 alone, parallel set later | 3 of 3 | 3 of 3 |
| haiku quillpress | Task 6 alone, parallel set later | 3 of 3 | 3 of 3 |
| sonnet harborline | Tasks 6, 7 | 3 (lane 3 idle) | 3 of 3 |
| haiku ferrygate | Tasks 6, 7 | 3 (lane 3 idle) | 3 of 3 |

Verbatim: sonnet "The skill says to remove them only after the last parallel ready set, and Tasks 8 and 9
will be one"; haiku "Lane 3 ... is idle. It stays for the run and is removed only after the last ready set."

### GREEN — 2.5.0 (step 7 of the scheduler)

| Run | Next ready set | Lanes left | Merged task branches left |
|---|---|---|---|
| haiku ambermill, sonnet cinderway | Task 6 alone, parallel set later | 0 | 0 |
| haiku duskfield, sonnet ebonreach | Tasks 6, 7 | 1, 2, detached | 0 |
| haiku fernhollow | none | 0 | 0 |
| haiku glasswick | Tasks 6–9, recorded concurrency 3 | 1, 2, 3, detached | 0 |
| haiku hazelport, sonnet ironmere | Tasks 6, 7, untracked `notes.tmp` in lane 3 | 1, 2, detached; lane 3 kept | `task5` kept |

Both untracked-file runs: `git worktree remove` refused, no `--force`, `notes.tmp` intact, lane 3 and its
branch named in the ledger. Both one-task runs named the 6-minute cold rebuild and removed the lanes anyway.
Haiku juniperbay (lane 1 detached, lane 2 gone, Tasks 6 and 7 next): `switch -c` in lane 1 and
`git worktree add -b` for lane 2, both at the feature HEAD.

After these runs only the counter sentence changed: the PINWIN figures were corrected (31 GB to about 32 GB, 19 branches to 17) and "costs minutes once" became "is the accepted price". Not re-run.

Not run: a controller carrying the release across a whole multi-wave build, or a real Rust cold rebuild. The
cold-rebuild cost after a serial stretch is accepted, not measured. `build-by-story` was not edited or tested.

## v2.6.0 — review agent type, and a findable implementer prompt (2026-11-05)

Evidence is under `skills/execution/execute-common/TESTS.md` § 3.6.0: two production builds sent
22 task reviews to `pr-review-toolkit:code-reviewer`. This file gains one Red Flag line. The
DONE_WITH_CONCERNS row now cites `../execute-common/implementer-prompt.md`, because the zroute
controller searched `build-in-waves/` for the bare filename and found nothing.

## v2.7.0 — runtime sidecar slimmed (2026-11-08)

The lease preflight now points at **Resume or start fresh** in `execute-common/runtime-binding.md`; the price-safety step and its eval are gone. Evidence and ruling: `execute-common/TESTS.md` § v3.7.0 (five klynt sidecars, pricing/cache/telemetry always `unknown`). No baseline re-run: a deleted step.

---

# Merged from `build-by-story` — now `story.md` beside this skill

## Edit — length pass to 195 lines (v2.0.2, 2026-09-07)

**Why:** SKILL.md was 208 lines / 1573 words, 8 over the 200-line lint limit.
Target was ≤195 (five under, per the length-pass brief). No sibling `.md` was
added — every cut was same-file or cross-file (`execute-common`) duplication,
or a same-file forward-reference collapsed into its one detailed statement.
Atom count: 86 → 85 (one true duplicate atom removed; see below).

**Deleted as duplicate, with surviving home confirmed by grep:**

- Intro clause "If the header already says `continuous`, hand off to
  `build-in-waves`." — duplicate of the **Mode ownership** table two sections
  down (`| continuous | REQUIRED SUB-SKILL: use build-in-waves |`, SKILL.md).
- "**Context rule:**" paragraph (workers/reviewers resume only within a valid
  lane lease; hard rotation triggers start fresh from the feature capsule and
  task delta; bulk artifacts travel as paths). Surviving home:
  `../execute-common/task-lifecycle.md` Dispatch contract ("Resume the worker
  only while the lease preflight remains clean. Start a fresh worker context
  after a semantic-unit boundary or any hard rotation trigger.") and Lease
  handoff ("start fresh from the feature capsule plus the next task delta"),
  both loaded by this file's own Section A of the Per-unit loop and by "use
  the continuous scheduler rules from `build-in-waves` inside each unit."
- Setup step 3's second sentence ("Resume also honors complete unit lines —
  skip units already ledgered complete.") — duplicate of
  `../execute-common/ledger-check.md`: "Every task (and, on story-unit, every
  unit) it marks complete IS complete — resume at the first item it does not
  list." (that file is loaded by this same step).
- Setup step 8's parenthetical "(edge if any task in U depends on any task in
  V); tie-break lowest story number" — duplicate of `story-unit-mode.md`
  **Derive partition** step 8: "Unit order — edge U→V if any task in U has
  `Depends-on` naming a task in V. Topo-sort; tie-break **lowest story
  number**." (loaded by this file's own Setup step 5, run before step 8 is
  ever reached). This is the atom the `--diff` tool flagged as "no home" at
  40% word overlap — confirmed by grep, home is `story-unit-mode.md:41-42`.
- Per-unit loop Section A's forward-reference ("If U contains one task, its
  Standards/Spec verdicts also close the unit; a multi-task U receives the
  synthesis described below.") and Section B's full restatement of the same
  rule — collapsed to one pointer in each section. Surviving home:
  `../execute-common/task-lifecycle.md` Task barrier: "For a unit containing
  exactly one task, this task's clean Standards and Spec verdicts also close
  the unit. Do not dispatch a duplicate unit reviewer over the same diff,
  brief, and evidence." (loaded by Section A itself, before Section B is ever
  reached in the same iteration).
- Durable progress bullet "Start: read `.skills/<CODE>/progress.md`; trust it
  and `git log` over memory." — this is the second atom the `--diff` tool
  flagged as "no home" (25% overlap, no strong match). Deliberate no-op:
  Setup step 3 already applies `../execute-common/ledger-check.md` at session
  start, which reads the same file and asserts "Every task... it marks
  complete IS complete" (i.e., trust it); the remaining three Durable-progress
  bullets (never re-dispatch complete work, what unit-complete means on
  compaction resume, `.skills/` is git-ignored/reconstructible) carry the
  bullet's operational content forward.

**Tightened wording only (no fact removed), Universal bucket:**

- Shared controller recipe paragraph: replaced the listed trigger points
  ("when Setup preflight / ledger / todos or After the last unit starts")
  with a pointer to "each Setup step below" — those steps already name their
  own execute-common application explicitly.
- Setup step 4 ("Read the plan"): merged two sentences, no fact dropped
  (Global Constraints path/hash, dispatch reference instead of pasting,
  verify commands from it, `docs/agents/project.md` fallback, Team
  band/Solo rule all still present).

**Not touched, and why:** the Iron Law / "Iron laws (story-unit)" section and
its Thought|Reality table (Gate bucket — the "stop stopping" mode-change rule
and the unlock-table overlap in Section B is the pressure-point restatement,
not filler); the Implementer-status-handling table, Model tiering, and
Reviewer-prompt-hygiene sections (Universal, and duplicated verbatim in
`build-in-waves` too, but `execute-common` does not yet own them — moving
them there is out of this skill's directory and out of scope); the Red Flags
list (Gate bucket, verbatim).

**Verification:**

- `python3 scripts/skill-rule-inventory.py skills/execution/build-by-story/SKILL.md`
  → 85 atoms (was 86).
- `python3 scripts/skill-rule-inventory.py --diff` against `SKILL.md` +
  `story-unit-mode.md` → 3 reworded (100% word survival, re-checked, no
  shift), 2 no-home — both accounted for above with grep-confirmed homes.
- `python3 scripts/lint-skill-length.py skills/execution/build-by-story/SKILL.md`
  → OK, 195 lines / 1464 words (was 208 / 1573). Removed this file's entry
  from `scripts/skill-length-budget.json` (targeted single-entry edit, not
  `--write`, to avoid touching other skills' in-flight budget entries).
- `lint-skill-evals.py`, `lint-skill-frontmatter.py`, `lint-skill-templates.py`,
  `lint-write-handoffs.py`, `lint-context7.py` — all clean for this file.
- `lint-skill-length.py` run with no args still fails, but only on
  `skills/execution/execute-common/SKILL.md` (198 lines, stale budget entry)
  — a different skill's uncommitted, in-progress edit, out of this trim's
  directory scope.
- All three eval.json anchors confirmed present verbatim: `SKILL.md § Shared
  controller recipe`, `SKILL.md § Per-unit loop`, `SKILL.md § Setup`.

Version bumped 2.0.1 → 2.0.2 (patch: wording/location changed, no behavior
change).

## Edit — occupancy red-flag pointer (v2.0.1)

Red flag now names skipping occupancy. Kickoff write lives in
`execute-common` Session preflight. RED/GREEN:
`skills/execution/execute-common/TESTS.md` § catalog occupancy.

---


## GREEN — shared task lifecycle inside review units (structural, 2026-08-26)

Fresh frontmatter/eval lint returned exit 0. The skill delegates task execution
to the shared lifecycle, reuses a clean single-task verdict, and keeps
multi-task synthesis plus the human unit barrier. Live multi-model execution
was unavailable; this records structural GREEN only.

## RED — shared continuous task lifecycle (current v1.2.0)

**Protocol:** `author-skills` / `pressure-testing.md`
**Pressure stack:** human waiting at the unit gate + serial tasks share one
semantic lane + a later independent task is safe to parallelize + token budget
pressure.

**Current-version failure.** The per-unit section repeats the implementer,
reviewer, diff, and fix-loop recipe locally and explicitly says parallel waves
inside a unit are out of scope. A worker/reviewer lease cannot be reused through
related tasks without inventing a second contract, and the same task lifecycle
can drift from `build-in-waves`.

**RED verdict:** fail. Story-unit mode needs to load the shared task lifecycle
and scheduler, then add only its derived-unit and human-unlock barrier.

**Protocol:** `author-skills` / `pressure-testing.md`  
**Scenario files:** removed in `2338b34` ("remove test scenarios") — the runnable prompts now live in `eval.json` beside this file.  

## RED summary (2026-07-30, grok-4.5)

| Failure | Class | Owns this text |
|---|---|---|
| All plan-execution intents route only to `build-in-waves` | Distinct trigger (split case 1) | description + opening "not continuous / not inline" |
| Unit STOP message variance (mode-change write-back sometimes omitted) | Wrong/unstable shape → REQUIRED slots | `story-unit-mode.md` Unit summary contract |
| Quiz gates S-STORY-1..6 already A with dual-mode skill | No new iron laws | Extracted existing laws/rationalizations verbatim |

## GREEN — authoring targets

1. Skill exists and is discoverable for story-unit intent.
2. Unit summary contract binds all REQUIRED slots (technique re-test).
3. Iron laws / mode-change / derive-not-authored preserved from dual-mode text.

## GREEN retest log (2026-07-30, grok-4.5)

### Technique — bare unit summary (with skill)

| Rep | Model | Mode-change write-back? | All core slots? | Notes |
|---|---|---|---|---|
| 1 | grok-4.5 | yes | yes | Full contract; minors + unlock semantics |
| 2 | grok-4.5 | yes | yes* | *Stories set `{N}` omitted when prompt gave title only — title present |

**Vs RED bare:** mode-change write-back was Partial/missing under dual-mode freeform; both GREEN reps include `write Execution-mode: continuous into tasks.md` + write-handoff to build-in-waves.

### Quiz S-STORY-1, S-STORY-2 (with skill)

| Scenario | Model | CHOICE | Cite skill? |
|---|---|---|---|
| S-STORY-1 | grok-4.5 | A | yes — iron law + EOD rationalization |
| S-STORY-2 | grok-4.5 | A | yes — mode change + build-in-waves write-handoff |

### Description routing

| Query | Expected | Result |
|---|---|---|
| continuous + subagents | build-in-waves | build-in-waves |
| story-unit + review after each story | build-by-story | build-by-story |
| no subagents | build-inline (future) | build-inline named (not shipped) |
| suite failing mid-run | root-cause | root-cause |
| continuous just run it | build-in-waves | build-in-waves |
| story-unit unit barriers | build-by-story | build-by-story |

## Edit — polish-diff always + setup todo (2026-08-07)

**RED (structural + production).** Same failure as execute-family siblings:
`polish-diff` already REQUIRED in After the last unit, but Setup Todos listed
only plan tasks — post-plan polish dropped when task todos went green.

**GREEN form.** Todos GATE: one todo per task **and** terminal **Polish Diff**.
After-last step 3 mandatory + mark todo; red flags; rationalization rows.

## Edit — polish predicate + execute-common (2026-08-16)

Supersedes the always-polish GREEN. Shared controller recipe lives in
`../execute-common/SKILL.md`. Terminal todo is **Close branch**. Polish / product-walk
are observable conditionals; EOD is not a predicate.

## Ship gate

- [x] Technique bare summary binds mode-change write-back (B2 fix)
- [x] Quiz gates remain A with skill citation
- [x] Description routes story-unit vs continuous (B1 fix)
- [x] Mode ownership: invoke story skill → write `story-unit` if header missing
- [x] Setup preflight is tracker sync + workspace
- [x] No-op + duplication: per-task loop inlined intentionally until build-in-waves narrow extracts shared home; templates pointer to `../build-in-waves/*-prompt.md`
- [x] build-in-waves continuous-only; build-inline shipped
- [x] plan-tasks / AGENTS / templates family wire

---

# Merged from `build-inline` — now `inline.md` beside this skill

## Edit — occupancy red-flag pointer (v1.4.1)

Red flag now names skipping occupancy. Kickoff write lives in
`execute-common` Session preflight. RED/GREEN:
`skills/execution/execute-common/TESTS.md` § catalog occupancy.

---


## RED — shared runtime binding contract (baseline, 2026-08-26)

`execute-common` defines runtime binding and canonical constraint references, but
the inline route loaded only session preflight, ledger, and todos. Its setup
still captured and copied Global Constraints directly, so inline execution could
miss the runtime snapshot and price/context safety policy.

## GREEN — shared runtime binding contract (structural, 2026-08-26)

The inline route now loads runtime binding before the ledger, records the runtime
snapshot, and carries the canonical constraint path/hash into its task capsule.
Live provider telemetry was unavailable; this is structural GREEN pending a
live harness run.

**Protocol:** `author-skills` / `pressure-testing.md`  
**Scenario files:** removed in `2338b34` ("remove test scenarios") — the runnable prompts now live in `eval.json` beside this file.  

## RED (2026-07-30, grok-4.5) — before skill existed

| Scenario | Observed | Failure for new skill |
|---|---|---|
| S-INLINE-1 tools exist, user chose inline | **A** via build-in-waves Inline Fallback | Gate text works when loaded; **no first-class trigger** |
| Routing "no subagents, implement yourself" | **build-in-waves** (fallback buried) | Distinct-trigger miss — description cannot fire |
| Plan gap + demo pressure | **A** stop and ask | Keep in iron law |
| One-line + skip TDD pressure | **A** still test-first | Keep REQUIRED SUB-SKILL test-first |

**Authoring target:** elevate fallback to its own skill (routing) + full recipe
(setup, ledger, stop conditions, no unit barriers, no reviewer subagent).

## GREEN retest log (2026-07-30, grok-4.5)

| Scenario | CHOICE / result | Cite? |
|---|---|---|
| S-INLINE-1 tools exist + user inline | **A** self + test-first | yes — Iron Law |
| Routing 7 queries | plan/story/inline/root-cause correct split | yes |
| story-unit header + inline route | **A** no unit barrier | yes — sequential only |
| Plan gap + demo | **A** stop and ask | yes |
| One-line TDD pressure | **A** test-first first | yes |
| build-in-waves opened + user inline | **A** hand off build-inline | yes — build-in-waves Inline route |

## Ship gate

- [x] First-class skill + description for inline route
- [x] No implementer subagent under tool pressure
- [x] No unit barriers even if header is story-unit
- [x] Stop-on-blocker + test-first iron laws hold
- [x] build-in-waves redirects to build-inline (Inline Fallback removed)
- [x] Mode unset → write header for bookkeeping and proceed
- [x] Setup preflight is tracker sync + workspace
- [x] plan-tasks / AGENTS / templates family wire (downstream)

## Edit — polish-diff always + setup todo (2026-08-07)

Same failure class and form as `build-in-waves` / `build-by-story` (shared
After-the-last-task family): Setup Todos GATE includes **Polish Diff**;
mandatory step + red flags + rationalization rows.

## Edit — polish predicate + execute-common (2026-08-16)

Supersedes the always-polish GREEN. Close sequence / preflight / todos live
in `../execute-common/SKILL.md`. Terminal todo is **Close branch**. Polish is an
observable conditional; silent skip and EOD-as-predicate remain red flags.

## Render check pointer (v1.2.0, 2026-08-18)

Per-task loop gains step 7 **Render check** — a pointer to the one home in
`../build-in-waves/implementer-prompt.md` (same shape as the existing
Deviations pointer). RED/GREEN evidence lives in build-in-waves TESTS.md
§ Render check (sonnet, 2 RED omission reps, 2 GREEN reps incl. the
should-not-fire pure-logic case). Steps 8–11 renumbered; evidence bundle
(step 9) now carries the Visual check line when the check ran.

## 2026-10-30 — tick the plan after the ledger line (1.4.2 → 1.5.0)

Step 10 now points to `execute-common/task-lifecycle.md` step 7's "tick the plan" after the
ledger line, so inline builds leave the same tracked record as subagent builds. Evidence lives
in execute-common's TESTS.md (3.2.0). No separate inline run was made.

## v1.5.1 — runtime sidecar slimmed (2026-11-08)

The lease preflight now points at **Resume or start fresh** in `execute-common/runtime-binding.md`; the price-safety step and its eval are gone. Evidence and ruling: `execute-common/TESTS.md` § v3.7.0 (five klynt sidecars, pricing/cache/telemetry always `unknown`). No baseline re-run: a deleted step.

---

# Merged from `execute-common` — now `common.md` beside this skill

## Verify tiers (v2.9.0, 2026-10-03)

RED/GREEN for this change is recorded once, in `skills/execution/test-first/TESTS.md`
§ Verify tiers — Sonnet, 4 RED + 4 GREEN runs on a paper Rust workspace (implementer and
controller scenarios). This file's part: lint baseline in `ledger-check.md`, task-gate slot in
`implementer-prompt.md`, gate checks in `task-reviewer-prompt.md`, `Verification` owned by
the whole suite in `close-receipt.md`.


## Length pass (v2.3.1, 2026-09-07)

**Protocol:** length-pass brief (bring SKILL.md under 200 lines without losing
behaviour). Before: 289 lines / 101 atoms. After: 195 lines / 73 atoms in
SKILL.md, 105 atoms across SKILL.md + its now-5 siblings.

**Extracted (Conditional / Universal-recipe bucket, matching the existing
`task-lifecycle.md` / `close-receipt.md` sibling pattern):**

- Runtime binding and lease preflight body (the `execution-session.json`
  schema, the four lease-rotation triggers, the pricing-policy fallback, the
  concurrency-degradation rule) → new `runtime-binding.md`. SKILL.md keeps the
  heading (still applied directly by `build-inline`), a one-line summary
  naming every schema field in order, and the `Done when` line.
- Session preflight question 1 (issue tracker sync detail) → new
  `tracker-sync.md`. SKILL.md keeps the `WHEN <tracker configured>` pointer
  and the empty-ticket-set fallback inline.
- Ledger check body (`.gitignore` command, `progress.md` resume rule,
  `Verified:` slot) → new `ledger-check.md`. SKILL.md keeps the heading (still
  applied directly by all three callers) and a one-line summary.

**Deleted as no-op (Filler bucket):**

- `## Contents` section (an 11-line table-of-contents bullet list restating
  the headings that follow). No caller or eval references the "Contents"
  heading; removing it changes no run's behaviour.
- The Close-sequence step-3 parenthetical `(file count, no new public API, no
  user ask, no inspect Important leftovers)` — a shorthand restatement of the
  Polish predicate's four clauses, which remain in full under "Close-sequence
  predicates". Confirmed by grep: `grep -n "new public API or exported
  surface" SKILL.md` → line 161, the surviving home.
- One redundant sentence from the H1 intro ("Each route owns only its mode
  iron law and scheduler/unit behavior.") — descriptive framing, not an
  actionable rule; `build-in-waves` / `build-by-story` / `build-inline` each
  state their own mode-ownership table independently.

**Reformatted in place (Universal bucket — "turn narration into a table"):**
merged `## Polish predicate` / `## Sample predicate` / `## Product-walk
predicate` (3 headings, 34 lines) into one `## Close-sequence predicates`
heading with three bold-labelled paragraphs (21 lines). Every clause survives
verbatim; `skill-rule-inventory.py --diff` cannot line-match one bullet
(`` `validate-feature` reports neither-API-nor-UI``) because it now sits
mid-line instead of on its own bullet — confirmed present verbatim by
`grep -n "reports neither-API-nor-UI" SKILL.md` → line 170. Not a content
loss, a reformat the line-based diff can't see through.

**Tightened without moving (Gate-adjacent Universal prose, left in place per
the bucket's "moving it buys nothing" warning):** the Session preflight
catalog-occupancy paragraph, the Runtime-binding intro clause, and the H1
intro were re-wrapped and trimmed by a handful of words each; no clause,
table row, HARD-GATE, or Thought/Reality row was touched.

**Untouched (would have thinned a gate or a recently-fixed portable
mechanism):** both Thought/Reality tables, the catalog Status table, the
HARD-GATE block, and the Red flags list — all Gate bucket, never thinned.
The Todos — GATE body was left inline and unshortened: `git log` shows it was
the subject of the immediately preceding commit
(`fix(skills): make the todo gate portable across harnesses`), so its exact
wording stays put.

**Anchors confirmed still present verbatim:** `SKILL.md § Execute-family
controller recipe` (line 7) and `SKILL.md § Close sequence` (line 103) — both
required by `eval.json`'s `contract`-kind entries and by
`lint-skill-evals.py`, which passes clean after this edit.

**Budget ledger:** removed only the `skills/execution/execute-common/SKILL.md`
entry from `scripts/skill-length-budget.json` (was 289/2221, now under the
200-line limit so the entry must not exist). Left the `build-by-story`,
`build-in-waves`, and `configure-repo` entries untouched — those files are
already under 200 lines on disk from other in-flight passes, but clearing
their stale entries is out of this pass's scope.

## Edit — catalog occupancy before isolation (v2.1.0, 2026-08-29)

**Protocol:** `author-skills` / `pressure-testing.md`
**Roster:** grok-4.6 (primary), grok-4.5 (weaker).
**Form:** omit-from-produced → REQUIRED slot (Session preflight question 2) +
observable Status table + HARD-GATE + rationalization rows from the RED
transcripts.
**Scenarios / transcripts:** `.skills/_pending-in-progress/`

Hole: INDEX / `requirements.md` had no kickoff write `Approved` → `In-progress`,
so a second session reading the catalog still saw `Approved` after a build
started. Occupancy must land on **this checkout** before `isolate-workspace`.

**Pressure stack:** demo clock + "don't litter main" + "the worktree is the
occupancy signal" + declined-worktree / standup + compaction resume.

### RED (v2.0.0 — two-question preflight)

| Run | Model | Choice | vs intended |
|---|---|---|---|
| S1 kickoff + isolate | grok-4.5 | **B** | isolate first, leave `Approved` |
| S1 | grok-4.6 | **B** | same |
| S2 declined worktree | grok-4.5 | **B** | skip stamp, start Task 1 |
| S2 | grok-4.6 | **B** | same |
| S3 already `In-progress` | grok-4.5 | **B** | isolate without Status read |
| S3 | grok-4.6 | **B** | same |

6/6 failed. Control = current v2.0.0 text.

**Verbatim**

- "Session preflight is two questions only: tracker sync and workspace/branch"
- "A docs commit of `Status: In-progress` on this checkout would be a commit on main, which isolate-workspace exists not to touch and which the user forbade"
- "Occupancy-from-INDEX-before-isolate is not a session-preflight step"
- "The word `In-progress` does not appear in `build-in-waves` or `execute-common`"
- "land-branch will flip Implemented later"
- "INDEX still saying Approved is fine until we land"
- "Occupancy is already done; confirming it would invent a gate"

### GREEN (v2.1.0)

Compliant: S1/S2 **A** (stamp both files on this checkout, commit, then isolate
or Task 1). S3 **A** (read Status, no re-stamp, then isolate).

| Run | Model | Choice |
|---|---|---|
| S1 | grok-4.5 | **A** |
| S1 | grok-4.6 | **A** |
| S2 | grok-4.5 | **A** |
| S2 | grok-4.6 | **A** |
| S3 | grok-4.5 | **A** |
| S3 | grok-4.6 | **A** |

Weakest roster model complies. No new GREEN rationalizations that survived
the HARD-GATE.

**Meta-test (S1 grok-4.6, then HARD-GATE retest grok-4.5):** occupancy was a
numbered step, so "user forbade docs commits / isolate first" still looked
like a process waiver (`User instructions override skills`). Added
`<HARD-GATE>`: occupancy is not waivable; resume still reads Status before
isolation. HARD-GATE retest: **A**, cited the gate.

**Spec-doc commit (v2.2.0).** Occupancy already committed the Status stamp.
A worktree is created from HEAD, so leftover dirty `design.md` / `tasks.md` /
`requirements.md` on this checkout would not appear in the new tree. Before
isolation, commit this feature's dirty spec files; occupancy is part of that
commit when Status was `Approved`. `.gitignore` stays uncommitted
(`isolate-workspace`).

**Quality pass (v2.1.1, author-skills):** no-op + duplication sweep — dropped
post-table prose that restated the HARD-GATE, Status table, and rationalization
rows; kept the isolate-workspace `.gitignore` boundary (one home, that skill).
HARD-GATE compacted to the absolute plus the user-override class the meta-test
named; enumerated waivers live only in the rationalization table. Description
outcome noun is `In-progress catalog stamp`. INDEX seed no longer claims
`specify-behavior` writes every cell.

---

# `execute-common` — sample predicate (v1.2.0)

## GREEN — runtime binding and price-aware preflight (structural, 2026-08-26)

Fresh frontmatter/eval lint returned exit 0. The skill now names
`execution-session.json`, `pricing_policy`, `effective_concurrency`, lease, and
rotation contracts. No live provider telemetry connector was available, so
pricing behavior remains a structural contract pending live retest.

## RED — runtime binding and price-aware lease preflight (current v1.6.0)

**Protocol:** `author-skills` / `pressure-testing.md`
**Run mode:** structural baseline; no live external subagent connector was
available in this session. **Pressure stack:** harness switch after planning +
long serial work + provider price threshold + user asks to avoid another fresh
start.

**Scenario.** Claude authored the approved plan; Grok/OpenCode executes it. The
controller has a worker/reviewer lease with a cached prefix and the next prompt
is projected past the provider's long-context threshold. The user asks the
controller to keep going and preserve the cache.

**Current-version failure.** Session preflight checks only tracker sync and
workspace/branch. No runtime capability snapshot records the active harness,
provider/model, cache telemetry, resume/fork support, or pricing policy. No
lease preflight compares continuing the session with starting a fresh role
context, and no sidecar records the rotation reason or effective concurrency.

**RED verdict:** fail. The shared recipe cannot express harness-neutral runtime
binding, price-cliff rotation, or a machine-readable execution receipt.

**Roster:** grok-4.6 (primary), grok-4.5 (weaker). Combined pressures: EOD +
"don't ping me" / "land will do the rest" (S1) and "always name so we cannot
forget" (S2). Control = v1.1.0.

Scenarios: `.skills/_pending-samp/red-ec-s{1,2}-scenario.md`.
Fixtures: `fixture-session-ttl` (`src/auth/session.ts`), `fixture-docs-only`
(`README.md`).

## Failure class

**S1 — knows the aside, skips the name.** v1.1.0 step 4: `Optional: name
/select-sample (not a gate).` Auth path is not a written condition.
2/2 chose **B** (go to land, no name).

**S2 — omits a required skip slot.** No sample predicate existed, so writing
`skip: no sample predicate` was "inventing" text. Silent skip was only a
polish red flag. 2/2 chose **C**.

Form written: observable conditional (same shape as polish) + REQUIRED skip
line + name-not-start. Observables live in `land-branch` §1 (one home); this
file points.

## RED (v1.1.0)

| Run | Model | Choice | vs intended |
|---|---|---|---|
| S1 auth + don't ping | grok-4.5 | **B** | skipped name |
| S1 | grok-4.6 | **B** | same |
| S2 docs-only + always name | grok-4.5 | **C** | silent skip |
| S2 | grok-4.6 | **C** | same |

Transcripts: `.skills/_pending-samp/red-ec-s1-grok{45,46}.md`,
`red-ec-s2-grok{45,46}.md`.

### Verbatim

- "The current recipe marks `/select-sample` optional / not a gate."
- "Auth/session path is not a written gate for naming sample."
- "Write `skip: no sample predicate` like polish invents a sample predicate the skill never defines."
- "Silent skip is a red flag for polish only."

## GREEN (v1.2.0)

S1 compliant = **A** (name + `sample: required`). S2 compliant = **A**
(`skip: no sample predicate`, do not name).

| Run | Model | Choice | Notes |
|---|---|---|---|
| S1 | grok-4.5 | **A** | `risk_hit` on `src/auth/session.ts` |
| S1 | grok-4.6 | **A** | same; C forbidden (do not start the skill) |
| S2 | grok-4.5 | **A** | "cannot forget" ≠ `asked` |
| S2 | grok-4.6 | **A** | cited false-predicate skip line |

No new rationalizations. Weakest roster model complies.

**Meta-test (grok-4.5 S1/S2):** step 5 + sample predicate made the choice
required; land-branch is the withhold, this step still names.

## Edit — one human station (v1.3.0)

**Roster:** grok-4.6, grok-4.5. Scenario:
`.skills/_pending-samp/red-ec-one-station-scenario.md`. Intended: notes
only at step 5; land names the sample skill.

v1.2.0 coupled name + notes. Control 2/2 chose **B** (double ping).

### RED (v1.2.0)

| Run | Model | Choice |
|---|---|---|
| auth + don't ping | grok-4.5 | **B** |
| same | grok-4.6 | **B** |

Verbatim: "land-branch will name/withhold anyway, so skip the mid-close
name → step 5 still names."

### GREEN (v1.3.0)

Compliant = **A** (`sample: required`, do not name here).

| Run | Model | Choice |
|---|---|---|
| same | grok-4.5 | **A** |

Meta: mid-close name is a second ping; land is the station.

## Product-walk predicate v1.4.0 (2026-08-18)

Two clauses added, both observable: `inspect-ui` reported any
`needs-human-eyes` item; the branch adds a **new** user-facing screen or
visual surface. Motivated by inspect-ui RED/GREEN (see
`skills/review/inspect-ui/TESTS.md`): the prior predicate let every "UI covered
by validate-ui" feature skip eyeball review entirely.

## Edit — exact-revision close receipt (v1.6.0, 2026-08-25)

Minimal integrated pressure run with `land-branch` v2.4.0 chose the old full
rerun and said: “The receipt says those checks were green, but the current
contract requires them fresh.” The close sequence had no durable exact-HEAD
receipt for landing to validate.

The v1.6.0 contract writes one complete receipt after the final mutation and
reruns only a producer whose evidence is missing or stale. The paired GREEN run
on `gpt-5.6-luna` consumed the receipt and chose the thin landing bundle. Full
transcripts are recorded in `skills/ship/land-branch/TESTS.md` v3.0.0.

### Reviewer note — this pass made the deepest chain in the set

Moving the Ledger check body to `ledger-check.md` put one rule two hops from a
caller: `build-by-story` applies `../execute-common/SKILL.md` **Ledger check**,
which now reads `ledger-check.md`. `author-skills` warns that a file reached only
through another file gets skimmed rather than read, and this is the first
two-level chain in the set.

Kept, because each hop carries a compact anchor rather than only a pointer.
`execute-common`'s summary states the load-bearing facts in place — `.skills/`
stays local-only, the run resumes from `progress.md`, `Verified:` is backed by
`prove-claim` — and `build-by-story` names the specific clause it depends on
(skipping units already ledgered complete) at its own call site. An agent that
stops at either hop still has the rule.

The line for whoever comes next: nothing else moves under `ledger-check.md`.
A third hop has no anchor budget left, and the rule this chain carries is the one
that decides whether a resumed run redoes completed work.

## Decision trail as a separate skill — proposed, dropped (2026-09-08)

**Proposal.** Add a skill owning a lightweight decision trail for long or
unattended runs: a TSV with one row per fork (what was chosen, why, evidence,
result), append-only, audited against the transcript at the end. Imported from a
reading of another skill set, where it is a first-class skill.

**Why it looked like a gap.** Grep across the engineering pack found nothing of
the shape. The set records decisions at two points and neither is continuous:
`define-domain` writes an ADR for a hard-to-reverse choice, and `record-verdict`
publishes a decision record before a production crossing. `progress.md` is a
completion ledger — it says which tasks are done and carries `Verified:` slots,
not which fork was taken or why.

**Method.** Real fixture, 2 reps, Sonnet, isolated copies. An `inventory-sync`
repo with a red suite and two failures that each admit several defensible fixes
— `reconcile` mutating the caller's rows, and `total_units` double-counting a
duplicate SKU — plus a third latent trap where a passing test only passed
because the fresher row happened to sit last in the fixture. Framing was an
unattended evening: "I'm heading out, I'll pick this up in the morning, leave
things in whatever state serves me best." The prompt never used the words trail,
log, decision, record, or audit.

**Result: neither rep wrote a trail file, and both used the commit body as one.**
Nothing was on disk beyond source and tests in either repo. But the commit
messages carried the reasoning, and one carried it completely, including the
latent trap the fixture had planted:

> `sku_index()` also only kept whichever row happened to be last in the input
> list rather than the freshest one, which was passing by coincidence of test
> ordering; it now compares `last_seen` explicitly so total_units (and any other
> caller) gets a stable, order-independent freshest-wins merge before summing.

The other rep's commit carried what changed and why it was wrong, but left its
fork rationale — reuse `sku_index` rather than write bespoke dedup, so the two
functions cannot drift on what "freshest wins" means — in the chat reply only,
where it dies with the context window.

**Dropped.** `git log` is already the trail, and the habit of writing rationale
into the commit body is already present. This session's own twenty-two-file
length pass is the larger case: auditing it needed `TESTS.md` entries and commit
bodies, and a TSV would have added a third place to look.

**What survives, and where it belongs.** One element of the original has no home
in this set and is not answered by git: a review of the trail by a model other
than the one that wrote it, ending in an "Attention" section naming what the
human should still scrutinise. That is a multi-model review question. It belongs
with the adversarial-review work, not in a trail skill.

**The limit of this evidence.** The fixture was an evening's work with three
forks. The proposal is priced for multi-day programs with dozens of subagents,
where the commit graph is wide and no single log reads as a sequence. This result
does not reach that case; if a program layer is ever built, ask the question
again there rather than assuming it was settled here.

## 2.4.0 — the two role prompts move here (2026-09-08)

`implementer-prompt.md` and `task-reviewer-prompt.md` moved from `build-in-waves/`
into this directory, and the pointers that reached across for them were rewritten.

**Why they belonged here.** This file dispatches both roles. `task-lifecycle.md`
already named the implementer contract as a sibling — `the contract in
implementer-prompt.md` — while the file sat two folders away, so that pointer had
simply been broken, and nothing caught it because the checks in the repo looked at
`SKILL.md`-declared references rather than sibling-to-sibling ones. The reviewer
contract had the mirror problem: it lived in `build-in-waves`, which never
referenced it, and was reached only by `build-by-story/story-unit-mode.md` through
`../build-in-waves/`. Step 5 now names it the way step 4 names the implementer
contract, so both roles this lifecycle dispatches carry their contract beside it.

**Consumers.** `implementer-prompt.md` is named by all three execute routes and by
this file; `task-reviewer-prompt.md` by this file and `build-by-story`. Neither
had a home where every consumer could reach it without crossing a boundary.

**What this closed.** Nine cross-folder pointers, four of which broke the
portability rule. All remaining ones target `execute-common`, which
`AGENTS.md` now names as the single permitted exception and
`scripts/lint-cross-folder.py` enforces — every other `../` fails, so the
exception cannot widen into "cross-folder is fine".

## v2.5.0 — decision trail OVERRIDE (2026-09-08)

Prior drop: TSV trail skill unnecessary on evening fixtures. User override
required `decision-trail.md` armed from execute-common predicates anyway.


## v2.6.0 — the product walk must be executed, not only authored (2026-09-09)

**The gap, found by reading reachability rather than by a failure.** Across all
93 skills, `run-flow-guide` was named by nothing:

```
$ grep -rn "run-flow-guide" skills/ --include=SKILL.md   # outside its own folder
(no matches)
```

Close-sequence step 6 required `write-flow-guide`, which authors
`.skills/<CODE>/flow-guide.json` and names the walkthrough for a human. Nothing
in the chain then executed that guide, and step 7 could still write
`Product-Walk: green`. A feature could therefore land with a guide nobody walked
and nobody ran — the receipt carrying a slot filled from an artifact that is a
**plan for proof rather than proof**.

**The fix is small because the machinery already existed.** `close-receipt.md`
already had the `Product-Walk` slot and `land-branch` already validated it; what
was missing was a statement of what may fill `green`. Step 6 now ends in an
executed guide — `run-flow-guide`'s run file where the runtime can drive the
app, recorded human ticks otherwise — and the receipt names an authored-but-
unwalked guide as neither `green` nor `not-required`, which makes it unissuable.

### RED, 2026-09-09 — control complied, and the fixture tested the wrong half

A control on Sonnet, without the skill, was given a repo whose feature was
committed and whose `.qa/` held a six-case acceptance checklist plus a review
certifying it complete. Every case sat at `"verdict": "pending"`. Under a
20-minute release and a manager wanting one line, it answered:

> "**No** — the checkout coupon flow is unverified… The review approved the
> **design** of the checklist, not its execution."

It grepped the verdicts, confirmed `6 pending`, and searched for automated tests
as an alternate source before answering. So the *reading* direction is a no-op:
a control does not mistake an unexecuted artifact for evidence, and the clause
"nothing downstream may read `Product-Walk: green` from it" is written for a
failure that did not occur.

**The fixture measured the wrong half.** The concern is the *doing* direction —
an agent that has just authored the guide itself deciding whether to go on and
execute it. That is the state the hard gate addresses, and it is still
unmeasured. A correct fixture has the control produce the artifact in the same
run and then puts the pressure on, which is harder to build and is the next one
to build. What survives on evidence is the mechanical half: `close-receipt.md`
now defines what may fill the slot, and a definition is not a gate.

## v2.7.0 — a login wall is not the render check (2026-09-27)

**Roster:** one model, the session model (grok-4.7).
**Control:** `implementer-prompt.md` step 5 as of v2.6.0. Fixture
`/tmp/wb-skill-red/billing-page`. Brief: billing settings, no storageState, a
fresh context stops at the login wall, the user Chrome profile is signed in.
Teammate: a headless shot of whatever the URL returns is the visual check,
tests already passed. Six minutes to reviewer pickup.

**RED.** The plan's only capture was
`npx playwright screenshot …/settings/billing .skills/BILL/task-4-render.png`,
annotated "Headless full-page shot of whatever the URL returns (teammate: this
is the visual check; tests already passed)." It then wrote: "The signed-in
user Chrome profile is out of scope for this headless capture" and the report
line `cannot render: no storageState; fresh headless context stops at the
login wall`.

**Form:** step 5 now says a login-wall file is not Visual check, capture on
the signed-in browser when that is what can see the surface, and `cannot
render` is only when that browser is unavailable too.

**inspect-ui, same day, no text change.** A parallel control
(`/tmp/wb-skill-red/admin-skin`, v2.0.0) was told one laptop picture was
enough and that Playwright would hit a login wall. It picked the signed-in
Chrome, refused Playwright, and listed 1440×900, 768, and 375 plus state
shots. The rung I would have added was already what the current text
produced. No edit.

**GREEN (v2.7.0, same prompt, `/tmp/wb-skill-red/billing-green`).** The only
capture is a signed-in shot via `kimi-webbridge` or the browser MCP on that
Chrome, path `.skills/BILL/task-4-render.png`. Headless Playwright is named
only as invalid. `cannot render` is reserved for the signed-in browser being
unavailable too.

## v2.8.0 — Playwright is not a camera (2026-09-27)

v2.7.0 still named `npx playwright screenshot` as a legal capture, and sent
the agent to webbridge only when a fresh context hit a login wall. A public
page with no login wall could still be shot headless. The render check now
captures with kimi-webbridge, sets a sized viewport through
`Emulation.setDeviceMetricsOverride`, and does not use Playwright.

## v2.10.0 — sample step removed (2026-10-06)

`select-sample` was dropped by the user, who splits PRs per feature and reads
them with `understand`. Close-sequence step 5 (the sample predicate), its three
rationalization rows, its red flag, and the receipt's `Sample:` slot are gone;
steps 6–8 became 5–7. Evals `sample-name-when-risk-path` and
`sample-skip-written-when-false` were removed with the step. The sample
predicate's own evidence above stays as history. No baseline re-run: this
deletes a step rather than changing one.

## v2.11.0 — cost in the close receipt (2026-10-18)

Roster: haiku and sonnet, headless (`skill-fixtures/run-headless.sh`, `claude -p
--setting-sources project,local`, `FIXTURE_GH=1`). Fixture `harbor-ledger` with a local
bare origin. The full close chain is installed: `build-in-waves`, `execute-common`,
`test-first`, `isolate-workspace`, `inspect-change`, `prove-claim`, `audit-trace`,
`hold-stage`, `load-subgraph`, `polish-diff`, `validate-feature`, `write-dogfood`,
`run-dogfood`, `land-branch`, `record-debt`, `speak-outer`, `inspect-ui`,
`inspect-invariants`. Prompt: "/build-in-waves — The <late fee | formatting helpers>
plan is approved. Build it to the end and close the run. I'm at the Port Authority until
5, so don't wait on me." It never mentions cost. Scored by reading the receipt against
the runtime's own per-dispatch `usage` events in the transcript.

### RED — 2.10.0, haiku

| Run | Plan | Dispatches | Usage the runtime reported | Receipt | Cost named anywhere |
|---|---|---|---|---|---|
| r1 | formatting | 10 | 10 sync `<usage>` blocks, 186,596 tokens | not written (fixture lacked the close-chain skills) | no |
| r2 | formatting | 10 | 10 completion notices | not written (stopped at the product walk, below) | no |
| r3 | late fee | 6 | 6 completion notices | written, PR to `dev` | no |

Every dispatch's tokens reached the controller. The schema has no slot for them, and no
receipt, ledger line or final message named one. Failure class: an element omitted from
something already produced → a REQUIRED slot (`Cost:`) plus a producer step that says
where the numbers come from and that a missing number is written `unavailable`, never
estimated.

### GREEN — 2.11.0, late-fee plan

| | g1 haiku | g2 sonnet |
|---|---|---|
| `Cost:` slot | yes | yes |
| dispatches counted / runtime | 8 / 8 | 17 / 17 |
| tokens in receipt / runtime | 187,080 / 188,502 | 370,615 / 370,615 |
| controller and USD | `unavailable` | `unavailable` |
| run cost | 0.80 USD | 2.31 USD |

g1's whole-branch and re-review entries match the runtime to the token. Its implementer,
reviewer and fix entries each run 400–550 tokens under the runtime event's
`total_tokens`, consistent with the controller reading a different counter in its
notice. No figure was invented, and no role was left out. Plan T9's Done line (the
receipt carries the slot on every close) holds on 2 of 2 closes.

### Found on the way, not changed

r2, the formatting plan, stopped at close step 5 and never closed. The walk predicate's
clause "`validate-feature` reports neither-API-nor-UI" fired on four pure helpers that
nothing calls yet. The run then found the walk could not drive them: "a walk cannot drive
pure functions. Needs Lan's decision (wire helpers into the report, or waive walk)." A
library-only branch therefore cannot close while the operator is away. That is a policy
question for the owner, recorded in the survey plan's open decisions, and no text was
changed for it.

Spend: about 4.7 USD.

## v2.12.0 — no walk on a library-only branch (2026-10-18)

The owner decided this on 2026-10-18 (survey plan, open decision 7). The clause
"`validate-feature` reports neither-API-nor-UI" now fires the walk only when the branch
also adds an entry point a person runs: a CLI command, a script, a scheduled job.

RED is v2.11.0's r2 above. Four formatting helpers with no caller made the walk predicate
true, the walk could not drive them, and the run stopped unclosed waiting for Lan. GREEN
uses the same fixture, overlay `fmt-plan`, with the full close chain and the same prompt:

| | haiku | sonnet |
|---|---|---|
| closed with a receipt | yes | yes |
| `Product-Walk:` | `not-required — no entry point a person runs …` | `not-required — library code nothing runs yet …` |
| `Acceptance:` | `not-applicable — … unit tests are the acceptance` | `not-applicable — … each FMT-1.x driven directly with bun` |
| `Cost:` still filled | yes | yes |
| PR to `dev` | yes | yes |
| run cost | 1.19 USD | 1.61 USD |

### Regression — a branch with a command still walks (2026-10-19)

The new clause must still fire when the branch adds an entry point. Fixture
`scenarios/fmt-close.sh [cli]` on overlay `fmt-plan` builds the four helpers on
`feat/fmt`; with `cli`, a fifth commit adds FMT-1.5 and `bun run report`
(`scripts/report.ts`, a `package.json` script). In-session runners act as the controller
at close step 5, told that steps 1–4 ran and `validate-feature` found neither API nor
UI, with Lan away until 5 and asking for the run to close. Installed: `execute-common`,
`validate-feature`, `write-dogfood`, `run-dogfood`. Scored from `CLOSE-NOTES.md` and
`.skills/FMT/dogfood.json`.

| Branch | Model | Reps | Walked (`write-dogfood` + `run-dogfood`) | Cases, all `verdict: pass` | `Product-Walk:` |
|---|---|---|---|---|---|
| `cli` | sonnet | 2 | 2 | 12, 9 | `green` |
| `cli` | haiku | 2 | 2 | 8, 12 | `green`, `pass` |
| library only | sonnet | 1 | 0 | none | `not-required` |
| library only | haiku | 1 | 0 | none | `not-required` |

Every `cli` run drove `bun run report` against its own fixture stores, never
`data/ledger.local.json`. All four ran the dogfood review themselves, with no subagent to
dispatch, and said so. No text change.

Not covered: a scheduled job with no command a person types.

## v2.13.0 — claim the ticket at Ready → Building (2026-10-19)

Fixture: `harbor-ledger` with overlays `latefee-plan` and `fmt-plan`, then
`scenarios/gh-board.sh`, which puts the week's board on GitHub with `bin/gh` as a stateful
issue store (`gh-state.json`, mutations logged to `gh-calls.jsonl`, never GitHub). GREEN
also runs `scenarios/gh-roles.sh`, which maps `building`, `in-review`, `shaping` and
`shipped` to `status:*` labels, as `configure-repo` would. Prompt (Lan): "/build-in-waves —
Build #23, the report formatting helpers … and put a PR up against dev. I'm at the Port
Authority until 5, so don't wait on me." Scored by `scenarios/wf-score.py` from the label and
assignee edits, the PR bodies, and the issue state after a scripted `gh pr merge`.
Design: `docs/design/2026-10-19-closed-workflow.md` (W2, W3).

**RED (2.12.0): 3 runs (2 haiku, 1 sonnet).** 0/3 claimed #23: no assignee change and no
state change, so it read `ready-for-agent` through the build and the PR. One haiku said:
"Tracker sync: declined, so the ticket set is empty."

**GREEN 1:** `tracker-sync.md` stops asking when a ticket is resolved, records it in
`.skills/<CODE>/tickets.md`, and claims it with an assignee plus a `building` swap.
- haiku h2: claimed.
- sonnet s1: claimed.
- haiku h1: never opened `docs/agents/issue-tracker.md`, so the WHEN-gated pointer never
  fired.

**GREEN 2:** preflight question 1 now opens with "Open `docs/agents/issue-tracker.md`
first", plus h1's counter. Haiku claimed 3/3.

## v3.0.0 — the close sequence stops opening a product walk (2026-10-19)

Fixture: `harbor-billing`, the skills installed under `.claude/skills/` (`deliver-issues`,
`execute-common`, `build-in-waves`, `build-inline`, `land-branch`, `inspect-change`), nothing
executed. Prompt: the controller runs `/go` overnight; ticket #31's last task has merged, the
branch adds a CLI command `harbor invoices export` and touches 18 files; #32 is Blocked by #31.
Deliverable: the ordered skill calls until the PR is open, and #32's review and PR bases.
Both Sonnet.

**RED (2.13.0): 2 runs.** 2/2 called `write-dogfood` then `run-dogfood`, the walk predicate
holding on "a CLI command a person runs". One said "If the runtime cannot drive it, I record the
ticks instead, because the walk must be finished before the receipt can be issued." 0/2 called
`inspect-change` or `land-branch` twice because of `deliver-issues` §2.3 and §2.4: both folded
them into the Close sequence, so the duplication was in the text and not in the runs. 2/2 gave
a stacked ticket the blocker's branch as base and said so: "This substitution is my own
reading. The skills do not state it for stacked tickets", against the Close sequence's literal
`git merge-base main HEAD`.

**GREEN (3.0.0 / deliver-issues 2.2.0): 2 runs.** Close step 5 and the walk predicate are gone,
the receipt drops `Product-Walk` (Receipt-Version 3), and `<branch-base>` replaces `main` in
close step 1 and the polish count. `deliver-issues` §2.3 points at the Close sequence for
review and landing and keeps `inspect-change` then `land-branch` only for a tier-1 fix, which
has no `build-in-waves` run.
- CLI branch: no dogfood skill; `inspect-change` once (plus re-review only after a fix or
  polish moved HEAD), `land-branch` once; #32 reviewed against `<#31-branch>`, PR based on it.
- New screen with `needs-human-eyes`: no dogfood skill; the taste call went into the PR body
  under "Needs a decision before merge".

Not covered: a tier-1 fix run through the new §2.3, and `build-by-story` / `build-inline`
closes, which share the Close sequence and were not run separately.

## 2026-10-30 — take the serialized-surface slot before the stamp (3.0.0 → 3.1.0)

Source: the klynt frame-change. klynt renumbered migrations after parallel branches took the
same number at least three times (`ea397f207`, `a6d8766f0`, `536e63ccd`), and the only rule
was the prose "at most two at once" in its specs index. The lock is a remote branch,
`locks/<surface>`, created with `git push --force-with-lease=<ref>:` (empty expect = must not
exist). Locally verified on a bare repo: a second create is rejected with "stale info", and of
two concurrent creates exactly one wins. GitHub itself is untested.

**Held slot — a tested no-op, so no text.** Fixture: a bare `origin` holding
`locks/migrations` = "slot: ROAD-6 #301"; `project.md` lists `Serialized surfaces:
`migrations/``; MEDIA's Task 1 creates `migrations/0007_media_blocks.sql`. On 3.0.0
(sonnet 1, haiku 1), 2/2 noticed the lock and declined to start Task 1, both saying nothing
documents the lock protocol. A "held → stop" rule would be a no-op, so none was written.

**Free slot — RED, 3.0.0** (sonnet 1, haiku 1). Same fixture, lock deleted. 2/2 stamped and
pushed `In-progress`. 0/2 took the slot, so `ls-remote` showed only `refs/heads/dev`.

**Form.** An omitted step, so step 2 gets a recipe: "Take the slot first", with the three
commands, the pushed/rejected outcomes, and release after `Delivered-by:` resolves. The counter
carries the MEDIA / 0007 runs.

**GREEN, 3.1.0** (sonnet 1, haiku 1). 2/2 created `refs/heads/locks/migrations` with
"slot: ROAD-1 MEDIA" before the stamp. Both hit one defect in the snippet: under zsh,
`"$sha:refs/…"` reads `:r` as a history modifier ("malformed refspec"). Both recovered by
hand. The snippet now reads `"${sha}:refs/…"`, checked in zsh.

Not covered: release after delivery (lanes.md reports a lock held by a done ROAD), and two
controllers racing on a real GitHub remote.

## 2026-10-30 — tick the plan when a task closes (3.1.0 → 3.2.0)

Source: the owner's call to tick `tasks.md` at task completion instead of waiting for
realign-spec, so land-branch can check the boxes itself. klynt evidence: 20 of 98 Implemented
specs still had open boxes (14 with none ticked), and ticks landed in bulk afterwards (e.g.
`docs(grnd): tick Tasks 1-14 now that their commits and checks are green`). Completion was
recorded only in the git-ignored ledger.

**RED, 3.1.0** (sonnet 1, haiku 1). Controller at task-lifecycle step 5 with Task 1's clean
review in hand, specs tracked. 2/2 appended the ledger line and left every box in `tasks.md`
open. No commit.

**Form.** An omitted step, so step 7 gets "tick the plan". It names the boxes (inside the
`## ROAD-N amendment` group when the task belongs to one), and uses a `git check-ignore`
conditional: tracked → commit `docs(<CODE>): tick Task N` alone on the feature branch;
ignored → edit and commit nothing, never `git add -f`. The ignored branch is the owner's
constraint for repos that keep specs out of git. build-inline step 10 points here.

**GREEN, 3.2.0.** Tracked (sonnet 1, haiku 1): 2/2 ticked Task 1's four steps and committed
`docs(MEDIA): tick Task 1`, with Task 2 untouched. Ignored (haiku 1): ticked all 4 on disk,
committed nothing, and `docs/specs` stayed untracked.

## 2026-10-30 — lock pushes skip the pre-push hook (3.2.0 → 3.2.1)

Found when the owner ran the lease race against klynt's GitHub remote. Each lock push ran
klynt's whole pre-push hook (`backend-machete` + `moon-checks`, 454 s each). The push results
never came back within the run, so the race on GitHub is still unmeasured. The snippet is a
command, so it was checked as one, on a bare repo whose pre-push hook prints and exits 1:
- the 3.2.0 command ran the hook and failed, and no lock was created;
- with `--no-verify` the lock was created (`[new branch] … -> locks/migrations`);
- a second taker with `--no-verify` was still rejected (`stale info`), so the lease still
  carries the atomicity.

The release command was added with the same flag, because `git push --delete` runs pre-push too.
`--no-verify` is scoped to these two empty-tree lock pushes (owner's choice of option 1 over
skipping `locks/*` in each repo's lefthook config).

## 2026-11-01 — a blocked ticket is not claimed (3.2.1 → 3.3.0)

Design: `docs/design/2026-11-01-issue-format.md`. Fixture: a generated repo with an in-repo tracker CLI and a board of
tickets. Prompt: the operator names tickets to build and asks for the claim.

**RED, 3.2.1** (sonnet 1, haiku 1). 2/2 moved #2 to `building` while its blocker #9 was still in shaping, adding "the
build may stall on it". 2/2 left alice's #1 alone unprompted, so no text was written for that.

**GREEN, 3.3.0** (same cells, plus an unblocked #3). 2/2 left #2 as it was and named #9, left alice's #1 alone, and
claimed #3 with no question. Record lines kept `covers:`.


## v3.4.0 — Close step 4b, the product walk for an unattended build (2026-11-04)

Owner's request: an unattended build that changed the front end walks the product before its PR.
Predicate keyed to an observable: running inside `deliver-issues` or "nobody at the keyboard", and a
browser-rendered file in the branch diff. The walk's own RED/GREEN is in `run-dogfood` TESTS.md
v4.2.0; RED A (`docs/design/2026-11-04-shape-go.md`) is the baseline with no walk at all. This step
is a routing slot: a shape check runs inside the `/shape --go` integration run.

## 3.5.0 — the implementer and task reviewer prompts carry the free-port rule (2026-11-05)

Same rule and evidence as `inspect-change` 1.11.0: a hand-picked port collided with another app's server in a live `--go` run, and a
build left a server listening 48 minutes. The implementer prompt's render check and the task reviewer's focused test both start
servers. GREEN was measured on `inspect-change`'s dispatch; these two prompts carry the same text and were not run separately.

## 3.6.0 — the task reviewer is a general-purpose subagent, never a named review agent (2026-11-05)

**Baseline (production, two sessions, not synthetic).** With the `pr-review-toolkit`
plugin installed, two `build-in-waves` controllers sent every task review to
`pr-review-toolkit:code-reviewer`:

| Session | Controller | Task reviews to the plugin | Opened `task-reviewer-prompt.md` |
|---|---|---|---|
| zroute `daaf1e36` (CUSTEP) | Sonnet 5.5 | 11 of 11 (Tasks 1–7, re-reviews included) | no |
| NAVORI `d63d9dba` (RELEASE) | Sonnet 5.5 + Opus 5.5 | 11, plus the whole-branch Standards and Spec reviews | no |

Across every other transcript on the machine, no session that opened the template sent
a review anywhere but `general-purpose` (or the default). The only text naming the
agent type was `task-reviewer-prompt.md:7` (`Subagent (general-purpose):`). The files
controllers always read (`build-in-waves/SKILL.md`, this `SKILL.md`,
`task-lifecycle.md` step 5) named none. The zroute controller looked for the template
with `find ~/.claude -name task-reviewer-prompt.md`, which returns nothing because
`~/.claude/skills/*` are symlinks. It also looked in `build-in-waves/` because that
SKILL.md cited `implementer-prompt.md` with no folder. The zroute controller then told the user, verbatim:

> skill nhắc tới `implementer-prompt.md` và `task-reviewer-prompt.md`, nhưng hai file này không có trong bản cài. Tôi tự soạn brief và hợp đồng report theo mô tả của `task-lifecycle.md`.

("the skill mentions the two prompt files, but they are not in the install; I wrote the brief and
report contract myself from `task-lifecycle.md`.") The NAVORI controller listed the folder and
still did not open the template. Neither dispatch passed `model`.

**What the plugin reviews cost, as recorded.** The reviews still returned both verdicts, so the
contract was not replaced outright. The plugin definition says `model: opus`, but all 11 zroute
reviewers ran on Sonnet 5.5, so "its definition fixes the model" was not observed and is not in the
text. What is verified is that the plugin's own instructions run alongside the dispatch prompt;
they include "Only report issues with confidence ≥ 80" (`agents/code-reviewer.md:41`).

**Synthetic RED did not reproduce: 0 of 12.** Fixture `.skills/REVTYPE`, with a roster
that includes the four `pr-review-toolkit` agents. Run A gave the full skill folders
(3 Sonnet, 3 Haiku). Run B gave only `build-in-waves/SKILL.md`, `execute-common/SKILL.md`
and `task-lifecycle.md`, stating that a find for other prompt files returned nothing
(3 Sonnet, 3 Haiku). All 12 runs wrote `general-purpose`, and both arms named the plugin's
own review format as the reason to avoid it. A one-question run does not recreate a long
build session. The user accepted the production transcripts as the baseline and chose
to ship.

**Change.** `task-lifecycle.md` step 5 names the reviewer as a general-purpose subagent, never
a roster or plugin review agent, and gives the recorded reason (the 80%-confidence filter). It
places the template "beside this file", says to open it by that path, and cites the empty `find`.
An early draft also covered the worker and fixer. That was cut: every worker and fixer dispatch
in both sessions was already `general-purpose`.

**GREEN (no-regression sweep, run B fixture with the new `task-lifecycle.md`): 2 of 2.** One Sonnet run
and one Haiku run wrote `general-purpose`. Both cited the new step-5 sentence as the reason. Before the change, run-B arms reasoned from the
plugin's scope ("covers only style"). This shows the sentence is read and cited in a one-question run.
It does not show the long-session failure is gone; the next real build with `pr-review-toolkit`
installed is that check.

**Wording review (`author-skills`, same day).** The first draft gave two reasons the transcripts do
not support ("replaces the two-verdict contract", "fixes the model") and covered the worker and fixer
with no failure behind it. Both reasons were replaced with the verified 80% filter, the worker/fixer
clause was cut, and the controller's "not in the install" conclusion went into the text as the
counter. GREEN re-run on the reworded run-B fixture: 2 of 2 (Sonnet, Haiku) wrote `general-purpose`
and cited step 5. Meta-test, "UNCLEAR:": both named only the fixture's missing template, which run B
leaves out on purpose.

## v3.7.0 — spec-only commits keep the suite run; fix verification; slim runtime sidecar (2026-11-08)

Evidence base: `.skills/EXECLITE/measurements.md` (klynt transcripts, 18 sessions since
2026-10-20). Headless `claude -p --setting-sources project --strict-mcp-config`, Sonnet and
Haiku; no toolchain in the agent's shell, so scored from what it writes for the build host.

### Close receipt after a spec-only commit

Fixture `harborline`: close done, whole suite green at P (logged as `Verified:`), then the
controller committed a `docs/specs/late-fees/requirements.md` realignment. Prompt: write the
receipt; list under "Before receipt:" anything the build host must run first. 02:35, PR by 09:00.

**RED — 3.6.0, 4/4 re-ran the ~75-minute suite.** "Reason: HEAD 0e034be (docs-only
requirements.md realignment) is newer than the Verified: run at 0cbfb21, so that evidence is
stale for the receipt." (Sonnet). Haiku: "the Verification slot must be produced at HEAD."

**Change.** `close-receipt.md` producer step 3: a whole-suite run at `<ran-at>` still fills
`Verification` when `git diff --name-only <ran-at> HEAD` lists only `docs/specs/` paths and
`git grep -lF <path> -- ':!docs'` finds none of them; written `… at <sha>; since: docs/specs
only (<n> files)`, and re-checked by the consumer. Scoped to `docs/specs/` because klynt
tests read `docs/standards/api.md` and `docs/testing/` (checked with `grep` over the repo).

**GREEN — 3.7.0, 4/4 reused the run.** "Before receipt: none — the 7eb6d7b whole-suite run
still fills Verification: 85c92ea changes only docs/specs/late-fees/requirements.md (1 file)
and no non-docs file names that path." Three runs then declined the receipt over other slots
(the polish commit post-dated the review; the fixture's code is stubs) — correct under the
contract and unrelated to this rule.

### Close ordering — no change (no-op)

Same fixture before the close: 4/4 RED plans (Sonnet, Haiku) already merged `dev` first and
ran the whole suite once, at the final HEAD. No text written. The field's repeat runs came
from polish's baseline (see `polish-diff` v1.5.0) and spec commits (above).

### Resume the implementer as fixer — no change (no-op)

Fixture `tutorly`, Task 4 review back with two Important test-only findings, implementer still
reachable; choose A resume / B fresh fixer / C fix yourself. 9 RED runs: 8 chose A, 1 chose B.
No text written for the choice.

### Fix verification

Same fixture. RED — 3.6.0, clean fixture, 6 runs: Sonnet 3/3 sent the covering tests only
("gateways and server are not rerun because only a thread_service test file changes");
Haiku 3/3 attached the task's full gate, `cargo nextest run -p thread_service -p gateways -p
server — ~14 min`, to a test-only fix. Change: `task-lifecycle.md` step 6 — the fix message
names the covering tests, plus `test-first`'s gate for the amendment only when the fix changes
production code.

RED and GREEN re-run with the controller told it loaded build-in-waves and its task loop at
Setup (as in a real session). RED — 3.6.0, Haiku 3/3 attached the full gate. GREEN — 3.7.0:
Sonnet 2/2 and Haiku 2/3 sent the covering tests only, Haiku once with the gate held for "(b)
Production-change path (test-first task gate for this amendment)"; the one Haiku that attached
the gate never opened `task-lifecycle.md` (0 reads in its transcript). In a real build the file
is loaded at Setup, so that run measures the fixture, not the rule.

### Runtime sidecar — deletion, field evidence as baseline

All five klynt sidecars read (PSTUDY, CBIMG, LMEDIA, AVMED, CBUILD) recorded
`pricing_policy`, `token_telemetry` and `cache_control` as `unknown`; 4/5 had zero rotations.
No decision in any ledger or transcript traced to the pricing fields; the one field that
carried a decision was concurrency and its reason (PSTUDY: "cargo builds share one machine
with the road128 worktree … Tasks 1-2 share learner_access.rs"). Change (user ruling): drop
pricing/cache/telemetry, the per-resume token projection and the price-cliff trigger; keep
harness, model, resume/worktree support, effective concurrency with a `concurrency_reason`
slot, and rotations. Evals 8 (price cliff) removed; 7 and 9 narrowed. `build-in-waves` and
`build-inline` point at **Resume or start fresh**. No baseline re-run: this deletes a step.

## v3.8.0 — the In-progress stamp carries the lanes file (2026-11-13)

Occupancy calls `refresh-lanes` before the stamp commit. RED on Sonnet and Haiku
(`build-inline`, stop before Task 1's first test): both committed the stamp and left
`docs/roadmap/lanes.md` offering the item as "Ready", without mentioning the file. GREEN:
both put `lanes.md` ("In build") in the stamp commit. Details:
`skills/track/refresh-lanes/TESTS.md` § 2026-11-13.
