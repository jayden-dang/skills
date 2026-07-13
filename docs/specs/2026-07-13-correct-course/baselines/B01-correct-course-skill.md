# B01 — correct-course skill

Baseline for Task 1: authoring `skills/track/correct-course/SKILL.md`. Each scenario is
walked by hand against the authored skill body (this repo verifies skills by baseline
scenario, not an automated harness — see Global Constraints). RED = walked before the
skill file existed (nothing to walk, scenario fails by definition); GREEN = walked after
authoring, confirmed to hold.

## S1 — Skill identity

The file is model-invoked (carries no `disable-model-invocation` line), lives at
`skills/track/correct-course/SKILL.md`, and its frontmatter `description` is valid YAML
containing no unquoted colon-space (`": "`).

**Walk:** Open the frontmatter block. Confirm only `name` and `description` keys are
present (no `disable-model-invocation`). Confirm the file path. Run
`scripts/lint-skill-frontmatter.py skills/track/correct-course/SKILL.md` and confirm it
exits clean.

`[CCOURSE-1.3] [CCOURSE-7.3]`

## S2 — Diagnose gate

Given a mid-execution discovery that invalidates the approved plan, Phase 1 authors a
notice with five labelled parts — What, Where, Why, How (+ impact), and other context —
presents it, and hard-stops for the user's explicit go/no-go before any classification or
artifact touch. If the user declines (no-go), the skill makes no spec or code change and
returns control without a rewind — a clean no-op.

**Walk:** Read Phase 1. Confirm all five labelled parts are named. Confirm the step's
**Done when:** is "the user has ruled go or no-go," gating everything after it. Confirm
the no-go branch is stated as a clean no-op with no artifact touched.

`[CCOURSE-2.1] [CCOURSE-2.2] [CCOURSE-2.3]`

## S3 — Classify

Only after the diagnosis go-ahead, Phase 2 names the lowest invalidated artifact — one of
Task-local / Plan / Design / Requirements / Vision — with cited evidence, and never picks
a higher level "to be safe" without evidence for that higher level. It then presents an
ephemeral change proposal (chosen level, evidence, proposed re-entry) and stops for the
user's approval; the proposal is never written to disk.

**Walk:** Read Phase 2. Confirm the inline 5-level table is present and matches the
design's table. Confirm the classification law ("pick the lowest level with evidence;
rewinding higher without evidence is prohibited") is stated prominently. Confirm the
proposal-then-stop step names its **Done when:** as user approval. Confirm an explicit
line states the proposal is ephemeral / never a standalone artifact.

`[CCOURSE-3.1] [CCOURSE-3.2] [CCOURSE-3.3] [CCOURSE-3.4]`

## S4 — Idempotency

A divergence that would re-classify the same already-acted-on evidence to the same
lowest invalidated artifact, with no new evidence, halts and escalates to the user
instead of re-entering that level — breaking the
`execute-plan → correct-course → write-* → sync-spec → execute-plan` loop. A genuinely
new discovery is recorded to the ledger (evidence fingerprint, chosen level, outcome) and
classification proceeds normally.

**Walk:** Read the Idempotency section. Confirm it names the ledger path
`.skills/corrections.md`, describes it as ephemeral/git-ignored/scoped to the in-flight
plan, and states the one-line-per-correction format (fingerprint + level + outcome).
Confirm the "read ledger before classifying" step and the same-evidence/same-level →
halt-and-escalate rule are both present.

`[CCOURSE-3.5] [CCOURSE-3.6]`

## S5 — Routing

Each of the five classification levels routes to its correct re-entry skill, invoked
directly (never merely suggested to the user) and left to run its own approval gate;
Vision with no `docs/product/vision.md` escalates to a human instead of silently
dropping the concern.

**Walk:** Read Phase 3. Confirm each row: Task-local → `execute-plan`/`tdd` with no
upstream rewind; Plan → `write-plan`; Design → `write-design` flowing into `write-plan`;
Requirements → `write-requirements` flowing into design and plan; Vision → the vision
layer WHERE `docs/product/vision.md` exists, ELSE escalate to a human and re-enter
`brainstorm` only on user agreement. Confirm a closing line states invoking the sub-skill
directly and deferring to its own gate is the rule for all five.

`[CCOURSE-4.1] [CCOURSE-4.2] [CCOURSE-4.3] [CCOURSE-4.4] [CCOURSE-4.5] [CCOURSE-4.6]`

## S6 — Thin-router exit

`correct-course` writes no spec files itself: all content generation delegates to
`write-*`, all triad reconciliation delegates to `sync-spec`. After the re-entry skill's
gate passes, it reconciles via `sync-spec` when approved artifacts or trace links
changed, records an ADR via `domain-modeling` only when the change carries an
architectural consequence (never for Task-local/Plan, never for an unapproved proposal),
and returns control to `execute-plan` — re-baselining the `.skills/progress.md` ledger
first when the rewind rewrote `tasks.md`.

**Walk:** Read the Thin-router exit section. Confirm the "never rewrite
requirements/design/plan/tasks/trace" line. Confirm Reconcile/Record/Resume are each
present with their conditions: reconcile is conditional on changed approved
artifacts/trace; ADR is conditional on architectural consequence, excluded for
Task-local/Plan, and never persisted without approval; resume states
`execute-plan` auto-resumes and the ledger is re-baselined (kept vs. dropped entries) on
a `tasks.md` rewrite, untouched for Task-local.

`[CCOURSE-5.1] [CCOURSE-5.2] [CCOURSE-5.3] [CCOURSE-5.4] [CCOURSE-5.5]`

## S7 — Boundaries

The `## Red Flags` block correctly sends a post-ship in-scope tweak to `amend`, broken
code against a still-valid spec to `debug`, and treats `sync-spec` as one of
correct-course's exits — the mechanical reconciler that runs after the decision — never
the maker of the decision.

**Walk:** Read the Red Flags block. Confirm the `amend` line, the `debug` line, and the
`sync-spec` line are each present with the stated distinction. Confirm a
`| Thought | Reality |` rationalization row is present (e.g. over-rewinding "to be safe").

`[CCOURSE-6.1] [CCOURSE-6.2]`

## Coverage self-check

Every one of Task 1's 24 IDs appears in at least one tag above: 1.3, 2.1, 2.2, 2.3, 3.1,
3.2, 3.3, 3.4, 3.5, 3.6, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 5.1, 5.2, 5.3, 5.4, 5.5, 6.1, 6.2,
7.3 — 24 of 24, none missing, none double-defined.
