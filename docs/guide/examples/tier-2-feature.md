# Example: a tier-2 feature, end to end

**The request:** "We should let people switch between modules — Notes, Tasks, Calendar — from a left icon rail."

This is the full chain. Every gate, every artifact, every hand-off.

---

## `brainstorm` — the hard gate

No code. No scaffolding. No implementation skill. Not yet.

### 1. Explore project context

`CONTEXT.md` and `docs/specs/INDEX.md` are read directly — small, and needed in context. Everything heavier goes to a **scan subagent**, which writes a digest to `.skills/module-rail-scan.md` and returns only that path.

Then the [feature-overlap](../concepts/feature-graph.md) search — an inline `grep` over `docs/specs/` for the idea's key terms and candidate paths:

```bash
grep -rli -e 'module' -e 'rail' -e 'src/app/Layout.tsx' docs/specs/
```

One spec matches. Read as its Summary card, it is `CHIPUI`, which owns `src/ui/Chip.tsx` and `src/ui/Rail.tsx`, and whose Out-of-Scope section says *"Navigation behavior — Rail is presentational only."*

That is exactly the information the check exists to surface. The new feature will *consume* `CHIPUI`'s rail component rather than build one, and `CHIPUI` explicitly declined to own the navigation behavior.

> **Done when:** you can state what already exists near this idea and how the new idea differs, citing feature codes. → *"`CHIPUI` owns the rail's presentation and explicitly excludes navigation. `SHELL` will own module switching and persistence, consuming `CHIPUI`'s `<Rail>`."*

### 2. Interview

[`grilling`](../skills/grilling.md) takes over: one question per message, each shipping a recommended answer and a one-line reason.

> **Q:** When the app starts for the very first time, with nothing persisted, which module should be active?
> **Recommendation:** Notes — it is the module with the lowest activation cost, and it is what users open most.

> **Q:** If the persisted module id names a module that is no longer installed, what should happen?
> **Recommendation:** Fall back to Notes and log a warning. Silently falling back hides an upgrade bug; hard-failing on startup punishes the user for ours.

Meanwhile [`domain-modeling`](../skills/domain-modeling.md) runs as a side effect. The user says "pane" and then "panel" for the same thing. `CONTEXT.md` gets a term, **inline, the instant it settles**:

```markdown
**Module**:
A top-level application area with its own route, icon, and persisted state.
_Avoid_: pane, panel, section, tab
```

### 3. Detour when a question needs evidence

> **Q:** Should the persisted selection live in `localStorage` or the OS keychain?

Nobody knows what the Tauri v2 store plugin guarantees on a hard kill. That is not a preference — it is a fact about an external system, so it detours to [`research`](../skills/research.md), which reads the plugin's actual source and returns one cited markdown file ending in an **Open decisions** section.

Research informs. It does not decide. The decision goes back through `grilling`.

### 4. Propose approaches

Three, with trade-offs, recommendation first. The user picks a hybrid.

### 5. Decide the ceremony tier — out loud

> **This is tier 2** because it introduces new persisted state, a new startup path, and a new interaction surface — four or five tasks, each deserving its own review verdict.

### 6. Terminal state

`write-requirements` is invoked. **That is the only exit.**

---

## `write-requirements` — WHAT

Register `SHELL` in `docs/specs/INDEX.md` **first**, with `Status: Draft`.

```markdown
# Requirements: Module Shell
Feature code: SHELL
Status: Draft

## 1. Module switching

**Story:** As a user, I want a left icon rail so I can switch modules.

- **SHELL-1.1** WHEN the app starts with no persisted module THE SYSTEM SHALL
  activate the Notes module.
- **SHELL-1.2** WHEN the user selects a module THE SYSTEM SHALL persist the
  selection and restore it on next launch.
- **SHELL-1.3** (guard) WHEN the user switches modules THE SYSTEM SHALL
  CONTINUE TO preserve unsaved editor state.
- **SHELL-1.4** IF the persisted module id matches no installed module THEN THE
  SYSTEM SHALL activate Notes and log a warning.

## Out of Scope

- Keyboard shortcuts for module switching — the rail is pointer-only in v1.
- Reordering modules in the rail.
```

`SHELL-1.3` exists because step 3's completion criterion demanded an active search for behaviors to guard. The editor's unsaved state is the one nobody would have mentioned.

