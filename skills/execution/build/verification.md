# Verification in continuous builds

Use the default task and wave gates unless both of these entries are set in
the project's approved `docs/agents/project.md`:

- `Verification gate placement: integration`
- `Integration gate: <command and declared scope>`

Read actual settings, outside template examples and placeholders. The command
takes the ready set's pinned pre-merge base and integrated candidate (as refs
or the corresponding checkout), covers the union of
changed units and affected consumers, and includes the wave compile/lint
scope. Its policy names shared inputs and a full-suite fallback for unknown
scope. Use default placement when either setting is missing or verification
wiring is incomplete, even if both settings are present. A known stub or
an unproven fallback makes the opt-in incomplete. Record the gap. If the
default commands are broken too, block verification.

| Placement | Worker, before handoff | Controller, before completion and next ready set |
|---|---|---|
| Default | Narrow test-first loop and Task gate | Parallel sets: Wave gate (configured command, else workspace typecheck/lint). Single tasks keep their Task gate result. |
| Integration | Narrow test-first loop and fresh focused checks on the final lane revision. Report changed paths, exercised boundaries and shared inputs to the controller. | After review, run the Integration gate once on the combined candidate, even for a single task. It replaces the Task gate and the separate Wave gate for this set. |

Bind the result to the tested revision. Capture the log and exit code together
on the first invocation. Read that result to settle a claim about the same
candidate and scope. Run again for a changed candidate, a required wider scope,
or a failed or incomplete run. Record warnings and elapsed time.

Before assembling a set with a combined gate, record the pending task IDs,
base and reviewed lane commits
in the ledger. Record the integrated SHA when assembled. On resume, reconcile
that pending set against Git and finish its gate before dispatching from the
ready queue. Reconstruct from reviewed commits if assembly was interrupted.
Use the canonical complete check for an unknown input, unexplained empty
selection, or shared input the selector cannot cover. If the integration
command ran that fallback and recorded the full result, use that evidence.
A fast profile with excluded tests cannot stand for the fallback. If the
complete check does not include the required
compile/lint checks, run those checks explicitly. Red, skipped, or unproven
checks leave the set pending. Never release a dependent on lane evidence alone.

The close suite still runs per the close receipt. Story-unit and inline modes
keep their current task gates. A scoped integration result is evidence only
for the tested scope.
