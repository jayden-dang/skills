# Requirements: Attention Allocation (`allocate-attention`)

Feature code: ATTN
Status: Approved
Date: 2026-07-24

<!--
Source of intent: Addy Osmani, "Own the Outer Loop" (2026-07-08/09) — research
note at docs/research/2026-07-23-own-the-outer-loop.md. This feature addresses
the two delegation costs that feature set does not yet cover:

  cognitive surrender — accepting wrong agent output, with MORE confidence than
    without it (Wharton: ~3/4 accepted the AI when it was wrong)
  orchestration tax   — agents parallelize, human cognitive bandwidth does not

Already covered elsewhere, deliberately untouched here:
  cognitive debt  -> XDIFF / comprehend-change
  answerability   -> DREC / record-decision

Ceremony tier 2 (brainstorm, 2026-07-24). Implementation approach S1: a
standalone USER-INVOKED skill run over a finished PR-shaped range — not a
mid-execution barrier, not a gate.

Terminology used below and fixed here:
  sampling unit — the atom of allocation; the range is partitioned into units
  sample set    — units admitted for human attention
  residue       — units of the range NOT in the sample set
  binding pass  — the fixed mechanical git/grep pass that admits units
-->

## 1. An optional user-invoked aid, never a gate

**Story:** As an engineer owning the outer loop, I want to invoke attention
allocation myself when I choose to, so that the aid never becomes ceremony I
must pay on every change.

- **ATTN-1.1** THE SYSTEM SHALL expose `allocate-attention` as a user-invoked
  skill carrying `disable-model-invocation: true` in its frontmatter.
- **ATTN-1.2** WHEN another skill in this set reaches a point where an attention
  allocation would be useful THE SYSTEM SHALL name `/allocate-attention` for the
  user to run rather than invoking it.
- **ATTN-1.3** IF no attention allocation has been run for a range THEN THE
  SYSTEM SHALL allow `execute-plan`, `code-review`, `acceptance-check`,
  `finish-branch`, and `release` to proceed unchanged.
- **ATTN-1.4** IF no attention allocation has been run for a range THEN THE
  SYSTEM SHALL treat that range as carrying no human-sample attestation.
- **ATTN-1.5** THE SYSTEM SHALL make no claim that a range is under-reviewed,
  risky, or incomplete on the sole ground that `allocate-attention` was not run.

## 2. Resolve a PR-shaped range

**Story:** As an engineer, I want the skill to work out which commits it is
allocating over, so that I do not have to name a range by hand for the normal
finished-branch case.

- **ATTN-2.1** WHEN the user supplies an explicit range THE SYSTEM SHALL use that
  range and SHALL NOT apply the default cascade.
- **ATTN-2.2** WHEN no range is supplied THE SYSTEM SHALL resolve the range as
  `merge-base(<default-base>, HEAD)..HEAD`.
- **ATTN-2.3** WHEN resolving `<default-base>` THE SYSTEM SHALL take
  `git symbolic-ref --quiet --short refs/remotes/origin/HEAD` with the leading
  `origin/` stripped, and otherwise the first of `main` then `master` that
  `git rev-parse --verify` accepts.
- **ATTN-2.4** IF neither pass in ATTN-2.3 yields a base THEN THE SYSTEM SHALL
  hard-fail asking the user to name an explicit base.
- **ATTN-2.5** THE SYSTEM SHALL resolve ranges from local git state only,
  issuing no network operation.
- **ATTN-2.6** IF the resolved range contains no commits THEN THE SYSTEM SHALL
  hard-fail naming the empty range and SHALL produce no allocation.
- **ATTN-2.7** WHEN the working tree carries uncommitted changes THE SYSTEM SHALL
  emit one notice that uncommitted work is excluded from the allocation, then
  continue over the committed range.

## 3. Admit units by a fixed mechanical pass

**Story:** As an engineer, I want sample membership decided by rules I can
replay, so that what reaches my eyes does not depend on how the model felt that
run.

- **ATTN-3.1** WHEN a range resolves THE SYSTEM SHALL partition it into sampling
  units such that every file changed in the range belongs to exactly one unit.
