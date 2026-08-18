# `build-in-waves` / implementer-prompt — deviation log

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
