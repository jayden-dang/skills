# Phase 2 — Specification

**Skills:** [`write-requirements`](../skills/write-requirements.md) → [`write-design`](../skills/write-design.md) → [`write-plan`](../skills/write-plan.md)

**Produces:** the spec triad in `docs/specs/<YYYY-MM-DD>-<feature>/`, and a registered feature code in `docs/specs/INDEX.md`.

**Runs only for tier ≥ 1.** Tier 0 goes straight to `tdd`. Tier 1 stops after a mini-spec.

## The shape of the phase

Three files, written in order. Each is **approved as a file**, not as conversational agreement:

> Do not proceed to design on the strength of conversational agreement — the written requirements are what get approved.

The reason is that a conversation cannot be cited. A requirement ID can.

## Step 1 — `requirements.md`: WHAT

**Register the feature code first.** Two to twelve characters, `A-Z0-9`, starting with a letter. It goes into `docs/specs/INDEX.md` *before* the requirements file is written, and a retired code is never reused.

**Write stories and EARS criteria.** One `## N. <title>` section per user story, each with acceptance criteria carrying [hierarchical IDs](../concepts/requirement-ids.md). Five [EARS](../resources/ears.md) forms:

| Form | Shape |
|---|---|
| Event-driven | `WHEN <event> THE SYSTEM SHALL <behavior>` |
| State-driven | `WHILE <state> THE SYSTEM SHALL <behavior>` |
| Error handling | `IF <unwanted condition> THEN THE SYSTEM SHALL <behavior>` |
| Optional feature | `WHERE <feature enabled> THE SYSTEM SHALL <behavior>` |
| Ubiquitous invariant | `THE SYSTEM SHALL <behavior>` |

One observable behavior per criterion. **If a sentence needs "and", it is usually two criteria.**

**Guard existing behavior.** For every existing behavior this feature touches:

```markdown
- **SHELL-1.3** (guard) WHEN the user switches modules THE SYSTEM SHALL
  CONTINUE TO preserve unsaved editor state.
```

Guards are what stop an agent from breaking load-bearing behavior nobody mentioned. And the completion criterion for this step forbids the lazy answer: *you have actively searched the touched surface for behaviors to guard — not merely found none by default.*

