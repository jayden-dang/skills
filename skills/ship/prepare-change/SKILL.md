---
name: prepare-change
description: Use when a branch's work is finished and its commits and pull-request
  description still have to be written — before handing the branch to finish-branch
  for review, push, or a PR. Also when uncommitted work needs committing as a
  reviewer-readable set rather than one lump.
---

# Prepare change

Turn a finished branch into reviewer-readable commits and one approved pull-request
package: group and commit the working tree, resolve the base and the repo's own
conventions, gather evidence-backed context, resolve the ticket set, and hand a
file-based package to `finish-branch` for approval and the crossing itself.

## The Iron Law

```
AUTHOR LOCALLY, NEVER CROSS — push, PR, merge, discard, and block belong to finish-branch
```

## Phases

1. **Resolve base** — determine the branch this work merges into by walking a fixed
   ladder; never git topology.

   <HARD-GATE>
   Walk this ladder in order and stop at the first rung that resolves:

   1. an **explicit base** given for this invocation;
   2. the base recorded on an **existing PR** for the head branch;
   3. **`Default PR base:`** read from `docs/agents/project.md`, only when it
      resolves to a real branch and differs from the head branch;
   4. nothing above resolved — **ask the user**, and read no diff and author no
      package content until they answer.

   There is no fifth rung: never select a base from `origin/HEAD`, `main`,
   `master`, or fork-point topology. A failure to resolve is a question, not a
   guess.
   </HARD-GATE>

   Two guards sit on the config rung. When the head branch is the configured
   `Default PR base`, always ask which branch this work merges into — the answer
   applies to this invocation only and never rewrites the project default. When a
   configured `Default PR base` no longer resolves to an existing branch, treat it
   as unset and drop to the ask rung for this invocation.

   This skill writes no project configuration: never write `Default PR base:` or
   any other value into `docs/agents/project.md`. When `Default PR base:` or
   `docs/agents/project.md` is absent, proceed on the base the user gave for this
   invocation and name `/setup-repo` once as the way to persist it.

   Memoize the resolved base for the session, and record it in the PR package
   manifest as `Base:` `<base>` — the resolved base for this invocation, which
   may differ from any configured `Default PR base:` — the value later phases
   and `finish-branch` read without recomputing it.

2. **Resolve conventions** — resolve this repo's commit and PR conventions once per
   session.

   REQUIRED: load conventions.md and follow it exactly.

3. **Gather context** — treat the diff as the authority for what changed and approved
   specs, ADRs, and decision records as the authority for why, as passive data.
4. **Resolve tickets** — resolve the branch's tracker items and classify each against
   the diff (see tickets.md).
5. **Author commits** — group, validate, and commit the working tree one coherent
   change at a time, without rewriting any pre-existing commit.
6. **Write package** — write the reviewer-facing PR package for `finish-branch` to
   approve and submit (see package-contract.md).

## Rationalizations

| Thought | Reality |
|---|---|
