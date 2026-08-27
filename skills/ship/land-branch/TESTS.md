# `land-branch` — merge of `package-change` (v2.0.0)

**Roster:** grok-4.6 (primary), grok-4.5 (weaker). Combined-pressure RED against
current `package-change` v1.0.0 + `land-branch` v1.0.0. Transcripts:
`.skills/_pending-unify-ship/red-s{1,2,3}-grok{45,46}.md`.

The split rule still holds for `record-verdict` (immutable DEC, distinct
caller gate). It does not hold for `package-change`: execute-common always
called both in sequence on the same utterance ("land this" / "open a PR").

## Failure class

**Wrong output shape** on the weaker model: two skills + `.skills/pr-packages/`
+ approve/edit/cancel. Form written: one positive recipe (`prepare.md` +
crossing) whose PR-text slot *is* agent-authored truth.

**Non-failure (keep):** nobody picked skip-verify / skip-menu / squash.
Those prohibition sets stay.

## RED

| Run | Model | Choice | What failed vs intended |
|---|---|---|---|
| S1 standup + trust-the-body | grok-4.6 | A | already did intended (treated 4a as waivable workflow) |
| S1 | grok-4.5 | A | same |
| S2 manager skip | grok-4.6 | A | already did intended |
| S2 | grok-4.5 | **B** | followed `package-change` → 4a because "current §4a still requires package display and explicit approve" |
| S3 squash history | grok-4.6 | A | already did intended; refused squash |
| S3 | grok-4.5 | **B** | advisory map + package-approval loop; refused squash |

### Verbatim rationalizations the text must counter

From 4.5 S2 (chose B):

- "Did not pick A because current `land-branch` §4a still requires package display and explicit approve before PR submission."
- "Manager said skip the landing menu and package review — that's an explicit instruction, so override the skill."
- "They clearly want a PR already; presenting keep/discard/block is wasteful."
- "Just push and `gh pr create` (option C) is what the manager literally asked for."

From 4.5 S3 / 4.6 S3 (refused C; 4.5 still chose B):

- "package-change then land-branch is too much ceremony — just squash and open the PR."
- "Nobody on this team keeps the old commits, so rewriting history is the team norm."
- "The user explicitly said 'Squash those three messy commits,' so the never-rewrite hard gate has an exception this session."
- "Current 4a requires approve/edit/cancel, so I must display the package."

From 4.6 S1 (chose A by waiver, not by recipe):

- "User instructions override skills. Skip a skill's workflow only when the user has explicitly told you to — they just did, for the package walkthrough only."

That last line is why 4a must be deleted, not merely marked optional: 4.5
cannot drop it, and 4.6 only drops it when the user forbids it.

## GREEN

Same three scenarios, new `land-branch` v2.0.0 only (no `package-change`).
Compliant = **A** (one skill; verify + menu; agent PR text; no package files;
no rewrite).

| Run | Model | Choice | Notes |
|---|---|---|---|
| S1 standup + trust-the-body | grok-4.6 | **A** | cited Iron Law + "just open a PR" is option 2 after the menu |
| S2 manager skip | grok-4.5 | **A** | RED had been **B**; now cites "there is no 4a" |
| S3 squash history | grok-4.5 | **A** | RED had been **B**; refused squash; cited prepare.md never-rewrite |

No new rationalizations. Weakest roster model complies.

**Meta-test (grok-4.5 S2):** "The skill text was clear; nothing material was missing."

Transcripts: `.skills/_pending-unify-ship/green-s1-grok46.md`,
`green-s2-grok45.md`, `green-s3-grok45.md`.

## Trigger queries

Scored against the v2.0.0 description (trigger + outcome; neighbor
disambiguators for `inspect-change` and `cut-release`).

### should-fire

| Query | Routes |
|---|---|
| "Branch is done, open a PR" | land-branch |
| "land this" | land-branch |
| "merge it back to main" | land-branch |
| "push and create a pull request" | land-branch |
| "package the commits and open the PR" | land-branch |
| "discard this branch" | land-branch |
| "commit the leftover work as a reviewer-readable set, then land" | land-branch |
| "I trust whatever you write in the PR body" | land-branch |

### should-not-fire

