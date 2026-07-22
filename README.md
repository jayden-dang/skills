# Skills

An A-to-Z agentic development skill set: one system that carries a project from
ideation to release, with **requirements traceability as the spine**.

Every feature gets a spec triad — `requirements.md` (EARS acceptance criteria
with hierarchical IDs), `design.md` (each section says which requirements it
satisfies), `tasks.md` (each task cites the IDs it implements). The same IDs
flow into test tags, commit trailers, and issue bodies, and the `trace` skill
keeps the whole chain honest — a `grep`-and-`git` check the agent runs, no
linter to install.

📖 **[Read the guide →](docs/guide/START-HERE.md)**

## Why

An LLM is a stochastic system. That is a feature when you want ideas and a
catastrophe when you want a codebase. Intent evaporates on compaction. Agents
rationalize past their own rules. "Done" gets claimed, not proven. Unit tests
go green while the feature is broken.

Each of those failures has a defense here, and the defenses are the point.

The load-bearing idea: **a requirement ID is a first-class runtime object.**
Not a heading in a document — a `grep`-selectable string that appears in a test
tag, a commit trailer, an issue body, and a changelog line. Because every use is
the same literal string, checking that those uses agree with the ID's definition
is `grep` plus set-difference — deterministic work the agent runs directly,
with no bundled linter to carry.

```
requirements.md   **SHELL-1.2** WHEN the user selects a module THE SYSTEM SHALL …
design.md         Satisfies: SHELL-1.2
tasks.md          _Requirements: SHELL-1.2_
test              test('restores the persisted module [SHELL-1.2]', …)
commit            Implements: SHELL-1.2
changelog         Module selection persists across launches — SHELL-1.2
```

That last line is derived, not written. It is derivable only because the ID is
the same string in all five places above it.

## Install

```bash
npx skills@latest add jayden-dang/skills
```

Or as a Claude Code plugin (this repo is a valid plugin: skills + a
session-start hook that keeps the skill-check gate active across compaction).

**Nothing to install into your repo.** The skill set is pure `SKILL.md` — no
Python, no linters to vendor, no build step, no runtime. To run from a local
clone (so `git pull` updates skills in place), symlink the skill folders into
`~/.claude/skills`:

```bash
git clone https://github.com/jayden-dang/skills ~/dev/skills
for d in ~/dev/skills/skills/*/*/; do ln -sfn "$d" ~/.claude/skills/"$(basename "$d")"; done
```

Then, once per repo, run `/setup-repo` to configure the issue tracker, verify
commands, and docs layout. It writes markdown config only — it vendors no
scripts and wires no CI. For a brand-new project, start with `/scaffold-project`.
See [Adopting the skill set](docs/guide/resources/adopting.md).

**Other platforms.** Nothing here is Claude-specific — the skills are plain
`SKILL.md` and the traceability check is `grep`/`git` the agent drives.
`AGENTS.md` at the repo root is the portable behavior contract; Codex CLI reads
it natively and Cursor picks up `.cursor/rules/using-skills.mdc`. See
[Running on other platforms](docs/guide/resources/platforms.md).

### Recommended prerequisite: the Context7 MCP

