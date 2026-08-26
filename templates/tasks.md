# Tasks: <Feature Name>

> **For agentic workers:** after plan approval, pick one execute skill —
> `build-in-waves` (continuous dependency-aware scheduler), `build-by-story` (human-gated story review
> units), or `build-inline` (controller implements, no implementer subagents).
> The chosen skill writes `Execution-mode:`. Steps use checkbox (`- [ ]`) syntax
> for tracking.

Feature code: <CODE>
Status: Draft
Date: <YYYY-MM-DD>
Execution-mode: unset
Max-concurrency: auto
Requirements: ./requirements.md
Design: ./design.md

**Goal:** <one sentence>

**Architecture:** <2-3 sentences>

**Tech Stack:** <languages, frameworks, test runners>

## Global Constraints

<Canonical project-wide constraints source — path plus content hash for test
commands, lint rules, i18n rules, naming conventions. Every task references this
source; execution carries a compact delta.>

## File Structure

<Map every file this plan creates or modifies and its responsibility, before any
task. A file not listed here should not be touched.>

---

### Task 1: <Component>

**Files:**
- Create: `<exact/path.ts>`
- Modify: `<exact/path.ts>`  # lines 86–103 — ranges in prose, not path:86-103
- Test: `<exact/path.test.ts>`

**Interfaces:**
- Consumes: <names + types this task uses from neighboring tasks>
- Produces: <names + types neighboring tasks will use>

**Depends-on:** <earlier tasks that must land first, e.g. `Task 1`; or `none`.
Omit the line for strict serial order. Tasks sharing no files or interfaces
declare no edge — the continuous `build-in-waves` scheduler may run those
together when worktree isolation is safe.>

- [ ] **Step 1: Write the failing test**

<complete test code block>

Run: `<exact command>` — expect: <failure message>

- [ ] **Step 2: Implement**

<complete code block — no placeholders, no "add appropriate error handling",
no "similar to Task N">

Run: `<exact command>` — expect: pass.

- [ ] **Step 3: Commit**

`git commit -m "<conventional subject explaining the change>"`

_Requirements: <CODE>-1.1, <CODE>-1.2_

---

### Task 2: ...

_Requirements: <CODE>-2.1_
