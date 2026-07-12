---
name: tdd
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

Exceptions exist only with the user's explicit permission: throwaway prototypes, generated code, pure configuration. "Skip it just this once" is not an exception; it is the rationalization this skill exists to block.

## Where tests go: pre-agreed seams

A seam is a public surface where behavior is observable without reaching into internals. Tests live only at seams listed in the feature's `design.md` under **Seams for testing**. Refuse to write a test at a seam that table does not confirm. No `design.md` for this work (tier 0/1 change, legacy area)? Propose the seam(s) to the user and get agreement before the first test. Testing effort is a budget — agreed seams put it on critical paths instead of on every internal detail.

## The loop

Work one vertical slice at a time: one behavior → one test → one minimal implementation → repeat. Each cycle responds to what the previous one taught you. Never write all the tests up front and then all the code — bulk-written tests verify imagined behavior.

**RED — write one failing test.** One behavior, a name that states the behavior, expectations against real code at an agreed seam. Tag it with the requirement ID it verifies (see below). Fixing a bug? REQUIRED SUB-SKILL: use `debug` to establish the root cause first — the RED test must reproduce *that* bug, failing for the bug's reason, before any fix.

**Verify RED — mandatory, never skip.** Run the test (single-file command from `docs/agents/project.md`). Confirm it fails, that the failure message is the one you expected, and that it fails because the behavior is missing — not because of a typo or import error. **Test passes immediately?** You are testing behavior that already exists — fix the test, not the code. Test errors instead of failing? Fix the error and re-run until it fails correctly.

**GREEN — write the simplest code that passes.** No speculative parameters, no extra features, no touching unrelated code.

**Verify GREEN — mandatory.** Run the full suite. Confirm: the new test passes, every other test still passes, and the output is pristine — zero warnings, zero stray errors, nothing you're "planning to clean up". New test fails? Fix the code, never loosen the test. Other tests fail? Fix now, before anything else.

**REFACTOR — only while green.** Remove duplication, improve names, extract helpers. Re-run the suite after each change. Add no behavior.

Then take the next slice.

## Requirement tagging

Every test carries the ID of the requirement it verifies, using the conventions in `docs/agents/project.md` (Test annotation conventions table). Typical forms:

| Layer | Convention |
|---|---|
| E2E (e.g. Playwright) | `{ tag: ['@CODE-N.M'] }` |
| Unit (e.g. Vitest) | `annotate('CODE-N.M', 'requirement')` or the ID in the test name |
| Compiled languages (e.g. Rust) | `/// REQ: CODE-N.M` doc comment above the test |

No requirement covers the behavior? For tier ≥1 work that is a gap — surface it to the user rather than shipping an untraceable test. If `docs/agents/project.md` is missing, say so, suggest running `setup-repo`, and fall back to putting the ID in the test name.

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

## Red flags — stop and start over

- Implementation exists and its test doesn't
- A new test passed on its first run
- You can't say why the test failed in RED
- A test targets a seam not in the design's seam table
- A test has no requirement ID
- "Just this once", "keep as reference", "spirit not ritual", "this case is different"

Any of these: delete the untested code, return to RED.

## Before claiming done

- [ ] Every new behavior has a test you watched fail first, for the expected reason
- [ ] Full suite green, output pristine (zero warnings/errors)
- [ ] Every test tagged with its requirement ID per `docs/agents/project.md`
- [ ] All tests sit at seams agreed in `design.md` (or agreed with the user)
- [ ] Mocks only at system boundaries, complete data structures, no assertions on mocks
- [ ] Edge cases and error paths covered

Can't tick a box? The work isn't done. REQUIRED SUB-SKILL: use `verify` before any completion claim.
