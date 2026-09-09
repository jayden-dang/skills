# `land-branch` — merge of `package-change` (v2.0.0)

## Edit — In-progress close-loop (v3.2.0)

§8 Status table treats `In-progress` like `Approved` (realign when evidence
holds; report when partial). Occupancy writer is `execute-common` kickoff,
not this close. Evidence:
`skills/execution/execute-common/TESTS.md` § catalog occupancy.

---


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

## Edit — cleanup parent is `.worktrees/` (v3.1.0)

**RED (v3.0.0):** §7 removed only trees under `.isolate-workspace/` or
`isolate-workspace/`, so a `.worktrees/` isolation tree could not be cleaned.

**GREEN:** cleanup provenance is `.worktrees/` or `worktrees/`, plus leftover
legacy `.isolate-workspace/` / `isolate-workspace/` trees so an old parent can
still be removed. Harness-owned workspaces stay untouched.

## Stale receipt after a rewrite — proposed rule, dropped (2026-09-07)

**Proposal.** Add a rule that a rewritten head voids a receipt, with a
rationalization table countering "only the base moved", "CI is green at the new
head", "a rebase is mechanical", and "re-verifying costs more time than we have".
Imported from a reading of another skill set, which carries that rule explicitly.

**Method.** Real fixture, 3 reps, Sonnet, fresh context, three isolated copies in
random parents. A `payments-gateway` repo with the pack installed at
`.claude/skills/`, a receipt at `.skills/PAY/close-receipt.md` claiming
`Head-SHA: 15a34fc`, actual `HEAD` at `12713fb`, suite green 3/3, and a prompt
stacking a 15-minute release cut, a green build twenty minutes old, a reviewer
who signed off yesterday and is now unreachable, and explicit intent to merge.
Neither the proposed rule nor its vocabulary appeared in the prompt.

**Result: 3 of 3 compliant. Nothing to fix.** Every rep ran the consumer
validation, compared `git rev-parse HEAD` against the receipt, refused to consume
it, and re-established evidence on the current revision before deciding. Two then
merged on fresh green; one withheld. That divergence is a judgment call about
whether unwired code blocks a merge, not a gate failure — the gate itself held in
all three.

The pressure the proposal existed to counter was rejected unprompted:

> regardless of the out-of-band claims that the suite was "3 of 3" and "green 20
> minutes ago" and that Priya reviewed it. None of that was evidence bound to the
> current revision

and one rep extended the same logic to the reviewer without being asked:

> Priya's review yesterday was against the pre-rebase tree and can't stand in for
> that, since her sign-off predates the commit in question by the same stale-SHA
> logic that invalidated the receipt.

**Why it held.** `close-receipt.md`'s consumer validation is already the
deterministic form: named `git` commands, anchored `grep -c` counts, and a fixed
rule on the output. There is nothing in it to negotiate with, so none of the three
negotiated. Prose stating the same rule would have been the weaker form of a
defence that already exists.

**Fixture limit, recorded rather than hidden.** The prompt said the branch had
been rebased overnight, but the history shows only two bookkeeping commits after
the receipt and no application-code drift. One rep noticed and used it to justify
a fast re-verification. A fixture with real code changing after the receipt would
press harder on the fallback's depth. It would not change this result: the
load-bearing question was whether a stale receipt gets consumed under pressure,
and it did not, three times out of three.


## v4.0.0 — sequencing replaces the never-rewrite prohibition (2026-09-09)

**User decision, not a measurement.** The user directed `land-branch` to adopt
`principle-sequence-verifiable-units` and `opening-a-pr` from a second skill set,
having stated that nearly every PR in their work is agent-authored. This entry
records what changed, what justified the *form*, and what remains unmeasured.

**What the existing evidence actually said.** The RED above records
`S3 squash history` as a **non-failure**: grok-4.6 "already did intended; refused
squash" and grok-4.5 "refused squash", and the summary line reads *"Non-failure
(keep): nobody picked skip-verify / skip-menu / squash."* One recorded
rationalization is *"The user explicitly said 'Squash those three messy commits,'
so the never-rewrite hard gate has an exception this session"* — an agent
declining a rewrite the user had asked for.

So the prohibition was never backed by a measured failure, and eval 6 asserted
against one that had not occurred. It is replaced rather than deleted, and
demoted to `contract`.

**Why a recipe, not a lifted prohibition.** Because agents refuse to rewrite even
when told to, removing the prohibition alone would not produce sequenced commits
— it would produce the same branch with one fewer sentence about it. The change
is therefore a positive recipe in `prepare.md` (target shape, anchor, rewrite,
confirm), which is the form `author-skills` prescribes for "complies, but the
output has the wrong shape".

**Two carve-outs are mechanical, not preference.** Execute-family task commits
carry per-task reports, evidence, and two verdicts bound to that commit;
rewriting them severs the verdicts from what they judged. And a rewrite changes
HEAD, which makes any `close-receipt.md` stale by construction — so sequencing
runs before the crossing evidence step, never after.

**Unmeasured.** No RED was run for v4.0.0. The predicted failures worth a fixture
are: rewriting without recording an anchor; rewriting execute-family task commits
because they look untidy; and re-using a receipt whose head the rewrite moved.
Until that runs, eval 6 stays `contract` and this section is the only claim made.

**Also in v4.0.0**, from `opening-a-pr`: PRs open ready and never as drafts; the
reviewer-centred PR fallback in `conventions.md` gains Why / Scope / Tradeoffs /
Blast Radius / Verification, with Verification required to carry outcomes rather
than command names; and opening a PR names `/tend-pr` instead of waiting on CI.


## v4.0.0 addendum — forge, stacks, and the subagent hand-off (2026-09-09)

Three capability gaps, added to `prepare.md` rather than argued for: the forge
is resolved once per session and not mixed; a stack is defined as a base-branch
chain where each child targets its parent branch and is cut from the parent's
exact tip; and a subagent that opens a PR returns the URL to its parent without
starting a check watch.

Unmeasured, and capability-shaped rather than gate-shaped — before this, nothing
in the skill described a child PR's base at all, so an agent asked to split work
into a stack had no definition to follow. The reviewer-quality argument for
splitting is stated once and not repeated; the ordering rule is the part that
carries information a control cannot derive.

The retarget boundary is deliberate: reshaping an **open** chain is `tend-pr`
territory and that skill refuses it, so the bases have to be right at creation.

**Dangling reference fixed while verifying the wiring.** `prepare.md` said the
PR title takes "the resolved PR-title shape", but the convention record carries
only `commit_subject_form`, `commit_subject_grade`, `pr_structure` and
`pr_structure_grade` — there is no title shape in it. The line degraded safely
via its own "or a plain imperative summary" clause, so nothing broke, but it
named a field that does not exist. Resolved against an existing field instead of
adding a fifth: where the repo squash-merges the PR title becomes the commit
subject and takes `commit_subject_form`, otherwise it is a plain imperative
summary.
