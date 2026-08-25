# The process

The skill set is a chain. Each link is a hand-off written into a skill body as a `REQUIRED SUB-SKILL:` line, so the chain is not a diagram someone drew afterward — it is how the skills actually reach each other.

## The main flow: idea → ship (tier 2)

```
gate-session                 session gate, injected on startup/clear/compact
      │
      ▼
/forge-prompt (optional)    vague ask → one prompt block for a fresh session (names no lane)
      │                      (skip when root-cause / frame-change / amend-feature already clear)
      ▼
frame-change                   clarify-decisions + define-domain; research/run-spike detours;
                             load-subgraph neighbors; tier decision; approach chosen
                             ══ HARD GATE: no code, no scaffolding ══
      │
      ▼
specify-behavior           EARS criteria + hierarchical IDs; guard requirements
                             ══ approval gate on the written file ══
      │
      ▼
design-solution                 Satisfies: per section; seams pre-agreed; design-it-twice
                             ══ approval gate ══
      │
      ▼
plan-tasks                   vertical-slice tasks with _Requirements:_ footers;
                             coverage check; (optional) publish issues
      │
      ▼
isolate-workspace                    isolated workspace, clean baseline
      │
      ▼
execute family               build-in-waves | build-by-story | build-inline
                             per task: brief → implement (test-first) → review/ledger →
                             two-verdict review → fixes → ledger
                             [debug on failures; prove-claim before any claim]
      │
      ▼
inspect-change                  whole-branch, two axes: Standards + Spec-by-ID
      │
      ▼
[polish-diff if predicate]   execute-common close sequence — polish / sample / product-walk
      │                      only when their observable predicates hold
      ▼
validate-feature             drive the running system through the spec's user-facing
                             behaviors (API + UI); fix; promote to domain-language tests
      │
      ▼
[sample notes]             execute-common writes sample: required or skip
      │
      ▼
land-branch                one human station + Status: Implemented (realign-spec
                             only if still Approved and evidence holds)
      │
      │  (many features may sit Implemented)
      ▼
/cut-release                   separate loop: last-tag..HEAD cohort of Implemented
                             → version, tag, notes → those specs Shipped
                             (does not call realign-spec)
      │
      ▼
realign-spec                    anti-rot / land forgot-net — not the cut close-out
```

## The bugfix flow (tier 1)

```
root-cause                        Phase 1: build a red-capable command and RUN it
                             ══ no theory-building before the loop exists ══
      │                      → reproduce & minimise → 3–5 ranked hypotheses
      │                      → one fix at the root cause
      ▼
test-first                          failing regression test first, at a correct seam
      │
      ▼
mini-spec                    a fix requirement + a SHALL CONTINUE TO guard, appended to
                             the owning requirements.md (or docs/specs/fixes.md)
      │
      ▼
prove-claim → inspect-change → land-branch
```

`root-cause` also asks, after the fix lands: *what would have prevented this bug?* When the answer is architectural — no good seam, hidden coupling, tangled callers — the specifics go to `/scan-architecture`.

## The maintenance loop

```
amend-feature                        small in-scope change to a shipped, spec'd feature
                             → tier 0: test-first
                             → tier 1: mini-spec (specify-behavior) → test-first
                             → genuinely new scope: escalate to frame-change

/scan-architecture        periodic codebase-wide friction scan → HTML report
                             → clarify-decisions on the chosen candidate → frame-change

/publish-issues                 a conversation, spec, or idea → tracer-bullet issues
                             on the tracker → execute or implement directly

/triage                      incoming issues and external PRs → the state machine
                             → ready-for-agent brief → execute or implement directly

realign-spec                    whenever a spec'd feature changed outside its plan
```

## Phase pages

| Phase | Skills | Page |
|---|---|---|
| Project layer *(optional, above the feature loop)* | `define-project`, `review-invariants` | [`define-project`](../skills/define-project.md) |
| Discovery | `frame-change` (+ `load-subgraph`), `clarify-decisions`, `research`, `run-spike`, `define-domain`, `/pathfind`, `/interpret-session`, `/deepen-codebase`, `/work-the-problem` | [Discovery](discovery.md) |
| Specification | `specify-behavior`, `design-solution`, `plan-tasks` | [Specification](specification.md) |
| Execution | `isolate-workspace`, `build-in-waves`, `build-by-story`, `build-inline`, `test-first`, `root-cause`, `prove-claim`, `audit-trace`, `load-subgraph` | [Execution](execution.md) |
| Review & acceptance | `inspect-change` (+ `load-subgraph`), `polish-diff`, `vet-feedback`, `review-invariants`, `acceptance-*`, `review-product-flow`, `run-product-walkthrough` | [Review and acceptance](review-and-acceptance.md) |
| Ship & maintain | `land-branch`, `cut-release`, `realign-spec`, `amend-feature`, `/map-features`, `publish-issues`, `triage`, `scan-architecture`, `write-handoff` | [Ship and maintain](ship-and-maintain.md) |

The **project layer** is optional and sits above the per-feature chain: on a large project, [`define-project`](../skills/define-project.md) writes a repo-level product vision and an IDed architecture-invariant spine that the discovery, spec, execution, and review phases consult when present — and ignore cleanly when absent. See [the artifact model](../concepts/artifacts.md#docsproduct-and-docsarchitecture--the-optional-project-layer).

## Context hygiene — the operational rule

Two facts about context shape how you run this chain, and violating either is expensive.

**Discovery through planning belongs in one unbroken context window.** `frame-change` → `specify-behavior` → `design-solution` → `plan-tasks` is a single continuous act of thinking; each step's output depends on decisions and code knowledge accumulated in the previous ones. If the window is filling before the plan is done, do not push through — run `/write-handoff`, which writes a resumable document to the OS temp directory, and start a fresh session from it.

**Execution is the opposite.** Subagent routes (`build-in-waves`, `build-by-story`) isolate *per task by design*: each task gets a fresh implementer whose world is a generated brief file. The controller stays for coordination; progress goes to `.skills/progress.md`. `build-inline` keeps the controller as implementer but still uses the ledger so compaction cannot re-run finished work.

## Where a chain can restart

The chain is not one-way. Several skills feed back into earlier phases:

- `design-solution` and `plan-tasks` both perform **upstream sync-back**: if designing or planning reveals an approved requirement is *wrong as written* — a false premise, a mechanism named wrong — the requirement's own text is corrected and re-surfaced for approval. Never satisfy a requirement by quietly reinterpreting words you now know are false.
- `root-cause` exits into the tier-1 mini-spec flow, which means it re-enters `specify-behavior`.
- `scan-architecture` ends by handing its chosen candidate to `frame-change`. Architecture work earns no exemption from the spec gate.
- `amend-feature` escalates to `frame-change` the moment a "small" change turns out to be new scope.
- `realign-spec` is invoked from `land-branch` (Approved + evidence) and `amend-feature` — and directly, whenever the audit-trace check comes back dirty. `cut-release` does not call it.

## See also

- [Overview](../methodology/overview.md) — what the system is and why
- [Ceremony tiers](../methodology/ceremony-tiers.md) — which flow your work belongs in
- [On-ramps](on-ramps.md) — one home for which skill starts a situation
- [`ask-me-bro`](../skills/ask-me-bro.md) — the router, when the entry point is unclear
- [Examples](../examples/tier-2-feature.md) — the chain run end to end
