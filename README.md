# Skills

This repository hosts **independent skill packages**. Install only what you need.

| Package | `npx skills` name | Path | Default install? | Role |
|---|---|---|---|---|
| **Engineer Pack** | `engineer-pack` | `skills/{meta,discovery,spec,…}/` | **Yes** (default plugin) | Spec-driven coding: ideation → ship |
| **Personal Pack** | `personal-pack` | `skills/personal/` | **Opt-in** | Life + multi-project *management* (secretary/coach) |

- Personal OS (standalone): **[skills/personal/README.md](skills/personal/README.md)** · **[docs/personal-os/START-HERE.md](docs/personal-os/START-HERE.md)**

Each package stands alone. Personal OS does **not** depend on the engineering package, and engineering installs do **not** require it.

---

## Engineering package

An A-to-Z agentic development skill set: one system that carries a project from
ideation to release, with **requirements traceability as the spine**.

Every feature gets a spec triad — `requirements.md` (EARS acceptance criteria
with hierarchical IDs), `design.md` (each section says which requirements it
satisfies), `tasks.md` (each task cites the IDs it implements). IDs stay in that
docs triad (and optional issue bodies). Application source, tests, and commits
use domain language — not mandatory ID tags or trailers. The docs-only
`audit-trace` skill keeps definitions and task citations honest — a `grep`-and-`git`
check the agent runs, no linter to install.

📖 **[Read the guide →](docs/guide/START-HERE.md)**

## Why

An LLM is a stochastic system. That is a feature when you want ideas and a
catastrophe when you want a codebase. Intent evaporates on compaction. Agents
rationalize past their own rules. "Done" gets claimed, not proven. Unit tests
go green while the feature is broken.

Each of those failures has a defense here, and the defenses are the point.

The load-bearing idea: **a requirement ID is a first-class object of the spec
triad.** Not a heading that evaporates — a `grep`-selectable string in
`requirements.md`, `Satisfies:`, and `_Requirements:` footers. Checking that
definitions and task citations agree is `grep` plus set-difference (docs-only
`audit-trace`). Tests prove behavior; Spec review maps IDs to the diff; changelog
can derive behavior prose from the specs.

```
requirements.md   **SHELL-1.2** WHEN the user selects a module THE SYSTEM SHALL …
design.md         Satisfies: SHELL-1.2
tasks.md          _Requirements: SHELL-1.2_
test              test('restores the persisted module after reload', …)  # domain language
changelog         Module selection persists across launches — SHELL-1.2  # from specs
```

## Install

### Engineering (default)

```bash
npx skills@latest add jayden-dang/skills
```

It clones this repo, reads `.claude-plugin/marketplace.json`, and offers the packs
by name. Useful flags:

| Flag | Effect |
|---|---|
| `-a '*'` | install into **every** agent store the CLI detects, not just the current one |
| `-g` | install globally (user-level) rather than into the current project |
| `--copy` | copy instead of symlinking — needed for agents that don't follow symlinked skill dirs (Codex CLI is one; verified absent from its list when symlinked, found when copied) |
| `-s '*'` | take every skill without the interactive picker |

Upgrading is `npx skills@latest update` (`-g` / `-p` to pick scope). The CLI writes
a `skills-lock.json`, and `experimental_install` restores from it — so a machine or
a teammate can be brought to the exact same set without this repo being vendored
anywhere.

Or as a Claude Code plugin (this repo is a valid plugin: **Engineer Pack** + a
session-start hook). Personal Pack is **not** in the default plugin list.

**Nothing to install into your repo.** Pure `SKILL.md` — no vendored runtime.

Dev symlink — for **working on this repo**, engineering only (so `git pull` updates
in place). Not the install path; use the CLI above for that:

```bash
git clone https://github.com/jayden-dang/skills ~/dev/skills
cd ~/dev/skills
for cat in meta discovery spec execution review acceptance craft ship track project setup; do
  for d in skills/$cat/*/; do
    [ -f "$d/SKILL.md" ] || continue
    ln -sfn "$PWD/$d" ~/.claude/skills/"$(basename "$d")"
  done
done
```

Then, once per **code** repo, run `/configure-repo`. See [Adopting](docs/guide/resources/adopting.md).

### Personal OS (opt-in, independent)

Full guide: [skills/personal/README.md](skills/personal/README.md).

```bash
npx skills@latest add jayden-dang/skills
```

Pick **Personal Pack** at the prompt — the two packs are listed separately, so an
engineering-only install never pulls these in.

In your notes vault, run `life-setup` once.

To install into *every* agent store on the machine, use the CLI's own fan-out:

```bash
npx skills@latest add jayden-dang/skills -a '*' --copy
```

See [Running on other platforms](docs/guide/resources/platforms.md) for which
agents need `--copy` and why.

