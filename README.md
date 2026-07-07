# Skills

An A-to-Z agentic development skill set: one system that carries a project from
ideation to release, with **requirements traceability as the spine**.

Every feature gets a spec triad — `requirements.md` (EARS acceptance criteria
with hierarchical IDs), `design.md` (each section says which requirements it
satisfies), `tasks.md` (each task cites the IDs it implements). The same IDs
flow into test tags, commit trailers, and issue bodies, and a trace-check
script keeps the whole chain honest in CI.

## Install

```bash
npx skills@latest add jayden-dang/skills
```

Or as a Claude Code plugin (this repo is a valid plugin: skills + a
session-start hook that keeps the skill-check gate active across compaction).

Dev mode — symlink so `git pull` updates skills in place:

```bash
./scripts/link-skills.sh
```

Then, once per repo, run `setup-repo` to configure the issue tracker, verify
commands, and docs layout. For a brand-new project, start with
`scaffold-project`.

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
                              code-review ──► finish-branch ──► release ──► sync-spec
```

- **Tier 0** (trivial): skip specs — `tdd` + `verify`.
- **Tier 1** (bugfix): a fix requirement + a `SHALL CONTINUE TO` guard + a
  tagged regression test.
- **Tier 2** (feature): the full triad.

Lost? Invoke `ask` — it routes any situation to the right entry point.

## Skill inventory

| Bucket | Skills |
|---|---|
| meta | `using-skills` (session gate), `ask` (router), `writing-skills` |
| setup | `setup-repo`, `scaffold-project` |
| discovery | `brainstorm`, `grilling`, `research`, `prototype`, `domain-modeling` |
| spec | `write-requirements`, `write-design`, `write-plan` |
| execution | `execute-plan`, `tdd`, `debug`, `verify`, `worktrees` |
| review | `code-review`, `receive-review` |
| ship | `finish-branch`, `release` |
| track | `triage`, `sync-spec`, `improve-architecture`, `handoff` |

## Traceability tooling

```bash
node scripts/check-trace.mjs [--strict] [--json]
```

Fails on: tasks or tests citing unknown requirement IDs; implemented/shipped
requirements with no covering test; duplicate ID definitions. Warns on
approved requirements not yet cited by any task.

`scripts/task-brief` and `scripts/review-package` support `execute-plan`'s
subagent-per-task engine (briefs, diffs, and reports are handed over as files,
never pasted text).

## Design

See [DESIGN.md](./DESIGN.md) for the full architecture: the artifact model,
the requirement-ID grammar, ceremony tiers, and the per-skill inventory.

## License

MIT
