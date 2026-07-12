# The skill model

A skill is a markdown file with YAML frontmatter that the agent reads and follows. That is the whole mechanism. Everything interesting is in the conventions layered on top.

## Anatomy

```markdown
---
name: tdd
description: Use when writing or changing any production code — a new feature, a
  bugfix, a behavior change, or a refactor — and before the first line of
  implementation exists; the test-first (TDD) gate.
---

# TDD

## The Iron Law
...
```

Three loading levels, and each costs differently:

| Level | Cost |
|---|---|
| **Metadata** — `name` + `description`, ~100 tokens | paid every turn of every session |
| **Body** — the SKILL.md text | paid every turn *once the skill fires* |
| **Reference file** — a sibling `.md` behind a pointer | costs nothing until the pointer is followed |

That budget is why discipline skills keep their core body to roughly 500 words, why the hard ceiling for any SKILL.md body is ~500 lines, and why the session-injected `using-skills` is the shortest gate in the set. Length is a failure mode in itself, even when every line is live.

## The two invocation kinds

**Model-invocable** skills have no special frontmatter. The agent invokes them on its own when the description matches the situation. These hold reusable discipline: `tdd`, `verify`, `debug`, `grilling`, `write-design`.

**User-invoked** skills carry `disable-model-invocation: true`. The agent *cannot* auto-invoke them; the user runs them as a slash command. These orchestrate: `/ask`, `/setup-repo`, `/scaffold-project`, `/triage`, `/improve-architecture`, `/handoff`, `/release`, `/writing-skills`.

The composition rule falls out of that:

> A user-invoked skill may invoke model-invoked skills, never another user-invoked one.

And the corollary, which `writing-skills` calls a real bug rather than a style nit: **no skill body may tell the agent to *invoke* a user-invoked skill.** Directing the agent to invoke a `disable-model-invocation` target is a dead-end hand-off — the invocation silently cannot happen. A hand-off reaches a user-invoked skill only by *naming it for the user to run*: "run `/triage`", "suggest the user run `/handoff`".

You can see the rule being obeyed in the wild. `debug` hands architectural findings to `improve-architecture` — but `improve-architecture` is user-invoked, so `using-skills` says: *"name a user-invoked one for the user to run."* Meanwhile `execute-plan` writes `REQUIRED SUB-SKILL: use \`code-review\`` freely, because `code-review` is model-invocable.

| Bucket | Skills | Kind |
|---|---|---|
| meta | `using-skills` | model (session-injected) |
| | `ask`, `writing-skills` | user |
| setup | `setup-repo`, `scaffold-project` | user |
| discovery | `brainstorm`, `grilling`, `research`, `prototype`, `domain-modeling` | model |
| spec | `write-requirements`, `write-design`, `write-plan` | model |
| execution | `execute-plan`, `tdd`, `debug`, `verify`, `trace`, `worktrees` | model |
| review | `code-review`, `receive-review` | model |
| acceptance | `acceptance-check`, `acceptance-api`, `acceptance-ui`, `dogfood` | model |
| ship | `finish-branch` | model |
| | `release` | user |
| track | `amend`, `sync-spec` | model |
| | `triage`, `improve-architecture`, `handoff` | user |

## The description is the highest-leverage line

It states **trigger + outcome, never the workflow.**

Name the *deliverable* the skill produces — the outcome noun, like "the `tasks.md` implementation plan" or "a two-axis review verdict" — plus when it fires. Never summarize the steps.

The reason is a specific observed failure. A process summary hands the agent a shortcut it obeys *instead of reading the body*:

- "use when a design is approved and the `tasks.md` plan needs writing" → the body gets read.
- "use when planning — dispatches a reviewer between tasks" → the summary gets obeyed and the body ignored.

There are two failure directions, and both are tested rather than guessed. Over-summarizing the workflow hands the agent a shortcut. Under-specifying is the commoner failure: the skill never fires at all. Keyword coverage and the outcome noun fight the second; omitting the workflow steps fights the first.

Hence: verb-first names (`writing-skills`, `receive-review`, `debug` — the action, not the topic), and descriptions packed with the words a user would actually type — symptoms, literal error text (`error`, `exception`, `e2e`, `tech debt`), file names (`tasks.md`), and synonyms (`spike`, `mock up`). Discovery is keyword match; a skill nobody finds is a skill that does not exist.

## The authoring vocabulary

These five terms recur throughout the set, and reading any skill is easier once you have them.

