# Traceability — the spine

Traceability is the answer to a single question, asked at every point in a project's life:

> **Why does this line of code exist, and how do we know it still does what it was supposed to?**

Most codebases cannot answer it. The intent lived in a conversation, a ticket, or someone's head, and all three decay.

## Intent as a persisted, addressable object

The core move is to refuse to store intent anywhere it can evaporate.

Chat history is the worst possible store: unaddressable, unsearchable, and deleted by compaction at exactly the moment the work has gone on long enough to need it. Ticket titles are barely better. So intent is written to `requirements.md`, given an [immutable ID](requirement-ids.md), and every downstream artifact points back at that ID.

This is why [`brainstorm`](../skills/brainstorm.md) refuses to exit into code, and why [`write-requirements`](../skills/write-requirements.md) presents *the file* for approval rather than accepting conversational agreement:

> Do not proceed to design on the strength of conversational agreement — the written requirements are what get approved.

## The chain

```
requirements.md          **SHELL-1.2** WHEN the user selects a module …
        │
        ▼
design.md                ### Module store
                         Satisfies: SHELL-1.1, SHELL-1.2
        │
        ▼
tasks.md                 ### Task 3: Persist the active module
                         _Requirements: SHELL-1.2_
        │
        ▼
test                     test('restores the persisted module [SHELL-1.2]', …)
        │
        ▼
commit                   Implements: SHELL-1.2
        │
        ▼
issue / changelog        Requirements covered: SHELL-1.2
                         "Module selection persists across launches — SHELL-1.2"
```

Every link is a citation. Every citation is machine-checkable. And the check runs on every `verify`, every `finish-branch`, every `release`, and in CI.

## Why a script, not diligence

Every project that has ever maintained a requirements traceability matrix by hand has watched it rot. The matrix is correct on the day it is written and wrong within a month, because keeping it correct is unpaid work that nobody notices until an audit.

So the system makes a different bet: **the trace is enforced by a linter or it does not exist.**

[`check-trace.mjs`](../resources/scripts.md#check-trace) is a zero-dependency Node script. It parses the requirements files for definitions, the task footers and test files for citations, and it fails:

| Code | Meaning |
|---|---|
| **E1** | a task or test cites an ID defined nowhere |
| **E2** | a requirement in an `Implemented`/`Shipped` spec has zero covering tests |
| **E3** | the same ID is defined twice |
| **W1** | an `Approved` requirement is cited by no task |
| **W2** | a requirements file lacks a `Status:` or `Feature code:` line |

This is [`writing-skills`](../skills/writing-skills.md)' doctrine applied to itself. From its table of what form fixes what failure:

| Baseline failure | Write this | Not this |
|---|---|---|
| A check that must never be skipped or misjudged | A bundled deterministic script the skill runs and acts on | Prose steps describing the check — **code is deterministic, language interpretation is not** |

And the corollary, from the same skill: *if the rule is mechanically enforceable, automate it and skip the skill.* Documentation is for the judgment calls a check cannot make.

## What "covered" actually means

The word does real work here, so the repo's glossary pins it down:

> **Covered** — a requirement is *covered* when at least one test citing its ID **ran and passed**, as attested by a test runner's report. A skipped, failing, or commented-out test is not coverage; neither is an ID that merely appears in a source file.
>
> *Avoid:* "has a test" (a string in a file is not a test), "tagged" (tagging is the mechanism, coverage is the outcome).

This is why [`verify`](../skills/verify.md) will not accept "requirements met" on green tests alone. Its claim-to-evidence table demands `check-trace` **and** `check-graph --verify` passing **and** each acceptance criterion checked off individually against observed behavior.

And it is why [`acceptance-check`](../skills/acceptance-check.md) exists at all. Green unit tests prove that the assertions someone wrote pass. They do not prove the feature works.

## What the spine buys

**Release notes for free.** [`release`](../skills/release.md) collects `git log <last-tag>..HEAD`, groups commits by their `Implements:` / `Guards:` trailers, and looks up each cited ID's requirement text in `docs/specs/`. The changelog entry reads as shipped behavior — "Module selection persists across launches — SHELL-1.2" — rather than as commit prose. `Guards:` trailers become a "Protected behavior" grouping. Nobody writes this; it is derived.

**A review axis that cannot be faked.** [`code-review`](../skills/code-review.md) runs a **Spec** subagent that walks the requirements ID by ID against the diff, reporting IDs that are missing, only partially implemented, or implemented wrong — quoting the ID on every finding. It runs *in parallel with and separately from* the Standards axis, because a change can pass one and fail the other: flawless code that builds the wrong thing, or a faithful implementation that tramples the repo's conventions. Merged reports let one axis mask the other.

**Guard requirements.** A `SHALL CONTINUE TO` criterion is the mechanism that stops an agent from breaking load-bearing behavior nobody thought to mention. `write-requirements` will not accept "found nothing to guard" as a default; its completion criterion is that you *actively searched the touched surface*.

**Honest resumption.** After compaction, the requirements file is the only surviving record of what was agreed. [`execute-plan`](../skills/execute-plan.md)'s ledger and `git log` outrank the agent's own recollection, and the plan's task footers say which requirement each completed commit served.

**Anti-rot.** [`sync-spec`](../skills/sync-spec.md) exists because a spec that is not resynced after change becomes fiction, and fiction is worse than no spec. It diffs requirements against design, tasks, and tests; surfaces orphans as *decisions*, not cleanup; and applies status transitions only where evidence exists.

## The failure this prevents

Concretely: an agent implements `SHELL-1.2`, a later refactor breaks it, and the test that would have caught it was deleted along with the code it tested.

Without the spine, nothing notices. The requirement is still in the document, still reading as true.

With it: `requirements.md` says `Status: Implemented`, `SHELL-1.2` has zero covering tests, and `check-trace` exits 1 with `E2 SHELL-1.2 (docs/specs/…/requirements.md, Implemented) has no covering test`. CI is red. `finish-branch` refuses to present the merge menu. `release` refuses to tag.

## Its limits

The spine proves that a *test citing an ID ran and passed*. It cannot prove the test is a good test.

That is the job of the surrounding skills, and it is worth being clear that they are doing separate work: [`tdd`](../skills/tdd.md)'s anti-pattern table (tautological tests, tests that assert on mocks, tests coupled to implementation), `code-review`'s Standards axis, and the acceptance family driving the running system as a real client. A tautological test tagged `@SHELL-1.2` satisfies `check-trace` completely and proves nothing at all.

Traceability guarantees the *presence* of an attested link. The rest of the system guarantees the link is worth having.

## See also

- [Requirement IDs](requirement-ids.md) — the grammar, immutability, and status lifecycle
- [The gates](gates.md) — the four Iron Laws the spine supports
- [`check-trace`](../resources/scripts.md#check-trace) — flags, config, exit codes
- [The feature graph](feature-graph.md) — the horizontal layer built on the same specs
