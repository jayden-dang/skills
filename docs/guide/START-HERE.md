# Start here

How the skill set works end to end: the A–Z workflow, the steps to use it in a new
repo, and what every skill does. For the architecture behind it, see
[`docs/architecture/`](../architecture/INDEX.md); for one page per skill, see
[the skill reference](skills/README.md).

The whole set is script-free. A consuming repo installs nothing executable beyond
the session-start hook — traceability is the [`audit-trace`](skills/audit-trace.md) skill
running deterministic `grep`/`git` passes, and feature overlap is an inline search
over `docs/specs/`.

## 1. The A–Z workflow

```
                        gate-session  ── the session gate: runs before every response,
                             │            routes your intent to the right skill
        ┌────────────────────┴─────────────────────────────────────────────┐
        ▼                                                                    │
  ask-me-bro  ── "I'm lost, where do I start?" ── routes to any entry point below  │
        │                                                                    │
 IDEATION → SPEC                          BUILD                    SHIP & MAINTAIN
 ─────────────────                        ─────                    ───────────────
 frame-change ─► specify-behavior ─► design-solution ─► plan-tasks
   [GATE: no code]   (EARS + IDs)     (Satisfies:)   (_Requirements:_ + audit-trace check)
        │                                                 │
        │ tier 0/1 shortcuts                              ▼
        │                     isolate-workspace ─► build-in-waves | build-by-story | build-inline
        ▼                                                 │  (route from Execution-mode + subagents?)
  root-cause / test-first / prove-claim / audit-trace  ◄── discipline skills govern every build ──┘
        (the gates)                                       │
                                                          ▼
              inspect-change ─► validate-feature ─► land-branch ─► cut-release ─► realign-spec
             (Standards+Spec)  (api/ui + review-product-flow)  (merge/PR)    (tag)   (mark Implemented/Shipped)

 MAINTENANCE LOOP:  amend-feature (small change) · publish-issues (context → issues) · triage (incoming issues) · scan-architecture (periodic)
```

**Ceremony tiers** decide how much of the chain you run (see
[ceremony tiers](methodology/ceremony-tiers.md)):

- **Tier 0 (trivial):** `test-first` + `prove-claim` only — no specs.
- **Tier 1 (bugfix):** `root-cause` → a mini-spec (fix requirement + a `SHALL CONTINUE TO`
  guard) → tagged regression test → `prove-claim` → `inspect-change` → `land-branch`.
- **Tier 2 (feature):** the full triad + execute family (`build-in-waves` /
  `build-by-story` / `build-inline`).

