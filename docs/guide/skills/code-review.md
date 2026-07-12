# `code-review`

> One diff, two independent axes. Standards and Spec are reviewed by separate subagents and reported separately, because a change can pass one and fail the other.

|  |  |
|---|---|
| **Bucket** | review |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | the diff `git diff <base>...HEAD`, commit list, `docs/specs/INDEX.md`, a feature's `requirements.md`, CLAUDE.md, lint/formatter configs, CONTRIBUTING docs, `CONTEXT.md`, `docs/agents/project.md`, `standards-baseline.md` (beside the skill) |
| **Writes** | nothing — the review is read-only; it produces a report, not commits |
| **Calls** | two READ-ONLY subagents (Standards, Spec) dispatched in parallel; an inline `docs/specs/` search for the duplication check |
| **Called by** | [`execute-plan`](execute-plan.md) (final whole-branch review), or the user asking to review work since some ref |

## When it fires

When a branch, PR, diff, or set of changes needs review before merging. It fires at the end of [`execute-plan`](execute-plan.md) when the plan reaches its final whole-branch review, or whenever the user asks to review the work done since some ref.

The organizing idea is that a diff is judged on **two independent axes**, each run by its own subagent:

- **Standards** — does the code follow this repo's documented conventions and avoid the baseline smells?
- **Spec** — does the code implement what the requirements asked for, ID by ID?

The axes are deliberately separate because a change can pass one and fail the other:

- **Standards pass, Spec fail** — flawless code that builds the wrong thing.
- **Spec pass, Standards fail** — a faithful implementation that tramples the repo's conventions.

Merged reports let one axis mask the other, so a strong showing on Standards can quietly absorb a Spec failure and vice versa.

## The steps

### 1. Pin the range — fail fast

Take the base ref the caller supplied — a sha, branch, tag, or merge-base. Confirm it resolves with `git rev-parse <base>`, and that `git diff <base>...HEAD` is non-empty. Also capture `git log <base>..HEAD --oneline`. A bad ref or an empty diff must fail **here**, not inside two parallel subagents that were dispatched over nothing. If no base was given, ask. *Done when the ref resolves and the diff is non-empty.*

### 2. Locate the spec

Find the governing requirements, in this order:

1. Requirement-ID trailers in the commits (`Implements:`, `Guards:`) — the feature code maps to a spec folder via `docs/specs/INDEX.md`.
2. A `docs/specs/<date>-<feature>/requirements.md` matching the branch or feature name.
3. A path the caller handed you.
4. Otherwise ask the user.

If the user confirms no spec exists, the Spec axis is skipped and the final report says so. *Done when you hold a `requirements.md` path, or an explicit "no spec".*

### 3. Gather the standards sources

Collect whatever documents how code here should be written: CLAUDE.md, lint and formatter configs, CONTRIBUTING-style docs, plus `CONTEXT.md` for the repo's canonical vocabulary. If `docs/agents/project.md` is missing, note it, suggest running [`setup-repo`](setup-repo.md), and proceed with what exists.

On top of the repo's own documents, the Standards axis always carries `standards-baseline.md` (beside the skill). Two rules bind the baseline: **a documented repo standard always overrides it**, and **every baseline hit is a labeled judgment call, never a hard violation**. Skip anything tooling already enforces — a reviewer repeating the linter is noise. *Done when the source list and the baseline path are in hand.*

### 3a. Check for duplication against existing features

Check the diff's changed source files against the features that already exist. `docs/specs/INDEX.md` is the registry — it maps every feature code to its spec folder and the surface it owns — so read it, then `grep docs/specs/` for the changed files' paths and the diff's key terms. Each hit points at a feature whose surface the diff touches; read that feature's `requirements.md` header for its owned paths and Out-of-Scope list. The step never blocks the review:

- If `docs/specs/INDEX.md` is **absent**, the registry is not set up — note that, name [`setup-repo`](setup-repo.md) as the remedy, and say it **at most once per session** rather than on every review. Fall back to grepping `docs/specs/` directly.
- If there is no `docs/specs/` at all, note there is nothing to check against and inject nothing into step 4.
- If no changed file overlaps any feature, state that no existing feature shares the diff's surface and inject nothing into step 4.

*Done when you hold the overlapping features' owned-paths and Out-of-Scope summaries, or an explicit "no overlap" / "no registry".*