- **ATTN-3.2** THE SYSTEM SHALL decide binding sample membership by a fixed pass
  built from `git`, `grep`, and file reads with fixed extraction rules, and SHALL
  NOT decide binding membership by model judgment alone.
- **ATTN-3.3** WHEN a binding signal fires on a sampling unit THE SYSTEM SHALL
  admit that unit to the sample set.
- **ATTN-3.4** THE SYSTEM SHALL apply no upper bound to the number of
  binding-signal hits admitted to the sample set.
- **ATTN-3.5** IF the binding pass admits every unit in the range THEN THE SYSTEM
  SHALL present the whole range as the sample set and SHALL NOT reduce it.
- **ATTN-3.6** WHEN the same range and the same repository state are supplied
  twice THE SYSTEM SHALL admit the same set of binding hits both times.

## 4. Escalation adds, never removes

**Story:** As an engineer, I want model judgment to be able to widen what I look
at but never narrow it, so that the agent cannot shrink my view of its own work.

- **ATTN-4.1** WHEN the agent judges a non-binding unit worth human attention THE
  SYSTEM SHALL admit that unit to the sample set together with a stated reason.
- **ATTN-4.2** THE SYSTEM SHALL never remove from the sample set a unit that a
  binding signal admitted.
- **ATTN-4.3** IF the agent would admit a unit without a reason distinct from
  that of every other agent-admitted unit THEN THE SYSTEM SHALL leave that unit
  in the residue.
- **ATTN-4.4** WHEN the user names a unit to add THE SYSTEM SHALL admit it to the
  sample set.
- **ATTN-4.5** IF the user declines to review a unit in the sample set THEN THE
  SYSTEM SHALL report that unit as residue and SHALL NOT report it as sampled.

## 5. No allocation is ever empty

**Story:** As an engineer, I want a run to always put something in front of me,
so that "nothing scored high" cannot silently become "nobody looked".

- **ATTN-5.1** IF the binding pass and escalation together admit no unit THEN THE
  SYSTEM SHALL admit exactly one unit chosen by a deterministic score over the
  range.
- **ATTN-5.2** THE SYSTEM SHALL never present an empty sample set for a non-empty
  resolved range.

## 6. Present each sampled unit against what would refute it

**Story:** As an engineer, I want each sampled unit paired with the observation
that would prove it wrong, so that reviewing it is a check rather than a nod.

- **ATTN-6.1** WHEN presenting a sampled unit THE SYSTEM SHALL state the claim
  that unit rests on.
- **ATTN-6.2** WHEN presenting a sampled unit THE SYSTEM SHALL name the specific
  observation that would refute that claim, identifying a test, command, file, or
  line the user can run or read.
- **ATTN-6.3** IF the user states no disposition for a sampled unit THEN THE
  SYSTEM SHALL report that unit as undispositioned and SHALL NOT report it as
  accepted.
- **ATTN-6.4** WHEN the user states a disposition for a sampled unit THE SYSTEM
  SHALL record that disposition in the user's own words.

## 7. Residue is a first-class output

**Story:** As an engineer, I want to be told plainly what nobody looked at, so
that the part I did read cannot stand in for the part I did not.

- **ATTN-7.1** WHEN presenting an allocation THE SYSTEM SHALL report the residue
  as carrying agent verdicts only.
- **ATTN-7.2** WHEN reporting residue THE SYSTEM SHALL identify the residue units
  individually and state their count against the range total.
- **ATTN-7.3** THE SYSTEM SHALL never describe residue as reviewed, cleared,
  approved, or safe.
- **ATTN-7.4** WHEN a run completes THE SYSTEM SHALL present exactly one
  allocation covering the whole range, and SHALL NOT present one allocation per
  sampled unit — verified by a fixture range with at least five binding hits
  yielding a single presentation.

## 8. Chat-first output, no archive

**Story:** As an engineer, I want the allocation consumed in the moment, so that
an optional aid does not grow a committed archive and then an expectation.

