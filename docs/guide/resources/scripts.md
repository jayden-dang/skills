# Enforcement and tooling

The skill set installs nothing into a consuming repo — no scripts, no linters, no CI job, no git hooks. Enforcement rests on two mechanisms, and both are built from primitives that already exist in any repo:

- **The `audit-trace` skill** — a fixed sequence of `grep` and `git` passes with fixed rules on their output, enforcing that one feature's requirements, tasks, and tests agree.
- **Feature-overlap derivation** — the [`load-subgraph`](../skills/load-subgraph.md) skill runs fixed passes over live `docs/specs/` (terms + `**Files:**` OWNS) and answers *does this idea or diff already exist?* without a generated graph file.

Determinism comes from the primitives — `grep`, file reads, and set operations produce the same finding set every run — and from the fixed rules in each skill. There is no consumer graph DB to install.

---

## The audit-trace check

The requirements traceability check. The vertical layer: one feature's requirements, tasks, and tests must agree. It is not a linter and not a program — it is a fixed routine the `audit-trace` skill runs, a set sequence of greps and git reads with a fixed verdict rule on each.

### Sources of truth

| Path | Role |
|---|---|
| `docs/specs/<feature>/requirements.md` | **defines** requirement IDs (`**CODE-N.M**`) |
| `docs/specs/fixes.md` | optional shared home for tier-1 fix and guard requirements |
| `docs/specs/<feature>/tasks.md` | **references** them, via `_Requirements: CODE-N.M_` footers |
| test files | **reference** them, via tags, annotations, names, or comments |

### The passes

The check runs a fixed sequence and never varies it:

1. **Collect definitions.** `grep` every `requirements.md` (and `fixes.md`) for bolded criterion IDs. A struck-through ID (`~~**SHELL-1.2**~~`) is deliberately excluded, so it reads as **undefined**.
2. **Collect citations.** `grep` the `tasks.md` footers and the repo's test files (enumerated with `git ls-files`, scoped by the configured test globs) for ID-shaped strings.
3. **Read status.** `grep` each `requirements.md` for its `Status:` and `Feature-code:` lines.
4. **Apply the rules** below to the three sets.

Because step 2 is a textual `grep`, **coverage is textual**: an ID string present in a test file counts as covering that requirement. The check does not — and cannot — judge whether the test actually asserts the behavior. That judgement belongs to [`test-first`](../skills/test-first.md), [`inspect-change`](../skills/inspect-change.md), and the acceptance family.

### The rules

| Code | Meaning |
|---|---|
| **E1** | a task or test cites an ID that is not defined in any requirements file |
| **E2** | a requirements file with `Status: Implemented` or `Shipped` has a requirement with zero test references |
| **E3** | the same ID is defined more than once |
| **W1** | a requirements file with `Status: Approved` or `In-progress` has a requirement not cited by any task |
| **W2** | a requirements file is missing a `Status:` line or a `Feature-code:` line |

Any **E** is a failure the invoking skill must act on; **W** findings are surfaced but do not fail the gate on their own. Zero requirements is a valid clean state.

### The ID grammar

The pattern the passes match is:

```
\b([A-Z][A-Z0-9]{1,11})-(\d+)\.(\d+)(?![.\d])
```

Two deliberate details. There is **no trailing `\b`**, because a markdown italics footer ends with `_` — a word character — which would silently drop the last ID on the line. And the negative lookahead `(?![.\d])` prevents matching a prefix of a longer number.

A struck-through ID counts as **undefined**, so retiring a requirement immediately surfaces every test and task still citing it as an E1.

### Fixture IDs

A [citation](../concepts/traceability.md) is an ID the audit-trace check counts; a **fixture ID** is an ID-shaped string that appears in source (example data, documentation) that no test asserts. Because the collect-citations pass is textual, a repo whose own fixtures contain ID-shaped strings can name those files in the **trace ignore** list in `docs/agents/project.md` so the pass skips them. That list filters the test-file scan only — it never stops a `requirements.md` from *defining* IDs.

The audit-trace check reads two optional settings from `docs/agents/project.md` — the **test globs** it searches and the **trace ignore** list — and falls back to defaults when they are absent. The default globs are `tests test e2e src src-tauri crates app lib packages`; the default ignore list is empty.

### Who runs it

The `audit-trace` skill is invoked by [`prove-claim`](../skills/prove-claim.md) (before any "requirements met" claim), [`plan-tasks`](../skills/plan-tasks.md) (its coverage check), [`cut-release`](../skills/cut-release.md) (its gate), and [`realign-spec`](../skills/realign-spec.md) (the before-and-after pictures). Each of these runs with an agent present to read and act on the findings.

There is no mandatory headless gate. A team that wants a hard CI or pre-push check can add one as its own choice, but it sits outside the default path — the audit-trace check does its work at the moments a skill is already about to make a claim.

---

## Feature-overlap derivation (`load-subgraph`)

The horizontal question — *which existing features touch this same surface?* — is answered by **`load-subgraph`**: fixed passes over live specs (P0 terms, P1 Files/OWNS, denoised OVERLAPS, ranked/bounded neighbors, OWNS coverage). No `GRAPH.md`; nothing to regenerate. [`docs/specs/INDEX.md`](../concepts/artifacts.md) is the feature registry.

Two skills invoke it:

- **[`frame-change`](../skills/frame-change.md)** — key terms + candidate paths before the interview; summary cards + coverage.
- **[`inspect-change`](../skills/inspect-change.md)** — diff paths (+ optional terms); Spec axis reuse-miss findings.

Brownfield fill-in of missing codes/binds/Files is **[`/map-features`](../skills/map-features.md)** (user-invoked, confirm-only).

See [feature overlap](../concepts/feature-graph.md) for the concept in full.

## See also

- [Traceability](../concepts/traceability.md) — what the audit-trace check is enforcing and why
- [Feature overlap](../concepts/feature-graph.md) — how neighbors are found
- [`load-subgraph`](../skills/load-subgraph.md) · [`map-features`](../skills/map-features.md)
- [Requirement IDs](../concepts/requirement-ids.md) — the string the audit-trace check follows
- [Troubleshooting](troubleshooting.md) — when a check reports a finding
- [Start here](../START-HERE.md) — end-to-end human tutorial
