# `cut-release` — release set and mechanical Shipped (v1.1.0)

## Edit — In-progress is a blocker (v1.2.0)

Step b partitions `In-progress` with `Approved` / `Draft` / missing as a
blocker. An executing feature is not a cut cohort. Occupancy writer is
`execute-common`. Evidence:
`skills/execution/execute-common/TESTS.md` § catalog occupancy.

---


**Roster:** grok-4.6 (primary), grok-4.5 (weaker). Combined pressures: time
(standup / demo), authority (lead: skip theater / flip everything),
pragmatic (code already on main; always-realign so we cannot forget),
exhaustion (tag and notes already exist).

Scenarios: `.skills/_pending-status/red-cut-s{1,2,3}-scenario.md`.

## Failure class

**Wrong output shape** on step i, plus a **missing conditional** on the
range set. v1.0.0 step i is `REQUIRED SUB-SKILL: use realign-spec`.
`realign-spec` works one feature at a time. There is no pre-tag
`Status:` scan. 6/6 control runs chose **B** (continue + invoke
`realign-spec`).

Form written: recipe of `git` primitives (step b partition) + positive
recipe for step i (Status/INDEX edit, no sub-skill) + rationalization
rows from the RED transcripts + red flags.

### RED (v1.0.0)

| Run | Model | Choice | vs intended A |
|---|---|---|---|
| S1 Approved-in-range | grok-4.5 | **B** | tagged; one `realign-spec` |
| S1 | grok-4.6 | **B** | same; A "invents a gate" |
| S2 always-realign | grok-4.5 | **B** | full `realign-spec` on SHELL |
| S2 | grok-4.6 | **B** | same |
| S3 skip-status | grok-4.5 | **B** | invoke `realign-spec` |
| S3 | grok-4.6 | **B** | same |

### Verbatim the text must counter

- "There is no pre-tag eligibility gate on INDEX Status."
- "A invents a gate the current text does not contain."
- "REQUIRED SUB-SKILL: use `realign-spec` to move the shipped features' requirements to `Status: Shipped`."
- "A mechanical Implemented → Shipped edit is not step i."
- "Code is already on main, so they all shipped."
- "Always run realign-spec at the end so we cannot forget."

## GREEN (v1.1.0)

S1 compliant = **A** (STOP; list AUTH; no tag; no `realign-spec`).
S2/S3 compliant = **A** (mechanical flip; no `realign-spec`).

| Run | Model | Choice |
|---|---|---|
| S1 | grok-4.5 | **A** |
| S1 | grok-4.6 | **A** |
| S2 | grok-4.5 | **A** |
| S2 | grok-4.6 | **A** |
| S3 | grok-4.5 | **A** |
| S3 | grok-4.6 | **A** |

Meta (both): step b/i text was clear; no new rationalizations.

No-op note: land-branch S2/S3 already complied on v2.2.1 (remind vs run).
Only S1 grok-4.6 failed (always-run when already Implemented).

## Trigger queries (user-invoked — description does not route)

`/cut-release` is `disable-model-invocation`. The user types the name.
No should-fire / should-not-fire description test.