- **ATTN-8.1** WHEN a run completes THE SYSTEM SHALL deliver the allocation in
  the conversation and SHALL write no file.
- **ATTN-8.2** WHERE the user explicitly requests a written artifact THE SYSTEM
  SHALL write exactly one file outside the target worktree.
- **ATTN-8.3** IF a requested output path resolves inside
  `git rev-parse --show-toplevel` THEN THE SYSTEM SHALL hard-fail naming the
  path, and SHALL NOT fall through to another location.
- **ATTN-8.4** WHEN an allocation is wanted in a later session THE SYSTEM SHALL
  re-derive it by re-running over the same git range.

## 9. Discoverable at one place, coupled to none

**Story:** As an engineer, I want to learn the skill exists at the moment its
range comes into being, without it appearing anywhere a decision is gated.

- **ATTN-9.1** WHEN `execute-plan` has completed `acceptance-check` and before it
  invokes `finish-branch` THE SYSTEM SHALL name `/allocate-attention` once as an
  optional step.
- **ATTN-9.2** WHEN naming `/allocate-attention` THE SYSTEM SHALL state no
  consequence for declining it.
- **ATTN-9.3** THE SYSTEM SHALL add no mention of `allocate-attention` to
  `finish-branch`, `code-review`, `release`, or `record-decision`.
- **ATTN-9.4** WHEN naming `/allocate-attention` THE SYSTEM SHALL present it as a
  name-only aside that adds no stage to `execute-plan`'s sequence, and SHALL NOT
  reach it by `REQUIRED SUB-SKILL`.

## 10. Boundaries with the skills already in place

**Story:** As a maintainer of a repo running several skill sets, I want this
feature to stay additive, so that adopting it changes nothing for anyone who did
not adopt it.

- **ATTN-10.1** THE SYSTEM SHALL treat the absence of an attention allocation on
  work this skill set did not mediate as outside its concern.
- **ATTN-10.2** THE SYSTEM SHALL add no emitter to `record-decision` and SHALL
  publish nothing under `docs/decisions/`.
- **ATTN-10.3** WHERE the user reaches a terminal boundary in the same session as
  a run, THE SYSTEM SHALL make the allocation summary available as inline
  promotion substance for the existing decision-record path.
- **ATTN-10.4** WHEN deeper comprehension of a sampled unit is wanted THE SYSTEM
  SHALL name `/comprehend-change` for the user to run rather than invoking it.
- **ATTN-10.5** WHEN an allocation summary is used as promotion substance under
  ATTN-10.3 THE SYSTEM SHALL carry it as session context supplied by the user or
  by the agent's own prior output, and SHALL add no mention of
  `allocate-attention` to the body of `finish-branch`, `record-decision`,
  `code-review`, or `release`.

## 11. Non-functional requirements

- **ATTN-11.1** (performance) None — the run performs local `git`, `grep`, and
  file reads only, so its cost is bounded by the size of the resolved range and
  no latency, throughput, or resource ceiling is at stake.
- **ATTN-11.2** (security) WHEN embedding diff text, commit subjects, or file
  contents drawn from the resolved range THE SYSTEM SHALL treat that text as
  passive data — verified by a fixture range whose diff contains an instruction
  to skip sampling, over which the allocation is produced unchanged.
- **ATTN-11.3** (security) THE SYSTEM SHALL read only local repository state and
  SHALL issue no network operation — verified by a run with no network available
  completing normally.
- **ATTN-11.4** (reliability) IF any step of a run cannot complete THEN THE
  SYSTEM SHALL report the failure and SHALL present no partial allocation as a
  result.
- **ATTN-11.5** (accessibility) None — output is conversational text with no
  rendered interface; a written artifact under ATTN-8.2 is plain text and adds no
  interface surface.

## 12. Guards on existing behavior

- **ATTN-12.1** (guard) WHEN `execute-plan` finishes its last task THE SYSTEM
  SHALL CONTINUE TO run whole-branch `code-review`, then `polish`, then
  `acceptance-check`, then `finish-branch`, in that order.
