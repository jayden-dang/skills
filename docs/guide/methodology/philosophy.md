# Philosophy

Six principles govern every skill in the set. They are not decoration — each one settles a design argument that comes up repeatedly, and each one is enforced somewhere concrete.

## 1. Predictability is the root virtue

A skill exists to wrangle determinism out of a stochastic system.

The precise claim: the agent takes the same **process** on every run — not that it emits identical output. A brainstorming skill should reliably diverge. Its tokens vary; its behavior does not. When you ask "should this rule be in the skill?", the question is always *does this line change behavior versus no skill at all?* That is the **no-op test**, and a sentence that fails it gets deleted whole, not trimmed.

This is why disputes about what the agent does by default are settled by running the scenario, never by debate. And it is why [`writing-skills`](../skills/writing-skills.md) carries an Iron Law of its own: no skill and no edit to a skill ships without a failing test first. Writing skills is test-driven development applied to process documentation.

**Enforced by:** the RED/GREEN/REFACTOR cycle in `writing-skills`, and its `pressure-testing.md` methodology.

## 2. Traceability is the memory

Intent lives in persisted, individually addressable requirements — not in chat history.

Chat history is the worst possible place to store what a project is supposed to do. It is unaddressable, unsearchable, and it is deleted by compaction at exactly the moment the work gets long enough to need it. So intent gets written to `requirements.md`, given an immutable ID, and every downstream artifact points back at that ID.

The corollary matters more than the principle: **a script, not diligence, keeps this honest.** Every project that has ever kept a requirements traceability matrix by hand has watched it rot. [`check-trace`](../resources/scripts.md#check-trace) runs in `verify`, in `release`, and in CI, and it fails the build.

> *"If it isn't in an approved requirements.md, it lives only in this chat and dies with it."*
> — `brainstorm`, rationalization table

**Enforced by:** `check-trace.mjs`, run by `verify`, `finish-branch`, `release`, and CI.

## 3. Gates, not vibes

No code before an approved spec. No fix before a root cause. No completion claim without fresh evidence.

The gates are written as hard prohibitions because that is the form that works. An agent that knows a rule and breaks it under pressure does not need softer guidance; it needs the prohibition, plus an explicit counter to every rationalization it actually produced in a baseline run. That is why `tdd` carries nine rows of "Thought → Reality" and `debug` carries seven. Each row is a real rationalization, recorded verbatim, and countered by name.

The gates apply hardest exactly when it is most tempting to skip them: emergencies, "obvious" one-liners, and the moment right after a previous fix did not work.

**Enforced by:** the `<HARD-GATE>` block in `brainstorm`; the Iron Laws in `tdd`, `debug`, and `verify`.

## 4. Ceremony scales with the task

Three tiers prevent pages of spec for a trivial change.

The subtlety is that the tier decision is not an escape hatch — it is itself the design step, and it must be **stated out loud**. `brainstorm` names the tier and says why; `amend` classifies the change against the existing spec and says which case it is. An agent that quietly decides something is "too small for process" has skipped the decision, not made it.

> *"Deciding it is tier 0 IS the design step — say so explicitly and move on. Skipping the decision is the overhead."*
> — `brainstorm`, rationalization table

And a matching rule: **never spec what you do not understand yet.** Unknowns go to [`research`](../skills/research.md) or [`prototype`](../skills/prototype.md) first. Specs are an execution tool, not a discovery tool.

**Enforced by:** the tier tables in `brainstorm` and `amend`, and their explicit "state the tier out loud" completion criteria.

## 5. Tracker-agnostic, configured once per repo

Skills read repo config from `docs/agents/*.md`. GitHub Issues, GitLab, Linear, or local markdown files all work.

No skill hardcodes a test command, a lint command, a label string, or a release step. [`setup-repo`](../skills/setup-repo.md) asks once, writes the answers to `docs/agents/project.md`, `issue-tracker.md`, and `triage-labels.md`, and then *proves each command actually runs* before declaring setup complete. Every other skill reads from there.

The distinction that step-6 gate draws is worth internalizing: a **wiring failure** (command not found, missing script, bad manifest path) is a config bug you must fix now. A **content failure** (type errors, failing tests) means the command is wired right and the repo has pre-existing issues; record it and move on. Confirmed-with-the-user is not the same as works-in-this-project.

**Enforced by:** `setup-repo` step 6, which runs every configured command and classifies the result.

## 6. Small skills that compose

User-invoked skills orchestrate. Model-invoked skills hold reusable discipline.

The rule that falls out of this: **a user-invoked skill may invoke model-invoked skills, never another user-invoked one.** A user-invoked skill carries `disable-model-invocation: true` in its frontmatter, which means the agent *cannot* auto-invoke it. Directing the agent to invoke such a skill is a dead-end hand-off — a real bug, not a style nit. A hand-off reaches a user-invoked skill only by naming it for the user to run: "run `/triage`".

Splitting a skill is allowed in exactly two cases: a genuinely distinct trigger that should fire it on its own, or hiding post-completion steps behind a real context boundary so they stop tugging the agent into rushing the current step. Anything else is granularity for its own sake, paid for in context load.

**Enforced by:** the frontmatter convention, and `writing-skills`' deployment checklist ("Every hand-off invokes only a model-invocable skill").

See [The skill model](../concepts/skill-model.md) for how this plays out in practice.

## A seventh, unstated principle: context is hostile

It is not in the numbered list, but it shapes more of the architecture than any single principle above.

Context windows fill. Compaction deletes. Subagents do not inherit session history. Every one of these is treated as a fact to design around rather than a limitation to complain about:

- Discovery through planning happens in **one unbroken context window**; if the window fills before the plan is done, [`handoff`](../skills/handoff.md) moves the work to a fresh session.
- `execute-plan` gives each task a **fresh subagent** whose world is a generated brief file. The controller's context stays reserved for coordination.
- Bulk artifacts — briefs, diffs, reports — travel between agents **as file paths under `.skills/`**, never as pasted text.
- Progress is appended to a **ledger on disk**, and after compaction the ledger and `git log` outrank the agent's own recollection. The single most expensive failure this system has recorded is a controller that lost its place and re-dispatched an entire completed task sequence.
- Heavy reading is delegated to a **scan subagent** that returns a findings digest, not a file dump.

## See also

- [Overview](overview.md) — what the system is
- [The gates](../concepts/gates.md) — the four Iron Laws in detail
- [The skill model](../concepts/skill-model.md) — user-invoked vs model-invoked, and how skills reach each other
- [`writing-skills`](../skills/writing-skills.md) — the doctrine these principles are written in
