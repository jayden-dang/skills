# Example: a tier-0 tweak

**The request:** "The active module icon in the rail should be indigo, not blue."

This is the smallest possible unit of work the system handles. It is here because the interesting part is what *does not* happen.

---

## The feature already has a spec

`SHELL` shipped months ago. Its `requirements.md` is `Status: Shipped`. So this is not `brainstorm` — it is [`amend`](../skills/amend.md), the lane for a small in-scope change to an already-shipped, spec'd feature.

## Step 1 — Ground the change in the existing spec

`amend` finds the spec via `docs/specs/INDEX.md`, reads the requirements the change touches, and the design section that owns them.

```markdown
- **SHELL-1.7** WHILE a module is active THE SYSTEM SHALL render its rail icon
  in the accent color.
```

**Done when: you can name the requirement IDs the change affects.** Here, `SHELL-1.7`.

## Step 2 — Classify the change, out loud

> This is **tier 0**. `SHELL-1.7` says the active icon renders "in the accent color" — it does not name the color. Changing the accent token from blue to indigo leaves every existing acceptance criterion reading true, unchanged. No behavior changes; only a token value does.

That sentence *is* the design step. Note what it required: reading the requirement carefully enough to notice it specifies a *role* (accent color) rather than a *value* (blue). Had `SHELL-1.7` said "in blue", this would be tier 1 — the requirement's text would be false after the change, and it would need amending plus a guard.

The distinction is not pedantry. It is the difference between a change that keeps the spec true and one that quietly makes it lie.

## Step 3 — `tdd`, because every path exits through it

Tier 0 is not an exemption from the test-first gate. From `amend`:

> This is a fast lane, not a gate bypass. Every path still exits through `tdd`.

There is no `design.md` seam table entry for "the color of the rail icon", so `tdd` proposes the seam and gets agreement first:

> No seam in `design.md` covers icon color. I propose asserting on the computed accent token in `theme.test.ts` — the existing unit seam for theme resolution — rather than snapshotting the rendered rail, which would break on unrelated layout changes. Agreed?

**RED:**

```ts
// src/theme/theme.test.ts
test('accent color is indigo [SHELL-1.7]', () => {
  expect(resolveTheme('light').accent).toBe('#4f46e5')   // indigo-600
})
```

Run the single-test-file command from `docs/agents/project.md`. It fails:

```
expected '#4f46e5', received '#2563eb'
```

That is a valid RED — it fails because the value is the old one, not because of a typo or a missing import.

**GREEN:** change one token. Run the full suite. 48 passing, output pristine.

**REFACTOR:** nothing.

## Commit

```
style(shell): use indigo for the active module accent

Implements: SHELL-1.7
```

The trailer cites `SHELL-1.7` because that is the requirement this change serves — the criterion did not change, but the code implementing it did.

## Step 4 — `verify`

Before the word "done" is spoken. `check-trace` is clean; `SHELL-1.7` still has a covering test; the full suite ran fresh in this session and its output was read.

---

## What did *not* happen

No `brainstorm`. No `requirements.md` edit. No `design.md`. No `tasks.md`. No `worktrees`. No `execute-plan`. No `code-review` subagents. Total artifacts produced: one changed token, one changed test, one commit.

**But the tier was named out loud, and the change was verified against the actual requirement text before it was named.** That is the entire ceremony, and it took one paragraph.

## Where this would have escalated

Three variations that are *not* tier 0, and how `amend` catches each:

| Variation | Tier | Why |
|---|---|---|
| `SHELL-1.7` had said "render its rail icon in blue" | **1** | The requirement's own text becomes false. Amend the criterion, add a `SHALL CONTINUE TO` guard for whatever else consumes the accent token, then `tdd` |
| "…and add a subtle glow animation" | **1** | New observable behavior extending a spec'd one. Mini-spec |
| "…and let users pick their own accent color" | **new scope** | A real UX decision with live alternatives (per-user? per-workspace? persisted where?). `amend` stops and escalates to `brainstorm` |

The honest test for that last row, from `amend`:

> Does the existing spec's intent already cover this behavior? **If you are inventing what it should do, it is new scope.**

Nothing in `SHELL`'s spec says anything about who chooses the accent color. Inventing that answer inside a "recolor the icon" request is exactly the failure `amend`'s red flags name: *the "small" change grew a design decision with real alternatives.*

And if the request had bundled both — "make it indigo, and let users pick their own" — `amend` splits it: the tweak stays in the fast lane, the new behavior goes to `brainstorm`. Route each half separately.

## See also

- [Ceremony tiers](../methodology/ceremony-tiers.md) — the full three-tier system
- [`amend`](../skills/amend.md) — the skill this example runs
- [Tier 1: a bugfix](tier-1-bugfix.md) — the next step up
