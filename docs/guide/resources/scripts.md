# Enforcement and tooling

The skill set installs nothing into a consuming repo — no scripts, no linters, no CI job, no git hooks. Enforcement rests on two mechanisms, and both are built from primitives that already exist in any repo:

- **The `trace` skill** — a fixed sequence of `grep` and `git` passes with fixed rules on their output, enforcing that one feature's requirements, tasks, and tests agree.
- **Feature-overlap search** — an inline `grep` over `docs/specs/` that answers *does this idea or diff already exist?*

Determinism comes from the primitives — `grep` and `git` produce the same output every run — and from the fixed rules applied to that output. There is no interpreter to install and no program to keep in sync.

---

## The trace check

The requirements traceability check. The vertical layer: one feature's requirements, tasks, and tests must agree. It is not a linter and not a program — it is a fixed routine the `trace` skill runs, a set sequence of greps and git reads with a fixed verdict rule on each.

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

Because step 2 is a textual `grep`, **coverage is textual**: an ID string present in a test file counts as covering that requirement. The check does not — and cannot — judge whether the test actually asserts the behavior. That judgement belongs to [`tdd`](../skills/tdd.md), [`code-review`](../skills/code-review.md), and the acceptance family.

### The rules

| Code | Meaning |
|---|---|
| **E1** | a task or test cites an ID that is not defined in any requirements file |
| **E2** | a requirements file with `Status: Implemented` or `Shipped` has a requirement with zero test references |
| **E3** | the same ID is defined more than once |
| **W1** | a requirements file with `Status: Approved` has a requirement not cited by any task |
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

A [citation](../concepts/traceability.md) is an ID the trace check counts; a **fixture ID** is an ID-shaped string that appears in source (example data, documentation) that no test asserts. Because the collect-citations pass is textual, a repo whose own fixtures contain ID-shaped strings can name those files in the **trace ignore** list in `docs/agents/project.md` so the pass skips them. That list filters the test-file scan only — it never stops a `requirements.md` from *defining* IDs.

The trace check reads two optional settings from `docs/agents/project.md` — the **test globs** it searches and the **trace ignore** list — and falls back to defaults when they are absent. The default globs are `tests test e2e src src-tauri crates app lib packages`; the default ignore list is empty.

### Who runs it

The `trace` skill is invoked by [`verify`](../skills/verify.md) (before any "requirements met" claim), [`write-plan`](../skills/write-plan.md) (its coverage check), [`release`](../skills/release.md) (its gate), and [`sync-spec`](../skills/sync-spec.md) (the before-and-after pictures). Each of these runs with an agent present to read and act on the findings.

There is no mandatory headless gate. A team that wants a hard CI or pre-push check can add one as its own choice, but it sits outside the default path — the trace check does its work at the moments a skill is already about to make a claim.

---

## Feature-overlap search

The horizontal question — *which existing features touch this same surface, and does this idea already exist?* — is answered by an inline `grep` over `docs/specs/`, not by any generated artifact. Nothing is derived and nothing goes stale; the specs that already exist are the source of truth, and [`docs/specs/INDEX.md`](../concepts/artifacts.md) is the feature registry.

Two skills run this search:

- **[`brainstorm`](../skills/brainstorm.md)** greps `docs/specs/` with the new idea's key terms and candidate file paths before the interview begins. Any feature whose spec matches is read as its **Summary card** — the top-of-spec digest (code, name, owned paths, out-of-scope) — so the agent can state which existing features share the idea's surface and how the new idea differs, citing feature codes, or that none do.
- **[`code-review`](../skills/code-review.md)** greps `docs/specs/` with the diff's changed file paths, so its Spec subagent can flag any place the diff reimplements behavior a neighboring feature already owns.

See [feature overlap](../concepts/feature-graph.md) for the concept in full.

## See also

- [Traceability](../concepts/traceability.md) — what the trace check is enforcing and why
- [Feature overlap](../concepts/feature-graph.md) — how neighbors are found by searching `docs/specs/`
- [Requirement IDs](../concepts/requirement-ids.md) — the string the trace check follows
- [Troubleshooting](troubleshooting.md) — when a check reports a finding
