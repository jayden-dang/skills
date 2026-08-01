# Requirements: Vet product flow

Feature code: VPF
Status: Approved
Date: 2026-08-01

<!--
Rules:
- Feature code: 2-12 chars, A-Z0-9, starts with a letter, unique repo-wide.
  Register it in docs/specs/INDEX.md before use.
- Every acceptance criterion gets a hierarchical ID: <CODE>-<story>.<criterion>.
- Criteria use EARS phrasing:
    WHEN <event/condition> THE SYSTEM SHALL <behavior>          (event-driven)
    WHILE <state> THE SYSTEM SHALL <behavior>                   (state-driven)
    IF <unwanted condition> THEN THE SYSTEM SHALL <behavior>    (unwanted behavior)
    WHERE <feature is included> THE SYSTEM SHALL <behavior>     (optional feature)
    THE SYSTEM SHALL <behavior>                                 (ubiquitous)
- Guard requirements protect existing behavior this feature touches:
    WHEN <condition> THE SYSTEM SHALL CONTINUE TO <existing behavior>
- IDs are immutable once Status is Approved. Retire a requirement by striking it
  through (~~**CODE-N.M**~~ reason) — never renumber.
-->

After a review-product-flow run file and HTML exist, the same authoring agent
still rubber-stamps its own coverage self-check. Dogfood then invents the test
plan mid-run when real shipped surfaces were never cased. This feature adds an
**isolated judgment skill** that maps the **implemented** user-observable surface
against the guide, produces a greppable findings report, hard-gates walkthrough
drive until the guide is clean (or the user names remaining findings), and keeps
guide-gap repair separate from product-defect isolation during dogfood.

## 1. Isolated skill and report artifact

**Story:** As an agent holding a finished review-product-flow guide, I want to
invoke a dedicated model-invoked skill that reviews the guide in a fresh
context and leaves a report on disk, so that completeness judgment is not the
same session that authored the cases.

- **VPF-1.1** THE SYSTEM SHALL provide a model-invoked skill named `vet-product-flow` at `skills/acceptance/vet-product-flow/SKILL.md`.
- **VPF-1.2** WHEN `vet-product-flow` runs THE SYSTEM SHALL perform the judgment pass in a **fresh isolated** context (read-only subagent, or sequential axis-close inline fallback when subagents are unavailable), never as a longer same-session self-check after authoring.
- **VPF-1.3** WHEN `vet-product-flow` completes a pass THE SYSTEM SHALL write `.skills/<slug>-vet-product-flow.md` holding: open findings (each with stable id, severity, missing-situation statement, evidence pointers), zero-open vs open summary, and a **re-check stamp** (when the pass ran and against which run-file path/identity).
- **VPF-1.4** THE SYSTEM SHALL identify findings as `VPF-N` (integer N), reusing the same id across re-checks when the same surface miss persists.
- **VPF-1.5** WHILE `vet-product-flow` is running THE SYSTEM SHALL leave the product codebase and the run file unmodified (read-only judgment — no product patches, no case writes, no self-stamped “clean” without a report).

## 2. Implementation-surface map (product claim)

**Story:** As a reviewer of a product-flow guide, I want missing-situation
findings only where the shipped product already exposes a user-observable
path or state that the guide never exercises, so that dogfood is not writing
the known-from-implementation test plan mid-run.

- **VPF-2.1** WHEN `vet-product-flow` judges guide sufficiency THE SYSTEM SHALL map **user-observable** shipped paths and states (routes, primary actions, empty/error/role UI the code actually renders, and other UI-exposed states) against cases in the run file — not every internal branch, helper, or service conditional.
- **VPF-2.2** WHEN the shipped product exposes a user-observable path or state and the run file has no corresponding case (including non-happy paths real use can hit on that surface) THE SYSTEM SHALL emit a **missing-situation** finding.
- **VPF-2.3** WHEN a missing-situation finding asserts that implementation already does X THE SYSTEM SHALL require evidence the reviewer actually opened: file/symbol/route/state pointer into **real code** (and/or the triad when the claim is spec / Out-of-Scope / persist) — never guide+spec prose alone for an implementation claim.
- **VPF-2.4** IF code for a candidate surface was not inspected THEN THE SYSTEM SHALL NOT assert that surface as a missing-situation finding.
- **VPF-2.5** WHEN emitting findings THE SYSTEM SHALL assign a severity label (`Critical` / `Important` / `Minor`) used only to **order the fix loop** and communicate blast — severity SHALL NOT clear or soften the dogfood gate by default.
- **VPF-2.6** THE SYSTEM SHALL treat authoring §1 hygiene rules (requirement-ID coverage, non-happy kinds, exceptions) as necessary but **not** this skill’s product claim; mechanical schema/kind/status passes SHALL NOT be named or sold as “guide complete for real users.”

