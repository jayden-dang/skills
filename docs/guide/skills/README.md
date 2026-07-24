# Skill reference

Forty-two skills in eleven buckets. Each has its own page.

**Invocation** is the thing to check first. A **model-invocable** skill is invoked by the agent on its own when its description matches the situation. A **user-invoked** skill carries `disable-model-invocation: true` in its frontmatter — the agent *cannot* invoke it, so you run it as a slash command.

The composition rule that follows: a user-invoked skill may invoke model-invoked skills, never another user-invoked one. See [The skill model](../concepts/skill-model.md).

---

## meta

The skills that govern the other skills.

| Skill | Invocation | What it does |
|---|---|---|
| [`using-skills`](using-skills.md) | model (session-injected) | The gate. If there is even a 1% chance a skill applies, invoke it first |
| [`ask`](ask.md) | `/ask` | The router. Maps any situation to the right entry point |
| [`writing-skills`](writing-skills.md) | `/writing-skills` | TDD for process documentation. The standard every skill here is written against |

## setup

Run once per repo.

| Skill | Invocation | What it does |
|---|---|---|
| [`setup-repo`](setup-repo.md) | `/setup-repo` | The seven-step wizard. Writes `docs/agents/*.md` markdown config and **proves every configured command actually runs** |
| [`scaffold-project`](scaffold-project.md) | `/scaffold-project` | Greenfield bootstrap to a verified baseline: one passing example test, every tool wired |

## discovery

Turn an idea into an agreed shape. Produces no code.

| Skill | Invocation | What it does |
|---|---|---|
| [`brainstorm`](brainstorm.md) | model | **The hard gate.** No code until the ceremony tier is stated out loud |
| [`grilling`](grilling.md) | model | The interview primitive. One question per message, each with a recommendation |
| [`research`](research.md) | model | Primary sources only. One cited markdown file, ending in Open decisions |
| [`prototype`](prototype.md) | model | Throwaway code answering one design question. The answer is the only deliverable |
| [`domain-modeling`](domain-modeling.md) | model | Maintains `CONTEXT.md` and `docs/adr/`. ADRs pass a three-part gate |

## spec

The triad. Each file approved before the next is written.

| Skill | Invocation | What it does |
|---|---|---|
| [`write-requirements`](write-requirements.md) | model | `requirements.md` — EARS criteria with immutable hierarchical IDs |
| [`write-design`](write-design.md) | model | `design.md` — every section cites what it `Satisfies:`; pre-agrees the test seams |
| [`write-plan`](write-plan.md) | model | `tasks.md` — vertical slices with `_Requirements:_` footers and tagged tests |

## execution

| Skill | Invocation | What it does |
|---|---|---|
| [`execute-plan`](execute-plan.md) | model | One fresh subagent per task, two-verdict reviews, a durable ledger |
| [`tdd`](tdd.md) | model | **Iron Law:** no production code without a failing test first |
| [`debug`](debug.md) | model | **Iron Law:** no fixes without root cause. Phase 1 is the red-capable command gate |
| [`verify`](verify.md) | model | **Iron Law:** no completion claims without fresh evidence |
| [`trace`](trace.md) | model | Deterministic traceability check — grep/git passes, fixed rules, zero errors to pass |
| [`worktrees`](worktrees.md) | model | Isolated workspace, clean baseline. Never fight the harness |

## review

| Skill | Invocation | What it does |
|---|---|---|
| [`code-review`](code-review.md) | model | Two axes — Standards and Spec — run by separate subagents and never merged |
| [`comprehend-change`](comprehend-change.md) | `/comprehend-change` | Outbound self-check: Background → Intuition → Code → Quiz HTML packet |
| [`allocate-attention`](allocate-attention.md) | `/allocate-attention` | Bounded human sample over a range, plus the explicit residue |
| [`receive-review`](receive-review.md) | model | Anti-sycophancy. Verify every claim before implementing or replying |
| [`check-invariants`](check-invariants.md) | model | Advisory, LLM-judged invariant conformance — the semantic counterpart to `trace` |

## acceptance

Green units prove assertions pass. These prove the feature works.

| Skill | Invocation | What it does |
|---|---|---|
| [`acceptance-check`](acceptance-check.md) | model | The orchestrator. Derives an ID-keyed checklist and dispatches by surface |
| [`acceptance-api`](acceptance-api.md) | model | Drives the running backend as a real client. Promotes checks to tagged tests |
| [`acceptance-ui`](acceptance-ui.md) | model | Drives the frontend in real Chromium via Playwright. Commits the specs |
| [`dogfood`](dogfood.md) | model | The manual sibling. Builds a persistent, checkable HTML artifact |

## craft

The visual layer. Fires before any HTML a human will look at.

| Skill | Invocation | What it does |
|---|---|---|
| [`design-page`](design-page.md) | model | Names the treatment, writes the color/type/layout plan, holds the page fundamentals |

## ship

| Skill | Invocation | What it does |
|---|---|---|
| [`finish-branch`](finish-branch.md) | model | Verify + trace gate, then exactly four options. "Discard" must be typed |
| [`release`](release.md) | `/release` | Nine gates. Changelog derived from requirement-ID commit trailers |

## track

| Skill | Invocation | What it does |
|---|---|---|
| [`amend`](amend.md) | model | The maintenance fast lane for a shipped, spec'd feature. Not a gate bypass |
| [`correct-course`](correct-course.md) | model | The mid-flight rewind decision. Classifies a plan-invalidating discovery to the lowest broken artifact and routes the re-entry |
| [`sync-spec`](sync-spec.md) | model | The anti-rot skill. Realigns the triad with what the code actually does |
| [`file-issues`](file-issues.md) | `/file-issues` | Context → tracker issues. Tracer-bullet slices with blocking edges, published agent-ready |
| [`triage`](triage.md) | `/triage` | A two-axis issue state machine. Verify the claim before recommending |
| [`improve-architecture`](improve-architecture.md) | `/improve-architecture` | Codebase-wide friction scan → an HTML report of deepening candidates |
| [`handoff`](handoff.md) | `/handoff` | A resumable document in the OS temp dir. Reference, never duplicate |

## project

The optional documentation layer above the feature workflow. Absent by default.

| Skill | Invocation | What it does |
|---|---|---|
| [`establish-project`](establish-project.md) | `/establish-project` | Authors and maintains the optional project layer — product vision, IDed architecture-invariant spine, and engineering guidelines |

---

## The four Iron Laws, in one place

```
brainstorm   Write NO code, scaffold NOTHING, until the ceremony tier is stated out loud.
tdd          NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
debug        NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
verify       NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

And the one above them, injected into every session:

```
using-skills  If there is even a 1% chance a skill applies, you MUST invoke it first.
```

See [The gates](../concepts/gates.md) for why each is written as a prohibition rather than as advice.

## See also

- [The process](../process/README.md) — how these skills chain together
- [The skill model](../concepts/skill-model.md) — invocation kinds, descriptions, and the authoring vocabulary
- [Start here](../START-HERE.md) — the workflow, new-repo setup, and every skill's behavior
