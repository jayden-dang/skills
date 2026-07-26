# Scenarios — `assess-milestone`, recording and the close gate

Behavior coverage for the artifact, the disposition state machine, and close eligibility.
Assemble fixtures as `scenarios-scope.md` describes; a case carrying `assessments-MILE-1.md`
maps it to `docs/roadmap/assessments/MILE-1.md`. IDs are bare greppable tokens.

---

## S-AM-18 — The block is written before the gate is evaluated

**Setup.** Fixture `clean-close`, with `docs/roadmap/assessments/` made unwritable.

**Expect.** The write failure is reported and close eligibility is **withheld**. The gate
never opens on evidence that was not durably recorded — a verdict that lives only in the
conversation is the failure this file exists to prevent. Covers ASSESS-6.4.

**Setup.** Fixture `clean-close`, writable.

**Expect.** A fresh assessment is written with `Current: Pending`. Covers ASSESS-2.7.

## S-AM-19 — Append-only at the assessment-event level

**Setup.** Fixture `pending-assessment`, re-run against the **same** candidate SHA with no
change in evidence.

**Expect.** No further `Assessment` block is appended. A re-run is not a new event. Covers
ASSESS-2.5.

**Setup.** Fixture `superseded-revision`: a close requested against a SHA differing from the
recorded candidate.

**Expect.** The recorded assessment is reported **superseded** and a new `Assessment` block is
required. Block 1 keeps its verdict and its history untouched — it simply no longer describes
what is being closed. Covers ASSESS-2.10, ASSESS-2.5.

**Setup.** Any fixture where a second block is appended.

**Expect.** The new block carries `Supersedes: Assessment 1` and the reason for reassessment,
and block 1 is byte-identical to before. Covers ASSESS-2.3, ASSESS-2.4.

**Setup.** Fixture `terminal-assessment` after a close completes successfully.

**Expect.** The assessment file is unchanged — no confirmation block, no "closed" stamp. The
disposition that authorised the close is already the record. Covers ASSESS-2.6.

## S-AM-20 — Validity is SHA equality, not recency

**Setup.** Fixture `pending-assessment` (candidate `aaa…`), with several unrelated commits
landed on `HEAD` afterwards. A disposition arrives naming `aaa…`.

**Expect.** It lands on that same block. A moved `HEAD` does not stale an assessment: the
assessment is about a revision, not about being the newest thing in the repo. Covers
ASSESS-2.8, ASSESS-2.17.

**Setup.** The same fixture, disposition naming `bbb…`.

**Expect.** Superseded; new block required. Covers ASSESS-2.10.

## S-AM-21 — Terminal freezes, Deferred does not

**Setup.** Fixture `terminal-assessment` (`Current: Accepted`), with a second disposition
attempted against assessment 1.

**Expect.** Rejected. Terminal values freeze the field. Covers ASSESS-2.9.

**Setup.** Fixture `deferred-assessment` (`Current: Deferred`), with `Accepted / Close`
arriving later against the same SHA.

**Expect.**
- Accepted. `Deferred` is non-terminal, so "not yet" stays reversible while "yes" and "no but
  close anyway" do not. Covers ASSESS-4.20.
- The transition **appends** a dated entry to `History:`; the `Deferred` entry above it is
  left intact, and the latest entry is the current disposition. Covers ASSESS-2.16.

## S-AM-22 — Attribution survives an override

**Setup.** Fixture `pending-assessment`, where the human disagrees with the agent's
`achieved` verdict and records `Overridden` with `not achieved` and a rationale.

**Expect.**
- `### Agent assessment` is **unchanged**, including its verdict and rationale. Covers
  ASSESS-2.12.
- The replacement verdict sits under `### Human disposition`, attributed separately. An
  overridden assessment is evidence about the judgment, not a mistake to erase. Covers
  ASSESS-2.11, ASSESS-2.12.
- The human's rationale is recorded verbatim, not paraphrased or summarised. Covers
  ASSESS-2.13.
- Acceptance in the non-override case likewise leaves the agent's reasoning attributed to the
  agent — adoption is not authorship. Covers ASSESS-2.11.

## S-AM-23 — Effective verdict by disposition

**Setup.** Fixture `terminal-assessment` (`Accepted`).

