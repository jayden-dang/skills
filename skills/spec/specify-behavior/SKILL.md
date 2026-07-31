---
name: specify-behavior
description: Use when discovery is complete and a tier-1 or tier-2 change needs its
  requirements written — the user stories and EARS acceptance criteria in
  requirements.md that every later task, test, and commit cites by ID. After
  frame-change, before any design or code.
---

Produce `docs/specs/<YYYY-MM-DD>-<feature>/requirements.md` from the approved
frame-change outcome. Requirements are the durable source of intent: they outlive
this conversation, and every task, test, and commit will cite their IDs.

## Two modes — pick by what you were handed

**Tier-1 mini-spec** — a fix plus a guard for an **already-approved** feature
(you came from `amend-feature` or `root-cause`). You are not authoring a new
`requirements.md`. Append to the owning feature's `requirements.md` (or
`docs/specs/fixes.md` if no feature owns it):

- the **fix requirement** — one EARS criterion (Step 2's forms) for the
  corrected behavior;
- its **`SHALL CONTINUE TO` guard** — Step 3, for the behavior the fix must not
  break.

Then self-review just those two criteria: the ambiguity and testability scans,
plus the code-claim check (Step 5) only when a criterion asserts how the system
*currently* works — a guard usually does. Present the two appended criteria for
approval, keep the feature's `Status`, and exit to `test-first`. **Skip Steps 1 and 4
and the whole-file review** — a new feature code, an Out-of-Scope section, and a
full-file self-review are for a new feature, not a two-line mini-spec.

**New feature** — tier 2, or anything nothing has spec'd yet. Start from the skill
set's `templates/requirements.md` — resolve `templates/` as
`${CLAUDE_PLUGIN_ROOT}/templates` when installed as a plugin, otherwise
`../../../templates` relative to this SKILL.md. Every heading in that template is a
REQUIRED slot: fill it, or write `None` under it — never drop one. Then run the full
sequence below. Create a todo per step.

## Step 1: Register the feature code

Pick a short unique prefix (2–12 chars, A–Z0–9, starts with a letter — e.g.
`SHELL`, `SYNC2`). Check `docs/specs/INDEX.md`; add a row there BEFORE writing
requirements. Never reuse a retired code.

**Bind the roadmap item.** WHERE `docs/roadmap/INDEX.md` exists and this work implements one
of its items, record that item's `ROAD-N` in the row's **Roadmap item** column. WHERE there
is no roadmap, or the work was never planned as an item, write `—` and register the feature
otherwise unchanged. This column is the only link between plan and spec, and this step is
its only writer — a `ROAD-N` is never invented here, only cited.
**Done when:** the code has a row in INDEX.md with status Draft, and its Roadmap item cell
holds a `ROAD-N` or `—`.

## Step 2: Write stories and EARS criteria

One `## N. <title>` section per user story, each with acceptance criteria as
EARS statements carrying hierarchical IDs `**CODE-N.M**` — **N is the story
number** (same N as the `## N` heading). That identity is load-bearing: later
skills derive review units from it.

Each behavioral story carries:

```
**Story:** As a <actor>, I want <capability>, so that <benefit>.
```

The `**Story:**` line must name **one demoable act** a person can do or prove-claim
once the story lands — not a technical layer ("the storage layer is rewritten").

EARS forms:

- `WHEN <event> THE SYSTEM SHALL <behavior>` — event-driven
- `WHILE <state> THE SYSTEM SHALL <behavior>` — state-driven
- `IF <unwanted condition> THEN THE SYSTEM SHALL <behavior>` — error handling
- `WHERE <feature enabled> THE SYSTEM SHALL <behavior>` — optional features
- `THE SYSTEM SHALL <behavior>` — always-true invariants

One observable behavior per criterion. If a sentence needs "and", it is
usually two criteria. There is **no criteria-count cap** — size is visible later
from task file paths at plan/execute preflight, not from counting EARS lines.
**Done when:** every story has ≥1 criterion, every criterion has exactly one
WHEN/WHILE/IF/WHERE/ubiquitous form, and each `**Story:**` names one demoable act.

## Step 2b: Non-functional requirements (quality attributes)

Behavioral criteria (Step 2) say *what* the system does; non-functional
requirements (NFRs) say *how well* it must do it — and unstated quality
attributes are where features quietly fail. After the behavioral criteria, fill
the template's NFR section (pre-printed in `templates/requirements.md`):

```
## <N>. Quality attributes
**Section-kind:** nfr
```

```
SECTION-KIND IRON LAW
- NFR section MUST carry **Section-kind:** nfr (pre-printed in the template —
  do not delete it).
- absent = story  (unmarked section is a behavioral review unit)
- Fail visible: unmarked NFR → extra unit in preflight.
- Fail silent (forbidden): marking a real story nfr → boundary disappears.
```

Walk the four quality attributes:

- **Performance** — latency, throughput, resource ceilings.
- **Security** — authn/authz, data protection, the trust boundaries crossed.
- **Reliability** — availability, error budget, recovery, durability.
- **Accessibility** — conformance target (e.g. WCAG 2.1 AA), keyboard and
  screen-reader support.

Write each applicable one as an EARS criterion (Step 2's forms) that names a
**measurable-or-checkable target AND its verification method**, carrying a
hierarchical `**CODE-N.M**` ID so it traces through tasks and tests exactly like
a behavioral criterion. Example:

- `**CODE-3.1** WHEN the notes list renders 1,000 items THE SYSTEM SHALL paint
  the first screen within 200 ms at p95 — verified by a CI performance trace.`

An attribute that does not apply is **not silently dropped**: record it as
`None` with a short reason (e.g. "Accessibility: None — headless CLI") so the
skip is a visible decision, not an oversight.

The category is **additive, never a new gate**: a feature with no quality-attribute
concerns records `None` across the four and its behavioral criteria, structure,
and both authoring modes are unchanged — NFRs surface quality concerns, they do
not block on them. In tier-1 mini-spec mode, capture an NFR only when the fix
itself is a quality-attribute change; the category adds no NFR obligation to a
behavioral mini-spec.
**Done when:** the NFR section carries `**Section-kind:** nfr`, and each of the
four quality attributes is either an IDed NFR criterion or explicitly `None`.

## Step 3: Guard existing behavior

List every file the change touches, then work that list. A file with no existing
behavior at risk gets an explicit `no behavior to guard` line and nothing more;
for every existing behavior in the rest, add a guard —
`**CODE-N.M** (guard) WHEN <condition> THE SYSTEM SHALL CONTINUE TO <existing
behavior>`. Guards are what stop an agent from breaking load-bearing behavior
nobody mentioned. For a tier-1 bugfix this step plus one fix requirement IS the
spec, appended to the destination named under Two modes.
**Done when:** every file the change touches is listed; every existing behavior
found in those files has its own guard requirement; and every file with none
carries the explicit `no behavior to guard` line. An empty guard set with no list
behind it does not count.

## Step 4: Out of Scope

List what this feature deliberately does NOT do. This section is the defense
against scope creep during implementation and review.

## Step 5: Self-review, then the approval gate

Self-review before showing the user:
- **Ambiguity scan:** could any criterion be read two different ways? Pick one
  reading and write it in.
- **Testability scan:** can each criterion be verified by an automated test or
  a concrete manual check? Rewrite any that can't.
- **Placeholder scan:** no "TBD", "etc.", "handle errors appropriately".
- **Code-claim check (independent):** if any criterion asserts how the system
  currently works — a data format, an existing behavior, a constraint —
  dispatch a review subagent to prove-claim each such claim against the real code
  (grep/read the files, cite `file:line`, flag any that don't hold), writing
  findings to `.skills/<slug>-req-review.md`. A false premise here — "the body is
  ProseMirror-JSON" when it is Markdown — poisons design, plan, and code.
  Correct the criterion before the gate; do not read the code yourself. (No
  subagents? Do the check yourself against the code.)

**Story-quality gate (consumer of demoable act).** Recipe:

1. List every non-NFR `## N` with its `**Story:**` line.
2. Ask the user to confirm each names **one** demoable act.
3. **IF** any fails → split/rewrite and re-present. **IF** all confirmed → you may
   set `Status: Approved` after they approve the file.
4. Never silent-approve. "Looks fine" without the per-story yes is not confirmation.

Then present the FILE to the user for review and STOP. Do not proceed to
design on the strength of conversational agreement — the written requirements
are what get approved. On approval (including story-quality confirmation), set
`Status: Approved`.
**Done when:** the user has approved the written file and confirmed each
behavioral story is one demoable act.

## ID immutability

Once Status is Approved, IDs never change meaning and are never renumbered.
Retire a requirement by striking it through (`~~**CODE-1.2**~~ superseded by
CODE-1.4`). the `audit-trace` check treats struck-through IDs as undefined, so citing
tests/tasks surface immediately.

## Exit

REQUIRED SUB-SKILL: use `design-solution` (tier 2) or hand tier-1 fixes straight
to `test-first` with the new IDs.
