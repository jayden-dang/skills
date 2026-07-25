# Requirements: Roadmap layer

Feature code: RMAP
Status: Implemented
Date: 2026-07-25

Adds the program band between `docs/product/vision.md` and a single feature's
`requirements.md`: a durable home for milestone intent (`write-roadmap`) and a
read-only derivation of roadmap health (`check-roadmap`).

**Namespaces this feature introduces or consumes.** `GOAL-N` — product outcomes in
`vision.md`. `MILE-N` — milestones. `ROAD-N` — roadmap items that exist before any
feature spec. Feature codes (`CODE`) and requirement IDs (`CODE-N.M`) stay owned by
`write-requirements`; architecture IDs (`ARCH-N`) stay owned by `establish-project`.

**Ownership split.** `docs/roadmap/INDEX.md` owns planning intent: outcomes, ordering,
membership, dependencies, commitments, blockers, deferrals, goal dispositions. Existing
specs, git history, test evidence, and `trace` own implementation truth. Feature progress
is recorded once — as `Status:` in each feature's `requirements.md`, mirrored into its
`docs/specs/INDEX.md` row — and is derived per run, never copied into the roadmap.

## 1. Author and maintain roadmap intent

**Story:** As a developer starting or replanning a multi-feature project, I want the
milestone decomposition written down with stable IDs and an explicit approval gate, so
that it outlives the conversation that produced it and later work can cite it.

- **RMAP-1.1** WHEN `write-roadmap` runs and `docs/roadmap/INDEX.md` does not exist THE SYSTEM SHALL create it from the roadmap template with every REQUIRED slot filled or written `None`.
- **RMAP-1.2** THE SYSTEM SHALL give every milestone a `MILE-N` ID, one testable outcome sentence, a member list, a `Depends-on` field, and a commitment state of `Planned`, `Committed`, or `Closed`.
- **RMAP-1.3** THE SYSTEM SHALL give every roadmap item a `ROAD-N` ID and a slug, and record it under exactly one milestone.
- **RMAP-1.4** THE SYSTEM SHALL identify a roadmap item by its `ROAD-N` ID and slug, leaving feature-code registration to `write-requirements`.
- ~~**RMAP-1.5**~~ retired 2026-07-25: no baseline failure. A fresh agent caught a forward dependency unprompted as its first finding. The structural check survives as S4 in the template rule block and as `check-roadmap` finding R11 — only the authoring-time rule is retired. Evidence: `tests/roadmap/red-baselines.md`.
- ~~**RMAP-1.6**~~ retired 2026-07-25: no baseline failure. Two independent baseline agents consolidated a surface repeated across milestones without prompting — one while reviewing, one while authoring. The `Surfaces:` slot that made the overlap visible is retained by RMAP-1.20. Evidence: `tests/roadmap/red-baselines.md`.
- **RMAP-1.7** WHEN a roadmap item leaves a milestone's membership THE SYSTEM SHALL record it under that milestone's `Deferred` slot with a date and a reason.
- **RMAP-1.8** WHERE `docs/product/vision.md` exists THE SYSTEM SHALL cite the goals each milestone serves by `GOAL-N` ID.
- **RMAP-1.9** WHERE `docs/product/vision.md` does not exist THE SYSTEM SHALL author the roadmap from the decomposition it was handed and record its goal citations as `None`.
- **RMAP-1.10** WHEN a milestone's commitment state becomes `Closed` THE SYSTEM SHALL record the closing release tag or commit in that milestone's `Closed` slot.
- **RMAP-1.11** WHILE `docs/roadmap/INDEX.md` exists THE SYSTEM SHALL keep every `MILE-N` and `ROAD-N` stable from first definition, retiring an ID by strikethrough with a reason.
- **RMAP-1.12** WHEN a `ROAD-N` moves to a different milestone THE SYSTEM SHALL keep its ID unchanged.
- **RMAP-1.13** THE SYSTEM SHALL expose `write-roadmap` as model-invocable, so `brainstorm` can reach it.
- **RMAP-1.14** (guard) WHEN `write-roadmap` runs THE SYSTEM SHALL CONTINUE TO leave `docs/specs/INDEX.md` unmodified.
- **RMAP-1.15** THE SYSTEM SHALL record a `Goal dispositions` section in `docs/roadmap/INDEX.md` in which every `GOAL-N` that is not struck through and not cited by any milestone appears as `GOAL-N → Deferred` or `GOAL-N → Out-of-scope`, each with a date and a reason.
- **RMAP-1.16** THE SYSTEM SHALL record a top-level `Status:` field in `docs/roadmap/INDEX.md` reading either `Draft` or `Approved`.
- **RMAP-1.17** WHEN the roadmap is otherwise complete THE SYSTEM SHALL present the whole file to the user and stop, setting `Status: Approved` only on explicit user approval.
- **RMAP-1.18** IF the roadmap carries a structural defect — a forward dependency, a duplicate or reused `MILE-N` or `ROAD-N`, a `ROAD-N` recorded under no milestone or several, a milestone missing its outcome sentence, or a `GOAL-N` neither cited nor dispositioned — THEN THE SYSTEM SHALL report the defect and withhold the RMAP-1.17 approval gate until it is resolved.
- **RMAP-1.19** WHEN `write-roadmap` applies a material change to a roadmap whose `Status:` is `Approved` — a change to any milestone's outcome, membership, ordering, commitment state, or goal citations — THE SYSTEM SHALL set `Status: Draft`, preserve every existing `MILE-N` and `ROAD-N`, and re-enter the RMAP-1.17 approval gate, which restores `Status: Approved` only on explicit user approval.
- **RMAP-1.20** THE SYSTEM SHALL give every roadmap item a `Surfaces:` slot naming the candidate components or paths it is expected to touch, or `None` with a reason.

