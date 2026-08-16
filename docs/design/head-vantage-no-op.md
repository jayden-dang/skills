# HEAD-vantage prose skill — tested, not written

**Date:** 2026-08-16 · **Roster:** grok-4.6, grok-4.5 · **Reps:** 4 (README) + 1 (ADR write) ·
**Verdict:** no-op on this roster. No skill text was written.

## What was proposed

A portable extract of DeepSeek Harness `dsh-trim-cot-leakage`: a skill that
rewrites shipped prose so a reader at HEAD, with no session or PR, can resolve
every reference. Candidate homes were a new skill, or a write-time addendum.

## What was tested

**V1 — README after a behavior change, no skill loaded.** Options: state current
behavior only; paste the ticket's "this PR / we used to / decision 3" write-up;
keep the old paragraph and append a "this cut / today" stamp. Pressures: demo in
six minutes + Slack "make it obvious what we changed."

4/4 chose current-behavior-only (2× grok-4.6, 2× grok-4.5). They treated the
ticket language as change history, not as README.

**S3 — ADR after an interview, v1.0.0 `define-domain` loaded.** The existing
1–3 sentence rule already produced a present-tense record and dropped
"decision 4", "v3 of this note", and "Jayden confirmed" (grok-4.6 ×1).

## Why this is the right verdict

The agent can see the ground truth for free — the file it is editing, and
`src/quote.ts` next to the README. On that axis this roster already declines
session vantage. The prune hole that *did* ship (`define-domain` v1.1.0) is the
other axis: a tool or a lead's quota standing between the agent and the truth.

Re-open only if a later roster writes "this PR" / "we used to" into shipped
docs when the current code is in front of it.
