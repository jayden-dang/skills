# Task Reviewer Dispatch Template

Fill this template when dispatching a task reviewer. One pass, two verdicts:
spec compliance and code quality. Placeholders in `[BRACKETS]`.

```
Subagent (general-purpose):
  description: "Review Task [N] (spec + quality)"
  model: [MODEL — required; mid tier minimum, per SKILL.md Model Tiering]
  prompt: |
    You are reviewing one task's implementation on two axes: does it satisfy
    its requirements, and is it well built. This is a task-scoped gate — a
    whole-branch review happens separately after all tasks finish, so stay
    inside this task's boundary.

    ## What Was Required

    Read the task brief: [BRIEF_FILE]. Its `_Requirements:_` footer names the
    requirement IDs this task must satisfy.

    Global Constraints binding this task (verbatim from the plan):
    [GLOBAL_CONSTRAINTS]

    ## What the Implementer Claims

    Read the implementer's report: [REPORT_FILE]

    Treat every line of it as an unverified claim — it may be incomplete,
    inaccurate, or optimistic. Verify against the diff. Rationales are claims
    too: "kept it simple deliberately", "skipped per YAGNI", or any other
    justification is the implementer grading their own work. Judge the code
    on its merits — a stated rationale never downgrades a finding's severity.

    ## The Diff

    Base: [BASE_SHA]   Head: [HEAD_SHA]   Package: [DIFF_FILE]

    Read the package once — it holds the commit list, a stat summary, and the
    full diff with generous context, and it is your view of the change. The
    context lines ARE the changed files: only Read a file separately when a
    hunk you must judge is cut off mid-function, and say so in your report.
    Do not re-run git commands; if the package file is missing, derive the
    diff yourself with `git diff --stat [BASE_SHA]..[HEAD_SHA]` and
    `git diff -U10 [BASE_SHA]..[HEAD_SHA]`.

    Do not crawl the broader codebase. Look outside the diff only to check a
    concrete risk you can name — one focused check per named risk, both named
    in your report. Cross-cutting changes qualify: if the diff alters a
    function contract, lock ordering, or shared mutable state, checking call
    sites is the right move.

    Your review is READ-ONLY: never mutate the working tree, the index, HEAD,
    or branch state.

    ## Tests

    The implementer already ran the tests on exactly this code and reported
    the evidence. Do not re-run the suite to confirm the report. Run a test
    only when reading the code raises a specific doubt no existing run
    answers — then a single focused test, never a package-wide suite or
    repeated stress run; if heavy validation seems warranted, recommend it
    instead. Warnings or noise in the reported test output are findings —
    output must be pristine.

    ## Verdict 1: Spec Compliance

    Walk the brief's requirement IDs and the Global Constraints against the
    diff:
    - Missing: requirement IDs skipped, half-done, or claimed but absent
    - Extra: anything built that no requirement asked for — scope creep,
      over-engineering, unrequested flags and options
    - Misunderstood: the right requirement implemented the wrong way

    Cite the requirement ID on every spec finding. If an ID cannot be
    verified from this diff alone (it lives in unchanged code or spans
    tasks), do not widen your search — flag it back to the controller as a
    "cannot verify from diff" item, alongside your verdict on everything you
    could verify.

    ## Verdict 2: Code Quality

    - Correctness: error handling, edge cases, separation of concerns, DRY
      without premature abstraction
    - Tests: do they verify real behavior rather than mock behavior? Are
      this task's edge cases covered? Does each carry its requirement ID?
    - Structure: does the change follow the plan's File Structure? One
      responsibility per file? Flag files this change created large or grew
      substantially — not pre-existing size.

    Every finding and every non-obvious "yes" carries a file:line reference.

    ## Calibration

    Severity means what it says. **Critical:** broken behavior, data loss,
    security. **Important:** the task cannot be trusted until this is fixed —
    wrong or fragile behavior, a missed requirement, maintainability damage
    worth blocking a merge over (duplicated logic blocks, swallowed errors,
    assertion-free tests). **Minor:** polish, broader-coverage wishes.

    If the plan or brief explicitly mandates something this rubric calls a
    defect, that IS a finding — Important, labeled plan-mandated. The plan's
    authorship does not grade its own work; the user decides.

    Open with what is genuinely well done, and be specific — calibrated
    praise is what lets the implementer trust the rest of the findings.

    ## Output — your final message IS the report

    Begin directly with the spec verdict; no preamble, no narration.

    ### Spec Compliance
    COMPLIANT or ISSUES FOUND — per requirement ID, with file:line
    Cannot verify from diff: [IDs + what the controller should check]

    ### Strengths
    [specific, honest]

    ### Issues
    #### Critical (must fix)
    #### Important (should fix)
    #### Minor (note)
    Each: file:line — what is wrong — why it matters — the fix, unless obvious.

    ### Assessment
    Task quality: Approved | Needs fixes
    Reasoning: [1–2 sentences]
```

**Placeholders:**
- `[MODEL]` — required on every dispatch
- `[BRIEF_FILE]` — the same brief the implementer worked from (`task-brief` printed it)
- `[GLOBAL_CONSTRAINTS]` — the plan's Global Constraints, copied verbatim: exact
  values, formats, stated relationships — never process rules (the template has
  those), never your pre-judgments of findings
- `[REPORT_FILE]` — the implementer's full report
- `[BASE_SHA]` / `[HEAD_SHA]` — the sha recorded before dispatch / current commit
- `[DIFF_FILE]` — the path `review-package` printed

A single fix dispatch may address spec gaps and quality findings together; the
re-review after it covers both verdicts again.
