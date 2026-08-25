# Skill reference

69 skills in eleven buckets (engineering package); every one has its own page.
See also [Start here](../START-HERE.md).

**Invocation** is the thing to check first. A **model-invocable** skill is invoked by the agent on its own when its description matches the situation. A **user-invoked** skill carries `disable-model-invocation: true` in its frontmatter — the agent *cannot* invoke it, so you run it as a slash command.

The composition rule that follows: a user-invoked skill may invoke model-invoked skills, never another user-invoked one. See [The skill model](../concepts/skill-model.md).

---

## meta

The skills that govern the other skills.

| Skill | Invocation | What it does |
|---|---|---|
| [`gate-session`](gate-session.md) | model (session-injected) | The gate. If there is even a 1% chance a skill applies, invoke it first |
| [`ask-me-bro`](ask-me-bro.md) | `/ask-me-bro` | The router. Maps any situation to the right entry point |
| [`author-skills`](author-skills.md) | `/author-skills` | TDD for process documentation. The standard every skill here is written against |
| [`teach-pack`](teach-pack.md) | `/teach-pack` | Guided teaching of the methodology |

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
| [`forge-prompt`](forge-prompt.md) | user | Vague ask → one paste-ready prompt block for a fresh session, via a question-by-question interview; names no next step |
| [`frame-change`](frame-change.md) | model | **The hard gate.** No code until the ceremony tier is stated out loud; neighbors via `load-subgraph` schema 1.1 |
| [`clarify-decisions`](clarify-decisions.md) | model | The interview primitive; nested reuses retrieval package, standalone loads once |
| [`research`](research.md) | model | Primary sources only. One cited markdown file, ending in Open decisions |
| [`run-spike`](run-spike.md) | model | Throwaway code answering one design question. The answer is the only deliverable |
| [`define-domain`](define-domain.md) | model | Maintains `CONTEXT.md` and `docs/adr/`. ADRs pass a three-part write gate; prune classifies keep / archive / drop |
| [`pathfind`](pathfind.md) | `/pathfind` | Layer 0 multi-session decision map (Chart / Work) before delivery |
| [`interpret-session`](interpret-session.md) | `/interpret-session` | Time-boxed companion: stance + paste-back reply (gấp / second-opinion) |
| [`deepen-codebase`](deepen-codebase.md) | `/deepen-codebase` | Learning companion: dual-axis deep foundation for any subject; no product decision |
| [`work-the-problem`](work-the-problem.md) | `/work-the-problem` | Multi-round deep solve + foundation→feature teaching + disk artifacts + carry-back |

## spec

The triad. Each file approved before the next is written.

| Skill | Invocation | What it does |
|---|---|---|
| [`specify-behavior`](specify-behavior.md) | model | `requirements.md` — EARS criteria with immutable hierarchical IDs |
| [`design-solution`](design-solution.md) | model | `design.md` — every section cites what it `Satisfies:`; Step 1 fresh `load-subgraph` before reuse ladder |
| [`plan-tasks`](plan-tasks.md) | model | `tasks.md` — vertical slices; after file map: `blast_radius` + `cluster(feature CODE)` |

## execution

| Skill | Invocation | What it does |
|---|---|---|
| [`build-in-waves`](build-in-waves.md) | model | Continuous + subagents: fresh implementer per task, two-verdict reviews, parallel waves, ledger |
| [`build-by-story`](build-by-story.md) | model | Story-unit: derived review units, human unlock after each unit, mode-change write-back |
| [`build-inline`](build-inline.md) | model | Controller implements with `test-first`; no implementer subagents; stop-on-blocker; sequential |
| [`execute-common`](execute-common.md) | model | Shared execute-family controller recipe (preflight, ledger, close sequence). Not an entry point |
| [`test-first`](test-first.md) | model | **Iron Law:** no production code without a failing test first |
| [`root-cause`](root-cause.md) | model | **Iron Law:** no fixes without root cause; `load-subgraph` only after Phase 2 (never the RED loop) |
| [`debug-remote`](debug-remote.md) | model | Deployed-env evidence pack (read-only); then `root-cause`. No prod writes |
| [`assess-observability`](assess-observability.md) | model | Readiness finding set for tracing/OTLP/sampling — not an incident |
| [`prove-claim`](prove-claim.md) | model | **Iron Law:** no completion claims without fresh evidence |
| [`audit-trace`](audit-trace.md) | model | Deterministic traceability check — grep/git passes, fixed rules, zero errors to pass |
| [`load-subgraph`](load-subgraph.md) | model | Ask-time neighbors (schema 1.1 path/term evidence), **`cluster(focus)`**, blast_radius from live specs; OWNS coverage; no graph file |
| [`isolate-workspace`](isolate-workspace.md) | model | Isolated workspace, clean baseline. Never fight the harness |
| [`hold-stage`](hold-stage.md) | model | Only the ideas this act uses; the rest stay on disk |

## review

