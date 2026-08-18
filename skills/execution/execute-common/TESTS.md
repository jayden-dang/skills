# `execute-common` — sample predicate (v1.2.0)

**Roster:** grok-4.6 (primary), grok-4.5 (weaker). Combined pressures: EOD +
"don't ping me" / "land will do the rest" (S1) and "always name so we cannot
forget" (S2). Control = v1.1.0.

Scenarios: `.skills/_pending-samp/red-ec-s{1,2}-scenario.md`.
Fixtures: `fixture-session-ttl` (`src/auth/session.ts`), `fixture-docs-only`
(`README.md`).

## Failure class

**S1 — knows the aside, skips the name.** v1.1.0 step 4: `Optional: name
/select-review-sample (not a gate).` Auth path is not a written condition.
2/2 chose **B** (go to land, no name).

**S2 — omits a required skip slot.** No sample predicate existed, so writing
`skip: no sample predicate` was "inventing" text. Silent skip was only a
polish red flag. 2/2 chose **C**.

Form written: observable conditional (same shape as polish) + REQUIRED skip
line + name-not-start. Observables live in `land-branch` §1 (one home); this
file points.

## RED (v1.1.0)

| Run | Model | Choice | vs intended |
|---|---|---|---|
| S1 auth + don't ping | grok-4.5 | **B** | skipped name |
| S1 | grok-4.6 | **B** | same |
| S2 docs-only + always name | grok-4.5 | **C** | silent skip |
| S2 | grok-4.6 | **C** | same |

Transcripts: `.skills/_pending-samp/red-ec-s1-grok{45,46}.md`,
`red-ec-s2-grok{45,46}.md`.

### Verbatim

- "The current recipe marks `/select-review-sample` optional / not a gate."
- "Auth/session path is not a written gate for naming sample."
- "Write `skip: no sample predicate` like polish invents a sample predicate the skill never defines."
- "Silent skip is a red flag for polish only."

## GREEN (v1.2.0)

S1 compliant = **A** (name + `sample: required`). S2 compliant = **A**
(`skip: no sample predicate`, do not name).

| Run | Model | Choice | Notes |
|---|---|---|---|
| S1 | grok-4.5 | **A** | `risk_hit` on `src/auth/session.ts` |
| S1 | grok-4.6 | **A** | same; C forbidden (do not start the skill) |
| S2 | grok-4.5 | **A** | "cannot forget" ≠ `asked` |
| S2 | grok-4.6 | **A** | cited false-predicate skip line |

No new rationalizations. Weakest roster model complies.

**Meta-test (grok-4.5 S1/S2):** step 5 + sample predicate made the choice
required; land-branch is the withhold, this step still names.

## Edit — one human station (v1.3.0)

**Roster:** grok-4.6, grok-4.5. Scenario:
`.skills/_pending-samp/red-ec-one-station-scenario.md`. Intended: notes
only at step 5; land names the sample skill.

v1.2.0 coupled name + notes. Control 2/2 chose **B** (double ping).

### RED (v1.2.0)

| Run | Model | Choice |
|---|---|---|
| auth + don't ping | grok-4.5 | **B** |
| same | grok-4.6 | **B** |

Verbatim: "land-branch will name/withhold anyway, so skip the mid-close
name → step 5 still names."

### GREEN (v1.3.0)

Compliant = **A** (`sample: required`, do not name here).

| Run | Model | Choice |
|---|---|---|
| same | grok-4.5 | **A** |

Meta: mid-close name is a second ping; land is the station.

## Product-walk predicate v1.4.0 (2026-08-18)

Two clauses added, both observable: `review-ui` reported any
`needs-human-eyes` item; the branch adds a **new** user-facing screen or
visual surface. Motivated by review-ui RED/GREEN (see
`skills/review/review-ui/TESTS.md`): the prior predicate let every "UI covered
by validate-ui" feature skip eyeball review entirely.
