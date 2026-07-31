# Skill reference

Fifty skills in eleven buckets (engineering package). Each has its own page.

**Invocation** is the thing to check first. A **model-invocable** skill is invoked by the agent on its own when its description matches the situation. A **user-invoked** skill carries `disable-model-invocation: true` in its frontmatter — the agent *cannot* invoke it, so you run it as a slash command.

The composition rule that follows: a user-invoked skill may invoke model-invoked skills, never another user-invoked one. See [The skill model](../concepts/skill-model.md).

---

## meta

The skills that govern the other skills.

| Skill | Invocation | What it does |
|---|---|---|
| [`gate-session`](gate-session.md) | model (session-injected) | The gate. If there is even a 1% chance a skill applies, invoke it first |
| [`route-work`](route-work.md) | `/route-work` | The router. Maps any situation to the right entry point |
| [`author-skills`](author-skills.md) | `/author-skills` | TDD for process documentation. The standard every skill here is written against |

## setup

Run once per repo.

| Skill | Invocation | What it does |
|---|---|---|
| [`configure-repo`](configure-repo.md) | `/configure-repo` | The seven-step wizard. Writes `docs/agents/*.md` markdown config and **proves every configured command actually runs** |
| [`bootstrap-repo`](bootstrap-repo.md) | `/bootstrap-repo` | Greenfield bootstrap to a verified baseline: one passing example test, every tool wired |

## discovery

Turn an idea into an agreed shape. Produces no code.

| Skill | Invocation | What it does |
|---|---|---|
| [`frame-change`](frame-change.md) | model | **The hard gate.** No code until the ceremony tier is stated out loud |
| [`probe-decisions`](probe-decisions.md) | model | The interview primitive. Full-context question cards, decisions table at close |
| [`research`](research.md) | model | Primary sources only. One cited markdown file, ending in Open decisions |
| [`run-spike`](run-spike.md) | model | Throwaway code answering one design question. The answer is the only deliverable |
| [`define-domain`](define-domain.md) | model | Maintains `CONTEXT.md` and `docs/adr/`. ADRs pass a three-part gate |

## spec

The triad. Each file approved before the next is written.

| Skill | Invocation | What it does |
|---|---|---|
| [`specify-behavior`](specify-behavior.md) | model | `requirements.md` — EARS criteria with immutable hierarchical IDs |
| [`design-solution`](design-solution.md) | model | `design.md` — every section cites what it `Satisfies:`; pre-agrees the test seams |
| [`plan-tasks`](plan-tasks.md) | model | `tasks.md` — vertical slices with `_Requirements:_` footers and tagged tests |

## execution

| Skill | Invocation | What it does |
|---|---|---|
| [`build-continuous`](build-continuous.md) | model | Continuous + subagents: fresh implementer per task, two-verdict reviews, parallel waves, ledger |
| [`build-story-units`](build-story-units.md) | model | Story-unit: derived review units, human unlock after each unit, mode-change write-back |
| [`build-inline`](build-inline.md) | model | Controller implements with `test-first`; no implementer subagents; stop-on-blocker; sequential |
| [`test-first`](test-first.md) | model | **Iron Law:** no production code without a failing test first |
| [`root-cause`](root-cause.md) | model | **Iron Law:** no fixes without root cause. Phase 1 is the red-capable command gate |
| [`prove-claim`](prove-claim.md) | model | **Iron Law:** no completion claims without fresh evidence |
| [`audit-trace`](audit-trace.md) | model | Deterministic traceability check — grep/git passes, fixed rules, zero errors to pass |
| [`isolate-workspace`](isolate-workspace.md) | model | Isolated workspace, clean baseline. Never fight the harness |

## review

| Skill | Invocation | What it does |
|---|---|---|
| [`inspect-change`](inspect-change.md) | model | Two axes — Standards and Spec — run by separate subagents and never merged |
| [`study-change`](study-change.md) | `/study-change` | Outbound self-check: Background → Intuition → Code → Quiz HTML packet |
| [`brief-team`](brief-team.md) | `/brief-team` | Team-shared pitch+map HTML under `docs/explainers/` (no quiz, never a ship gate) |
| [`sample-attention`](sample-attention.md) | `/sample-attention` | Bounded human sample over a range, plus the explicit residue |
| [`vet-feedback`](vet-feedback.md) | model | Anti-sycophancy. Prove Claim every claim before implementing or replying |
| [`judge-invariants`](judge-invariants.md) | model | Advisory, LLM-judged invariant conformance — the semantic counterpart to `audit-trace` |

