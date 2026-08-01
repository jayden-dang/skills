# Architecture domain: Skills

Status: Approved
Date: 2026-07-22
Part of: [`INDEX.md`](./INDEX.md) (architecture SSOT)

Skill inventory for this set. Legend: (U) user-invoked, (m) model-invoked.
Human per-skill pages live under `docs/guide/skills/`. Agent constitution and
quick reference: `AGENTS.md`.

## meta/

1. **gate-session** (m, session-injected) — the gate. 1%-rule, skill-check before
   ANY response, red-flags table, process-skills-before-implementation priority,
   user instructions override skills.
2. **ask-me-bro** (U) — router. Maps situations to flows; the main idea→ship chain, the
   bugfix on-ramp, the maintenance loop, context hygiene.
3. **author-skills** (U) — TDD for skills + the authoring vocabulary. The standard
   every skill here is written against. A deterministic check driven by an LLM
   (grep/git under a precise skill) is a first-class form, not an anti-pattern.
4. **teach-pack** (U) — guided teaching of the methodology.

## setup/

5. **configure-repo** (U) — run-once per repo. One-decision-at-a-time wizard: issue
   tracker, triage-label mapping, docs layout, **verify commands**, **release
   steps**, feature-code registry location, project posture, team, optional
   project-docs layer. Writes `docs/agents/*.md` + an `## Agent skills` block.
   Offers to install the session-start hook. Writes only markdown and settings —
   it vendors nothing and installs no linter, CI step, or git hook by default.
   (An optional hard CI gate is documented for teams that want one.)
6. **bootstrap-repo** (U) — greenfield bootstrap: grills stack/layout decisions,
   scaffolds repo (test harness, formatter/linter, pre-commit, CI stub, README,
   CONTEXT.md seed, docs/specs/INDEX.md), then runs configure-repo. Ends with a
   verified "hello world + one passing test" baseline.

## discovery/

7. **clarify-decisions** (m) — the interview primitive.
8. **frame-change** (m) — HARD GATE: no code until requirements are approved. Explore
   context → `load-subgraph` for overlapping features (terms + paths) → clarify-decisions → detours to
   research/run-spike → approaches with a recommendation → tier decision.
9. **research** (m) — background investigation against primary sources.
10. **run-spike** (m) — throwaway code that answers a question.
11. **define-domain** (m) — glossary + ADR upkeep.
11a. **pathfind** (U) — optional Layer 0: multi-session decision map (Chart/Work);
    plan-don't-do; composes clarify-decisions / research / run-spike; hands off by
    naming only.
11b. **interpret-session** (U) — companion session for non-English decision work;
    names hand-offs only.

## spec/

12. **specify-behavior** (m) — produce `requirements.md`: EARS + hierarchical
    IDs, SHALL-CONTINUE-TO guards, Out-of-Scope. Approval gate. IDs immutable once
    approved.
13. **design-solution** (m) — `design.md`: architecture, `Satisfies:` per section,
    seams agreed. Approval gate.
14. **plan-tasks** (m) — `tasks.md`: Global Constraints verbatim, per-task
    Files/Interfaces, TDD steps, `_Requirements:` footers. Coverage self-check via
    the `audit-trace` skill: every requirement cited by ≥1 task before execution starts.
    Exit: approve plan, then offer one of three execute skills (mode write-back is
    owned by the chosen skill — not a continuous/story-unit interview at Exit).

## execution/

15. **build-in-waves** (m) — `Execution-mode: continuous` + subagent waves. Fresh
    implementer per task via file handoffs in `.skills/`; two-verdict task review;
    parallel waves; progress ledger; no human pause between tasks.
15a. **build-by-story** (m) — `Execution-mode: story-unit`. Derived review units,
    unit agent review → human unlock, mode-change write-back, unit ledger lines;
    whole-branch review still runs after the last unit.
15b. **build-inline** (m) — controller implements sequentially with `test-first`; no
    implementer/reviewer subagents; stop-on-blocker; same ledger shape; no unit
    barriers (even if the header is story-unit).
16. **test-first** (m) — Iron Law: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST. Test
    only at pre-agreed seams; every test carries its requirement ID.
17. **root-cause** (m) — Iron Law: NO FIXES WITHOUT ROOT CAUSE.
18. **prove-claim** (m) — Iron Law: NO COMPLETION CLAIMS WITHOUT FRESH EVIDENCE.
    "Requirements met" claims require the `audit-trace` skill clean + a per-ID checklist
    against acceptance criteria, not just green tests.
