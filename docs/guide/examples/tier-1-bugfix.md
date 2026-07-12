# Example: a tier-1 bugfix

**The report:** "Sometimes when I restart the app it opens Notes instead of the module I was last in."

---

## Entry point: `debug`, not `tdd`

Something behaves unexpectedly. That is [`debug`](../skills/debug.md), and its Iron Law binds before anything else:

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

The word "sometimes" is the interesting part. It means non-deterministic, which changes the Phase 1 strategy.

## Phase 1 — Build the feedback loop (the gate)

Before reading a single line of code to form a theory, there must be **one command that is red right now because of this exact bug** and goes green when it is fixed.

> Build the right feedback loop and the bug is 90% fixed; every later phase merely consumes it.

Tactic 1 from `debug`'s ordered list — a failing test at whatever seam reaches the bug:

```ts
// src/shell/module-store.test.ts
test('restores the persisted module on startup', async () => {
  localStorage.setItem('activeModule', 'tasks')
  const store = createModuleStore()
  await store.init()
  expect(store.activeModule).toBe('tasks')
})
```

It passes. Every time.

**That is not a red-capable command**, so Phase 2 is not available. The bug is non-deterministic, and `debug` is explicit about what to do:

> Non-deterministic bug? Don't chase a clean repro — raise the reproduction rate (loop the trigger 100×, add stress, shrink timing windows) until it's high enough to debug against.

Shrink the timing window. `store.init()` awaits hydration; the real app renders before that resolves. Test what the app actually does:

```ts
test('rail reads the restored module, not the default', async () => {
  localStorage.setItem('activeModule', 'tasks')
  const store = createModuleStore()
  store.init()                          // NOT awaited — as the real app calls it
  expect(store.activeModule).toBe('tasks')
})
```

```
FAIL  expected 'tasks', received 'notes'
```

Red, deterministically, and for the user's exact symptom. **Gate check passed** — the command is named and one run of its red output is pasted.

Notice what just happened: constructing the loop *found the bug*. The failing test's shape is the root cause.

## Phase 2 — Reproduce and minimise

Run the loop; watch it go red with the failure the user described. Read the complete error. Check recent changes: `git log` shows a commit three weeks ago that made `init()` async to support a migration.

Shrink one cut at a time until every remaining element is load-bearing. Remove the `localStorage.setItem` — the test still fails, but now for a *different* reason (nothing to restore). Put it back; it is load-bearing.

## Phase 3 — Hypothesise

Three to five ranked, falsifiable hypotheses **before testing any**, because a single hypothesis anchors you to the first plausible idea. Each carries a stated prediction.

1. **`init()` returns before hydration completes, and the rail reads `activeModule` synchronously after calling it.** *Prediction: awaiting `init()` in the rail's mount makes the bug disappear.*
2. `localStorage` write is racing a `storage` event listener that resets it. *Prediction: removing the listener makes the bug disappear.*
3. The default is applied after restore rather than before. *Prediction: reordering the assignments in `init()` fixes it.*

Test the smallest first, one variable at a time. Hypothesis 1's prediction holds. Hypotheses 2 and 3 are struck without being tried, because 1 explains the whole symptom including the "sometimes" — the race resolves differently depending on whether `localStorage` reads hit a warm cache.

**Root cause:** `restoreModule()` reads the persisted key before the store hydrates, so it sees `undefined` whenever hydration has not yet resolved.

## Phase 4 — Fix

**Failing regression test first**, via [`tdd`](../skills/tdd.md), at a *correct* seam — one that exercises the real bug pattern as it occurred. The Phase 1 loop already *is* that test.

**One fix**, addressing the root cause. No "while I'm here" improvements:

```ts
async init() {
-   this.activeModule = this.read('activeModule') ?? 'notes'
    await this.hydrate()
+   this.activeModule = this.read('activeModule') ?? 'notes'
}
```

Watch the regression test pass. Re-run the full suite. Re-run the Phase 1 loop against the original un-minimised scenario.

## Exit — the tier-1 mini-spec

This is where `debug` hands to [`write-requirements`](../skills/write-requirements.md), and the tier-1 ceremony is exactly **two criteria** appended to `SHELL`'s existing `requirements.md`:

```markdown
- **SHELL-1.8** WHEN the app starts with a persisted module THE SYSTEM SHALL
  activate that module after the store has hydrated.
- **SHELL-1.9** (guard) WHEN the store hydrates THE SYSTEM SHALL CONTINUE TO
  preserve unsaved editor state.
```

The first is the fix. The second is the **guard** — and finding it required actively searching what else `init()` touches, because `write-requirements`' completion criterion for that step forbids the lazy answer:

> You have **actively searched** the touched surface for behaviors to guard — not merely found none by default.

Moving the assignment after `await this.hydrate()` means the editor's state restoration now runs *before* the module is set. Does anything depend on that ordering? A test tagged `@SHELL-1.9` now asserts it does not.

Both IDs get tagged onto tests:

```ts
test('activates the persisted module after hydration [SHELL-1.8]', …)
test('preserves unsaved editor state across hydration [SHELL-1.9]', …)
```

## Cleanup and post-mortem

`debug`'s exit checklist:

- **Remove ALL instrumentation.** `grep` for the `[DBG-x7q2]` prefix used during Phase 3. Delete throwaway harnesses.
- **State the confirmed root cause in the commit message.**
- **Ask: what would have prevented this bug?**

```
fix(shell): activate the persisted module after store hydration

restoreModule() read the persisted key before hydrate() resolved, so it saw
undefined whenever hydration had not yet completed — which depended on whether
the localStorage read hit a warm cache. Hence "sometimes".

Implements: SHELL-1.8
Guards: SHELL-1.9
```

The post-mortem answer here is architectural: `init()` had no seam at which "hydrated" was observable, which is why the original test could only be written the wrong way. That specific finding goes to `/improve-architecture` — **after the fix lands, when you know the most.**

## `verify`, then finish

```
IDENTIFY → the full suite plus the trace check
RUN      → fresh, complete
READ     → exit 0, 50 passing, zero warnings; trace check clean
CONFIRM  → SHELL-1.8 and SHELL-1.9 each have a covering test
```

And the regression-proof pattern, because a regression test only counts once it has demonstrably caught the bug:

```
write test → passes → revert the fix → test MUST fail → restore fix → passes
```

Then `code-review` (Spec axis, against the two new IDs) and `finish-branch`.

---

## The whole ceremony, counted

Two requirement criteria. Two tagged tests. One three-line fix. One commit with two trailers.

No `design.md`. No `tasks.md`. No `execute-plan`.

What tier 1 bought that a bare fix would not have: the guard requirement, which is now a permanent, machine-checked assertion that hydration does not eat unsaved editor state — a behavior nobody would have thought to protect, found only because the process required actively looking for it.

## See also

- [Ceremony tiers](../methodology/ceremony-tiers.md) — the mini-spec in context
- [`debug`](../skills/debug.md) — the four phases and the red-capable command gate
- [EARS reference](../resources/ears.md) — why guards get their own section
- [Tier 2: a full feature](tier-2-feature.md)
