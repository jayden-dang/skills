# `tdd`

> The test-first gate. No line of production code exists before a test that fails for the right reason.

|  |  |
|---|---|
| **Bucket** | execution |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | `design.md` (Seams for testing), `docs/agents/project.md` (verify commands, test annotation conventions) |
| **Writes** | tests, production code, commits carrying `Implements:` / `Guards:` trailers |
| **Calls** | [`debug`](debug.md) (when the change is a bugfix), [`verify`](verify.md) (before any completion claim) |
| **Called by** | [`brainstorm`](brainstorm.md) (tier 0), [`amend`](amend.md), [`write-requirements`](write-requirements.md) (tier 1), [`execute-plan`](execute-plan.md), [`prototype`](prototype.md), [`receive-review`](receive-review.md), [`improve-architecture`](improve-architecture.md) |

## When it fires

Before the first line of any production code — a new feature, a bugfix, a behavior change, or a refactor. It also fires when you are about to add a mock, a test utility, or a test to code that currently has none.

This is the most frequently invoked skill in the set. Almost every path through the system exits through it.

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

If implementation was written before its test, the skill's instruction is to **delete it** — not keep it as reference, not adapt it while tests catch up. The reasoning is that code written first becomes the thing the test describes: you end up testing what you built rather than what was required.

Exceptions exist only with the user's explicit permission, and the set names them: throwaway prototypes, generated code, pure configuration. "Skip it just this once" is not an exception — it is the specific rationalization the skill exists to block.

## Where tests are allowed to live

A **seam** is a public boundary where behavior is observable without reaching into internals. Tests live only at seams listed in the feature's `design.md` under *Seams for testing*. The skill refuses to write a test at a seam that table does not confirm.

This is the contract between [`write-design`](write-design.md) and `tdd`: the design pre-agrees where the testing budget gets spent, so it lands on critical paths instead of on every internal detail. When there is no `design.md` — a tier 0/1 change, or a legacy area — the skill proposes the seams to the user and gets agreement before the first test.

## The loop

Work one vertical slice at a time: one behavior, one test, one minimal implementation, repeat. Each cycle responds to what the previous one taught you. Writing all the tests up front and then all the code is explicitly ruled out, because bulk-written tests verify imagined behavior.

1. **RED — write one failing test.** One behavior, a name that states the behavior, expectations against real code at an agreed seam. Tag it with the requirement ID it verifies. Fixing a bug? `debug` establishes the root cause first, and the RED test must reproduce *that* bug, failing for the bug's reason.

2. **Verify RED — mandatory.** Run the test. Confirm it fails, that the failure message is the one you expected, and that it fails because the behavior is missing — not because of a typo or an import error. A test that passes immediately is testing behavior that already exists: fix the test, not the code.

3. **GREEN — write the simplest code that passes.** No speculative parameters, no extra features, no touching unrelated code.

4. **Verify GREEN — mandatory.** Run the full suite. The new test passes, every other test still passes, and the output is pristine: zero warnings, zero stray errors, nothing you are "planning to clean up". If the new test fails, fix the code — never loosen the test.

5. **REFACTOR — only while green.** Remove duplication, improve names, extract helpers. Re-run the suite after each change. Add no behavior.

Then take the next slice.

## Requirement tagging

Every test carries the ID of the requirement it verifies, using the conventions recorded in `docs/agents/project.md` by [`setup-repo`](setup-repo.md). This is the link that makes the [`trace`](trace.md) check able to prove coverage.

| Layer | Convention |
|---|---|
| E2E (e.g. Playwright) | `{ tag: ['@CODE-N.M'] }` |
| Unit (e.g. Vitest) | `annotate('CODE-N.M', 'requirement')`, or the ID in the test name |
| Compiled languages (e.g. Rust) | `/// REQ: CODE-N.M` doc comment above the test |

If no requirement covers the behavior, that is a gap for tier ≥ 1 work: surface it to the user rather than shipping an untraceable test.