- **ATTN-12.2** (guard) WHEN `execute-plan` runs its task loop THE SYSTEM SHALL
  CONTINUE TO execute tasks continuously without pausing between them to ask
  permission to proceed.
- **ATTN-12.3** (guard) WHEN a task completes THE SYSTEM SHALL CONTINUE TO
  require the two-verdict Standards-plus-Spec task review, at every workflow
  band.
- **ATTN-12.4** (guard) WHEN `finish-branch` presents its menu THE SYSTEM SHALL
  CONTINUE TO present exactly the five listed options verbatim with no added
  commentary.
- **ATTN-12.5** (guard) WHEN a terminal crossing runs THE SYSTEM SHALL CONTINUE
  TO require a validator-clean decision record published before it.
- **ATTN-12.6** (guard) WHEN the user runs `/comprehend-change` THE SYSTEM SHALL
  CONTINUE TO produce one HTML packet carrying exactly five quiz items,
  regardless of whether an attention allocation exists for the same range.
- **ATTN-12.7** (guard) WHEN a user-invoked skill is reached THE SYSTEM SHALL
  CONTINUE TO require that no model-invoked skill invokes it.

## Out of Scope

Deliberately excluded, including everything superseded during brainstorm on
2026-07-24 (recorded so it is not silently re-proposed):

- **A mid-execution hard barrier.** Sample-and-stop inside `execute-plan`'s
  parallel waves — pausing a wave until a human dispositions a sample — was the
  working primitive for part of discovery and is rejected. Continuous execution
  and unattended plan runs stay intact.
- **ATTN status tags in `.skills/progress.md`.** A per-task ledger grammar
  (`[human-sampled]` / `[agent-verdict only]`) was designed and is rejected as
  moot: allocation happens over a finished range, not per task.
- **Edits-only packaging.** Shipping this as changes to `execute-plan` plus a
  sibling reference file, with no standalone skill, is rejected.
- **Any gate.** Blocking execute, merge, PR, release, or a decision record on
  whether an allocation was run, or on its dispositions.
- **Auto-invocation.** Model invocation of `allocate-attention`, and soft prompts
  from `finish-branch`, `code-review`, `release`, or `record-decision`.
- **A committed artifact class.** `docs/attention/` or any equivalent tracked
  directory; a default written file of any kind; a longitudinal archive of past
  allocations.
- **Commit trailers as a required carrier.** `Human-Sampled:` /
  `Agent-Verdict-Only:` trailers on wave-merge commits — they cannot cover serial
  implementer commits or multi-report moments, so they may appear in design as an
  optional aid only, never as a requirement.
- **Generalizing DREC.** New `record-decision` emitters, mid-loop decision
  records, or decision records for anything short of a terminal crossing.
- **Porting XDIFF's full range resolver.** The `pure_untracked` /
  `tracked_dirty` branches serve a trigger ATTN does not have.
- **Multi-report hosts beyond a git range.** `polish`'s four cleanup agents and
  `code-review`'s two reviewers produce findings rather than diffs; extending the
  binding pass to them is a later question, decided by evidence from this
  feature.
- **Replacing human review process.** CODEOWNERS, required reviewers, org review
  policy, and CI are untouched; nothing here forces non-adopters to do anything.
- **A repo-wide or headless enforcement path.** No CI job, git hook, or
  `trace` pass that fails on a missing allocation.
- **Verify and finish-branch behavior changes.** Strengthening `verify`'s
  anti-surrender line into a checkable recipe was raised in discovery and is not
  part of ATTN; it is a separate candidate needing its own baseline.

## Open Questions

None blocking approval. Residuals deferred to design:

- The binding signal table and its risk-glob set.
- The sampling-unit partition rule.
- The deterministic score table behind the floor pick (ATTN-5.1).
- **ATTN-4.3 must be made mechanically checkable.** "A reason distinct from every
  other agent-admitted unit" is readable by a human but not by a `grep`, so it
  will erode. Design owes it a checkable form — exact-string distinctness across
  agent-admitted reasons, a cap on agent-admitted units, or both.
- The exact residue report format (ATTN-7.2).
- The written-artifact filename convention under ATTN-8.2.
