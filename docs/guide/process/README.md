# The process

The skill set is a chain. Each link is a hand-off written into a skill body as a `REQUIRED SUB-SKILL:` line, so the chain is not a diagram someone drew afterward — it is how the skills actually reach each other.

## The main flow: idea → ship (tier 2)

```
using-skills                 session gate, injected on startup/clear/compact
      │
      ▼
brainstorm                   grilling + domain-modeling; research/prototype detours;
                             docs/specs/ overlap search; tier decision; approach chosen
                             ══ HARD GATE: no code, no scaffolding ══
      │
      ▼
write-requirements           EARS criteria + hierarchical IDs; guard requirements
                             ══ approval gate on the written file ══
      │
      ▼
write-design                 Satisfies: per section; seams pre-agreed; design-it-twice
                             ══ approval gate ══
      │
      ▼
write-plan                   vertical-slice tasks with _Requirements:_ footers;
                             coverage check; (optional) publish issues
      │
      ▼
worktrees                    isolated workspace, clean baseline
      │
      ▼
execute-plan                 per task: brief → implementer (tdd) → review diff →
                             two-verdict review → fixes → ledger
                             [debug on failures; verify before any claim]
      │
      ▼
code-review                  whole-branch, two axes: Standards + Spec-by-ID
      │
      ▼
acceptance-check             drive the running system through the spec's user-facing
                             behaviors (API + UI); fix; promote to tagged tests
                             (+ dogfood for a manual, human-eyeball pass)
      │
      ▼
finish-branch                verify + trace gate, then merge / PR / keep / discard
      │
      ▼
release                      full verify + clean trace → changelog from commit
                             trailers → version bump → tag → build → smoke → notes
      │
      ▼
sync-spec                    mark requirements Implemented / Shipped
```

## The bugfix flow (tier 1)

```
debug                        Phase 1: build a red-capable command and RUN it
                             ══ no theory-building before the loop exists ══
      │                      → reproduce & minimise → 3–5 ranked hypotheses
      │                      → one fix at the root cause
      ▼
tdd                          failing regression test first, at a correct seam
      │
      ▼
mini-spec                    a fix requirement + a SHALL CONTINUE TO guard, appended to
                             the owning requirements.md (or docs/specs/fixes.md)
      │
      ▼
verify → code-review → finish-branch
```

`debug` also asks, after the fix lands: *what would have prevented this bug?* When the answer is architectural — no good seam, hidden coupling, tangled callers — the specifics go to `/improve-architecture`.

## The maintenance loop

```
amend                        small in-scope change to a shipped, spec'd feature
                             → tier 0: tdd
                             → tier 1: mini-spec (write-requirements) → tdd
                             → genuinely new scope: escalate to brainstorm

/improve-architecture        periodic codebase-wide friction scan → HTML report
                             → grilling on the chosen candidate → brainstorm

/file-issues                 a conversation, spec, or idea → tracer-bullet issues
                             on the tracker → execute or implement directly

/triage                      incoming issues and external PRs → the state machine
                             → ready-for-agent brief → execute or implement directly

sync-spec                    whenever a spec'd feature changed outside its plan
```

## Phase pages

| Phase | Skills | Page |
|---|---|---|
| Project layer *(optional, above the feature loop)* | `establish-project`, `check-invariants` | [`establish-project`](../skills/establish-project.md) |
| Discovery | `brainstorm`, `grilling`, `research`, `prototype`, `domain-modeling` | [Discovery](discovery.md) |
| Specification | `write-requirements`, `write-design`, `write-plan` | [Specification](specification.md) |
| Execution | `worktrees`, `execute-plan`, `tdd`, `debug`, `verify`, `trace` | [Execution](execution.md) |
| Review & acceptance | `code-review`, `receive-review`, `check-invariants`, `acceptance-*`, `dogfood` | [Review and acceptance](review-and-acceptance.md) |
| Ship & maintain | `finish-branch`, `release`, `sync-spec`, `amend`, `file-issues`, `triage`, `improve-architecture`, `handoff` | [Ship and maintain](ship-and-maintain.md) |

The **project layer** is optional and sits above the per-feature chain: on a large project, [`establish-project`](../skills/establish-project.md) writes a repo-level product vision and an IDed architecture-invariant spine that the discovery, spec, execution, and review phases consult when present — and ignore cleanly when absent. See [the artifact model](../concepts/artifacts.md#docsproduct-and-docsarchitecture--the-optional-project-layer).

## Context hygiene — the operational rule

Two facts about context shape how you run this chain, and violating either is expensive.

**Discovery through planning belongs in one unbroken context window.** `brainstorm` → `write-requirements` → `write-design` → `write-plan` is a single continuous act of thinking; each step's output depends on decisions and code knowledge accumulated in the previous ones. If the window is filling before the plan is done, do not push through — run `/handoff`, which writes a resumable document to the OS temp directory, and start a fresh session from it.

**Execution is the opposite.** `execute-plan` sessions are context-isolated *per task by design*. Each task gets a fresh implementer subagent whose entire world is a generated brief file. The controller's context stays reserved for coordination, and progress is appended to `.skills/progress.md` after each task, because conversation memory does not survive compaction and the ledger does.

## Where a chain can restart

The chain is not one-way. Several skills feed back into earlier phases:

- `write-design` and `write-plan` both perform **upstream sync-back**: if designing or planning reveals an approved requirement is *wrong as written* — a false premise, a mechanism named wrong — the requirement's own text is corrected and re-surfaced for approval. Never satisfy a requirement by quietly reinterpreting words you now know are false.
- `debug` exits into the tier-1 mini-spec flow, which means it re-enters `write-requirements`.
- `improve-architecture` ends by handing its chosen candidate to `brainstorm`. Architecture work earns no exemption from the spec gate.
- `amend` escalates to `brainstorm` the moment a "small" change turns out to be new scope.
- `sync-spec` is invoked from `finish-branch`, `release`, and `amend` — and directly, whenever the trace check comes back dirty.

## See also

- [Overview](../methodology/overview.md) — what the system is and why
- [Ceremony tiers](../methodology/ceremony-tiers.md) — which flow your work belongs in
- [`ask`](../skills/ask.md) — the router, when the entry point is unclear
- [Examples](../examples/tier-2-feature.md) — the chain run end to end
