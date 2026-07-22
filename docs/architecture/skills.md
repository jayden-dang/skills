# Architecture domain: Skills

Status: Approved
Date: 2026-07-22
Part of: [`INDEX.md`](./INDEX.md) (architecture SSOT)

Skill inventory for this set. Legend: (U) user-invoked, (m) model-invoked.
Human per-skill pages live under `docs/guide/skills/`. Agent constitution and
quick reference: `AGENTS.md`.

## meta/

1. **using-skills** (m, session-injected) — the gate. 1%-rule, skill-check before
   ANY response, red-flags table, process-skills-before-implementation priority,
   user instructions override skills.
2. **ask** (U) — router. Maps situations to flows; the main idea→ship chain, the
   bugfix on-ramp, the maintenance loop, context hygiene.
3. **writing-skills** (U) — TDD for skills + the authoring vocabulary. The standard
   every skill here is written against. A deterministic check driven by an LLM
   (grep/git under a precise skill) is a first-class form, not an anti-pattern.
4. **teach** (U) — guided teaching of the methodology.

## setup/

5. **setup-repo** (U) — run-once per repo. One-decision-at-a-time wizard: issue
   tracker, triage-label mapping, docs layout, **verify commands**, **release
   steps**, feature-code registry location, project posture, team, optional
   project-docs layer. Writes `docs/agents/*.md` + an `## Agent skills` block.
   Offers to install the session-start hook. Writes only markdown and settings —
   it vendors nothing and installs no linter, CI step, or git hook by default.
   (An optional hard CI gate is documented for teams that want one.)
6. **scaffold-project** (U) — greenfield bootstrap: grills stack/layout decisions,
   scaffolds repo (test harness, formatter/linter, pre-commit, CI stub, README,
   CONTEXT.md seed, docs/specs/INDEX.md), then runs setup-repo. Ends with a
   verified "hello world + one passing test" baseline.

## discovery/

7. **grilling** (m) — the interview primitive.
8. **brainstorm** (m) — HARD GATE: no code until requirements are approved. Explore
   context → search `docs/specs/` for overlapping features → grilling → detours to
   research/prototype → approaches with a recommendation → tier decision.
9. **research** (m) — background investigation against primary sources.
10. **prototype** (m) — throwaway code that answers a question.
11. **domain-modeling** (m) — glossary + ADR upkeep.

## spec/

12. **write-requirements** (m) — produce `requirements.md`: EARS + hierarchical
    IDs, SHALL-CONTINUE-TO guards, Out-of-Scope. Approval gate. IDs immutable once
    approved.
13. **write-design** (m) — `design.md`: architecture, `Satisfies:` per section,
    seams agreed. Approval gate.
14. **write-plan** (m) — `tasks.md`: Global Constraints verbatim, per-task
    Files/Interfaces, TDD steps, `_Requirements:` footers. Coverage self-check via
    the `trace` skill: every requirement cited by ≥1 task before execution starts.

## execution/

15. **execute-plan** (m) — fresh subagent per task via file handoffs in `.skills/`.
    The task brief and review package are assembled by the agent directly (copy the
    task block + Global Constraints; `git log`/`git diff` into a bundle) — no helper
    scripts. Implementer contract, two-verdict task review, progress ledger.
16. **tdd** (m) — Iron Law: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST. Test
    only at pre-agreed seams; every test carries its requirement ID.
17. **debug** (m) — Iron Law: NO FIXES WITHOUT ROOT CAUSE.
18. **verify** (m) — Iron Law: NO COMPLETION CLAIMS WITHOUT FRESH EVIDENCE.
    "Requirements met" claims require the `trace` skill clean + a per-ID checklist
    against acceptance criteria, not just green tests.
19. **trace** (m) — the traceability check (see [artifacts.md](./artifacts.md#the-trace-check)).
    Driven by `grep`/`git`/reads under fixed rules; reports E1–E3 / W1–W2 (and
    E4/E5/W3 when an architecture spine exists). Invoked by verify, release,
    sync-spec, and write-plan.
20. **worktrees** (m) — isolation with a clean-baseline test run before work starts.

## review/

21. **code-review** (m) — two parallel subagents: **Standards** (repo standards +
    code-smell baseline) and **Spec** (diff vs requirements, every finding quotes
    the ID). Includes an inline feature-overlap search (grep `docs/specs/` for the
    diff's paths) so a diff reimplementing a neighbor is caught. Runs the advisory
    `check-invariants` lane when an architecture spine exists.
22. **receive-review** (m) — anti-sycophancy; verify each item before implementing.
23. **check-invariants** (m) — advisory, LLM-judged invariant conformance: per
    `Respects: ARCH-N` citation, a respects/violates/unclear verdict. The semantic
    counterpart to `trace`; never a hard gate.

## acceptance/

24. **acceptance-check** (m) — pre-merge validation from the user's seat; ID-keyed
    checklist dispatched by surface.
25. **acceptance-api** (m) — drive the running backend as a real client.
26. **acceptance-ui** (m) — drive the frontend in a real browser.
27. **dogfood** (m) — the manual sibling; checkable HTML artifact.

## craft/

28. **design-page** (m) — the visual-craft gate before any human-facing HTML: names
    the treatment (utilitarian vs editorial), writes the color/type/layout plan, and
    holds the fundamentals (both themes at token level, self-contained assets, copy).
    Required by `dogfood`.

## ship/

29. **finish-branch** (m) — verify → merge/PR/keep/discard → worktree cleanup.
30. **release** (U) — full verify + `trace` clean → changelog from commit trailers
    → version bump → tag → build → smoke-check → release notes.

## track/

31. **amend** (m) — the iteration lane for a shipped feature; routes to the lightest
    tier, always exits through `tdd`, `sync-spec` keeps the trace honest.
32. **triage** (U) — issue state machine; agent briefs as the contract.
33. **sync-spec** (m) — realign the triad after drift: diff requirements ↔ design ↔
    tasks ↔ tests via the `trace` skill; update Status fields; update INDEX.md.
34. **improve-architecture** (U) — periodic deepening scan; the natural home for
    promoting a recurring cross-cutting pattern into an architecture invariant.
35. **handoff** (U) — compact the conversation into a handoff doc.
36. **file-issues** (U) — capture a conversation, spec, or idea into tracker issues.
37. **correct-course** (m) — the mid-flight rewind decision: classifies a discovery that
    invalidates an approved plan to the lowest invalidated artifact and routes to the right
    re-entry, delegating content to `write-*` and reconciliation to `sync-spec`.

## project/

38. **establish-project** (U) — the optional project-documentation layer: authors and
    maintains `docs/product/vision.md`, this `docs/architecture/` tree, and
    `docs/product/guidelines.md` (create/update/validate modes). Consulted by
    `brainstorm`, `write-design`, `write-plan`, `execute-plan`, and `code-review`;
    entirely optional — absent, the feature workflow is unchanged.

**Deliberately not in v1:** full CI/CD authoring. (The project-documentation layer —
repo-level vision + IDed architecture invariants — is the `project/` bucket; see
[system.md — The project layer](./system.md#the-project-layer-optional).)