The library-reasoning skills — `research`, `brainstorm`, and `write-design` —
prefer the **[Context7 MCP](https://github.com/upstash/context7)** for current,
version-accurate library and API facts instead of a model's training-cutoff
memory (which drifts stale: a version bumped, an API renamed, a package moved).
When it is present the skills reach for it before answering; when it is absent
they fall back to fetching official docs directly, so it is a recommendation,
not a hard dependency — but installing it is strongly advised for any project
that pulls in third-party libraries.

`/setup-repo` offers to install it and records the choice in
`docs/agents/project.md`. To add it yourself, follow the setup instructions at
**[github.com/upstash/context7](https://github.com/upstash/context7)** — for
Claude Code, register the server in the project's `.mcp.json` (or your user MCP
config); for another harness (Codex, Kimi, …), add it to that harness's MCP
configuration.

## The flow

```
brainstorm ──► write-requirements ──► write-design ──► write-plan
   (gate: no code)     (EARS + IDs)      (Satisfies:)     (_Requirements:_)
        │                                                       │
        │ tier 0/1 shortcuts                                    ▼
        │                                     worktrees ──► execute-plan
        ▼                                                       │
  debug / tdd / verify  ◄── discipline skills govern ──────────┘
                                                                │
              code-review ──► acceptance-check ──► finish-branch ──► release ──► sync-spec
                          (drive the running system as a real user)
```

- **Tier 0** (trivial): skip specs — `tdd` + `verify`.
- **Tier 1** (bugfix): a fix requirement + a `SHALL CONTINUE TO` guard + a
  tagged regression test.
- **Tier 2** (feature): the full triad.

**Optional project layer** (large projects, off by default): `establish-project`
maintains a repo-level product vision plus an IDed architecture-invariant spine
(`docs/architecture/`, each rule an `**ARCH-N**`) that `brainstorm`, `write-design`,
`write-plan`, `execute-plan`, and `code-review` consult when present. Feature
`design.md` files cite the invariants they rely on as `Respects: ARCH-N`, and `trace`
checks those citations the same way it checks requirement IDs. A repo that opts into
nothing behaves exactly as above.

Lost? Invoke `/ask` — it routes any situation to the right entry point.

## The four gates

```
brainstorm   Write NO code, scaffold NOTHING, until the ceremony tier is stated out loud.
tdd          NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
debug        NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
verify       NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

They are written as hard prohibitions with explicit rationalization tables,
because that is the form that survives an agent under pressure. Each row of
each table is a real rationalization, recorded verbatim from a baseline run,
and countered by name. See [The gates](docs/guide/concepts/gates.md).

## Skill inventory

| Bucket | Skills |
|---|---|
| meta | `using-skills` (session gate), `ask` (router), `writing-skills`, `teach` |
| setup | `setup-repo`, `scaffold-project` |
| discovery | `brainstorm`, `grilling`, `research`, `prototype`, `domain-modeling`, `interpret` |
| spec | `write-requirements`, `write-design`, `write-plan` |
| execution | `execute-plan`, `tdd`, `debug`, `verify`, `trace`, `worktrees` |
| review | `code-review`, `receive-review`, `check-invariants` |
| acceptance | `acceptance-check`, `acceptance-api`, `acceptance-ui`, `dogfood` |
| craft | `design-page` |
| ship | `finish-branch`, `release` |
| track | `amend`, `triage`, `sync-spec`, `improve-architecture`, `handoff`, `file-issues` |
| project | `establish-project` (optional project-documentation layer) |

One page per skill in the [skill reference](docs/guide/skills/README.md).

## Traceability, without a linter

The vertical layer — does every requirement trace to a task and a test? — is the
`trace` skill. It runs a fixed sequence of `grep` passes (bold `**CODE-N.M**`
definitions, `_Requirements:` task citations, ID strings across the test globs)
and diffs the sets: it reports tasks or tests citing unknown IDs, implemented or
shipped requirements with no covering test, and duplicate definitions; it warns on
approved requirements no task cites. Because the passes are `grep` and the rules
are set operations, the result is the same whoever runs it — the determinism is in
the primitives, not in a bundled script. `verify`, `release`, `sync-spec`, and
`write-plan` invoke it.

The horizontal layer — "does this idea already exist?" for `brainstorm`, "does
this diff reimplement a neighbor?" for `code-review` — is an inline search over
`docs/specs/`, with `docs/specs/INDEX.md` as the feature registry. No generated
graph to keep fresh.

Teams that want a build-failing gate in CI (which runs with no agent present) can
opt into a documented CI job; it is outside the default path. See
[Traceability](docs/guide/concepts/traceability.md).

## Documentation

| | |
|---|---|
| **[Start here](docs/guide/START-HERE.md)** | the workflow, new-repo setup, and every skill's behavior |
| [Overview](docs/guide/methodology/overview.md) | what this is and what it defends against |
| [Philosophy](docs/guide/methodology/philosophy.md) | the principles, and what enforces each |
| [When to use it](docs/guide/methodology/when-to-use.md) | the honest boundaries |
| [Traceability](docs/guide/concepts/traceability.md) | the spine |
| [The process](docs/guide/process/README.md) | the chain, phase by phase |
| [Skill reference](docs/guide/skills/README.md) | one page per skill |
| [Examples](docs/guide/examples/tier-2-feature.md) | tier 0, 1, and 2 walkthroughs |
| [Troubleshooting](docs/guide/resources/troubleshooting.md) | symptoms and causes |
| [DESIGN.md](./DESIGN.md) | the architecture spec of record |

## Developing this repo

Editing skills here? Run this once after cloning:

```bash
lefthook install
```

It wires a `pre-commit` / `pre-push` hook that lints every `SKILL.md`
frontmatter (`scripts/lint-skill-frontmatter.py`, needs `lefthook` and PyYAML).
The `skills` CLI silently skips any `SKILL.md` whose YAML won't parse, so a stray
unquoted colon can drop a skill from `npx skills add` with no error — this catches
that before it reaches `origin`. This tooling is for *this* repo only; a repo that
*consumes* the skill set still installs nothing.

## License

MIT
