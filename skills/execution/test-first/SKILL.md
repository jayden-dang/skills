---
name: test-first
version: 1.3.0
description: Use when writing or changing any production code — a new feature, a bugfix,
  a behavior change, or a refactor — and before the first line of
  implementation exists; the test-first (TDD) gate. Also use when about to add
  a mock, a test utility, or a test to existing untested code.
---

# TDD

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Wrote implementation before the test? Delete it. Not "keep it as reference", not "adapt it while the tests catch up" — you will end up testing what you built instead of what was required. Delete means delete; implement again from the test. Violating the letter of this law is violating the spirit of it.

Exceptions exist only with the user's explicit permission: throwaway run-spikes, generated code, pure configuration. "Skip it just this once" is not an exception; it is the rationalization this skill exists to block.

## Where tests go: pre-agreed seams

A seam is a public surface where behavior is observable without reaching into internals. Tests live only at seams listed in the feature's `design.md` under **Seams for testing**. Refuse to write a test at a seam that table does not confirm. No `design.md` for this work (tier 0/1 change, legacy area)? Propose the seam(s) to the user and get agreement before the first test. Testing effort is a budget — agreed seams put it on critical paths instead of on every internal detail.

## The loop

Work one vertical slice at a time: one behavior → one test → one minimal implementation → repeat. Each cycle responds to what the previous one taught you. Never write all the tests up front and then all the code — bulk-written tests prove-claim imagined behavior.

**RED — write one failing test.** One behavior, a name that states the behavior in
domain language, expectations against real code at an agreed seam. Do **not**
require embedding a requirement ID in application or test source (docs-only
spine). Map the test to its requirement ID in the task report / Spec review.
Look for an existing check at that seam first. Extend it when the same setup
can expose the new failure. A second check earns its setup by witnessing a
different failure or boundary. Name the expected result from the requirement
or an independent worked example before running.
Fixing a bug? REQUIRED SUB-SKILL: use `root-cause` to establish the root cause
first — the RED test must reproduce *that* bug, failing for the bug's reason,
before any fix.

**Verify RED — mandatory.** Run the check with the project's narrow command.
For behavioral RED record the assertion reached and expected versus observed
result. Fix a missing symbol, setup error or unrelated timeout before counting
RED. A compile-time contract uses its explicitly expected diagnostic.
If a check passes immediately, compare it to the required change. Fix a weak
assertion or record an unchanged-behavior guard separately. A guard cannot
replace the failing test for changed behavior.

**Time and ordering.** Use the repo's controllable clock for logical time and
observable synchronization for race ordering. Put a deadline around the wait.
Use elapsed real time when the contract itself needs that measurement.

**GREEN — write the simplest code that passes.** No speculative parameters, no extra features, no touching unrelated code.

**Verify GREEN — mandatory.** Run the narrowest command that builds and runs the new test's target (the single-file pattern). Confirm: the new test passes, every other test in that run still passes, and the output is pristine — zero warnings, zero stray errors, nothing you're "planning to clean up". New test fails? Fix the code, never loosen the test. Other tests fail? Fix now, before anything else.

**REFACTOR — only while green.** Remove duplication, improve names, extract helpers. Re-run that same command after each change. Add no behavior.

Then take the next slice.

## The task gate — once, before you claim the work done

Each step above stays narrow. Run the task gate at the final commit by default.
If a continuous build brief explicitly assigns broad checks to its configured
integration gate, run fresh narrow checks at the final commit and report scope
and shared inputs. The controller verifies the integrated revision before
marking the task complete. All other work uses the task gate:

1. **Test what can see the change.** Use the project's **Task gate** command and
   its declared scope. Include changed units and affected callers and boundaries.
   Build or typecheck the remaining dependents when the repo has that check.
   Without a configured selector, use the repo's dependency data and check
   consumers of changed interfaces and shared inputs. Choose the full suite
   if you cannot establish the scope. A text search alone cannot rule out a consumer.
2. **Lint and format** over the same units, against the lint baseline recorded at session start. A finding absent from the baseline is yours. Never suppress a lint rule to get past a red baseline.
3. **Escalate to the whole suite** when the change reaches what the build graph cannot see: schema or migrations, shared fixtures or test data, build manifests or feature flags, generated contracts, a root package nearly everything depends on. You judge it and name the reason.

When the whole suite is cheap (a couple of minutes), it *is* the gate — run it. Report the scope you ran: `Task gate: <commands> — tested <units> (changed) + <units> (calls <item>); compiled <units>`, or `Whole suite: <command> — escalated: <reason>`. A gate run is never quoted as the suite; the whole suite runs at close.

## Requirement linkage (docs-only)

Requirement IDs live in `docs/specs/**` (`requirements.md`, design `Satisfies:`,
task `_Requirements:` footers). Tests prove **behavior** in domain language.

- **Do not** require `/// REQ:`, `@CODE-N.M`, or IDs in test titles for consumer
  application code. Legacy annotations are ignored by `audit-trace`.