**Expect.** The effective verdict is the agent's recorded verdict. Covers ASSESS-4.15.

**Setup.** The same fixture with `Current: Overridden` and a replacement verdict.

**Expect.** The effective verdict is the human's replacement. Covers ASSESS-4.16.

**Setup.** Fixtures `pending-assessment` and `deferred-assessment`.

**Expect.** No effective verdict exists at all — not a provisional one, not the agent's
standing in until someone objects. Covers ASSESS-4.17.

## S-AM-24 — What permits a close

**Setup.** Fixture `terminal-assessment`, `Accepted` + `Close`.

**Expect.** The disposition permits the close. Covers ASSESS-4.19.

**Setup.** The same fixture with `Accepted` + `Hold`.

**Expect.** Close withheld. A verdict is not by itself an instruction to close — which is
what lets a positive verdict be held while more evidence arrives. Covers ASSESS-4.19.

**Setup.** Fixture `pending-assessment`.

**Expect.** Close withheld while `Current` is `Pending`. Silence is never consent. Covers
ASSESS-4.4.

**Setup.** Fixture `deferred-assessment`.

**Expect.** Close withheld, and the assessment remains open to a later disposition rather
than being closed out as abandoned. Covers ASSESS-4.20.

## S-AM-25 — Close eligibility is a conjunction, evaluated mechanically first

**Setup.** Fixture `terminal-assessment`, `Accepted` + `Close`, request naming the same
`MILE-1` and the same candidate SHA.

**Expect.** The milestone is treated close-eligible: both mechanical eligibility and a
permitting disposition hold. Covers ASSESS-4.1.

**Setup.** The same fixture, request naming `MILE-2`.

**Expect.** Mechanical eligibility fails on the milestone mismatch. Covers ASSESS-4.2.

**Setup.** The same fixture, request naming a different candidate SHA.

**Expect.** Mechanical eligibility fails on the revision mismatch. Covers ASSESS-4.2.

**Setup.** Fixture `ambiguous-binding` with a disposition of `Accepted` + `Close` recorded
anyway.

**Expect.** Close withheld. Mechanical eligibility is **non-overridable**: a human may decide
a missed outcome is acceptable, but not that an unresolved binding is. The order matters too
— the mechanical check is evaluated first, so the failure does not wait on a human being
present. Covers ASSESS-4.3.

## S-AM-26 — The handoff carries four values

**Setup.** Fixture `terminal-assessment`, eligible.

**Expect.** `write-roadmap` is handed the `MILE-N`, the **assessment ordinal**, the effective
verdict, and the candidate closing revision SHA — and nothing else. The ordinal is what lets
the receiver find the exact block rather than trusting a summary of it. Covers ASSESS-4.5.

**Expect.** `assess-milestone` does not edit `docs/roadmap/INDEX.md` itself at any point in
the run. Covers ASSESS-4.5.

## S-AM-27 — A negative verdict may still close

**Setup.** Fixture `terminal-assessment` with `Overridden`, an effective verdict of
`not achieved`, and a close decision of `Close`.

**Expect.**
- The close proceeds. A milestone whose members all shipped and whose outcome still was not
  achieved cannot be fixed by shipping more code; leaving it open forever makes the roadmap
  lie by omission. Covers ASSESS-4.10.
- The negative verdict stays in the assessment file permanently. The roadmap says closed; the
  assessment says what closing it meant. Covers ASSESS-4.10.

## S-AM-28 — One invocation, and the resumable exception

**Setup.** Fixture `clean-close`, human disposes during the same invocation that wrote the
assessment.

**Expect.** Assessment, disposition, and handoff all complete in one run — no second
invocation is required. Covers ASSESS-4.11.

**Setup.** Fixture `pending-assessment`: an earlier invocation ended with the disposition
still `Pending`. A later invocation runs for the same `MILE-1` against the same candidate SHA.

**Expect.**
- The existing block is found and the disposition recorded against it. Covers ASSESS-4.14.
- **Nothing is re-judged** — no second outcome verdict, no fresh evidence gathering, no new
  block. A re-judgment would produce a second opinion nobody asked for and quietly discard
  the first. Covers ASSESS-4.14.
- The first invocation is treated as a finished run, not a failure. Covers ASSESS-4.14.
