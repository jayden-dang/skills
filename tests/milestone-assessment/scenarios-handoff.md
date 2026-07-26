# Scenarios — `write-roadmap`, assessment handoff verification

Behavior coverage for the gated closure step and the boundaries this feature must not cross.
Assemble fixtures as `scenarios-scope.md` describes. IDs are bare greppable tokens.

---

## S-AM-29 — Five properties verified before `Closed` is written

**Setup.** Fixture `terminal-assessment`: block 1, candidate `aaa…`, `Accepted` + `Close`,
verdict `achieved`. A handoff arrives naming `MILE-1`, ordinal 1, verdict `achieved`, SHA
`aaa…`.

**Expect.** All five are verified against the block read from
`docs/roadmap/assessments/MILE-1.md` before anything is written: same `MILE-N`, ordinal
exists, SHA equal, disposition terminal, verdict and close decision matching. Covers
ASSESS-4.6.

**Setup.** The same handoff against an assessment whose current disposition is `Pending`.

**Expect.** Refused on property 4. A `Pending` block authorises nothing, however confident the
handoff sounds. Covers ASSESS-4.6.

**Setup.** A handoff naming ordinal 3 in a file holding two blocks.

**Expect.** Refused on property 2. Covers ASSESS-4.6.

**Setup.** An assessment file violating `A2` (a 7-character SHA) or `A5` (terminal `Current:`
with no `Close decision:`).

**Expect.** Refused before verification proper — an unparseable assessment cannot authorise
anything. Covers ASSESS-4.6.

## S-AM-30 — Mismatch refuses and says which value disagreed

**Setup.** Fixture `handoff-mismatch`: the block says candidate `aaa…` and verdict
`achieved`; the handoff asserts `bbb…` and `not achieved`.

**Expect.** The close is refused, the report names which values disagreed, and `Closed:` is
never written. Covers ASSESS-4.7.

## S-AM-31 — The file wins over the handoff

**Setup.** Fixture `handoff-mismatch`.

**Expect.**
- Every verified value is **re-derived by reading the assessment file**; the handoff's values
  are treated as claims to check, never as facts to trust. Covers ASSESS-4.13.
- A handoff asserting a verdict the file contradicts loses. The file is the record; the
  handoff is hearsay. Covers ASSESS-4.13.

**Setup.** A valid handoff whose SHA matches the file.

**Expect.** The `Closed:` slot receives the SHA **read from the file**, verbatim — not the
handoff's copy of it, even though they are equal here. Where the two could ever diverge, only
one of them is the record. Covers ASSESS-4.8.

## S-AM-32 — No handoff, no close

**Setup.** Fixture `clean-close` with no assessment file at all, and a request to set
`MILE-1`'s `Commitment:` to `Closed`.

**Expect.**
- Refused, with `/assess-milestone` named for the user to run — named, never run, since it is
  user-invoked. Covers ASSESS-4.12.
- This holds in a repo that has never run `assess-milestone`. The gate is not opt-in: it is
  the reason a closed milestone means something. Covers ASSESS-4.12.

## S-AM-33 — `write-roadmap` reads the assessment and writes only the roadmap

**Setup.** A verified close.

**Expect.** No assessment block is appended, no confirmation is stamped, and the assessment is
not re-run. `write-roadmap` reads that file and writes only `docs/roadmap/INDEX.md`. Covers
ASSESS-4.9.

## S-AM-34 — The approval gate is unchanged, and still runs

**Setup.** A reorder of the milestone table, a reworded `Outcome:`, a new `Planned` milestone,
and a deferral — none of them a closure.

**Expect.** Each reaches the RMAP-1.17 approval gate exactly as before: material change to an
`Approved` roadmap demotes it to `Draft`, the file is presented whole, and `Status: Approved`
is written only on explicit user approval. The assessment gate does not fire. Covers
ASSESS-5.7.

**Setup.** A verified close.

**Expect.** The approval gate runs **after** the assessment gate passes. The assessment gate
is additive and never replaces it — a verified handoff is not a substitute for the user
approving the resulting roadmap. Covers ASSESS-5.13.

**Setup.** Any of the above.

**Expect.** `docs/specs/INDEX.md` is unmodified throughout. Feature codes belong to
`write-requirements`, and closing a milestone does not touch them. Covers ASSESS-5.8.

## S-AM-35 — Boundaries held by construction

**Expect.**
- `assess-milestone` modifies `docs/roadmap/INDEX.md` only through `write-roadmap` — it has no
  write step targeting that file, and the closure it wants is expressed as a handoff. Covers
  ASSESS-5.9.
- `/allocate-attention` is named for the user, never run from inside the skill;
  `scripts/lint-handoffs.py` fails the build on any invoking phrasing, and did so once during
  this feature's own implementation. Covers ASSESS-5.10.
- `trace` still checks referential integrity for `CODE-N.M` and `ARCH-N` only. This feature
  adds no ID namespace — an assessment is identified by its milestone and its ordinal — and
  `tests/test_trace_scope.py` locks the scope. Covers ASSESS-5.11.
- `record-decision`'s caller set stays closed to `finish-branch` and `release`. It is not
  among this feature's five finding destinations, and a milestone assessment is neither of
  its two callers. Covers ASSESS-5.12.
