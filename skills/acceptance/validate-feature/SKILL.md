---
name: validate-feature
version: 1.5.0
description: "Use before merging or finishing a branch, when a feature's unit tests are green but its user-facing behavior has not been driven through the running system as a real client, API or browser. Produces an acceptance pass over the happy paths and edge cases, with a regression test for each defect. Also when the repo has no documented way to run the app locally."
---

# Validate Feature

Green unit tests prove that the assertions someone wrote pass. They do not prove
the feature works. The gap between the two — an API that returns `201` where the
client reads `200`, a checkbox that flips in memory but never reaches the store,
a form that clears on a failed submit — is where features ship broken. This
skill closes it: drive the **running** system, not the test suite.

Run this after `inspect-change`, before `land-branch`.

**Cold-start control.** IF `docs/agents/verify.md` exists, Launch and Doctor
from that file before any checklist item (it owns how a later agent boots this
app). Drive each item with its Feature section when one matches; Evidence must
include the persist/reload check that file names. IF it is missing, continue
from `project.md` **Run locally (dev)** as today, and **name** `/configure-repo`
once so the user can generate the recipe (Decision M) — do not invoke it.

**When another session built the branch.** Your brief may say that a different session built
the branch and that your result goes back to it, as `/shape --go`'s acceptance from the card
does. In that case, change no file in the repo: no fix, no test, no commit. Every fix this skill
or its files would make becomes a finding in your result instead, giving the Example or probe,
the request sent and what came back. The build session fixes the findings. One such run
committed six fixes from outside the build. Another left an untracked test file and had its
edits to `src/` refused.

## 1. Derive the acceptance checklist from the spec

Read the feature's `requirements.md`, `design.md`, and `tasks.md`. For every
requirement describing user-observable behavior, list its concrete checks — the
happy path AND each edge/error criterion — keyed to the requirement ID. The spec
is the source: a behavior nobody hand-fed you is still on the hook, and an
untraced one is a gap to raise, not to skip.

Write the checklist to `.skills/<CODE>/acceptance.md` (a working ledger,
git-ignored) and create one todo per item. Heavy reading? Dispatch a scan
subagent to map the touched surface and digest it to the ledger; keep this
context lean. *Done when: every user-facing requirement ID has at least one
concrete, observable check with an expected result.*

### Product context docs (optional)

**Applicability:** acceptance criteria touch personas or measurable success outcomes.  
**Load:** `skills/project/define-project/consult-recipe.md`.  
**Paths:** `docs/product/personas.md`, `metrics.md`, `principles.md`.

**When Approved:** fold relevant constraints into checklist expectations (advisory;
requirements remain normative). **When absent:** CONTINUE; suggest once
`/define-project product/personas|metrics|principles` only if the gap makes
acceptance materially clearer; never auto-invoke.

## 2. Dispatch by surface

The checklist splits by where each behavior lives. Run whichever apply — most
features need both:

- The change exposes an HTTP/RPC API a client calls →
  **REQUIRED: read `api.md` beside this file and follow it**.
- The change has a frontend a user drives →
  **REQUIRED: read `ui.md` beside this file and follow it**. Its §2 picks the browser.
  It does not install a browser harness. **The exception is when your caller says the build's
  product walk drives this branch's browser surface next.** The walk is `write-dogfood`, then
  `run-dogfood`, and build's Close step 4b runs it inside `go` or when nobody is at the keyboard.
  In that case the walk owns the browser. Skip `ui.md`, and write
  `UI: the product walk drives it next` in the ledger. Two baseline close runs drove `/book` in
  `agent-browser` with that walk queued behind them.
- The behavior is neither an API nor a UI (a CLI, a library, a batch/cron job) →
  drive it directly against the running system yourself, record each observed
  result in the ledger, and promote the passing checks into committed tests
  that describe the domain behavior (docs-only spine — no requirement-ID tags
  required in test files). For human-eyeball qualities (visuals, feel) hand
  off to `write-dogfood`.
- The change adds or changes anything a client, command or job calls (an API, a CLI, a
  job, a library entry point) → after its checklist, **REQUIRED: read `system.md`
  beside this file and run it**.

Hand each child its slice of the ledger by path; it writes results back to the
same file.

## 3. Close the loop

Report the checklist with each item's observed result. Any item you could not
exercise is an open risk — name it; do not let it pass silently. Then hand back
to `land-branch`. The UI acceptance evidence is `.skills/<CODE>/validate-feature.md`
from the browser drive. A product defect still gets its regression in the
repo's existing test stack. *Done when: every checklist item is observed green
against the running system, each failure fixed with a regression test in that
existing stack, and the UI drive record is on disk, or the ledger names the product walk
that drives the UI next.*