19. **audit-trace** (m) — the traceability check (see [artifacts.md](./artifacts.md#the-trace-check)).
    Driven by `grep`/`git`/reads under fixed rules; reports E1–E3 / W1–W2 (and
    E4/E5/W3 when an architecture spine exists). Invoked by prove-claim, cut-release,
    realign-spec, and plan-tasks.
19a. **load-subgraph** (m) — ask-time feature-subgraph derivation (P0–P5); neighbors /
    ancestors / blast_radius / subgraph with OWNS coverage; no graph file. Used by
    frame-change and inspect-change for horizontal neighbors.
20. **isolate-workspace** (m) — isolation with a clean-baseline test run before work starts.

## review/

21. **inspect-change** (m) — two parallel subagents: **Standards** (repo standards +
    code-smell baseline) and **Spec** (diff vs requirements, every finding quotes
    the ID). Obtains horizontal neighbors via `load-subgraph` (paths + optional
    terms) so a diff reimplementing a neighbor is caught. Runs the advisory
    `review-invariants` lane when an architecture spine exists.
21a. **study-change** (U) — outbound self-check: one HTML packet
    (Background → Intuition → Code → Quiz) for a resolved git range; optional
    read-only DREC enrichment; never a ship gate or decision-record emitter.
21b. **brief-team** (U) — team-shared pitch+map HTML under `docs/explainers/`
    for a resolved git range; overwrite + INDEX; no quiz; never a ship gate;
    named (not invoked) from land-branch on large/architecture changes.
21c. **select-review-sample** (U) — bounded human sample over a range plus the
    explicit residue; never a ship gate.
21d. **polish-diff** (m) — behavior-preserving quality cleanup over a diff/branch
    before merge; last tidy step of build-in-waves.
22. **vet-feedback** (m) — anti-sycophancy; prove-claim each item before implementing.
23. **review-invariants** (m) — advisory, LLM-judged invariant conformance: per
    `Respects: ARCH-N` citation, a respects/violates/unclear verdict. The semantic
    counterpart to `audit-trace`; never a hard gate.

## acceptance/

24. **validate-feature** (m) — pre-merge validation from the user's seat; ID-keyed
    checklist dispatched by surface.
25. **validate-api** (m) — drive the running backend as a real client.
26. **validate-ui** (m) — drive the frontend in a real browser.
27. **review-product-flow** (m) — the manual sibling; cases YAML SSOT + shell-rendered HTML;
    coverage gate + kind taxonomy; CLI `render` for the human view.
27a. **vet-product-flow** (m) — isolated judgment of a finished run file against the
    shipped user-observable surface; writes `.skills/<slug>-vet-product-flow.md`
    with code-grounded missing-situation findings; required before agent dogfood.
27b. **run-product-walkthrough** (m) — execute an existing review-product-flow catalog against the product
    app; CLI run ledger (`init`/`mark`/`next`/`report`) with screen + backend
    evidence; never guide localStorage ticks; requires fresh clean vet report (or
    named override); product fails route to `root-cause`.

## craft/

28. **craft-page** (m) — the visual-craft gate before any human-facing HTML: names
    the treatment (utilitarian vs editorial), writes the color/type/layout plan, and
    holds the fundamentals (both themes at token level, self-contained assets, copy).
    Optional craft for `review-product-flow` (default is the checked-in review-product-flow shell).

## ship/

28a. **package-change** (m) — reviewer-facing commits and PR package before
    land-branch; packages uncommitted work as a readable set rather than one lump.
29. **land-branch** (m) — prove-claim → merge/PR/keep/discard/block → worktree cleanup;
    terminal verdicts hand off to `record-verdict` before crossings.
30. **record-verdict** (m) — publish an immutable boundary decision record after a
    named emitter (land-branch or cut-release) obtains a terminal human verdict.
31. **cut-release** (U) — full prove-claim + `audit-trace` clean → changelog from commit trailers
    → version bump → tag → build → smoke-check → release notes; terminal verdict
    emits one decision record.

## track/

32. **amend-feature** (m) — the iteration lane for a shipped feature; routes to the lightest
    tier, always exits through `test-first`, `realign-spec` keeps the audit-trace honest.
33. **triage** (U) — issue state machine; agent briefs as the contract.
34. **realign-spec** (m) — realign the triad after drift: diff requirements ↔ design ↔
    tasks ↔ tests via the `audit-trace` skill; update Status fields; update INDEX.md.
34a. **refresh-roadmap-status** (U) — horizontal plan-to-reality check over
    `docs/roadmap/INDEX.md` + specs + git; names one next action; writes nothing.
34b. **assess-milestone** (U) — close gate for a `MILE-N`; append-only disposition;
    holds close until the user disposes of the verdict.
35. **scan-architecture** (U) — periodic deepening scan; the natural home for
    promoting a recurring cross-cutting pattern into an architecture invariant.
35a. **map-features** (U) — brownfield backfill: propose Feature code / ROAD bind /
    OWNS gaps / DEPENDS_ON candidates → confirm → additive SSOT only.
36. **write-handoff** (U) — compact the conversation into a handoff doc.
37. **publish-issues** (U) — capture a conversation, spec, or idea into tracker issues.
38. **reroute-plan** (m) — the mid-flight rewind decision: classifies a discovery that
    invalidates an approved plan to the lowest invalidated artifact and routes to the right
    re-entry, delegating content to the spec triad and reconciliation to `realign-spec`.

## project/

39. **define-project** (U) — the optional project-documentation layer: authors and
    maintains `docs/product/vision.md`, this `docs/architecture/` tree, and
    `docs/product/guidelines.md` (create/update/validate modes). Consulted by
    `frame-change`, `design-solution`, `plan-tasks`, `build-in-waves`, and `inspect-change`;
    entirely optional — absent, the feature workflow is unchanged.
39a. **assess-pivot-impact** (U) — disposition ledger when a product pivot puts shipped
    code at odds with a new vision or architecture. Writes
    `docs/product/pivot-ledger.md` only; names `/define-project` (update) after
    confirmation. Does not rewrite the vision layer itself.
39b. **plan-milestones** (m) — authors and revises `docs/roadmap/INDEX.md`
    (`MILE-N` / `ROAD-N`); any roadmap edit goes through this skill.

**Deliberately not in v1:** full CI/CD authoring. (The project-documentation layer —
repo-level vision + IDed architecture invariants — is the `project/` bucket; see
[system.md — The project layer](./system.md#the-project-layer-optional).)
