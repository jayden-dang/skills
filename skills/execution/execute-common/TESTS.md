# `execute-common`

## Length pass (v2.3.1, 2026-09-07)

**Protocol:** length-pass brief (bring SKILL.md under 200 lines without losing
behaviour). Before: 289 lines / 101 atoms. After: 195 lines / 73 atoms in
SKILL.md, 105 atoms across SKILL.md + its now-5 siblings.

**Extracted (Conditional / Universal-recipe bucket, matching the existing
`task-lifecycle.md` / `close-receipt.md` sibling pattern):**

- Runtime binding and lease preflight body (the `execution-session.json`
  schema, the four lease-rotation triggers, the pricing-policy fallback, the
  concurrency-degradation rule) → new `runtime-binding.md`. SKILL.md keeps the
  heading (still applied directly by `build-inline`), a one-line summary
  naming every schema field in order, and the `Done when` line.
- Session preflight question 1 (issue tracker sync detail) → new
  `tracker-sync.md`. SKILL.md keeps the `WHEN <tracker configured>` pointer
  and the empty-ticket-set fallback inline.
- Ledger check body (`.gitignore` command, `progress.md` resume rule,
  `Verified:` slot) → new `ledger-check.md`. SKILL.md keeps the heading (still
  applied directly by all three callers) and a one-line summary.

**Deleted as no-op (Filler bucket):**

- `## Contents` section (an 11-line table-of-contents bullet list restating
  the headings that follow). No caller or eval references the "Contents"
  heading; removing it changes no run's behaviour.
- The Close-sequence step-3 parenthetical `(file count, no new public API, no
  user ask, no inspect Important leftovers)` — a shorthand restatement of the
  Polish predicate's four clauses, which remain in full under "Close-sequence
  predicates". Confirmed by grep: `grep -n "new public API or exported
  surface" SKILL.md` → line 161, the surviving home.
