---
name: acceptance-check
description: Use before merging or finishing a branch, when a feature's unit tests are
  green but its user-facing behavior has not been driven through the running
  system as a real client — the acceptance / end-to-end pass over the happy
  paths and edge cases that pass in isolation yet break in practice.
  Orchestrates API- and UI-surface validation and leaves committed tests
  behind, unlike a manual dogfooding pass. Also when the repo has no
  documented way to run the app locally.
---

# Acceptance Check

Green unit tests prove that the assertions someone wrote pass. They do not prove
the feature works. The gap between the two — an API that returns `201` where the
client reads `200`, a checkbox that flips in memory but never reaches the store,
a form that clears on a failed submit — is where features ship broken. This
skill closes it: derive the user-facing behaviors from the spec, drive the
**running** system through every one as a real user would, fix what breaks, and
leave behind a repeatable harness so the next run is cheap.

Run this after `code-review`, before `finish-branch`.

## 1. Derive the acceptance checklist from the spec

Read the feature's `requirements.md`, `design.md`, and `tasks.md`. For every
requirement describing user-observable behavior, list its concrete checks — the
happy path AND each edge/error criterion — keyed to the requirement ID. The spec
is the source: a behavior nobody hand-fed you is still on the hook, and an
untraced one is a gap to raise, not to skip.

Write the checklist to `.skills/<feature>-acceptance.md` (a working ledger,
git-ignored) and create one todo per item. Heavy reading? Dispatch a scan
subagent to map the touched surface and digest it to the ledger; keep this
context lean. *Done when: every user-facing requirement ID has at least one
concrete, observable check with an expected result.*

## 2. Dispatch by surface

The checklist splits by where each behavior lives. Run whichever apply — most
features need both:

- The change exposes an HTTP/RPC API a client calls →
  **REQUIRED SUB-SKILL: use `acceptance-api`**.
- The change has a frontend a user drives →
  **REQUIRED SUB-SKILL: use `acceptance-ui`**.
- The behavior is neither an API nor a UI (a CLI, a library, a batch/cron job) →
  drive it directly against the running system yourself, record each observed
  result in the ledger, and promote the passing checks into committed, ID-tagged
  tests. For human-eyeball qualities (visuals, feel) hand off to `dogfood`.

Each child locates (and persists) how to run its surface, exercises its slice of
the checklist against the live system, fixes failures through `debug`, and
promotes the passing checks into committed, ID-tagged tests. Hand each child its
slice of the ledger by path; it writes results back to the same file.

## 3. Close the loop

Report the checklist with each item's observed result. Any item you could not
exercise is an open risk — name it; do not let it pass silently. Then hand back
to `finish-branch`. *Done when: every checklist item is observed green against
the running system, each failure fixed with a regression test, and the durable
tests committed and tagged so `finish-branch`'s verify gate keeps enforcing
them.*