## Anti-patterns it names

The skill carries a table of six test smells with their tells and counters. In short:

| Anti-pattern | The tell |
|---|---|
| Tautological test | The expected value is recomputed the same way the code computes it, so it passes by construction |
| Implementation-coupled test | Breaks on refactor with no behavior change; asserts call counts, private methods, or verifies through a side channel |
| Testing mock behavior | The assertion checks that the mock exists or was called; the test fails when the mock is removed |
| Test-only methods on production classes | A method called only from test files |
| Incomplete mocks | The mock carries only the fields this test happens to read |
| Mocking your own modules | Internal collaborators stubbed out "to isolate" |

The governing rule: **mock only at system boundaries** — external APIs, time, randomness, sometimes filesystem or database. Never mock code you own. If mocking your own module seems necessary, the design is too coupled; inject dependencies instead.

Two heuristics decide when a mock has become the problem: mock setup longer than the test logic, and a test that fails when a mock is removed. Either one means prefer an integration test through real components.

## Red flags

Any of these means: delete the untested code and return to RED.

- Implementation exists and its test does not
- A new test passed on its first run
- You cannot say why the test failed in RED
- A test targets a seam not in the design's seam table
- A test has no requirement ID
- The words "just this once", "keep as reference", "spirit not ritual", or "this case is different"

## Worked example

A tier-1 bugfix on a feature whose code is `SHELL`. `debug` has already established the root cause: `restoreModule()` reads the persisted key before the store hydrates, so it always sees `undefined`.

**RED.** Write one test at the seam `design.md` names for module persistence:

```ts
// src/shell/module-store.test.ts
test('restores the persisted module after hydration [SHELL-1.2]', async () => {
  await store.hydrate({ activeModule: 'notes' })
  expect(store.activeModule).toBe('notes')   // known-good literal, not store.read()
})
```

Run the single-file command from `docs/agents/project.md`. It fails with `expected 'notes', received undefined` — the failure the root cause predicted, not an import error. That is a valid RED.

**GREEN.** Make `restoreModule()` await hydration. Nothing else. Run the full suite: the new test passes, the other 47 still pass, output pristine.

**REFACTOR.** Nothing to clean. Commit:

```
fix(shell): restore persisted module after store hydration

Implements: SHELL-1.4
Guards: SHELL-1.2
```

The ID in the test name and the ID in the trailer are what let [`trace`](trace.md) prove `SHELL-1.4` is covered, and what let [`release`](release.md) write the changelog entry as shipped behavior rather than commit prose.

Note what the expected value is *not*: `store.read('activeModule')`. That would be a tautological test — recomputing the expectation the same way the code computes it. The literal `'notes'` comes from an independent source of truth, the requirement text itself.

## Before claiming done

The skill ends on a checklist, and it hands off to [`verify`](verify.md) before any completion claim is spoken:

- Every new behavior has a test you watched fail first, for the expected reason
- Full suite green, output pristine
- Every test tagged with its requirement ID
- All tests sit at seams agreed in `design.md` (or agreed with the user)
- Mocks only at system boundaries, complete data structures, no assertions on mocks
- Edge cases and error paths covered

## Why it is written the way it is

`tdd` is a **pressure-gate skill**: the baseline failure it was written against is an agent that knows the rule and breaks it under pressure. Per [`writing-skills`](writing-skills.md), that failure class calls for a hard prohibition plus a rationalization table plus a red-flags list — which is exactly the shape of this document. The nine-row rationalization table is not padding; each row is a rationalization observed in a baseline run and countered by name.

## See also

- [The gates](../concepts/gates.md) — how `tdd`'s Iron Law relates to the other three
- [Traceability](../concepts/traceability.md) — why every test carries an ID
- [`verify`](verify.md) — the skill that decides whether "done" may be said
- [`debug`](debug.md) — the skill that must run first when the change is a fix