**Other platforms.** Nothing here is Claude-specific — the skills are plain
`SKILL.md` and the traceability check is `grep`/`git` the agent drives.
`AGENTS.md` at the repo root is the portable behavior contract; Codex CLI reads
it natively and Cursor picks up `.cursor/rules/gate-session.mdc`. See
[Running on other platforms](docs/guide/resources/platforms.md).

### Recommended prerequisite: the Context7 MCP

The library-reasoning skills — `research`, `frame-change`, and `design-solution` —
prefer the **[Context7 MCP](https://github.com/upstash/context7)** for current,
version-accurate library and API facts instead of a model's training-cutoff
memory (which drifts stale: a version bumped, an API renamed, a package moved).
When it is present the skills reach for it before answering; when it is absent
they fall back to fetching official docs directly, so it is a recommendation,
not a hard dependency — but installing it is strongly advised for any project
that pulls in third-party libraries.

`/configure-repo` offers to install it and records the choice in
`docs/agents/project.md`. To add it yourself, follow the setup instructions at
**[github.com/upstash/context7](https://github.com/upstash/context7)** — for
Claude Code, register the server in the project's `.mcp.json` (or your user MCP
config); for another harness (Codex, Kimi, …), add it to that harness's MCP
configuration.

## The flow

```
solve-problem? ──► frame-change (+ load-subgraph) ──► specify-behavior ──► design-solution ──► plan-tasks
(gap/workflow unclear)  (gate: no code)                 (EARS + IDs)         (Satisfies:)     (_Requirements:_)
        │                                                                               │
        │ tier 0/1 shortcuts                                                            ▼
        │                          isolate-workspace ──► build-in-waves | build-by-story | build-inline
        ▼                                                                               │
  root-cause / debug-remote / assess-observability / test-first / prove-claim  ◄── discipline ────────────────┘
                                                                                        │
   inspect-change (+ load-subgraph) ──► validate-feature ──► land-branch
                          (drive the running system as a real user)     (Status: Implemented)
                                                                              │
                                                         /cut-release ────────┘  (separate loop:
                                                         cohort of Implemented → Shipped)
```

- **Tier 0** (trivial): skip specs — `test-first` + `prove-claim`.
- **Tier 1** (bugfix): a fix requirement + a `SHALL CONTINUE TO` guard + a
  regression test of the fixed behavior.
- **Tier 2** (feature): the full triad.

**Optional project layer** (large projects, off by default): `define-project`,
`assess-pivot-impact` (pivot disposition ledger when shipped code collides with new intent)
maintains a repo-level product vision plus an IDed architecture-invariant spine
(`docs/architecture/`, each rule an `**ARCH-N**`) that `frame-change`, `design-solution`,
`plan-tasks`, the execute family, and `inspect-change` consult when present. Feature
`design.md` files cite the invariants they rely on as `Respects: ARCH-N`, and `audit-trace`
checks those citations the same way it checks requirement IDs. A repo that opts into
nothing behaves exactly as above.

Lost? Invoke `/ask-me-bro` — it routes any situation to the right entry point.

## The four gates

```
frame-change   Write NO code, scaffold NOTHING, until the ceremony tier is stated out loud.
test-first          NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
root-cause        NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
prove-claim       NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

They are written as hard prohibitions with explicit rationalization tables,
because that is the form that survives an agent under pressure. Each row of
each table is a real rationalization, recorded verbatim from a baseline run,
and countered by name. See [The gates](docs/guide/concepts/gates.md).

## Skill inventory

### Engineering

| Bucket | Skills |
|---|---|
| meta | `gate-session` (session gate), `ask-me-bro` (router), `author-skills`, `teach-pack` |
| setup | `configure-repo`, `bootstrap-repo` |
| discovery | `solve-problem`, `frame-change`, `clarify-decisions`, `research`, `run-spike`, `define-domain`, `interpret-session`, `deepen-codebase`, `work-the-problem`, `pathfind` |
| spec | `specify-behavior`, `design-solution`, `plan-tasks` |
| execution | `build-in-waves`, `build-by-story`, `build-inline`, `execute-common`, `test-first`, `root-cause`, `debug-remote`, `assess-observability`, `prove-claim`, `audit-trace`, `load-subgraph`, `isolate-workspace` |
| review | `inspect-change`, `study-change`, `brief-team`, `select-review-sample`, `polish-diff`, `vet-feedback`, `review-invariants`, `review-ui` |
| acceptance | `validate-feature`, `validate-api`, `validate-ui`, `review-product-flow`, `vet-product-flow`, `run-product-walkthrough` |
| craft | `craft-page`, `draft-ui` |
| ship | `land-branch`, `record-verdict`, `cut-release` |
| track | `amend-feature`, `reroute-plan`, `triage`, `realign-spec`, `refresh-roadmap-status`, `assess-milestone`, `scan-architecture`, `map-features`, `write-handoff`, `publish-issues`, `record-debt` |
| project | `define-project`, `assess-pivot-impact`, `plan-milestones` (optional project / multi-milestone layer) |

One page per skill in the [skill reference](docs/guide/skills/README.md).

### Personal OS (opt-in, independent package)

Standalone product docs: [skills/personal/README.md](skills/personal/README.md) · [docs/personal-os/START-HERE.md](docs/personal-os/START-HERE.md).

| | |
|---|---|
| gate | `life-start` |
| setup | `life-setup` |
| capture | `life-capture`, `life-process-inbox` |
| plan | `life-orient`, `life-plan-day`, `life-execute-session` |
| portfolio | `life-open-project`, `life-plan-project`, `life-close-project`, `life-maintain-area` |
| learning | `life-open-learning-track`, `life-log-learning` |
| review | `life-review-week`, `life-review-quarter`, `life-replan`, `life-charter` |
| disk | `life-sync-workspaces` |

Templates: `templates/personal-os/`.

## Traceability, without a linter

The vertical layer — does every requirement agree across definition and task
citation in `docs/specs/`? — is the docs-only `audit-trace` skill. It runs a fixed
sequence of `grep` passes (bold `**CODE-N.M**` definitions, `_Requirements:` task
citations) and diffs the sets: it reports tasks citing unknown IDs and duplicate
definitions; it warns on approved requirements no task cites. It does **not**
grep application tests for IDs. Because the passes are `grep` and the rules are
set operations, the result is the same whoever runs it. `prove-claim`,
`cut-release`, `realign-spec`, and `plan-tasks` invoke it.

The horizontal layer — "does this idea already exist?" for `frame-change`, "does
this diff reimplement a neighbor?" for `inspect-change` — is **`load-subgraph`**:
ask-time derivation over live specs (P0 terms + P1 Files/OWNS), with
`docs/specs/INDEX.md` as the feature registry. No generated graph to keep fresh.
Brownfield gaps backfill via `/map-features`.

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
| `docs/architecture/INDEX.md` | architecture SSOT (invariants + system design) |
| `docs/product/vision.md` | product north star (engineering) |
| [Personal OS](./skills/personal/README.md) | independent life/management skill set |

## Developing this repo

Editing skills here? Run this once after cloning:

```bash
lefthook install
```

It wires `pre-commit` / `pre-push` hooks running four checks (needs `lefthook`
and PyYAML). This tooling is for *this* repo only; a repo that *consumes* the
skill set still installs nothing.

| Check | Guards against |
|---|---|
| `lint-skill-frontmatter.py` | A `SKILL.md` whose YAML won't parse — the `skills` CLI skips it silently, so a stray unquoted colon drops a skill from `npx skills add` with no error. Also fails a missing or malformed `version:` |
| `lint-skill-evals.py` | An `eval.json` that isn't grounded — assertions with no `TESTS.md` beside them are guesses about what agents get wrong, not recorded failures |
| `lint-write-handoffs.py` | A dead-end hand-off: a body telling the agent to invoke a `disable-model-invocation` skill, which it cannot do |
| `lint-context7.py` | A library-reasoning skill silently losing its Context7 reference |

### Skill versions and test material

Every `SKILL.md` carries `version:` (semver). Bump it on each behavioral edit —
patch for wording that changes nothing, minor for a new rule or slot, major when
existing usage breaks. The frontmatter lint fails a missing or malformed one.

A skill's test material lives in two files with two different jobs, so they don't
become two sources of truth:

- **`TESTS.md`** — the recorded evidence. RED transcripts verbatim, the
  rationalizations the text had to counter, what changed between iterations.
  The *why*.
- **`eval.json`** — the runnable assertions, each citing its source via
  `derived_from`. The *what must hold*.

Evals come in two kinds, and the difference is the whole point:

| `kind` | Asserts | Cites | Means |
|---|---|---|---|
| `behavior` / `trigger` | that an **observed** failure does not come back | `TESTS.md` | a regression test with a real baseline behind it |
| `contract` | that the skill does what **its own text** already promises | `SKILL.md § <heading>` | a conformance checklist — *not* proof anything was tested |

`lint-skill-evals.py` enforces both provenance rules mechanically: a
`behavior`/`trigger` eval must cite a `TESTS.md` that exists, and a `contract`
eval must cite a heading that really appears in that `SKILL.md` — so neither an
ungrounded regression claim nor an invented contract can pass. Coverage is
reported per kind, so a contract checklist is never mistaken for evidence.

Every skill has contract evals; **22 of 81 have evidence-backed ones**. Closing
that gap means running real baselines, not writing more assertions.

## License

MIT
