# Requirement IDs

The requirement ID is the single most important object in this system. Everything else is scaffolding around it.

It is not a heading in a document. It is a string that appears in a test tag, a commit trailer, an issue body, a design section, a task footer, and a changelog line — and the [trace check](traceability.md) reports a failure when those uses disagree with its definition.

## The grammar

```
SHELL-1.2
└─┬─┘ │ │
  │   │ └─ criterion number within the story
  │   └─── story number within the feature
  └─────── feature code
```

**Feature code.** 2–12 characters, `A-Z0-9`, starting with a letter. Unique repo-wide, forever — a retired code is never reused. Registered in `docs/specs/INDEX.md` **before** the requirements file that uses it is written.

**Story number.** Corresponds to a `## N. <title>` section in `requirements.md`, one per user story.

**Criterion number.** One observable behavior. If an acceptance criterion needs the word "and", it is usually two criteria.

The pattern the [trace check](../resources/scripts.md#the-trace-check) matches is `\b([A-Z][A-Z0-9]{1,11})-(\d+)\.(\d+)(?![.\d])`. Two details in there are deliberate. There is no trailing `\b`, because a markdown italics footer ends with `_` — a word character — which would silently drop the last ID on the line. And the negative lookahead `(?![.\d])` guards against matching a prefix of a longer number.

## Where a definition lives

An ID is *defined* in exactly one place: a `requirements.md` file, as a bolded criterion.

```markdown
- **SHELL-1.2** WHEN the user selects a module THE SYSTEM SHALL persist the
  selection and restore it on next launch.
```

Tier-1 fixes that no feature owns may instead be defined in `docs/specs/fixes.md`, a shared home the trace check reads the same way.

Defining the same ID twice is error **E3**.

## Where an ID travels

| Artifact | Carries the ID as |
|---|---|
| `design.md` section | a `Satisfies: SHELL-1.1, SHELL-1.2` line |
| `tasks.md` task | a `_Requirements: SHELL-1.1, SHELL-1.2_` footer |
| Playwright test | `{ tag: ['@SHELL-1.2'] }` — grep-selectable, and present in the JSON reporter |
| Vitest test | `annotate('SHELL-1.2', 'requirement')`, or the ID in the test name |
| Rust test | `/// REQ: SHELL-1.2` doc comment above the test |
| Commit message | an `Implements: SHELL-1.2` or `Guards: SHELL-1.3` trailer |
| Issue body | a `Requirements covered:` section |
| Changelog entry | assembled from the trailers, rendered as the requirement's own text |

The per-layer test conventions are not hardcoded. [`setup-repo`](../skills/setup-repo.md) asks which convention each test layer in *this* repo uses and records the answers in `docs/agents/project.md`; [`tdd`](../skills/tdd.md) and the [trace check](../resources/scripts.md#the-trace-check) both read from there. The only hard requirement is that the convention be **greppable**.

## Immutability

> Once `Status: Approved`, IDs never change meaning and are never renumbered.

This is the rule that makes the ID worth citing. A test tagged `@SHELL-1.2` is worthless if `SHELL-1.2` might come to mean something else next month.

So requirements are never deleted and never renumbered. They are **retired by strikethrough**:

```markdown
- ~~**SHELL-1.2**~~ superseded by SHELL-1.4
```

The trace check treats a struck-through ID as **undefined**. That is the clever part: the moment you retire a requirement, every test and task still citing it surfaces immediately as an **E1** error ("cites unknown requirement"). Retirement cannot be done quietly.

New requirements take the next free number under their story. [`sync-spec`](../skills/sync-spec.md) enforces both rules as its Iron Rules, and treats the orphans that strikethrough surfaces as *decisions to put to the user*, not cleanup to perform silently.

## The checks that enforce it

The [trace check](../resources/scripts.md#the-trace-check) reports three errors and two warnings. Any error is a failure the invoking skill acts on; warnings are surfaced but do not fail the gate on their own.

| Code | Meaning |
|---|---|
| **E1** | a task or test cites an ID that is not defined in any requirements file |
| **E2** | a requirements file with `Status: Implemented` or `Shipped` has a requirement with zero test references |
| **E3** | the same ID is defined more than once |
| **W1** | a requirements file with `Status: Approved` has a requirement not cited by any task |
| **W2** | a requirements file is missing a `Status:` line or a `Feature code:` line |

The interplay between W1 and E2 is the one to understand, and [`write-plan`](../skills/write-plan.md) calls it out explicitly. A task footer citing an ID satisfies W1 while the spec is merely `Approved`. But a footer is not a test. The moment the feature flips to `Implemented`, that same uncovered ID becomes an **E2 error**.

So `write-plan`'s coverage check goes further than the trace check can at plan time: every requirement ID must appear not only in a task footer, but in a **test annotation inside some task's steps**. An ID the design promised to cover but the plan left untagged is *dropped coverage* — the fix is to add the test, never to renumber.

## Status lifecycle

The `Status:` line on `requirements.md` is what arms E2.

```
Draft ──► Approved ──► Implemented ──► Shipped
```

| Transition | Evidence required |
|---|---|
| Draft → Approved | the user explicitly approved the written file — never inferred from conversation |
| Approved → Implemented | every task box checked **and** the trace check shows every live requirement covered by a test |
| Implemented → Shipped | the feature went out in a release (normally applied by [`release`](../skills/release.md)) |

`sync-spec` applies a transition only when its evidence exists. If the evidence is partial, it says exactly what is missing rather than transitioning.

## What counts as coverage

From the repo's own glossary, because the distinction is easy to fudge:

> **Covered** — a requirement is *covered* when at least one test citing its ID **ran and passed**, as attested by a test runner's report. A skipped, failing, or commented-out test is not coverage; neither is an ID that merely appears in a source file.
>
> *Avoid:* "has a test" (a string in a file is not a test), "tagged" (tagging is the mechanism, coverage is the outcome).

And the companion term:

> **Citation** — an occurrence of a requirement ID that a runner attests to. Distinct from a **fixture ID**: an ID-shaped string appearing in source (example data, documentation) that no test ever asserts.

That distinction matters because the trace check's citation pass is a textual `grep`: an ID string present in a test file counts, and the check cannot tell a real assertion from a fixture. So its coverage signal is textual — necessary but not sufficient. A repo whose own fixtures carry ID-shaped strings can name those files in the trace ignore list in `docs/agents/project.md` so the pass skips them and does not report phantom citations.

## Worked example

`SHELL-1.2` is approved. It flows outward:

**Design** (`design.md`):
```markdown
### Module store

Satisfies: SHELL-1.1, SHELL-1.2
```

**Plan** (`tasks.md`):
```markdown
### Task 3: Persist the active module

- [ ] Step 1: Write the failing test
      test('restores the persisted module after hydration [SHELL-1.2]', ...)

_Requirements: SHELL-1.2_
```

**Test** (`src/shell/module-store.test.ts`):
```ts
test('restores the persisted module after hydration [SHELL-1.2]', async () => { … })
```

**Commit**:
```
feat(shell): persist and restore the active module

Implements: SHELL-1.2
```

**Changelog**, assembled by `release` from that trailer plus the requirement's own text:
```markdown
### Shipped behavior
- Module selection persists across launches — SHELL-1.2
```

Nobody wrote that changelog line. It was derived, and it is derivable precisely because the ID is the same string in all five places.

## See also

- [Traceability](traceability.md) — why the spine exists and what it buys
- [EARS reference](../resources/ears.md) — the criterion syntax the IDs attach to
- [The trace check](../resources/scripts.md#the-trace-check) — the grep/git passes and their rules
- [`write-requirements`](../skills/write-requirements.md) — where IDs are minted