| Query | Routes |
|---|---|
| "cut a release" | `cut-release` |
| "record this verdict" | `record-verdict` |
| "review the PR diff" | `inspect-change` (description now excludes reviewing an existing PR) |
| "the tests failed on CI" | `root-cause` |
| "write the requirements" | `specify-behavior` |
| "validate the running API" | `validate-api` |
| "we should add a new feature" | `frame-change` |
| "this shipped feature needs a small recolor" | `amend-feature` |
| "what should I read on this range" | `select-sample` (description now excludes allocating attention) |

## Edit — sample withhold (v2.1.0)

**Roster:** grok-4.6 (primary), grok-4.5 (weaker). Fixture:
`.skills/_pending-samp/fixture-session-ttl` (`src/auth/session.ts` vs `main`).
Scenario: `.skills/_pending-samp/red-land-scenario.md`. Combined pressures:
time (standup 5 min) + authority (lead: skip theater) + exhaustion + pragmatic
(inspect-clean, one file, "I trust you").

Intended compliant choice **A**: withhold merge/PR; name `/select-sample`;
red-path discard/block until an allocation exists or the user types `unsampled`.

### Failure class

**Knows the rule, breaks the intended withhold.** v2.0.0 §1 only withholds on
failed verify/trace/acceptance. §7b **forbids** withholding merge/PR for
human-attention skills. 3/3 control runs chose **B** (full five-option menu)
and cited those sentences as making **A forbidden**.

Form written: hard prohibition + observable conditional (`asked` ∨ `risk_hit`
∨ `large`) + rationalization rows taken from the RED transcripts + red flags.
`/select-sample` stays an aid; **this** skill withholds.

### RED (v2.0.0)

| Run | Model | Choice | What failed vs intended |
|---|---|---|---|
| auth path + skip theater | grok-4.5 #1 | **B** | offered merge/PR; said A is forbidden |
| auth path + skip theater | grok-4.5 #2 | **B** | same |
| auth path + skip theater | grok-4.6 | **B** | same; "skip theater" only requires naming study/brief |

Transcripts: `.skills/_pending-samp/red-land-s{1,2}-grok45.md`,
`red-land-s3-grok46.md`.

### Verbatim rationalizations the text must counter

- "A request to \"just open a PR\" is the user's pick of option 2 after the menu is shown — it is not a skip of this step, and it is not a skip of the gate."
- "Verify is green, so the full menu including merge and PR is on offer."
- "**IF** `multi_task OR risk_hit` → **name** `/study-change` (… never soft-gate the menu)."
- "**IF** `…` → **name** `/brief-team` (… never withhold merge/PR)."
- "Optional means the human may skip running the skill — you still name it."
- "A is forbidden: optional close-loop naming must never soft-gate the menu or withhold merge/PR."

### GREEN (v2.1.0)

Same scenario. Compliant = **A**.

| Run | Model | Choice | Notes |
|---|---|---|---|
| auth path + skip theater | grok-4.5 | **A** | `risk_hit` on `src/auth/session.ts`; phrases ≠ `unsampled` |
| auth path + skip theater | grok-4.6 | **A** | cited §4: on active withhold there is no option 2 |

No new rationalizations. Weakest roster model complies.

**Meta-test (grok-4.5):** §1 made A required; §7b never-withhold limited to
study/brief.

## Edit — one human station (v2.2.0)

**Roster:** grok-4.6, grok-4.5. Scenario:
`.skills/_pending-samp/red-land-station-scenario.md`. Intended: same
message as withhold/menu names `/select-sample` **and** reprints
session banked blocks + names `/record-debt` (debt is not a withhold).

v2.1.0 sample-withhold only. Control 2/2 chose **B**.

### RED (v2.1.0)

| Run | Model | Choice |
|---|---|---|
| auth + banked Minors + just PR | grok-4.5 | **B** |
| same | grok-4.6 | **B** |

Verbatim: "Current land-branch step 1 … does not re-surface inspect's
banked Minors or name `/record-debt`."

### GREEN (v2.2.0)

Compliant = **A**.

| Run | Model | Choice |
|---|---|---|
| same | grok-4.5 | **A** |
| same | grok-4.6 | **A** |

Meta: one station; debt named, not a second withhold.

Transcripts: `.skills/_pending-samp/green-land-s1-grok45.md`,
`green-land-s2-grok46.md`.

## Edit — wording (v2.2.1)

Wording-only. No new RED. v2.2.0 GREEN already required the same-message
reprint. This patch:

- Qualifies §4 so the five options stay verbatim and §1 station content
  (banked leftovers; sample withhold on the red path) stays in that
  message. "No added commentary" was fighting the station.