- **Do** ensure each new behavior maps to a requirement in the task brief; if no
  requirement covers it, surface the gap (tier ≥1) rather than inventing scope.
- **Exception:** this skill-set repository's own pack tests may embed greppable
  `CODE-N.M` tokens as **product fixtures** testing the pack — that is not a
  consumer convention.

If `docs/agents/project.md` is missing, say so and suggest `configure-repo`;
still write domain-named tests at agreed seams.

### Testing standards doc (optional)

Read approved `docs/standards/testing.md` for test layers, seam and dependency
rules. Commands come from `docs/agents/project.md`. Apply the project rules
alongside the Iron Law. When the standard is absent, use the repo's existing
tests and the agreed design. Suggest `/define-project standards/testing` once
only when a missing standard matters to the change.

## Anti-patterns and their counters

| Anti-pattern | Tell | Counter |
|---|---|---|
| Tautological test | Expected value is recomputed the same way the code computes it (`expect(sum(items)).toBe(items.reduce(...))`), so it passes by construction | Expected values come from an independent source of truth: a known-good literal, a worked example, the requirement text |
| Implementation-coupled test | Breaks on refactor with no behavior change; asserts call counts/order, private methods, or verifies through a side channel (raw DB query instead of the interface) | Assert observable behavior through the public seam only |
| Testing mock behavior | Assertion checks the mock exists or was called; test fails when the mock is removed | Test the real component, or stop asserting on the mock entirely |
| Test-only methods on production classes | A method (e.g. `destroy()`) called only from test files | Move it to a test utility; production classes carry production API only |
| Incomplete mocks | Mock carries only the fields this test happens to read; integration breaks on omitted fields | Mirror the complete real data structure — every field the real response contains |
| Mocking your own modules | Internal collaborators stubbed out "to isolate" | Mock only at system boundaries (external APIs, time, randomness, sometimes FS/DB). Never mock code you own — if that seems necessary, the design is too coupled: inject dependencies instead |

Mock setup longer than the test logic, or a test that fails when a mock is removed, means the mock is the problem — prefer an integration test through real components.

## Rationalizations

| Thought | Reality |
|---|---|
| "Too simple to test" | Simple code breaks too; the test costs a minute |
| "I'll add tests right after" | A test written after passes immediately and proves nothing — you never saw it catch anything |
| "Tests-after achieve the same thing in spirit" | Tests-after answer "what does this do?"; tests-first answer "what should this do?" — the first is biased by your implementation |
| "I already exercised it manually" | Ad-hoc, unrecorded, unrepeatable. It vanishes on the next change |
| "Deleting hours of work is wasteful" | Sunk cost. Untested code you keep is the actual waste |
| "Keep it as reference while I write tests" | That is testing after, with extra steps |
| "The test is hard to write" | Hard to test means hard to use — simplify the interface, don't skip the test |
| "TDD slows me down" | Slower than typing, faster than debugging |
| "This file has no tests anyway" | You're changing it; your change gets a test |
| "Run the whole suite on every GREEN to be safe" | Six 18-minute runs per task buys nothing the task gate and the close run don't. Narrow each step; gate once |
| "The scoped run passed — tests pass" | Name the scope you ran. "Tests pass" is the whole suite's claim |
| "Lint was already red, so allow the rule / it can't be checked" | Compare against the baseline. Suppressing the rule hides your findings with the old one |
| "It's only a migration file, the crate tests cover it" | Every test reads that schema. Escalate |
| "Run every dependent's tests to be safe" | A dependent that never calls the changed code cannot see it — compiling it proves the signature still fits. Follow the callers; test the units they reach |
| "The selector matched no source path" | Check shared inputs and the consumers the selector covers. An unknown input or an unexplained empty scope requires the full check |

## Red flags — stop and start over

- Implementation exists and its test doesn't
- A green guard is used as RED evidence for changed behavior
- You can't say why the test failed in RED
- A test targets a seam not in the design's seam table
- A new behavior has no mapping to a requirement in the brief (tier ≥1)
- "Just this once", "keep as reference", "spirit not ritual", "this case is different"

Any of these: delete the untested code, return to RED.

## Before claiming done

- [ ] Every new behavior has a test you watched fail first, for the expected reason — error paths and boundary values count as behaviors
- [ ] Configured scope verified and named at its scheduled gate, with no lint finding outside the baseline. For lane handoff under integration placement, final narrow evidence and affected inputs recorded, integration still pending until verified by the controller
- [ ] Each new behavior maps to a requirement in the task brief / report (IDs stay in docs, not required in test source)
- [ ] All tests sit at seams agreed in `design.md` (or agreed with the user)
- [ ] Mocks only at system boundaries, complete data structures, no assertions on mocks

Can't tick a box? The work isn't done. REQUIRED SUB-SKILL: use `prove-claim` before any completion claim.