| Skill | Invocation | What it does |
|---|---|---|
| [`inspect-change`](inspect-change.md) | model | Two axes — Standards and Spec — run by separate subagents and never merged; neighbors schema 1.1 via `load-subgraph` |
| [`study-change`](study-change.md) | `/study-change` | Outbound self-check: Background → Intuition → Code → Quiz HTML packet |
| [`teach-build`](teach-build.md) | `/teach-build` | Journey + operation teach packet: deviations retold, runtime map beyond the diff, `.skills/<CODE>/teach-build.html` |
| [`brief-team`](brief-team.md) | `/brief-team` | Team-shared pitch+map HTML under `docs/explainers/` (no quiz, never a ship gate) |
| [`select-review-sample`](select-review-sample.md) | `/select-review-sample` | Bounded human sample over a range, plus the explicit residue |
| [`polish-diff`](polish-diff.md) | model | Behavior-preserving quality pass over a diff before merge |
| [`vet-feedback`](vet-feedback.md) | model | Anti-sycophancy. Prove Claim every claim before implementing or replying |
| [`vet-source`](vet-source.md) | model | Fetched / tool / third-party text that instructs: keep the original job, drop the orders |
| [`speak-outer`](speak-outer.md) | model | Person-facing text: outer register, no process machinery |
| [`review-invariants`](review-invariants.md) | model | Advisory, LLM-judged invariant conformance — the semantic counterpart to `audit-trace` |
| [`review-ui`](review-ui.md) | model | Live, screenshot-backed design review of UI-touching diffs — three viewports, states, contrast, token conformance |

## acceptance

Green units prove assertions pass. These prove the feature works.

| Skill | Invocation | What it does |
|---|---|---|
| [`validate-feature`](validate-feature.md) | model | The orchestrator. Derives an ID-keyed checklist and dispatches by surface |
| [`validate-api`](validate-api.md) | model | Drives the running backend as a real client. Promotes checks to tagged tests |
| [`validate-ui`](validate-ui.md) | model | Drives the frontend in real Chromium via Playwright. Commits the specs |
| [`review-product-flow`](review-product-flow.md) | model | The manual sibling. Builds a persistent, checkable HTML artifact |
| [`vet-product-flow`](vet-product-flow.md) | model | Isolated implementation-surface judgment before dogfood; missing-situation findings |
| [`run-product-walkthrough`](run-product-walkthrough.md) | model | Executes an existing review-product-flow guide in a real browser; run ledger with FE+BE evidence |

## craft

The visual layer. Fires before any HTML a human will look at.

| Skill | Invocation | What it does |
|---|---|---|
| [`craft-page`](craft-page.md) | model | Names the treatment, writes the color/type/layout plan, holds the page fundamentals; figure-gated diagram recipes when a primary figure is warranted |
| [`draft-ui`](draft-ui.md) | model | Divergent real-HTML screen variants + review loop + locked ui-brief the design chain lifts |
| [`draft-ux`](draft-ux.md) | model | Runnable takes of one flow that differ in when the world changes + review loop + a locked `## Interaction` section in the same brief |

## ship

| Skill | Invocation | What it does |
|---|---|---|
| [`land-branch`](land-branch.md) | model | Verify, author commits + PR text, then merge / PR / keep / discard / block. Agent PR text is truth |
| [`record-verdict`](record-verdict.md) | model | Immutable decision record before a production crossing |
| [`cut-release`](cut-release.md) | `/cut-release` | Full prove-claim + audit-trace. Changelog from requirement-ID commit trailers |

## track

| Skill | Invocation | What it does |
|---|---|---|
| [`amend-feature`](amend-feature.md) | model | The maintenance fast lane for a shipped, spec'd feature. Not a gate bypass |
| [`reroute-plan`](reroute-plan.md) | model | The mid-flight rewind decision. Classifies a plan-invalidating discovery to the lowest broken artifact and routes the re-entry |
| [`realign-spec`](realign-spec.md) | model | The anti-rot skill. Realigns the triad with what the code actually does |
| [`refresh-roadmap-status`](refresh-roadmap-status.md) | `/refresh-roadmap-status` | The horizontal check. Derives where the plan stands from the roadmap, the specs and git, then names one next action. Writes nothing |
| [`assess-milestone`](assess-milestone.md) | `/assess-milestone` | The close gate. Judges whether a milestone's outcome was achieved, records it append-only, and holds the close until you dispose of the verdict |
| [`publish-issues`](publish-issues.md) | `/publish-issues` | Context → tracker issues. Tracer-bullet slices with blocking edges, published agent-ready |
| [`triage`](triage.md) | `/triage` | A two-axis issue state machine. Verify the claim before recommending |
| [`scan-architecture`](scan-architecture.md) | `/scan-architecture` | Codebase-wide friction scan → an HTML report of deepening candidates |
| [`map-features`](map-features.md) | `/map-features` | Brownfield backfill: Feature code, ROAD binds, OWNS gaps, DEPENDS_ON candidates (confirm only) |
| [`write-handoff`](write-handoff.md) | `/write-handoff` | A resumable document in the OS temp dir. Reference, never duplicate |
| [`record-debt`](record-debt.md) | `/record-debt` | Banks a finding judged real and deliberately left unfixed into `docs/quality/debt.md`. Decisions, never observations |

## project

The optional documentation layer above the feature workflow. Absent by default.

| Skill | Invocation | What it does |
|---|---|---|
| [`define-project`](define-project.md) | `/define-project` | Authors and maintains the optional project layer — product vision, IDed architecture-invariant spine, and engineering guidelines |
| [`define-system-doc`](define-system-doc.md) | `/define-system-doc` | One Hybrid 1A system-doc artifact per run (e.g. Codebase Map); pack catalog under the skill |
| [`assess-pivot-impact`](assess-pivot-impact.md) | `/assess-pivot-impact` | Disposition ledger when a product pivot puts shipped code at odds with a new vision or architecture — before vision rewrites |
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