## 2. Persist decomposition and bind roadmap items

**Story:** As a developer whose brainstorm just split work into several sub-features, I
want that split persisted and later bound to the specs that implement it, so that no
sub-feature is silently dropped and every spec can be traced to the plan that asked for
it.

- **RMAP-2.1** WHEN `brainstorm` decomposes work into two or more independent sub-features THE SYSTEM SHALL persist that decomposition through `write-roadmap` before the first sub-feature continues into `write-requirements`.
- **RMAP-2.2** WHEN a decomposition is persisted and `docs/roadmap/INDEX.md` already exists THE SYSTEM SHALL add the sub-features as new `ROAD-N` items in the existing roadmap.
- **RMAP-2.3** (guard) WHEN `brainstorm` shapes work confined to a single subsystem THE SYSTEM SHALL CONTINUE TO exit to `write-requirements` for tier ≥ 1 or to `tdd` for tier 0.
- **RMAP-2.4** WHEN `write-requirements` registers a feature code for work that implements a roadmap item THE SYSTEM SHALL record that item's `ROAD-N` in the feature's `Roadmap item` column in `docs/specs/INDEX.md`.
- **RMAP-2.5** WHERE `docs/roadmap/INDEX.md` does not exist THE SYSTEM SHALL leave the `Roadmap item` column empty and register the feature unchanged.
- **RMAP-2.6** (guard) WHEN a feature code is registered THE SYSTEM SHALL CONTINUE TO treat `write-requirements` Step 1 as its sole registrar, with the code unique repo-wide and the new row's status `Draft`.
- **RMAP-2.7** WHEN `establish-project` writes `docs/product/vision.md` THE SYSTEM SHALL give every goal a `GOAL-N` ID.
- **RMAP-2.8** WHEN `establish-project` updates a `docs/product/vision.md` whose goals carry no IDs THE SYSTEM SHALL assign `GOAL-N` IDs in document order and report the migration to the user.
- **RMAP-2.9** THE SYSTEM SHALL keep every `GOAL-N` already recorded in an approved `docs/product/vision.md` immutable across every later update, retiring a goal by strikethrough with a reason.
- **RMAP-2.10** (guard) WHEN `trace` runs THE SYSTEM SHALL CONTINUE TO check referential integrity for `CODE-N.M` and `ARCH-N` only.

## 3. Derive roadmap health and recommend the next action