## acceptance

Green units prove assertions pass. These prove the feature works.

| Skill | Invocation | What it does |
|---|---|---|
| [`validate-feature`](validate-feature.md) | model | The orchestrator. Derives an ID-keyed checklist and dispatches by surface |
| [`validate-api`](validate-api.md) | model | Drives the running backend as a real client. Promotes checks to tagged tests |
| [`validate-ui`](validate-ui.md) | model | Drives the frontend in real Chromium via Playwright. Commits the specs |
| [`walk-product`](walk-product.md) | model | The manual sibling. Builds a persistent, checkable HTML artifact |
| [`drive-walk`](drive-walk.md) | model | Executes an existing walk-product guide in a real browser; run ledger with FE+BE evidence |

## craft

The visual layer. Fires before any HTML a human will look at.

| Skill | Invocation | What it does |
|---|---|---|
| [`craft-page`](craft-page.md) | model | Names the treatment, writes the color/type/layout plan, holds the page fundamentals |

## ship

| Skill | Invocation | What it does |
|---|---|---|
| [`land-branch`](land-branch.md) | model | Prove Claim + audit-trace gate, then exactly four options. "Discard" must be typed |
| [`cut-release`](cut-release.md) | `/cut-release` | Nine gates. Changelog derived from requirement-ID commit trailers |

## track

| Skill | Invocation | What it does |
|---|---|---|
| [`amend-feature`](amend-feature.md) | model | The maintenance fast lane for a shipped, spec'd feature. Not a gate bypass |
| [`reroute-plan`](reroute-plan.md) | model | The mid-flight rewind decision. Classifies a plan-invalidating discovery to the lowest broken artifact and routes the re-entry |
| [`realign-spec`](realign-spec.md) | model | The anti-rot skill. Realigns the triad with what the code actually does |
| [`status-roadmap`](status-roadmap.md) | `/status-roadmap` | The horizontal check. Derives where the plan stands from the roadmap, the specs and git, then names one next action. Writes nothing |
| [`assess-milestone`](assess-milestone.md) | `/assess-milestone` | The close gate. Judges whether a milestone's outcome was achieved, records it append-only, and holds the close until you dispose of the verdict |
| [`publish-issues`](publish-issues.md) | `/publish-issues` | Context → tracker issues. Audit Tracer-bullet slices with blocking edges, published agent-ready |
| [`triage`](triage.md) | `/triage` | A two-axis issue state machine. Verify the claim before recommending |
| [`scan-architecture`](scan-architecture.md) | `/scan-architecture` | Codebase-wide friction scan → an HTML report of deepening candidates |
| [`write-handoff`](write-handoff.md) | `/write-handoff` | A resumable document in the OS temp dir. Reference, never duplicate |

## project

The optional documentation layer above the feature workflow. Absent by default.

| Skill | Invocation | What it does |
|---|---|---|
| [`anchor-project`](anchor-project.md) | `/anchor-project` | Authors and maintains the optional project layer — product vision, IDed architecture-invariant spine, and engineering guidelines |
| [`dispose-pivot`](dispose-pivot.md) | `/dispose-pivot` | Disposition ledger when a product pivot puts shipped code at odds with a new vision or architecture — before vision rewrites |
| [`plan-milestones`](plan-milestones.md) | model-invocable | Authors and maintains `docs/roadmap/INDEX.md` — `MILE-N` milestones and `ROAD-N` items, intent only, progress never stored |

---

## The four Iron Laws, in one place

```
frame-change   Write NO code, scaffold NOTHING, until the ceremony tier is stated out loud.
test-first          NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
root-cause        NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
prove-claim       NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

And the one above them, injected into every session:

```
gate-session  If there is even a 1% chance a skill applies, you MUST invoke it first.
```

See [The gates](../concepts/gates.md) for why each is written as a prohibition rather than as advice.

## See also

- [The process](../process/README.md) — how these skills chain together
- [The skill model](../concepts/skill-model.md) — invocation kinds, descriptions, and the authoring vocabulary
- [Start here](../START-HERE.md) — the workflow, new-repo setup, and every skill's behavior