## 3. Explicit non-claims (refuse)

**Story:** As a stakeholder reading a vet report, I want the skill to refuse
claims that belong to dogfood or product design, so that a green report never
means “good UX” or “shipped.”

- **VPF-3.1** THE SYSTEM SHALL NOT claim true novelty at runtime, feel, or visual-polish taste as pass/fail outcomes of `vet-product-flow`.
- **VPF-3.2** THE SYSTEM SHALL NOT require or invent chaos, load, race, or security-fuzz suites in the guide or the report.
- **VPF-3.3** IF a candidate is “users will want X” or “the product should do X” and X is not already on the shipped user-observable surface THEN THE SYSTEM SHALL NOT emit it as a missing-situation finding.
- **VPF-3.4** THE SYSTEM SHALL NOT stamp global outcomes such as “good UX”, “complete for real users”, or “ready to ship” in the report or skill prose.
- **VPF-3.5** THE SYSTEM SHALL NOT replace dogfood: no drive-app pass/fail ownership, no FE+BE evidence ownership inside `vet-product-flow`.

## 4. Author hand-off from review-product-flow

**Story:** As an agent finishing `review-product-flow`, I want a mandatory hand-off
into `vet-product-flow` after the run file and HTML exist, so that hand-over is
not “artifacts on disk, dogfood whenever.”

- **VPF-4.1** WHEN `review-product-flow` reaches hand-over with a run file and rendered HTML on disk THE SYSTEM SHALL name `vet-product-flow` as the next required step and invoke or instruct that skill before treating the guide as ready for agent dogfood.
- **VPF-4.2** (guard) WHEN `review-product-flow` authors cases THE SYSTEM SHALL CONTINUE TO apply its §1 coverage gate and seven-kind taxonomy; this feature adds a peer skill rather than removing authoring hygiene.
- **VPF-4.3** (guard) WHEN `review-product-flow` renders THE SYSTEM SHALL CONTINUE TO use the run file as SSOT and the checked-in shell render path (no craft-page default).

## 5. Hard gate before run-product-walkthrough drive

**Story:** As an agent about to drive product cases, I want walkthrough blocked
until a fresh clean vet report exists (or I name remaining findings in-thread),
so that mid-run plan writing is structurally prevented.

- **VPF-5.1** BEFORE `run-product-walkthrough` drives any product case THE SYSTEM SHALL require that `vet-product-flow` has been run and a **fresh** `.skills/<slug>-vet-product-flow.md` exists for that run file.
- **VPF-5.2** IF the fresh report has any open missing-situation finding and the user has not given an explicit in-thread yes that **names** each remaining open finding THEN THE SYSTEM SHALL NOT drive product cases.
- **VPF-5.3** WHEN the user overrides with an explicit in-thread yes THE SYSTEM SHALL require that the yes names the remaining open findings (greppable trail; no silent skip; no bare “just go”).
- **VPF-5.4** THE SYSTEM SHALL treat every open code-grounded missing-situation finding as **blocking** for drive until fixed or named-overridden — severity labels SHALL NOT reintroduce a hard-only-on-Critical gate.
- **VPF-5.5** (guard) WHEN `run-product-walkthrough` checks origin THE SYSTEM SHALL CONTINUE TO require local default or explicit non-local consent naming that origin before any product click.
- **VPF-5.6** (guard) WHEN `run-product-walkthrough` marks `pass` THE SYSTEM SHALL CONTINUE TO require non-empty `--saw` and `--server` evidence per the Iron Law (including the `presentational` sentinel rules).

## 6. Guide-gap fix and re-check loop

**Story:** As a controller holding open vet findings, I want a prescribed
artifact-only fix loop with mandatory fresh re-judgment and a circuit breaker,
so that gaps close without same-agent self-clear or endless taste thrash.

