# Troubleshooting

Symptoms, causes, and where to look.

## The trace check reports a finding

The trace check is the [`trace`](../concepts/traceability.md) skill: a set of deterministic `grep`/`git` passes over `docs/specs/` and the test tree, each finding decided by a fixed rule. `verify`, `release`, `sync-spec`, and `write-plan`'s coverage check all run it. Two agents running it on the same repo reach the same finding set.

### `E1 task cites unknown requirement SHELL-1.2`

A task footer or a test tag names an ID that no `requirements.md` defines.

Three causes, in descending order of likelihood:

1. **The requirement was retired.** A struck-through ID (`~~**SHELL-1.2**~~`) counts as *undefined* — that is the mechanism working. Something still cites it. Run [`sync-spec`](../skills/sync-spec.md), which lists orphans with a suggested disposition per item. Orphans are decisions, not cleanup: repoint the citation to a live ID, retire the test, or resurrect the requirement.
2. **A typo** in the tag or footer.
3. **The requirements file is outside the spec root.** Check the `specsDir` named in `docs/agents/project.md`.

### `E2 SHELL-1.2 (…, Implemented) has no covering test`

The feature is marked `Implemented` (or `Shipped`) and this requirement's ID string appears in no test file.

This usually means a task footer cited the ID but no *test* was ever tagged with it. [`write-plan`](../skills/write-plan.md) is supposed to catch that at plan time — its coverage check requires every ID to appear in a **test annotation inside some task's steps**, not merely in a footer, precisely because a footer-only citation passes as a W1 warning while `Approved` and fails as an E2 error the moment the status flips.

The fix is to add the test, never to renumber. If the behavior cannot be unit-tested in isolation, tag the e2e test or an existing test that already exercises it — one test may carry several IDs.

A guard or negative requirement counts only if a real test asserts it.

### `E3 duplicate definition of SHELL-1.2`

Two requirements files define the same ID. Usually a feature code was reused, or a criterion was copy-pasted between a feature spec and `docs/specs/fixes.md`. Feature codes are unique repo-wide, forever.

### `W1 SHELL-1.2 (…, Approved) is not cited by any task`

The plan is incomplete. Either add a covering task, or strike the requirement through with a reason.

### `W2 … missing "Status:" line`

The requirements file has no `Status:` or `Feature code:` header. The trace check needs `Status:` to know whether E2 applies.

### The check finds phantom IDs in a fixture file

A test file that legitimately contains ID-shaped example strings that no test asserts. Those are **fixture IDs**, not citations. Coverage is textual — an ID counts as covered when its string appears anywhere in a test file — so a fixture that carries IDs as data reads as coverage unless it is excluded.

The only sanctioned exclusion is the **ignore list** in `docs/agents/project.md`: name the fixture or test-support file there and it drops out of the test-file walk wholesale. That is the walk *only* — it cannot exclude a requirements file from defining IDs, so it cannot hide a real requirement from coverage checking. Never exclude an ID by hand, one at a time.

---

## Overlapping features are not flagged

Duplication is caught by an inline `docs/specs/` search: [`brainstorm`](../skills/brainstorm.md) and [`code-review`](../skills/code-review.md) grep the existing specs for a feature that already covers the idea, and `docs/specs/INDEX.md` is the feature-code registry they read.

### `brainstorm` never mentions an overlapping feature

Two likely causes:

1. **`INDEX.md` is empty or stale.** `write-requirements` registers each feature code in `docs/specs/INDEX.md` *before* writing the file. A code that was never registered leaves nothing for the search to match — the overlap is invisible. Register the missing rows.
2. **The spec text does not name the shared concept.** The search is textual; two features that solve the same problem in different words will not collide. Say the shared term out loud in the requirements so a future search finds it.

### A feature code is missing from `INDEX.md`

A `requirements.md` declares a feature code with no row in `docs/specs/INDEX.md`. `write-requirements` registers the code *before* writing the file; this means that step was skipped. Add the row so the registry stays complete.

---

## Skills do not fire

### The agent answers without invoking any skill

The [`using-skills`](../skills/using-skills.md) gate is not in context. It is injected by a `SessionStart` hook with matcher `startup|clear|compact`.

- Installed as a plugin? The hook ships in `hooks/hooks.json`.
- Installed by symlink, or into a harness with no hook support? Re-run `/setup-repo` and accept the session-start hook, which copies `templates/session-start.sh` into `.claude/hooks/` and wires it through `$CLAUDE_PROJECT_DIR`.

Verify it fires: execute `.claude/hooks/session-start.sh` and confirm it prints one line of valid JSON.

### A specific skill never triggers

Its `description` is the trigger, and it is the one field you cannot eyeball. Per [`writing-skills`](../skills/writing-skills.md), under-specifying is the commoner of the two failure directions: the skill simply never fires.