**Self-review** runs four passes — ambiguity, testability, placeholders, and a **code-claim check** dispatched to a review subagent, because `SHELL-1.3` asserts that unsaved editor state *currently* survives. Does it? The subagent greps, cites `editor/state.ts:88`, and confirms it. Had it not, the criterion would be a false premise poisoning design, plan, and code.

Then the **file** is presented, and the skill stops. On approval: `Status: Approved`. From this moment the IDs are immutable.

---

## `write-design` — HOW

A scan subagent maps the touched surface into `.skills/shell-scan.md`. Design against the digest.

```markdown
### Module store

Satisfies: SHELL-1.1, SHELL-1.2, SHELL-1.4

A single `moduleStore` owning `activeModule` and its persistence…

### Rail integration

Satisfies: SHELL-1.3

Consumes `CHIPUI`'s presentational `<Rail>`; adds no rendering of its own…
```

Every section carries `Satisfies:`. A section without one is either infrastructure — and says so — or does not belong here.

**The seam table** — the contract [`tdd`](../skills/tdd.md) will hold you to:

| Seam | Kind | Covers |
|---|---|---|
| `moduleStore` public API | unit | SHELL-1.1, SHELL-1.2, SHELL-1.4 |
| rail → editor state | e2e | SHELL-1.3 |

Two seams, both existing. The ideal number of *new* seams is zero or one.

Then an **independent design review subagent** verifies every named seam, signature, and data path against real code, citing `file:line`, defaulting to flag.

### It finds something

> `SHELL-1.2` says "persist the selection and restore it on next launch". The design's persistence path writes to the Tauri store, which the research note says is flushed asynchronously and may lose the last write on a hard kill. "Restore it on next launch" is not guaranteed as written.

This triggers **upstream sync-back**, and the rule is unambiguous:

> You MUST correct the requirement's own text and re-surface it for approval — never satisfy a requirement by quietly reinterpreting words you now know are false. A `Satisfies:` line pointing at a requirement whose wording is wrong makes the trace spine **cite a lie**.

`SHELL-1.2` is amended to say "…restore it on next launch, provided the store was flushed", a new `SHELL-1.5` covers the hard-kill case, and both go back through the approval gate.

---

## `write-plan` — the PLAN

Written for an implementer who is skilled but knows **nothing** about this codebase and will see **only their own task** plus the Global Constraints.

```markdown
## Global Constraints
- Tests: `pnpm vitest run`  |  Single file: `pnpm vitest run <path>`
- Every test carries its requirement ID in the title: `[SHELL-N.M]`
- Never import from `src/ui/` internals; consume CHIPUI's public exports only.

## File Structure
| Path | Responsibility |
|---|---|
| `src/shell/module-store.ts` | owns activeModule + persistence |
| `src/shell/module-store.test.ts` | unit tests at the store seam |

---

### Task 2: Persist and restore the active module

**Files:**
- Modify: `src/shell/module-store.ts:12-40`
- Test: `src/shell/module-store.test.ts`

**Interfaces:**
- Consumes: `Store` from `@tauri-apps/plugin-store`
- Produces: `moduleStore.setActive(id: ModuleId): Promise<void>`

**Depends-on:** Task 1

- [ ] **Step 1: Write the failing test**
      test('restores the persisted module after hydration [SHELL-1.2]', …)
      Run: `pnpm vitest run src/shell/module-store.test.ts` — expect:
      `expected 'tasks', received 'notes'`

- [ ] **Step 2: Implement**  <complete code, no placeholders>
- [ ] **Step 3: Commit**  `git commit -m "…"  # trailer: Implements: SHELL-1.2`

_Requirements: SHELL-1.2, SHELL-1.5_
```

**The coverage check goes further than the trace check can.** The trace check confirms every Approved ID is cited by a task footer. But a footer is not a test — a footer-only citation passes as a `W1` warning now and fails as an **`E2` error** the moment the spec flips to `Implemented`. So `write-plan` also requires every ID to appear in a **test annotation inside a task's steps**, and reconciles that against the design's seam table. An ID the design promised and the plan left untagged is *dropped coverage*.

An **independent plan review subagent** then verifies every symbol, signature, path, import, and **hardcoded test value** against real code. A fabricated golden value is the classic plan defect.

---

## `worktrees` → `execute-plan`

An isolated workspace, dependencies installed, and a **clean baseline**. Baseline red would stop everything — you cannot tell your bugs from pre-existing ones.

Then the loop, per task:

```
BASE=$(git rev-parse HEAD)              ← before dispatch, always
assemble .skills/task-2-brief.md        (copy the task block + Global Constraints verbatim)
dispatch a FRESH implementer            (model stated explicitly; mid tier — prose task)
  → it reads only the brief, works test-first via tdd,
    commits with the trailer, writes .skills/task-2-report.md
    with RED and GREEN evidence, and returns DONE in ≤15 lines