### 4. Dispatch both subagents in parallel

Send **one** message containing both dispatches so they run concurrently and neither pollutes the other's context. Both are **read-only**: no mutation of the working tree, index, HEAD, or branch state. To inspect another revision, use a temporary worktree (`git worktree add <tmpdir> <sha>`) — never move HEAD, because a review that leaves HEAD somewhere else is no longer reviewing the diff it was handed. Keep each brief under 400 words, and never pre-judge findings in a dispatch: no "do not flag", no pre-rated severities, since a dispatch that pre-rates its own findings has stopped being a review.

| Subagent | What it receives | What it reports |
|---|---|---|
| **Standards** | the diff command and commit list; the standards-source paths; the path to `standards-baseline.md`, which it MUST read first and check the diff against each of the twelve smells in turn | every place the diff breaks a documented standard (citing document and rule — these may be hard findings); and, for each of the twelve baseline smells, every hit (naming the smell, quoting the hunk — always judgment calls). Repo documents override the baseline; skip anything tooling enforces; include `CONTEXT.md` vocabulary drift |
| **Spec** | the diff command and commit list; the `requirements.md` path; when step 3a found overlaps, ALSO the neighbor summaries (owned paths + Out-of-Scope) | IDs missing or only partially implemented; behavior no requirement asked for (scope creep); IDs that look implemented but wrong — quoting the requirement ID on every finding. It also verifies each covered ID has a test tagged with it per `docs/agents/project.md` and flags untagged coverage. Where the diff reimplements behavior a shares-surface neighbor already owns, it flags a **reuse-miss** finding citing the neighbor's feature code |

*Done when both reports are back.*

### 5. Aggregate

Present the reports under `## Standards` and `## Spec` headings — lightly cleaned at most. Do **NOT** merge, dedupe across axes, or rerank one axis's findings against the other's; that reranking is exactly what the separation prevents.

When step 2 ended in an explicit "no spec", the Spec axis was never dispatched, and the report says so under the `## Spec` heading rather than leaving it silently empty.

Every finding carries: severity (Critical / Important / Minor), file:line, why it matters, and a suggested fix unless obvious. The skill ends with the verdict block:

```
Ready to merge? Yes | No | With fixes
[1–2 sentences of technical reasoning]
```

*Done when both axis sections and the verdict are delivered.*

## The twelve baseline smells

The Standards subagent walks `standards-baseline.md` and checks the diff against each of these in turn. Every hit is a labeled judgment call; a documented repo standard overrides any item; skip anything tooling enforces. Each entry is **what it is → how to fix.**

1. **Duplicated knowledge** — one fact or rule (a formula, a validation, a mapping) encoded in two or more places in the diff, so a future change must find every copy → extract the single source of truth and make every site consume it.
2. **Shallow module** — a class, function, or file whose interface is nearly as complicated as what it hides; callers gain nothing by going through it → deepen it, or delete it and let callers do the work directly.
3. **Leaky abstraction** — an interface that forces callers to know its internals: exposed storage shapes, required call orderings, error types from three layers down → redesign the boundary so the caller can stay ignorant of the implementation.
4. **Feature envy** — a function that spends its time reading and picking apart another module's data rather than its own → move the behavior onto the module that owns the data.
5. **Long parameter list** — a signature taking so many arguments (or several that always travel together) that call sites become unreadable and error-prone → bundle the co-traveling values into one named type, or let the function fetch what it can derive.
6. **Dead code** — functions, branches, flags, or exports the diff adds or keeps that nothing reaches → delete it; version control remembers.
7. **Speculative generality** — abstraction, hooks, or parameters added for needs no requirement has ("we might need it later") → remove it and inline until a real caller shows up.
8. **Shotgun surgery** — one logical change in the diff forcing small edits scattered across many files → gather the pieces that change together into one module so the next change lands in one place.
9. **Primitive obsession** — a bare string, number, or map standing in for a domain concept (an ID, a money amount, a state) that deserves its own type → introduce the small domain type and move the validation into it.
10. **Mysterious name** — an identifier that hides what it does or holds (`data2`, `process`, `handleStuff`), or one that describes the mechanism instead of the purpose → rename to what it means; if no honest name exists, the design underneath is the problem.
11. **Comment compensating for bad code** — a comment that explains WHAT confusing code does, papering over structure that should explain itself → refactor until the comment is unnecessary; keep comments that explain WHY.
12. **Inconsistent vocabulary** — the same concept under different names across the diff, or a name that contradicts `CONTEXT.md`'s glossary → pick the repo's canonical term and use it everywhere; update `CONTEXT.md` if the term is genuinely new.