**Story:** As a developer returning to a multi-milestone project, I want one read-only
report of where the plan and the specs disagree plus a single next action, so that I can
resume without trusting a status file that may have drifted.

- **RMAP-3.1** WHEN `check-roadmap` runs THE SYSTEM SHALL derive its report from `docs/roadmap/INDEX.md`, `docs/specs/INDEX.md`, each cited feature's `requirements.md`, `docs/product/vision.md`, `git`, and — where it exists — `.skills/progress.md`, writing no file.
- **RMAP-3.2** IF a milestone's goal citation does not resolve to exactly one live, non-struck-through `GOAL-N` in `docs/product/vision.md` THEN THE SYSTEM SHALL report a dangling goal citation.
- **RMAP-3.3** WHEN a `GOAL-N` that is not struck through is neither cited by a milestone nor recorded in the roadmap's `Goal dispositions` section THE SYSTEM SHALL report it as uncovered.
- **RMAP-3.4** IF a `ROAD-N` appears under more than one milestone THEN THE SYSTEM SHALL report duplicate membership.
- **RMAP-3.5** IF a `Roadmap item` binding in `docs/specs/INDEX.md` does not resolve to exactly one live, non-struck-through `ROAD-N` THEN THE SYSTEM SHALL report an unresolved binding.
- **RMAP-3.6** IF two feature codes bind to the same `ROAD-N` THEN THE SYSTEM SHALL report a conflicting binding.
- **RMAP-3.7** WHEN no feature code binds to a `ROAD-N` THE SYSTEM SHALL report that item as unspecced.
- **RMAP-3.8** WHERE `docs/roadmap/INDEX.md` exists THE SYSTEM SHALL report every feature row whose `Roadmap item` column is empty as unplanned.
- **RMAP-3.9** WHERE `docs/roadmap/INDEX.md` does not exist THE SYSTEM SHALL report the roadmap layer as absent and exit without findings.
- **RMAP-3.10** WHEN every check has run and no finding withholds a recommendation THE SYSTEM SHALL select exactly one next action through a single fixed priority ladder recorded in `design.md`, naming the skill to run and the `ROAD-N`, `MILE-N`, or feature code it applies to, so that identical artifact state yields the same recommendation.
- **RMAP-3.11** WHEN the user asks for a standup THE SYSTEM SHALL render the same derivation as a standup card naming the milestone currently in flight, the current status of that milestone's `ROAD-N` members, and the one next action.
- **RMAP-3.12** WHEN reporting how far a feature has progressed THE SYSTEM SHALL cite that feature's `Status:` and name `trace` for deeper coverage verification.
- **RMAP-3.13** THE SYSTEM SHALL expose `check-roadmap` as user-invoked, carrying `disable-model-invocation: true`.
- **RMAP-3.14** (guard) WHEN `check-roadmap` runs THE SYSTEM SHALL CONTINUE TO derive feature progress from the `Status:` recorded in each feature's `requirements.md` and mirrored in its `docs/specs/INDEX.md` row, creating no roadmap-level copy of that status.
- **RMAP-3.15** IF a milestone whose commitment state is `Closed` holds a non-deferred `ROAD-N` that no feature code binds, or one whose bound feature's `Status:` is not `Shipped`, THEN THE SYSTEM SHALL report premature closure and withhold the next-action recommendation.
- **RMAP-3.16** WHEN a finding withholds the next-action recommendation THE SYSTEM SHALL report the withholding reason in place of a next action.
- **RMAP-3.17** WHERE `.skills/progress.md` exists THE SYSTEM SHALL read it as local advisory evidence that never overrides a tracked `Status:`.
- **RMAP-3.18** WHERE `.skills/progress.md` does not exist THE SYSTEM SHALL proceed without reporting a finding about its absence.
- **RMAP-3.19** IF a feature's `requirements.md` `Status:` differs from the `Status` recorded in its `docs/specs/INDEX.md` row THEN THE SYSTEM SHALL report a status mismatch and withhold the next-action recommendation.
- **RMAP-3.20** IF `docs/product/vision.md` defines the same `GOAL-N` more than once THEN THE SYSTEM SHALL report a duplicate goal definition.

## 4. Quality attributes

