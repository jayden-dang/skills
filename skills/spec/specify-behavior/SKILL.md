---
name: specify-behavior
version: 1.2.1
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
set's `templates/requirements.md`. Resolve pack seeds in this order, first
path that exists: (1) `templates/` beside this SKILL.md, (2)
`${CLAUDE_PLUGIN_ROOT}/templates` when that variable is set, (3)
`../../../templates` relative to this SKILL.md. Every heading in that template is a
REQUIRED slot: fill it, or write `None` under it — never drop one. Then run the full
sequence below. Create a todo per step.

## Step 1: Register the feature code

Pick a short unique prefix (2–12 chars, A–Z0–9, starts with a letter — e.g.
`SHELL`, `SYNC2`). Check `docs/specs/INDEX.md`; add a row there BEFORE writing
requirements. Never reuse a retired code.

**Bind the roadmap item.** Slot vs CODE definitions live in `plan-milestones`
(**ROAD-N is a slot, not a feature**). This step only writes the join.

WHERE `docs/roadmap/INDEX.md` exists and this work implements one of its items, put that
item's `ROAD-N` in the row's **Roadmap item** column. WHERE there is no roadmap, or the work
was never a roadmap item, write `—`.

This column is the only plan↔spec join, and this step is its only writer — never invent a
`ROAD-N` here. IF the chosen ROAD is already bound to another CODE (`R6` in
`templates/roadmap-findings.md`) → stop and surface the collision; do not rebind or mint
another ROAD.

**Promote ephemera.** IF a `.skills/_pending-<slug>/` directory was used for this work, move it to `.skills/<CODE>/` (`mv` when CODE dir absent) so subsequent writes use the Feature root — see `templates/skills-ephemera-paths.md`.
**Done when:** the code has a row in INDEX.md with status Draft, and its Roadmap item cell
holds a `ROAD-N` or `—`, and that ROAD is not already bound to another CODE.

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

### System docs for NFR grounding (thin consult)

**Load:** `skills/project/define-system-doc/consult-recipe.md` (authority,
hard-constraint precedence, no-op when absent/non-authoritative, once-per-entry
suggest, never auto-invoke).

**When:** before writing each quality-attribute line that is **material** for
this feature (the attribute is not already headed for `None`). Do **not** load
architecture narrative, codebase map/modules/ownership/deps, or ops runbooks
here — those are design-solution / plan-tasks layer.

| Attribute material when… | Consult if Approved | Ground the NFR with… |
|---|---|---|
| Feature owns a measured latency/throughput surface | `docs/product/metrics.md` first; if Absent/non-authoritative, then `docs/ops/reliability.md` for latency/throughput **SLO** lines only | standing product metric, else greppable `SLO-N` that names this surface — never a freehand number when either doc defines one |
| Crosses authn/authz, tenant scope, public vs admin data, or compliance | `docs/security/threat-model.md`; also `compliance.md` when regulatory | greppable `TB-N` / `THR-N` / `CMP-N` **only** when bold-defined in those docs |
| Owns availability, error budget, recovery, or durability targets | `docs/ops/reliability.md` | greppable `SLO-N` (or stated error-budget rule) **only** when bold-defined. A pure latency SLO used under Performance does **not** force Reliability material |
| Ships UI a person perceives (not headless/API-only) | `docs/standards/accessibility.md` | house conformance target and keyboard/SR rules |

**Story actors (not an NFR slot):** WHEN a `**Story:**` line names a product role
and `docs/product/personas.md` is Approved, align the actor with standing persona
vocabulary — do not invent a parallel cast.

**Hard constraints for this step** (outrank any system doc — consult-recipe):
confirmed frame-change decisions and vision non-goals. Live `ARCH-N` the feature
already relies on stays binding; do not invent a contradicting NFR.

**Write rules after consult:**

- **Approved + material:** write the NFR EARS criterion so its measurable target
  (and any TB/THR/CMP/SLO ID you cite) comes from the Approved doc — not from
  industry habit or a number you invent. Name verification method as today.