## Worked example

Reviewing a branch since `main`. Step 1 resolves the base and the diff is non-empty. Step 2 finds `Implements: BILLING-2.3` trailers, which `docs/specs/INDEX.md` maps to `docs/specs/2026-06-01-billing/requirements.md`. Step 3 gathers CLAUDE.md and the lint config, adds `standards-baseline.md`, and drops the formatter's own rules since tooling enforces them. Step 3a reads `docs/specs/INDEX.md` and greps `docs/specs/` for the changed files' paths, which surfaces an overlap with feature `PRICING`. Both subagents run in one message; the aggregate comes back under separate headings, unmerged:

```
## Standards

- Important — src/billing/invoice.ts:44 — Duplicated knowledge (judgment call).
  The tax-rounding rule (round half-up to cents) is re-encoded here and in
  pricing/round.ts. A rate change now has to find both copies.
  Fix: consume the existing roundCents() helper.

## Spec

- Critical — BILLING-2.3 — the requirement asks the invoice total to include
  the late fee when the due date has passed; invoice.ts computes the total
  before applying lateFee(), so overdue invoices under-bill.
- Minor — reuse-miss (neighbor PRICING) — src/billing/tiers.ts:12 reimplements
  tier lookup that PRICING already owns in pricing/tiers.ts.

Ready to merge? No
The overdue-total bug (BILLING-2.3) mis-bills real invoices; fix it and the
duplicated rounding rule before merging.
```

Note the two axes stay in their own sections. The Standards finding (a duplicated rounding rule) and the Spec finding (an under-billing bug against `BILLING-2.3`) live on the same diff but are never reranked against each other — a clean-code reviewer and a spec reviewer would each have missed the other's finding, which is the whole reason they run apart.

The **reuse-miss** finding only exists because step 3a's `docs/specs/` search surfaced the `PRICING` neighbor and step 4 handed its summary to the Spec subagent. Had the registry been absent, that overlap could go unspotted, the report would carry a one-time note pointing at [`setup-repo`](setup-repo.md), and the review would continue unblocked — the duplication check is advisory, never a gate.

## Why it is written the way it is

The separation is the load-bearing decision. A single reviewer, or a merged report, lets a strong showing on one axis quietly absorb a failure on the other — beautiful code that builds the wrong feature reads as "looks good", and a faithful implementation written in the repo's anti-patterns reads as "ships the requirement". Two subagents dispatched in one message keep each axis's context clean, and the explicit ban on merging, deduping, and reranking in step 5 preserves that separation all the way to the reader.

Running the two in a single message is not just for speed: concurrent dispatch means neither subagent's reasoning ever enters the other's context, so the Standards reviewer cannot be nudged by a Spec finding and vice versa. Independence of judgment, not wall-clock time, is the reason the parallel dispatch is mandatory rather than merely allowed.

The read-only constraint exists because a reviewer that mutates the tree is no longer reviewing the thing that was handed to it. The fail-fast range check in step 1 exists so a bad ref costs one `git rev-parse`, not two wasted subagent runs. And the baseline's two binding rules — repo standards override it, every hit is a judgment call — keep the twelve smells advisory, so the reviewer never hard-fails a diff for a heuristic the repo never signed up for.

Two smaller instructions carry weight for the same reason. **Skip anything tooling already enforces**: a finding that repeats the linter or formatter is noise that buries the findings a human or an agent actually had to reason about. And each subagent brief is capped **under 400 words** and forbidden from pre-judging — a brief that grows unbounded or seeds its own conclusions turns the subagent into an echo of the dispatcher rather than an independent reviewer, which is the failure the two-axis design exists to prevent.

## See also

- [`receive-review`](receive-review.md) — the other side: how the author evaluates these findings as claims
- [Traceability](../concepts/traceability.md) — why the Spec axis checks every covered ID for a tagged test
- [`setup-repo`](setup-repo.md) — sets up the `docs/specs/INDEX.md` registry and `docs/agents/project.md` the review leans on
