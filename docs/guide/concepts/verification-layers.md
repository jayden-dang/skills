# Verification layers

Four independent *methods* this pack uses to check work. They are not a
fifth Iron Law and not a fifth skill. Each layer is enforced by the skill
in the table — not by this page.

**Skills do not load this file at runtime.** A consuming repo that installed
the pack via `npx skills add` does not even have `docs/guide/`. If an agent
needs a layer, it follows that layer's SKILL.md. This page is the map so a
human (or a later author) can see which method is which — and which gap is
already closed — without inventing a Guide-Verify-Solve skill.

The four Iron Laws stay in [The gates](gates.md). Those are *when* the
agent is forbidden to proceed. These layers are *how* a check is performed.

## The four layers

| Layer | Method | Same result if someone else runs it? | Skills (the home) |
|---|---|---|---|
| **Computational** | Tests, typecheck, lint, `audit-trace` greps | Yes — exit code / same `grep` set | `test-first`, `prove-claim`, `audit-trace`, verify commands in `docs/agents/project.md` |
| **Judgment** | Isolated LLM review of a diff | No — another model can disagree | `inspect-change` (Standards + Spec), `polish-diff`, `inspect-invariants` (advisory) |
| **Behavioral** | Drive the running system as a client | Mostly — same request, same UI | `validate-feature` → `validate-api` / `validate-ui`; product-walk trio when the walk predicate holds |
| **Human** | A person reads a bounded sample or configures a decision boundary | N/A | `/select-sample`; `/record-debt`; configured `record-verdict` |

A layer does not replace another. Green tests do not make inspect optional.
A close receipt does not replace a missing check; it binds completed checks to
the exact revision so landing can validate instead of replay them.

## What each layer is *not*

- **Computational** is not a new `scan-code` skill. The pack does not
  install SAST into consumers. If the repo already has a scanner, it is a
  verify command in `project.md` and `prove-claim` / `land-branch` run it.
- **Judgment** is not independent of *method* from the implementer (both
  are LLMs). Independence here is **context**: a fresh reviewer subagent,
  two unmerged axes, no “do not flag”.
- **Behavioral** is not “the unit tests were green.”
- **Human** attention remains advisory. `/select-sample` never withholds
  a crossing after review and acceptance evidence is bound to the receipt.

## Where it sits in the close sequence

`execute-common` already sequences the layers. It does not read this page
to do that.

```
inspect-change          ← judgment
  → fixer → re-review
  → polish-diff?        ← judgment (conditional)
  → validate-feature    ← behavioral
  → sample notes        ← write sample: required or skip (no human ping)
  → walk?               ← behavioral (conditional)
  → close receipt       ← binds all layers to base + HEAD
  → land-branch         ← resolves intent and performs the crossing
```

Banked Minors / scope-drops leave a paste-ready body for `/record-debt`.
That is how a judgment leftover becomes a durable human record.

## See also

- [The gates](gates.md) — *when* work is forbidden
- [`execute-common`](../skills/execute-common.md) — close-sequence home
- [`land-branch`](../skills/land-branch.md) — exact-revision receipt consumer
- [`inspect-change`](../skills/inspect-change.md) — two-axis judgment
- [`prove-claim`](../skills/prove-claim.md) — computational claim gate
- [`select-sample`](../skills/select-sample.md) — human allocation
