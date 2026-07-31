# Scenarios — `assess-milestone`, scope resolution

Behavior coverage for the mechanical half of the skill. `tests/test_assessment_artifact.py`
asserts the static contracts (template slots, disposition values, frontmatter); it cannot
assert what the skill *emits*, because a markdown skill has no entry point Python can call.
That is what these scenarios are for. IDs are bare greppable tokens.

Run a scenario by assembling a throwaway repo from
`tests/milestone-assessment/fixtures/<case>/` — `roadmap-INDEX.md` → `docs/roadmap/INDEX.md`,
`specs-INDEX.md` → `docs/specs/INDEX.md`, `vision.md` → `docs/product/vision.md`, and any
`requirements.md` under the spec folder its INDEX row names — then `git init && git add -A &&
git commit` unless the case says otherwise, then running `/assess-milestone` for `MILE-1` and
comparing against that case's `expected.txt`.

---

## S-AM-1 — No roadmap layer is a clean exit

**Setup.** Fixture `no-roadmap`: a spec index and a vision, no `docs/roadmap/INDEX.md`.

**Expect.**
- The run reports that the project has no milestone scope and stops.
- No file is written — in particular no `docs/roadmap/assessments/` directory appears.
- No outcome verdict is produced, and no complaint is raised. A project running short
  features through `prove-claim`, `inspect-change`, `validate-feature`, and `realign-spec` is never
  obliged to create a `MILE-N`. Covers ASSESS-1.1.

## S-AM-2 — Milestone identity resolves to exactly one live block

**Setup.** Fixture `clean-close`.

**Expect.** `MILE-1` resolves to exactly one live, non-struck-through block. Covers
ASSESS-1.2.

**Setup.** The same fixture with a second `## MILE-1 — Capture (old)` block added.

**Expect.** The run reports the ambiguity and withholds the outcome verdict — it does not
pick the first, the last, or the longer block. Covers ASSESS-1.3.

**Setup.** The same fixture with the milestone struck through as
`## ~~MILE-1~~ — superseded by MILE-2`.

**Expect.** Strike spans are deleted before matching, so the retired milestone does not
resolve, and the run reports the ambiguity rather than assessing a retired milestone.
Covers ASSESS-1.2, ASSESS-1.3.

## S-AM-3 — Membership excludes what the Deferred slot lists

**Setup.** Fixture `clean-close` with a second member `- **ROAD-9** later-thing` and
`**Deferred:** ROAD-9 later-thing → MILE-2 (2026-03-05, waiting on vendor)`.

**Expect.** Membership is `{ROAD-1}`. `ROAD-9` is not assessed as a member — it left, and the
`Deferred:` slot is the record that it did. Covers ASSESS-1.4.

## S-AM-4 — Each member binds to exactly one feature code

**Setup.** Fixture `clean-close`.

**Expect.** `ROAD-1` resolves to exactly one code, `CAP`. Covers ASSESS-1.5.

**Setup.** Fixture `ambiguous-binding`: `CAP` and `CAP2` both bind `ROAD-1`.

**Expect.** The run reports the unresolved binding and withholds the outcome verdict. Two
claims is not a binding, and the more recently added row is not a tie-break. Covers
ASSESS-1.6.

**Setup.** Fixture `clean-close` with the `specs-INDEX.md` row's `Roadmap item` cell emptied.

**Expect.** The member resolves to no feature code — reported, verdict withheld. Covers
ASSESS-1.6.

## S-AM-5 — A moved item is resolved by its unchanged ID

**Setup.** Fixture `clean-close`, then move `ROAD-1` out of `MILE-1` into a new `MILE-2`
block, leaving its `specs-INDEX.md` binding untouched, and assess `MILE-2`.

**Expect.** The binding resolves by ID. Position within the roadmap carries build order, not
identity, so a move renumbers nothing and re-binds nothing. Covers ASSESS-1.7.

## S-AM-6 — Baseline and candidate are SHAs, not dates

**Setup.** Fixture `clean-close`, committed.

**Expect.**
- The candidate closing revision is one full 40-hex SHA, and every value recorded in the run
  refers to that same revision — it does not change if `HEAD` moves mid-run. Covers
  ASSESS-1.9.
- The committed baseline is the full SHA of the single commit that introduced the milestone's
  current `**Commitment:** Committed 2026-03-01` line, found with one pickaxe query over
  `docs/roadmap/INDEX.md`. Covers ASSESS-1.8.

**Setup.** The same fixture where a *second* milestone was committed on the same date.

**Expect.** The two baselines differ. A date cannot distinguish them; a SHA does. Covers
ASSESS-1.8.

**Setup.** Fixture `unresolvable-baseline`: assembled but never committed, so the
`Commitment` line is present in the working tree and absent from history.

**Expect.** The pickaxe returns empty; the run reports the failure and withholds the outcome
verdict rather than falling back to a date or to `HEAD`. Covers ASSESS-1.10.

## S-AM-7 — Structural preconditions come before judgment

**Setup.** Fixture `withholding-r10`: `docs/specs/INDEX.md` says `Approved`, the feature's
`requirements.md` says `Shipped`.

**Expect.**
- The withholding set `{R2, R4, R9, R10, R11}` is read from `templates/roadmap-findings.md`
  and evaluated **before** any outcome judgment. Covers ASSESS-1.11.
- `R10` fires, is relevant to `MILE-1` (it names a member's feature), and the outcome verdict
  is withheld with that finding reported in its place. Covers ASSESS-1.12.
- The run names `/status-roadmap` for the user if they want the repo-wide picture, and does
  not run it — `scripts/lint-handoffs.py` enforces this. Covers ASSESS-1.11.

**Setup.** Fixture `clean-close` with a live `GOAL-2` that no milestone cites and no
disposition — an `R2`.

**Expect.** `R2` is evaluated and filtered out as not relevant to `MILE-1`: by its own
condition it names a goal *no* milestone cites, so it can never name one this milestone
cites. The verdict is not withheld on it. Covers ASSESS-1.12.

## S-AM-8 — Bounded cost

**Setup.** Fixture `scale-50-members`.

**Expect.** One full read each of the roadmap, the spec index, the vision, and the assessment
file, plus the fixed `git` calls — no command runs once per member, and the run's cost is
indistinguishable from the two-member case. Covers ASSESS-6.1.

## S-AM-9 — Untrusted input

**Setup.** Fixture `clean-close`, assessed with a milestone argument of `--output=/tmp/x`,
then with `MILE-1; rm -rf /`, then with `$(whoami)`.

**Expect.** Each fails the `^MILE-[0-9]+$` shape check and is rejected before reaching any
command. Nothing is executed, nothing is written. Covers ASSESS-6.2.

**Setup.** The same fixture with a revision argument of `--upload-pack=evil` and one of
`HEAD`.

**Expect.** Both fail `^[0-9a-f]{40}$` and are rejected. Every value that does pass is handed
to `git` as a single non-option argument after `--`. Covers ASSESS-6.2.

## S-AM-10 — Invocation boundary

**Expect.**
- `skills/track/assess-milestone/SKILL.md` frontmatter carries
  `disable-model-invocation: true`, so no agent can fire the gate on its own. Covers
  ASSESS-5.1.
- `/status-roadmap` names this skill in ladder row 8 rather than running it, and this skill
  names `/status-roadmap` back rather than running it. Neither direction is an invocation.
  Covers ASSESS-5.1.
