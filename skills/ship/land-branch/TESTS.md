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
