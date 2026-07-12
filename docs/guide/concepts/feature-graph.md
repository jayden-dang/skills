# Feature overlap

The [trace check](traceability.md) is the **vertical** layer: it proves that one feature's requirements, tasks, and tests agree with each other.

Feature overlap is the **horizontal** question — *which features touch the same code, and does this new idea already exist somewhere?* It is answered by searching the specs that already exist, so there is nothing to generate and nothing that can go stale.

## The problem

An agent asked to "add a keyboard shortcut for switching modules" has no way to know that a feature called `CHIPUI` already owns half the files it is about to edit, and that its Out-of-Scope section explicitly declined keyboard shortcuts three months ago.

The information exists. It is spread across a dozen `requirements.md`, `design.md`, and `tasks.md` files nobody is going to read — unless something reads them at the two moments it matters.

## How overlap is found

There is no index to build and no derived file to maintain. When a skill needs to know a feature's neighbors, it runs an inline `grep` over `docs/specs/`:

- the idea's or diff's **candidate file paths** — the source files it will create or touch — find features whose specs already name those paths;
- the idea's **key terms** find features that describe the same behavior in prose.

Any feature whose spec matches on either is a neighbor. The source of truth is the specs as they stand; a path already written in a task's `Files: Create:` block or a `design.md` section is what the search reads.

## The Summary card

A matched neighbor is loaded as its **Summary card**, not its full spec — a bounded per-feature digest sitting at the top of the spec: the feature code, its name, the paths it owns, and its Out-of-Scope list. The card lets the agent grasp a neighbor's essence — what it already covers and what it deliberately declined — without pulling a whole design document into context.

A card reads roughly like this:

```markdown
### CHIPUI — Module chip rail
- owns: src/shell/chip-rail.tsx, src/shell/module-store.ts
- interfaces: useActiveModule() → Module, setActiveModule(id)
- out-of-scope: keyboard shortcuts for switching | drag-to-reorder
```

That single Out-of-Scope line is often the whole answer: the new idea was already considered here and set aside, with a reason.

## `docs/specs/INDEX.md` — the registry

`INDEX.md` is the sole feature registry. Every feature code is unique repo-wide, forever, and is registered here — by [`write-requirements`](../skills/write-requirements.md) — before the requirements file that uses it is written. It is the one place that enumerates every feature, so an overlap search always knows the full set of neighbors to consider.

```markdown
| Code | Feature | Spec | Status |
|---|---|---|---|
| SHELL | Left icon rail for module switching | ./2026-07-09-shell/ | Implemented |
| CHIPUI | Module chip rail | ./2026-04-02-chip-rail/ | Shipped |
```

## Where overlap is consumed

Exactly two gates look for neighbors, and both do so *advisorily*.

**[`brainstorm`](../skills/brainstorm.md), at the front of the chain.** Before the interview begins, it searches `docs/specs/` with the scan's candidate files and the idea's key terms. Any matching features are presented as their **Summary cards** — each card's owned paths and Out-of-Scope list show what the neighbor already covers.

Its completion criterion is a sentence the agent must be able to say: *which existing features share this idea's surface and how the new idea differs, citing feature codes — or that no existing feature shares its surface.*

**[`code-review`](../skills/code-review.md), at the back of the chain.** It searches with the diff's changed source files. When a neighbor comes back, the **Spec** subagent receives its card, with a brief directing it to flag — as a *reuse-miss* finding citing the neighbor's feature code — any place the diff reimplements behavior a neighbor already owns.

## An advisory signal, never a gate

The overlap search never fails a review and never stops a brainstorm. It sharpens a decision; it does not make one. If the search returns nothing, the agent proceeds and says so. If `docs/specs/` is empty or a young repo has few specs, that is simply a thin neighborhood, not an error state.

This keeps the horizontal layer honest: it costs a `grep`, it reads only what is already written, and it can never be stale, because there is no derived copy of anything to fall behind.

## See also

- [Traceability](traceability.md) — the vertical layer this sits beside
- [Enforcement and tooling](../resources/scripts.md#feature-overlap-search) — the search mechanics
- [Artifacts](artifacts.md) — where `INDEX.md` and the specs live
- [`brainstorm`](../skills/brainstorm.md) — the overlap check at the front of the chain
- [`code-review`](../skills/code-review.md) — the reuse-miss check at the back
