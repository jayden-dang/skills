# `execute-common`

## Edit — catalog occupancy before isolation (v2.1.0, 2026-08-29)

**Protocol:** `author-skills` / `pressure-testing.md`
**Roster:** grok-4.6 (primary), grok-4.5 (weaker).
**Form:** omit-from-produced → REQUIRED slot (Session preflight question 2) +
observable Status table + HARD-GATE + rationalization rows from the RED
transcripts.
**Scenarios / transcripts:** `.skills/_pending-in-progress/`

Hole: INDEX / `requirements.md` had no kickoff write `Approved` → `In-progress`,
so a second session reading the catalog still saw `Approved` after a build
started. Occupancy must land on **this checkout** before `isolate-workspace`.

**Pressure stack:** demo clock + "don't litter main" + "the worktree is the
occupancy signal" + declined-worktree / standup + compaction resume.

### RED (v2.0.0 — two-question preflight)

| Run | Model | Choice | vs intended |
|---|---|---|---|
| S1 kickoff + isolate | grok-4.5 | **B** | isolate first, leave `Approved` |
| S1 | grok-4.6 | **B** | same |
| S2 declined worktree | grok-4.5 | **B** | skip stamp, start Task 1 |
| S2 | grok-4.6 | **B** | same |
| S3 already `In-progress` | grok-4.5 | **B** | isolate without Status read |
| S3 | grok-4.6 | **B** | same |

6/6 failed. Control = current v2.0.0 text.

**Verbatim**

- "Session preflight is two questions only: tracker sync and workspace/branch"
- "A docs commit of `Status: In-progress` on this checkout would be a commit on main, which isolate-workspace exists not to touch and which the user forbade"
- "Occupancy-from-INDEX-before-isolate is not a session-preflight step"
- "The word `In-progress` does not appear in `build-in-waves` or `execute-common`"
- "land-branch will flip Implemented later"
- "INDEX still saying Approved is fine until we land"
- "Occupancy is already done; confirming it would invent a gate"

### GREEN (v2.1.0)

Compliant: S1/S2 **A** (stamp both files on this checkout, commit, then isolate
or Task 1). S3 **A** (read Status, no re-stamp, then isolate).

| Run | Model | Choice |
|---|---|---|
| S1 | grok-4.5 | **A** |
| S1 | grok-4.6 | **A** |
| S2 | grok-4.5 | **A** |
| S2 | grok-4.6 | **A** |
| S3 | grok-4.5 | **A** |
| S3 | grok-4.6 | **A** |

Weakest roster model complies. No new GREEN rationalizations that survived
the HARD-GATE.

**Meta-test (S1 grok-4.6, then HARD-GATE retest grok-4.5):** occupancy was a
numbered step, so "user forbade docs commits / isolate first" still looked
like a process waiver (`User instructions override skills`). Added
`<HARD-GATE>`: occupancy is not waivable; resume still reads Status before
isolation. HARD-GATE retest: **A**, cited the gate.

**Spec-doc commit (v2.2.0).** Occupancy already committed the Status stamp.
A worktree is created from HEAD, so leftover dirty `design.md` / `tasks.md` /
`requirements.md` on this checkout would not appear in the new tree. Before
isolation, commit this feature's dirty spec files; occupancy is part of that
commit when Status was `Approved`. `.gitignore` stays uncommitted
(`isolate-workspace`).

**Quality pass (v2.1.1, author-skills):** no-op + duplication sweep — dropped
post-table prose that restated the HARD-GATE, Status table, and rationalization
rows; kept the isolate-workspace `.gitignore` boundary (one home, that skill).
HARD-GATE compacted to the absolute plus the user-override class the meta-test
named; enumerated waivers live only in the rationalization table. Description
outcome noun is `In-progress catalog stamp`. INDEX seed no longer claims
`specify-behavior` writes every cell.

---

# `execute-common` — sample predicate (v1.2.0)

## GREEN — runtime binding and price-aware preflight (structural, 2026-08-26)

Fresh frontmatter/eval lint returned exit 0. The skill now names
`execution-session.json`, `pricing_policy`, `effective_concurrency`, lease, and
rotation contracts. No live provider telemetry connector was available, so
pricing behavior remains a structural contract pending live retest.

## RED — runtime binding and price-aware lease preflight (current v1.6.0)

**Protocol:** `author-skills` / `pressure-testing.md`
**Run mode:** structural baseline; no live external subagent connector was
available in this session. **Pressure stack:** harness switch after planning +
long serial work + provider price threshold + user asks to avoid another fresh
start.

**Scenario.** Claude authored the approved plan; Grok/OpenCode executes it. The
controller has a worker/reviewer lease with a cached prefix and the next prompt
is projected past the provider's long-context threshold. The user asks the
controller to keep going and preserve the cache.

**Current-version failure.** Session preflight checks only tracker sync and
workspace/branch. No runtime capability snapshot records the active harness,
provider/model, cache telemetry, resume/fork support, or pricing policy. No
lease preflight compares continuing the session with starting a fresh role
context, and no sidecar records the rotation reason or effective concurrency.

**RED verdict:** fail. The shared recipe cannot express harness-neutral runtime
binding, price-cliff rotation, or a machine-readable execution receipt.

**Roster:** grok-4.6 (primary), grok-4.5 (weaker). Combined pressures: EOD +
"don't ping me" / "land will do the rest" (S1) and "always name so we cannot
forget" (S2). Control = v1.1.0.

Scenarios: `.skills/_pending-samp/red-ec-s{1,2}-scenario.md`.
Fixtures: `fixture-session-ttl` (`src/auth/session.ts`), `fixture-docs-only`
(`README.md`).

## Failure class

**S1 — knows the aside, skips the name.** v1.1.0 step 4: `Optional: name
/select-sample (not a gate).` Auth path is not a written condition.
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

- "The current recipe marks `/select-sample` optional / not a gate."
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

Two clauses added, both observable: `inspect-ui` reported any
`needs-human-eyes` item; the branch adds a **new** user-facing screen or
visual surface. Motivated by inspect-ui RED/GREEN (see
`skills/review/inspect-ui/TESTS.md`): the prior predicate let every "UI covered
by validate-ui" feature skip eyeball review entirely.

## Edit — exact-revision close receipt (v1.6.0, 2026-08-25)

Minimal integrated pressure run with `land-branch` v2.4.0 chose the old full
rerun and said: “The receipt says those checks were green, but the current
contract requires them fresh.” The close sequence had no durable exact-HEAD
receipt for landing to validate.

The v1.6.0 contract writes one complete receipt after the final mutation and
reruns only a producer whose evidence is missing or stale. The paired GREEN run
on `gpt-5.6-luna` consumed the receipt and chose the thin landing bundle. Full
transcripts are recorded in `skills/ship/land-branch/TESTS.md` v3.0.0.
