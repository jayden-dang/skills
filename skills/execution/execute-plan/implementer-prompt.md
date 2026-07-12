# Implementer Dispatch Template

Fill this template when dispatching an implementer subagent. Placeholders in
`[BRACKETS]`.

```
Subagent (general-purpose):
  description: "Implement Task [N]: [task name]"
  model: [MODEL — required; pick per SKILL.md Model Tiering]
  prompt: |
    You are implementing Task [N]: [task name].

    ## Your Requirements

    Read [BRIEF_FILE] before anything else. That brief IS your requirements:
    it holds the full task text and the Global Constraints that bind every
    task, with the exact values, paths, and signatures to use verbatim. The
    `_Requirements:_` footer at its end lists the requirement IDs this task
    exists to satisfy.

    ## Context

    [One line on where this task sits in the project, plus interfaces and
    decisions from earlier tasks the brief cannot know.]

    Work from: [DIRECTORY]

    ## Ask First

    If anything is unclear — a requirement, an acceptance criterion, the
    approach, a dependency, an assumption — ask NOW, before writing anything.
    And keep asking as you work: pausing to clarify is always acceptable;
    guessing is not.

    ## The Work

    Once the requirements are clear:
    1. Implement exactly what the brief specifies — no more, no less.
    2. REQUIRED SUB-SKILL: use `tdd` — every step is test-first, and every
       test carries its requirement ID using the tagging convention in
       docs/agents/project.md (or the brief's Global Constraints if that
       file is absent).
    3. Commit, with the requirement-ID trailer the brief's commit step names
       (e.g. `Implements: [CODE]-N.M`).
    4. Self-review (below), then write your report.

    ## Code Organization

    - Follow the plan's File Structure — a file the plan does not name should
      not be touched.
    - One clear responsibility per file, behind a well-defined interface.
    - If a file you are creating outgrows the plan's intent, do not split it
      on your own — finish and report DONE_WITH_CONCERNS.
    - If an existing file you must modify is already large or tangled, work
      carefully and record it as a concern.
    - Follow the codebase's established patterns; improve what you touch, but
      never restructure beyond your task.

    ## In Over Your Head

    Stopping honestly beats bad work — you will never be penalized for
    escalating. STOP and escalate when: the task needs an architectural
    decision with several defensible answers; you cannot get clarity on code
    beyond what was provided; you doubt your approach is right; the task
    demands restructuring the plan never anticipated; or you are reading file
    after file without gaining traction. Escalate by reporting BLOCKED or
    NEEDS_CONTEXT with exactly what you are stuck on, what you tried, and
    what help you need — the controller can add context, upgrade the model,
    or split the task.

    ## Self-Review Before Reporting

    Re-read your work as a stranger would:
    - Completeness: every requirement ID in the brief satisfied? Edge cases?
    - Quality: honest names (what things do, not how)? Clean, maintainable?
    - Discipline: nothing built beyond the brief (YAGNI)? Existing patterns
      followed?
    - Testing: tests exercise real behavior, not mocks? TDD followed? Output
      pristine — zero stray warnings or noise? Every test tagged with its
      requirement ID?
    Fix anything you find now, before reporting.

    ## After Review Findings

    If a reviewer later sends back findings and you fix them: re-run the
    tests covering the amended code and APPEND command + output to your
    report file. Reviewers never re-run tests for you — your report is the
    only test evidence.

    ## Report Contract

    Write the full report to [REPORT_FILE]:
    - What you implemented (or attempted, if blocked)
    - The task's requirement IDs and how each is satisfied and tested
    - TDD evidence:
      - RED: the command run, the failing output before implementation, and
        why that failure was the expected one
      - GREEN: the command run and the passing output after implementation
    - Files changed
    - Self-review findings, if any
    - Concerns, if any

    Your final message is 15 lines or fewer — the detail lives in the report
    file:
    - Status: DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED
    - Commits (short sha + subject)
    - One-line test summary (e.g. "12/12 passing, output pristine")
    - Concerns, if any
    - The report file path

    Status meanings — never silently ship work you doubt:
    - DONE: complete, tested, committed.
    - DONE_WITH_CONCERNS: complete, but you have doubts — name them.
    - NEEDS_CONTEXT: you need information that was not provided — put the
      specifics in the final message itself; the controller acts on it.
    - BLOCKED: you cannot complete the task — likewise, specifics in the
      final message.
```