**Write Out of Scope.** What this feature deliberately does not do. This section is read again later, by `code-review` (as the scope-creep reference), by `dogfood` (as deliberate non-behaviors to check), and by the feature-overlap search (as a Summary-card field a neighboring feature's `brainstorm` reads straight out of `docs/specs/`).

**Self-review, then gate.** Four passes before the user sees it:

- **Ambiguity scan** — could any criterion be read two ways? Pick one reading and write it in.
- **Testability scan** — can each criterion be verified by an automated test or a concrete manual check?
- **Placeholder scan** — no "TBD", "etc.", "handle errors appropriately".
- **Code-claim check** — if any criterion asserts how the system *currently* works, a **review subagent** verifies each such claim against the real code, citing `file:line`. You do not read the code yourself. A false premise here — "the body is ProseMirror-JSON" when it is Markdown — poisons design, plan, and code alike.

Then present the file and **stop**. On approval, `Status: Approved`.

**IDs are immutable from that moment.** Retire by strikethrough (`~~**SHELL-1.2**~~ superseded by SHELL-1.4`), never by renumbering. The trace check treats struck-through IDs as undefined, so every test or task still citing one surfaces immediately as an E1 error.

## Step 2 — `design.md`: HOW

**Context and decisions.** Two to four paragraphs on what exists today and which constraint shapes the approach. To learn "what exists today" without flooding context, a **scan subagent** maps the touched surface — current signatures, data shapes, save/load paths — and returns a digest file. Design against the digest; pull a specific file into context only when a decision hinges on its exact contents.

**Architecture with `Satisfies:` lines.** One `###` section per component. Every section carries the requirement IDs it exists to meet:

```markdown
### Module store

Satisfies: SHELL-1.1, SHELL-1.2
```

A section with no `Satisfies:` line is either infrastructure — and says so — or does not belong in this feature.

For the genuinely hard parts, **design it twice**: dispatch two or three parallel subagents with *divergent constraints* (minimize the interface / maximize flexibility / optimize the common caller), compare on interface depth and seam placement, and commit to one with a stated reason. Be opinionated. The user wants a strong recommendation, not a menu.

Design for depth: a module's interface should be much simpler than what it hides. Apply the **deletion test** — if this module vanished, how much would callers need to know to rebuild it? If the answer is "everything it did", the interface is shallow.

**Agree the seams.** The *Seams for testing* table is a contract, not documentation:

| Seam | Kind | Covers |
|---|---|---|
| `moduleStore` public API | unit | SHELL-1.1, SHELL-1.2 |
| module rail (e2e) | e2e | SHELL-1.3 |

`tdd` **refuses** to write a test at a seam this table does not confirm. Prefer existing seams; the ideal number of *new* seams is zero or one. Every requirement ID maps to at least one row.

**Coverage self-check, independent review, and the gate.** Walk `requirements.md` top to bottom: every ID appears in exactly one `Satisfies:` line, or is listed as deliberately unmapped with a reason.

Then dispatch an **independent design review subagent** — fresh context has no stake in your framing, which is the bias that reinterprets a stale requirement rather than catching it. It verifies that every named seam, signature, and data path exists as described, citing `file:line`, defaulting to flag.

### Upstream sync-back — the rule nobody expects

Designing routinely surfaces a fact that contradicts an **already-approved** requirement. When it does:

> You MUST correct the requirement's own text and re-surface it for approval — never satisfy a requirement by quietly reinterpreting words you now know are false.

A `Satisfies:` line pointing at a requirement whose wording is wrong makes the trace spine **cite a lie**, and the error survives all the way to code. If you changed any requirement, say exactly which and why when you present for approval.

## Step 3 — `tasks.md`: the PLAN

Written for an implementer who is skilled but knows **nothing** about this codebase or problem domain, and will see **only their own task** plus the Global Constraints. That constraint drives everything:

- **Global Constraints**, copied verbatim from the design and `docs/agents/project.md`. Every task's requirements implicitly include this section, and it travels with each task brief.
- **File structure first.** Map every file the plan creates or modifies, with one-line responsibilities, before writing any task. A file not in the map should not be touched.
- **Tasks as vertical slices** — demoable end to end, not horizontal layers. If a slice needs prefactoring, that prefactoring is its own earlier task: *make the change easy, then make the easy change.*
- Right-sizing: a task is the **smallest unit that carries its own test cycle and deserves its own review verdict.** Split only where a reviewer could reject one task while approving its neighbor.

Per task: **Files** (create / modify with line ranges / test), **Interfaces** (Consumes and Produces — how an isolated implementer learns what to call things), **Steps** as bite-sized checkboxes following the TDD cycle with exact commands and expected output, and a `_Requirements: SHELL-1.1, SHELL-1.2_` **footer**.

**No placeholders.** "TBD", "add appropriate error handling", "similar to Task 3", or a type referenced but defined in no task — each is a plan bug, fixed before the plan ships.

### The coverage check that goes further than the trace check

This is the subtlest thing in the phase.

The trace check verifies every `Approved` requirement is cited by at least one task footer. But **a footer is not a test.** A footer citation with no tagged test passes the trace check today (Approved → W1 warning) and fails **E2** the moment the feature is marked `Implemented`.

So `write-plan` requires more: every requirement ID must also appear in a **test annotation inside some task's steps** — `[SHELL-1.2]` in a Vitest title, `/// REQ: SHELL-1.2` on a Rust test, `@SHELL-1.2` in a Playwright tag. And it reconciles against the design's seam table: an ID the design *promised* to cover but the plan left untagged is **dropped coverage**. Add the test; never renumber.

A guard or negative requirement counts only if a real test asserts it. When a behavior cannot be unit-tested in isolation, tag the e2e task or an existing test that already exercises it — one test may carry several IDs.

Finally, an **independent plan review subagent** verifies against real code every symbol, signature, path, import, and **hardcoded test value** the plan asserts. A fabricated golden value or a guessed API is the classic plan defect.

**Optionally**, publish each task as a tracker issue in dependency order — native sub-issues and blocking links where supported. The issue body describes *behavior and interfaces, never file paths*, and includes a `Requirements covered:` list. (Those issues are then out of scope for `/triage`, which skips anything born agent-ready.)

## Exit

`write-plan` offers exactly two execution routes: `execute-plan` in an isolated workspace via `worktrees` (recommended), or inline execution for environments without subagents.

## Next

→ [Phase 3 — Execution](execution.md)

## See also

- [Requirement IDs](../concepts/requirement-ids.md) — the grammar and the status lifecycle
- [EARS reference](../resources/ears.md) — the five criterion forms
- [Templates](../resources/templates.md) — the three seed files
- [The trace check](../resources/scripts.md#the-trace-check) — W1 versus E2, and why the distinction bites