git diff $BASE..HEAD                     → .skills/review-a1b2c3d..e4f5g6h.diff
dispatch a task reviewer                (two verdicts: Spec Compliance, Code Quality)
```

The reviewer returns **Important: `SHELL-1.5`'s hard-kill path has no test — the report claims coverage but the diff shows none.** So: a **fix subagent** (never the controller's own context — that pollutes it), then a **re-review**. Clean.

```
append to .skills/progress.md:
  Task 2: complete (commits a1b2c3d..e4f5g6h, review clean)
```

Then straight to Task 3. No "should I continue?" — the user asked for the plan to be executed.

That ledger line is the most important artifact in the loop. If the session compacts, the controller trusts `.skills/progress.md` and `git log` over its own memory. Controllers that trusted memory have re-dispatched entire completed task sequences.

---

## `code-review` — two axes

Base = `git merge-base main HEAD`, never a mid-branch sha. Two subagents dispatched **in one message**, read-only, neither seeing the other's findings.

```markdown
## Standards
**Minor** — `src/shell/module-store.ts:34` — *primitive obsession*: `ModuleId` is a
bare string. Consider a branded type. (Baseline smell #9; judgment call.)

## Spec
**COMPLIANT** — SHELL-1.1, 1.2, 1.4, 1.5 implemented and tagged.
**Important** — SHELL-1.3 (guard): tagged only on a unit test asserting the store
does not clear editor state. The requirement says state survives a *module switch*,
which is the e2e seam the design promised. `file:line` cited.

Ready to merge? With fixes
```

The reports are **not merged**. They are presented under separate headings, un-reranked, because a change can pass one axis and fail the other, and merging lets one mask the other.

---

## `acceptance-check`

Green unit tests prove the assertions someone wrote pass. They do not prove the feature works.

The checklist is derived from the spec, keyed to requirement ID, and written to `.skills/shell-acceptance.md`. The UI slice goes to [`acceptance-ui`](../skills/acceptance-ui.md):

```ts
test('switching modules preserves unsaved editor text', { tag: '@SHELL-1.3' }, async ({ page }) => {
  await page.getByRole('textbox', { name: 'Note body' }).fill('unsaved draft')
  await page.getByRole('button', { name: 'Tasks' }).click()
  await page.getByRole('button', { name: 'Notes' }).click()
  await expect(page.getByRole('textbox', { name: 'Note body' })).toHaveValue('unsaved draft')
})
```

It fails. The rail unmounts the editor. This is a real defect, found before a user found it, and the failing spec **is** `debug`'s red-capable loop. Fix the root cause, keep the spec as the regression, commit it tagged — so it joins the verify suite forever.

That is the `code-review` Spec finding above, confirmed live. The guard requirement earned its existence.

---

## `finish-branch` → `release` → `sync-spec`

`verify` runs every command fresh, and the trace check must be clean. Then exactly four options, verbatim, with no added commentary: merge locally, push and PR, keep, or discard — and discard requires typing the word `discard`.

When the version ships, `/release` assembles the changelog by grouping commits under their trailers and looking up each requirement's own text:

```markdown
### Shipped behavior
- Module selection persists across launches — SHELL-1.2
- Unknown persisted modules fall back to Notes — SHELL-1.4

### Protected behavior
- Unsaved editor state survives a module switch — SHELL-1.3
```

Nobody wrote those lines. They were derived, and they are derivable only because `SHELL-1.3` is the same string in the requirement, the Playwright tag, and the commit trailer.

Finally `sync-spec` flips `Status: Shipped`, updates `INDEX.md`, and re-runs the trace check — so the *next* feature's `brainstorm`, searching `docs/specs/`, finds `SHELL`'s spec: its Summary card, its owned paths, and its Out-of-Scope note that keyboard shortcuts were deliberately deferred.

The loop closes.

## See also

- [The process](../process/README.md) — every phase in detail
- [Traceability](../concepts/traceability.md) — the spine this example is threaded on
- [Tier 1: a bugfix](tier-1-bugfix.md) — the same feature, one bug later
- [Tier 0: a tweak](tier-0-tweak.md)
