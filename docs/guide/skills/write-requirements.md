# `write-requirements`

> The durable statement of intent. User stories and EARS criteria, each carrying an ID that every later task, test, and commit will cite.

|  |  |
|---|---|
| **Bucket** | spec |
| **Invocation** | model-invocable (the agent calls it on its own) |
| **Reads** | `templates/requirements.md`, `docs/specs/INDEX.md`, the approved brainstorm outcome |
| **Writes** | `docs/specs/<date>-<feature>/requirements.md`, a row in `docs/specs/INDEX.md`, an independent review to `.skills/<slug>-review.md` (via subagent) |
| **Calls** | a review subagent (independent code-claim check), then [`write-design`](write-design.md) (tier 2) or [`tdd`](tdd.md) (tier 1) |
| **Called by** | [`brainstorm`](brainstorm.md) |

## When it fires

After discovery is complete and a tier-1 or tier-2 change needs its requirements written. It runs once the shape of the feature is agreed but before any design or code exists. The output is the source of intent that outlives the conversation: every task footer, every test annotation, and every commit trailer downstream cites the IDs this skill mints.

For a tier-1 bugfix the skill is deliberately small — a guard on the behavior being fixed plus one fix requirement is the whole spec, appended to the owning feature's file or to `docs/specs/fixes.md`. For a tier-2 feature it produces a full stories-and-criteria document.

## The five steps

The skill walks five steps, one todo each, starting from `templates/requirements.md`.

1. **Register the feature code.** Pick a short unique prefix — 2 to 12 characters, `A–Z0–9`, starting with a letter (`SHELL`, `SYNC2`). Add a row to `docs/specs/INDEX.md` with status Draft *before* writing any requirements. A retired code is never reused, so the ID namespace stays globally unambiguous.

2. **Write stories and EARS criteria.** One `## N. <title>` section per user story. Each acceptance criterion is an EARS statement with a hierarchical ID `**CODE-N.M**`. One observable behavior per criterion — if a sentence needs "and", it is usually two criteria.

3. **Guard existing behavior.** For every existing behavior the feature touches, add a guard that pins it in place so an agent cannot break load-bearing behavior nobody mentioned.

4. **Out of Scope.** List what the feature deliberately does not do — the defense against scope creep during implementation and review.

5. **Self-review, then the approval gate.** Run the scans, dispatch the independent code-claim check, then present the written file and stop for approval.

## The five EARS forms

Every criterion takes exactly one form. Choosing the form forces you to name what kind of behavior you mean — an event, a sustained state, an error path, an optional feature, or a standing invariant.

| Form | Shape | Use for |
|---|---|---|
| Event-driven | `WHEN <event> THE SYSTEM SHALL <behavior>` | a response to a trigger |
| State-driven | `WHILE <state> THE SYSTEM SHALL <behavior>` | behavior that holds during a state |
| Unwanted condition | `IF <condition> THEN THE SYSTEM SHALL <behavior>` | error handling |
| Optional feature | `WHERE <feature enabled> THE SYSTEM SHALL <behavior>` | behavior gated behind a flag |
| Ubiquitous | `THE SYSTEM SHALL <behavior>` | an always-true invariant |

The [EARS reference](../resources/ears.md) covers the grammar in full. The done-condition for this step is that every story has at least one criterion and every criterion carries exactly one of these forms.

## Guards

A guard is a criterion in the shape `**CODE-N.M** (guard) WHEN <condition> THE SYSTEM SHALL CONTINUE TO <existing behavior>`. Guards are what stop the implementer from quietly breaking behavior the feature happens to sit next to. The step is not done when you glance and find nothing to guard — it is done when you have *actively searched the touched surface* for behaviors to guard and either written them or confirmed there are none. "Found none by default" is not the same as "searched and found none", and the skill draws the line there deliberately.

For a tier-1 bugfix this step plus one fix requirement is the entire spec. The guard pins the behavior being fixed so the fix cannot regress it, and the fix requirement states the new correct behavior. Those two criteria, appended to the owning feature's `requirements.md` — or to `docs/specs/fixes.md` when no feature owns the surface — are the whole document; there is no separate design or plan.

## Self-review and the code-claim check

Before showing the user anything, the skill runs four scans:

- **Ambiguity scan** — could any criterion be read two ways? Pick one reading and write it in.
- **Testability scan** — can each criterion be verified by an automated test or a concrete manual check? Rewrite any that cannot.
- **Placeholder scan** — no "TBD", "etc.", "handle errors appropriately".
- **Code-claim check (independent)** — if any criterion asserts how the system *currently* works (a data format, an existing behavior, a constraint), dispatch a review subagent to verify each claim against the real code, cite `file:line`, and flag any that do not hold. The findings land in `.skills/<slug>-review.md`, and you correct the criterion before the gate. You do **not** read the code yourself: a false premise here — "the body is ProseMirror-JSON" when it is actually Markdown — would poison the design, the plan, and the code that follow. (With no subagents available, you do the check yourself against the code.)