**Optional project layer** (large projects, off by default): before feature work,
`/define-project` writes a repo-level product vision and an IDed
architecture-invariant spine (`docs/architecture/`, each rule an `**ARCH-N**`). The
discovery, spec, execution, and review skills consult it when present — a `design.md`
cites `Respects: ARCH-N`, and `audit-trace` checks those citations — and ignore it cleanly when
absent. See [the artifact model](concepts/artifacts.md#docsproduct-and-docsarchitecture--the-optional-project-layer).

**The gates** — hard prohibitions written to survive an agent under pressure (see
[the gates](concepts/gates.md)):

| Gate | Iron law |
|---|---|
| `frame-change` | No code, scaffold nothing, until the tier is stated out loud |
| `test-first` | No production code without a failing test first |
| `root-cause` | No fixes without root-cause investigation first |
| `prove-claim` | No completion claims without fresh verification evidence |

## 2. Using it in a new repo — step by step

**Mental model:** you drive with **9 slash-command skills** (and plain-English
requests); the other 23 are **model-invoked** — they fire on their own when their
trigger matches, and skills hand off to each other. The session gate
([`gate-session`](skills/gate-session.md)), re-injected by the session-start hook
after every `/clear` and compaction, is what makes that routing reliable.

**One-time setup**

1. **Install** — as a Claude Code plugin, or `npx skills@latest add jayden-dang/skills`.
   From a clone:
   ```bash
   for d in skills/*/*/; do ln -sfn "$PWD/$d" ~/.claude/skills/$(basename "$d"); done
   ```
   Nothing is installed *into* your project.
2. **Configure the repo** — run **`/bootstrap-repo`** (brand-new project) or
   **`/configure-repo`** (existing repo). It's a one-decision-at-a-time wizard: issue
   tracker, labels, verify commands (typecheck/lint/test/e2e), release steps, docs
   layout. It writes `docs/agents/*.md`, `docs/specs/INDEX.md`, `CONTEXT.md`, an
   `## Agent skills` block into `AGENTS.md`/`CLAUDE.md`, and offers the
   session-start hook. It installs **no scripts, no linters, no CI**.

**Building a feature (tier 2)** — you mostly type `/frame-change` once and answer
questions; the rest chains automatically:

3. **`/frame-change`** — describe the idea. It explores context, `grep`s
   `docs/specs/` for overlap, grills you, picks the tier, and — no code until then —
   hands off to `specify-behavior`.
4. **`specify-behavior`** (auto) → `requirements.md` with EARS criteria and IDs →
   **you approve**.
5. **`design-solution`** (auto) → `design.md`, each section `Satisfies:` IDs →
   **you approve**.
6. **`plan-tasks`** (auto) → `tasks.md`; runs the [`audit-trace`](skills/audit-trace.md)
   coverage check (every requirement cited by ≥1 task).
7. **`isolate-workspace`** (auto) → isolated workspace with a clean-baseline test run.
8. **Execute family** (auto, one of three) — from `Execution-mode` and route:
   - **`build-in-waves`** — continuous + subagent waves, two-verdict task review, ledger
   - **`build-by-story`** — story-unit + human review units, then ledger
   - **`build-inline`** — controller implements with `test-first`, no implementer subagents
9. **`inspect-change`** (auto) → Standards + Spec axes, plus an inline `docs/specs/`
   overlap check.
10. **`validate-feature`** (auto) → drives the running system
    (`validate-api`/`validate-ui`), optionally `review-product-flow` for a manual pass.
11. **`land-branch`** (auto) → merge / PR / keep / discard.
12. **`/cut-release`** (when shipping) → full prove-claim + `audit-trace` clean → changelog → tag →
    build → notes.
13. **`realign-spec`** (auto) → marks requirements Implemented/Shipped, updates
    `INDEX.md`.

**Fixing a bug (tier 1):** just describe the bug — `root-cause` fires, roots it out, you
add the mini-spec + guard, `test-first` writes the regression test, `prove-claim` proves it,
`land-branch` lands it.

**Maintaining:** `amend-feature` for small in-scope changes, **`/publish-issues`** to capture
a conversation or idea into tracker issues, **`/triage`** for incoming issues,
**`/scan-architecture`** for periodic deepening scans, **`/write-handoff`** to
compact a long session.

## 3. Behavior of every skill (all 36)

`U` = user-invoked slash command · `m` = model-invoked (fires on its trigger)

### meta
| Skill | Kind | Fires when | Core behavior | Produces |
|---|---|---|---|---|
| [`gate-session`](skills/gate-session.md) | m (session-injected) | Before any response, every session | The gate: 1%-rule skill check before acting; process skills before implementation skills; your instructions override skills | A routing decision |
| [`ask-me-bro`](skills/ask-me-bro.md) | U | You're unsure which skill or flow applies | Router: maps your situation to the right entry point and chain | A recommended next skill |
| [`author-skills`](skills/author-skills.md) | U | Authoring/editing/reviewing a skill | TDD for skills: no skill ships without a failing pressure-test first; the authoring vocabulary and checklist | A tested skill |

### setup
| Skill | Kind | Fires when | Core behavior | Produces |
|---|---|---|---|---|
| [`configure-repo`](skills/configure-repo.md) | U | Once per repo | One-decision wizard: tracker, labels, verify commands, release steps; writes `docs/agents/*.md` + Agent-skills block; offers the session-start hook; proves the config runs | A configured repo (markdown only) |
| [`bootstrap-repo`](skills/bootstrap-repo.md) | U | Brand-new / greenfield project | Grills stack & layout, scaffolds test harness/linter/CI stub/`INDEX.md`/`CONTEXT.md`, then runs `configure-repo`; ends on a passing hello-world | A bootstrapped baseline |

### project *(optional layer, off by default)*
| Skill | Kind | Fires when | Core behavior | Produces |
|---|---|---|---|---|
| [`define-project`](skills/define-project.md) | U | Large/long-lived project, before feature work | Tri-modal (create/update/validate): grills out a product vision and an IDed `**ARCH-N**` architecture-invariant spine + engineering guidelines; feature skills consult them when present | `docs/product/vision.md`, `docs/architecture/`, `docs/product/guidelines.md` |

### discovery
| Skill | Kind | Fires when | Core behavior | Produces |
|---|---|---|---|---|
| [`clarify-decisions`](skills/clarify-decisions.md) | m | A decision must be drawn out of you | Full-context question cards (inline only), blast-radius first, walks every branch; ends with a decisions table + constraints you confirm | Confirmed decisions package |
| [`frame-change`](skills/frame-change.md) | U | New feature/idea, before any code | HARD GATE (no code): explore context, `docs/specs/` overlap search, grill, pick tier, choose approach; exits only into `specify-behavior` | Tier decision + chosen approach |
| [`research`](skills/research.md) | m | A question turns on external facts | Investigate primary sources, every claim cited; fan-out + adversarial verify for high-stakes questions | A cited notes file |
| [`run-spike`](skills/run-spike.md) | m | A design question needs a runnable answer | Throwaway spike — a logic TUI or 3 structurally different UI variants; capture the answer, then delete/absorb | The answer (as ADR/req/commit) |
| [`define-domain`](skills/define-domain.md) | m | A term is fuzzy, or a hard-to-reverse decision | Challenge terms against `CONTEXT.md`, update the glossary inline; ADRs only when hard-to-reverse + surprising | Glossary / ADR updates |
| [`interpret-session`](skills/interpret-session.md) | U | Frame Changeing in English but thinking/deciding in another language | Companion session: per pasted response, a committed stance plus translate → explain → the detail behind it; the English reply once the direction is settled | Native-language analysis + a reply to paste back |

### spec
| Skill | Kind | Fires when | Core behavior | Produces |
|---|---|---|---|---|
| [`specify-behavior`](skills/specify-behavior.md) | m | Approved discovery → requirements | EARS acceptance criteria + hierarchical IDs, guards, explicit Out-of-Scope; ambiguity/testability scan; approval gate; IDs immutable once approved | `requirements.md` |
| [`design-solution`](skills/design-solution.md) | m | Approved requirements → design | Architecture, file map, `Satisfies:` per section, testing seams agreed; every requirement maps to a section; approval gate | `design.md` |
| [`plan-tasks`](skills/plan-tasks.md) | m | Approved design → plan | Bite-sized TDD tasks with Files/Interfaces, Global Constraints verbatim, `_Requirements:_` footers; runs `audit-trace` coverage check | `tasks.md` |

### execution
| Skill | Kind | Fires when | Core behavior | Produces |
|---|---|---|---|---|
| [`build-in-waves`](skills/build-in-waves.md) | m | Approved `tasks.md`, `Execution-mode: continuous`, subagent waves | Fresh subagent per task; two-verdict review; parallel waves; no human pause between tasks; ledger | Implemented, reviewed tasks |
| [`build-by-story`](skills/build-by-story.md) | m | Approved `tasks.md`, `Execution-mode: story-unit` | Derived review units; unit agent review → human unlock; mode-change write-back; unit ledger | Story-gated implemented units |
| [`build-inline`](skills/build-inline.md) | m | Approved plan, no implementer subagents / user chose inline | Controller implements with `test-first`; stop-on-blocker; sequential; no unit barriers | Implemented tasks (self-reviewed) |
| [`test-first`](skills/test-first.md) | m | Writing any production code | **Iron law:** no production code without a failing test first; test only at agreed seams; every test carries its requirement ID | Tested code |
| [`root-cause`](skills/root-cause.md) | m | Anything misbehaves | **Iron law:** no fix without root cause; red-capable command gate first; one falsifiable hypothesis; ≥3 failed fixes = question the architecture | Root-caused fix + guard |
| [`prove-claim`](skills/prove-claim.md) | m | About to claim done/fixed/passing | **Iron law:** no completion claim without fresh evidence; identify→run→read→confirm; "requirements met" needs `audit-trace` clean + per-ID check | A verified claim with evidence |
| [`audit-trace`](skills/audit-trace.md) | m | Traceability check (called by prove-claim/cut-release/realign-spec/plan-tasks) | Deterministic `grep`/`git` passes + fixed rules — E1 undefined-ID citation, E2 Implemented/Shipped with no covering test, E3 duplicate definition, W1 Approved uncited, W2 missing Status/code; **coverage is textual** | A finding set (errors/warnings) |
| [`isolate-workspace`](skills/isolate-workspace.md) | m | Starting isolated multi-commit work | Native-tool-first isolation, git-ignore check, clean-baseline test run before work begins | An isolated workspace |

### review
| Skill | Kind | Fires when | Core behavior | Produces |
|---|---|---|---|---|
| [`inspect-change`](skills/inspect-change.md) | m | A branch/diff needs review | Two parallel read-only subagents — Standards (repo standards + code-smell baseline) and Spec (diff vs requirement IDs); inline `docs/specs/` overlap search; calibrated verdict | A two-axis merge verdict |
| [`vet-feedback`](skills/vet-feedback.md) | m | Review feedback / PR comments arrive | Anti-sycophancy: prove-claim each item against the code, push back when the reviewer is wrong, clarify all items before implementing any | A vetted action list |
| [`review-invariants`](skills/review-invariants.md) | m | A design/diff cites `Respects: ARCH-N` (repo has `docs/architecture/`) | Advisory, LLM-judged conformance: per citation, a respects/violates/unclear verdict + rationale; the semantic counterpart to `audit-trace`, never a hard gate | Invariant verdicts |

### acceptance
| Skill | Kind | Fires when | Core behavior | Produces |
|---|---|---|---|---|
| [`validate-feature`](skills/validate-feature.md) | m | Pre-merge; units green but not user-driven | Derive an ID-keyed checklist of user-facing behaviors from the spec, dispatch by surface, close the loop | Validated behaviors + tagged tests |
| [`validate-api`](skills/validate-api.md) | m | Validate a backend as a real client | Get the server up (persist the run command), turn each checklist item into a real request (status/body/persistence), fix via `root-cause`, promote to a tagged integration test | Committed API tests |
| [`validate-ui`](skills/validate-ui.md) | m | Validate a frontend in a real browser | Ensure a Playwright/Chromium harness, write a user-driven spec per flow (role/label locators, reload persistence), run headless, commit tagged specs | Committed e2e tests |
| [`review-product-flow`](skills/review-product-flow.md) | m | A manual, human-eyeball pass | Scope abilities with a coverage gate (happy + edge/error/nonbehavior/persist kinds), ground each in real code, boot the app, build a checkable HTML artifact with `data-kind` slots | An HTML test guide + findings |
| [`run-product-walkthrough`](skills/run-product-walkthrough.md) | m | An existing review-product-flow guide must be executed, not only authored | Parse the guide into a run ledger, drive every case in a real browser, require backend probes for state cases, fix via `root-cause`, resume from the ledger | Evidence-backed run ledger + report |

### ship
| Skill | Kind | Fires when | Core behavior | Produces |
|---|---|---|---|---|
| [`land-branch`](skills/land-branch.md) | m | Implementation done; integration decision | Prove Claim tests → four options (merge / PR / keep / discard — "discard" must be typed), provenance-checked worktree cleanup, re-run tests after merge | An integrated branch |
| [`cut-release`](skills/cut-release.md) | U | Shipping a cut-release | Full prove-claim + `audit-trace` clean → changelog assembled from commit trailers → version bump → tag → build → smoke-check → release notes | A tagged release |

### track
| Skill | Kind | Fires when | Core behavior | Produces |
|---|---|---|---|---|
| [`amend-feature`](skills/amend-feature.md) | m | Small in-scope change to a shipped feature | Read the triad, classify the change out loud, route to the lightest lane (tier 0 → `test-first`; tier 1 → mini-spec → `test-first`; new scope → escalate to `frame-change`); always exits through `test-first` | A routed, traced change |
| [`reroute-plan`](skills/reroute-plan.md) | m | A mid-execution discovery invalidated the approved plan | Diagnose (What/Where/Why/How), classify the lowest invalidated artifact with evidence, route to the matching re-entry skill; delegate content to `write-*` and reconciliation to `realign-spec` | A classified, routed plan correction |
| [`publish-issues`](skills/publish-issues.md) | U | A conversation / spec / idea to capture as tracker work | Break into tracer-bullet vertical slices with blocking edges, quiz the user, publish agent-ready issues in dependency order (native blocking links or local `.scratch/` files); AI-marked so `triage` skips them | Agent-ready tracker issues |
| [`triage`](skills/triage.md) | U | Incoming issues / PRs | Issue state machine, redundancy + prior-rejection checks, prove-claim claims before recommending, agent briefs as the contract; wontfix → `.out-of-scope/` | Triaged issues + agent briefs |
| [`realign-spec`](skills/realign-spec.md) | m | A feature's spec has drifted from reality | Diff requirements ↔ design ↔ tasks ↔ tests via `audit-trace`; add tasks for new requirements; flag orphans; update `Status:` + `INDEX.md` | A realigned triad |
| [`scan-architecture`](skills/scan-architecture.md) | U | Periodic deepening scan | Friction scan (shallow modules, poor locality, untested seams, deletion test), self-contained HTML report, grill through the chosen candidate; feeds back into `frame-change` | Improvement candidates |
| [`write-handoff`](skills/write-handoff.md) | U | Compacting / continuing a long session | Compact the conversation into a handoff doc (reference by path, redact secrets, suggested-skills section); optional background-agent continuation | A handoff doc |

## Where to go next

- [Methodology overview](methodology/overview.md) — what this is and what it defends against
- [Traceability](concepts/traceability.md) — the spine, and how the `audit-trace` check keeps it honest
- [The process, phase by phase](process/README.md)
- [Examples](examples/tier-2-feature.md) — tier 0, 1, and 2 walkthroughs
- [`docs/architecture/`](../architecture/INDEX.md) — architecture SSOT (invariants + system design)