**Story:** As a developer relying on this layer across a long-lived project, I want its
derivation bounded, its inputs untrusted, and its failures loud, so that the report stays
cheap to run and never invents a clean bill of health.

- **RMAP-4.1** WHEN `check-roadmap` runs THE SYSTEM SHALL complete its derivation with one full read of each source artifact and a bounded number of `git` commands independent of the number of features and milestones — verified by a scenario containing at least 200 features and 50 milestones.
- **RMAP-4.2** IF a value read from `docs/roadmap/INDEX.md`, `docs/specs/INDEX.md`, or `docs/product/vision.md` reaches a shell command THEN THE SYSTEM SHALL pass it as a single non-option argument and reject any value that does not match the expected ID or rev shape — verified by a scenario supplying an option-shaped and a metacharacter-bearing value.
- **RMAP-4.3** THE SYSTEM SHALL treat prose read from `docs/roadmap/INDEX.md`, `docs/specs/INDEX.md`, and `docs/product/vision.md` as passive data — verified by a scenario embedding an instruction in a milestone outcome and confirming it is reported, not obeyed.
- **RMAP-4.4** IF `docs/roadmap/INDEX.md` is unparseable, or carries any structural defect listed in RMAP-1.18, or holds a `Depends-on` that does not resolve to exactly one live, non-struck-through `MILE-N`, THEN THE SYSTEM SHALL report the defect and withhold the next-action recommendation — verified by a scenario over a fixture roadmap carrying each defect in turn.

**Accessibility: None** — this feature ships markdown skills and a markdown artifact, and
renders its reports as conversational markdown through the host harness. It introduces no
custom interactive, keyboard, or visual UI surface, and therefore adds no accessibility
conformance target of its own.

## Out of Scope

- **A separate `standup` skill.** Standup is a presentation mode of `check-roadmap`
  (RMAP-3.11). It splits out only if real usage reveals distinct team-ceremony
  responsibilities — cadence, attendance, per-person assignment.
- **Persisted run state.** `check-roadmap` writes no file (RMAP-3.1), so it holds no
  baseline of a previous run and reports current state only.
- **A milestone `retrospective` skill.** The seams it will consume are required here —
  the outcome sentence (RMAP-1.2), the deferral record (RMAP-1.7), the goal dispositions
  (RMAP-1.15), and the `Closed` marker that resolves a git range (RMAP-1.10) — but no
  retrospective ships in this feature.
- **Judging whether a milestone outcome was achieved.** `check-roadmap` catches
  structural status contradictions (RMAP-3.15); a future retrospective judges the
  outcome itself.
- **Treating attention residue as reviewed.** When a future retrospective consumes an
  allocation the user has already produced, it counts the sample as sampled and records
  the residue as unreviewed. `/allocate-attention` is user-invoked; a model-invoked
  retrospective may name it for the user to run, never invoke it.
- **A second action-item bucket.** The roadmap holds no action-item list. A future
  retrospective routes each finding by concern: a small in-scope change to a shipped
  feature → `amend`; an approved plan invalidated mid-flight → `correct-course`;
  milestone intent invalidated → a `write-roadmap` update under RMAP-1.19; a
  hard-to-reverse architecture decision → an ADR via `domain-modeling`; tracker work →
  `/file-issues` named for the user to run. `record-decision` is not a destination: its
  caller set is closed to `finish-branch` and `release` carrying a terminal verdict.
- **Any mutable progress or status file** of the `sprint-status.yaml` shape. Feature
  progress lives in `requirements.md` `Status:`, mirrored into the INDEX row (RMAP-3.14).
- **Extending `trace`** to `GOAL-N`, `MILE-N`, or `ROAD-N` referential integrity — those
  checks live in `check-roadmap` (RMAP-2.10).
- **Acceptance criteria on roadmap items.** A `ROAD-N` carries intent, not criteria;
  behavior criteria live in the feature's `requirements.md`.
- **Estimation, dates, capacity, velocity, and burndown.** The roadmap records ordering
  and commitment, not schedule.
- **Per-story context files, agent personas, and step-file DSLs** from the researched
  BMAD implementation.