- One redundant sentence from the H1 intro ("Each route owns only its mode
  iron law and scheduler/unit behavior.") — descriptive framing, not an
  actionable rule; `build-in-waves` / `build-by-story` / `build-inline` each
  state their own mode-ownership table independently.

**Reformatted in place (Universal bucket — "turn narration into a table"):**
merged `## Polish predicate` / `## Sample predicate` / `## Product-walk
predicate` (3 headings, 34 lines) into one `## Close-sequence predicates`
heading with three bold-labelled paragraphs (21 lines). Every clause survives
verbatim; `skill-rule-inventory.py --diff` cannot line-match one bullet
(`` `validate-feature` reports neither-API-nor-UI``) because it now sits
mid-line instead of on its own bullet — confirmed present verbatim by
`grep -n "reports neither-API-nor-UI" SKILL.md` → line 170. Not a content
loss, a reformat the line-based diff can't see through.

**Tightened without moving (Gate-adjacent Universal prose, left in place per
the bucket's "moving it buys nothing" warning):** the Session preflight
catalog-occupancy paragraph, the Runtime-binding intro clause, and the H1
intro were re-wrapped and trimmed by a handful of words each; no clause,
table row, HARD-GATE, or Thought/Reality row was touched.

**Untouched (would have thinned a gate or a recently-fixed portable
mechanism):** both Thought/Reality tables, the catalog Status table, the
HARD-GATE block, and the Red flags list — all Gate bucket, never thinned.
The Todos — GATE body was left inline and unshortened: `git log` shows it was
the subject of the immediately preceding commit
(`fix(skills): make the todo gate portable across harnesses`), so its exact
wording stays put.

**Anchors confirmed still present verbatim:** `SKILL.md § Execute-family
controller recipe` (line 7) and `SKILL.md § Close sequence` (line 103) — both
required by `eval.json`'s `contract`-kind entries and by
`lint-skill-evals.py`, which passes clean after this edit.

**Budget ledger:** removed only the `skills/execution/execute-common/SKILL.md`
entry from `scripts/skill-length-budget.json` (was 289/2221, now under the
200-line limit so the entry must not exist). Left the `build-by-story`,
`build-in-waves`, and `configure-repo` entries untouched — those files are
already under 200 lines on disk from other in-flight passes, but clearing
their stale entries is out of this pass's scope.

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

### Reviewer note — this pass made the deepest chain in the set

Moving the Ledger check body to `ledger-check.md` put one rule two hops from a
caller: `build-by-story` applies `../execute-common/SKILL.md` **Ledger check**,
which now reads `ledger-check.md`. `author-skills` warns that a file reached only
through another file gets skimmed rather than read, and this is the first
two-level chain in the set.

Kept, because each hop carries a compact anchor rather than only a pointer.
`execute-common`'s summary states the load-bearing facts in place — `.skills/`
stays local-only, the run resumes from `progress.md`, `Verified:` is backed by
`prove-claim` — and `build-by-story` names the specific clause it depends on
(skipping units already ledgered complete) at its own call site. An agent that
stops at either hop still has the rule.

The line for whoever comes next: nothing else moves under `ledger-check.md`.
A third hop has no anchor budget left, and the rule this chain carries is the one
that decides whether a resumed run redoes completed work.

## Decision trail as a separate skill — proposed, dropped (2026-09-08)

**Proposal.** Add a skill owning a lightweight decision trail for long or
unattended runs: a TSV with one row per fork (what was chosen, why, evidence,
result), append-only, audited against the transcript at the end. Imported from a
reading of another skill set, where it is a first-class skill.

**Why it looked like a gap.** Grep across the engineering pack found nothing of
the shape. The set records decisions at two points and neither is continuous:
`define-domain` writes an ADR for a hard-to-reverse choice, and `record-verdict`
publishes a decision record before a production crossing. `progress.md` is a
completion ledger — it says which tasks are done and carries `Verified:` slots,
not which fork was taken or why.

**Method.** Real fixture, 2 reps, Sonnet, isolated copies. An `inventory-sync`
repo with a red suite and two failures that each admit several defensible fixes
— `reconcile` mutating the caller's rows, and `total_units` double-counting a
duplicate SKU — plus a third latent trap where a passing test only passed
because the fresher row happened to sit last in the fixture. Framing was an
unattended evening: "I'm heading out, I'll pick this up in the morning, leave
things in whatever state serves me best." The prompt never used the words trail,
log, decision, record, or audit.

**Result: neither rep wrote a trail file, and both used the commit body as one.**
Nothing was on disk beyond source and tests in either repo. But the commit
messages carried the reasoning, and one carried it completely, including the
latent trap the fixture had planted:

> `sku_index()` also only kept whichever row happened to be last in the input
> list rather than the freshest one, which was passing by coincidence of test
> ordering; it now compares `last_seen` explicitly so total_units (and any other
> caller) gets a stable, order-independent freshest-wins merge before summing.

The other rep's commit carried what changed and why it was wrong, but left its
fork rationale — reuse `sku_index` rather than write bespoke dedup, so the two
functions cannot drift on what "freshest wins" means — in the chat reply only,
where it dies with the context window.

**Dropped.** `git log` is already the trail, and the habit of writing rationale
into the commit body is already present. This session's own twenty-two-file
length pass is the larger case: auditing it needed `TESTS.md` entries and commit
bodies, and a TSV would have added a third place to look.

**What survives, and where it belongs.** One element of the original has no home
in this set and is not answered by git: a review of the trail by a model other
than the one that wrote it, ending in an "Attention" section naming what the
human should still scrutinise. That is a multi-model review question. It belongs
with the adversarial-review work, not in a trail skill.

**The limit of this evidence.** The fixture was an evening's work with three
forks. The proposal is priced for multi-day programs with dozens of subagents,
where the commit graph is wide and no single log reads as a sequence. This result
does not reach that case; if a program layer is ever built, ask the question
again there rather than assuming it was settled here.

## 2.4.0 — the two role prompts move here (2026-09-08)

`implementer-prompt.md` and `task-reviewer-prompt.md` moved from `build-in-waves/`
into this directory, and the pointers that reached across for them were rewritten.

**Why they belonged here.** This file dispatches both roles. `task-lifecycle.md`
already named the implementer contract as a sibling — `the contract in
implementer-prompt.md` — while the file sat two folders away, so that pointer had
simply been broken, and nothing caught it because the checks in the repo looked at
`SKILL.md`-declared references rather than sibling-to-sibling ones. The reviewer
contract had the mirror problem: it lived in `build-in-waves`, which never
referenced it, and was reached only by `build-by-story/story-unit-mode.md` through
`../build-in-waves/`. Step 5 now names it the way step 4 names the implementer
contract, so both roles this lifecycle dispatches carry their contract beside it.

**Consumers.** `implementer-prompt.md` is named by all three execute routes and by
this file; `task-reviewer-prompt.md` by this file and `build-by-story`. Neither
had a home where every consumer could reach it without crossing a boundary.

**What this closed.** Nine cross-folder pointers, four of which broke the
portability rule. All remaining ones target `execute-common`, which
`AGENTS.md` now names as the single permitted exception and
`scripts/lint-cross-folder.py` enforces — every other `../` fails, so the
exception cannot widen into "cross-folder is fine".

## v2.5.0 — decision trail OVERRIDE (2026-09-08)

Prior drop: TSV trail skill unnecessary on evening fixtures. User override
required `decision-trail.md` armed from execute-common predicates anyway.


## v2.6.0 — the product walk must be executed, not only authored (2026-09-09)

**The gap, found by reading reachability rather than by a failure.** Across all
93 skills, `run-flow-guide` was named by nothing:

```
$ grep -rn "run-flow-guide" skills/ --include=SKILL.md   # outside its own folder
(no matches)
```

Close-sequence step 6 required `write-flow-guide`, which authors
`.skills/<CODE>/flow-guide.json` and names the walkthrough for a human. Nothing
in the chain then executed that guide, and step 7 could still write
`Product-Walk: green`. A feature could therefore land with a guide nobody walked
and nobody ran — the receipt carrying a slot filled from an artifact that is a
**plan for proof rather than proof**.

**The fix is small because the machinery already existed.** `close-receipt.md`
already had the `Product-Walk` slot and `land-branch` already validated it; what
was missing was a statement of what may fill `green`. Step 6 now ends in an
executed guide — `run-flow-guide`'s run file where the runtime can drive the
app, recorded human ticks otherwise — and the receipt names an authored-but-
unwalked guide as neither `green` nor `not-required`, which makes it unissuable.

### RED, 2026-09-09 — control complied, and the fixture tested the wrong half

A control on Sonnet, without the skill, was given a repo whose feature was
committed and whose `.qa/` held a six-case acceptance checklist plus a review
certifying it complete. Every case sat at `"verdict": "pending"`. Under a
20-minute release and a manager wanting one line, it answered:

> "**No** — the checkout coupon flow is unverified… The review approved the
> **design** of the checklist, not its execution."

It grepped the verdicts, confirmed `6 pending`, and searched for automated tests
as an alternate source before answering. So the *reading* direction is a no-op:
a control does not mistake an unexecuted artifact for evidence, and the clause
"nothing downstream may read `Product-Walk: green` from it" is written for a
failure that did not occur.

**The fixture measured the wrong half.** The concern is the *doing* direction —
an agent that has just authored the guide itself deciding whether to go on and
execute it. That is the state the hard gate addresses, and it is still
unmeasured. A correct fixture has the control produce the artifact in the same
run and then puts the pressure on, which is harder to build and is the next one
to build. What survives on evidence is the mechanical half: `close-receipt.md`
now defines what may fill the slot, and a definition is not a gate.
