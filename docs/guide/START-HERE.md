# Start here

How the skill set works end to end: the A–Z workflow, the steps to use it in a new
repo, and what every skill does. For the architecture behind it, see
[DESIGN.md](../../DESIGN.md); for one page per skill, see
[the skill reference](skills/README.md).

The whole set is script-free. A consuming repo installs nothing executable beyond
the session-start hook — traceability is the [`trace`](skills/trace.md) skill
running deterministic `grep`/`git` passes, and feature overlap is an inline search
over `docs/specs/`.

## 1. The A–Z workflow

```
                        using-skills  ── the session gate: runs before every response,
                             │            routes your intent to the right skill
        ┌────────────────────┴─────────────────────────────────────────────┐
        ▼                                                                    │
  ask  ── "I'm lost, where do I start?" ── routes to any entry point below  │
        │                                                                    │
 IDEATION → SPEC                          BUILD                    SHIP & MAINTAIN
 ─────────────────                        ─────                    ───────────────
 brainstorm ─► write-requirements ─► write-design ─► write-plan
   [GATE: no code]   (EARS + IDs)     (Satisfies:)   (_Requirements:_ + trace check)
        │                                                 │
        │ tier 0/1 shortcuts                              ▼
        │                                  worktrees ─► execute-plan
        ▼                                                 │  (per task: tdd → review → ledger)
  debug / tdd / verify / trace  ◄── discipline skills govern every build ──┘
        (the gates)                                       │
                                                          ▼
              code-review ─► acceptance-check ─► finish-branch ─► release ─► sync-spec
             (Standards+Spec)  (api/ui + dogfood)  (merge/PR)    (tag)   (mark Implemented/Shipped)

 MAINTENANCE LOOP:  amend (small change) · file-issues (context → issues) · triage (incoming issues) · improve-architecture (periodic)
```

**Ceremony tiers** decide how much of the chain you run (see
[ceremony tiers](methodology/ceremony-tiers.md)):

- **Tier 0 (trivial):** `tdd` + `verify` only — no specs.
- **Tier 1 (bugfix):** `debug` → a mini-spec (fix requirement + a `SHALL CONTINUE TO`
  guard) → tagged regression test → `verify` → `code-review` → `finish-branch`.
- **Tier 2 (feature):** the full triad + `execute-plan`.

