# Skills

An A-to-Z agentic development skill set: one system that carries a project from
ideation to release, with **requirements traceability as the spine**.

Every feature gets a spec triad — `requirements.md` (EARS acceptance criteria
with hierarchical IDs), `design.md` (each section says which requirements it
satisfies), `tasks.md` (each task cites the IDs it implements). The same IDs
flow into test tags, commit trailers, and issue bodies, and a trace-check
script keeps the whole chain honest in CI.

📖 **[Read the guide →](docs/guide/NAVIGATION.md)**

## Why

An LLM is a stochastic system. That is a feature when you want ideas and a
catastrophe when you want a codebase. Intent evaporates on compaction. Agents
rationalize past their own rules. "Done" gets claimed, not proven. Unit tests
go green while the feature is broken.

Each of those failures has a defense here, and the defenses are the point.

The load-bearing idea: **a requirement ID is a first-class runtime object.**
Not a heading in a document — a string that appears in a test tag, a commit
trailer, an issue body, and a changelog line, with a linter that fails the
build when those uses disagree with its definition.

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

**No Node runtime required.** The `npx` path above needs Node only to fetch the
package; the skill set itself — including its two linters — runs on the Python 3
(3.9+) that ships with your machine. To install with no Node at all, clone the
repo and symlink the skills directly:

```bash
git clone https://github.com/jayden-dang/skills ~/dev/skills
~/dev/skills/scripts/link-skills.sh
```

`scripts/link-skills.sh` (and the rest of the shell tooling) is plain
`bash` — no dependency of its own either way.

Dev mode — symlink so `git pull` updates skills in place:

```bash
./scripts/link-skills.sh
```

Then, once per repo, run `/setup-repo` to configure the issue tracker, verify
commands, and docs layout. For a brand-new project, start with
`/scaffold-project`. See [Adopting the skill set](docs/guide/resources/adopting.md).

**Other platforms.** Nothing here is Claude-specific — the skills are plain
`SKILL.md`, the linters are Python stdlib, the tooling is bash. `AGENTS.md` at
the repo root is the portable behavior contract; Codex CLI reads it natively and
Cursor picks up `.cursor/rules/using-skills.mdc`. See
[Running on other platforms](docs/guide/resources/platforms.md).

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
| meta | `using-skills` (session gate), `ask` (router), `writing-skills` |
| setup | `setup-repo`, `scaffold-project` |
| discovery | `brainstorm`, `grilling`, `research`, `prototype`, `domain-modeling` |
| spec | `write-requirements`, `write-design`, `write-plan` |
| execution | `execute-plan`, `tdd`, `debug`, `verify`, `worktrees` |
| review | `code-review`, `receive-review` |
| acceptance | `acceptance-check`, `acceptance-api`, `acceptance-ui`, `dogfood` |
| ship | `finish-branch`, `release` |
| track | `amend`, `triage`, `sync-spec`, `improve-architecture`, `handoff` |

One page per skill in the [skill reference](docs/guide/skills/README.md).

## Traceability tooling

```bash
python3 scripts/check_trace.py [--strict] [--json]     # the vertical layer
python3 scripts/check_graph.py [--harvest|--query|--verify]   # the horizontal layer
```

Both are Python 3.9+ stdlib scripts — no third-party package, no network access.

`check_trace.py` fails on: tasks or tests citing unknown requirement IDs;
implemented/shipped requirements with no covering test; duplicate ID
definitions. Warns on approved requirements not yet cited by any task.

`check_graph.py` harvests each feature's surface from its existing specs and
answers "does this idea already exist?" for `brainstorm` and "does this diff
reimplement a neighbor?" for `code-review`.

`scripts/task-brief` and `scripts/review-package` support `execute-plan`'s
subagent-per-task engine (briefs, diffs, and reports are handed over as files,
never pasted text). `scripts/vendor_linters.py` installs the two linters into
a consuming repo and detects drift.

Full reference: [Scripts](docs/guide/resources/scripts.md).

## Documentation

| | |
|---|---|
| **[Navigation](docs/guide/NAVIGATION.md)** | by role, by problem, by phase |
| [Overview](docs/guide/methodology/overview.md) | what this is and what it defends against |
| [Philosophy](docs/guide/methodology/philosophy.md) | six principles, and what enforces each |
| [When to use it](docs/guide/methodology/when-to-use.md) | the honest boundaries |
| [Traceability](docs/guide/concepts/traceability.md) | the spine |
| [The process](docs/guide/process/README.md) | the chain, phase by phase |
| [Skill reference](docs/guide/skills/README.md) | one page per skill |
| [Examples](docs/guide/examples/tier-2-feature.md) | tier 0, 1, and 2 walkthroughs |
| [Troubleshooting](docs/guide/resources/troubleshooting.md) | symptoms and causes |
| [DESIGN.md](./DESIGN.md) | the architecture spec of record |

## License

MIT