The description should carry the words a user would actually type — symptoms, literal error text, file names, synonyms — plus the outcome noun. Trigger-test it with should-fire and should-not-fire queries, per the `pressure-testing.md` reference beside `writing-skills`.

### The agent reads the description and skips the body

The opposite failure, and a subtler one. A description that summarizes the *workflow* hands the agent a shortcut it obeys instead of the body.

> "use when planning — dispatches a reviewer between tasks" gets the summary obeyed and the body ignored.

Rewrite the description as **trigger + outcome noun, never the workflow**.

### The agent says it will invoke `/triage` and then does nothing

`triage` carries `disable-model-invocation: true`. The agent *cannot* invoke it. Some skill body is directing a hand-off to a user-invoked target — that is a real bug, not a style nit. A hand-off reaches a user-invoked skill only by *naming it for the user to run*.

The user-invoked set: `/ask`, `/writing-skills`, `/teach`, `/setup-repo`, `/scaffold-project`, `/establish-project`, `/triage`, `/improve-architecture`, `/handoff`, `/file-issues`, `/release`.

---

## Execution problems

### `execute-plan` re-ran a task that was already done

The controller trusted its own memory after a compaction. `.skills/progress.md` is the source of truth:

> Controllers that lost their place have re-dispatched entire completed task sequences — the single most expensive failure this loop has.

After compaction or resume, trust the ledger and `git log`. Never re-dispatch a task the ledger marks complete. If `.skills/` was wiped (it is git-ignored), reconstruct progress from `git log`.

### The reviewer approved a task that was obviously broken

Check the review bundle's diff base. The controller builds the bundle itself — `git log`/`git diff` from a recorded base into `.skills/review-<base7>..<head7>.diff` — and if that base is `HEAD~1` instead of the sha recorded *before* the implementer was dispatched, the reviewer saw only the last commit of a multi-commit task.

`execute-plan` warns about this: `BASE=$(git rev-parse HEAD)` is step 1 of the per-task loop for exactly this reason.

### An implementer keeps returning BLOCKED

Never force the same model to retry with nothing changed. Diagnose:

| Cause | Move |
|---|---|
| Missing context | Supply the file, interface, or decision it named, and re-dispatch on the same model |
| Reasoning ceiling | Re-dispatch on a stronger model |
| Task too large | Split it into smaller dispatches |
| The plan itself is wrong | Escalate to the user |

### The plan mandates something the reviewer flags as a defect

The plan does not grade its own work. Present the finding **and** the mandating plan text to the user and ask which governs. Never dismiss the finding; never dispatch a fix that contradicts the plan without asking.

`execute-plan`'s pre-flight scan is meant to catch these before any dispatch and batch them into one question.

---

## Verification problems

### Tests are green but the feature is broken

That is the expected state, not an anomaly. Green unit tests prove that the assertions someone wrote pass.

Run [`acceptance-check`](../skills/acceptance-check.md): derive the user-facing behaviors from the spec, drive the running system through every one as a real client, and promote the passing checks into committed ID-tagged tests.

### The trace check passes but the code is wrong

The spine proves that an ID is defined, cited, and present in a test file. It cannot prove the test is a *good* test.

A tautological test — one whose expected value is recomputed the same way the code computes it — satisfies the trace check completely and proves nothing. That is [`tdd`](../skills/tdd.md)'s anti-pattern table's job, and `code-review`'s Standards axis, and the acceptance skills'.

### A regression test that never catches anything

Apply the regression-proof pattern from [`verify`](../skills/verify.md):

```
write test → passes → revert the fix → test MUST fail → restore fix → passes
```

A test that survives the revert is testing nothing.

---

## Debugging problems

### Three fixes in and the bug is still there

Stop. From [`debug`](../skills/debug.md):

> **Three failed fix attempts = STOP.** The architecture is in question, not your latest hypothesis — especially if each fix reveals new coupling somewhere else. Discuss with the user before attempt 4.

### Cannot build a red-capable command

Say so explicitly, list what you tried, and ask the user for a reproducing environment, a captured artifact, or permission to add temporary instrumentation. **Do not proceed on vibes.** No red-capable command means no Phase 2.

For a non-deterministic bug, do not chase a clean repro. Raise the reproduction rate — loop the trigger 100×, add stress, shrink timing windows — until it is high enough to debug against.

---

## Setup problems

### A verify command works in my shell but fails in `tdd`

`docs/agents/project.md` records commands that were *pre-filled from detection* and may never have been run. Re-run `/setup-repo` and pay attention to step 6, which classifies each command as a wiring failure, a content failure, or a pass. Setup is not done while any command is mis-wired.

## See also

- [Traceability — the spine](../concepts/traceability.md) — what the trace check is and the finding codes
- [The gates](../concepts/gates.md) — what each Iron Law is preventing
- [`sync-spec`](../skills/sync-spec.md) — the skill for realigning a drifted spec
- [`ask`](../skills/ask.md) — the router, when you do not know which flow you are in
