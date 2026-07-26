# Design: Milestone assessment

Feature code: ASSESS
Status: Approved
Date: 2026-07-26
Requirements: ./requirements.md

## Context

The roadmap layer (RMAP) shipped two skills and stopped deliberately short of one boundary.
`write-roadmap` authors milestone intent and owns every write to `docs/roadmap/INDEX.md`;
`check-roadmap` derives structural health read-only and carries a `<NON-NEGOTIABLE>` block
handing outcome judgment to a future skill by name. Nothing in the set writes a milestone's
`Closed:` slot except `write-roadmap`, and nothing anywhere judges whether a milestone
actually delivered what its `Outcome:` sentence promised. This feature fills exactly that
gap and nothing wider.

The constraint that shapes everything here is **ARCH-1 plus ARCH-5 in tension**. ARCH-1
requires vertical checks to be exact `grep`/`git`/file-read passes, never LLM judgment —
but "was the outcome achieved" is irreducibly a judgment. The resolution is to split the
skill in two along that line: every *precondition* (scope resolution, structural rules,
handoff verification, close eligibility) is a mechanical pass that two agents reproduce
identically, and the one genuinely judged thing — the outcome verdict — is never terminal on
its own, because a human disposition gates it. ARCH-1 is respected because nothing judged is
ever treated as a check. Meanwhile ARCH-5 forbids this user-invoked skill from invoking
`check-roadmap` or `allocate-attention`, both of which carry
`disable-model-invocation: true` — and `scripts/lint-handoffs.py` enforces that mechanically
at commit time, so the design cannot cheat it.

That last constraint is what makes rule *reuse* structural rather than optional. `R1`–`R11`
live inline in `check-roadmap/SKILL.md` today, and this feature needs the withholding subset
of them. It cannot call `check-roadmap` to get them, so the rules must move somewhere both
skills read. The repo has exactly one established mechanism for shared content across
skills — `templates/`, resolved as `${CLAUDE_PLUGIN_ROOT}/templates` by seven skills already,
and already the authoritative home for the roadmap's `S1`–`S7` structural rules. No skill in
the set reads another skill's `references/` directory; introducing that pattern for one file
would be a new cross-skill coupling with no precedent and no resolution rule.

A note on posture: this repo is `Production` / `Active development`, so backward
compatibility carries real weight. Two shipped skills change behavior here. `check-roadmap`
changes only where its rules are *stated* (its finding set is guarded byte-for-byte by
ASSESS-5.4) plus one added ladder row. `write-roadmap` genuinely loses a capability — it can
no longer close a milestone unilaterally, in any repo, including one that never runs this
skill. That is the intended reading of "close the bypass," and it is the single most
consequential decision in this design.

## Decisions

1. **Shared rules live at `templates/roadmap-findings.md`.** `R1`–`R11` move out of
   `check-roadmap/SKILL.md` into a new file both skills read by the existing
   `${CLAUDE_PLUGIN_ROOT}/templates` resolution. It is a rules statement, not a seed:
   `setup-repo` and `establish-project` name the template files they copy individually and
   never glob, so nothing copies it into a consumer repo.
2. **Outcome judgment is never a check.** The mechanical passes and the judged verdict are
   separated in the skill body and in the artifact. This is what keeps ARCH-1 intact.
3. **The committed baseline is resolved with one pickaxe query,** not by date arithmetic:
   the most recent commit that changed the occurrence count of the milestone's exact
   `**Commitment:** Committed …` line in `docs/roadmap/INDEX.md`. Because the line is
   verified present at the candidate revision first, the most recent count change is
   necessarily its addition.
4. **The assessment artifact is markdown with a fixed, greppable block grammar,** seeded from
   a new `templates/milestone-assessment.md`. `write-roadmap` must re-derive handoff values
   from it, so it has to parse deterministically — the same reason the roadmap has `S1`–`S7`.
