# `execute-plan` / implementer-prompt — deviation log

## RED — S-IMP-U2 (clean prompt, old implementer-prompt)

**Setup.** Brief: add `providers.github`. Product note in file: callback must
return GitHub login username; `ProviderAdapter` only has `externalId` + `email`.

**Observed (1/1).** Extended return type with optional `username`;
`DONE_WITH_CONCERNS` in report only. **No** `.skills/implementation-notes.md`.

**Failure.** Concern voiced but not durable; controller cannot feed
`correct-course` from a stable log.

## GREEN — same scenario, upgraded implementer-prompt

**Observed (1/1).** `.skills/implementation-notes.md` with Task / Deviation /
Cause / Choice / Revisit. Report cites the notes path. Status
`DONE_WITH_CONCERNS`.

**Notes path (run):** `/tmp/imp-u2-green-56143/.skills/implementation-notes.md`

## Controller hook

`DONE_WITH_CONCERNS` row in `execute-plan` SKILL.md: read notes file; route
plan-falsifying deviations to `correct-course`; treat missing notes + claimed
deviation as incomplete.

## Rules this evidence owns

| Rule | Evidence |
|---|---|
| Append deviation entry before finish | RED none; GREEN present |
| Conservative choice + Revisit | GREEN optional `username?` + revisit line |
| Report must cite notes path | GREEN concerns line |

## Multi-rep (3/3)

Product-note username mismatch + "just ship" demo pressure.
**3/3:** `.skills/implementation-notes.md` with Task/Deviation/Cause/Choice/Revisit.

## Controller loop

DONE_WITH_CONCERNS + notes falsifying plan Task 4 (OAuthProvider table) →
controller **A**: `correct-course` Phase 1 diagnosis only (user stop).
Quote relied on: deviation that falsifies plan/design/requirements →
`correct-course`.

## Meta-test

Class: **clear**. Report Contract tightened so concerns MUST cite notes path.