- **Absent or non-authoritative (after the table's full path):** CONTINUE
  (no-op). Then, in order: (1) frame-change lock that already states a target →
  use it; (2) else domain-judgment EARS **without** a fabricated greppable ID;
  (3) else `None — no standing <entry> target`. Suggest
  `/define-system-doc <entry-key>` **at most once per entry** when the gap is
  material for *this* feature; never auto-invoke.
- **Do not invent** TB/THR/CMP/SLO (or product metric IDs) without a bold
  definition in an Approved doc. Prefer omitting the ID (prose target from a
  lock) or `None — no standing <entry> target` over a fabricated ID.
- Design-solution still owns HOW (`Security:` / `Reliability:` design slots,
  seams, modules). This step only mints **WHAT** quality criteria as `CODE-N.M`.

Write each applicable attribute as an EARS criterion (Step 2's forms) that names a
**measurable-or-checkable target AND its verification method**, carrying a
hierarchical `**CODE-N.M**` ID so it traces through tasks and tests exactly like
a behavioral criterion. Example (targets illustrated only — prefer standing docs
when Approved):

- `**CODE-3.1** WHEN the notes list renders 1,000 items THE SYSTEM SHALL paint
  the first screen within 200 ms at p95 — verified by a CI performance trace.`

An attribute that does not apply is **not silently dropped**: record it as
`None` with a short reason (e.g. "Accessibility: None — headless CLI") so the
skip is a visible decision, not an oversight. `None` is for non-material
attributes, **not** a shortcut past consult when the attribute *is* material.

The category is **additive, never a new gate**: a feature with no quality-attribute
concerns records `None` across the four and its behavioral criteria, structure,
and both authoring modes are unchanged — NFRs surface quality concerns, they do
not block on them. In tier-1 mini-spec mode, capture an NFR only when the fix
itself is a quality-attribute change (run this thin consult only for that
attribute); the category adds no NFR obligation to a behavioral mini-spec.

| Thought | Reality |
|---|---|
| "Design will set security/SLO targets later" | Design `Satisfies` NFR IDs; freestyled design prose is not a `CODE-N.M` contract |
| "Industry default (200 ms / WCAG AA) is fine" | Approved house docs outrank habit; inventing a target when the matching doc is Approved is a miss |
| "No system docs — invent TB-1 so design can cite it" | No bold definition → no ID; use prose or `None — no standing threat-model` |
| "Consult means load architecture and codebase map" | Wrong layer; thin table only — design-solution owns shape docs |
| "Standup in five — mark all four None" | Material attributes need a criterion or an honest reason; time changes *when* you report, not whether consult ran |

**Done when:** the NFR section carries `**Section-kind:** nfr`; each of the four
quality attributes is either an IDed NFR criterion or explicitly `None` with
reason; and for every **material** attribute the consult outcome is recorded
(Approved doc used, or Absent/non-authoritative no-op) before the line is written.

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
- **Placeholder scan:** no bare "TBD", "etc.", "handle errors appropriately".
  WHEN the clarify-decisions close package listed **Owned unknowns**, paste them
  into Open Questions as `topic — owner — date — forbid-guess` (`cấm đoán`). A bare
  TBD without those three fields **blocks** `Status: Approved` — do not delete
  Open Questions by sweeping unknowns under the rug.
- **Code-claim check (independent):** if any criterion asserts how the system
  currently works — a data format, an existing behavior, a constraint —
  dispatch a review subagent to prove-claim each such claim against the real code
  (grep/read the files, cite `file:line`, flag any that don't hold), writing
  findings to `.skills/<CODE>/req-review.md`. A false premise here — "the body is
  ProseMirror-JSON" when it is Markdown — poisons design, plan, and code.
  Correct the criterion before the gate; do not read the code yourself. (No
  subagents? Do the check yourself against the code.)
- **Close-package ingest (when present):** paste Success / Boundaries / Accepted
  risks into Out of Scope, NFR, or story criteria as appropriate; do not drop
  Reliability locks by marking NFR `None` when the close package already locked
  prose targets or Owned unknowns for Reliability.

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