5. **`Deferred` is a non-terminal disposition.** It withholds the close and leaves the
   assessment open. Only `Accepted` and `Overridden` are terminal, and only they freeze.
6. **Disposition values accumulate as a dated history** inside the assessment block, so a
   `Deferred → Accepted` path stays legible without appending a whole new assessment.
7. **The skill lives at `skills/track/assess-milestone/`,** beside `check-roadmap`,
   `sync-spec`, and `amend` — the lifecycle-tracking category.
8. **No new ADR.** [ADR 0002](../../adr/0002-outcome-truth-outside-the-roadmap.md) already
   records the artifact-location decision. The human-disposition gate fails the ADR gate's
   "surprising without context" limb — in this codebase every terminal verdict is already
   human (`write-roadmap`'s approval gate, `finish-branch`, `record-decision`), so this is
   the house pattern rather than a departure from it.

## Architecture

### Shared roadmap findings reference

Satisfies: ASSESS-5.3, ASSESS-5.4
Respects: ARCH-1, ARCH-3
Reuse: existing — extends the `templates/` shared-rules mechanism that already carries
`S1`–`S7` for `write-roadmap` and `check-roadmap` (rung 2)

New file `templates/roadmap-findings.md`, opening with a line naming itself authoritative and
naming its two readers — the shape `skills/review/allocate-attention/references/signals.md`
already uses. It carries the `R1`–`R11` table verbatim as it exists in
`check-roadmap/SKILL.md:25-37` today (code, tier, condition, withholds), the rule statements
from `:117-130`, and the withholding set `{R2, R4, R9, R10, R11}` stated once as a named set
so both readers cite it rather than re-deriving it.

Pure markdown, no executable content, so ARCH-3 holds for consumer repos. The move is
byte-preserving on rule semantics; ASSESS-5.4 is the guard that proves it.

### `check-roadmap` changes

Satisfies: ASSESS-5.2, ASSESS-5.5, ASSESS-5.6
Respects: ARCH-1, ARCH-5
Reuse: existing — edits `skills/track/check-roadmap/SKILL.md` in place (rung 2)

Two edits, both narrow:

1. **Rules dereferenced.** The inline `R1`–`R11` table and rule list are replaced by a
   pointer to `templates/roadmap-findings.md`, exactly as the skill already points at
   `templates/roadmap-INDEX.md` for `S1`–`S7` ("That block is authoritative — read the rules
   there, do not restate them", `:55-56`). The six passes, the ladder, the output shape, and
   the `<NON-NEGOTIABLE>` block are untouched.
2. **One ladder row added.** The priority ladder gains a row between the current rows 7 and
   8: *a `Committed` milestone whose members are all bound and whose bound features' `Status:`
   are all `Shipped` → run `/assess-milestone` for that `MILE-N`*. Rows 8 and 9 shift down to
   9 and 10. Ladder rows are positional, not identifiers, so renumbering repoints nothing.
   The row **names** the skill for the user to run rather than invoking it, which is both
   ARCH-5 and what `scripts/lint-handoffs.py` will accept.

The ladder is specified in RMAP's own `design.md` under RMAP-3.10, so that file is edited
too — the ladder has one statement, and leaving RMAP's copy stale would make two.

### Scope resolution pass

Satisfies: ASSESS-1.1, ASSESS-1.2, ASSESS-1.3, ASSESS-1.4, ASSESS-1.5, ASSESS-1.6, ASSESS-1.7, ASSESS-1.8, ASSESS-1.9, ASSESS-1.10, ASSESS-1.11, ASSESS-1.12
Respects: ARCH-1, ARCH-2, ARCH-5
Reuse: existing — reuses `check-roadmap`'s membership and binding extraction verbatim from
the shared reference (rung 2)

The opening section of `skills/track/assess-milestone/SKILL.md`. Fixed passes, in order,
each a `grep`/`git`/file read whose output feeds the next:

```bash
# 0. Layer presence — absent is a clean exit, never a complaint (ARCH-2)
test -f docs/roadmap/INDEX.md || exit_reporting_no_milestone_scope

# 1. Milestone identity — live blocks only, strike spans deleted first
sed -E 's/~~[^~]*~~//g' docs/roadmap/INDEX.md | grep -nE '^## MILE-[0-9]+'

# 2. Membership and slots for the resolved milestone's block
grep -nE '^- \*\*ROAD-[0-9]+\*\*|^\*\*(Outcome|Goals|Depends-on|Commitment|Closed|Deferred|Blockers):' \
  docs/roadmap/INDEX.md

# 3. Bindings
grep -nE '^\| [A-Z][A-Z0-9]{1,11} \|' docs/specs/INDEX.md

# 4. Candidate closing revision
git rev-parse HEAD

# 5. Committed baseline — one pickaxe query, count-change on the exact line
git log -1 --format=%H -S "$COMMITMENT_LINE" -- docs/roadmap/INDEX.md

# 6. Roadmap revision assessed, and whether the working tree modifies it
git log -1 --format=%H -- docs/roadmap/INDEX.md
git status --porcelain -- docs/roadmap/INDEX.md
```

**Baseline resolution (ASSESS-1.8).** `$COMMITMENT_LINE` is the milestone's exact
`**Commitment:** Committed <date>` line as it reads at HEAD. Pass 5 runs only after the line
is confirmed present in the file at the candidate revision; given presence, the most recent
count change for that string must be its addition, so `-1` yields the single introducing
commit. Empty output means the state is untracked or was added and removed inside one commit
— both withhold under ASSESS-1.10. The query is `O(1)` in members, satisfying ASSESS-6.1.

**Roadmap revision (ASSESS-2.2).** Pass 6 records the revision and a `Working tree:
clean|modified` marker beside it. A modified working tree is recorded, not gated — the
requirements fix the withholding set and this design adds no rule to it.

**Structural preconditions (ASSESS-1.11, ASSESS-1.12).** The withholding set
`{R2, R4, R9, R10, R11}` is read from the shared reference and evaluated, then filtered to
findings **relevant to the resolved milestone**: one naming that `MILE-N`, one of its members,
or a goal it cites. `R2` names a goal no milestone cites and so is relevant by definition
never — it is evaluated and filtered out, stated here so a reader does not read its absence as
an omission.

**Untrusted input (ASSESS-6.2).** `MILE-N` matches `^MILE-[0-9]+$` and revisions match
`^[0-9a-f]{40}$` before either reaches a command; every interpolated value is passed as a
single argument after `--`.

### Evidence gathering and judgment

Satisfies: ASSESS-3.1, ASSESS-3.2, ASSESS-3.3, ASSESS-3.6, ASSESS-3.7, ASSESS-3.8, ASSESS-3.9, ASSESS-3.10, ASSESS-3.11, ASSESS-3.12
Respects: ARCH-1, ARCH-5, ARCH-6
Reuse: existing — goal and disposition extraction reuse `check-roadmap`'s passes 1 and 3
via the shared reference (rung 2)

The judged section, explicitly fenced off from the mechanical passes above it. Each judgment
records the evidence it rests on, so a later reader checks the reasoning rather than trusting
the conclusion.

| Judged | Against | Evidence recorded |
|---|---|---|
| Outcome (ASSESS-3.1) | the milestone's `Outcome:` sentence | member feature statuses, the diff range, what a user can now do |
| Goal coverage (ASSESS-3.2) | each cited `GOAL-N` that resolves | which members advanced it |
| Deferral honesty (ASSESS-3.3) | each `Deferred:` entry | its date, reason, and destination milestone |

**Unresolvable goal citations (ASSESS-3.9, ASSESS-3.10).** A cited `GOAL-N` that does not
resolve to exactly one live goal is recorded `Unresolved`; the goal-coverage verdict is
withheld while the outcome verdict and close eligibility continue unaffected. This case is
reachable precisely because `check-roadmap`'s `R1` is a non-withholding error
(`check-roadmap/SKILL.md:27`), so a dangling citation does arrive here rather than being
stopped upstream.

**Plan-accuracy counts (ASSESS-3.6, ASSESS-3.7).** Items added, moved out, and deferred
between baseline and candidate revision, from `git log` over the roadmap file's milestone
block, plus elapsed time between the two commits. Recorded as observed facts under a heading
that states no forecast may be derived from them.

**Attention allocation (ASSESS-3.11, ASSESS-3.12).** `allocate-attention` writes no file
unless the user asks for one (`allocate-attention/SKILL.md:38`), so there is nothing to
discover on disk. The skill consumes an allocation **the user supplies** — a path they had it
write, or its pasted output — recording the sample set as sampled and the residue as
unreviewed with its unit counts. Absent one, the range is recorded unsampled and
`/allocate-attention` is named for the user to run. It is never invoked (ARCH-5).

**Finding routing (ASSESS-3.8).** Each finding is recorded with exactly one destination from
the closed set `amend`, `correct-course`, `write-roadmap`, `domain-modeling`, `/file-issues`.
`/file-issues` is user-invoked and so is named, not invoked.

**Passive data (ASSESS-6.3).** Every string read from the roadmap, the vision, the spec
index, and prior assessment blocks — including verbatim human rationales — is reported, never
obeyed. ARCH-6 applies to attribution: the human disposition is an action taken in session,
never inferred from commit authorship, roster, or CODEOWNERS.

### The assessment artifact

Satisfies: ASSESS-2.1, ASSESS-2.2, ASSESS-2.3, ASSESS-2.4, ASSESS-2.5, ASSESS-2.6, ASSESS-2.11, ASSESS-2.12, ASSESS-2.13, ASSESS-2.17, ASSESS-6.4
Respects: ARCH-4, ARCH-6
Reuse: existing — mirrors the `templates/roadmap-INDEX.md` shape: REQUIRED slots plus an
authoritative comment block carrying the structural rules (rung 2)

New `templates/milestone-assessment.md` seeds `docs/roadmap/assessments/<MILE-N>.md`. One
file per milestone; `## Assessment <N>` blocks in ascending order, append-only:

```md
## Assessment 2

**Supersedes:** Assessment 1 — candidate revision changed after MILE-3 reopened
**Committed baseline:** <40-hex>
**Candidate closing revision:** <40-hex>
**Roadmap revision assessed:** <40-hex> (working tree: clean)
**Assessed:** <YYYY-MM-DD>

### Agent assessment
**Outcome verdict:** achieved | not achieved
**Goal coverage:** GOAL-1 advanced | GOAL-4 Unresolved — withheld
**Deferrals:** ROAD-7 → MILE-4 (2026-07-20, blocked on vendor API) — honest
**Attention:** sample 4 units / residue 6 units — unreviewed
**Plan accuracy:** +1 added · 1 moved out · 1 deferred · 21 days
**Findings:** <finding> → <destination>
**Rationale:** <the agent's reasoning>

### Human disposition
**Current:** Accepted
**Close decision:** Close
**History:**
- 2026-07-26 Pending
- 2026-07-27 Deferred — "want to see the vendor fix land first"
- 2026-07-28 Accepted / Close — "good enough, ship it"
```

The block's structural rules live in the template's comment block, authoritative in the same
way `S1`–`S7` are, so both this skill and `write-roadmap` validate against one statement:
every assessment ordinal unique and ascending; both revision fields full 40-hex; exactly one
`### Agent assessment` and one `### Human disposition` per block; a terminal `**Current:**`
accompanied by a `**Close decision:**`; and a `**Supersedes:**` line on every block after the
first.

Earlier blocks are never rewritten (ASSESS-2.3). A successful close writes nothing further
(ASSESS-2.6). Verbatim human rationale is quoted (ASSESS-2.13) and remains passive data on
every later read. **Write-failure handling (ASSESS-6.4):** the file is written *before* close
eligibility is evaluated, and a failed write reports and withholds — the gate can never open
on evidence that was not durably recorded.

### Disposition state machine

Satisfies: ASSESS-2.7, ASSESS-2.8, ASSESS-2.9, ASSESS-2.10, ASSESS-2.14, ASSESS-2.15, ASSESS-2.16, ASSESS-4.15, ASSESS-4.16, ASSESS-4.17, ASSESS-4.18, ASSESS-4.19, ASSESS-4.20
Respects: ARCH-6
Reuse: none — new state table (rung 7); no existing skill models a resumable two-party
verdict, and the four states plus two transitions are smaller than anything reusable

Stated once, as a table in `SKILL.md` and enforced by the template's rules:

| Current | Terminal | Effective verdict | Close eligibility | May change to |
|---|---|---|---|---|
| `Pending` | no | none | withheld | `Deferred`, `Accepted`, `Overridden` |
| `Deferred` | no | none | withheld | `Accepted`, `Overridden` |
| `Accepted` | yes | the agent's recorded verdict | `Close` decision → eligible; `Hold` → withheld | nothing |
| `Overridden` | yes | the human's replacement verdict | `Close` decision → eligible; `Hold` → withheld | nothing |

Every terminal transition also records a close decision of `Close` or `Hold` (ASSESS-4.18),
and each transition appends a dated history entry rather than overwriting (ASSESS-2.16) — the
latest entry is the current value. Freezing applies only to terminal values (ASSESS-2.9), so
`Deferred` genuinely reopens.

**Validity is SHA equality, not recency (ASSESS-2.8, ASSESS-2.10, ASSESS-2.17).** A
disposition or close request carries the closing revision it means. Equal to the recorded
candidate → it lands on that block. Different → the block is reported superseded and a new
`Assessment` block is required. Commits landing on HEAD in between change nothing; only a
different *requested* revision does.

### Close gate

Satisfies: ASSESS-4.1, ASSESS-4.2, ASSESS-4.3, ASSESS-4.4, ASSESS-4.5, ASSESS-4.10, ASSESS-4.11, ASSESS-4.14
Respects: ARCH-1, ARCH-5
Reuse: existing — hands off to `write-roadmap`, the model-invocable owner of every roadmap
write (rung 2)

Close eligibility is the conjunction of two independent things, evaluated in this order so a
mechanical failure never depends on a human being present:

1. **Mechanical eligibility** (ASSESS-4.2) — same `MILE-N`, same candidate revision, every
   member binding resolved, baseline resolved. Non-overridable: no disposition rescues it
   (ASSESS-4.3).
2. **A permitting disposition** — terminal, with close decision `Close` (ASSESS-4.19).

A negative effective verdict with a `Close` decision proceeds (ASSESS-4.10); the verdict stays
in the file permanently. When both hold, the skill hands `write-roadmap` the `MILE-N`, the
assessment ordinal, the effective verdict, and the candidate SHA (ASSESS-4.5) — a hand-off to
a model-invocable skill, which ARCH-5 permits and `lint-handoffs.py` allows.

**Single invocation, with an honest exception** (ASSESS-4.11, ASSESS-4.14). When the human
disposes during the invocation that wrote the assessment, everything completes in one run.
When they do not, the invocation ends with the block recorded and non-terminal; a later run
resolves the same `MILE-N`, finds the existing block, and — if the requested revision matches
— records the disposition against it without re-judging anything.

### `write-roadmap` changes

Satisfies: ASSESS-4.6, ASSESS-4.7, ASSESS-4.8, ASSESS-4.9, ASSESS-4.12, ASSESS-4.13, ASSESS-5.7, ASSESS-5.8, ASSESS-5.13
Respects: ARCH-1, ARCH-4
Reuse: existing — extends the **Update** mode's "Record a closure" step already at
`write-roadmap/SKILL.md:106-108` (rung 2)

The "Record a closure" step becomes gated. On any request that would move a milestone's
`Commitment:` to `Closed`:

1. **Require a handoff** (ASSESS-4.12). Without one, refuse and name `/assess-milestone` for
   the user to run. This is the behavior change with the widest blast radius: it applies in
   every repo, including one that never adopts this skill.
2. **Re-derive, do not trust** (ASSESS-4.13). Read
   `docs/roadmap/assessments/<MILE-N>.md`, locate the block at the referenced ordinal, and
   read the milestone, the candidate SHA, the current disposition, the effective verdict, and
   the close decision **out of the file**. The handoff's values are compared against what was
   read; they are never the source (ARCH-1 — an exact file-read pass, no judgment).
3. **Verify five properties** (ASSESS-4.6): same `MILE-N`, the ordinal exists, same 40-hex
   SHA, disposition terminal, and the verdict plus close decision matching what the handoff
   asserts. Any mismatch refuses and reports (ASSESS-4.7).
4. **Record** the SHA read from the file, verbatim, into `Closed:` (ASSESS-4.8) — the file's
   value, not the handoff's, so a divergence cannot survive as a written fact.
5. **Then run the existing approval gate** (ASSESS-5.13). The assessment gate is additive: it
   precedes RMAP-1.17, never replaces it. For every update that does not close a milestone,
   the gate is reached exactly as before (ASSESS-5.7), and `docs/specs/INDEX.md` stays
   untouched throughout (ASSESS-5.8).

`write-roadmap` never writes the assessment file (ASSESS-4.9) — reading it is the whole of its
involvement.

### Registration, boundaries, and safety

Satisfies: ASSESS-5.1, ASSESS-5.9, ASSESS-5.10, ASSESS-5.11, ASSESS-5.12, ASSESS-6.1, ASSESS-6.2, ASSESS-6.3
Respects: ARCH-3, ARCH-5
Reuse: existing — follows the registration path every skill in the set already uses (rung 2)

`skills/track/assess-milestone/SKILL.md` carries `disable-model-invocation: true`
(ASSESS-5.1). Registration touches `AGENTS.md` in the same three places `check-roadmap`
occupies — the user-invoked list (`:76`), the `track/` line of the repo-layout comment
(`:249`), and the `track` category row (`:338`) — plus a guide page at
`docs/guide/skills/assess-milestone.md`, matching what `check-roadmap` and `write-roadmap`
did.

Boundaries held by construction and checked mechanically:

- `docs/roadmap/INDEX.md` is modified only through `write-roadmap` (ASSESS-5.9) — this skill
  has no write step targeting it.
- `allocate-attention` is named, never invoked (ASSESS-5.10); `scripts/lint-handoffs.py`
  fails the build on any invoking phrasing.
- `trace` is untouched, so its `CODE-N.M`/`ARCH-N` scope is unchanged (ASSESS-5.11), already
  locked by `tests/test_trace_scope.py`.
- `record-decision`'s caller set is untouched (ASSESS-5.12); this feature routes findings to
  five destinations and that skill is not among them.

Performance (ASSESS-6.1): one full read each of the roadmap, the spec index, the vision, and
the assessment file, plus a fixed six `git` invocations — none of them per-member. Injection
safety (ASSESS-6.2) and passive data (ASSESS-6.3) are as stated in the scope-resolution and
judgment sections.

## Seams for testing

The repo's established model has two seam kinds, and RMAP uses both: Python `unittest` files
under `tests/` assert *static structure* (a markdown skill has no entry point Python can
call), and scenario markdown carries *behavior* coverage as greppable bare ID tokens, run by
pointing a fresh agent at a fixture repo. No new seam **kind** is introduced; the two new
files are new instances of existing kinds, which the repo requires one of each per feature.

| Seam | Kind | Covers |
|---|---|---|
| `tests/test_check_roadmap_rules.py` (existing, extended) | unit | ASSESS-5.3, ASSESS-5.4 |
| `tests/roadmap/scenarios-check-roadmap.md` (existing, extended) | scenario | ASSESS-5.2, ASSESS-5.5, ASSESS-5.6 |
| `tests/test_assessment_artifact.py` (new) | unit | ASSESS-2.1, ASSESS-2.2, ASSESS-2.3, ASSESS-2.4, ASSESS-2.14, ASSESS-2.15, ASSESS-2.16, ASSESS-4.18, ASSESS-5.1 |
| `tests/milestone-assessment/scenarios-scope.md` (new) | scenario | ASSESS-1.1, ASSESS-1.2, ASSESS-1.3, ASSESS-1.4, ASSESS-1.5, ASSESS-1.6, ASSESS-1.7, ASSESS-1.8, ASSESS-1.9, ASSESS-1.10, ASSESS-1.11, ASSESS-1.12, ASSESS-6.1, ASSESS-6.2 |
| `tests/milestone-assessment/scenarios-judgment.md` (new) | scenario | ASSESS-3.1, ASSESS-3.2, ASSESS-3.3, ASSESS-3.6, ASSESS-3.7, ASSESS-3.8, ASSESS-3.9, ASSESS-3.10, ASSESS-3.11, ASSESS-3.12, ASSESS-6.3 |
| `tests/milestone-assessment/scenarios-gate.md` (new) | scenario | ASSESS-2.5, ASSESS-2.6, ASSESS-2.7, ASSESS-2.8, ASSESS-2.9, ASSESS-2.10, ASSESS-2.11, ASSESS-2.12, ASSESS-2.13, ASSESS-2.17, ASSESS-4.1, ASSESS-4.2, ASSESS-4.3, ASSESS-4.4, ASSESS-4.5, ASSESS-4.10, ASSESS-4.11, ASSESS-4.14, ASSESS-4.15, ASSESS-4.16, ASSESS-4.17, ASSESS-4.19, ASSESS-4.20, ASSESS-6.4 |
| `tests/milestone-assessment/scenarios-handoff.md` (new) | scenario | ASSESS-4.6, ASSESS-4.7, ASSESS-4.8, ASSESS-4.9, ASSESS-4.12, ASSESS-4.13, ASSESS-5.7, ASSESS-5.8, ASSESS-5.9, ASSESS-5.10, ASSESS-5.11, ASSESS-5.12, ASSESS-5.13 |

Fixtures follow `tests/roadmap/fixtures/<case>/` exactly: a `roadmap-INDEX.md`,
`specs-INDEX.md`, `vision.md`, any `requirements.md`, and now an `assessments/<MILE-N>.md`,
assembled into a throwaway repo per case.

## Coverage check

All 76 live requirement IDs appear in exactly one `Satisfies:` line. Section totals: shared
reference 2, `check-roadmap` 3, scope resolution 12, judgment 10, artifact 11, state machine
13, close gate 8, `write-roadmap` 9, registration 8 — 76.

Deliberately unmapped: none.

**Retired upstream.** `ASSESS-3.4` and `ASSESS-3.5` are retired by strikethrough and replaced
by `ASSESS-3.11` and `ASSESS-3.12`. Their premise was false: they read "WHERE an
`allocate-attention` allocation … exists", implying a discoverable artifact, but
`allocate-attention/SKILL.md:38` ends with *"no file exists unless they asked for one"* — an
allocation is conversational by default, with no defined path or format. The replacements turn
on the user **supplying** one. This correction is reported here rather than absorbed silently,
because a `Satisfies:` line pointing at a false premise would carry the error into the plan
and the code.
