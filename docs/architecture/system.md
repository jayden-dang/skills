# Architecture domain: System

Status: Approved
Date: 2026-07-22
Part of: [`INDEX.md`](./INDEX.md) (architecture SSOT)

This domain is the system design of the skill set itself: how the repository is
laid out, how adopters install it, and the optional project-docs layer. Product
intent lives in [`docs/product/vision.md`](../product/vision.md). Hard invariants
live only in [`INDEX.md`](./INDEX.md) (ARCH-N).

## Principles

1. **Predictability is the root virtue**: a skill exists to wrangle determinism
   out of a stochastic system — the agent takes the same process every run.
2. **Traceability is the memory**: intent lives in persisted, individually
   addressable requirements — not chat history. Every task, test, and commit
   points at a requirement ID.
3. **Determinism comes from the primitives**: the trace check is `grep` +
   set-difference — operations that are exact no matter who runs them. A skill
   specifies the passes and the rules; the agent runs the passes and reads the
   output. The honesty lives in deterministic tools driven by a precise skill.
   (See [artifacts.md — The trace check](./artifacts.md#the-trace-check).)
4. **Gates, not vibes**: no code before an approved spec; no fix before a root
   cause; no completion claim without fresh evidence.
5. **Ceremony scales with the task**: a three-tier system prevents pages of spec
   for a trivial change.
6. **Zero mandatory tooling in the consuming repo**: adoption requires only the
   skills (plugin or npx) and markdown config. No Python, no vendored scripts, no
   CI or hook wiring is needed to get the full methodology. A hard headless gate is
   an *optional* add-on, documented separately, never the default path.
7. **Tracker-agnostic, configured once per repo**: skills read repo config from
   `docs/agents/*.md`; GitHub Issues, GitLab, or local markdown all work.
8. **Small skills that compose**: user-invoked skills orchestrate; model-invoked
   skills hold reusable discipline. A user-invoked skill may invoke model-invoked
   skills, never another user-invoked one.

## Repository architecture (this repo)

```
skills/
  meta/        using-skills, ask, writing-skills, teach
  setup/       setup-repo, scaffold-project
  discovery/   brainstorm, grilling, research, prototype, domain-modeling
  spec/        write-requirements, write-design, write-plan
  execution/   execute-plan, tdd, debug, verify, trace, worktrees
  review/      code-review, receive-review, check-invariants
  acceptance/  acceptance-check, acceptance-api, acceptance-ui, dogfood
  craft/       design-page
  ship/        finish-branch, release
  track/       amend, correct-course, triage, sync-spec, improve-architecture, handoff, file-issues
  project/     establish-project              (optional project-documentation layer)
templates/     requirements.md, design.md, tasks.md, docs/agents seeds, CONTEXT.md seed,
               product-vision.md, architecture-INDEX.md, product-guidelines.md seeds
hooks/         session-start (injects meta/using-skills)
docs/          per-skill human docs + product/architecture layer (this tree)
.claude-plugin/plugin.json   (Claude Code plugin manifest)
```

The traceability discipline lives in the `trace` skill; feature-overlap detection
lives as inline grep-and-read steps inside `brainstorm` and `code-review`. Both run
on `grep`/`git` and file reads, so the whole set is `SKILL.md` and templates — a
consuming repo installs nothing executable beyond the session-start hook.

- **Installation:** `npx skills@latest add jayden-dang/skills` (skills.sh) or as a
  Claude Code plugin. Dev mode: clone the repo and either add it as a plugin, or
  symlink the skill folders into `~/.claude/skills` with a one-line shell loop
  documented in the README (no committed installer script).
- **Activation:** a `SessionStart` hook (matcher `startup|clear|compact`) injects
  the full text of `meta/using-skills` so the skill-check gate survives compaction.
  This is the one piece of scaffolding the design keeps. When installed via
  skills.sh (no plugin hook support), `setup-repo` offers to add the hook to the
  project's settings.
- **Conventions:** verb-first skill names; frontmatter descriptions state
  *triggering conditions only, never the workflow*; cross-references as
  `REQUIRED SUB-SKILL:` prose, never `@`-links; user-invoked skills carry
  `disable-model-invocation: true`.

## The project layer (optional)

Above the per-feature workflow sits an **optional** repo-level documentation layer, for
large or long-lived projects. It is authored by one user-invoked skill,
`establish-project` (create/update/validate), and consists of:

```
docs/product/vision.md      # the product north star — problem, users, goals, non-goals, scope
docs/architecture/          # this tree — IDed ARCH-N invariants (INDEX) + system design domains
docs/product/guidelines.md  # human-facing engineering guidelines (write-plan sources these)
```

The load-bearing idea is the **architecture spine as invariants**: not a diagram doc, but
the small set of cross-cutting rules that keep independently-built features from
diverging — each a greppable ARCH-N ID, exactly like a requirement ID. A feature
`design.md` cites the ones it relies on as `Respects: ARCH-N`, and the `trace` check
extends **one level up**: it verifies each citation points at a *live* invariant
(referential integrity — codes E4/E5/W3), while the *semantic* judgment of whether a
design truly respects an invariant is a separate, advisory, LLM-judged check
(`check-invariants`), never folded into deterministic `trace`.

The layer is **optional by construction**. Feature skills consult it through
observable-predicate, no-op-if-absent hooks (`brainstorm` checks product scope;
`write-design` cites invariants; `write-plan` folds them into Global Constraints;
`execute-plan` surfaces them per task; `code-review` runs the advisory lane). A repo that
opts into nothing behaves exactly as before — `setup-repo` gates the whole layer behind a
default-**No** decision.

This repo dogfoods the full layer: invariants in [`INDEX.md`](./INDEX.md) (ARCH-1..5),
system design in the domain files listed there, vision and guidelines under
`docs/product/`.