**Optional project layer** (large projects, off by default): before feature work,
`/establish-project` writes a repo-level product vision and an IDed
architecture-invariant spine (`docs/architecture/`, each rule an `**ARCH-N**`). The
discovery, spec, execution, and review skills consult it when present — a `design.md`
cites `Respects: ARCH-N`, and `trace` checks those citations — and ignore it cleanly when
absent. See [the artifact model](concepts/artifacts.md#docsproduct-and-docsarchitecture--the-optional-project-layer).

**The gates** — hard prohibitions written to survive an agent under pressure (see
[the gates](concepts/gates.md)):

| Gate | Iron law |
|---|---|
| `brainstorm` | No code, scaffold nothing, until the tier is stated out loud |
| `tdd` | No production code without a failing test first |
| `debug` | No fixes without root-cause investigation first |
| `verify` | No completion claims without fresh verification evidence |

## 2. Using it in a new repo — step by step

**Mental model:** you drive with **9 slash-command skills** (and plain-English
requests); the other 23 are **model-invoked** — they fire on their own when their
trigger matches, and skills hand off to each other. The session gate
([`using-skills`](skills/using-skills.md)), re-injected by the session-start hook
after every `/clear` and compaction, is what makes that routing reliable.

**One-time setup**

1. **Install** — as a Claude Code plugin, or `npx skills@latest add jayden-dang/skills`.
   From a clone:
   ```bash
   for d in skills/*/*/; do ln -sfn "$PWD/$d" ~/.claude/skills/$(basename "$d"); done
   ```
   Nothing is installed *into* your project.
2. **Configure the repo** — run **`/scaffold-project`** (brand-new project) or
   **`/setup-repo`** (existing repo). It's a one-decision-at-a-time wizard: issue
   tracker, labels, verify commands (typecheck/lint/test/e2e), release steps, docs
   layout. It writes `docs/agents/*.md`, `docs/specs/INDEX.md`, `CONTEXT.md`, an
   `## Agent skills` block into `AGENTS.md`/`CLAUDE.md`, and offers the
   session-start hook. It installs **no scripts, no linters, no CI**.

**Building a feature (tier 2)** — you mostly type `/brainstorm` once and answer
questions; the rest chains automatically:

3. **`/brainstorm`** — describe the idea. It explores context, `grep`s
   `docs/specs/` for overlap, grills you, picks the tier, and — no code until then —
   hands off to `write-requirements`.
4. **`write-requirements`** (auto) → `requirements.md` with EARS criteria and IDs →
   **you approve**.
5. **`write-design`** (auto) → `design.md`, each section `Satisfies:` IDs →
   **you approve**.
6. **`write-plan`** (auto) → `tasks.md`; runs the [`trace`](skills/trace.md)
   coverage check (every requirement cited by ≥1 task).
7. **`worktrees`** (auto) → isolated workspace with a clean-baseline test run.
8. **`execute-plan`** (auto) → one fresh subagent per task, each doing `tdd`, then a
   two-verdict review, logged to a progress ledger.
9. **`code-review`** (auto) → Standards + Spec axes, plus an inline `docs/specs/`
   overlap check.
10. **`acceptance-check`** (auto) → drives the running system
    (`acceptance-api`/`acceptance-ui`), optionally `dogfood` for a manual pass.
11. **`finish-branch`** (auto) → merge / PR / keep / discard.
12. **`/release`** (when shipping) → full verify + `trace` clean → changelog → tag →
    build → notes.
13. **`sync-spec`** (auto) → marks requirements Implemented/Shipped, updates
    `INDEX.md`.

**Fixing a bug (tier 1):** just describe the bug — `debug` fires, roots it out, you
add the mini-spec + guard, `tdd` writes the regression test, `verify` proves it,
`finish-branch` lands it.

**Maintaining:** `amend` for small in-scope changes, **`/file-issues`** to capture
a conversation or idea into tracker issues, **`/triage`** for incoming issues,
**`/improve-architecture`** for periodic deepening scans, **`/handoff`** to
compact a long session.

## 3. Behavior of every skill (all 36)

`U` = user-invoked slash command · `m` = model-invoked (fires on its trigger)

### meta
| Skill | Kind | Fires when | Core behavior | Produces |
|---|---|---|---|---|
| [`using-skills`](skills/using-skills.md) | m (session-injected) | Before any response, every session | The gate: 1%-rule skill check before acting; process skills before implementation skills; your instructions override skills | A routing decision |
| [`ask`](skills/ask.md) | U | You're unsure which skill or flow applies | Router: maps your situation to the right entry point and chain | A recommended next skill |
| [`writing-skills`](skills/writing-skills.md) | U | Authoring/editing/reviewing a skill | TDD for skills: no skill ships without a failing pressure-test first; the authoring vocabulary and checklist | A tested skill |

### setup
| Skill | Kind | Fires when | Core behavior | Produces |
|---|---|---|---|---|
| [`setup-repo`](skills/setup-repo.md) | U | Once per repo | One-decision wizard: tracker, labels, verify commands, release steps; writes `docs/agents/*.md` + Agent-skills block; offers the session-start hook; proves the config runs | A configured repo (markdown only) |
| [`scaffold-project`](skills/scaffold-project.md) | U | Brand-new / greenfield project | Grills stack & layout, scaffolds test harness/linter/CI stub/`INDEX.md`/`CONTEXT.md`, then runs `setup-repo`; ends on a passing hello-world | A bootstrapped baseline |

### project *(optional layer, off by default)*
| Skill | Kind | Fires when | Core behavior | Produces |
|---|---|---|---|---|
| [`establish-project`](skills/establish-project.md) | U | Large/long-lived project, before feature work | Tri-modal (create/update/validate): grills out a product vision and an IDed `**ARCH-N**` architecture-invariant spine + engineering guidelines; feature skills consult them when present | `docs/product/vision.md`, `docs/architecture/`, `docs/product/guidelines.md` |

### discovery
| Skill | Kind | Fires when | Core behavior | Produces |
|---|---|---|---|---|
| [`grilling`](skills/grilling.md) | m | A decision must be drawn out of you | One question at a time, a recommended answer each, walks every branch; facts from the codebase, decisions from you; confirmation gate | Resolved decisions |
| [`brainstorm`](skills/brainstorm.md) | U | New feature/idea, before any code | HARD GATE (no code): explore context, `docs/specs/` overlap search, grill, pick tier, choose approach; exits only into `write-requirements` | Tier decision + chosen approach |
| [`research`](skills/research.md) | m | A question turns on external facts | Investigate primary sources, every claim cited; fan-out + adversarial verify for high-stakes questions | A cited notes file |
| [`prototype`](skills/prototype.md) | m | A design question needs a runnable answer | Throwaway spike — a logic TUI or 3 structurally different UI variants; capture the answer, then delete/absorb | The answer (as ADR/req/commit) |
| [`domain-modeling`](skills/domain-modeling.md) | m | A term is fuzzy, or a hard-to-reverse decision | Challenge terms against `CONTEXT.md`, update the glossary inline; ADRs only when hard-to-reverse + surprising | Glossary / ADR updates |
| [`interpret`](skills/interpret.md) | U | Brainstorming in English but thinking/deciding in another language | Companion session: per pasted response, translate → simplify → Feynman → independent critique of the options → a copy-ready reply to send back | Native-language analysis + a reply to paste back |

### spec
| Skill | Kind | Fires when | Core behavior | Produces |
|---|---|---|---|---|
| [`write-requirements`](skills/write-requirements.md) | m | Approved discovery → requirements | EARS acceptance criteria + hierarchical IDs, guards, explicit Out-of-Scope; ambiguity/testability scan; approval gate; IDs immutable once approved | `requirements.md` |
| [`write-design`](skills/write-design.md) | m | Approved requirements → design | Architecture, file map, `Satisfies:` per section, testing seams agreed; every requirement maps to a section; approval gate | `design.md` |
| [`write-plan`](skills/write-plan.md) | m | Approved design → plan | Bite-sized TDD tasks with Files/Interfaces, Global Constraints verbatim, `_Requirements:_` footers; runs `trace` coverage check | `tasks.md` |

### execution
| Skill | Kind | Fires when | Core behavior | Produces |
|---|---|---|---|---|
| [`execute-plan`](skills/execute-plan.md) | m | Approved `tasks.md` → build | Fresh subagent per task via `.skills/` file handoffs; implementer contract (4 statuses); two-verdict task review; progress ledger; continuous | Implemented, reviewed tasks |
| [`tdd`](skills/tdd.md) | m | Writing any production code | **Iron law:** no production code without a failing test first; test only at agreed seams; every test carries its requirement ID | Tested code |
| [`debug`](skills/debug.md) | m | Anything misbehaves | **Iron law:** no fix without root cause; red-capable command gate first; one falsifiable hypothesis; ≥3 failed fixes = question the architecture | Root-caused fix + guard |
| [`verify`](skills/verify.md) | m | About to claim done/fixed/passing | **Iron law:** no completion claim without fresh evidence; identify→run→read→confirm; "requirements met" needs `trace` clean + per-ID check | A verified claim with evidence |
| [`trace`](skills/trace.md) | m | Traceability check (called by verify/release/sync-spec/write-plan) | Deterministic `grep`/`git` passes + fixed rules — E1 undefined-ID citation, E2 Implemented/Shipped with no covering test, E3 duplicate definition, W1 Approved uncited, W2 missing Status/code; **coverage is textual** | A finding set (errors/warnings) |
| [`worktrees`](skills/worktrees.md) | m | Starting isolated multi-commit work | Native-tool-first isolation, git-ignore check, clean-baseline test run before work begins | An isolated workspace |

### review
| Skill | Kind | Fires when | Core behavior | Produces |
|---|---|---|---|---|
| [`code-review`](skills/code-review.md) | m | A branch/diff needs review | Two parallel read-only subagents — Standards (repo standards + code-smell baseline) and Spec (diff vs requirement IDs); inline `docs/specs/` overlap search; calibrated verdict | A two-axis merge verdict |
| [`receive-review`](skills/receive-review.md) | m | Review feedback / PR comments arrive | Anti-sycophancy: verify each item against the code, push back when the reviewer is wrong, clarify all items before implementing any | A vetted action list |
| [`check-invariants`](skills/check-invariants.md) | m | A design/diff cites `Respects: ARCH-N` (repo has `docs/architecture/`) | Advisory, LLM-judged conformance: per citation, a respects/violates/unclear verdict + rationale; the semantic counterpart to `trace`, never a hard gate | Invariant verdicts |

### acceptance
| Skill | Kind | Fires when | Core behavior | Produces |
|---|---|---|---|---|
| [`acceptance-check`](skills/acceptance-check.md) | m | Pre-merge; units green but not user-driven | Derive an ID-keyed checklist of user-facing behaviors from the spec, dispatch by surface, close the loop | Validated behaviors + tagged tests |
| [`acceptance-api`](skills/acceptance-api.md) | m | Validate a backend as a real client | Get the server up (persist the run command), turn each checklist item into a real request (status/body/persistence), fix via `debug`, promote to a tagged integration test | Committed API tests |
| [`acceptance-ui`](skills/acceptance-ui.md) | m | Validate a frontend in a real browser | Ensure a Playwright/Chromium harness, write a user-driven spec per flow (role/label locators, reload persistence), run headless, commit tagged specs | Committed e2e tests |
| [`dogfood`](skills/dogfood.md) | m | A manual, human-eyeball pass | Scope every user-facing ability keyed to IDs, ground each in the real code, boot the app, build a checkable HTML artifact you tick off | An HTML test guide + findings |

### ship
| Skill | Kind | Fires when | Core behavior | Produces |
|---|---|---|---|---|
| [`finish-branch`](skills/finish-branch.md) | m | Implementation done; integration decision | Verify tests → four options (merge / PR / keep / discard — "discard" must be typed), provenance-checked worktree cleanup, re-run tests after merge | An integrated branch |
| [`release`](skills/release.md) | U | Shipping a release | Full verify + `trace` clean → changelog assembled from commit trailers → version bump → tag → build → smoke-check → release notes | A tagged release |

### track
| Skill | Kind | Fires when | Core behavior | Produces |
|---|---|---|---|---|
| [`amend`](skills/amend.md) | m | Small in-scope change to a shipped feature | Read the triad, classify the change out loud, route to the lightest lane (tier 0 → `tdd`; tier 1 → mini-spec → `tdd`; new scope → escalate to `brainstorm`); always exits through `tdd` | A routed, traced change |
| [`correct-course`](skills/correct-course.md) | m | A mid-execution discovery invalidated the approved plan | Diagnose (What/Where/Why/How), classify the lowest invalidated artifact with evidence, route to the matching re-entry skill; delegate content to `write-*` and reconciliation to `sync-spec` | A classified, routed plan correction |
| [`file-issues`](skills/file-issues.md) | U | A conversation / spec / idea to capture as tracker work | Break into tracer-bullet vertical slices with blocking edges, quiz the user, publish agent-ready issues in dependency order (native blocking links or local `.scratch/` files); AI-marked so `triage` skips them | Agent-ready tracker issues |
| [`triage`](skills/triage.md) | U | Incoming issues / PRs | Issue state machine, redundancy + prior-rejection checks, verify claims before recommending, agent briefs as the contract; wontfix → `.out-of-scope/` | Triaged issues + agent briefs |
| [`sync-spec`](skills/sync-spec.md) | m | A feature's spec has drifted from reality | Diff requirements ↔ design ↔ tasks ↔ tests via `trace`; add tasks for new requirements; flag orphans; update `Status:` + `INDEX.md` | A realigned triad |
| [`improve-architecture`](skills/improve-architecture.md) | U | Periodic deepening scan | Friction scan (shallow modules, poor locality, untested seams, deletion test), self-contained HTML report, grill through the chosen candidate; feeds back into `brainstorm` | Improvement candidates |
| [`handoff`](skills/handoff.md) | U | Compacting / continuing a long session | Compact the conversation into a handoff doc (reference by path, redact secrets, suggested-skills section); optional background-agent continuation | A handoff doc |

## Where to go next

- [Methodology overview](methodology/overview.md) — what this is and what it defends against
- [Traceability](concepts/traceability.md) — the spine, and how the `trace` check keeps it honest
- [The process, phase by phase](process/README.md)
- [Examples](examples/tier-2-feature.md) — tier 0, 1, and 2 walkthroughs
- [DESIGN.md](../../DESIGN.md) — the architecture spec of record
