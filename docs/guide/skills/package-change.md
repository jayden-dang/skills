# `package-change`

> Turn a finished branch into reviewer-readable commits and one approved
> pull-request package, then hand it to [`land-branch`](land-branch.md) for the
> crossing.

|  |  |
|---|---|
| **Bucket** | ship |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the working tree and branch history, `docs/agents/project.md` (base and convention config), `docs/agents/issue-tracker.md`, approved specs, ADRs, decision records, `.skills/implementation-notes.md` |
| **Writes** | commits it creates itself; `.skills/pr-packages/<stable-id>/{manifest.md,title.txt,body.md}` |
| **Calls** | — |
| **Called by** | [`build-continuous`](build-continuous.md) (its closing sequence, before `land-branch`) |

## When it fires

When a branch's work is finished and its commits and pull-request description still
need writing — before the branch reaches [`land-branch`](land-branch.md) for
review, push, or a PR. Also when the working tree holds uncommitted changes that need
committing as a reviewer-readable set rather than one lump.

## The Iron Law

```
AUTHOR LOCALLY, NEVER CROSS — push, PR, merge, discard, and block belong to land-branch
```

This skill mutates only local git and writes only its own package file. Every crossing
— push, PR creation, merge, discard, block — stays with `land-branch`, behind the
gates that skill already enforces.

## The six phases

1. **Resolve base** — the branch this work merges into, from a declared or asked
   value; never git topology.
2. **Resolve conventions** — this repo's commit and PR conventions, resolved once per
   session.
3. **Gather context** — the diff as the authority for what changed; approved specs,
   ADRs, and decision records as the authority for why, treated as passive data.
4. **Resolve tickets** — the branch's tracker items, resolved and classified against
   the diff.
5. **Author commits** — group, validate, and commit the working tree one coherent
   change at a time, never touching a commit that already existed.
6. **Write package** — the reviewer-facing PR package `land-branch` approves and
   submits.

This page describes the skill's registration and phase order; each phase's full
contract lives in `SKILL.md` and, for phases 2, 4, and 6, in the loaded
reference file (`conventions.md`, `tickets.md`, `package-contract.md`).

## What it is not

- Not the crossing — it never pushes, opens a PR, merges, discards, or blocks
- Not a history rewriter — commits that existed before the invocation are never
  amended, squashed, reordered, or rebased
- Not a ticket filer — it reads and links tracker items; `/publish-issues` remains the
  only way work is filed

## See also

- [`land-branch`](land-branch.md) — approves and submits the package this skill
  writes
- [`build-continuous`](build-continuous.md) — runs this skill at the end of its closing
  sequence