**Leading word.** A compact concept the model already carries from pretraining — "seam", "tracer bullet", "red" — that anchors a whole region of behavior in a few tokens. Repeated as a token, it accumulates a distributed definition across the skill; three sentences of restatement often collapse into one such word. A *coined* word recruits no priors, so reach for a pretrained one first.

**Completion criterion.** Every step ends on a condition the agent can check: "suite green, output pristine", not "tests look good". This is the defense against premature completion — a vague bound lets attention slip toward *being done* instead of the work. Nearly every step in every skill here ends with a `Done when:` line.

**The no-op test.** Does this line change behavior versus no skill at all? A line can be true, relevant, and still a no-op ("be careful"). Disputes about what the default behavior is are settled by running the scenario, never by debate. A sentence that fails is deleted whole, not trimmed.

**Negation trap.** A prohibition names the banned behavior into context, where it half-reads as an instruction. Prompt the positive ("write one-line comments") so the banned pattern is never spoken. The one exception is pressure-gate skills, where hard prohibitions plus explicit counters are exactly the right tool.

**Information hierarchy.** In-skill steps, then in-skill reference, then disclosed reference behind a context pointer. Inline what every run needs; push behind a pointer what only some branches reach. The pointer's *wording*, not its target, decides whether the material is ever loaded — a must-read file behind a limp pointer is a variance bug. Keep reference files **one level deep** from SKILL.md, and give any reference over ~100 lines a table of contents.

## Cross-references

Skills reference each other **as prose**, never as file links:

```markdown
REQUIRED SUB-SKILL: use `verify` before any completion claim.
```

Never `@`-links or markdown links into another skill's folder. A link force-loads content and couples the folders. Files that live *beside* a SKILL.md are referenced by relative filename, with pointer wording that says when to load them — `standards-baseline.md` beside `code-review`, `implementer-prompt.md` beside `execute-plan`.

## When *not* to write a skill

> If the rule is mechanically enforceable — a regex, a linter, a schema check, a git hook — automate it and skip the skill.

Documentation is for the judgment calls a check cannot make. A skill that only restates what a deterministic check already guarantees is context the agent pays for on every run, to enforce what fixed rules could have enforced for free. This is precisely why the `trace` skill runs a fixed sequence of `grep` and `git` passes instead of a "remember to keep the trace matrix updated" skill.

## When to split one

Exactly two cases:

1. **Genuinely distinct trigger** — a separate condition or leading word should fire it on its own, or another skill must reach it independently.
2. **Hiding post-completion steps** — later steps visibly tug the agent into rushing the current one, and the split places them behind a *real* context boundary: a sub-skill hand-off or a subagent dispatch. An inline mention leaves them in context and hides nothing.

Anything else is granularity for its own sake, paid for in context load or the user's memory.

## Skills are test-driven

`writing-skills` carries its own Iron Law:

```
NO NEW SKILL AND NO EDIT TO A SKILL SHIPS WITHOUT A FAILING TEST FIRST
```

RED: run the scenario *without* the skill and record the failures and rationalizations verbatim. If the baseline agent does not fail, stop — there is nothing to fix, and text with no failure behind it is a no-op. GREEN: write the smallest text addressing those recorded failures, and re-run. REFACTOR: under pressure the agent invents new rationalizations; capture each verbatim, add an explicit counter, re-test.

> Wrote the text before running the baseline? You documented what you *guess* agents do wrong, not what they do wrong.

This is why the rationalization tables in `tdd`, `debug`, `verify`, and `brainstorm` read so specifically. Every row is a real rationalization, recorded from a real baseline run, and countered by name.

## Activation

The set ships as a Claude Code plugin. `hooks/hooks.json` registers a `SessionStart` hook with matcher `startup|clear|compact` that injects the full text of `using-skills` into context — so the skill-check gate survives `/clear` and compaction, the two moments it would otherwise silently disappear.

When installed without plugin hook support, `setup-repo` offers to copy `templates/session-start.sh` into the project's own `.claude/hooks/` and reference it via `$CLAUDE_PROJECT_DIR` — never an absolute path, which would be committed into `.claude/settings.json` and break on every other machine.

## See also

- [The gates](gates.md) — the four skills that guard rules the agent breaks under pressure
- [`writing-skills`](../skills/writing-skills.md) — the full authoring doctrine and its deployment checklist
- [`using-skills`](../skills/using-skills.md) — the session gate
- [Skill reference](../skills/README.md) — all 33 skills