Then the skill presents the **written file** and stops. Conversational agreement is not approval — the file is what gets approved, and on approval its `Status` becomes Approved. The template carries an **Open Questions** section for anything still unresolved; every entry must be settled before the status flips, and the section is deleted once empty. Approving a file with open questions would leave the design step to guess, which is exactly the ambiguity the scans exist to remove.

## ID immutability

Once `Status` is Approved, an ID never changes meaning and is never renumbered. To retire a requirement you strike it through: `~~**CODE-1.2**~~ superseded by CODE-1.4`. [`check-trace`](../resources/scripts.md#check-trace) treats a struck-through ID as undefined, so any test or task still citing it surfaces immediately as an E1 error rather than rotting silently. This is why the ID, not the prose, is the unit of reference across the whole system — see [Requirement IDs](../concepts/requirement-ids.md).

## Worked example

The feature is `SHELL`: a left icon rail for switching between the app's modules. This example carries across the [`write-design`](write-design.md) and [`write-plan`](write-plan.md) pages, so the three read as one story.

Step 1 adds a `SHELL — Draft` row to `docs/specs/INDEX.md`. Then `requirements.md`:

```md
## 1. Switch the active module

**Story:** As a user, I want a left icon rail, so that I can move between
modules without losing my place.

- **SHELL-1.1** WHEN the user clicks a module icon in the rail THE SYSTEM
  SHALL make that module active and render its panel.
- **SHELL-1.2** WHEN the app reloads THE SYSTEM SHALL restore the module
  that was active before the reload.
- **SHELL-1.3** IF the persisted module id no longer exists THEN THE SYSTEM
  SHALL fall back to the default module.

## 2. Keyboard access

**Story:** As a keyboard user, I want to reach the rail, so that I do not
need a pointer.

- **SHELL-2.1** WHILE the rail has focus THE SYSTEM SHALL move the selection
  with the arrow keys.
- **SHELL-2.2** (guard) WHEN a module renders THE SYSTEM SHALL CONTINUE TO
  restore that module's last scroll position.

## Out of Scope

- Reordering or hiding rail icons — the rail is fixed for this feature.

## Open Questions

- (resolved before approval; the section is deleted once empty)
```

Reading the excerpt against the five steps:

- **Step 1** put a `SHELL` row in `INDEX.md` before a word of this file was written.
- **Step 2** gives each criterion exactly one EARS form — `SHELL-1.1`/`SHELL-1.2` event-driven, `SHELL-1.3` the `IF…THEN` error path, `SHELL-2.1` the `WHILE` state form — and one observable behavior each, so none needs an "and".
- **Step 3** produced `SHELL-2.2` (guard): rendering a module already restores scroll position, and the search for touched behavior found it, so it is pinned rather than left to break silently.
- **Step 4** is the Out of Scope line that keeps "let me just also let users reorder the icons" out of implementation.
- **Step 5** runs the scans and, because `SHELL-1.2` asserts persistence exists, dispatches the code-claim check to confirm the store actually persists before the user is asked to approve.

When a tier-1 bugfix later lands on the persistence path, it appends `SHELL-1.4` as a fix requirement and guards `SHELL-1.2` — the immutable IDs from this file are exactly what that fix's test and commit trailer cite.

## Exit

The skill hands off as a required sub-skill: [`write-design`](write-design.md) for tier-2 features, or [`tdd`](tdd.md) directly for tier-1 fixes, carrying the new IDs. It never proceeds on conversational agreement — the file must be Approved first. Which route it takes is the tier decision made back in [`brainstorm`](brainstorm.md); see [ceremony tiers](../methodology/ceremony-tiers.md) for what separates a tier-1 fix from a tier-2 feature.

## Why it is written the way it is

Requirements are the root of the trace spine. If an ID is ambiguous, untestable, or built on a false claim about the current code, the error does not stay contained — it propagates through design, plan, tests, and shipped behavior, and each hop makes it harder to see. So the skill front-loads the cost: register the code before writing, force each criterion into a single EARS form, guard by active search rather than by default, and verify every code-claim with a fresh pair of eyes that has no stake in the framing. The approval gate is on the written file precisely because the file — not the chat — is what the rest of the system will read.

## See also

- [Requirement IDs](../concepts/requirement-ids.md) — why the ID outlives the prose
- [EARS reference](../resources/ears.md) — the five criterion forms in full
- [`write-design`](write-design.md) — the next step for tier-2 work
- [`brainstorm`](brainstorm.md) — the discovery skill that hands off to this one