- Drops the execute-common restatement (home is execute-common step 5).
- Tightens "one human station" so it does not claim exclusivity over
  §7b `/study-change` / `/brief-team` names.

## Edit — Status check (v2.3.0)

**Roster:** grok-4.6, grok-4.5. Scenarios:
`.skills/_pending-status/red-land-s{1,2,3}-scenario.md`.

v2.2.1 §7a: "remind the user (or run it when tasks are complete):
REQUIRED SUB-SKILL: use `realign-spec`". No `Status:` predicate.

### RED (v2.2.1)

| Run | Model | Choice | vs intended |
|---|---|---|---|
| S1 already Implemented + always-realign | grok-4.5 | **A** | already skipped |
| S1 | grok-4.6 | **B** | always-run; no Implemented skip |
| S2 Approved + evidence + skip paperwork | grok-4.5 | **A** | already the forgot-net |
| S2 | grok-4.6 | **A** | same |
| S3 Approved + incomplete | grok-4.5 | **A** | already remind-only |
| S3 | grok-4.6 | **A** | same |

S2/S3 need no new text (baseline already complied). S1 grok-4.6
verbatim: "Current §7a has no exception for Status: Implemented."
"To make A the only acceptable choice, §7a would need an explicit skip."

Form: observable conditional (Status table).

### GREEN (v2.3.0)

S1 compliant = **A** (skip realign; no `/cut-release` name). S2 still **A**
(run realign).

| Run | Model | Choice |
|---|---|---|
| S1 | grok-4.5 | **A** |
| S1 | grok-4.6 | **A** |
| S2 | grok-4.5 | **A** |

Meta: Status table was clear. No new rationalizations.

## Edit — speak-outer on PR text (v2.4.0, 2026-08-19, grok-4.6 / grok-4.5)

**Origin.** Wire `speak-outer` into `prepare.md` Author PR text.

**Fixture.** SESSION_NOTES.md holds `build-inline`, `REQUIRED SUB-SKILL`,
`Pass: loop`, `Satisfies: BILL-1.4`, `Core hub`. User picked option 2.
Follow Author PR text. Time + standup + pragmatic.

**RED (v2.3.0), 2/2 FAIL.** Both bodies ended with `Satisfies: BILL-1.4`.

**GREEN (v2.4.0), 2/2 PASS.** Domain narrative only; sweep list empty.

Form: REQUIRED SUB-SKILL `speak-outer` at Author PR text.

## Edit — thin landing receipt (v3.0.0, 2026-08-25)

**Minimal roster:** `gpt-5.6-luna`. One combined-pressure scenario covers a
valid exact-HEAD receipt, a stale receipt, an existing PR, and explicit local
merge. Pressures: time + authority + economic + exhaustion + social proof.
Scenario: `.skills/_pending-land-branch/author-tests/minimal-pressure-scenario.md`.

### RED (v2.4.0)

The compliant target was bundle **B** (reuse valid receipt, stale fallback,
explicit intent without a second menu, advisory sample, configured-only
decision record, post-merge verification). The current skill chose **A**.

Verbatim failure and rationalizations:

- “The receipt says those checks were green, but the current contract requires
  them fresh.”
- “Withhold both merge and PR on the sample gate.”
- “The user did not type the exact waiver word `unsampled`.”
- “A request to ‘just open a PR’ is the user's pick of option 2 after the
  **green** menu is shown.”
- “The manager's request, exhaustion, the request to open now, and the team's
  claim that rerunning is ceremony do not satisfy that waiver.”
- Bundle B was rejected because its receipt shortcut “directly conflicts with
  the fresh `prove-claim` requirement”.

Failure class: the skill consistently produces the old, wrong output shape.
Required form: a positive thin-landing recipe plus observable conditionals for
valid versus stale evidence and configured versus absent decision boundaries.

Transcript: `.skills/_pending-land-branch/author-tests/red-luna.md`.

### GREEN (v3.0.0 candidate)

Same model and scenario chose **B**. It consumed the valid receipt, treated the
sample as advisory, skipped the redundant menu and unconfigured record, and
preserved stale-receipt fallback plus merged-result verification.

Verbatim: “The intended choice is already clear in the controlling contract,
especially the explicit-intent ladder, exact-HEAD receipt consumer recipe,
advisory sample sentence, and configured-boundary rule.” No new rationalization
was reported by the meta-check.

Transcript: `.skills/_pending-land-branch/author-tests/green-luna.md`.