- **VPF-6.1** WHILE open missing-situation findings remain and no named override is on record THE SYSTEM SHALL keep `run-product-walkthrough` from driving product cases.
- **VPF-6.2** WHEN applying guide-gap fixes THE SYSTEM SHALL order work by severity labels, patch **only** the run file (add/reshape cases/sections/slots) and re-render HTML — not product code, not mid-drive invent-cases.
- **VPF-6.3** AFTER run-file patches for guide gaps THE SYSTEM SHALL re-invoke `vet-product-flow` in a **fresh isolated** pass; the dogfood gate SHALL re-evaluate only against the new report.
- **VPF-6.4** THE SYSTEM SHALL clear a finding only when the new report no longer carries it, or when the user names it in an explicit override — never by self-declaration without a new report.
- **VPF-6.5** IF open finding count is ≥ 5 OR the required rewrite spans ≥ 2 ability areas THEN THE SYSTEM SHALL dispatch an **isolated fixer subagent** whose brief is the finding set + run-file path (+ evidence pointers), not full session history; then re-run fresh `vet-product-flow`.
- **VPF-6.6** IF 2 full re-judgment cycles complete with open findings still present THEN THE SYSTEM SHALL stop for the human (fix more, named override listing remaining findings, or shrink surface) rather than thrashing.
- **VPF-6.7** IF an item is non-code-grounded, taste, or outside the skill claim THEN THE SYSTEM SHALL NOT keep the fix loop alive on that item as if it were a missing-situation finding.

## 7. Product-defect isolation during dogfood (separate loop)

**Story:** As a controller mid-walkthrough, I want product defects debugged in a
subagent while I own re-test, so that long dogfood context stays clean and
root-cause still applies.

- **VPF-7.1** WHEN a case fails during `run-product-walkthrough` for a deterministic product defect THE SYSTEM SHALL keep **master (controller)** ownership of case selection, evidence slots, `mark` pass/fail/blocked, and **re-test** after a fix.
- **VPF-7.2** WHEN isolated debug/fix work is needed for a product defect THE SYSTEM SHALL dispatch a **subagent** with a red-capable brief (repro, saw/server, case id, req) — not the whole session history.
- **VPF-7.3** WHEN that subagent reports DONE THE SYSTEM SHALL return control to the master, which SHALL re-drive the failed case and SHALL CONTINUE TO re-drive already-`pass` cases whose `req` the product fix touched (existing walkthrough re-drive rules).
- **VPF-7.4** WHILE product-defect work runs in a subagent THE SYSTEM SHALL still route deterministic product defects through **`root-cause`** (and test-first) inside that isolated work — context isolation is not a free pass to patch without root-cause.
- **VPF-7.5** THE SYSTEM SHALL keep the guide-gap fix loop (story 6) and the product-defect dogfood loop (this story) separate — guide gaps edit the run file and re-vet; product defects do not absorb missing-situation findings.

## 8. Quality attributes

**Section-kind:** nfr

**Story:** As a stakeholder, I want measurable quality targets for this feature, so that how-well is not left implicit.

- **Performance:** None — skill is agent-orchestrated judgment over files; no latency budget for end users.
- **Security:** None — no new network surface, secrets path, or auth boundary (read-only file/code inspection).
- **Reliability:** **VPF-8.1** WHEN a re-check pass runs against the same run file and an unchanged surface miss still holds THE SYSTEM SHALL reuse the prior finding id `VPF-N` for that miss — verified by scenario tests that assert id stability across two fixture reports.
- **Accessibility:** None — no new end-user UI; the human guide remains owned by `review-product-flow` render/serve.

## Files touched (guard inventory)

| File | Existing behavior at risk | Guards |
|---|---|---|
| `skills/acceptance/review-product-flow/SKILL.md` | §1 coverage gate; taxonomy; run file + render hand-over | VPF-4.2, VPF-4.3 |
| `skills/acceptance/run-product-walkthrough/SKILL.md` | Iron Law evidence; origin consent; failure routing; re-drive after fix | VPF-5.5, VPF-5.6, VPF-7.3 |
| `skills/acceptance/vet-product-flow/SKILL.md` | new file | n/a |
| `docs/specs/INDEX.md` | feature registry row | no behavior to guard |
| `AGENTS.md` / package indexes / human guides | inventory listings | no behavior to guard |
| `CONTEXT.md` | glossary terms if added | no behavior to guard |
| `tests/trigger/*`, scenario markdown | routing tests | no behavior to guard |

## Out of Scope

- **CLI-first “completeness” pass** as the product claim (schema/kind/status counts may exist later only as optional hygiene — never marketed as guide-complete-for-real-users).
- **Same-agent §4 self-check** as a substitute for isolated judgment.
- **Spec-only review** (requirements without reading shipped UI code) as the primary depth.
- **Full adversarial speculative critique** (“users will want…”) and capped optional speculative noise rows as gate material.
- **Driving the app / FE+BE evidence / feel / true novelty** — remains `run-product-walkthrough`.
- **Promoting guide cases into committed e2e** — remains `validate-ui` when the user asks.
- **Rewriting `audit-trace`** or merging this skill into `inspect-change`.
- **Automatic product code changes** by `vet-product-flow` itself.

## Open Questions

- None — frame-change locks closed 2026-08-01.
